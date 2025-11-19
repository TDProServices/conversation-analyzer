# Research Findings: Conversation Analysis Tools & Frameworks (2024-2025)

**Date:** 2025-11-19
**Researcher:** Claude Code
**Project:** conversation-analyzer
**Purpose:** Identify existing tools to compose/adapt before building custom solutions

---

## Executive Summary

This research evaluated existing tools and frameworks from 2024-2025 that could be used or adapted for analyzing Claude Code conversations to extract TODOs, bugs, and feature requests. The findings show that **no single tool meets all requirements**, but several high-quality libraries can be composed to create an effective solution with 60-70% less custom code than building from scratch.

### Key Recommendations

1. **Use LangChain** for document parsing and structured extraction (replaces custom parsers)
2. **Use markdown-analysis** for parsing markdown files including TODO lists
3. **Use LiteLLM** as a unified interface to Ollama (handles retries, timeouts, fallbacks)
4. **Use SQLModel** for database ORM (combines SQLAlchemy + Pydantic validation)
5. **Use dedupe or text-dedup** for intelligent deduplication
6. **Use ripgrep directly** via subprocess for fast file scanning (already required)
7. **Build custom** conversation-specific extraction logic and Claude Code format parsing

**Estimated Development Time Savings:** 40-50 hours by using existing libraries

---

## Category 1: Conversation & Chat Analysis Tools

### 1.1 Meetily - Open Source Meeting Assistant

**GitHub:** https://meetily.zackriya.com/
**Status:** Active (2024)
**Language:** Python
**Installation:** Self-hosted, requires local setup

**Key Features:**
- 100% local processing (privacy-first)
- Real-time transcription with Whisper.cpp
- Automatic action item extraction
- Key points and decisions identification
- Custom HyperLLM-V1 model for meeting summarization

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Action item extraction, local processing, open source
- **Cons:** Focused on audio/meeting transcripts, not text conversations
- **Adaptation Potential:** Could study their action item extraction prompts

**Recommendation:** Study implementation for prompt engineering ideas, but don't integrate directly

---

### 1.2 Chatistics - Multi-Platform Chat Parser

**GitHub:** https://github.com/MasterScrat/Chatistics
**Status:** Active
**Language:** Python
**Installation:** `pip install chatistics`

**Key Features:**
- Parses Messenger, Hangouts, WhatsApp, Telegram logs
- Converts chats to pandas DataFrames
- Exports to pickle files for analysis
- Supports raw text output

**Relevance to Our Use Case:** ⭐⭐ (Low-Medium)
- **Pros:** Battle-tested chat parsing, DataFrame output
- **Cons:** Doesn't support Claude format, no extraction logic
- **Adaptation Potential:** Could use as reference for conversation structure

**Recommendation:** Reference architecture only, don't integrate

---

### 1.3 Claude Conversation Extractor

**GitHub:** https://github.com/ZeroSumQuant/claude-conversation-extractor
**Status:** Active (2024)
**Language:** JavaScript
**Installation:** Browser tool

**Key Features:**
- Extracts Claude Code conversations from `~/.claude/projects`
- Reads JSONL format logs
- Only tool specifically for Claude Code

**Relevance to Our Use Case:** ⭐⭐⭐⭐⭐ (Critical!)
- **Pros:** Exactly what we need for Claude Code log access
- **Cons:** JavaScript, not Python (but could use same approach)
- **Adaptation Potential:** **Must implement similar logic in Python**

**Recommendation:** **HIGH PRIORITY** - Study source code and replicate in Python

**Action Items:**
1. Clone repo and analyze JSONL parsing logic
2. Implement Python version for reading `~/.claude/projects/**/*.jsonl`
3. Handle Claude Code's specific format

---

### 1.4 Claude Export Tools (Browser Extensions)

**Tools Found:**
- Claude Exporter (Chrome extension) - PDF, MD, TXT, CSV, JSON export
- claude-export (GitHub) - Browser script for MD, JSON, PNG export
- Claude Chat Exporter - Perfect markdown fidelity

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Handles Claude.ai web format exports
- **Cons:** Browser-based, manual export required
- **Adaptation Potential:** Study export formats

**Recommendation:** Support exported markdown files as alternative input format

---

### 1.5 transcript-seeker - Meeting Transcript Manager

**GitHub:** https://github.com/meeting-baas/transcript-seeker
**Status:** Active (2024)
**Language:** JavaScript/Browser
**Installation:** Browser-based

**Key Features:**
- Browser-based transcript viewer
- Upload and transcribe meeting recordings
- AI chat with transcripts
- Note-taking integration

**Relevance to Our Use Case:** ⭐⭐ (Low)
- **Pros:** AI-powered transcript analysis
- **Cons:** Browser-based, meeting-focused
- **Adaptation Potential:** UI inspiration only

**Recommendation:** Skip integration, different use case

---

## Category 2: TODO & Action Item Extraction

### 2.1 ripgrep + Todo Tree Pattern

**GitHub:** https://github.com/Gruntfuggly/todo-tree (VS Code extension)
**Status:** Active (2024)
**Language:** JavaScript (uses ripgrep binary)
**Installation:** VS Code extension

**Key Features:**
- Uses ripgrep for fast TODO/FIXME/BUG/HACK scanning
- Regex patterns: `(TODO|FIXME|BUG|HACK|XXX)`
- Supports custom tag configuration
- Tree view organization

**Relevance to Our Use Case:** ⭐⭐⭐⭐ (High)
- **Pros:** Proven pattern, battle-tested regex, fast
- **Cons:** VS Code extension (but can use approach)
- **Adaptation Potential:** **Use exact approach with Python subprocess**

**Recommendation:** **IMPLEMENT THIS PATTERN**

**Implementation:**
```python
import subprocess
import json

def scan_todos(directory):
    result = subprocess.run(
        ['rg', '--json', r'(TODO|FIXME|BUG|HACK|XXX|NOTE)', directory],
        capture_output=True,
        text=True
    )
    # Parse JSON output
    return [json.loads(line) for line in result.stdout.split('\n') if line]
```

---

### 2.2 markdown-analysis Library

**PyPI:** https://pypi.org/project/markdown-analysis/
**Status:** Active (2024)
**Language:** Python
**Installation:** `pip install markdown-analysis`

**Key Features:**
- Extensive markdown parsing
- **Task list extraction** (- [ ], - [x])
- Understands hierarchy and structure
- Extracts various elements from markdown

**Relevance to Our Use Case:** ⭐⭐⭐⭐⭐ (Critical!)
- **Pros:** **Exactly what we need** for TODO.md parsing
- **Cons:** None identified
- **Adaptation Potential:** Use directly

**Recommendation:** **MUST USE** - Primary tool for markdown TODO extraction

**Usage Example:**
```python
from markdown_analysis import MarkdownAnalyzer

analyzer = MarkdownAnalyzer(markdown_content)
tasks = analyzer.extract_tasks()
# Returns structured task data with checkboxes, hierarchy
```

---

### 2.3 Instructor Library - Action Item Extraction

**GitHub:** https://python.useinstructor.com/
**Status:** Very Active (2024)
**Language:** Python
**Installation:** `pip install instructor`

**Key Features:**
- Extract structured data from LLM responses using Pydantic
- Specifically designed for action item extraction
- Works with OpenAI API and **Ollama**
- Type-safe extraction with validation

**Relevance to Our Use Case:** ⭐⭐⭐⭐⭐ (Critical!)
- **Pros:** **Perfect for LLM-based extraction**, Ollama support, Pydantic validation
- **Cons:** Designed for cloud LLMs primarily (but supports Ollama)
- **Adaptation Potential:** Use directly with Ollama

**Recommendation:** **MUST USE** - Core library for LLM extraction

**Usage Example:**
```python
import instructor
from pydantic import BaseModel
from ollama import Client

class ActionItem(BaseModel):
    task: str
    priority: str
    confidence: float

client = instructor.from_ollama(Client())
response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": conversation}],
    response_model=ActionItem
)
```

---

## Category 3: LLM Integration & Frameworks

### 3.1 LangChain - Document Analysis & Extraction

**Docs:** https://python.langchain.com/docs/tutorials/extraction/
**Status:** Very Active (2024-2025)
**Language:** Python
**Installation:** `pip install langchain`

**Key Features:**
- Open-source extraction service (2024)
- Structured data extraction from unstructured text
- Doctran property extractor with "action_item" classification
- Document loaders for PDF, markdown, text
- Chunking and context management
- Agent workflows with LangGraph

**Relevance to Our Use Case:** ⭐⭐⭐⭐ (High)
- **Pros:** Industry standard, robust extraction, document loaders, active development
- **Cons:** Heavy framework, might be overkill for simple use case
- **Adaptation Potential:** Use selectively (document loaders, extraction chains)

**Recommendation:** **USE SELECTIVELY** - Use document loaders and extraction patterns, skip full framework

**Useful Components:**
- Document loaders for markdown/text files
- Text splitters for chunking large conversations
- Extraction chain patterns
- Prompt templates

---

### 3.2 LiteLLM - Unified LLM Interface

**Docs:** https://docs.litellm.ai/
**Status:** Very Active (2024-2025)
**Language:** Python
**Installation:** `pip install litellm`

**Key Features:**
- Unified interface to 100+ LLM providers (OpenAI, Ollama, etc.)
- Built-in retries, timeouts, fallbacks
- Logging and callbacks
- Provider-agnostic (switch models with single string change)
- Native Ollama support with `ollama/` prefix

**Relevance to Our Use Case:** ⭐⭐⭐⭐⭐ (Critical!)
- **Pros:** **Exactly what we need** for Ollama integration, handles all edge cases
- **Cons:** None for our use case
- **Adaptation Potential:** Use directly as primary LLM client

**Recommendation:** **MUST USE** - Replace direct Ollama client

**Usage Example:**
```python
from litellm import completion

response = completion(
    model="ollama/qwen2.5:3b",
    messages=[{"role": "user", "content": prompt}],
    api_base="http://localhost:11434",
    timeout=30,
    max_retries=3
)
```

**Version Requirements:** LiteLLM 1.41.27+ for Ollama function calling

---

### 3.3 spaCy + spaCy-LLM - NLP with LLM Integration

**Website:** https://spacy.io/
**Status:** Very Active (2024)
**Language:** Python
**Installation:** `pip install spacy spacy-llm`

**Key Features:**
- Industrial-strength NLP library
- Named entity recognition
- Dependency parsing
- Pattern matching (Matcher class)
- spacy-llm package for LLM integration
- Fast and production-ready

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Powerful NLP, could extract entities from conversations
- **Cons:** Might be overkill, adds complexity
- **Adaptation Potential:** Use for advanced entity extraction if needed

**Recommendation:** **OPTIONAL** - Evaluate in Phase 2 if simple extraction insufficient

**Potential Use Cases:**
- Extract person names, dates, project names from conversations
- Identify technical terms and concepts
- Advanced pattern matching for implicit TODOs

---

### 3.4 BERTopic - Topic Modeling

**GitHub:** https://github.com/MaartenGr/BERTopic
**Docs:** https://maartengr.github.io/BERTopic/
**Status:** Very Active (2024)
**Language:** Python
**Installation:** `pip install bertopic`

**Key Features:**
- BERT-based topic modeling
- Handles both long and short texts
- Online/incremental learning (`.partial_fit`)
- Easily interpretable topics
- Guided topic modeling

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Could cluster similar TODOs/issues across conversations
- **Cons:** Complex, might be overkill for initial version
- **Adaptation Potential:** Use in Phase 4 for pattern detection

**Recommendation:** **FUTURE ENHANCEMENT** - For cross-conversation pattern analysis

**Use Cases:**
- Cluster similar pain points across multiple conversations
- Identify recurring themes in feature requests
- Detect project patterns (e.g., "authentication issues" theme)

---

## Category 4: Data Management & Deduplication

### 4.1 SQLModel - ORM with Pydantic

**Docs:** https://sqlmodel.tiangolo.com/
**Status:** Active (2024)
**Language:** Python
**Installation:** `pip install sqlmodel`

**Key Features:**
- Combines SQLAlchemy ORM + Pydantic validation
- Single model for DB and API validation
- Type safety with autocompletion
- SQLite support
- FastAPI integration

**Relevance to Our Use Case:** ⭐⭐⭐⭐⭐ (Critical!)
- **Pros:** **Perfect for our needs** - SQLite + validation in one
- **Cons:** None identified
- **Adaptation Potential:** Use directly

**Recommendation:** **MUST USE** - Primary database ORM

**Usage Example:**
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime

class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    type: str  # todo, bug, feature
    source_file: str
    confidence: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

engine = create_engine("sqlite:///conversation_analyzer.db")
SQLModel.metadata.create_all(engine)
```

---

### 4.2 dedupe - Fuzzy Matching & Deduplication

**GitHub:** https://github.com/dedupeio/dedupe
**PyPI:** https://pypi.org/project/dedupe/
**Status:** Active (2024, version 3.0.3 uploaded Aug 2024)
**Language:** Python
**Installation:** `pip install dedupe`

**Key Features:**
- Machine learning-based fuzzy matching
- Record deduplication and entity resolution
- Fast and scalable
- Actively maintained

**Relevance to Our Use Case:** ⭐⭐⭐⭐ (High)
- **Pros:** **Exactly what we need** for smart deduplication
- **Cons:** Might need training data
- **Adaptation Potential:** Use directly for TODO deduplication

**Recommendation:** **USE FOR DEDUPLICATION** - Better than simple string matching

**Alternative:** text-dedup for embedding-based deduplication

---

### 4.3 text-dedup - Modern Deduplication Methods

**GitHub:** https://github.com/ChenghaoMou/text-dedup
**PyPI:** https://pypi.org/project/text-dedup/
**Status:** Active (2024)
**Language:** Python
**Installation:** `pip install text-dedup`

**Key Features:**
- Embedding-based deduplication (RETSim/UniSim)
- MinHash + MinHashLSH
- Spark implementation for large datasets
- Multiple algorithms (SuperMinHash, ProbMinHash, TreeMinHash)

**Relevance to Our Use Case:** ⭐⭐⭐⭐ (High)
- **Pros:** Modern approach, semantic similarity
- **Cons:** Requires Python 3.10+ (we meet this)
- **Adaptation Potential:** Use for semantic deduplication

**Recommendation:** **EVALUATE BOTH** - Compare with dedupe, choose best fit

**Use Case:**
```python
from text_dedup import MinHashDeduplicator

deduplicator = MinHashDeduplicator(threshold=0.8)
unique_todos = deduplicator.deduplicate(todo_list)
```

---

### 4.4 recordlinkage - Data Matching Library

**Docs:** https://recordlinkage.readthedocs.io/
**Status:** Active (2024)
**Language:** Python
**Installation:** `pip install recordlinkage`

**Key Features:**
- String similarity (Jaro-Winkler, Levenshtein)
- Numerical and date comparisons
- Multiple comparison techniques
- Requires Python 3.8+

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Comprehensive similarity metrics
- **Cons:** More complex than needed
- **Adaptation Potential:** Use for advanced matching

**Recommendation:** **BACKUP OPTION** - If dedupe/text-dedup insufficient

---

## Category 5: Markdown & Document Parsing

### 5.1 markdown-it-py - CommonMark Parser

**GitHub:** https://github.com/executablebooks/markdown-it-py
**Status:** Very Active (2024)
**Language:** Python
**Installation:** `pip install markdown-it-py`

**Key Features:**
- 100% CommonMark support
- Extensions and syntax plugins
- High speed
- Ported from JavaScript markdown-it

**Relevance to Our Use Case:** ⭐⭐⭐⭐ (High)
- **Pros:** Fast, spec-compliant, extensible
- **Cons:** Lower-level than markdown-analysis
- **Adaptation Potential:** Use if need custom parsing logic

**Recommendation:** **SECONDARY OPTION** - Use if markdown-analysis insufficient

---

### 5.2 mistletoe - Fast Markdown Parser

**GitHub:** https://github.com/miyuchina/mistletoe
**Status:** Active (2024)
**Language:** Python (pure)
**Installation:** `pip install mistletoe`

**Key Features:**
- Fast and spec-compliant
- Pure Python
- Extensible with custom tokens
- Easy customization

**Relevance to Our Use Case:** ⭐⭐⭐ (Medium)
- **Pros:** Pure Python, fast, customizable
- **Cons:** Lower-level API
- **Adaptation Potential:** Use for custom parsing needs

**Recommendation:** **TERTIARY OPTION** - Backup if others don't fit

---

### 5.3 Python-Markdown - Standard Library Alternative

**Docs:** https://python-markdown.github.io/
**Status:** Stable (2024)
**Language:** Python
**Installation:** `pip install markdown`

**Key Features:**
- Long-established standard
- Extension system
- Well-documented

**Relevance to Our Use Case:** ⭐⭐ (Low-Medium)
- **Pros:** Stable, well-known
- **Cons:** Slower than alternatives, less modern
- **Adaptation Potential:** Fallback option

**Recommendation:** **SKIP** - Better alternatives exist

---

## Gaps Requiring Custom Code

Based on research, the following components have **no existing tools** and must be built custom:

### 1. Claude Code Conversation Format Parser
**Gap:** No existing parser for Claude Code's specific conversation format

**What We Need:**
- Parse JSONL files from `~/.claude/projects/*/conversations/*.jsonl`
- Extract user/assistant message pairs
- Handle artifacts, file references, tool calls
- Preserve conversation context and flow

**Approach:** Study claude-conversation-extractor (JavaScript) and replicate in Python

**Estimated Effort:** 8-12 hours

---

### 2. Conversation-Specific Extraction Logic
**Gap:** Generic action item extractors don't understand coding conversations

**What We Need:**
- Detect implicit TODOs: "I need to...", "We should...", "Don't forget to..."
- Identify bugs: "This is broken", "Error when...", "Doesn't work..."
- Find feature requests: "It would be nice if...", "We need a way to..."
- Understand code context (not just natural language)

**Approach:**
- Use Instructor library with custom Pydantic models
- Craft specialized prompts for coding conversations
- Test/refine on real Claude Code conversations

**Estimated Effort:** 16-24 hours (includes prompt engineering)

---

### 3. Multi-Source Aggregation
**Gap:** No tool aggregates from conversations + code + git + docs

**What We Need:**
- Scan multiple source types (conversations, markdown, code, commits)
- Normalize findings from different sources
- Cross-reference related items
- Track source provenance

**Approach:** Build orchestration layer using found libraries

**Estimated Effort:** 12-16 hours

---

### 4. Priority Scoring Algorithm
**Gap:** Generic extractors don't score priority/urgency

**What We Need:**
- Score based on urgency keywords ("critical", "blocking", "urgent")
- Consider recency (recent mentions = higher priority)
- Factor in frequency (multiple mentions)
- Domain weighting (legal/medical = higher priority)

**Approach:** Custom scoring function combining heuristics + LLM

**Estimated Effort:** 6-8 hours

---

### 5. Report Generation
**Gap:** No tool generates our specific report format

**What We Need:**
- Markdown reports with sections (High/Medium/Low priority)
- Statistics (items found, duplicates, processing time)
- Source references with line numbers
- Suggested actions

**Approach:** Jinja2 templates with SQLModel queries

**Estimated Effort:** 4-6 hours

---

## Recommended Technology Stack

Based on research findings, here's the recommended stack:

### Core Libraries (Must Use)
```python
# LLM Integration
litellm==1.50.0+           # Unified LLM interface with retry/timeout
instructor==1.0.0+         # Structured extraction with Pydantic

# Database & Models
sqlmodel==0.0.18+          # ORM + Pydantic validation
pydantic==2.5.0+           # Data validation (dependency of above)

# Document Parsing
markdown-analysis==0.1.0+  # TODO list extraction from markdown
markdown-it-py==3.0.0+     # General markdown parsing

# Deduplication
dedupe==3.0.3+             # Fuzzy matching & deduplication
# OR
text-dedup==0.3.0+         # Embedding-based deduplication

# Utilities
python-dotenv==1.0.0+      # Environment configuration
rich==13.0.0+              # Beautiful CLI output
typer==0.12.0+             # CLI framework
```

### Optional Libraries (Evaluate Later)
```python
# Advanced Analysis (Phase 2+)
langchain==0.1.0+          # If need document loaders
spacy==3.7.0+              # If need NER/entity extraction
bertopic==0.16.0+          # If need topic modeling

# Testing & Quality
pytest==8.0.0+             # Testing framework
pytest-asyncio==0.23.0+    # Async testing
ruff==0.3.0+               # Linting
black==24.0.0+             # Formatting
mypy==1.8.0+               # Type checking
```

### External Tools
```bash
# Already Required
ripgrep                     # Fast file scanning

# Recommended
docker                      # Reproducible environment
ollama                      # Local LLM (already required)
```

---

## Development Phases with Libraries

### Phase 1: MVP (Weeks 1-2)

**Goal:** Basic TODO extraction from conversations

**Libraries to Use:**
- LiteLLM (Ollama client)
- Instructor (extraction)
- SQLModel (database)
- markdown-it-py (parsing)
- Typer (CLI)

**Custom Code:**
- Claude Code JSONL parser
- Basic extraction prompts
- Simple report generator

**Deliverable:** CLI tool that scans one conversation and outputs markdown report

---

### Phase 2: Intelligence (Weeks 3-4)

**Goal:** Add deduplication and multi-source scanning

**Libraries to Add:**
- dedupe or text-dedup (deduplication)
- markdown-analysis (TODO.md parsing)

**Custom Code:**
- Multi-source scanner
- Deduplication logic
- Priority scoring
- Cross-referencing

**Deliverable:** Scan multiple sources with smart deduplication

---

### Phase 3: Scale (Week 5)

**Goal:** Batch processing and automation

**Libraries to Add:**
- watchdog (optional, for file watching)

**Custom Code:**
- Batch processor
- Incremental scanning
- Performance optimization

**Deliverable:** Daily automated reports

---

### Phase 4: Patterns (Week 6+)

**Goal:** Project pattern detection

**Libraries to Add:**
- BERTopic (topic modeling)
- spaCy (entity extraction)

**Custom Code:**
- Pattern detection algorithms
- Project suggestion generator

**Deliverable:** Automated project opportunity detection

---

## Installation & Setup Recommendations

### Docker Configuration

**Recommendation:** **YES, use Docker** (user wants this evaluated)

**Benefits:**
- Consistent environment across machines
- Easy Ollama integration
- Reproducible builds
- Simplified dependencies

**Docker Compose Structure:**
```yaml
version: '3.8'
services:
  analyzer:
    build: .
    volumes:
      - ~/.claude:/root/.claude:ro  # Read Claude Code logs
      - ./reports:/app/reports        # Output reports
      - ./data:/app/data              # SQLite database
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

---

### Project Structure

```
conversation-analyzer/
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD
├── src/
│   └── conversation_analyzer/
│       ├── __init__.py
│       ├── main.py                # CLI entry point (Typer)
│       ├── parsers/
│       │   ├── __init__.py
│       │   ├── claude_code.py     # JSONL parser (CUSTOM)
│       │   ├── markdown.py        # markdown-analysis wrapper
│       │   └── code_comments.py   # ripgrep wrapper
│       ├── extractors/
│       │   ├── __init__.py
│       │   ├── base.py            # Instructor-based (CUSTOM)
│       │   └── models.py          # Pydantic models
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── database.py        # SQLModel setup
│       │   └── models.py          # DB models
│       ├── deduplication/
│       │   ├── __init__.py
│       │   └── deduper.py         # dedupe wrapper
│       ├── reporting/
│       │   ├── __init__.py
│       │   ├── generator.py       # Report generation (CUSTOM)
│       │   └── templates/
│       │       └── report.md.j2   # Jinja2 template
│       └── llm/
│           ├── __init__.py
│           └── client.py          # LiteLLM wrapper
├── tests/
│   ├── __init__.py
│   ├── test_parsers.py
│   ├── test_extractors.py
│   └── fixtures/
│       └── sample_conversation.jsonl
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── pyproject.toml                 # Dependencies & config
├── README.md
├── CLAUDE.md                      # Project instructions
├── TODO.md
└── .env.example
```

---

## Cost-Benefit Analysis

### Building from Scratch
**Estimated Time:** 120-160 hours
**Code to Write:** ~5,000-7,000 lines
**Maintenance:** High (all bugs are ours)
**Risk:** High (reinventing wheels)

### Using Recommended Stack
**Estimated Time:** 60-80 hours (50% reduction)
**Code to Write:** ~2,000-3,000 lines (60% reduction)
**Maintenance:** Low (library updates handled upstream)
**Risk:** Low (battle-tested libraries)

### Time Savings Breakdown
- **LLM Integration:** Save 12-16 hours (LiteLLM + Instructor vs custom)
- **Database:** Save 8-12 hours (SQLModel vs raw SQL)
- **Markdown Parsing:** Save 6-8 hours (markdown-analysis vs custom)
- **Deduplication:** Save 16-24 hours (dedupe vs custom algorithm)
- **Document Loading:** Save 4-6 hours (LangChain loaders vs custom)

**Total Savings:** 46-66 hours (approximately 40-50% of project time)

---

## Risks & Mitigation

### Risk 1: Library Incompatibilities
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Test integration early (first week)
- Have fallback options documented
- Use version pinning

### Risk 2: Ollama Integration Issues
**Probability:** Low
**Impact:** High
**Mitigation:**
- LiteLLM handles retries/timeouts
- Test with multiple Ollama versions
- Document model requirements

### Risk 3: Performance with Large Conversations
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Use LangChain text splitters for chunking
- Implement streaming where possible
- Add progress indicators

### Risk 4: Deduplication Accuracy
**Probability:** Medium
**Impact:** Medium
**Mitigation:**
- Test both dedupe and text-dedup
- Tune similarity thresholds
- Allow manual review/override

---

## Next Steps

### Immediate Actions (This Week)

1. **Set up project structure**
   - Create pyproject.toml with recommended dependencies
   - Set up Docker configuration
   - Configure linting (ruff, black, mypy)

2. **Install and test core libraries**
   ```bash
   pip install litellm instructor sqlmodel markdown-analysis
   ```

3. **Prototype core components**
   - LiteLLM + Ollama connection test
   - Instructor extraction with sample text
   - SQLModel database setup
   - markdown-analysis TODO extraction

4. **Study Claude Code format**
   - Clone claude-conversation-extractor repo
   - Analyze JSONL structure in ~/.claude/projects
   - Design Python parser

### Week 1 Goals

- [ ] Working Ollama integration with LiteLLM
- [ ] Basic extraction with Instructor
- [ ] SQLModel database created
- [ ] Parse one Claude Code conversation
- [ ] Generate simple markdown report

### Week 2 Goals

- [ ] Extract TODOs from conversations with 80%+ accuracy
- [ ] Scan code comments with ripgrep
- [ ] Parse TODO.md files
- [ ] Basic deduplication working
- [ ] CLI interface with Typer

---

## Conclusion

The research reveals a **mature ecosystem** of tools that can handle 60-70% of our requirements:

**Use Directly (No Custom Code):**
- ✅ LiteLLM - Ollama client
- ✅ Instructor - LLM extraction
- ✅ SQLModel - Database
- ✅ markdown-analysis - Markdown TODOs
- ✅ dedupe - Deduplication
- ✅ ripgrep - File scanning

**Adapt/Reference:**
- 📚 claude-conversation-extractor - JSONL parsing approach
- 📚 LangChain - Extraction patterns
- 📚 Todo Tree - Regex patterns

**Build Custom:**
- 🔨 Claude Code JSONL parser
- 🔨 Conversation-specific extraction prompts
- 🔨 Multi-source orchestration
- 🔨 Priority scoring
- 🔨 Report generation

**Recommendation:** **Proceed with recommended stack** - significant time savings with battle-tested libraries.

---

## References

### Documentation Links
- LiteLLM: https://docs.litellm.ai/
- Instructor: https://python.useinstructor.com/
- SQLModel: https://sqlmodel.tiangolo.com/
- markdown-analysis: https://pypi.org/project/markdown-analysis/
- dedupe: https://github.com/dedupeio/dedupe
- LangChain: https://python.langchain.com/
- BERTopic: https://maartengr.github.io/BERTopic/

### GitHub Repositories
- claude-conversation-extractor: https://github.com/ZeroSumQuant/claude-conversation-extractor
- Todo Tree: https://github.com/Gruntfuggly/todo-tree
- text-dedup: https://github.com/ChenghaoMou/text-dedup
- Meetily: https://meetily.zackriya.com/

### Research Date
All searches conducted: 2025-11-19

---

**Next Document:** Implementation plan with chosen stack
