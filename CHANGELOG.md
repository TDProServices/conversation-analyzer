# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Conversation parser (mistune-based)
- Ollama integration for LLM analysis
- TODO/bug extractor (hybrid regex + LLM)
- SQLite database layer
- Markdown report generator
- Deduplication logic
- Priority scoring
- Confidence scoring

## [0.1.0] - 2025-11-17

### Added
- Initial project structure with src-layout
- CLI framework with Click (analyze, scan, report, check commands)
- Comprehensive documentation (README, CLAUDE, SETUP, RESEARCH)
- Project configuration (pyproject.toml, requirements.txt)
- Development tooling (pytest, ruff, black, mypy)
- Configuration template (.conversation-analyzer.yaml.example)
- Beginner-friendly troubleshooting guides
- Test framework structure

### Research & Decisions
- Evaluated 25+ sources for technology choices
- Decided: pyproject.toml + venv (not Poetry/Docker)
- Selected: qwen2.5:3b (primary), llama3.1:8b (fallback)
- Chose: mistune (fastest markdown parser, 15.49s benchmark)
- Selected: official ollama library for LLM integration

### Documentation
- README.md: Comprehensive prerequisites, installation, FAQ (Score: 95/100)
- CLAUDE.md: Project guidance with troubleshooting (Score: 92/100)
- RESEARCH.md: 698 lines, 25 sources, all decisions justified
- SETUP.md: Step-by-step beginner guide with troubleshooting
- TODO.md: Task tracking with commit hashes

### Project Structure
```
conversation-analyzer/
├── src/conversation_analyzer/  # Source code
├── tests/                      # Test suite
├── docs/                       # Documentation (empty, for Phase 4+)
├── examples/                   # Examples (empty, for Phase 4+)
└── Configuration files
```

### Known Issues
- License placeholder (MIT) needs confirmation
- Email placeholder needs real address
- CLI commands scaffolded but not implemented (Phase 4 work)

### Commits
- e574a73: Documentation improvements (README, CLAUDE.md)
- 9f675a4: Comprehensive research documentation
- 4515566: Project structure initialization
- 408c072: TODO.md synchronization

## [0.0.0] - 2025-11-16

### Research Phase (Pre-release)
- Initial research on conversation analysis tools
- Evaluated TODO extraction approaches
- Analyzed Ollama model capabilities
- Created project guidance documents

---

**Note:** Detailed commit information is available in git history.
Use `git log --oneline` for concise history or `git log` for full details.
