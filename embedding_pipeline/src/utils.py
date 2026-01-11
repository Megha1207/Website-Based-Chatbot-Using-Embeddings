import json
from pathlib import Path


def load_json(path: str):
    """Load JSON file safely."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: str):
    """Save JSON file safely."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def batch(iterable, size=32):
    """Yield batches for large embedding jobs."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]
