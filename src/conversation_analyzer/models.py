"""Pydantic models for data validation and structure."""

from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator
import json


class ExtractedItem(BaseModel):
    """Single extracted item from LLM output."""

    type: Literal["TODO", "BUG", "FEATURE", "PROJECT"]
    description: str = Field(..., min_length=5, max_length=1000)
    priority: Literal["high", "medium", "low"]
    source_context: str = Field(..., max_length=2000)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @field_validator("description", "source_context")
    @classmethod
    def clean_whitespace(cls, v: str) -> str:
        """Clean excessive whitespace from text fields."""
        return " ".join(v.split())

    model_config = {
        "json_schema_extra": {
            "example": {
                "type": "TODO",
                "description": "Fix login timeout issue",
                "priority": "high",
                "source_context": "We should fix the login timeout...",
                "confidence": 0.95,
            }
        }
    }


class ExtractionResult(BaseModel):
    """Result from LLM extraction containing multiple items."""

    items: List[ExtractedItem] = Field(default_factory=list)


class Item(BaseModel):
    """Database item model with full metadata."""

    id: Optional[int] = None
    type: Literal["TODO", "BUG", "FEATURE", "PROJECT"]
    description: str
    priority: Literal["high", "medium", "low"]
    priority_score: float = 0.5
    source_context: str
    confidence: float

    # Source tracking
    source_type: Literal["conversation", "code", "document", "git"]
    source_file: str
    source_line: Optional[int] = None
    extracted_at: datetime = Field(default_factory=datetime.now)

    # Metadata
    tags: List[str] = Field(default_factory=list)
    entities: Dict[str, List[str]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Deduplication
    status: Literal["open", "in_progress", "completed", "duplicate"] = "open"
    is_duplicate: bool = False
    duplicate_of: Optional[int] = None
    embedding_hash: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for database storage."""
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "priority": self.priority,
            "priority_score": self.priority_score,
            "source_context": self.source_context,
            "confidence": self.confidence,
            "source_type": self.source_type,
            "source_file": self.source_file,
            "source_line": self.source_line,
            "extracted_at": self.extracted_at.isoformat(),
            "tags": json.dumps(self.tags),
            "entities": json.dumps(self.entities),
            "metadata": json.dumps(self.metadata),
            "status": self.status,
            "is_duplicate": int(self.is_duplicate),
            "duplicate_of": self.duplicate_of,
            "embedding_hash": self.embedding_hash,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Item":
        """Create Item from database dict."""
        # Parse JSON fields
        if isinstance(data.get("tags"), str):
            data["tags"] = json.loads(data["tags"])
        if isinstance(data.get("entities"), str):
            data["entities"] = json.loads(data["entities"])
        if isinstance(data.get("metadata"), str):
            data["metadata"] = json.loads(data["metadata"])

        # Parse datetime fields
        for field in ["extracted_at", "created_at", "updated_at"]:
            if isinstance(data.get(field), str):
                data[field] = datetime.fromisoformat(data[field])

        # Convert boolean
        if "is_duplicate" in data:
            data["is_duplicate"] = bool(data["is_duplicate"])

        return cls(**data)


class Relationship(BaseModel):
    """Relationship between two items."""

    id: Optional[int] = None
    item_id_1: int
    item_id_2: int
    relationship_type: Literal["duplicate", "related", "blocks", "blocked_by", "parent", "child"]
    similarity_score: Optional[float] = None
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Source(BaseModel):
    """Source file tracking."""

    id: Optional[int] = None
    source_type: Literal["conversation", "code", "document", "git"]
    file_path: str
    file_hash: str
    items_count: int = 0
    last_processed: datetime = Field(default_factory=datetime.now)
    processing_status: Literal["success", "failed", "partial"] = "success"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for database storage."""
        return {
            "id": self.id,
            "source_type": self.source_type,
            "file_path": self.file_path,
            "file_hash": self.file_hash,
            "items_count": self.items_count,
            "last_processed": self.last_processed.isoformat(),
            "processing_status": self.processing_status,
            "error_message": self.error_message,
            "metadata": json.dumps(self.metadata),
            "created_at": self.created_at.isoformat(),
        }


class ExtractionRun(BaseModel):
    """Extraction run tracking for auditing."""

    id: Optional[int] = None
    model_name: str
    prompt_version: str
    sources_processed: int = 0
    items_extracted: int = 0
    duration_seconds: Optional[float] = None
    status: Literal["running", "completed", "failed"] = "running"
    error_message: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class AnalysisResult(BaseModel):
    """Result from analyzing a file or directory."""

    sources_processed: int = 0
    items_extracted: int = 0
    items_deduplicated: int = 0
    high_priority: int = 0
    medium_priority: int = 0
    low_priority: int = 0
    by_type: Dict[str, int] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    duration_seconds: float = 0.0


class DuplicateGroup(BaseModel):
    """Group of duplicate items."""

    primary_item: Item
    duplicates: List[Item]
    similarity_scores: List[float]
