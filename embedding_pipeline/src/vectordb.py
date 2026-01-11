import chromadb
from pathlib import Path
from embedding_pipeline.config import COLLECTION_NAME


class VectorDB:
    def __init__(self, persist_dir: str):
        """
        Each website gets its own vector store directory
        """
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        print("[VECTOR DB] Persist directory:", self.persist_dir)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

    def add(self, documents, embeddings, metadatas, ids):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query_embedding, top_k=5):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
