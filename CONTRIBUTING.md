# Contributing to Conversation Analyzer

Thank you for your interest in contributing! This is a personal project by Tanya Davis, but community contributions are welcome.

## Getting Started

1. **Read the documentation:**
   - [README.md](README.md) - Project overview
   - [SETUP.md](SETUP.md) - Development setup
   - [CLAUDE.md](CLAUDE.md) - Development guidance
   - [RESEARCH.md](RESEARCH.md) - Technology decisions

2. **Set up your development environment:**
   ```bash
   git clone https://github.com/TDProServices/conversation-analyzer.git
   cd conversation-analyzer
   python3 -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   pytest  # Verify tests pass
   ```

## How to Contribute

### Reporting Bugs

Create a GitHub issue with:
- **Description:** What went wrong?
- **Steps to reproduce:** How can we see the bug?
- **Expected behavior:** What should happen?
- **Actual behavior:** What actually happened?
- **Environment:** OS, Python version, Ollama version
- **Error messages:** Full output if applicable

### Suggesting Features

Create a GitHub issue with:
- **Problem statement:** What need does this address?
- **Proposed solution:** How should it work?
- **Alternatives considered:** What else did you think about?
- **Use case:** When would you use this?

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow code style:**
   - Run `ruff check src/` (linting)
   - Run `black src/` (formatting)
   - Run `mypy src/` (type checking)
3. **Write tests** for new functionality
4. **Update documentation** (README, CHANGELOG, etc.)
5. **Write good commit messages:**
   - Follow Conventional Commits format
   - Keep body to 20-40 lines (use CHANGELOG.md for details)
   - See [Commit Guidelines](#commit-guidelines) below
6. **Submit PR** with clear description

## Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes

# 3. Run quality checks
pytest                    # Tests
ruff check src/          # Linting
black src/               # Formatting
mypy src/                # Type checking

# 4. Commit (see guidelines below)
git add .
git commit -m "feat(scope): concise description

More detailed explanation of WHY this change.

Author: Your Name
Organization: Your Org (optional)
"

# 5. Push and create PR
git push origin feature/your-feature-name
# Then create PR on GitHub
```

## Commit Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

Author: Your Name
Organization: Your Organization (optional)
```

### Types
- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **refactor:** Code refactoring
- **test:** Adding/updating tests
- **chore:** Maintenance tasks

### Rules
1. **Subject line:** 50-72 characters, imperative mood
2. **Body:** 20-40 lines maximum (use CHANGELOG.md for details)
3. **Explain WHY, not WHAT** (what is in the diff)
4. **Attribution:** Include your name
5. **NO AI co-author attribution** (even if AI-assisted)

### Good Example
```
feat(parser): add support for multi-line code blocks

Claude conversations often contain multi-line code blocks that
the current parser doesn't handle correctly. This adds support
for fenced code blocks with language specifiers.

Fixes issue #23.

Author: Jane Developer
```

### Bad Example
```
Update parser

Added some stuff to make it work better.
```

## Code Style

- **Python:** Follow PEP 8 (enforced by ruff and black)
- **Line length:** 88 characters (Black's default)
- **Type hints:** Required for public APIs
- **Docstrings:** Google style for modules, classes, functions
- **Comments:** Explain WHY, not WHAT

## Testing

- **Write tests** for new features
- **Maintain coverage:** Minimum 70% (configured in pyproject.toml)
- **Test types:**
  - Unit tests: `tests/test_*.py`
  - Integration tests: Mark with `@pytest.mark.integration`
  - Slow tests: Mark with `@pytest.mark.slow`

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_cli.py

# Skip slow tests
pytest -m "not slow"
```

## Documentation

- **Update README.md** for user-facing changes
- **Update CHANGELOG.md** for all changes
- **Update CLAUDE.md** for development guidance changes
- **Add docstrings** to new code
- **Beginner-friendly:** Assume novice user level

## Project Structure

```
conversation-analyzer/
├── src/conversation_analyzer/  # Source code
│   ├── __init__.py
│   ├── cli.py                  # CLI interface
│   ├── parser.py               # (Phase 4) Conversation parser
│   ├── ollama_client.py        # (Phase 4) Ollama integration
│   ├── extractor.py            # (Phase 4) TODO extraction
│   ├── database.py             # (Phase 4) SQLite layer
│   └── reporter.py             # (Phase 4) Report generator
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_*.py               # More tests as implemented
├── docs/                       # Additional documentation
└── examples/                   # Example usage
```

## Questions?

- **Issues:** https://github.com/TDProServices/conversation-analyzer/issues
- **Discussions:** https://github.com/TDProServices/conversation-analyzer/discussions
- **Email:** [email protected] (for sensitive topics)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
