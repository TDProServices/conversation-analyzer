"""Unit tests for data models."""

import pytest
from datetime import datetime
from conversation_analyzer.models import (
    ExtractedItem,
    ExtractionResult,
    Item,
    Relationship,
    Source,
)


class TestExtractedItem:
    """Test ExtractedItem model."""

    def test_create_valid_item(self):
        """Test creating a valid extracted item."""
        item = ExtractedItem(
            type="TODO",
            description="Fix bug",
            priority="high",
            source_context="We need to fix this",
            confidence=0.9,
        )

        assert item.type == "TODO"
        assert item.priority == "high"
        assert item.confidence == 0.9

    def test_clean_whitespace(self):
        """Test that whitespace is cleaned."""
        item = ExtractedItem(
            type="BUG",
            description="Fix   multiple   spaces",
            priority="high",
            source_context="Context  with   spaces",
            confidence=0.8,
        )

        assert item.description == "Fix multiple spaces"
        assert item.source_context == "Context with spaces"

    def test_invalid_type(self):
        """Test that invalid type raises validation error."""
        with pytest.raises(Exception):  # Pydantic ValidationError
            ExtractedItem(
                type="INVALID",
                description="Test",
                priority="high",
                source_context="test",
                confidence=0.8,
            )

    def test_invalid_confidence(self):
        """Test that invalid confidence raises validation error."""
        with pytest.raises(Exception):
            ExtractedItem(
                type="TODO",
                description="Test",
                priority="high",
                source_context="test",
                confidence=1.5,  # > 1.0
            )


class TestExtractionResult:
    """Test ExtractionResult model."""

    def test_empty_result(self):
        """Test creating empty result."""
        result = ExtractionResult(items=[])
        assert len(result.items) == 0

    def test_result_with_items(self):
        """Test result with multiple items."""
        items = [
            ExtractedItem(
                type="TODO",
                description="Task 1",
                priority="high",
                source_context="ctx",
                confidence=0.9,
            ),
            ExtractedItem(
                type="BUG",
                description="Bug 1",
                priority="high",
                source_context="ctx",
                confidence=0.8,
            ),
        ]

        result = ExtractionResult(items=items)
        assert len(result.items) == 2


class TestItem:
    """Test Item model."""

    def test_create_item(self, sample_item):
        """Test creating an item."""
        assert sample_item.type == "TODO"
        assert sample_item.description == "Fix the login bug"
        assert sample_item.confidence == 0.9

    def test_to_dict(self, sample_item):
        """Test converting item to dict."""
        data = sample_item.to_dict()

        assert data["type"] == "TODO"
        assert data["description"] == "Fix the login bug"
        assert "extracted_at" in data

    def test_from_dict(self, sample_item):
        """Test creating item from dict."""
        data = sample_item.to_dict()
        item = Item.from_dict(data)

        assert item.type == sample_item.type
        assert item.description == sample_item.description

    def test_default_values(self):
        """Test default values are set."""
        item = Item(
            type="TODO",
            description="Test",
            priority="medium",
            source_context="test",
            confidence=0.8,
            source_type="conversation",
            source_file="test.md",
        )

        assert item.priority_score == 0.5  # Default
        assert item.status == "open"
        assert item.is_duplicate == False
        assert isinstance(item.created_at, datetime)


class TestRelationship:
    """Test Relationship model."""

    def test_create_relationship(self):
        """Test creating a relationship."""
        rel = Relationship(
            item_id_1=1,
            item_id_2=2,
            relationship_type="duplicate",
            similarity_score=0.95,
        )

        assert rel.item_id_1 == 1
        assert rel.item_id_2 == 2
        assert rel.similarity_score == 0.95


class TestSource:
    """Test Source model."""

    def test_create_source(self):
        """Test creating a source."""
        source = Source(
            source_type="conversation",
            file_path="test.md",
            file_hash="abc123",
            items_count=5,
        )

        assert source.source_type == "conversation"
        assert source.items_count == 5
        assert source.processing_status == "success"

    def test_to_dict(self):
        """Test converting source to dict."""
        source = Source(
            source_type="code",
            file_path="test.py",
            file_hash="def456",
        )

        data = source.to_dict()
        assert data["source_type"] == "code"
        assert data["file_path"] == "test.py"
