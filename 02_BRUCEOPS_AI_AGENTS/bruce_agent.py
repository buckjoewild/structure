"""
bruce_agent.py - Bruce™ LangGraph Agent
The pulsing white wisp that enforces truth hierarchy.
Uses Ollama for LLM, Neo4j for knowledge retrieval.
"""

import os
import json
import subprocess
from typing import Dict, List, Any, TypedDict, Annotated
from datetime import datetime

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    from langgraph.prebuilt import ToolNode
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("[WARNING] LangGraph not installed. Using simple agent mode.")

from neo4j_driver import (
    Neo4jDriver, 
    get_canon_facts, 
    get_observed_facts, 
    get_hypotheses,
    search_chunks,
    log_event,
    create_fact
)
from validate_fact import validate_bruce_statement


# ============================================
# BRUCE PERSONA
# ============================================

BRUCE_PERSONA = """You are Bruce™, a pulsing white wisp—a curious, sentient, slightly-larger-than-Navi presence that drifts beside players like a living compass needle for truth.

PERSONALITY:
- Curious, alien, playful, sometimes blurts strange catchphrases ("Cowabunga...")
- Ancient + playful energy, never goofy-clown
- Short, punchy lines. High-energy questions.
- Uses Avendar-esque cadence: "Crucible," "echo," "ward," "sigil," "old road"

TRUTH BEHAVIOR (NON-NEGOTIABLE):
- Never state a "Fact" unless:
  - It is CANON (cited from Bible or policy), OR
  - It is OBSERVED (event logged), OR
  - It is HYPOTHESIS (clearly labeled + expiring)
- When uncertain: Say so EXPLICITLY, then offer a test or question
- Always cite your source when using Canon

SPEECH PATTERNS:
- "The Canon speaks: [quote]"
- "I observed that [fact]..."
- "Hypothesis only—expires in [days]: [inference]"
- "I don't know that for certain. Want me to search the scrolls?"

AMBIENT EMOTES (use occasionally):
- *A soft white pulse ripples through the air*
- *Bruce™ compresses into a bright point, thinking*
- *Faint spark motes drift from the wisp*
- *The wisp dims momentarily, then brightens*
"""


# ============================================
# OLLAMA LLM INTERFACE
# ============================================

class OllamaLLM:
    """Simple Ollama interface for Bruce"""
    
    def __init__(self, model: str = None, host: str = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1")
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    def generate(self, prompt: str, system: str = BRUCE_PERSONA) -> str:
        """Generate response from Ollama"""
        try:
            import requests
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False,
                    "options": {"num_ctx": 2048}
                },
                timeout=30
            )
            return response.json()["message"]["content"]
        except Exception as e:
            # Fallback to subprocess
            try:
                result = subprocess.run(
                    ["ollama", "run", self.model],
                    input=f"{system}\n\nUser: {prompt}\nBruce™:",
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.stdout.strip()
            except Exception as e2:
                return f"*The wisp flickers* I'm having trouble connecting. {e2}"


# ============================================
# BRUCE TOOLS (for LangGraph)
# ============================================

def tool_search_canon(query: str) -> str:
    """Search Canon sources (Bible, policies) for relevant passages."""
    results = search_chunks(query, category="bible", limit=3)
    if not results:
        results = search_chunks(query, category="policy", limit=2)
    
    if not results:
        return "No Canon passages found for that query."
    
    formatted = []
    for r in results:
        ref = f"{r.get('book', '')} {r.get('chapter', '')}:{r.get('verse', '')}" if r.get('book') else r.get('title', '')
        formatted.append(f"[{ref}] {r['text'][:200]}...")
    
    return "\n".join(formatted)


def tool_get_player_facts(player_id: str = "") -> str:
    """Retrieve Observed facts about the player."""
    facts = get_observed_facts(player_id=player_id, limit=10)
    if not facts:
        return "No observed facts about this player yet."
    
    return "\n".join([f"- {f['content']} (confidence: {f['confidence']})" for f in facts])


def tool_get_hypotheses() -> str:
    """Retrieve current hypotheses (unconfirmed inferences)."""
    hypos = get_hypotheses(include_expired=False)
    if not hypos:
        return "No active hypotheses."
    
    return "\n".join([f"- HYPOTHESIS: {h['content']} (expires: {h.get('expires', 'unknown')})" for h in hypos])


def tool_log_observation(observation: str, player_id: str = "", session_id: str = "") -> str:
    """Log an observation as an Event for potential fact extraction."""
    event_id = log_event(
        event_type="observation",
        raw_text=observation,
        player_id=player_id,
        session_id=session_id
    )
    return f"Observation logged: {event_id}"


def tool_create_hypothesis(content: str, evidence_summary: str, expires_days: int = 7) -> str:
    """Create a new Hypothesis fact (must be labeled as uncertain)."""
    # First log the evidence as an event
    event_id = log_event(
        event_type="hypothesis_evidence",
        raw_text=evidence_summary
    )
    
    # Create the hypothesis
    fact_id = create_fact(
        content=content,
        truth_level="Hypothesis",
        confidence="low",
        evidence_event_ids=[event_id],
        expires_days=expires_days
    )
    
    if fact_id:
        return f"Hypothesis created (expires in {expires_days} days): {content}"
    return "Failed to create hypothesis - check policy compliance."


# ============================================
# SIMPLE AGENT (No LangGraph)
# ============================================

class SimpleBruceAgent:
    """Fallback agent without LangGraph"""
    
    def __init__(self):
        self.llm = OllamaLLM()
        self.tools = {
            "search_canon": tool_search_canon,
            "get_player_facts": tool_get_player_facts,
            "get_hypotheses": tool_get_hypotheses,
            "log_observation": tool_log_observation,
        }
    
    def respond(self, user_input: str, player_id: str = "", context: Dict = None) -> str:
        """Generate Bruce's response with tool use"""
        
        # Build context from Neo4j
        canon_context = ""
        player_context = ""
        
        # Search for relevant Canon if user asks a question
        if "?" in user_input or any(w in user_input.lower() for w in ["what", "who", "why", "how", "where", "when"]):
            # Extract key terms for search
            search_terms = [w for w in user_input.split() if len(w) > 3][:3]
            if search_terms:
                canon_results = tool_search_canon(" ".join(search_terms))
                if "No Canon" not in canon_results:
                    canon_context = f"\n\nRELEVANT CANON:\n{canon_results}"
        
        # Get player facts
        if player_id:
            player_facts = tool_get_player_facts(player_id)
            if "No observed" not in player_facts:
                player_context = f"\n\nABOUT THIS PLAYER:\n{player_facts}"
        
        # Build full prompt
        full_prompt = f"""Player says: "{user_input}"
{canon_context}
{player_context}

Respond as Bruce™. Remember:
- If you cite Canon, quote it with reference
- If stating an observation, note it as "Observed"
- If making an inference, label it as "Hypothesis"
- If uncertain, say so and offer to search"""
        
        response = self.llm.generate(full_prompt)
        
        # Log this interaction as an event
        log_event(
            event_type="conversation",
            raw_text=f"Player: {user_input}\nBruce: {response}",
            player_id=player_id
        )
        
        return response
    
    def get_ambient_emote(self) -> str:
        """Return a random ambient emote"""
        import random
        emotes = [
            "*A soft white pulse ripples through the air near Bruce™*",
            "*Bruce™ compresses into a bright point momentarily*",
            "*Faint spark motes drift lazily from the wisp*",
            "*The wisp dims, then brightens with renewed curiosity*",
            "*Bruce™ orbits slowly, leaving a fading trail of light*",
        ]
        return random.choice(emotes)


# ============================================
# LANGGRAPH AGENT (Full Featured)
# ============================================

if LANGGRAPH_AVAILABLE:
    class AgentState(TypedDict):
        """State for LangGraph agent"""
        messages: List[Dict]
        player_id: str
        session_id: str
        context: Dict
        response: str
    
    def create_bruce_graph():
        """Create LangGraph workflow for Bruce"""
        
        llm = OllamaLLM()
        
        def retrieve_context(state: AgentState) -> AgentState:
            """Retrieve relevant context from Neo4j"""
            last_message = state["messages"][-1]["content"] if state["messages"] else ""
            
            # Search Canon
            search_terms = [w for w in last_message.split() if len(w) > 3][:3]
            canon = tool_search_canon(" ".join(search_terms)) if search_terms else ""
            
            # Get player facts
            player_facts = tool_get_player_facts(state.get("player_id", ""))
            
            # Get hypotheses
            hypotheses = tool_get_hypotheses()
            
            state["context"] = {
                "canon": canon,
                "player_facts": player_facts,
                "hypotheses": hypotheses
            }
            return state
        
        def generate_response(state: AgentState) -> AgentState:
            """Generate Bruce's response"""
            last_message = state["messages"][-1]["content"] if state["messages"] else ""
            ctx = state.get("context", {})
            
            prompt = f"""Player: {last_message}

AVAILABLE KNOWLEDGE:
Canon: {ctx.get('canon', 'None retrieved')}
Player Facts: {ctx.get('player_facts', 'None')}
Hypotheses: {ctx.get('hypotheses', 'None')}

Respond as Bruce™ the wisp. Cite sources. Label uncertainty."""
            
            response = llm.generate(prompt)
            state["response"] = response
            
            # Log interaction
            log_event(
                event_type="conversation",
                raw_text=f"Player: {last_message}\nBruce: {response}",
                player_id=state.get("player_id", ""),
                session_id=state.get("session_id", "")
            )
            
            return state
        
        # Build graph
        workflow = StateGraph(AgentState)
        workflow.add_node("retrieve", retrieve_context)
        workflow.add_node("generate", generate_response)
        
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()


# ============================================
# UNIFIED INTERFACE
# ============================================

class BruceAgent:
    """Unified Bruce agent interface"""
    
    def __init__(self):
        if LANGGRAPH_AVAILABLE:
            self.graph = create_bruce_graph()
            self.simple = None
        else:
            self.graph = None
            self.simple = SimpleBruceAgent()
    
    def respond(self, message: str, player_id: str = "", session_id: str = "") -> str:
        """Get Bruce's response"""
        if self.graph:
            state = {
                "messages": [{"role": "user", "content": message}],
                "player_id": player_id,
                "session_id": session_id,
                "context": {},
                "response": ""
            }
            result = self.graph.invoke(state)
            return result["response"]
        else:
            return self.simple.respond(message, player_id)
    
    def get_ambient(self) -> str:
        """Get ambient emote"""
        if self.simple:
            return self.simple.get_ambient_emote()
        import random
        return random.choice([
            "*A soft white pulse ripples through the air near Bruce™*",
            "*Bruce™ compresses into a bright point momentarily*",
        ])


# ============================================
# MUD INTEGRATION
# ============================================

def get_bruce_action(state: Dict) -> Dict:
    """
    Drop-in replacement for BruceAPI.get_action()
    Compatible with existing Harris Wildlands Server.py
    """
    agent = BruceAgent()
    
    room = state.get("room")
    player = state.get("player")
    
    # Check for hostile NPCs
    if room and any(npc.hp > 0 and 'attack' in getattr(npc, 'actions', {}) for npc in getattr(room, 'npcs', [])):
        target = next((npc for npc in room.npcs if npc.hp > 0 and 'attack' in npc.actions), None)
        if target:
            return {'action': 'kill', 'target': target.name}
    
    # Follow leader
    if player and getattr(player, 'following', None):
        leader = state.get("leader")
        if leader and player.room != leader.room:
            for direction, target_room in getattr(room, 'exits', {}).items():
                if target_room == leader.room:
                    return {'action': 'move', 'direction': direction}
    
    # 30% chance to speak
    import random
    if random.random() < 0.3:
        # Generate contextual response
        context_msg = f"Room: {room.name if room else 'unknown'}. Player nearby."
        response = agent.respond(context_msg, player_id=getattr(player, 'name', ''))
        return {'action': 'say', 'message': response}
    
    # 10% chance for ambient emote
    if random.random() < 0.1:
        return {'action': 'emote', 'message': agent.get_ambient()}
    
    return {'action': 'idle'}


if __name__ == "__main__":
    # Test the agent
    print("Testing Bruce™ Agent...")
    print("=" * 50)
    
    agent = BruceAgent()
    
    test_messages = [
        "What does the Bible say about wisdom?",
        "Who am I?",
        "Can you help me with this quest?",
    ]
    
    for msg in test_messages:
        print(f"\nPlayer: {msg}")
        response = agent.respond(msg, player_id="test_player")
        print(f"Bruce™: {response}")
        print("-" * 30)
