import re
import uuid
from embedding_pipeline.config import CHUNK_SIZE, CHUNK_OVERLAP

def split_into_chunks(text: str):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def process_pages(pages: list):
    processed = []

    for page in pages:
        chunks = split_into_chunks(page["text"])

        for idx, chunk in enumerate(chunks):
            processed.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk,
                "source_url": page["url"],
                "title": page["title"],
                "depth": page["depth"]
            })

    return processed
