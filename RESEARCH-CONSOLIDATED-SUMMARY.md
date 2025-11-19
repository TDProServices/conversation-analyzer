# Consolidated Research Summary - TODO Extraction Tools & Libraries

**Date:** 2025-11-19
**Status:** Research Phase Complete ✅
**Total Research Sessions:** 2 (different focuses, complementary findings)

---

## Overview

Comprehensive research was conducted on existing TODO extraction libraries and tools focusing on 2024-2025 solutions. Research was divided into two complementary areas:

1. **Python Libraries & Frameworks** - General conversation analysis and document parsing
2. **TODO Extraction Tools** - Specific tools for extracting TODO comments and action items

---

## Research Documents Summary

### 1. RESEARCH-PYTHON-LIBRARIES.md
**Focus:** Python standard library and basic parsing libraries

**Key Findings:**
- **mistune 3.0+** - Fast markdown parser (3x faster than python-markdown)
- **tokenize** (stdlib) - Extract Python comments without dependencies
- **ast** (stdlib) - Code analysis, sufficient for our needs
- **os.walk()** - Fast enough for file traversal (stdlib)
- **ripgrepy** - Python wrapper for ripgrep

**Recommendation:** Prefer stdlib where possible, add dependencies only when significant value

---

### 2. RESEARCH-FINDINGS-2024-2025.md
**Focus:** Conversation analysis tools and modern frameworks

**Key Findings:**
- **LiteLLM** - Unified interface to Ollama with retry/timeout handling
- **Instructor** - Structured LLM extraction with Pydantic models
- **SQLModel** - Combines SQLAlchemy + Pydantic validation
- **markdown-analysis** - Parse markdown including TODO lists
- **dedupe / text-dedup** - Intelligent deduplication libraries
- **Claude Conversation Extractor** - Existing tool for Claude Code JSONL format

**Critical Discovery:** https://github.com/ZeroSumQuant/claude-conversation-extractor already parses Claude Code logs!

**Time Savings:** 40-60 hours by using existing libraries instead of building from scratch

---

### 3. RESEARCH-TODO-EXTRACTION-TOOLS.md (NEW)
**Focus:** Specific TODO extraction libraries and tools

**Key Findings:**

#### Python Libraries:
- **comment-parser** ⭐ - Multi-language code comment extraction (Dec 2024 update)
  - Extracts all comments with line numbers
  - MIME type support for multiple languages
  - Returns structured Comment objects
  - Installation: `pip install comment-parser`

- **python-todo-comments** - CLI for TODO comment extraction from Python
  - Directory scanning
  - Markdown output
  - Limited to Python files only

- **todocom** - CLI TODO extractor with multi-line support
  - Single and multi-line comments
  - Multi-line docstrings (Python only currently)

- **flake8-todos** - Linting tool for TODO comment formatting

#### JavaScript Tools (Reference):
- **leasot** - Industry standard (Node.js)
  - 90+ language support
  - Multiple output formats (json, xml, markdown, vscode)
  - Reference for best practices

#### Markdown Parsers:
- **markdown-analysis** ⭐ - Comprehensive markdown parsing
  - Extracts task lists: `- [ ]`, `- [x]`
  - Understands hierarchy and structure
  - Python-native

#### LLM-Based Extraction:
- **Ollama with custom prompts** ⭐ - For unstructured text
  - Recommended models: qwen2.5:3b (fast), llama3.1:8b (accurate)
  - Structured output with JSON
  - Prompt engineering best practices documented
  - System messages in Modelfile for customization

#### Commercial Tools (Rejected):
- Fireflies.ai, Otter.ai, Sembly AI, Read.ai, Tactiq.io, Notta.ai
- All cloud-only, violates privacy-first requirement
- Good for feature inspiration, not for implementation

#### Fast Scanning:
- **ripgrep** ⭐ - Essential for fast file scanning
  - 10-100x faster than Python file reading
  - Respects .gitignore automatically
  - Pattern: `rg "TODO|FIXME|HACK|XXX|BUG|NOTE" -n`

---

### 4. RESEARCH-SUMMARY.md
**Quick reference for Python libraries research**

**Recommended Stack:**
```bash
pip install mistune>=3.0.0 ripgrepy>=2.2.0
```

**Code Examples:**
- Directory scanning with os.walk()
- Markdown parsing with mistune
- TODO extraction with tokenize
- Fast search with ripgrepy

---

### 5. RECOMMENDED-STACK.md
**Comprehensive technology stack with Docker setup**

**Core Dependencies:**
```toml
litellm = "^1.50.0"           # LLM interface
instructor = "^1.0.0"         # Structured extraction
sqlmodel = "^0.0.18"          # Database ORM
markdown-analysis = "^0.1.0"  # Markdown parsing
dedupe = "^3.0.3"             # Deduplication
typer = "^0.12.0"             # CLI framework
rich = "^13.0.0"              # Terminal output
```

**Architecture:**
```
User CLI → Multi-Source Scanner → Extractors → LLM Analysis →
Deduplication → Priority Scoring → SQLite → Report Generator
```

**Time Savings:** 40-62 hours using libraries vs. building from scratch

---

## Consolidated Recommendations

### Phase 1: Structured Extraction (High Confidence)

**1. Code Comment Extraction**
```python
# Use: comment-parser (NEW finding)
from comment_parser import comment_parser

comments = comment_parser.extract_comments('/path/to/file.py')
for comment in comments:
    if 'TODO' in comment.text():
        print(f"Line {comment.line_number()}: {comment.text()}")
```

**Alternative (stdlib only):**
```python
# Use: tokenize (from RESEARCH-PYTHON-LIBRARIES)
import tokenize

with open('file.py', 'rb') as f:
    for tok in tokenize.tokenize(f.readline):
        if tok.type == tokenize.COMMENT and 'TODO' in tok.string:
            print(f"Line {tok.start[0]}: {tok.string}")
```

**2. Markdown TODO Extraction**
```python
# Use: markdown-analysis (found in both researches)
from markdown_analysis import MarkdownAnalyzer

analyzer = MarkdownAnalyzer()
doc = analyzer.analyze_file('TODO.md')

for task in doc.tasks:
    print(f"Task: {task.text}, Completed: {task.completed}")
```

**3. Fast File Scanning**
```python
# Use: ripgrep via ripgrepy or subprocess
from ripgrepy import Ripgrepy

rg = Ripgrepy('TODO|FIXME|HACK', '/path/to/projects')
results = rg.with_filename().line_number().run().as_dict

# Or direct subprocess (lighter dependency)
import subprocess
result = subprocess.run(['rg', 'TODO', '-n'], capture_output=True)
```

---

### Phase 2: Unstructured Extraction (LLM-Based)

**4. Conversation TODO Extraction with Ollama**
```python
# Option A: LiteLLM (recommended from RESEARCH-FINDINGS)
from litellm import completion

response = completion(
    model="ollama/qwen2.5:3b",
    messages=[{
        "role": "user",
        "content": "Extract TODOs from: I need to fix the auth bug and add tests"
    }],
    api_base="http://localhost:11434"
)

# Option B: Instructor for structured output (recommended)
import instructor
from ollama import Client
from pydantic import BaseModel

class TodoItem(BaseModel):
    description: str
    priority: str
    confidence: float

client = instructor.from_ollama(Client())
result = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": conversation_text}],
    response_model=TodoItem
)
```

**Prompt Engineering Best Practices:**
```
ROLE: You are a TODO extraction expert
TASK: Extract action items from conversation
CONSTRAINTS: Format as JSON, include confidence scores
OUTPUT: Structured format with examples
EXAMPLES: [1-3 concrete examples]
```

---

### Phase 3: Deduplication & Storage

**5. Deduplication**
```python
# Option A: dedupe library (recommended for accuracy)
from dedupe import Dedupe

# Option B: Simple text similarity (fallback)
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Option C: text-dedup (alternative)
from text_dedup import TextDedup
```

**6. Database with SQLModel**
```python
from sqlmodel import SQLModel, Field, create_engine, Session

class TodoItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    type: str  # "bug", "feature", "task"
    priority: str
    confidence: float
    source_file: str
    source_line: int

engine = create_engine("sqlite:///todos.db")
SQLModel.metadata.create_all(engine)
```

---

## Final Tool Stack Decision Matrix

| Component | Option A (Recommended) | Option B (Alternative) | Option C (Fallback) |
|-----------|------------------------|------------------------|---------------------|
| **Code Comments** | comment-parser | tokenize (stdlib) | ripgrep + regex |
| **Markdown** | markdown-analysis | mistune + custom parser | - |
| **LLM Interface** | LiteLLM + Instructor | Direct Ollama API | - |
| **Database** | SQLModel | SQLAlchemy | sqlite3 (stdlib) |
| **Deduplication** | dedupe | text-dedup | difflib (stdlib) |
| **File Scanning** | ripgrep | os.walk (stdlib) | - |
| **CLI** | Typer + Rich | Click | argparse (stdlib) |

---

## What to Build vs. Use

### ✅ USE EXISTING TOOLS:

1. **comment-parser** - Code comment extraction (multi-language)
2. **markdown-analysis** - Markdown task list parsing
3. **LiteLLM** - LLM interface with retry/timeout
4. **Instructor** - Structured LLM extraction
5. **SQLModel** - Database ORM
6. **dedupe** - Deduplication algorithm
7. **ripgrep** - Fast file scanning
8. **Typer + Rich** - CLI framework

**Estimated Time Saved:** 40-62 hours

---

### 🔨 MUST BUILD CUSTOM:

1. **Claude Code JSONL Parser** (8-12h)
   - No existing Python tool for this format
   - Study: https://github.com/ZeroSumQuant/claude-conversation-extractor
   - Parse ~/.claude/projects/*/conversations/*.jsonl

2. **Conversation-Specific Extraction Logic** (16-24h)
   - Custom prompts for coding conversations
   - Handle Claude-specific patterns
   - Validate extraction accuracy

3. **Multi-Source Orchestration** (12-16h)
   - Coordinate scanning across sources
   - Merge results from different extractors
   - Handle conflicts and priorities

4. **Priority Scoring Algorithm** (6-8h)
   - Coding-specific priority rules
   - Urgency/impact calculation
   - LLM-assisted scoring

5. **Report Generation** (4-6h)
   - Custom markdown templates
   - Statistics and summaries
   - Action item formatting

**Total Custom Code:** 46-66 hours
**Total with Libraries:** ~56-76 hours
**Total from Scratch:** ~120-160 hours

**Net Savings:** 44-84 hours (37-52% reduction)

---

## Installation Quick Start

### Recommended Dependencies:

```bash
# Core functionality
pip install comment-parser markdown-analysis litellm instructor sqlmodel

# CLI and utilities
pip install typer rich python-dotenv pyyaml

# Deduplication (choose one)
pip install dedupe  # OR pip install text-dedup

# Development
pip install ruff black mypy pytest

# System requirements
sudo apt install ripgrep  # Ubuntu/Debian
brew install ripgrep      # macOS
```

### Test Installations:

```bash
# Test comment-parser
python -c "from comment_parser import comment_parser; print('✓ comment-parser')"

# Test markdown-analysis
python -c "from markdown_analysis import MarkdownAnalyzer; print('✓ markdown-analysis')"

# Test LiteLLM with Ollama
python -c "from litellm import completion; print('✓ litellm')"

# Test Instructor
python -c "import instructor; print('✓ instructor')"

# Test SQLModel
python -c "from sqlmodel import SQLModel; print('✓ sqlmodel')"

# Test ripgrep
rg --version

# All good? You're ready to build! 🚀
```

---

## Next Steps

### Immediate (Today):
1. ✅ Research complete
2. ⏳ Get user approval on recommended stack
3. ⏳ Install dependencies
4. ⏳ Test Ollama connection
5. ⏳ Verify all libraries work

### Week 1 - MVP:
- Set up Python project structure (src/, tests/)
- Implement comment-parser integration
- Implement markdown-analysis integration
- Create basic CLI with Typer
- Test on sample files

### Week 2 - LLM Integration:
- Study claude-conversation-extractor source
- Implement JSONL parser for Claude Code
- Create Instructor extraction models
- Test LiteLLM + Ollama connection
- Validate >85% extraction accuracy

### Week 3 - Intelligence:
- Implement deduplication with dedupe
- Build priority scoring algorithm
- Create SQLite database with SQLModel
- Add confidence scoring
- Cross-reference analysis

### Week 4 - Production:
- Generate markdown reports
- Add batch processing
- Create Docker setup
- Write beginner-friendly documentation
- Final testing and refinement

---

## Success Metrics

### Accuracy Targets:
- **Code comments:** 95%+ precision (explicit TODO markers)
- **Markdown tasks:** 90%+ precision (checkbox format)
- **Conversations:** 85%+ precision (LLM-based, requires validation)

### Performance Targets:
- **Single conversation (5000 words):** < 30 seconds
- **Single code file (500 lines):** < 1 second
- **Full project scan (1000 files):** < 2 minutes
- **Daily batch (20 conversations):** < 5 minutes

### Quality Targets:
- **False positives:** < 10%
- **Deduplication accuracy:** > 90%
- **Priority scoring accuracy:** > 80%

---

## Risk Mitigation

### Library Fallbacks:
- If **comment-parser** fails → Use tokenize (stdlib)
- If **markdown-analysis** fails → Use mistune + custom parser
- If **LiteLLM** fails → Use direct Ollama HTTP API
- If **Instructor** fails → Manual JSON parsing
- If **dedupe** fails → Use text-dedup or difflib
- If **SQLModel** fails → Use SQLAlchemy or sqlite3

### Version Pinning:
```toml
# Always pin major.minor versions
comment-parser = "^1.2.5"
litellm = "^1.50.0"
instructor = "^1.0.0"
# Never use "*" or ">=" without upper bound
```

---

## Cost Analysis

### Financial Cost: $0
- ✅ All libraries are free/open-source
- ✅ No API fees (local Ollama)
- ✅ No subscriptions
- ✅ No cloud services

### Time Investment:
- ✅ Research: 6-8 hours (COMPLETE)
- ⏳ Setup & integration: 8-12 hours
- ⏳ Custom development: 46-66 hours
- ⏳ Testing & refinement: 8-12 hours
- **Total: 68-98 hours** (vs 120-160 hours from scratch)

### Compute Cost:
- Laptop/desktop with Ollama: Free
- Minimal RAM needed (qwen2.5:3b ~ 4GB)
- No GPU required (nice to have)

---

## Critical Findings Summary

1. ⭐ **comment-parser exists** - Don't build custom comment extractor
2. ⭐ **markdown-analysis handles task lists** - Don't parse `- [ ]` manually
3. ⭐ **LiteLLM saves massive time** - Don't build Ollama client from scratch
4. ⭐ **Instructor enables type-safe extraction** - Don't manually parse JSON
5. ⭐ **Claude conversation extractor exists** - Study its JSONL approach
6. ⭐ **dedupe is battle-tested** - Don't build fuzzy matching yourself
7. ⭐ **ripgrep is essential** - 10-100x faster than Python file scanning

---

## Questions Answered

### "Should we build or use existing tools?"
**Answer:** Use existing for 60-70% of functionality, build custom for Claude-specific logic only.

### "Which markdown parser?"
**Answer:** markdown-analysis for task lists, mistune for general parsing.

### "How to extract code TODOs?"
**Answer:** comment-parser for multi-language, tokenize for Python-only.

### "Best LLM integration?"
**Answer:** LiteLLM + Instructor for structured, type-safe extraction.

### "Deduplication approach?"
**Answer:** Start with dedupe library, fallback to text-dedup or difflib if needed.

### "Docker or native?"
**Answer:** Docker recommended for reproducibility, especially for ripgrep dependency.

---

## References

### Research Documents:
- `/home/user/conversation-analyzer/RESEARCH-TODO-EXTRACTION-TOOLS.md`
- `/home/user/conversation-analyzer/RESEARCH-FINDINGS-2024-2025.md`
- `/home/user/conversation-analyzer/RESEARCH-PYTHON-LIBRARIES.md`
- `/home/user/conversation-analyzer/RESEARCH-SUMMARY.md`
- `/home/user/conversation-analyzer/RECOMMENDED-STACK.md`

### External Resources:
- comment-parser: https://pypi.org/project/comment-parser/
- markdown-analysis: https://pypi.org/project/markdown-analysis/
- LiteLLM: https://github.com/BerriAI/litellm
- Instructor: https://github.com/jxnl/instructor
- Claude Conversation Extractor: https://github.com/ZeroSumQuant/claude-conversation-extractor
- ripgrep: https://github.com/BurntSushi/ripgrep

### Standards:
- PEP 350 (Codetags): https://peps.python.org/pep-0350/
- TODO.md Format: https://github.com/todomd/todo.md
- GitHub Flavored Markdown Task Lists

---

## Conclusion

**Research Status:** ✅ COMPLETE

**Recommendation:** Proceed with hybrid approach:
1. Use **comment-parser** for code comment extraction
2. Use **markdown-analysis** for markdown task lists
3. Use **LiteLLM + Instructor** for conversation analysis with Ollama
4. Use **SQLModel** for database
5. Use **dedupe** for deduplication
6. Use **ripgrep** for fast file scanning
7. Use **Typer + Rich** for CLI

**Build custom only for:**
- Claude Code JSONL parser
- Conversation-specific extraction logic
- Multi-source orchestration
- Priority scoring algorithm
- Report generation

**Expected Outcome:**
- 40-60 hours time savings
- Higher quality (battle-tested libraries)
- Better maintainability (standard tools)
- Easier for beginners (well-documented libraries)

**Ready to implement:** ✅ YES

---

**Last Updated:** 2025-11-19
**Status:** Research complete, awaiting user approval to proceed with implementation
