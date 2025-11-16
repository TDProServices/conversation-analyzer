# Conversation Analyzer

Local LLM-powered analysis of conversations, files, and documentation to extract missed TODOs, bugs, feature requests, and identify potential projects.

## Purpose

Automatically analyze:
- Claude Code conversations (exported or from logs)
- Project files (TODO.md, code comments, documentation)
- Git history and commit messages

To discover:
- Action items and TODOs that weren't tracked
- Bugs mentioned but not filed
- Feature requests discussed but not documented
- Patterns suggesting new projects or automation opportunities

## Tech Stack

- **LLM:** Ollama (local, offline, private)
- **Language:** Python 3.10+
- **Storage:** SQLite + Markdown reports
- **Search:** Ripgrep for fast file scanning

## Status

Project initialized. Design and implementation in progress.

**Author:** Tanya Davis / TD Professional Services LLC
