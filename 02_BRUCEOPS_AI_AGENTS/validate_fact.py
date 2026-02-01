"""
validate_fact.py - Semantic Memory Write Policy Enforcement
Truth Hierarchy: Canon > Observed > Hypothesis
Every fact MUST have evidence. No freestanding facts allowed.
"""

from typing import Dict, List, Optional
from datetime import datetime


def validate_fact_creation(
    content: str,
    truth_level: str,
    evidence_event_ids: List[str] = None,
    cites_chunk_id: str = None,
    confirmation_criteria: str = None
) -> Dict:
    """
    Validate fact against Semantic Memory Write Policy.
    Returns {"valid": bool, "reason": str}
    """
    
    # Rule 1: Valid truth levels only
    valid_levels = {"Canon", "Observed", "Hypothesis"}
    if truth_level not in valid_levels:
        return {
            "valid": False,
            "reason": f"Invalid truth_level '{truth_level}'. Must be one of: {valid_levels}"
        }
    
    # Rule 2: Content required
    if not content or len(content.strip()) < 3:
        return {
            "valid": False,
            "reason": "Content is empty or too short"
        }
    
    # Rule 3: Canon facts MUST cite a chunk
    if truth_level == "Canon":
        if not cites_chunk_id:
            return {
                "valid": False,
                "reason": "Canon facts MUST have [:CITES]->(:Chunk) relationship. No chunk_id provided."
            }
        # Additional: Verify chunk exists (would need DB check)
        return {"valid": True, "reason": "Canon fact validated"}
    
    # Rule 4: Observed facts MUST have evidence events
    if truth_level == "Observed":
        if not evidence_event_ids or len(evidence_event_ids) == 0:
            return {
                "valid": False,
                "reason": "Observed facts MUST have [:EVIDENCED_BY]->(:Event) relationships. No events provided."
            }
        return {"valid": True, "reason": "Observed fact validated"}
    
    # Rule 5: Hypothesis facts MUST have evidence AND should have confirmation criteria
    if truth_level == "Hypothesis":
        if not evidence_event_ids or len(evidence_event_ids) == 0:
            return {
                "valid": False,
                "reason": "Hypothesis facts MUST have [:EVIDENCED_BY]->(:Event) relationships. No events provided."
            }
        # Warning only for missing confirmation criteria
        if not confirmation_criteria:
            return {
                "valid": True,
                "reason": "Hypothesis validated (warning: no confirmation criteria provided)"
            }
        return {"valid": True, "reason": "Hypothesis fact validated"}
    
    return {"valid": False, "reason": "Unknown validation error"}


def validate_promotion(
    from_level: str,
    to_level: str,
    user_override: bool = False
) -> Dict:
    """
    Validate truth level promotion.
    Promotions from lower to higher require explicit user override.
    """
    hierarchy = {"Hypothesis": 0, "Observed": 1, "Canon": 2}
    
    if from_level not in hierarchy or to_level not in hierarchy:
        return {"valid": False, "reason": "Invalid truth levels"}
    
    from_rank = hierarchy[from_level]
    to_rank = hierarchy[to_level]
    
    # Demotion is always allowed
    if to_rank < from_rank:
        return {"valid": True, "reason": "Demotion allowed"}
    
    # Same level is a no-op
    if to_rank == from_rank:
        return {"valid": True, "reason": "Same level"}
    
    # Promotion requires user override
    if to_rank > from_rank:
        if user_override:
            return {"valid": True, "reason": "Promotion approved by user override"}
        else:
            return {
                "valid": False,
                "reason": f"Promotion from {from_level} to {to_level} requires explicit user override"
            }


def check_conflict(existing_content: str, new_content: str, threshold: float = 0.8) -> Dict:
    """
    Check if new fact conflicts with existing fact.
    Simple substring check - could be enhanced with embeddings.
    """
    # Normalize
    existing_lower = existing_content.lower().strip()
    new_lower = new_content.lower().strip()
    
    # Direct contradiction patterns
    contradiction_pairs = [
        ("is", "is not"),
        ("does", "does not"),
        ("can", "cannot"),
        ("will", "will not"),
        ("true", "false"),
        ("yes", "no"),
    ]
    
    for pos, neg in contradiction_pairs:
        if pos in existing_lower and neg in new_lower:
            return {
                "conflict": True,
                "reason": f"Potential contradiction detected: '{pos}' vs '{neg}'"
            }
        if neg in existing_lower and pos in new_lower:
            return {
                "conflict": True,
                "reason": f"Potential contradiction detected: '{neg}' vs '{pos}'"
            }
    
    # High similarity might indicate duplicate or conflict
    common_words = set(existing_lower.split()) & set(new_lower.split())
    max_words = max(len(existing_lower.split()), len(new_lower.split()))
    similarity = len(common_words) / max_words if max_words > 0 else 0
    
    if similarity > threshold:
        return {
            "conflict": True,
            "reason": f"High similarity ({similarity:.2f}) - possible duplicate or conflict"
        }
    
    return {"conflict": False, "reason": "No conflict detected"}


def format_policy_violation(violation: Dict, fact_data: Dict) -> str:
    """Format a human-readable policy violation log entry"""
    timestamp = datetime.now().isoformat()
    return f"""[POLICY VIOLATION] {timestamp}
  Reason: {violation['reason']}
  Attempted fact: {fact_data.get('content', 'N/A')[:100]}...
  Truth level: {fact_data.get('truth_level', 'N/A')}
  Evidence provided: {fact_data.get('evidence_event_ids', [])}
  Chunk citation: {fact_data.get('cites_chunk_id', 'None')}
"""


# ============================================
# BRUCE RESPONSE VALIDATION
# ============================================

def validate_bruce_statement(statement: str, available_facts: List[Dict]) -> Dict:
    """
    Validate that Bruce's statement is grounded in available facts.
    Returns grounding status and source.
    """
    statement_lower = statement.lower()
    
    # Check against Canon first (highest authority)
    for fact in available_facts:
        if fact.get("truth_level") == "Canon":
            if any(word in statement_lower for word in fact.get("content", "").lower().split()):
                return {
                    "grounded": True,
                    "source": "Canon",
                    "fact_id": fact.get("fact_id")
                }
    
    # Check Observed
    for fact in available_facts:
        if fact.get("truth_level") == "Observed":
            if any(word in statement_lower for word in fact.get("content", "").lower().split()):
                return {
                    "grounded": True,
                    "source": "Observed",
                    "fact_id": fact.get("fact_id")
                }
    
    # Check Hypothesis
    for fact in available_facts:
        if fact.get("truth_level") == "Hypothesis":
            if any(word in statement_lower for word in fact.get("content", "").lower().split()):
                return {
                    "grounded": True,
                    "source": "Hypothesis",
                    "fact_id": fact.get("fact_id"),
                    "warning": "Statement based on Hypothesis - should be labeled as uncertain"
                }
    
    # Not grounded in any fact
    return {
        "grounded": False,
        "source": None,
        "warning": "Statement not grounded in any known fact - Bruce should acknowledge uncertainty"
    }


if __name__ == "__main__":
    # Test validation
    print("Testing Canon validation...")
    result = validate_fact_creation(
        content="In the beginning God created the heaven and the earth.",
        truth_level="Canon",
        cites_chunk_id=None  # Missing!
    )
    print(f"  Result: {result}")
    
    print("\nTesting Observed validation...")
    result = validate_fact_creation(
        content="Player prefers fire magic.",
        truth_level="Observed",
        evidence_event_ids=["event-123"]
    )
    print(f"  Result: {result}")
    
    print("\nTesting Hypothesis validation...")
    result = validate_fact_creation(
        content="Player might be interested in crafting.",
        truth_level="Hypothesis",
        evidence_event_ids=[]  # Missing!
    )
    print(f"  Result: {result}")
