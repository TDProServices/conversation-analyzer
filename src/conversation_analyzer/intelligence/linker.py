"""Entity linking to find related items."""

import re
from typing import List, Dict, Set, Any
from ..config import EntityLinkingConfig


class EntityLinker:
    """Extract entities and link related items."""

    def __init__(self, config: EntityLinkingConfig):
        """Initialize entity linker."""
        self.config = config

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text.

        Returns:
            Dict with entity types as keys and lists of entities as values
        """
        entities = {
            "files": self._extract_file_paths(text),
            "functions": self._extract_function_names(text),
            "components": self._extract_component_names(text),
            "keywords": self._extract_keywords(text),
        }

        # Filter out empty lists
        return {k: v for k, v in entities.items() if v}

    def _extract_file_paths(self, text: str) -> List[str]:
        """Extract file paths from text."""
        # Match file paths with extensions
        pattern = r'\b[\w/\-\.]+\.\w+\b'
        matches = re.findall(pattern, text)

        # Filter to likely file paths (contain / or . in middle)
        files = [m for m in matches if '/' in m or m.count('.') > 1]
        return list(set(files))

    def _extract_function_names(self, text: str) -> List[str]:
        """Extract function names from text."""
        # Match function calls: word()
        pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\(\)'
        matches = re.findall(pattern, text)
        return list(set(matches))

    def _extract_component_names(self, text: str) -> List[str]:
        """Extract component names from text."""
        # Match PascalCase or Component/Class names
        pattern = r'\b([A-Z][a-zA-Z0-9]+(?:Component|Service|Controller|Manager|Handler|Class))\b'
        matches = re.findall(pattern, text)
        return list(set(matches))

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        # Common technical keywords to look for
        keywords_to_find = [
            "login", "auth", "authentication", "password", "security",
            "payment", "checkout", "user", "admin", "api", "database",
            "cache", "session", "token", "email", "notification",
            "validation", "sanitization", "encryption", "logging"
        ]

        text_lower = text.lower()
        found = [kw for kw in keywords_to_find if kw in text_lower]
        return found

    def link_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add entity information and related_to links to items."""
        if not self.config.enabled:
            return items

        # Build entity index
        entity_map = {}  # entity -> [item_ids]

        for item in items:
            item_id = item.get("id")
            if not item_id:
                continue

            # Extract entities from description and source_context
            text = f"{item.get('description', '')} {item.get('source_context', '')}"
            entities = self.extract_entities(text)

            # Store entities on item
            item["entities"] = entities

            # Build entity map
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    key = f"{entity_type}:{entity}"
                    if key not in entity_map:
                        entity_map[key] = []
                    entity_map[key].append(item_id)

        # Link related items
        for item in items:
            item_id = item.get("id")
            if not item_id:
                continue

            related = set()
            entities = item.get("entities", {})

            # Find items sharing entities
            for entity_type, entity_list in entities.items():
                for entity in entity_list:
                    key = f"{entity_type}:{entity}"
                    related_ids = entity_map.get(key, [])
                    related.update(related_ids)

            # Remove self
            related.discard(item_id)

            # Filter by minimum shared entities if needed
            if self.config.min_entities_shared > 1:
                # Count shared entities with each related item
                filtered_related = []
                for related_id in related:
                    related_item = next((i for i in items if i.get("id") == related_id), None)
                    if related_item:
                        shared_count = self._count_shared_entities(
                            entities, related_item.get("entities", {})
                        )
                        if shared_count >= self.config.min_entities_shared:
                            filtered_related.append(related_id)
                related = set(filtered_related)

            item["related_to"] = list(related)

        return items

    def _count_shared_entities(
        self, entities1: Dict[str, List[str]], entities2: Dict[str, List[str]]
    ) -> int:
        """Count number of shared entities between two entity dicts."""
        count = 0
        for entity_type in entities1:
            if entity_type in entities2:
                set1 = set(entities1[entity_type])
                set2 = set(entities2[entity_type])
                count += len(set1 & set2)
        return count
