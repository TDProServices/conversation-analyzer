"""Deduplication using embeddings and fuzzy matching."""

from typing import List, Dict, Tuple, Any
import difflib

from ..config import DeduplicationConfig
from ..models import Item, DuplicateGroup
from .embeddings import EmbeddingGenerator


class Deduplicator:
    """Find and handle duplicate items."""

    def __init__(self, config: DeduplicationConfig):
        """Initialize deduplicator."""
        self.config = config
        if config.enabled:
            self.embedder = EmbeddingGenerator(config.embedding_model)
        else:
            self.embedder = None

    def find_duplicates(self, items: List[Item]) -> List[DuplicateGroup]:
        """Find duplicate groups among items."""
        if not self.config.enabled or len(items) < 2:
            return []

        # Generate embeddings for all items
        descriptions = [item.description for item in items]
        embeddings = self.embedder.generate_batch(descriptions)

        # Calculate similarity matrix
        similarity_matrix = self.embedder.similarity_matrix(embeddings)

        # Find duplicates
        duplicate_groups = []
        processed = set()

        for i in range(len(items)):
            if i in processed:
                continue

            duplicates = []
            scores = []

            for j in range(i + 1, len(items)):
                if j in processed:
                    continue

                similarity = similarity_matrix[i][j]

                if similarity >= self.config.similarity_threshold:
                    if not duplicates:  # First duplicate found
                        duplicates.append(items[j])
                        scores.append(similarity)
                    else:
                        duplicates.append(items[j])
                        scores.append(similarity)
                    processed.add(j)

            if duplicates:
                group = DuplicateGroup(
                    primary_item=items[i],
                    duplicates=duplicates,
                    similarity_scores=scores,
                )
                duplicate_groups.append(group)
                processed.add(i)

        return duplicate_groups

    def find_exact_duplicates(self, items: List[Item]) -> List[Tuple[Item, Item]]:
        """Find exact description matches."""
        duplicates = []
        seen = {}

        for item in items:
            desc_normalized = item.description.strip().lower()
            if desc_normalized in seen:
                duplicates.append((seen[desc_normalized], item))
            else:
                seen[desc_normalized] = item

        return duplicates

    def fuzzy_match(self, text1: str, text2: str, threshold: float = 0.9) -> float:
        """Calculate fuzzy string similarity ratio."""
        return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def find_fuzzy_duplicates(
        self, items: List[Item], threshold: float = 0.9
    ) -> List[Tuple[Item, Item, float]]:
        """Find fuzzy matches using string similarity."""
        duplicates = []

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                ratio = self.fuzzy_match(items[i].description, items[j].description)
                if ratio >= threshold:
                    duplicates.append((items[i], items[j], ratio))

        return duplicates

    def merge_duplicates(
        self, duplicate_groups: List[DuplicateGroup], keep: str = "highest_confidence"
    ) -> Dict[int, int]:
        """Determine which items to keep and which to mark as duplicates.

        Args:
            duplicate_groups: List of duplicate groups
            keep: Strategy for choosing primary item
                  - "highest_confidence": Keep item with highest confidence
                  - "first": Keep the first item
                  - "newest": Keep newest item

        Returns:
            Dict mapping duplicate_id -> primary_id
        """
        merge_map = {}

        for group in duplicate_groups:
            # Determine primary item
            if keep == "highest_confidence":
                all_items = [group.primary_item] + group.duplicates
                primary = max(all_items, key=lambda x: x.confidence)
            elif keep == "first":
                primary = group.primary_item
            elif keep == "newest":
                all_items = [group.primary_item] + group.duplicates
                primary = max(all_items, key=lambda x: x.created_at)
            else:
                primary = group.primary_item

            # Map all others to primary
            all_items = [group.primary_item] + group.duplicates
            for item in all_items:
                if item.id != primary.id and item.id is not None:
                    merge_map[item.id] = primary.id

        return merge_map
