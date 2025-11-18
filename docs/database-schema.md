# Database Schema Documentation

**Version:** 0.1.0
**Database:** SQLite 3
**Last Updated:** 2025-11-18
**Status:** Design complete, implementation pending (Phase 4)

---

## Overview

The Conversation Analyzer uses SQLite for structured storage of extracted findings, metadata, and deduplication tracking. SQLite was chosen for:

- **Zero configuration:** No server setup required
- **Portability:** Single-file database
- **Sufficient performance:** Adequate for expected data volumes (< 100K records)
- **Built-in Python support:** No additional dependencies

---

## Entity-Relationship Diagram

```
┌──────────────────┐         ┌─────────────────┐         ┌──────────────────┐
│  conversations   │         │    findings     │         │     sources      │
├──────────────────┤         ├─────────────────┤         ├──────────────────┤
│ id (PK)          │────────<│ conversation_id │         │ id (PK)          │
│ file_path        │         │ id (PK)         │>───────┤ finding_id       │
│ file_hash        │         │ type            │         │ file_path        │
│ analyzed_at      │         │ description     │         │ line_number      │
│ model_used       │         │ confidence      │         │ context_before   │
│ duration_seconds │         │ priority        │         │ context_after    │
│ findings_count   │         │ created_at      │         │ created_at       │
└──────────────────┘         │ updated_at      │         └──────────────────┘
                             │ status          │
                             └─────────────────┘
                                      │
                                      │
                             ┌────────┴─────────┐
                             │                  │
                    ┌────────▼────────┐  ┌──────▼───────────┐
                    │ deduplications  │  │  patterns       │
                    ├─────────────────┤  ├──────────────────┤
                    │ id (PK)         │  │ id (PK)          │
                    │ finding_id_1    │  │ pattern_type     │
                    │ finding_id_2    │  │ description      │
                    │ similarity      │  │ first_seen       │
                    │ method          │  │ last_seen        │
                    │ created_at      │  │ frequency        │
                    └─────────────────┘  │ related_findings │
                                          │ created_at       │
                                          └──────────────────┘
```

---

## Table Definitions

### 1. `conversations`

Stores metadata about analyzed conversation files.

```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL UNIQUE,
    file_hash TEXT NOT NULL,
    analyzed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    model_used TEXT NOT NULL,
    duration_seconds REAL,
    findings_count INTEGER DEFAULT 0,
    metadata_json TEXT  -- Stores additional metadata as JSON
);

CREATE INDEX idx_conversations_file_path ON conversations(file_path);
CREATE INDEX idx_conversations_analyzed_at ON conversations(analyzed_at);
CREATE INDEX idx_conversations_file_hash ON conversations(file_hash);
```

**Columns:**

- `id`: Primary key, auto-increment
- `file_path`: Absolute path to conversation file (unique)
- `file_hash`: SHA-256 hash of file content (for change detection)
- `analyzed_at`: When analysis was performed
- `model_used`: Ollama model used (e.g., "qwen2.5:3b")
- `duration_seconds`: How long analysis took
- `findings_count`: Number of findings extracted (denormalized for performance)
- `metadata_json`: Additional metadata (conversation date, participants, etc.)

**Purpose:** Track which conversations have been analyzed and when, prevent re-analyzing unchanged files.

---

### 2. `findings`

Stores extracted TODOs, bugs, features, and other action items.

```sql
CREATE TABLE findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('todo', 'bug', 'feature', 'enhancement', 'question')),
    description TEXT NOT NULL,
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 100),
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    status TEXT NOT NULL DEFAULT 'new' CHECK(status IN ('new', 'confirmed', 'duplicate', 'false_positive', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata_json TEXT,  -- Stores extracted keywords, context, etc.

    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX idx_findings_conversation_id ON findings(conversation_id);
CREATE INDEX idx_findings_type ON findings(type);
CREATE INDEX idx_findings_confidence ON findings(confidence);
CREATE INDEX idx_findings_priority ON findings(priority);
CREATE INDEX idx_findings_status ON findings(status);
CREATE INDEX idx_findings_created_at ON findings(created_at);

-- Composite index for common queries
CREATE INDEX idx_findings_type_priority ON findings(type, priority);
CREATE INDEX idx_findings_status_confidence ON findings(status, confidence);
```

**Columns:**

- `id`: Primary key, auto-increment
- `conversation_id`: Foreign key to conversations table
- `type`: Category of finding (todo, bug, feature, enhancement, question)
- `description`: The extracted action item text
- `confidence`: How confident the extractor is (0-100)
- `priority`: Computed priority (low, medium, high, critical)
- `status`: Current status of finding
  - `new`: Just extracted
  - `confirmed`: User reviewed and confirmed
  - `duplicate`: Identified as duplicate of another finding
  - `false_positive`: Incorrectly extracted
  - `completed`: Action item has been completed
- `created_at`: When finding was first extracted
- `updated_at`: When finding was last modified
- `metadata_json`: Additional extracted data (keywords, urgency indicators, etc.)

**Purpose:** Core table for storing all extracted action items.

---

### 3. `sources`

Stores exact source locations for each finding (file, line number, context).

```sql
CREATE TABLE sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    line_number INTEGER,
    context_before TEXT,  -- 3 lines before
    context_after TEXT,   -- 3 lines after
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (finding_id) REFERENCES findings(id) ON DELETE CASCADE
);

CREATE INDEX idx_sources_finding_id ON sources(finding_id);
CREATE INDEX idx_sources_file_path ON sources(file_path);
```

**Columns:**

- `id`: Primary key, auto-increment
- `finding_id`: Foreign key to findings table
- `file_path`: Source file where finding was extracted
- `line_number`: Line number in file (if applicable)
- `context_before`: Text before the finding (for context in reports)
- `context_after`: Text after the finding
- `created_at`: When source was recorded

**Purpose:** Allow users to jump to exact location where TODO/bug was mentioned.

**Note:** A finding can have multiple sources if mentioned in multiple places.

---

### 4. `deduplications`

Tracks relationships between similar findings to prevent duplicate reporting.

```sql
CREATE TABLE deduplications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_id_1 INTEGER NOT NULL,
    finding_id_2 INTEGER NOT NULL,
    similarity REAL NOT NULL CHECK(similarity >= 0 AND similarity <= 100),
    method TEXT NOT NULL CHECK(method IN ('exact', 'fuzzy', 'semantic')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (finding_id_1) REFERENCES findings(id) ON DELETE CASCADE,
    FOREIGN KEY (finding_id_2) REFERENCES findings(id) ON DELETE CASCADE,

    CHECK (finding_id_1 < finding_id_2)  -- Prevent duplicate pairs
);

CREATE INDEX idx_deduplications_finding_id_1 ON deduplications(finding_id_1);
CREATE INDEX idx_deduplications_finding_id_2 ON deduplications(finding_id_2);
CREATE INDEX idx_deduplications_similarity ON deduplications(similarity);
CREATE UNIQUE INDEX idx_deduplications_pair ON deduplications(finding_id_1, finding_id_2);
```

**Columns:**

- `id`: Primary key, auto-increment
- `finding_id_1`: First finding (always lower ID)
- `finding_id_2`: Second finding (always higher ID)
- `similarity`: How similar the findings are (0-100)
- `method`: How similarity was determined
  - `exact`: Identical text
  - `fuzzy`: High string similarity (Levenshtein distance)
  - `semantic`: LLM determined they mean the same thing
- `created_at`: When relationship was identified

**Purpose:** Group duplicate findings together, track frequency of mentions.

**Usage:** When generating reports, findings marked as duplicates can be:
- Grouped together with frequency count
- Shown as "mentioned 3 times across 2 conversations"
- Confidence boosted due to repetition

---

### 5. `patterns`

Stores detected patterns that suggest automation opportunities or recurring issues.

```sql
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_type TEXT NOT NULL CHECK(pattern_type IN ('automation_opportunity', 'recurring_bug', 'feature_request_pattern')),
    description TEXT NOT NULL,
    first_seen TIMESTAMP NOT NULL,
    last_seen TIMESTAMP NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 1,
    related_findings_json TEXT NOT NULL,  -- JSON array of finding IDs
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_pattern_type ON patterns(pattern_type);
CREATE INDEX idx_patterns_frequency ON patterns(frequency);
CREATE INDEX idx_patterns_confidence ON patterns(confidence);
```

**Columns:**

- `id`: Primary key, auto-increment
- `pattern_type`: Type of pattern detected
  - `automation_opportunity`: Repeated manual tasks
  - `recurring_bug`: Same bug mentioned multiple times
  - `feature_request_pattern`: Similar feature requests
- `description`: Human-readable description of pattern
- `first_seen`: When pattern was first detected
- `last_seen`: When pattern was last reinforced
- `frequency`: How many times pattern observed
- `related_findings_json`: JSON array of finding IDs that match this pattern
- `confidence`: How confident we are this is a real pattern
- `created_at`: When pattern was first created
- `updated_at`: When pattern was last updated

**Purpose:** Phase 5 intelligence feature - suggest projects based on patterns.

---

## Common Queries

### Get all high-priority TODOs from last 30 days

```sql
SELECT
    f.id,
    f.description,
    f.confidence,
    f.priority,
    c.file_path,
    s.line_number,
    f.created_at
FROM findings f
JOIN conversations c ON f.conversation_id = c.id
LEFT JOIN sources s ON f.id = s.finding_id
WHERE f.type = 'todo'
  AND f.priority IN ('high', 'critical')
  AND f.status = 'new'
  AND f.created_at >= datetime('now', '-30 days')
ORDER BY
    CASE f.priority
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        ELSE 4
    END,
    f.confidence DESC;
```

### Find duplicate findings

```sql
SELECT
    f1.id AS finding_1_id,
    f1.description AS finding_1,
    f2.id AS finding_2_id,
    f2.description AS finding_2,
    d.similarity,
    d.method
FROM deduplications d
JOIN findings f1 ON d.finding_id_1 = f1.id
JOIN findings f2 ON d.finding_id_2 = f2.id
WHERE d.similarity > 80
ORDER BY d.similarity DESC;
```

### Get conversation analysis statistics

```sql
SELECT
    COUNT(*) as total_conversations,
    SUM(findings_count) as total_findings,
    AVG(findings_count) as avg_findings_per_conversation,
    AVG(duration_seconds) as avg_analysis_time,
    MIN(analyzed_at) as first_analysis,
    MAX(analyzed_at) as latest_analysis
FROM conversations;
```

### Get breakdown by finding type and priority

```sql
SELECT
    type,
    priority,
    COUNT(*) as count,
    AVG(confidence) as avg_confidence
FROM findings
WHERE status = 'new'
GROUP BY type, priority
ORDER BY
    type,
    CASE priority
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        ELSE 4
    END;
```

### Find findings with multiple sources (mentioned in multiple places)

```sql
SELECT
    f.id,
    f.description,
    f.type,
    COUNT(s.id) as source_count,
    GROUP_CONCAT(s.file_path, '; ') as files
FROM findings f
JOIN sources s ON f.id = s.finding_id
GROUP BY f.id
HAVING source_count > 1
ORDER BY source_count DESC;
```

---

## Indexes Strategy

### Primary Indexes (Created Above)

- **conversations:** file_path (unique), analyzed_at, file_hash
- **findings:** type, confidence, priority, status, created_at
- **sources:** finding_id, file_path
- **deduplications:** finding pairs (unique), similarity

### Composite Indexes

For common query patterns:
- `(type, priority)` - Filter by type and sort by priority
- `(status, confidence)` - Find high-confidence new findings

### Why These Indexes?

1. **file_path:** Quick lookup to check if conversation already analyzed
2. **file_hash:** Detect changed files for re-analysis
3. **type + priority:** Common filtering in reports ("show me all high-priority bugs")
4. **status:** Separate new findings from confirmed/duplicates
5. **confidence:** Sort by confidence to show most reliable findings first

---

## Data Migration Strategy

### Version 1.0 (Current Design)

Initial schema as documented above.

### Future Migrations

**Planned migrations:**
1. Add `tags` table for custom categorization
2. Add `users` table if multi-user support needed
3. Add `exports` table to track generated reports

**Migration approach:**
- Use Alembic or custom migration scripts
- Store schema version in `schema_info` table
- Provide upgrade/downgrade paths

```sql
-- Track schema version
CREATE TABLE schema_info (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_info (version, description)
VALUES (1, 'Initial schema - conversations, findings, sources, deduplications, patterns');
```

---

## Data Retention Policy

### Conversations
**Retention:** Indefinite (user's local data)
**Cleanup:** User can manually delete old analyses

### Findings
**Retention:** Until marked as `completed` or `false_positive`
**Auto-cleanup:** Option to delete findings older than 1 year if status = completed

### Patterns
**Retention:** Indefinite (valuable historical data)
**Update:** Recompute periodically as new findings added

---

## Performance Considerations

### Expected Data Volumes

**Per user:**
- Conversations: 100-1,000 files
- Findings: 1,000-10,000 records
- Sources: 1,500-15,000 records (1.5x findings)
- Deduplications: 500-5,000 records
- Patterns: 10-100 records

**Database size estimate:** 10-100 MB per user

### Performance Targets

- **Insert finding:** < 10ms
- **Query high-priority TODOs:** < 50ms
- **Generate report:** < 500ms
- **Deduplication scan:** < 2 seconds

### Optimization Notes

- SQLite performs well for < 100K records
- Indexes cover all common queries
- If performance degrades, consider:
  - VACUUM to reclaim space
  - ANALYZE to update query planner statistics
  - Archiving old data to separate database

---

## Example Data

### Sample Conversation

```sql
INSERT INTO conversations (file_path, file_hash, model_used, duration_seconds, findings_count)
VALUES ('/home/user/Documents/Projects/my-app/conversation-2025-11-18.md',
        'a1b2c3d4e5f6...', 'qwen2.5:3b', 23.5, 8);
```

### Sample Finding

```sql
INSERT INTO findings (conversation_id, type, description, confidence, priority, metadata_json)
VALUES (1, 'todo', 'Implement password hashing with bcrypt', 95.0, 'high',
        '{"keywords": ["security", "password"], "urgency": "high"}');
```

### Sample Source

```sql
INSERT INTO sources (finding_id, file_path, line_number, context_before, context_after)
VALUES (1, '/home/user/Documents/Projects/my-app/conversation-2025-11-18.md', 42,
        'User: The login code is insecure.\n\nClaude: You should hash passwords.',
        'TODO: Implement password hashing with bcrypt\n\nUser: Good idea!');
```

---

## Testing Strategy

### Unit Tests

```python
def test_create_finding():
    # Test creating a finding with valid data
    finding = Finding(
        conversation_id=1,
        type='todo',
        description='Test TODO',
        confidence=85.0,
        priority='medium'
    )
    db.session.add(finding)
    db.session.commit()
    assert finding.id is not None

def test_duplicate_detection():
    # Test finding duplicates
    finding1 = Finding(...)
    finding2 = Finding(...)  # Similar to finding1

    similarity = compute_similarity(finding1, finding2)
    assert similarity > 80

    dedupe = Deduplication(
        finding_id_1=finding1.id,
        finding_id_2=finding2.id,
        similarity=similarity,
        method='fuzzy'
    )
    db.session.add(dedupe)
    db.session.commit()
```

### Integration Tests

```python
def test_full_analysis_workflow():
    # Test complete workflow: analyze → extract → store
    conversation = analyze_conversation('test.md')
    assert conversation.findings_count > 0

    findings = Finding.query.filter_by(conversation_id=conversation.id).all()
    assert len(findings) == conversation.findings_count

    # Verify sources created
    for finding in findings:
        assert len(finding.sources) > 0
```

---

## References

- **SQLite Documentation:** https://www.sqlite.org/docs.html
- **SQL Style Guide:** https://www.sqlstyle.guide/
- **Database Design Best Practices:** See RESEARCH.md

---

**Status:** Design complete, ready for Phase 4 implementation
**Next Steps:**
1. Create SQLAlchemy models based on this schema
2. Write migration script to create tables
3. Implement database access layer with proper error handling
4. Add comprehensive tests

**Document Version:** 1.0
**Last Updated:** 2025-11-18
