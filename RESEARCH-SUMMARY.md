# Research Summary - Quick Reference

**Date:** 2025-11-19
**Full Report:** [RESEARCH-PYTHON-LIBRARIES.md](./RESEARCH-PYTHON-LIBRARIES.md)

---

## TL;DR - Recommended Tech Stack

### Core Dependencies
```bash
pip install mistune>=3.0.0 ripgrepy>=2.2.0 ripgrep>=15.0.0
```

### Use These Tools

| Task | Tool | Why |
|------|------|-----|
| **Parse Markdown** | `mistune 3.0+` | 3x faster, simple API, battle-tested by Jupyter |
| **Extract Comments** | `tokenize` + regex | No deps, full control, beginner-friendly |
| **Analyze Code** | `ast` (stdlib) | Sufficient, no deps, well-documented |
| **Scan Files** | `os.walk()` | Fast enough, simple, stdlib |
| **Fast Search** | `ripgrepy` | 10-100x faster than Python loops |

### Sample Code

#### Scan Directories
```python
import os

IGNORE_DIRS = {'.git', '__pycache__', '.venv'}

for root, dirs, files in os.walk('/path/to/projects'):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
    for file in files:
        if file.endswith('.md'):
            print(os.path.join(root, file))
```

#### Parse Markdown
```python
import mistune

html = mistune.html("# Hello World\n\nSome *text*")
```

#### Extract TODOs
```python
import tokenize
import re

def extract_todos(filepath):
    pattern = re.compile(r'#\s*(TODO|FIXME|HACK):\s*(.+)')
    todos = []

    with open(filepath, 'rb') as f:
        for tok in tokenize.tokenize(f.readline):
            if tok.type == tokenize.COMMENT:
                match = pattern.match(tok.string)
                if match:
                    todos.append({
                        'line': tok.start[0],
                        'type': match.group(1),
                        'text': match.group(2)
                    })
    return todos
```

#### Fast Search with ripgrep
```python
from ripgrepy import Ripgrepy

rg = Ripgrepy('TODO|FIXME', '/path/to/code')
results = rg.with_filename().line_number().run().as_dict

for filepath, matches in results.items():
    print(f"{filepath}:")
    for match in matches:
        print(f"  Line {match['line_number']}: {match['line']}")
```

---

## Key Findings

### Performance (2024-2025 Benchmarks)
- **mistune:** ~14ms to parse (vs 48ms for python-markdown)
- **os.walk():** 11.49 iter/sec (vs 6.17 for pathlib)
- **ripgrep:** 10-100x faster than Python file reading
- **Expected:** <5 minutes to scan 20 repos ✅

### Licenses (All Permissive)
- mistune: BSD-3-Clause ✅
- markdown-it-py: MIT ✅
- ripgrepy: MIT ✅
- Python stdlib: PSF ✅

### Maintenance Status (All Active)
- mistune: Released 2024-2025 ✅
- markdown-it-py: v4.0.0 (2024) ✅
- ripgrepy: v2.2.0 (July 2025) ✅

---

## Architecture Decisions

### ✅ Use Existing Tools
- **Don't build:** Custom markdown parsers (use mistune)
- **Don't build:** Custom file walkers (use os.walk)
- **Don't build:** Regex-only comment extractors (use tokenize)

### ✅ Keep It Simple
- Prefer stdlib when sufficient
- Add deps only when significant value
- Choose beginner-friendly APIs
- Optimize for maintainability > performance

### ✅ Docker for Deployment
- Guarantees ripgrep availability
- Pins Python version
- Reproducible across systems
- Easy for beginners

---

## Next Actions

1. **Create requirements.txt** with recommended deps
2. **Set up project structure** (src/, tests/)
3. **Implement file scanner** using os.walk()
4. **Implement TODO extractor** using tokenize
5. **Add Ollama integration** for LLM analysis
6. **Build markdown parser** using mistune
7. **Create Docker setup** for deployment

---

## Resources

- **Full Research:** [RESEARCH-PYTHON-LIBRARIES.md](./RESEARCH-PYTHON-LIBRARIES.md)
- **Project Guide:** [CLAUDE.md](./CLAUDE.md)
- **TODO List:** [TODO.md](./TODO.md)

---

**Status:** Research complete, ready to implement! 🚀
