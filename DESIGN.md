# Conversation Analyzer - System Design

**Date:** November 16, 2025
**Author:** TD Professional Services LLC
**Status:** Design Phase

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CONVERSATION ANALYZER                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   INPUTS     │──────│  PROCESSING  │──────│   OUTPUTS    │
└──────────────┘      └──────────────┘      └──────────────┘
      │                     │                      │
      ├─ Conversations      ├─ Parser             ├─ SQLite DB
      ├─ Code Comments      ├─ Extractor          ├─ Markdown Reports
      ├─ TODO.md files      ├─ Validator          ├─ JSON Exports
      ├─ Git commits        ├─ Deduplicator       └─ CLI Output
      └─ Documentation      ├─ Scorer
                            └─ Linker

┌──────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                          │
├──────────────────────────────────────────────────────────────────┤
│  • Ollama (nuextract, llama3.1)                                  │
│  • sentence-transformers (for embeddings)                        │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Breakdown

#### Input Layer
- **ConversationParser:** Parse Claude Code conversations (Markdown/JSON)
- **CodeScanner:** Scan code files for TODO/FIXME comments
- **DocumentReader:** Extract from TODO.md, README.md, etc.
- **GitAnalyzer:** Analyze git history and commit messages

#### Processing Layer
- **Extractor:** Use Ollama + NuExtract to extract items
- **Validator:** Pydantic-based validation and cleaning
- **Deduplicator:** Embedding-based similarity detection
- **PriorityScorer:** Calculate priority scores
- **EntityLinker:** Link related items via shared entities

#### Storage Layer
- **SQLite Database:** Primary data store
- **FileCache:** Cache embeddings and intermediate results

#### Output Layer
- **ReportGenerator:** Generate Markdown/JSON reports
- **DatabaseExporter:** Query and export data
- **CLIInterface:** Interactive command-line interface

### 1.3 Data Flow

```
1. INPUT STAGE
   └─> Read source files (conversations, code, docs)
   └─> Parse into standardized format
   └─> Extract text chunks (handle context window limits)

2. EXTRACTION STAGE
   └─> Send chunks to Ollama with extraction prompt
   └─> Parse JSON responses
   └─> Validate with Pydantic models
   └─> Store raw extractions

3. INTELLIGENCE STAGE
   └─> Generate embeddings for descriptions
   └─> Find duplicates via similarity
   └─> Calculate priority scores
   └─> Extract entities and create links
   └─> Merge/deduplicate items

4. OUTPUT STAGE
   └─> Store in SQLite database
   └─> Generate reports (Markdown, JSON)
   └─> Display summary in CLI
```

---

## 2. Database Schema

### 2.1 SQLite Schema

```sql
-- Items: Core extracted items
CREATE TABLE items (
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
    tags TEXT,  -- JSON array
    entities TEXT,  -- JSON object
    metadata TEXT,  -- JSON object for extensibility

    -- Deduplication
    is_duplicate BOOLEAN NOT NULL DEFAULT 0,
    duplicate_of INTEGER REFERENCES items(id),
    embedding_hash TEXT,  -- For quick lookup

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_items_type ON items(type);
CREATE INDEX idx_items_priority ON items(priority);
CREATE INDEX idx_items_status ON items(status);
CREATE INDEX idx_items_source_file ON items(source_file);
CREATE INDEX idx_items_extracted_at ON items(extracted_at);
CREATE INDEX idx_items_embedding_hash ON items(embedding_hash);

-- Embeddings: Store vector embeddings for similarity search
CREATE TABLE embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    embedding BLOB NOT NULL,  -- Pickle serialized numpy array
    model_name TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(item_id, model_name)
);

CREATE INDEX idx_embeddings_item_id ON embeddings(item_id);

-- Relationships: Links between related items
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id_1 INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    item_id_2 INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    relationship_type TEXT NOT NULL CHECK(relationship_type IN ('duplicate', 'related', 'blocks', 'blocked_by', 'parent', 'child')),
    similarity_score REAL,
    reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(item_id_1, item_id_2, relationship_type)
);

CREATE INDEX idx_relationships_item1 ON relationships(item_id_1);
CREATE INDEX idx_relationships_item2 ON relationships(item_id_2);

-- Sources: Track source files and their processing status
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL CHECK(source_type IN ('conversation', 'code', 'document', 'git')),
    file_path TEXT NOT NULL UNIQUE,
    file_hash TEXT NOT NULL,  -- SHA256 of file content
    items_count INTEGER NOT NULL DEFAULT 0,
    last_processed TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processing_status TEXT NOT NULL DEFAULT 'success' CHECK(processing_status IN ('success', 'failed', 'partial')),
    error_message TEXT,
    metadata TEXT,  -- JSON object
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sources_file_path ON sources(file_path);
CREATE INDEX idx_sources_file_hash ON sources(file_hash);

-- Extraction Runs: Track each extraction run for auditing
CREATE TABLE extraction_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    sources_processed INTEGER NOT NULL DEFAULT 0,
    items_extracted INTEGER NOT NULL DEFAULT 0,
    duration_seconds REAL,
    status TEXT NOT NULL CHECK(status IN ('running', 'completed', 'failed')),
    error_message TEXT,
    config TEXT,  -- JSON object with extraction config
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_extraction_runs_started_at ON extraction_runs(started_at);

-- Tags: Normalized tag storage
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tags_name ON tags(name);

-- Item Tags: Many-to-many relationship
CREATE TABLE item_tags (
    item_id INTEGER NOT NULL REFERENCES items(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, tag_id)
);

-- Trigger to update updated_at timestamp
CREATE TRIGGER update_items_timestamp
AFTER UPDATE ON items
FOR EACH ROW
BEGIN
    UPDATE items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### 2.2 Data Models (Pydantic)

```python
from datetime import datetime
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, validator
import json

class ExtractedItem(BaseModel):
    """Single extracted item from source"""
    type: Literal["TODO", "BUG", "FEATURE", "PROJECT"]
    description: str = Field(..., min_length=5, max_length=1000)
    priority: Literal["high", "medium", "low"]
    source_context: str = Field(..., max_length=2000)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @validator('description', 'source_context')
    def clean_whitespace(cls, v):
        return ' '.join(v.split())

    class Config:
        json_schema_extra = {
            "example": {
                "type": "TODO",
                "description": "Fix login timeout issue",
                "priority": "high",
                "source_context": "We should fix the login timeout...",
                "confidence": 0.95
            }
        }

class ExtractionResult(BaseModel):
    """Result from LLM extraction"""
    items: List[ExtractedItem]

class Item(BaseModel):
    """Database item model"""
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
    tags: List[str] = []
    entities: Dict[str, List[str]] = {}
    metadata: Dict[str, Any] = {}

    # Deduplication
    status: Literal["open", "in_progress", "completed", "duplicate"] = "open"
    is_duplicate: bool = False
    duplicate_of: Optional[int] = None
    embedding_hash: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """Convert to dict for database storage"""
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description,
            'priority': self.priority,
            'priority_score': self.priority_score,
            'source_context': self.source_context,
            'confidence': self.confidence,
            'source_type': self.source_type,
            'source_file': self.source_file,
            'source_line': self.source_line,
            'extracted_at': self.extracted_at.isoformat(),
            'tags': json.dumps(self.tags),
            'entities': json.dumps(self.entities),
            'metadata': json.dumps(self.metadata),
            'status': self.status,
            'is_duplicate': self.is_duplicate,
            'duplicate_of': self.duplicate_of,
            'embedding_hash': self.embedding_hash,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Relationship(BaseModel):
    """Relationship between items"""
    id: Optional[int] = None
    item_id_1: int
    item_id_2: int
    relationship_type: Literal["duplicate", "related", "blocks", "blocked_by", "parent", "child"]
    similarity_score: Optional[float] = None
    reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Source(BaseModel):
    """Source file tracking"""
    id: Optional[int] = None
    source_type: Literal["conversation", "code", "document", "git"]
    file_path: str
    file_hash: str
    items_count: int = 0
    last_processed: datetime = Field(default_factory=datetime.now)
    processing_status: Literal["success", "failed", "partial"] = "success"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)

class ExtractionRun(BaseModel):
    """Extraction run tracking"""
    id: Optional[int] = None
    model_name: str
    prompt_version: str
    sources_processed: int = 0
    items_extracted: int = 0
    duration_seconds: Optional[float] = None
    status: Literal["running", "completed", "failed"] = "running"
    error_message: Optional[str] = None
    config: Dict[str, Any] = {}
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
```

---

## 3. Module Structure

### 3.1 Project Layout

```
conversation-analyzer/
├── README.md
├── RESEARCH_REPORT.md
├── DESIGN.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
│
├── src/
│   └── conversation_analyzer/
│       ├── __init__.py
│       ├── __main__.py           # CLI entry point
│       │
│       ├── config.py              # Configuration management
│       ├── models.py              # Pydantic models
│       ├── database.py            # Database operations
│       │
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── base.py           # Base parser interface
│       │   ├── conversation.py   # Conversation parser
│       │   ├── code.py           # Code comment scanner
│       │   ├── document.py       # Document parser
│       │   └── git.py            # Git history analyzer
│       │
│       ├── extraction/
│       │   ├── __init__.py
│       │   ├── extractor.py      # Main extraction logic
│       │   ├── prompts.py        # Prompt templates
│       │   ├── ollama_client.py  # Ollama integration
│       │   └── validator.py      # Output validation
│       │
│       ├── intelligence/
│       │   ├── __init__.py
│       │   ├── deduplicator.py   # Deduplication logic
│       │   ├── scorer.py         # Priority scoring
│       │   ├── linker.py         # Entity linking
│       │   └── embeddings.py     # Embedding generation
│       │
│       ├── reporting/
│       │   ├── __init__.py
│       │   ├── markdown.py       # Markdown report generator
│       │   ├── json_export.py    # JSON export
│       │   └── cli_display.py    # CLI formatting
│       │
│       └── utils/
│           ├── __init__.py
│           ├── file_hash.py      # File hashing utilities
│           ├── text_chunking.py  # Handle context window limits
│           └── logging.py        # Logging configuration
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── fixtures/
│   │   ├── conversations/
│   │   │   ├── sample_conversation_1.md
│   │   │   └── sample_conversation_2.json
│   │   ├── code/
│   │   │   └── sample_code.py
│   │   └── expected_outputs/
│   │       └── sample_1_expected.json
│   │
│   ├── unit/
│   │   ├── test_parsers.py
│   │   ├── test_extractor.py
│   │   ├── test_deduplicator.py
│   │   ├── test_scorer.py
│   │   └── test_database.py
│   │
│   ├── integration/
│   │   ├── test_full_pipeline.py
│   │   └── test_report_generation.py
│   │
│   └── llm_eval/
│       ├── test_extraction_quality.py
│       ├── test_consistency.py
│       └── test_edge_cases.py
│
├── data/                          # Created at runtime
│   ├── conversations/
│   ├── database/
│   │   └── analyzer.db
│   └── reports/
│
└── docs/
    ├── INSTALLATION.md
    ├── USAGE.md
    ├── CONFIGURATION.md
    └── DEVELOPMENT.md
```

### 3.2 Module Responsibilities

**`config.py`:**
- Load configuration from environment/files
- Manage Ollama connection settings
- Define prompt templates
- Set thresholds for scoring/deduplication

**`database.py`:**
- SQLite connection management
- CRUD operations for all tables
- Query helpers (get items by type, find duplicates, etc.)
- Schema migration support

**`parsers/`:**
- Each parser implements `BaseParser` interface
- Extract text chunks from different source types
- Handle format-specific quirks
- Return standardized `ParsedSource` objects

**`extraction/`:**
- Orchestrate LLM extraction
- Manage prompts and model selection
- Handle retries and errors
- Validate outputs with Pydantic

**`intelligence/`:**
- Implement deduplication algorithm
- Calculate priority scores
- Extract and link entities
- Generate embeddings

**`reporting/`:**
- Generate Markdown reports with grouping
- Export to JSON
- Format for CLI display
- Support custom templates

---

## 4. Configuration System

### 4.1 Configuration File (YAML)

```yaml
# config.yaml

ollama:
  host: "http://localhost:11434"
  extraction_model: "nuextract"
  analysis_model: "llama3.1:8b"
  temperature: 0.1
  max_tokens: 2048
  timeout: 60

extraction:
  prompt_version: "v1.0"
  confidence_threshold: 0.5
  batch_size: 10
  chunk_size: 1800  # tokens, leave room for prompt

intelligence:
  deduplication:
    enabled: true
    similarity_threshold: 0.85
    embedding_model: "all-MiniLM-L6-v2"

  priority_scoring:
    urgency_keywords: ["urgent", "critical", "asap", "immediately", "blocker"]
    impact_keywords: ["breaks", "blocks", "prevents", "security", "data loss"]
    base_score: 0.5

  entity_linking:
    enabled: true
    min_entities_shared: 1

database:
  path: "data/database/analyzer.db"
  backup_enabled: true
  backup_interval: 86400  # seconds (1 day)

reporting:
  output_dir: "data/reports"
  formats: ["markdown", "json"]
  group_by: "type"  # type, priority, source
  include_duplicates: false

logging:
  level: "INFO"
  file: "data/logs/analyzer.log"
  console: true

sources:
  conversations:
    - "data/conversations/**/*.md"
    - "data/conversations/**/*.json"
  code:
    - "**/*.py"
    - "**/*.js"
    - "**/*.ts"
  documents:
    - "**/TODO.md"
    - "**/README.md"
    - "**/NOTES.md"
  git:
    enabled: false
    branch: "main"
    since: "30 days ago"
```

### 4.2 Environment Variables

```bash
# .env

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=nuextract

# Database
DATABASE_PATH=data/database/analyzer.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=data/logs/analyzer.log

# Testing
TEST_MODE=false
TEST_OLLAMA_MODEL=nuextract  # Can use smaller model for tests
```

---

## 5. API Design

### 5.1 Core Classes

```python
# Main Analyzer class
class ConversationAnalyzer:
    def __init__(self, config: Config):
        self.config = config
        self.db = Database(config.database.path)
        self.extractor = Extractor(config.ollama, config.extraction)
        self.intelligence = Intelligence(config.intelligence)
        self.reporter = Reporter(config.reporting)

    def analyze_file(self, file_path: str) -> AnalysisResult:
        """Analyze a single file"""
        pass

    def analyze_directory(self, dir_path: str) -> AnalysisResult:
        """Analyze all files in directory"""
        pass

    def generate_report(self, output_format: str = "markdown") -> str:
        """Generate report from database"""
        pass

    def find_duplicates(self) -> List[DuplicateGroup]:
        """Find and return duplicate items"""
        pass

# Extractor class
class Extractor:
    def __init__(self, ollama_config: OllamaConfig, extraction_config: ExtractionConfig):
        self.ollama = OllamaClient(ollama_config)
        self.config = extraction_config
        self.validator = OutputValidator()

    def extract(self, text: str, source_info: SourceInfo) -> ExtractionResult:
        """Extract items from text"""
        pass

    def extract_batch(self, texts: List[str], source_infos: List[SourceInfo]) -> List[ExtractionResult]:
        """Extract from multiple texts"""
        pass

# Database class
class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = self._connect()

    def save_item(self, item: Item) -> int:
        """Save item and return ID"""
        pass

    def get_items(self, filters: Dict[str, Any] = None) -> List[Item]:
        """Get items with optional filters"""
        pass

    def mark_duplicate(self, item_id: int, duplicate_of: int):
        """Mark item as duplicate"""
        pass

    def update_priority(self, item_id: int, priority: str, score: float):
        """Update item priority"""
        pass
```

### 5.2 CLI Interface

```bash
# Basic usage
conversation-analyzer analyze <path>
conversation-analyzer report --format markdown --output report.md
conversation-analyzer deduplicate --dry-run
conversation-analyzer stats

# Advanced usage
conversation-analyzer analyze --source-type conversation data/conversations/
conversation-analyzer analyze --source-type code --patterns "**/*.py"
conversation-analyzer query --type TODO --priority high
conversation-analyzer export --format json --output items.json
conversation-analyzer merge-duplicate 123 456

# Configuration
conversation-analyzer config set ollama.model llama3.1:8b
conversation-analyzer config get
conversation-analyzer test-connection

# Maintenance
conversation-analyzer db vacuum
conversation-analyzer db backup
conversation-analyzer clear-duplicates
```

---

## 6. Testing Strategy

### 6.1 Test Pyramid

```
         ┌─────────────┐
         │  LLM Eval   │  <- 20% (Quality, consistency, edge cases)
         │   Tests     │
         └─────────────┘
       ┌─────────────────┐
       │  Integration    │  <- 30% (End-to-end pipelines)
       │     Tests       │
       └─────────────────┘
   ┌───────────────────────┐
   │     Unit Tests        │  <- 50% (Individual functions)
   └───────────────────────┘
```

### 6.2 Unit Tests

**Coverage Areas:**
- Parsers: Test each parser with valid/invalid inputs
- Extraction: Test prompt formatting, validation
- Deduplication: Test similarity calculation
- Priority Scoring: Test score calculation with various inputs
- Entity Linking: Test entity extraction and linking logic
- Database: Test CRUD operations

**Example:**
```python
def test_priority_scorer_urgent_keywords():
    scorer = PriorityScorer()
    item = {"description": "URGENT: Fix critical security bug"}
    score = scorer.calculate_score(item, {})
    assert score >= 0.75
    assert scorer.get_priority(score) == "high"
```

### 6.3 Integration Tests

**Coverage Areas:**
- Full extraction pipeline (file → items → database)
- Report generation from database
- Deduplication with actual embeddings
- Multi-source analysis

**Example:**
```python
def test_full_extraction_pipeline(sample_conversation, temp_db):
    analyzer = ConversationAnalyzer(config)
    result = analyzer.analyze_file(sample_conversation)

    assert result.items_extracted > 0
    items = analyzer.db.get_items()
    assert len(items) == result.items_extracted
    assert all(item.confidence >= 0.5 for item in items)
```

### 6.4 LLM Evaluation Tests

**Using DeepEval:**
```python
from deepeval import assert_test
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

def test_extraction_faithfulness(sample_conversation, extractor):
    result = extractor.extract(sample_conversation, source_info)

    for item in result.items:
        test_case = LLMTestCase(
            input=sample_conversation,
            actual_output=item.description,
            retrieval_context=[sample_conversation]
        )

        metric = FaithfulnessMetric(threshold=0.8)
        assert_test(test_case, [metric])

def test_extraction_consistency():
    """Test that same input produces similar output"""
    text = "TODO: Fix the login bug. It's urgent."

    results = [extractor.extract(text, source_info) for _ in range(3)]

    # All should extract same number of items
    assert len(set(len(r.items) for r in results)) == 1

    # All should identify same type
    types = [[i.type for i in r.items] for r in results]
    assert all(t == types[0] for t in types)
```

### 6.5 Test Fixtures

**Sample Conversations:**
- Simple: Single TODO
- Complex: Multiple TODOs, bugs, features mixed
- Edge cases: Very long, very short, no items, ambiguous
- Malformed: Invalid JSON, corrupted text

**Expected Outputs:**
- Golden set of expected extractions
- Used for regression testing
- Updated when extraction improves

**Mock Ollama:**
- For fast unit tests without Ollama running
- Returns predefined responses
- Tests error handling

---

## 7. Error Handling & Edge Cases

### 7.1 Error Handling Strategy

**Graceful Degradation:**
- If Ollama unavailable: Cache for retry, notify user
- If extraction fails: Log error, mark source as failed
- If validation fails: Store with low confidence, flag for review

**Retry Logic:**
```python
class Extractor:
    MAX_RETRIES = 3
    BACKOFF_FACTOR = 2

    def extract_with_retry(self, text: str) -> ExtractionResult:
        for attempt in range(self.MAX_RETRIES):
            try:
                return self._extract(text)
            except OllamaConnectionError as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                time.sleep(self.BACKOFF_FACTOR ** attempt)
            except OllamaTimeoutError:
                # Reduce chunk size and retry
                text = self._reduce_chunk_size(text)
        raise ExtractionError("Max retries exceeded")
```

### 7.2 Edge Cases

**Context Window Limits:**
- Chunk long conversations with overlap
- Extract from each chunk separately
- Merge results, handle cross-chunk duplicates

**Ambiguous Items:**
- "Maybe we should..." → Low confidence feature request
- "This might be a bug" → Medium confidence bug
- Use confidence scores to filter

**Duplicate Detection:**
- Exact duplicates: Easy (string match)
- Paraphrased: Use embeddings
- Same issue, different context: Link but don't merge

**Empty/Invalid Responses:**
- LLM returns empty JSON: Log, mark as failed
- LLM returns invalid JSON: Attempt to fix, else discard
- LLM hallucinates: Faithfulness metric should catch

---

## 8. Performance Considerations

### 8.1 Optimization Targets

**Throughput:**
- Process 100 conversations in < 5 minutes
- Extract from 1000 code files in < 10 minutes

**Latency:**
- Single conversation: < 5 seconds
- Report generation: < 2 seconds

**Resource Usage:**
- RAM: < 4GB (excluding Ollama)
- Disk: Minimal (SQLite + embeddings cache)

### 8.2 Optimization Strategies

**Batch Processing:**
- Group small files together
- Send batches to Ollama
- Parallel processing where possible

**Caching:**
- Cache embeddings (only compute once)
- Cache file hashes (skip unchanged files)
- Cache LLM responses (optional, for development)

**Database Optimization:**
- Indexes on frequently queried columns
- Batch inserts (transaction per file, not per item)
- VACUUM database periodically

**Smart Chunking:**
- Don't chunk unnecessarily
- Overlap chunks by 100 tokens
- Use sliding window for long docs

---

## 9. Security & Privacy

### 9.1 Privacy Guarantees

**Local Processing:**
- All LLM processing via Ollama (local)
- No external API calls
- No data sent to cloud services

**Data Storage:**
- SQLite database stored locally
- User controls location and access
- Can be encrypted at rest (OS-level)

### 9.2 Security Considerations

**Input Validation:**
- Validate file paths (prevent traversal)
- Sanitize inputs before LLM
- Limit file sizes

**Database Security:**
- Use parameterized queries (prevent SQL injection)
- Set appropriate file permissions
- Support database encryption

**Code Scanning Safety:**
- Don't execute scanned code
- Sandbox file access
- Respect .gitignore

---

## 10. Future Enhancements

### 10.1 Phase 4-5 Features

**Enhanced Intelligence:**
- Trend analysis (what types of items are common)
- Burndown tracking (mark as done, track progress)
- Effort estimation (based on description)

**Integration:**
- GitHub Issues export
- Jira integration
- Slack/Discord notifications
- VS Code extension

**Automation:**
- Watch mode (monitor directories for changes)
- Auto-update (re-analyze modified files)
- Scheduled reports (daily/weekly summaries)

**Advanced Analytics:**
- Heat maps (which files have most TODOs)
- Technical debt scoring
- Contributor analysis (from git history)

### 10.2 Potential Model Upgrades

**Specialized Models:**
- Fine-tune own model on project-specific data
- Multi-model voting (ensemble for higher accuracy)
- Different models for different item types

**Multimodal:**
- Extract from screenshots (diagrams, whiteboards)
- Video/audio conversation analysis
- Image-based documentation

---

## Summary

This design provides:
- ✅ **Clear architecture** with separation of concerns
- ✅ **Robust database schema** supporting all requirements
- ✅ **Flexible configuration** system
- ✅ **Comprehensive testing** strategy
- ✅ **Error handling** and edge cases covered
- ✅ **Performance** considerations addressed
- ✅ **Privacy & security** as first-class citizens

**Next Steps:**
1. Create test fixtures
2. Set up project structure
3. Implement core database layer
4. Build extraction pipeline MVP
5. Add intelligence features
6. Polish and test

**Estimated Implementation Time:**
- Database & Models: 2 hours
- Parsers: 2 hours
- Extraction Pipeline: 2-3 hours
- Intelligence Features: 2-3 hours
- Reporting: 1 hour
- Testing: 2-3 hours
- Documentation: 1 hour

**Total: 12-15 hours**
