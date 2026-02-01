"""
neo4j_driver.py - Connection wrapper for Harris Wildlands Neo4j
Handles connection, queries, and truth hierarchy enforcement
"""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()


class Neo4jDriver:
    """Singleton Neo4j connection manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_driver()
        return cls._instance
    
    def _init_driver(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "")
        self.database = os.getenv("NEO4J_DATABASE", "neo4j")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def close(self):
        if self.driver:
            self.driver.close()
    
    def run_query(self, query: str, params: dict = None) -> List[Dict]:
        """Execute Cypher query and return results"""
        with self.driver.session(database=self.database) as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    
    def run_write(self, query: str, params: dict = None) -> Any:
        """Execute write transaction"""
        with self.driver.session(database=self.database) as session:
            return session.execute_write(lambda tx: tx.run(query, params or {}).consume())


# ============================================
# SOURCE & CHUNK OPERATIONS
# ============================================

def create_source(title: str, category: str, edition: str = "", publisher: str = "") -> str:
    """Create a Canon source node"""
    db = Neo4jDriver()
    source_id = str(uuid.uuid4())
    query = """
    CREATE (s:Source {
        source_id: $source_id,
        title: $title,
        category: $category,
        edition: $edition,
        publisher: $publisher,
        date_added: datetime()
    })
    RETURN s.source_id
    """
    db.run_write(query, {
        "source_id": source_id,
        "title": title,
        "category": category,
        "edition": edition,
        "publisher": publisher
    })
    return source_id


def create_chunk(source_id: str, text: str, chunk_index: int, book: str = "", chapter: int = 0, verse: int = 0) -> str:
    """Create a chunk linked to source"""
    db = Neo4jDriver()
    chunk_id = str(uuid.uuid4())
    query = """
    MATCH (s:Source {source_id: $source_id})
    CREATE (c:Chunk {
        chunk_id: $chunk_id,
        source_id: $source_id,
        text: $text,
        chunk_index: $chunk_index,
        book: $book,
        chapter: $chapter,
        verse: $verse
    })
    CREATE (s)-[:HAS_CHUNK {order: $chunk_index}]->(c)
    RETURN c.chunk_id
    """
    db.run_write(query, {
        "source_id": source_id,
        "chunk_id": chunk_id,
        "text": text,
        "chunk_index": chunk_index,
        "book": book,
        "chapter": chapter,
        "verse": verse
    })
    return chunk_id


# ============================================
# FACT OPERATIONS (Truth Hierarchy Enforced)
# ============================================

def create_fact(
    content: str,
    truth_level: str,
    confidence: str = "medium",
    evidence_event_ids: List[str] = None,
    cites_chunk_id: str = None,
    applies_to_profile: str = None,
    expires_days: int = 7,
    tags: List[str] = None
) -> Optional[str]:
    """
    Create a fact with policy enforcement.
    truth_level: "Canon" | "Observed" | "Hypothesis"
    Returns fact_id or None if validation fails.
    """
    from validate_fact import validate_fact_creation
    
    # Validate before write
    validation = validate_fact_creation(
        content=content,
        truth_level=truth_level,
        evidence_event_ids=evidence_event_ids,
        cites_chunk_id=cites_chunk_id
    )
    
    if not validation["valid"]:
        print(f"[POLICY VIOLATION] {validation['reason']}")
        return None
    
    db = Neo4jDriver()
    fact_id = str(uuid.uuid4())
    
    # Base fact creation
    query = """
    CREATE (f:Fact {
        fact_id: $fact_id,
        content: $content,
        truth_level: $truth_level,
        confidence: $confidence,
        created_at: datetime(),
        last_confirmed: datetime(),
        tags: $tags
    })
    """
    params = {
        "fact_id": fact_id,
        "content": content,
        "truth_level": truth_level,
        "confidence": confidence,
        "tags": tags or []
    }
    
    # Add expiry for Hypothesis
    if truth_level == "Hypothesis":
        query = query.replace(
            "tags: $tags",
            "tags: $tags, expires_at: datetime() + duration({days: $expires_days})"
        )
        params["expires_days"] = expires_days
    
    db.run_write(query, params)
    
    # Link to Canon chunk
    if cites_chunk_id and truth_level == "Canon":
        link_query = """
        MATCH (f:Fact {fact_id: $fact_id})
        MATCH (c:Chunk {chunk_id: $chunk_id})
        CREATE (f)-[:CITES {chunk_ref: $chunk_id}]->(c)
        """
        db.run_write(link_query, {"fact_id": fact_id, "chunk_id": cites_chunk_id})
    
    # Link to evidence events
    if evidence_event_ids:
        for event_id in evidence_event_ids:
            link_query = """
            MATCH (f:Fact {fact_id: $fact_id})
            MATCH (e:Event {event_id: $event_id})
            CREATE (f)-[:EVIDENCED_BY]->(e)
            """
            db.run_write(link_query, {"fact_id": fact_id, "event_id": event_id})
    
    # Link to profile
    if applies_to_profile:
        link_query = """
        MATCH (f:Fact {fact_id: $fact_id})
        MATCH (p:Profile {profile_id: $profile_id})
        CREATE (f)-[:APPLIES_TO]->(p)
        """
        db.run_write(link_query, {"fact_id": fact_id, "profile_id": applies_to_profile})
    
    return fact_id


# ============================================
# EVENT OPERATIONS
# ============================================

def log_event(
    event_type: str,
    raw_text: str,
    session_id: str = "",
    player_id: str = "",
    room_id: str = ""
) -> str:
    """Log an event (append-only)"""
    db = Neo4jDriver()
    event_id = str(uuid.uuid4())
    query = """
    CREATE (e:Event {
        event_id: $event_id,
        type: $event_type,
        raw_text: $raw_text,
        timestamp: datetime(),
        session_id: $session_id,
        player_id: $player_id,
        room_id: $room_id
    })
    RETURN e.event_id
    """
    db.run_write(query, {
        "event_id": event_id,
        "event_type": event_type,
        "raw_text": raw_text,
        "session_id": session_id,
        "player_id": player_id,
        "room_id": room_id
    })
    return event_id


# ============================================
# QUERY HELPERS
# ============================================

def get_canon_facts(topic: str = "", limit: int = 10) -> List[Dict]:
    """Retrieve Canon facts with citations"""
    db = Neo4jDriver()
    query = """
    MATCH (f:Fact {truth_level: "Canon"})-[:CITES]->(c:Chunk)<-[:HAS_CHUNK]-(s:Source)
    WHERE f.content CONTAINS $topic OR $topic = ""
    RETURN f.content AS content, c.text AS citation, s.title AS source, 
           c.book AS book, c.chapter AS chapter, c.verse AS verse
    LIMIT $limit
    """
    return db.run_query(query, {"topic": topic, "limit": limit})


def get_observed_facts(player_id: str = "", limit: int = 20) -> List[Dict]:
    """Retrieve Observed facts ordered by recency"""
    db = Neo4jDriver()
    query = """
    MATCH (f:Fact {truth_level: "Observed"})-[:EVIDENCED_BY]->(e:Event)
    WHERE $player_id = "" OR e.player_id = $player_id
    RETURN f.content AS content, f.confidence AS confidence, 
           e.timestamp AS last_evidence, f.tags AS tags
    ORDER BY e.timestamp DESC
    LIMIT $limit
    """
    return db.run_query(query, {"player_id": player_id, "limit": limit})


def get_hypotheses(include_expired: bool = False) -> List[Dict]:
    """Retrieve Hypothesis facts"""
    db = Neo4jDriver()
    if include_expired:
        query = """
        MATCH (f:Fact {truth_level: "Hypothesis"})
        RETURN f.content AS content, f.confidence AS confidence,
               f.expires_at AS expires, f.tags AS tags
        """
    else:
        query = """
        MATCH (f:Fact {truth_level: "Hypothesis"})
        WHERE f.expires_at > datetime()
        RETURN f.content AS content, f.confidence AS confidence,
               f.expires_at AS expires, f.tags AS tags
        """
    return db.run_query(query)


def search_chunks(search_text: str, category: str = "", limit: int = 5) -> List[Dict]:
    """Search chunks by text content"""
    db = Neo4jDriver()
    query = """
    MATCH (c:Chunk)<-[:HAS_CHUNK]-(s:Source)
    WHERE c.text CONTAINS $search_text
    AND ($category = "" OR s.category = $category)
    RETURN c.chunk_id, c.text, s.title, c.book, c.chapter, c.verse
    LIMIT $limit
    """
    return db.run_query(query, {"search_text": search_text, "category": category, "limit": limit})


# ============================================
# MAINTENANCE
# ============================================

def expire_hypotheses() -> int:
    """Delete expired hypothesis facts"""
    db = Neo4jDriver()
    query = """
    MATCH (f:Fact {truth_level: "Hypothesis"})
    WHERE f.expires_at < datetime()
    DETACH DELETE f
    RETURN count(f) AS deleted
    """
    result = db.run_query(query)
    return result[0]["deleted"] if result else 0


def init_schema():
    """Initialize database schema from cypher file"""
    db = Neo4jDriver()
    schema_path = os.path.join(os.path.dirname(__file__), "create_schema.cypher")
    with open(schema_path) as f:
        statements = f.read().split(";")
    for stmt in statements:
        stmt = stmt.strip()
        if stmt and not stmt.startswith("//"):
            try:
                db.run_write(stmt)
            except Exception as e:
                if "already exists" not in str(e).lower():
                    print(f"Schema error: {e}")


if __name__ == "__main__":
    print("Initializing Neo4j schema...")
    init_schema()
    print("Schema initialized.")
