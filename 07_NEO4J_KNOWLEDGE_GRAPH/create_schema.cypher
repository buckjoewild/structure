// Harris Wildlands Reborn: Eternal Truth Chamber
// Neo4j Schema v1.0
// Run this ONCE to initialize your database

// ============================================
// CONSTRAINTS (Uniqueness + Existence)
// ============================================

CREATE CONSTRAINT source_id IF NOT EXISTS 
FOR (s:Source) REQUIRE s.source_id IS UNIQUE;

CREATE CONSTRAINT chunk_id IF NOT EXISTS 
FOR (c:Chunk) REQUIRE c.chunk_id IS UNIQUE;

CREATE CONSTRAINT fact_id IF NOT EXISTS 
FOR (f:Fact) REQUIRE f.fact_id IS UNIQUE;

CREATE CONSTRAINT event_id IF NOT EXISTS 
FOR (e:Event) REQUIRE e.event_id IS UNIQUE;

CREATE CONSTRAINT profile_id IF NOT EXISTS 
FOR (p:Profile) REQUIRE p.profile_id IS UNIQUE;

CREATE CONSTRAINT room_id IF NOT EXISTS 
FOR (r:Room) REQUIRE r.room_id IS UNIQUE;

CREATE CONSTRAINT npc_id IF NOT EXISTS 
FOR (n:NPC) REQUIRE n.npc_id IS UNIQUE;

// ============================================
// INDEXES (Query Performance)
// ============================================

CREATE INDEX source_category IF NOT EXISTS 
FOR (s:Source) ON (s.category);

CREATE INDEX fact_truth_level IF NOT EXISTS 
FOR (f:Fact) ON (f.truth_level);

CREATE INDEX fact_expires IF NOT EXISTS 
FOR (f:Fact) ON (f.expires_at);

CREATE INDEX event_timestamp IF NOT EXISTS 
FOR (e:Event) ON (e.timestamp);

CREATE INDEX event_type IF NOT EXISTS 
FOR (e:Event) ON (e.type);

CREATE INDEX chunk_source IF NOT EXISTS 
FOR (c:Chunk) ON (c.source_id);

// ============================================
// VECTOR INDEX (Semantic Search - Optional)
// Uncomment if using embeddings
// ============================================

// CREATE VECTOR INDEX chunk_embeddings IF NOT EXISTS
// FOR (c:Chunk) ON (c.embedding)
// OPTIONS { indexConfig: { 
//   `vector.dimensions`: 384,
//   `vector.similarity_function`: 'cosine' 
// }};

// ============================================
// SAMPLE CANON SOURCES (Categories)
// ============================================

// Bible sources will be created by ingest_canon.py
// Categories: "bible", "policy", "lore", "medical"

// ============================================
// RELATIONSHIP TYPES REFERENCE
// ============================================
// (:Source)-[:HAS_CHUNK {order: int}]->(:Chunk)
// (:Fact)-[:CITES {chunk_ref: str}]->(:Chunk)
// (:Fact)-[:EVIDENCED_BY]->(:Event)
// (:Fact)-[:SUPERSEDES]->(:Fact)
// (:Fact)-[:CONFLICTS_WITH]->(:Fact)
// (:Fact)-[:APPLIES_TO]->(:Profile)
// (:Event)-[:GENERATED]->(:Fact)
// (:Room)-[:EXIT {direction: str}]->(:Room)
// (:NPC)-[:LOCATED_IN]->(:Room)
// (:Profile)-[:CURRENT_ROOM]->(:Room)
