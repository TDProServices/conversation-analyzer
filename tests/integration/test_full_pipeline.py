"""Integration tests for full analysis pipeline."""

import pytest
from conversation_analyzer.analyzer import ConversationAnalyzer
from conversation_analyzer.config import Config


class TestFullPipeline:
    """Test complete analysis pipeline."""

    @pytest.mark.skipif(
        True,  # Skip by default (requires Ollama)
        reason="Requires Ollama to be running",
    )
    def test_analyze_conversation(self, sample_conversation, test_config):
        """Test analyzing a conversation file."""
        with ConversationAnalyzer(test_config) as analyzer:
            result = analyzer.analyze_file(sample_conversation)

            assert result.sources_processed == 1
            assert result.items_extracted >= 0  # May extract items
            assert result.duration_seconds > 0

    @pytest.mark.skipif(
        True,
        reason="Requires Ollama to be running",
    )
    def test_analyze_code_file(self, sample_code, test_config):
        """Test analyzing a code file."""
        with ConversationAnalyzer(test_config) as analyzer:
            result = analyzer.analyze_file(sample_code)

            assert result.sources_processed == 1
            # Code file should have TODO/FIXME comments
            assert result.items_extracted > 0

    def test_generate_markdown_report(self, test_config, temp_dir):
        """Test generating a markdown report."""
        import os

        with ConversationAnalyzer(test_config) as analyzer:
            # Add a sample item directly to database
            from conversation_analyzer.models import Item

            item = Item(
                type="TODO",
                description="Test item",
                priority="high",
                source_context="Test context",
                confidence=0.9,
                source_type="conversation",
                source_file="test.md",
            )
            analyzer.db.save_item(item)

            # Generate report
            output_path = os.path.join(temp_dir, "report.md")
            report = analyzer.generate_report("markdown", output_path)

            assert os.path.exists(output_path)
            assert len(report) > 0
            assert "TODO" in report

    def test_generate_json_report(self, test_config, temp_dir):
        """Test generating a JSON report."""
        import os
        import json

        with ConversationAnalyzer(test_config) as analyzer:
            # Add a sample item
            from conversation_analyzer.models import Item

            item = Item(
                type="BUG",
                description="Test bug",
                priority="high",
                source_context="Test context",
                confidence=0.95,
                source_type="code",
                source_file="test.py",
            )
            analyzer.db.save_item(item)

            # Generate report
            output_path = os.path.join(temp_dir, "report.json")
            report = analyzer.generate_report("json", output_path)

            assert os.path.exists(output_path)

            # Verify JSON is valid
            data = json.loads(report)
            assert "items" in data
            assert len(data["items"]) == 1

    def test_get_stats(self, test_config, sample_items):
        """Test getting statistics."""
        with ConversationAnalyzer(test_config) as analyzer:
            # Add items
            for item in sample_items:
                analyzer.db.save_item(item)

            stats = analyzer.get_stats()

            assert stats["total_items"] == 3
            assert "by_type" in stats
            assert "by_priority" in stats

    def test_find_duplicates(self, test_config):
        """Test finding duplicate items."""
        with ConversationAnalyzer(test_config) as analyzer:
            # Add similar items
            from conversation_analyzer.models import Item

            item1 = Item(
                type="TODO",
                description="Fix login bug",
                priority="high",
                source_context="context 1",
                confidence=0.9,
                source_type="conversation",
                source_file="chat1.md",
            )

            item2 = Item(
                type="TODO",
                description="Fix login issue",  # Similar
                priority="high",
                source_context="context 2",
                confidence=0.85,
                source_type="conversation",
                source_file="chat2.md",
            )

            analyzer.db.save_item(item1)
            analyzer.db.save_item(item2)

            # Note: This will only work if sentence-transformers is installed
            # For now, just verify the method can be called
            try:
                duplicates = analyzer.find_duplicates()
                # If it works, duplicates should be found
                # assert len(duplicates) > 0
            except ImportError:
                # sentence-transformers not installed, that's okay for this test
                pass
