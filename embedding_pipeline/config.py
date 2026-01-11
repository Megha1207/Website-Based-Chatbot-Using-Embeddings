CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "website_docs"
TOP_K = 4
DISTANCE_THRESHOLD = 0.45


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DB_DIR = str(BASE_DIR / "vector_store")
COLLECTION_NAME = "website_docs"


