"""
ingest_canon.py - Ingest Canon sources (Bible, policies) into Neo4j
Chunks text and creates :Source -> :Chunk relationships
"""

import os
import re
import uuid
from typing import List, Dict, Tuple
from docx import Document
from neo4j_driver import Neo4jDriver, create_source, create_chunk


def parse_bible_verse(text: str) -> List[Dict]:
    """
    Parse Bible text into book/chapter/verse chunks.
    Expected format: "Book Chapter:Verse Text" or numbered lines
    """
    verses = []
    
    # Pattern: "Genesis 1:1 In the beginning..." or "1:1 In the beginning..."
    verse_pattern = re.compile(
        r'^(?:(\d?\s?[A-Za-z]+)\s+)?(\d+):(\d+)\s+(.+)$',
        re.MULTILINE
    )
    
    current_book = "Unknown"
    
    for match in verse_pattern.finditer(text):
        book = match.group(1) or current_book
        if match.group(1):
            current_book = book.strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))
        content = match.group(4).strip()
        
        verses.append({
            "book": current_book,
            "chapter": chapter,
            "verse": verse,
            "text": content
        })
    
    return verses


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Simple text chunking for non-verse content (policies, lore).
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        # Try to break at sentence boundary
        if end < len(text):
            last_period = text.rfind('.', start, end)
            if last_period > start + chunk_size // 2:
                end = last_period + 1
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks


def read_docx(filepath: str) -> str:
    """Extract text from .docx file"""
    doc = Document(filepath)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def ingest_bible(filepath: str, version: str = "AKJV") -> Tuple[str, int]:
    """
    Ingest Bible docx into Neo4j as Canon source.
    Returns (source_id, chunk_count)
    """
    print(f"Ingesting Bible: {filepath} ({version})")
    
    # Create source node
    source_id = create_source(
        title=f"Holy Bible ({version})",
        category="bible",
        edition=version,
        publisher="Public Domain"
    )
    print(f"  Created source: {source_id}")
    
    # Read and parse
    text = read_docx(filepath)
    verses = parse_bible_verse(text)
    
    # If verse parsing fails, fall back to chunking
    if len(verses) < 100:
        print(f"  Verse parsing found only {len(verses)} verses, using chunking...")
        chunks = chunk_text(text, chunk_size=300)
        for i, chunk in enumerate(chunks):
            create_chunk(
                source_id=source_id,
                text=chunk,
                chunk_index=i,
                book="",
                chapter=0,
                verse=0
            )
        print(f"  Created {len(chunks)} chunks")
        return source_id, len(chunks)
    
    # Create verse chunks
    for i, v in enumerate(verses):
        create_chunk(
            source_id=source_id,
            text=v["text"],
            chunk_index=i,
            book=v["book"],
            chapter=v["chapter"],
            verse=v["verse"]
        )
        if i % 1000 == 0:
            print(f"  Progress: {i}/{len(verses)} verses...")
    
    print(f"  Created {len(verses)} verse chunks")
    return source_id, len(verses)


def ingest_policy(filepath: str, title: str) -> Tuple[str, int]:
    """
    Ingest policy document as Canon source.
    """
    print(f"Ingesting policy: {title}")
    
    source_id = create_source(
        title=title,
        category="policy",
        edition="v1.0",
        publisher="Harris Wildlands"
    )
    
    text = read_docx(filepath)
    chunks = chunk_text(text, chunk_size=400)
    
    for i, chunk in enumerate(chunks):
        create_chunk(
            source_id=source_id,
            text=chunk,
            chunk_index=i
        )
    
    print(f"  Created {len(chunks)} chunks")
    return source_id, len(chunks)


def ingest_lore_json(filepath: str, title: str = "Avendar Lore") -> Tuple[str, int]:
    """
    Ingest lore JSON as Canon source (Avendar wiki data).
    """
    import json
    
    print(f"Ingesting lore: {title}")
    
    source_id = create_source(
        title=title,
        category="lore",
        edition="Wiki Export",
        publisher="Avendar"
    )
    
    with open(filepath) as f:
        lore = json.load(f)
    
    chunk_count = 0
    for key, value in lore.items():
        if isinstance(value, str) and len(value) > 10:
            create_chunk(
                source_id=source_id,
                text=f"{key}: {value}",
                chunk_index=chunk_count,
                book=key
            )
            chunk_count += 1
    
    print(f"  Created {chunk_count} lore chunks")
    return source_id, chunk_count


def run_full_ingestion(uploads_dir: str = "/mnt/user-data/uploads"):
    """
    Run full Canon ingestion from uploads directory.
    """
    print("=" * 50)
    print("CANON INGESTION - Harris Wildlands")
    print("=" * 50)
    
    results = []
    
    # Bible files
    akjv_path = os.path.join(uploads_dir, "akjv.docx")
    if os.path.exists(akjv_path):
        results.append(("AKJV Bible", *ingest_bible(akjv_path, "AKJV")))
    
    asv_path = os.path.join(uploads_dir, "asv.docx")
    if os.path.exists(asv_path):
        results.append(("ASV Bible", *ingest_bible(asv_path, "ASV")))
    
    # Policy files
    policy_path = os.path.join(uploads_dir, "__Semantic_Memory_Write_Policy.docx")
    if os.path.exists(policy_path):
        results.append(("Write Policy", *ingest_policy(policy_path, "Semantic Memory Write Policy")))
    
    drift_path = os.path.join(uploads_dir, "DRIFT_DETECTION_SYSTEM__2_.docx")
    if os.path.exists(drift_path):
        results.append(("Drift Detection", *ingest_policy(drift_path, "Drift Detection System")))
    
    # Lore
    lore_path = os.path.join(uploads_dir, "avendar_wiki_lore.json")
    if os.path.exists(lore_path):
        results.append(("Avendar Lore", *ingest_lore_json(lore_path)))
    
    # Summary
    print("\n" + "=" * 50)
    print("INGESTION COMPLETE")
    print("=" * 50)
    total_chunks = 0
    for name, source_id, count in results:
        print(f"  {name}: {count} chunks")
        total_chunks += count
    print(f"\nTotal: {total_chunks} chunks ingested")
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        uploads_dir = sys.argv[1]
    else:
        uploads_dir = "/mnt/user-data/uploads"
    
    run_full_ingestion(uploads_dir)
