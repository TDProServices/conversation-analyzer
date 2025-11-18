## Contributing to Conversation Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and constructive. We're building together!

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/conversation-analyzer.git
   cd conversation-analyzer
   ```

3. **Set up development environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Install Ollama** (for testing):
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull nuextract
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add type hints
- Update documentation

### 3. Add Tests

All new features and bug fixes must include tests:

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/conversation_analyzer

# Run specific test file
pytest tests/unit/test_models.py
```

### 4. Format Code

```bash
# Format with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/
```

### 5. Update Documentation

- Update README.md if adding features
- Update docs/ for significant changes
- Add docstrings to new functions/classes
- Update CHANGELOG.md

### 6. Commit Changes

Use conventional commit messages:

```bash
git add .
git commit -m "feat: add support for CSV parsing"
# or
git commit -m "fix: resolve SQL injection in query builder"
# or
git commit -m "docs: update installation guide"
```

**Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### 7. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style

- Follow PEP 8
- Use type hints
- Max line length: 100 characters
- Use docstrings (Google style)

**Example:**

```python
def extract_items(text: str, confidence_threshold: float = 0.5) -> List[Item]:
    """Extract items from text.

    Args:
        text: Input text to analyze
        confidence_threshold: Minimum confidence to keep items

    Returns:
        List of extracted items

    Raises:
        ValueError: If text is empty
    """
    pass
```

### Testing

- Write unit tests for all new functions
- Write integration tests for new features
- Aim for >80% code coverage
- Use descriptive test names

**Example:**

```python
def test_extract_items_with_high_confidence():
    """Test that high confidence items are extracted."""
    result = extract_items("TODO: Fix bug", confidence_threshold=0.9)
    assert len(result) > 0
```

## Areas for Contribution

### High Priority

- **Additional Parsers:**
  - CSV file parser
  - XML/HTML parser
  - Email (mbox) parser
  - Slack export parser

- **Integrations:**
  - GitHub Issues integration
  - Jira integration
  - Linear integration
  - Notion integration

- **Testing:**
  - Add more LLM evaluation tests
  - Improve test coverage
  - Add performance benchmarks

### Medium Priority

- **Features:**
  - Web UI (React/Vue)
  - Watch mode for continuous analysis
  - Custom prompt templates
  - Multi-language support

- **Intelligence:**
  - Better entity extraction
  - Improve priority scoring
  - Add sentiment analysis
  - Trend detection

### Low Priority

- **Documentation:**
  - Video tutorials
  - More examples
  - API reference docs
  - Architecture diagrams

- **Infrastructure:**
  - Docker support
  - Kubernetes manifests
  - GitHub Actions improvements

## Pull Request Process

1. **Ensure tests pass:**
   ```bash
   pytest
   ```

2. **Update documentation** if needed

3. **Add entry to CHANGELOG.md** under "Unreleased"

4. **Create PR** with clear description:
   - What does this PR do?
   - Why is this change needed?
   - How was it tested?
   - Screenshots (if UI changes)

5. **Respond to review feedback** promptly

6. **Squash commits** before merge (if requested)

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v0.2.0`
4. Push tag: `git push origin v0.2.0`
5. GitHub Actions will build and release

## Questions?

- **Documentation:** Check docs/ folder
- **Issues:** Search existing issues
- **Discussions:** Use GitHub Discussions
- **Contact:** Open an issue with your question

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
