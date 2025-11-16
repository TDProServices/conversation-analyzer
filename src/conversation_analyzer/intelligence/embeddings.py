"""Embedding generation for similarity calculations."""

from typing import List
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding generator."""
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        """Lazy load the model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError(
                    "sentence-transformers not installed. "
                    "Install with: pip install sentence-transformers"
                )
        return self._model

    def generate(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        return self.model.encode(text)

    def generate_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        return self.model.encode(texts)

    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings."""
        from sklearn.metrics.pairwise import cosine_similarity

        return float(cosine_similarity([embedding1], [embedding2])[0][0])

    def similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """Calculate similarity matrix for multiple embeddings."""
        from sklearn.metrics.pairwise import cosine_similarity

        return cosine_similarity(embeddings)
