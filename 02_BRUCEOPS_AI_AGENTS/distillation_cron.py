"""
distillation_cron.py - Event → Fact Distillation System
Runs periodically to extract structured facts from raw events.
Enforces truth hierarchy during extraction.
"""

import os
import schedule
import time
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from neo4j_driver import (
    Neo4jDriver,
    log_event,
    create_fact,
    expire_hypotheses
)


# ============================================
# OLLAMA DISTILLATION
# ============================================

def ollama_extract(events_text: str, extraction_type: str = "preference") -> List[Dict]:
    """
    Use Ollama to extract potential facts from events.
    Returns list of {content, truth_level, confidence, evidence}
    """
    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    prompts = {
        "preference": """Analyze these player interactions and extract any PREFERENCES stated or demonstrated.
Return JSON array of objects with: content, confidence (high/medium/low)
Only extract clear preferences, not assumptions.

Events:
{events}

Return ONLY valid JSON array, no explanation.""",

        "observation": """Analyze these events and extract FACTUAL OBSERVATIONS about what happened.
Return JSON array of objects with: content, confidence (high/medium/low)
Only extract things that definitely occurred.

Events:
{events}

Return ONLY valid JSON array, no explanation.""",

        "hypothesis": """Analyze these events and suggest possible HYPOTHESES about patterns or intentions.
Return JSON array of objects with: content, confidence (low/medium), confirmation_test
These are uncertain inferences that need testing.

Events:
{events}

Return ONLY valid JSON array, no explanation."""
    }
    
    prompt = prompts.get(extraction_type, prompts["observation"]).format(events=events_text)
    
    try:
        import requests
        response = requests.post(
            f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"num_ctx": 2048}
            },
            timeout=60
        )
        result = response.json()["message"]["content"]
        
        # Parse JSON from response
        import json
        import re
        # Find JSON array in response
        match = re.search(r'\[.*\]', result, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception as e:
        print(f"[Distillation Error] {e}")
        return []


# ============================================
# DISTILLATION JOBS
# ============================================

def get_recent_events(hours: int = 24, event_type: str = None) -> List[Dict]:
    """Fetch recent events from Neo4j"""
    db = Neo4jDriver()
    
    if event_type:
        query = """
        MATCH (e:Event)
        WHERE e.timestamp > datetime() - duration({hours: $hours})
        AND e.type = $event_type
        AND NOT exists((e)<-[:GENERATED]-(:Fact))
        RETURN e.event_id, e.type, e.raw_text, e.timestamp, e.player_id
        ORDER BY e.timestamp
        """
        params = {"hours": hours, "event_type": event_type}
    else:
        query = """
        MATCH (e:Event)
        WHERE e.timestamp > datetime() - duration({hours: $hours})
        AND NOT exists((e)<-[:GENERATED]-(:Fact))
        RETURN e.event_id, e.type, e.raw_text, e.timestamp, e.player_id
        ORDER BY e.timestamp
        """
        params = {"hours": hours}
    
    return db.run_query(query, params)


def mark_events_processed(event_ids: List[str], fact_id: str):
    """Link events to the fact they generated"""
    db = Neo4jDriver()
    for event_id in event_ids:
        query = """
        MATCH (f:Fact {fact_id: $fact_id})
        MATCH (e:Event {event_id: $event_id})
        CREATE (e)-[:GENERATED]->(f)
        """
        db.run_write(query, {"fact_id": fact_id, "event_id": event_id})


def run_micro_distillation():
    """
    Micro distillation - runs every 10-30 minutes.
    Extracts quick observations from recent conversations.
    """
    print(f"[{datetime.now()}] Running micro distillation...")
    
    # Get last 30 minutes of conversation events
    events = get_recent_events(hours=0.5, event_type="conversation")
    
    if not events:
        print("  No new events to process")
        return
    
    print(f"  Processing {len(events)} events")
    
    # Group by player
    player_events = {}
    for e in events:
        pid = e.get("player_id", "unknown")
        if pid not in player_events:
            player_events[pid] = []
        player_events[pid].append(e)
    
    facts_created = 0
    
    for player_id, pevents in player_events.items():
        events_text = "\n".join([e["raw_text"] for e in pevents])
        
        # Extract observations
        extractions = ollama_extract(events_text, "observation")
        
        for ext in extractions:
            if ext.get("confidence") in ["high", "medium"]:
                event_ids = [e["event_id"] for e in pevents]
                fact_id = create_fact(
                    content=ext["content"],
                    truth_level="Observed",
                    confidence=ext["confidence"],
                    evidence_event_ids=event_ids,
                    applies_to_profile=player_id if player_id != "unknown" else None
                )
                if fact_id:
                    mark_events_processed(event_ids, fact_id)
                    facts_created += 1
    
    print(f"  Created {facts_created} Observed facts")


def run_nightly_distillation():
    """
    Nightly distillation - runs once per day.
    Deep analysis for preferences and hypotheses.
    """
    print(f"[{datetime.now()}] Running nightly distillation...")
    
    # Get last 24 hours
    events = get_recent_events(hours=24)
    
    if not events:
        print("  No events to process")
        return
    
    print(f"  Processing {len(events)} events")
    
    events_text = "\n".join([f"[{e['type']}] {e['raw_text']}" for e in events[:50]])  # Limit for context
    
    # Extract preferences
    print("  Extracting preferences...")
    preferences = ollama_extract(events_text, "preference")
    for pref in preferences:
        event_ids = [e["event_id"] for e in events[:10]]  # Link to relevant events
        fact_id = create_fact(
            content=pref["content"],
            truth_level="Observed",
            confidence=pref.get("confidence", "medium"),
            evidence_event_ids=event_ids,
            tags=["preference"]
        )
        if fact_id:
            print(f"    Created preference: {pref['content'][:50]}...")
    
    # Extract hypotheses
    print("  Generating hypotheses...")
    hypotheses = ollama_extract(events_text, "hypothesis")
    for hypo in hypotheses:
        event_ids = [e["event_id"] for e in events[:10]]
        fact_id = create_fact(
            content=hypo["content"],
            truth_level="Hypothesis",
            confidence="low",
            evidence_event_ids=event_ids,
            expires_days=7,
            tags=["auto-generated"]
        )
        if fact_id:
            print(f"    Created hypothesis: {hypo['content'][:50]}...")
    
    # Expire old hypotheses
    print("  Expiring old hypotheses...")
    expired = expire_hypotheses()
    print(f"    Expired {expired} hypotheses")
    
    print("  Nightly distillation complete")


def run_weekly_reflection():
    """
    Weekly reflection - proposes patterns for user review.
    Does NOT auto-create Canon (user must approve).
    """
    print(f"[{datetime.now()}] Running weekly reflection...")
    
    db = Neo4jDriver()
    
    # Find confirmed hypotheses (high evidence)
    query = """
    MATCH (f:Fact {truth_level: "Hypothesis"})
    WHERE f.confidence = "high" OR size([(f)-[:EVIDENCED_BY]->(e) | e]) >= 3
    RETURN f.fact_id, f.content, f.confidence, 
           size([(f)-[:EVIDENCED_BY]->(e) | e]) AS evidence_count
    """
    candidates = db.run_query(query)
    
    if candidates:
        print("  Candidates for promotion to Observed:")
        for c in candidates:
            print(f"    - {c['content'][:60]}... (evidence: {c['evidence_count']})")
        print("  [Note: Promotion requires user approval via 'promote_fact' command]")
    
    # Find potential conflicts
    query = """
    MATCH (f1:Fact), (f2:Fact)
    WHERE f1.fact_id < f2.fact_id
    AND f1.content CONTAINS f2.content OR f2.content CONTAINS f1.content
    RETURN f1.fact_id, f1.content, f2.fact_id, f2.content
    LIMIT 5
    """
    conflicts = db.run_query(query)
    
    if conflicts:
        print("  Potential conflicts detected:")
        for c in conflicts:
            print(f"    - '{c['f1.content'][:30]}...' vs '{c['f2.content'][:30]}...'")
    
    print("  Weekly reflection complete")


# ============================================
# SCHEDULER
# ============================================

def start_scheduler():
    """Start the distillation scheduler"""
    print("Starting distillation scheduler...")
    print("  - Micro distillation: every 15 minutes")
    print("  - Nightly distillation: 3:00 AM")
    print("  - Weekly reflection: Sundays 4:00 AM")
    
    schedule.every(15).minutes.do(run_micro_distillation)
    schedule.every().day.at("03:00").do(run_nightly_distillation)
    schedule.every().sunday.at("04:00").do(run_weekly_reflection)
    
    # Also run on startup
    run_micro_distillation()
    
    while True:
        schedule.run_pending()
        time.sleep(60)


# ============================================
# CLI
# ============================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "micro":
            run_micro_distillation()
        elif cmd == "nightly":
            run_nightly_distillation()
        elif cmd == "weekly":
            run_weekly_reflection()
        elif cmd == "expire":
            expired = expire_hypotheses()
            print(f"Expired {expired} hypotheses")
        elif cmd == "daemon":
            start_scheduler()
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python distillation_cron.py [micro|nightly|weekly|expire|daemon]")
    else:
        print("Distillation System - Harris Wildlands")
        print("Usage: python distillation_cron.py [micro|nightly|weekly|expire|daemon]")
        print("\nCommands:")
        print("  micro   - Run micro distillation (recent events)")
        print("  nightly - Run full nightly distillation")
        print("  weekly  - Run weekly reflection")
        print("  expire  - Expire old hypotheses")
        print("  daemon  - Start scheduler daemon")
