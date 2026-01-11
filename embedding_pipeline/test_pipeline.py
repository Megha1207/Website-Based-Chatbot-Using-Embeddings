import json
from pathlib import Path

from src.processor import process_pages
from src.embedder import Embedder
from src.vectordb import VectorDB
from embedding_pipeline.src.site_id import website_id

# --------------------------------------------------
# Resolve paths safely (works from anywhere)
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CRAWL_PATH = DATA_DIR / "crawl_output.json"
PROCESSED_PATH = DATA_DIR / "processed_chunks.json"

if not CRAWL_PATH.exists():
    raise FileNotFoundError(f"Crawl output not found at {CRAWL_PATH}")

# --------------------------------------------------
# Load crawl output
# --------------------------------------------------

with open(CRAWL_PATH, "r", encoding="utf-8") as f:
    pages = json.load(f)

print(f"[INFO] Pages loaded: {len(pages)}")

# --------------------------------------------------
# Compute website ID (CRITICAL FIX)
# --------------------------------------------------

if not pages:
    print(
        "[WARN] No valid content extracted. "
        "Website may be empty, blocked, or unsuitable for crawling."
    )
    exit(0)


site_id_value = website_id(pages[0]["url"])


# --------------------------------------------------
# Process & chunk
# --------------------------------------------------

chunks = process_pages(pages)
print(f"[INFO] Chunks created: {len(chunks)}")

# Save processed chunks
with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)
if not chunks:
    print("[WARN] No chunks created after processing. Skipping embedding.")
    exit(0)

# --------------------------------------------------
# Embed
# --------------------------------------------------

embedder = Embedder()
texts = [c["text"] for c in chunks]
embeddings = embedder.embed(texts)

embedding_vectors = [e.tolist() for e in embeddings]

# --------------------------------------------------
# Store in Vector DB (PER-WEBSITE)
# --------------------------------------------------

db = VectorDB(
    persist_dir=f"embedding_pipeline/vector_store/{site_id_value}"
)

db.add(
    documents=texts,
    embeddings=embedding_vectors,
    metadatas=[{
        "url": c["source_url"],
        "title": c["title"],
        "depth": c["depth"]
    } for c in chunks],
    ids=[c["chunk_id"] for c in chunks]
)

print("Phase 2 complete: embeddings stored.")
