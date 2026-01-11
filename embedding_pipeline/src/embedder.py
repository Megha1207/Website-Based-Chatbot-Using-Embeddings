from sentence_transformers import SentenceTransformer
from embedding_pipeline.config import EMBEDDING_MODEL

class Embedder:
    _model = None  # class-level cache

    def __init__(self):
        if Embedder._model is None:
            Embedder._model = SentenceTransformer(
                EMBEDDING_MODEL,
                device="cpu"
            )
        self.model = Embedder._model

    def embed(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )
