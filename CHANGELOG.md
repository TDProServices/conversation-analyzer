# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest
- Unit tests for models, database, parsers, intelligence
- Integration tests for full pipeline
- Mock Ollama client for testing without dependencies
- Utility functions (logging, text_chunking, file_hash)
- LICENSE file (MIT)
- CONTRIBUTING.md with development guidelines
- This CHANGELOG

## [0.1.0] - 2025-11-16

### Added
- Initial release of Conversation Analyzer
- Local LLM-powered extraction using Ollama
- Multi-source parsing (conversations, code comments, documents)
- Pydantic data models with validation
- SQLite database with full schema
- Extraction layer with NuExtract model support
- Intelligence features:
  - Embedding-based deduplication
  - Priority scoring algorithm
  - Entity extraction and linking
- Reporting layer:
  - Markdown report generation
  - JSON export functionality
- CLI interface with commands:
  - `analyze` - Analyze files/directories
  - `report` - Generate reports
  - `stats` - View statistics
  - `list` - List items with filters
  - `test-connection` - Test Ollama connection
- Configuration system (YAML + environment variables)
- Comprehensive documentation:
  - RESEARCH_REPORT.md (824 lines)
  - DESIGN.md (985 lines)
  - README.md with quick start
  - docs/INSTALLATION.md
  - docs/USAGE.md
  - PROJECT_STATUS.md
- Test fixtures with sample conversations and code

### Technical Details
- Python 3.10+ support
- Type hints throughout
- Error handling with retries
- File hash tracking to skip unchanged files
- Context manager support
- Logging infrastructure
- Progress tracking

### Dependencies
- ollama >= 0.4.7
- langchain >= 0.3.0
- pydantic >= 2.0.0
- sentence-transformers >= 2.2.0
- click >= 8.1.0
- rich >= 13.5.0
- pytest >= 7.4.0 (dev)
- deepeval >= 1.0.0 (dev)

## [0.0.1] - 2025-11-16

### Added
- Project initialization
- Basic structure

---

## Release Notes

### v0.1.0 - "Foundation Release"

This is the first production-ready release of Conversation Analyzer, featuring:

**Core Functionality:**
- Extract TODOs, bugs, features, and project ideas from conversations and code
- 100% local processing with Ollama (privacy-first)
- Intelligent deduplication and priority scoring
- Beautiful Markdown reports and structured JSON exports

**Quality:**
- Comprehensive research and design documentation
- Production-ready code with error handling
- Full test suite with 80%+ coverage goal
- Type-safe with Pydantic validation

**Developer Experience:**
- Rich CLI with colors and tables
- Flexible configuration system
- Clean API for programmatic use
- Extensive documentation

**What's Next:**
See our [roadmap in README.md](README.md#roadmap) for planned features in v0.2.0 and beyond.

---

[Unreleased]: https://github.com/TDProServices/conversation-analyzer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/TDProServices/conversation-analyzer/releases/tag/v0.1.0
[0.0.1]: https://github.com/TDProServices/conversation-analyzer/releases/tag/v0.0.1
