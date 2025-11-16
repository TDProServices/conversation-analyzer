# Usage Guide

## Quick Start

### 1. Analyze a Conversation File

```bash
python -m conversation_analyzer analyze tests/fixtures/conversations/sample_simple.md
```

This will:
1. Parse the conversation
2. Extract TODOs, bugs, features, and projects
3. Store results in the database
4. Display summary statistics

### 2. Generate a Report

```bash
python -m conversation_analyzer report
```

This creates a Markdown report in `data/reports/report.md`.

### 3. View Statistics

```bash
python -m conversation_analyzer stats
```

Shows a summary table of all extracted items.

## CLI Commands

### `analyze` - Analyze Files

Analyze conversations, code, or documents for action items.

**Syntax:**
```bash
python -m conversation_analyzer analyze <path> [options]
```

**Examples:**

```bash
# Analyze a single conversation
python -m conversation_analyzer analyze data/conversations/chat.md

# Analyze a directory
python -m conversation_analyzer analyze data/conversations/

# Analyze with custom config
python -m conversation_analyzer analyze data/ --config my_config.yaml

# Verbose output
python -m conversation_analyzer analyze data/ --verbose
```

**Options:**
- `--config, -c`: Path to config file
- `--verbose, -v`: Show detailed output including errors

### `report` - Generate Reports

Generate a report from analyzed items.

**Syntax:**
```bash
python -m conversation_analyzer report [options]
```

**Examples:**

```bash
# Generate Markdown report
python -m conversation_analyzer report --format markdown

# Generate JSON report
python -m conversation_analyzer report --format json

# Save to specific file
python -m conversation_analyzer report --output my_report.md

# Generate both formats
python -m conversation_analyzer report --format markdown --output report.md
python -m conversation_analyzer report --format json --output report.json
```

**Options:**
- `--format, -f`: Output format (`markdown` or `json`)
- `--output, -o`: Output file path
- `--config, -c`: Path to config file

### `stats` - View Statistics

Display database statistics in a table.

**Syntax:**
```bash
python -m conversation_analyzer stats [options]
```

**Example:**
```bash
python -m conversation_analyzer stats
```

**Output:**
```
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Metric              ┃ Count ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Total Items         │ 25    │
│   BUG               │ 10    │
│   TODO              │ 8     │
│   FEATURE           │ 5     │
│   PROJECT           │ 2     │
│                     │       │
│   High Priority     │ 12    │
│   Medium Priority   │ 8     │
│   Low Priority      │ 5     │
└─────────────────────┴───────┘
```

### `list` - List Items

List items from the database with filters.

**Syntax:**
```bash
python -m conversation_analyzer list [options]
```

**Examples:**

```bash
# List all items (first 20)
python -m conversation_analyzer list

# List only bugs
python -m conversation_analyzer list --type BUG

# List high priority items
python -m conversation_analyzer list --priority high

# List high priority bugs
python -m conversation_analyzer list --type BUG --priority high

# Show 50 items
python -m conversation_analyzer list --limit 50
```

**Options:**
- `--type, -t`: Filter by type (TODO, BUG, FEATURE, PROJECT)
- `--priority, -p`: Filter by priority (high, medium, low)
- `--limit, -l`: Maximum items to show (default: 20)
- `--config, -c`: Path to config file

### `test-connection` - Test Ollama Connection

Verify that Ollama is accessible.

**Syntax:**
```bash
python -m conversation_analyzer test-connection
```

**Success Output:**
```
✓ Successfully connected to Ollama
Host: http://localhost:11434
Model: nuextract
```

**Failure Output:**
```
✗ Cannot connect to Ollama
Start Ollama with: ollama serve
```

## Workflows

### Analyzing a New Project

```bash
# 1. Test connection
python -m conversation_analyzer test-connection

# 2. Place conversation files in data/conversations/
cp ~/Downloads/chat_export.md data/conversations/

# 3. Analyze
python -m conversation_analyzer analyze data/conversations/

# 4. View stats
python -m conversation_analyzer stats

# 5. Generate report
python -m conversation_analyzer report --output report.md

# 6. Review high priority items
python -m conversation_analyzer list --priority high
```

### Analyzing Code Comments

```bash
# Analyze Python files for TODO/FIXME comments
python -m conversation_analyzer analyze src/ --verbose

# List extracted items
python -m conversation_analyzer list --type TODO

# Generate report
python -m conversation_analyzer report
```

### Regular Updates

The analyzer tracks file hashes and skips unchanged files:

```bash
# First run - analyzes all files
python -m conversation_analyzer analyze data/

# Second run - only analyzes new/changed files
python -m conversation_analyzer analyze data/
```

## Configuration

### Custom Configuration File

Create `my_config.yaml`:

```yaml
ollama:
  host: "http://localhost:11434"
  extraction_model: "llama3.1:8b"  # Use larger model
  temperature: 0.05  # More deterministic

intelligence:
  deduplication:
    enabled: true
    similarity_threshold: 0.90  # Stricter deduplication

  priority_scoring:
    urgency_keywords: ["urgent", "critical", "asap", "now"]
    impact_keywords: ["breaks", "security", "data loss"]

reporting:
  group_by: "priority"  # Group by priority instead of type
```

Use it:
```bash
python -m conversation_analyzer analyze data/ --config my_config.yaml
```

### Environment Variables

Override settings via environment variables:

```bash
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=llama3.1:8b
export DATABASE_PATH=my_custom.db

python -m conversation_analyzer analyze data/
```

## File Formats

### Supported Input Formats

**Conversations:**
- Markdown (`.md`, `.markdown`)
- JSON (`.json`)

**Code:**
- Python (`.py`)
- JavaScript (`.js`)
- TypeScript (`.ts`, `.tsx`)
- Java (`.java`)
- C/C++ (`.c`, `.cpp`, `.h`, `.hpp`)
- Go (`.go`)
- Rust (`.rs`)
- Ruby (`.rb`)
- PHP (`.php`)
- Shell (`.sh`, `.bash`)

### Conversation Format Examples

**Markdown:**
```markdown
**User:** We need to fix the login bug.

**Assistant:** I'll look into it.

**User:** Also TODO: update the docs.
```

**JSON:**
```json
{
  "messages": [
    {"role": "user", "content": "We need to fix the login bug."},
    {"role": "assistant", "content": "I'll look into it."}
  ]
}
```

## Report Formats

### Markdown Report Structure

```markdown
# Conversation Analysis Report

## Summary
- Total Items: 25
- By Type: TODO (8), BUG (10), FEATURE (5), PROJECT (2)
- By Priority: High (12), Medium (8), Low (5)

## Items by Type

### BUGs (10)

#### 🐛 🔴 SQL injection vulnerability in login
- Type: BUG
- Priority: High (0.95)
- Confidence: 0.95
- Source: `src/auth.py`
- Line: 42
- Context: "...not sanitizing input..."
```

### JSON Report Structure

```json
{
  "generated_at": "2025-11-16T10:30:00",
  "total_items": 25,
  "items": [
    {
      "id": 1,
      "type": "BUG",
      "description": "SQL injection vulnerability in login",
      "priority": "high",
      "priority_score": 0.95,
      "confidence": 0.95,
      "source": {
        "type": "code",
        "file": "src/auth.py",
        "line": 42,
        "context": "..."
      }
    }
  ]
}
```

## Advanced Usage

### Python API

Use the analyzer programmatically:

```python
from conversation_analyzer.config import Config
from conversation_analyzer.analyzer import ConversationAnalyzer

# Load config
config = Config.load()

# Create analyzer
with ConversationAnalyzer(config) as analyzer:
    # Analyze files
    result = analyzer.analyze_file("data/chat.md")

    print(f"Extracted {result.items_extracted} items")

    # Get high priority items
    high_priority = analyzer.get_items(priority="high")

    # Generate report
    report = analyzer.generate_report("markdown")
    print(report)
```

### Custom Parsers

Add support for new file formats:

```python
from conversation_analyzer.parsers.base import BaseParser, ParsedChunk

class CustomParser(BaseParser):
    def can_parse(self, file_path: str) -> bool:
        return file_path.endswith(".custom")

    def get_source_type(self) -> str:
        return "custom"

    def parse(self, file_path: str) -> List[ParsedChunk]:
        # Your parsing logic
        pass
```

## Tips & Best Practices

### 1. Start with Small Batches

Test on a few files first to ensure extraction quality:

```bash
python -m conversation_analyzer analyze tests/fixtures/conversations/sample_simple.md
```

### 2. Review Confidence Scores

Low confidence items may need manual review. Filter in reports:

```python
# In code
items = [i for i in analyzer.get_items() if i.confidence < 0.7]
```

### 3. Adjust Thresholds

If you're getting too many false positives:

```yaml
extraction:
  confidence_threshold: 0.7  # Default is 0.5
```

### 4. Use Deduplication

Enable deduplication to merge similar items:

```yaml
intelligence:
  deduplication:
    enabled: true
    similarity_threshold: 0.85
```

### 5. Regular Analysis

Run analysis regularly on new conversations:

```bash
# Add to cron or scheduled task
python -m conversation_analyzer analyze data/conversations/
python -m conversation_analyzer report --output daily_report.md
```

## Troubleshooting

### No items extracted

**Possible causes:**
- File format not recognized
- Content doesn't match extraction patterns
- Confidence threshold too high

**Solutions:**
- Check file extension
- Review sample data for patterns
- Lower confidence threshold
- Use `--verbose` to see errors

### Slow extraction

**Possible causes:**
- Large files
- Slow model (llama3.1 vs nuextract)
- Network latency to Ollama

**Solutions:**
- Use nuextract model (faster)
- Chunk large files
- Ensure Ollama is running locally

### Too many duplicates

**Solutions:**
- Increase similarity threshold:
  ```yaml
  deduplication:
    similarity_threshold: 0.90  # Higher = stricter
  ```

### Items have wrong priority

**Solutions:**
- Adjust priority keywords in config
- Use custom scoring logic
- Manually review and adjust

## Getting Help

- **Documentation:** Check README.md, DESIGN.md, and RESEARCH_REPORT.md
- **Issues:** https://github.com/TDProServices/conversation-analyzer/issues
- **Examples:** See `tests/fixtures/` for sample data

## Next Steps

- Explore the [RESEARCH_REPORT.md](../RESEARCH_REPORT.md) for technical details
- Review the [DESIGN.md](../DESIGN.md) for architecture
- Check the test fixtures for examples
- Customize the config for your workflow
