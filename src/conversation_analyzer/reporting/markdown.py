"""Markdown report generation."""

from datetime import datetime
from typing import List, Dict, Any
from ..models import Item, AnalysisResult


class MarkdownReporter:
    """Generate Markdown reports from analyzed items."""

    def __init__(self, include_duplicates: bool = False, group_by: str = "type"):
        """Initialize reporter."""
        self.include_duplicates = include_duplicates
        self.group_by = group_by

    def generate_report(
        self, items: List[Item], stats: Dict[str, Any], result: AnalysisResult = None
    ) -> str:
        """Generate complete Markdown report."""
        sections = []

        # Header
        sections.append(self._generate_header())

        # Summary statistics
        sections.append(self._generate_summary(stats, result))

        # Filter items
        display_items = items if self.include_duplicates else [
            item for item in items if not item.is_duplicate
        ]

        # Grouped items
        if self.group_by == "type":
            sections.append(self._generate_by_type(display_items))
        elif self.group_by == "priority":
            sections.append(self._generate_by_priority(display_items))
        elif self.group_by == "source":
            sections.append(self._generate_by_source(display_items))

        return "\n\n".join(sections)

    def _generate_header(self) -> str:
        """Generate report header."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""# Conversation Analysis Report

**Generated:** {now}

---
"""

    def _generate_summary(self, stats: Dict[str, Any], result: AnalysisResult = None) -> str:
        """Generate summary statistics."""
        lines = ["## Summary\n"]

        total = stats.get("total_items", 0)
        lines.append(f"**Total Items:** {total}")

        if result:
            lines.append(f"**Sources Processed:** {result.sources_processed}")
            lines.append(f"**Items Extracted:** {result.items_extracted}")
            if result.items_deduplicated > 0:
                lines.append(f"**Duplicates Found:** {result.items_deduplicated}")
            lines.append(f"**Processing Time:** {result.duration_seconds:.2f}s")

        # By type
        by_type = stats.get("by_type", {})
        if by_type:
            lines.append("\n**By Type:**")
            for item_type, count in sorted(by_type.items()):
                lines.append(f"- {item_type}: {count}")

        # By priority
        by_priority = stats.get("by_priority", {})
        if by_priority:
            lines.append("\n**By Priority:**")
            for priority in ["high", "medium", "low"]:
                count = by_priority.get(priority, 0)
                if count > 0:
                    lines.append(f"- {priority.title()}: {count}")

        return "\n".join(lines)

    def _generate_by_type(self, items: List[Item]) -> str:
        """Generate items grouped by type."""
        sections = ["## Items by Type\n"]

        for item_type in ["BUG", "TODO", "FEATURE", "PROJECT"]:
            type_items = [item for item in items if item.type == item_type]
            if not type_items:
                continue

            sections.append(f"### {item_type}s ({len(type_items)})\n")

            for item in sorted(type_items, key=lambda x: x.priority_score, reverse=True):
                sections.append(self._format_item(item))

        return "\n".join(sections)

    def _generate_by_priority(self, items: List[Item]) -> str:
        """Generate items grouped by priority."""
        sections = ["## Items by Priority\n"]

        for priority in ["high", "medium", "low"]:
            priority_items = [item for item in items if item.priority == priority]
            if not priority_items:
                continue

            sections.append(f"### {priority.title()} Priority ({len(priority_items)})\n")

            for item in priority_items:
                sections.append(self._format_item(item))

        return "\n".join(sections)

    def _generate_by_source(self, items: List[Item]) -> str:
        """Generate items grouped by source file."""
        sections = ["## Items by Source\n"]

        # Group by source file
        by_source = {}
        for item in items:
            source = item.source_file
            if source not in by_source:
                by_source[source] = []
            by_source[source].append(item)

        # Generate sections
        for source, source_items in sorted(by_source.items()):
            sections.append(f"### {source} ({len(source_items)})\n")

            for item in sorted(source_items, key=lambda x: x.priority_score, reverse=True):
                sections.append(self._format_item(item))

        return "\n".join(sections)

    def _format_item(self, item: Item) -> str:
        """Format a single item."""
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        type_emoji = {"TODO": "✅", "BUG": "🐛", "FEATURE": "✨", "PROJECT": "📦"}

        lines = []
        lines.append(
            f"#### {type_emoji.get(item.type, '')} {priority_emoji.get(item.priority, '')} "
            f"{item.description}"
        )

        lines.append(f"- **Type:** {item.type}")
        lines.append(f"- **Priority:** {item.priority.title()} ({item.priority_score:.2f})")
        lines.append(f"- **Confidence:** {item.confidence:.2f}")
        lines.append(f"- **Source:** `{item.source_file}`")
        if item.source_line:
            lines.append(f"- **Line:** {item.source_line}")

        # Source context (quoted)
        if item.source_context:
            context = item.source_context[:200] + "..." if len(item.source_context) > 200 else item.source_context
            lines.append(f'- **Context:** "{context}"')

        # Tags
        if item.tags:
            tags_str = ", ".join(f"`{tag}`" for tag in item.tags)
            lines.append(f"- **Tags:** {tags_str}")

        # Related items
        if item.metadata.get("related_to"):
            related_count = len(item.metadata["related_to"])
            lines.append(f"- **Related Items:** {related_count}")

        lines.append("")  # Blank line between items

        return "\n".join(lines)
