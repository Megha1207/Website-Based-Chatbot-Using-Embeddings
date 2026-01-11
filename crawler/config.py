# config.py

from pathlib import Path

MAX_DEPTH = 1
REQUEST_TIMEOUT = 10

USER_AGENT = "Website-Chatbot-Crawler/1.0"

MAX_PAGES = 10

MIN_TEXT_LENGTH = 200
MAX_TEXT_LENGTH = 120000   # truncate very long pages

REQUEST_TIMEOUT = 10

HEADERS = {
    "User-Agent": USER_AGENT
}

# ❌ Wikipedia/system-style filters (generic + reusable)
EXCLUDE_KEYWORDS = [
    "Special:", "Help:", "Wikipedia:", "Portal:", "File:", "Category:",
    "Main_Page", "Talk:", "User:", "Template:",
    "action=edit", "action=history", "action=info", "printable=yes",
    "oldid=", "diff=", "curid=",
    "(disambiguation)"
]

# Only allow clean article URLs

ALLOW_SUBDOMAIN = False
REQUIRE_WIKI_ARTICLE = True



# Project root (AI WEBSITE CHATBOT)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Embedding pipeline data directory
EMBEDDING_DATA_DIR = PROJECT_ROOT / "embedding_pipeline" / "data"
EMBEDDING_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Crawl output path (used by Phase 2 automatically)
CRAWL_OUTPUT_PATH = EMBEDDING_DATA_DIR / "crawl_output.json"