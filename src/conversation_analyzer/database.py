"""SQLite database operations for Conversation Analyzer."""

import sqlite3
import pickle
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

from .models import Item, Relationship, Source, ExtractionRun


class Database:
    """SQLite database manager."""

    SCHEMA_SQL = """
    -- Items: Core extracted items
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('TODO', 'BUG', 'FEATURE', 'PROJECT')),
        description TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('high', 'medium', 'low')),
        priority_score REAL NOT NULL DEFAULT 0.5,
        source_context TEXT,
        confidence REAL NOT NULL CHECK(confidence >= 0.0 AND confidence <= 1.0),
        status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'completed', 'duplicate')),

        -- Source tracking
        source_type TEXT NOT NULL CHECK(source_type IN ('conversation', 'code', 'document', 'git')),
        source_file TEXT NOT NULL,
        source_line INTEGER,
        extracted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        -- Metadata
        tags TEXT,
        entities TEXT,
        metadata TEXT,

        -- Deduplication
        is_duplicate BOOLEAN NOT NULL DEFAULT 0,
        duplicate_of INTEGER REFERENCES items(id),
        embedding_hash TEXT,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_items_type ON items(type);
    CREATE INDEX IF NOT EXISTS idx_items_priority ON items(priority);
    CREATE INDEX IF NOT EXISTS idx_items_status ON items(status);
    CREATE INDEX IF NOT EXISTS idx_items_source_file ON items(source_file);
    CREATE INDEX IF NOT EXISTS idx_items_extracted_at ON items(extracted_at);
    CREATE INDEX IF NOT EXISTS idx_items_embedding_hash ON items(embedding_hash);

    -- Embeddings: Store vector embeddings for similarity search
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
        embedding BLOB NOT NULL,
        model_name TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2',
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(item_id, model_name)
    );

    CREATE INDEX IF NOT EXISTS idx_embeddings_item_id ON embeddings(item_id);

    -- Relationships: Links between related items
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id_1 INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
        item_id_2 INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
        relationship_type TEXT NOT NULL CHECK(relationship_type IN ('duplicate', 'related', 'blocks', 'blocked_by', 'parent', 'child')),
        similarity_score REAL,
        reason TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(item_id_1, item_id_2, relationship_type)
    );

    CREATE INDEX IF NOT EXISTS idx_relationships_item1 ON relationships(item_id_1);
    CREATE INDEX IF NOT EXISTS idx_relationships_item2 ON relationships(item_id_2);

    -- Sources: Track source files and their processing status
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_type TEXT NOT NULL CHECK(source_type IN ('conversation', 'code', 'document', 'git')),
        file_path TEXT NOT NULL UNIQUE,
        file_hash TEXT NOT NULL,
        items_count INTEGER NOT NULL DEFAULT 0,
        last_processed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        processing_status TEXT NOT NULL DEFAULT 'success' CHECK(processing_status IN ('success', 'failed', 'partial')),
        error_message TEXT,
        metadata TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_sources_file_path ON sources(file_path);
    CREATE INDEX IF NOT EXISTS idx_sources_file_hash ON sources(file_hash);

    -- Extraction Runs: Track each extraction run for auditing
    CREATE TABLE IF NOT EXISTS extraction_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT NOT NULL,
        prompt_version TEXT NOT NULL,
        sources_processed INTEGER NOT NULL DEFAULT 0,
        items_extracted INTEGER NOT NULL DEFAULT 0,
        duration_seconds REAL,
        status TEXT NOT NULL CHECK(status IN ('running', 'completed', 'failed')),
        error_message TEXT,
        config TEXT,
        started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_extraction_runs_started_at ON extraction_runs(started_at);

    -- Trigger to update updated_at timestamp
    CREATE TRIGGER IF NOT EXISTS update_items_timestamp
    AFTER UPDATE ON items
    FOR EACH ROW
    BEGIN
        UPDATE items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """

    def __init__(self, db_path: str):
        """Initialize database connection."""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema."""
        self.conn.executescript(self.SCHEMA_SQL)
        self.conn.commit()

    def save_item(self, item: Item) -> int:
        """Save an item and return its ID."""
        data = item.to_dict()
        del data["id"]  # Auto-increment handles this

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" * len(data))
        sql = f"INSERT INTO items ({columns}) VALUES ({placeholders})"

        cursor = self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return cursor.lastrowid

    def get_item(self, item_id: int) -> Optional[Item]:
        """Get item by ID."""
        cursor = self.conn.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if row:
            return Item.from_dict(dict(row))
        return None

    def get_items(
        self,
        item_type: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        source_file: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Item]:
        """Get items with optional filters."""
        conditions = []
        params = []

        if item_type:
            conditions.append("type = ?")
            params.append(item_type)
        if priority:
            conditions.append("priority = ?")
            params.append(priority)
        if status:
            conditions.append("status = ?")
            params.append(status)
        if source_file:
            conditions.append("source_file = ?")
            params.append(source_file)

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        limit_clause = f"LIMIT {limit}" if limit else ""

        sql = f"SELECT * FROM items {where_clause} ORDER BY priority_score DESC, created_at DESC {limit_clause}"
        cursor = self.conn.execute(sql, params)

        return [Item.from_dict(dict(row)) for row in cursor.fetchall()]

    def update_item(self, item: Item):
        """Update an existing item."""
        if not item.id:
            raise ValueError("Item must have an ID to update")

        data = item.to_dict()
        item_id = data.pop("id")

        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        sql = f"UPDATE items SET {set_clause} WHERE id = ?"

        self.conn.execute(sql, list(data.values()) + [item_id])
        self.conn.commit()

    def mark_duplicate(self, item_id: int, duplicate_of: int):
        """Mark an item as duplicate of another."""
        self.conn.execute(
            """UPDATE items
               SET is_duplicate = 1, duplicate_of = ?, status = 'duplicate'
               WHERE id = ?""",
            (duplicate_of, item_id),
        )
        self.conn.commit()

    def save_relationship(self, relationship: Relationship) -> int:
        """Save a relationship between items."""
        sql = """INSERT INTO relationships
                 (item_id_1, item_id_2, relationship_type, similarity_score, reason)
                 VALUES (?, ?, ?, ?, ?)
                 ON CONFLICT (item_id_1, item_id_2, relationship_type) DO NOTHING"""

        cursor = self.conn.execute(
            sql,
            (
                relationship.item_id_1,
                relationship.item_id_2,
                relationship.relationship_type,
                relationship.similarity_score,
                relationship.reason,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_related_items(self, item_id: int) -> List[tuple]:
        """Get items related to the given item."""
        sql = """SELECT item_id_2 as related_id, relationship_type, similarity_score
                 FROM relationships
                 WHERE item_id_1 = ?
                 UNION
                 SELECT item_id_1 as related_id, relationship_type, similarity_score
                 FROM relationships
                 WHERE item_id_2 = ?"""

        cursor = self.conn.execute(sql, (item_id, item_id))
        return [(row["related_id"], row["relationship_type"], row["similarity_score"]) for row in cursor.fetchall()]

    def save_source(self, source: Source) -> int:
        """Save or update a source."""
        data = source.to_dict()
        del data["id"]

        sql = """INSERT INTO sources
                 (source_type, file_path, file_hash, items_count, last_processed,
                  processing_status, error_message, metadata)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                 ON CONFLICT(file_path) DO UPDATE SET
                 file_hash = excluded.file_hash,
                 items_count = excluded.items_count,
                 last_processed = excluded.last_processed,
                 processing_status = excluded.processing_status,
                 error_message = excluded.error_message,
                 metadata = excluded.metadata"""

        cursor = self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return cursor.lastrowid

    def get_source_by_path(self, file_path: str) -> Optional[Source]:
        """Get source by file path."""
        cursor = self.conn.execute("SELECT * FROM sources WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()
        if row:
            data = dict(row)
            if isinstance(data.get("metadata"), str):
                data["metadata"] = json.loads(data["metadata"])
            if isinstance(data.get("last_processed"), str):
                data["last_processed"] = datetime.fromisoformat(data["last_processed"])
            if isinstance(data.get("created_at"), str):
                data["created_at"] = datetime.fromisoformat(data["created_at"])
            return Source(**data)
        return None

    def save_embedding(self, item_id: int, embedding: Any, model_name: str):
        """Save embedding for an item."""
        embedding_bytes = pickle.dumps(embedding)
        sql = """INSERT INTO embeddings (item_id, embedding, model_name)
                 VALUES (?, ?, ?)
                 ON CONFLICT(item_id, model_name) DO UPDATE SET
                 embedding = excluded.embedding"""

        self.conn.execute(sql, (item_id, embedding_bytes, model_name))
        self.conn.commit()

    def get_embedding(self, item_id: int, model_name: str) -> Optional[Any]:
        """Get embedding for an item."""
        cursor = self.conn.execute(
            "SELECT embedding FROM embeddings WHERE item_id = ? AND model_name = ?",
            (item_id, model_name),
        )
        row = cursor.fetchone()
        if row:
            return pickle.loads(row["embedding"])
        return None

    def get_all_embeddings(self, model_name: str) -> List[tuple]:
        """Get all embeddings for a model (item_id, embedding)."""
        cursor = self.conn.execute(
            "SELECT item_id, embedding FROM embeddings WHERE model_name = ?", (model_name,)
        )
        return [(row["item_id"], pickle.loads(row["embedding"])) for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {}

        # Total counts
        cursor = self.conn.execute("SELECT COUNT(*) as count FROM items")
        stats["total_items"] = cursor.fetchone()["count"]

        # By type
        cursor = self.conn.execute(
            "SELECT type, COUNT(*) as count FROM items GROUP BY type"
        )
        stats["by_type"] = {row["type"]: row["count"] for row in cursor.fetchall()}

        # By priority
        cursor = self.conn.execute(
            "SELECT priority, COUNT(*) as count FROM items GROUP BY priority"
        )
        stats["by_priority"] = {row["priority"]: row["count"] for row in cursor.fetchall()}

        # By status
        cursor = self.conn.execute(
            "SELECT status, COUNT(*) as count FROM items GROUP BY status"
        )
        stats["by_status"] = {row["status"]: row["count"] for row in cursor.fetchall()}

        return stats

    def vacuum(self):
        """Vacuum the database to reclaim space."""
        self.conn.execute("VACUUM")

    def backup(self, backup_path: str):
        """Create a backup of the database."""
        import shutil

        shutil.copy2(self.db_path, backup_path)

    def close(self):
        """Close database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
