"""Unit tests for database operations."""

import pytest
from conversation_analyzer.models import Item, Relationship, Source


class TestDatabase:
    """Test database operations."""

    def test_save_and_get_item(self, temp_db, sample_item):
        """Test saving and retrieving an item."""
        # Save item
        item_id = temp_db.save_item(sample_item)
        assert item_id > 0

        # Retrieve item
        retrieved = temp_db.get_item(item_id)
        assert retrieved is not None
        assert retrieved.description == sample_item.description
        assert retrieved.type == sample_item.type

    def test_get_nonexistent_item(self, temp_db):
        """Test getting an item that doesn't exist."""
        item = temp_db.get_item(9999)
        assert item is None

    def test_get_items_with_filters(self, temp_db, sample_items):
        """Test getting items with filters."""
        # Save multiple items
        for item in sample_items:
            temp_db.save_item(item)

        # Get all items
        all_items = temp_db.get_items()
        assert len(all_items) == 3

        # Filter by type
        bugs = temp_db.get_items(item_type="BUG")
        assert len(bugs) == 1
        assert bugs[0].type == "BUG"

        # Filter by priority
        high_priority = temp_db.get_items(priority="high")
        assert len(high_priority) == 1

        # Filter by status
        open_items = temp_db.get_items(status="open")
        assert len(open_items) == 3

    def test_update_item(self, temp_db, sample_item):
        """Test updating an item."""
        # Save item
        item_id = temp_db.save_item(sample_item)
        sample_item.id = item_id

        # Update item
        sample_item.priority = "low"
        sample_item.status = "completed"
        temp_db.update_item(sample_item)

        # Verify update
        updated = temp_db.get_item(item_id)
        assert updated.priority == "low"
        assert updated.status == "completed"

    def test_mark_duplicate(self, temp_db, sample_items):
        """Test marking an item as duplicate."""
        # Save items
        id1 = temp_db.save_item(sample_items[0])
        id2 = temp_db.save_item(sample_items[1])

        # Mark as duplicate
        temp_db.mark_duplicate(id2, id1)

        # Verify
        item = temp_db.get_item(id2)
        assert item.is_duplicate == True
        assert item.duplicate_of == id1
        assert item.status == "duplicate"

    def test_save_relationship(self, temp_db, sample_items):
        """Test saving relationships."""
        # Save items
        id1 = temp_db.save_item(sample_items[0])
        id2 = temp_db.save_item(sample_items[1])

        # Create relationship
        rel = Relationship(
            item_id_1=id1,
            item_id_2=id2,
            relationship_type="related",
            similarity_score=0.75,
        )

        rel_id = temp_db.save_relationship(rel)
        assert rel_id > 0

    def test_get_related_items(self, temp_db, sample_items):
        """Test getting related items."""
        # Save items
        id1 = temp_db.save_item(sample_items[0])
        id2 = temp_db.save_item(sample_items[1])

        # Create relationship
        rel = Relationship(
            item_id_1=id1,
            item_id_2=id2,
            relationship_type="related",
        )
        temp_db.save_relationship(rel)

        # Get related items
        related = temp_db.get_related_items(id1)
        assert len(related) == 1
        assert related[0][0] == id2  # related_id

    def test_save_source(self, temp_db):
        """Test saving source information."""
        source = Source(
            source_type="conversation",
            file_path="test.md",
            file_hash="abc123",
            items_count=5,
        )

        source_id = temp_db.save_source(source)
        assert source_id > 0

        # Retrieve source
        retrieved = temp_db.get_source_by_path("test.md")
        assert retrieved is not None
        assert retrieved.file_hash == "abc123"
        assert retrieved.items_count == 5

    def test_get_stats(self, temp_db, sample_items):
        """Test getting database statistics."""
        # Save items
        for item in sample_items:
            temp_db.save_item(item)

        stats = temp_db.get_stats()

        assert stats["total_items"] == 3
        assert stats["by_type"]["BUG"] == 1
        assert stats["by_type"]["TODO"] == 1
        assert stats["by_type"]["FEATURE"] == 1

    def test_save_and_get_embedding(self, temp_db, sample_item):
        """Test saving and retrieving embeddings."""
        import numpy as np

        # Save item
        item_id = temp_db.save_item(sample_item)

        # Create mock embedding
        embedding = np.array([0.1, 0.2, 0.3, 0.4])

        # Save embedding
        temp_db.save_embedding(item_id, embedding, "test-model")

        # Retrieve embedding
        retrieved = temp_db.get_embedding(item_id, "test-model")

        assert retrieved is not None
        assert np.array_equal(retrieved, embedding)

    def test_get_all_embeddings(self, temp_db, sample_items):
        """Test getting all embeddings for a model."""
        import numpy as np

        # Save items and embeddings
        for i, item in enumerate(sample_items):
            item_id = temp_db.save_item(item)
            embedding = np.array([i * 0.1, i * 0.2])
            temp_db.save_embedding(item_id, embedding, "test-model")

        # Get all embeddings
        embeddings = temp_db.get_all_embeddings("test-model")

        assert len(embeddings) == 3
        assert all(isinstance(emb[1], np.ndarray) for emb in embeddings)
