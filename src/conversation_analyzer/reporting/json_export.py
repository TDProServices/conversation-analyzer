"""JSON export functionality."""

import json
from datetime import datetime
from typing import List, Dict, Any
from ..models import Item, AnalysisResult


class JSONExporter:
    """Export items and analysis results to JSON."""

    def __init__(self, include_duplicates: bool = False):
        """Initialize exporter."""
        self.include_duplicates = include_duplicates

    def export(
        self, items: List[Item], stats: Dict[str, Any] = None, result: AnalysisResult = None
    ) -> str:
        """Export to JSON string."""
        data = self._build_export_data(items, stats, result)
        return json.dumps(data, indent=2, default=str)

    def export_to_file(
        self,
        items: List[Item],
        file_path: str,
        stats: Dict[str, Any] = None,
        result: AnalysisResult = None,
    ):
        """Export to JSON file."""
        data = self._build_export_data(items, stats, result)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

    def _build_export_data(
        self, items: List[Item], stats: Dict[str, Any] = None, result: AnalysisResult = None
    ) -> Dict[str, Any]:
        """Build export data structure."""
        # Filter items
        display_items = (
            items
            if self.include_duplicates
            else [item for item in items if not item.is_duplicate]
        )

        data = {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(display_items),
            "items": [self._item_to_dict(item) for item in display_items],
        }

        # Add statistics
        if stats:
            data["statistics"] = stats

        # Add analysis result
        if result:
            data["analysis_result"] = {
                "sources_processed": result.sources_processed,
                "items_extracted": result.items_extracted,
                "items_deduplicated": result.items_deduplicated,
                "high_priority": result.high_priority,
                "medium_priority": result.medium_priority,
                "low_priority": result.low_priority,
                "by_type": result.by_type,
                "errors": result.errors,
                "duration_seconds": result.duration_seconds,
            }

        return data

    def _item_to_dict(self, item: Item) -> Dict[str, Any]:
        """Convert Item to dict for JSON serialization."""
        return {
            "id": item.id,
            "type": item.type,
            "description": item.description,
            "priority": item.priority,
            "priority_score": item.priority_score,
            "confidence": item.confidence,
            "source": {
                "type": item.source_type,
                "file": item.source_file,
                "line": item.source_line,
                "context": item.source_context,
            },
            "tags": item.tags,
            "entities": item.entities,
            "status": item.status,
            "is_duplicate": item.is_duplicate,
            "duplicate_of": item.duplicate_of,
            "related_to": item.metadata.get("related_to", []),
            "extracted_at": item.extracted_at.isoformat(),
            "created_at": item.created_at.isoformat(),
        }
