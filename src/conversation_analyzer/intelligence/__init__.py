"""Intelligence layer for deduplication, scoring, and linking."""

from .deduplicator import Deduplicator
from .scorer import PriorityScorer
from .linker import EntityLinker
from .embeddings import EmbeddingGenerator

__all__ = [
    "Deduplicator",
    "PriorityScorer",
    "EntityLinker",
    "EmbeddingGenerator",
]
