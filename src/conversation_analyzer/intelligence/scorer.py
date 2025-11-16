"""Priority scoring for items."""

from typing import Dict, Any
from ..config import PriorityScoringConfig


class PriorityScorer:
    """Calculate priority scores for items."""

    def __init__(self, config: PriorityScoringConfig):
        """Initialize priority scorer."""
        self.config = config

    def calculate_score(self, item: Dict[str, Any], context: Dict[str, Any] = None) -> float:
        """Calculate priority score for an item.

        Args:
            item: Item dict with description, type, etc.
            context: Additional context (mention_count, etc.)

        Returns:
            Priority score between 0.0 and 1.0
        """
        if context is None:
            context = {}

        score = self.config.base_score
        description_lower = item.get("description", "").lower()
        source_context_lower = item.get("source_context", "").lower()
        full_text = f"{description_lower} {source_context_lower}"

        # Check urgency keywords
        for keyword in self.config.urgency_keywords:
            if keyword.lower() in full_text:
                score += 0.2
                break  # Only count once

        # Check impact keywords
        for keyword in self.config.impact_keywords:
            if keyword.lower() in full_text:
                score += 0.15
                break  # Only count once

        # Boost for explicit high priority
        if item.get("priority") == "high":
            score += 0.3
        elif item.get("priority") == "medium":
            score += 0.1

        # Boost for BUG type (bugs are typically important)
        if item.get("type") == "BUG":
            score += 0.15

        # Boost for security-related items
        security_keywords = ["security", "vulnerability", "exploit", "injection", "xss"]
        if any(keyword in full_text for keyword in security_keywords):
            score += 0.2

        # Boost if mentioned multiple times
        mention_count = context.get("mention_count", 1)
        if mention_count > 1:
            score += 0.1 * min(mention_count - 1, 3)  # Max +0.3

        # Normalize to 0-1
        score = min(score, 1.0)
        score = max(score, 0.0)

        return round(score, 2)

    def get_priority(self, score: float) -> str:
        """Convert score to priority label."""
        if score >= 0.75:
            return "high"
        elif score >= 0.45:
            return "medium"
        else:
            return "low"

    def recalculate_priority(self, item: Dict[str, Any], context: Dict[str, Any] = None) -> tuple:
        """Recalculate priority and return (priority, score)."""
        score = self.calculate_score(item, context)
        priority = self.get_priority(score)
        return priority, score
