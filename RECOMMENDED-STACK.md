# Recommended Technology Stack - Quick Reference

**Date:** 2025-11-19
**Status:** Ready for Implementation
**Full Research:** See RESEARCH-FINDINGS-2024-2025.md

---

## TL;DR - Use These Libraries

### Must Use (Core Stack)
```toml
[tool.poetry.dependencies]
python = "^3.10"

# LLM Integration - Replaces custom Ollama client
litellm = "^1.50.0"        # Unified LLM interface with retry/timeout
instructor = "^1.0.0"       # Structured extraction with Pydantic

# Database - Replaces raw SQLite
sqlmodel = "^0.0.18"        # SQLAlchemy + Pydantic in one
pydantic = "^2.5.0"         # Data validation

# Document Parsing - Replaces custom markdown parser
markdown-analysis = "^0.1.0"  # Extract TODO lists from markdown
markdown-it-py = "^3.0.0"     # General markdown parsing

# Deduplication - Replaces custom fuzzy matching
dedupe = "^3.0.3"           # OR text-dedup = "^0.3.0"

# CLI & Utilities
typer = "^0.12.0"           # CLI framework (better than argparse)
rich = "^13.0.0"            # Beautiful terminal output
python-dotenv = "^1.0.0"    # Environment variables

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
pytest-asyncio = "^0.23.0"
ruff = "^0.3.0"            # Linting (replaces flake8/pylint)
black = "^24.0.0"          # Formatting
mypy = "^1.8.0"            # Type checking
```

### External Tools
- **ripgrep** - Fast file scanning (already required by project)
- **Docker** - Reproducible environment (recommended)
- **Ollama** - Local LLM (already required)

---

## Time Savings

| Component | Build Custom | Use Library | Time Saved |
|-----------|--------------|-------------|------------|
| LLM client with retry/timeout | 12-16h | LiteLLM (0h) | 12-16h |
| Structured extraction | 8-12h | Instructor (0h) | 8-12h |
| Database ORM | 8-12h | SQLModel (0h) | 8-12h |
| Markdown parsing | 6-8h | markdown-analysis (0h) | 6-8h |
| Deduplication algorithm | 16-24h | dedupe (0h) | 16-24h |
| **TOTAL** | **50-72h** | **~10h integration** | **40-62h** |

**Conclusion:** Save 40-60 hours by using existing tools

---

## What We Still Need to Build

### 1. Claude Code JSONL Parser (8-12h)
**Why:** No existing tool parses Claude Code's conversation format
**Approach:** Study https://github.com/ZeroSumQuant/claude-conversation-extractor and replicate in Python

```python
# Read from ~/.claude/projects/*/conversations/*.jsonl
def parse_claude_conversation(jsonl_path):
    # Parse JSONL format
    # Extract user/assistant messages
    # Handle artifacts, tool calls
    pass
```

### 2. Conversation-Specific Extraction (16-24h)
**Why:** Generic extractors don't understand coding conversations
**Approach:** Use Instructor with custom prompts

```python
from instructor import from_ollama
from pydantic import BaseModel

class TodoItem(BaseModel):
    description: str
    type: str  # "todo", "bug", "feature"
    priority: str
    confidence: float
    source_quote: str

# Use with LiteLLM + Ollama
```

### 3. Multi-Source Orchestration (12-16h)
**Why:** Need to coordinate scanning conversations, code, markdown, git
**Approach:** Build orchestration layer using found libraries

### 4. Priority Scoring (6-8h)
**Why:** Need custom algorithm for coding-specific priorities
**Approach:** Heuristics + LLM scoring

### 5. Report Generation (4-6h)
**Why:** Need specific markdown format
**Approach:** Jinja2 templates + SQLModel queries

**Total Custom Code:** 46-66 hours (vs 120-160h if building everything)

---

## Quick Start Commands

### 1. Install Dependencies
```bash
# Using pip
pip install litellm instructor sqlmodel markdown-analysis dedupe typer rich python-dotenv

# Using poetry (recommended)
poetry add litellm instructor sqlmodel markdown-analysis dedupe typer rich python-dotenv
poetry add --group dev pytest ruff black mypy
```

### 2. Test Ollama Connection
```python
from litellm import completion

response = completion(
    model="ollama/qwen2.5:3b",
    messages=[{"role": "user", "content": "Extract TODOs from: I need to fix the bug"}],
    api_base="http://localhost:11434"
)
print(response.choices[0].message.content)
```

### 3. Test Structured Extraction
```python
import instructor
from ollama import Client
from pydantic import BaseModel

class ActionItem(BaseModel):
    task: str
    priority: str

client = instructor.from_ollama(Client())
result = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "I need to refactor the auth module"}],
    response_model=ActionItem
)
print(result.task, result.priority)
```

### 4. Test Markdown TODO Extraction
```python
from markdown_analysis import MarkdownAnalyzer

markdown = """
# My TODOs
- [ ] Fix authentication bug
- [x] Add tests
- [ ] Deploy to production
"""

analyzer = MarkdownAnalyzer(markdown)
tasks = analyzer.extract_tasks()
print(tasks)
```

### 5. Test Database
```python
from sqlmodel import SQLModel, Field, create_engine, Session

class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    type: str

engine = create_engine("sqlite:///test.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    todo = TodoItem(description="Test task", type="todo")
    session.add(todo)
    session.commit()
    print("Saved!")
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Invokes CLI                      │
│                    (Typer framework)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Multi-Source Scanner                      │
│              (Custom orchestration)                      │
└─┬──────────┬──────────┬──────────┬────────────────────┬─┘
  │          │          │          │                    │
  ▼          ▼          ▼          ▼                    ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         ┌──────────┐
│Claude│  │TODO  │  │ Code │  │ Git  │         │  Other   │
│Code  │  │.md   │  │Cmts  │  │Logs  │         │  Docs    │
│JSONL │  │Files │  │      │  │      │         │          │
└──┬───┘  └───┬──┘  └───┬──┘  └───┬──┘         └─────┬────┘
   │          │         │         │                   │
   │(CUSTOM)  │(lib)    │(rg)     │(rg)              │(lib)
   │          │         │         │                   │
   ▼          ▼         ▼         ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│              markdown-analysis                            │
│              markdown-it-py                               │
│              ripgrep subprocess                           │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              LLM-Based Extraction                        │
│              (LiteLLM + Instructor)                      │
│              Ollama: qwen2.5:3b or llama3.1:8b          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Deduplication Layer                         │
│              (dedupe or text-dedup)                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Priority Scoring                            │
│              (Custom algorithm)                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              SQLite Database                             │
│              (SQLModel ORM)                              │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Report Generator                            │
│              (Jinja2 templates)                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
                 Markdown Report
```

**Legend:**
- **(CUSTOM)** = We must build this
- **(lib)** = Use existing library
- **(rg)** = Use ripgrep subprocess

---

## Docker Setup (Recommended)

### Dockerfile
```dockerfile
FROM python:3.10-slim

# Install ripgrep
RUN apt-get update && apt-get install -y ripgrep && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install poetry && poetry install --no-dev

# Copy application
COPY src/ ./src/

CMD ["poetry", "run", "python", "-m", "conversation_analyzer"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  analyzer:
    build: .
    volumes:
      - ~/.claude:/root/.claude:ro    # Read Claude Code logs
      - ./reports:/app/reports          # Output
      - ./data:/app/data                # Database
    environment:
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_models:/root/.ollama
    ports:
      - "11434:11434"

volumes:
  ollama_models:
```

### Usage
```bash
# Build and start
docker-compose up -d

# Run analysis
docker-compose exec analyzer python -m conversation_analyzer scan

# View reports
cat reports/analysis-$(date +%Y-%m-%d).md
```

---

## Critical Findings from Research

### 1. Claude Code Conversation Extractor EXISTS!
**GitHub:** https://github.com/ZeroSumQuant/claude-conversation-extractor

This tool already knows how to read `~/.claude/projects/**/*.jsonl` - we MUST study its approach!

### 2. Instructor Library is Perfect for This
Instructor + Ollama = type-safe extraction with Pydantic models. Exactly what we need.

### 3. markdown-analysis Handles TODO Lists
No need to parse `- [ ]` and `- [x]` ourselves - library does it.

### 4. LiteLLM Saves Massive Time
Retry logic, timeout handling, fallbacks, logging - all built-in. Don't reinvent.

### 5. SQLModel = SQLAlchemy + Pydantic
One model definition for both DB and validation. Perfect for our needs.

---

## Risk Mitigation

### If Library Doesn't Work
- **LiteLLM fails:** Fallback to direct Ollama HTTP API
- **Instructor fails:** Fallback to manual JSON parsing
- **dedupe fails:** Use text-dedup or simple Levenshtein
- **markdown-analysis fails:** Use markdown-it-py
- **SQLModel fails:** Use raw SQLAlchemy

### Version Compatibility
```bash
# Pin all versions in pyproject.toml
litellm = "^1.50.0"  # Not ">=1.50.0" or "*"
```

### Testing Strategy
```python
# Test each library integration in isolation first
def test_litellm_ollama():
    # Verify LiteLLM works with local Ollama
    pass

def test_instructor_extraction():
    # Verify structured extraction
    pass

def test_deduplication():
    # Verify dedupe accuracy
    pass
```

---

## Next Steps (Priority Order)

1. **TODAY:** Create pyproject.toml with dependencies
2. **TODAY:** Test Ollama + LiteLLM connection
3. **TODAY:** Test Instructor extraction
4. **TOMORROW:** Study claude-conversation-extractor source code
5. **TOMORROW:** Implement JSONL parser
6. **THIS WEEK:** Build MVP with core libraries
7. **NEXT WEEK:** Add deduplication and multi-source scanning

---

## Questions to Answer During Implementation

### Week 1
- [ ] Does LiteLLM work reliably with Ollama?
- [ ] Can Instructor extract TODOs with 80%+ accuracy?
- [ ] Is qwen2.5:3b fast enough, or do we need llama3.1:8b?
- [ ] Does markdown-analysis handle all TODO.md formats?

### Week 2
- [ ] Does dedupe work well for TODO deduplication?
- [ ] How do we handle cross-conversation references?
- [ ] What's the optimal confidence threshold?
- [ ] Do we need rate limiting for Ollama?

### Week 3
- [ ] Is Docker adding value or complexity?
- [ ] Should we use LangChain document loaders?
- [ ] Do we need spaCy for entity extraction?
- [ ] Is BERTopic necessary for pattern detection?

---

## Success Criteria

### Week 1 - MVP
- [x] Research complete (this document)
- [ ] Dependencies installed
- [ ] Ollama integration working
- [ ] Parse one Claude Code conversation
- [ ] Extract TODOs with 70%+ accuracy
- [ ] Store in SQLite
- [ ] Generate markdown report

### Week 2 - Intelligence
- [ ] Scan TODO.md files
- [ ] Scan code comments with ripgrep
- [ ] Deduplication working
- [ ] Priority scoring implemented
- [ ] 80%+ extraction accuracy

### Week 3 - Scale
- [ ] Batch processing
- [ ] Scan all projects in ~/Documents/Projects/
- [ ] Daily reports automated
- [ ] Performance < 5 min per conversation

### Week 4 - Polish
- [ ] Docker setup complete
- [ ] Documentation for beginners
- [ ] Tests for core components
- [ ] GitHub Actions CI/CD

---

## Resources

- **Full Research Report:** `/home/user/conversation-analyzer/RESEARCH-FINDINGS-2024-2025.md`
- **Project Instructions:** `/home/user/conversation-analyzer/CLAUDE.md`
- **TODO Tracking:** `/home/user/conversation-analyzer/TODO.md`

---

**Last Updated:** 2025-11-19
**Status:** ✅ Ready to implement
**Confidence:** High - all libraries tested in real-world projects
