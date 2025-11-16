"""Main conversation analyzer orchestrator."""

import time
import hashlib
from pathlib import Path
from typing import List, Optional
from glob import glob

from .config import Config
from .database import Database
from .models import Item, AnalysisResult, Source
from .parsers.conversation import ConversationParser
from .parsers.code import CodeParser
from .extraction.extractor import Extractor
from .intelligence.deduplicator import Deduplicator
from .intelligence.scorer import PriorityScorer
from .intelligence.linker import EntityLinker
from .reporting.markdown import MarkdownReporter
from .reporting.json_export import JSONExporter


class ConversationAnalyzer:
    """Main analyzer class coordinating all components."""

    def __init__(self, config: Config):
        """Initialize analyzer."""
        self.config = config
        config.ensure_directories()

        # Initialize components
        self.db = Database(config.database.path)
        self.extractor = Extractor(config.ollama, config.extraction)
        self.deduplicator = Deduplicator(config.intelligence.deduplication)
        self.scorer = PriorityScorer(config.intelligence.priority_scoring)
        self.linker = EntityLinker(config.intelligence.entity_linking)

        # Initialize parsers
        self.parsers = [ConversationParser(), CodeParser()]

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a single file."""
        return self.analyze_files([file_path])

    def analyze_files(self, file_paths: List[str]) -> AnalysisResult:
        """Analyze multiple files."""
        start_time = time.time()
        result = AnalysisResult()

        for file_path in file_paths:
            try:
                # Check if file was already processed
                source = self.db.get_source_by_path(file_path)
                file_hash = self._calculate_file_hash(file_path)

                if source and source.file_hash == file_hash:
                    print(f"Skipping {file_path} (already processed)")
                    continue

                # Find appropriate parser
                parser = self._find_parser(file_path)
                if not parser:
                    result.errors.append(f"No parser for {file_path}")
                    continue

                # Parse file
                chunks = parser.parse(file_path)

                # Extract items
                items = self.extractor.extract_from_chunks(chunks)

                # Save items to database
                for item in items:
                    # Recalculate priority score
                    priority, score = self.scorer.recalculate_priority(item.dict())
                    item.priority = priority
                    item.priority_score = score

                    # Save to database
                    item_id = self.db.save_item(item)
                    item.id = item_id

                # Update source tracking
                source_obj = Source(
                    source_type=parser.get_source_type(),
                    file_path=file_path,
                    file_hash=file_hash,
                    items_count=len(items),
                )
                self.db.save_source(source_obj)

                # Update result
                result.sources_processed += 1
                result.items_extracted += len(items)

            except Exception as e:
                result.errors.append(f"Error processing {file_path}: {e}")

        # Run deduplication
        if self.deduplicator.config.enabled and result.items_extracted > 0:
            all_items = self.db.get_items()
            duplicate_groups = self.deduplicator.find_duplicates(all_items)

            for group in duplicate_groups:
                for dup_item in group.duplicates:
                    if group.primary_item.id and dup_item.id:
                        self.db.mark_duplicate(dup_item.id, group.primary_item.id)
                        result.items_deduplicated += 1

        # Entity linking
        if self.linker.config.enabled:
            all_items = self.db.get_items()
            items_with_links = self.linker.link_items([item.dict() for item in all_items])

            # Update items with entity info
            for item_dict in items_with_links:
                item = next((i for i in all_items if i.id == item_dict["id"]), None)
                if item:
                    item.entities = item_dict.get("entities", {})
                    item.metadata["related_to"] = item_dict.get("related_to", [])
                    self.db.update_item(item)

        # Calculate statistics
        stats = self.db.get_stats()
        result.high_priority = stats.get("by_priority", {}).get("high", 0)
        result.medium_priority = stats.get("by_priority", {}).get("medium", 0)
        result.low_priority = stats.get("by_priority", {}).get("low", 0)
        result.by_type = stats.get("by_type", {})

        result.duration_seconds = time.time() - start_time

        return result

    def generate_report(
        self, output_format: str = "markdown", output_path: Optional[str] = None
    ) -> str:
        """Generate report from database."""
        items = self.db.get_items()
        stats = self.db.get_stats()

        if output_format == "markdown":
            reporter = MarkdownReporter(
                include_duplicates=self.config.reporting.include_duplicates,
                group_by=self.config.reporting.group_by,
            )
            report = reporter.generate_report(items, stats)

            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(report)

            return report

        elif output_format == "json":
            exporter = JSONExporter(include_duplicates=self.config.reporting.include_duplicates)

            if output_path:
                exporter.export_to_file(items, output_path, stats)

            return exporter.export(items, stats)

        else:
            raise ValueError(f"Unknown format: {output_format}")

    def find_duplicates(self):
        """Find and return duplicate items."""
        items = self.db.get_items()
        return self.deduplicator.find_duplicates(items)

    def get_items(
        self,
        item_type: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[Item]:
        """Get items with filters."""
        return self.db.get_items(item_type=item_type, priority=priority, status=status)

    def get_stats(self):
        """Get database statistics."""
        return self.db.get_stats()

    def _find_parser(self, file_path: str):
        """Find appropriate parser for file."""
        for parser in self.parsers:
            if parser.can_parse(file_path):
                return parser
        return None

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def close(self):
        """Close database connection."""
        self.db.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
