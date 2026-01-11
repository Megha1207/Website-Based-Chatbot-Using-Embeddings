# embedding_pipeline/src/retriever.py

from embedding_pipeline.src.embedder import Embedder
from embedding_pipeline.src.vectordb import VectorDB
from embedding_pipeline.config import TOP_K
from embedding_pipeline.src.site_id import website_id

class Retriever:
    def __init__(self, website_url: str):
        self.site_id = website_id(website_url)
        self.embedder = Embedder()

        self.db = VectorDB(
            persist_dir=f"embedding_pipeline/vector_store/{self.site_id}"
        )

    def retrieve(self, question: str):
        query_embedding = self.embedder.embed([question])[0].tolist()
        return self.db.search(query_embedding, top_k=TOP_K)
