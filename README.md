# Conversation Analyzer

**Version:** 0.1.0 (In Development)
**Author:** Tanya Davis / TD Professional Services LLC
**License:** [To be determined]

---

## What Is This?

Conversation Analyzer is a tool that reads your Claude Code conversations and project files to automatically find things you might have forgotten:

- TODOs you mentioned but didn't write down
- Bugs you talked about but didn't file
- Feature ideas you discussed but didn't document
- Patterns that suggest you could automate something

**Example:** You chat with Claude about fixing a bug. You fix it, but forget to update the TODO list. This tool finds that conversation and reminds you.

**Privacy First:** Everything runs on your computer using Ollama (a local AI). No data is sent to the cloud. Perfect for sensitive legal or medical projects.

---

## Quick Start

### Prerequisites

Before you can use this tool, you need:

#### 1. **Operating System**
- Linux (Ubuntu 22.04 or newer recommended)
- macOS (12 or newer)
- Windows with WSL2 (Windows Subsystem for Linux)

#### 2. **Python 3.10 or Newer**

**Check if you have it:**
```bash
python3 --version
```

**If you see `Python 3.10.x` or higher:** ✅ You're good!
**If you see an error or lower version:** Install Python:

- **Ubuntu/Debian:**
  ```bash
  sudo apt update
  sudo apt install python3.10 python3-pip
  ```

- **macOS:**
  ```bash
  brew install python@3.10
  ```

- **Windows WSL:**
  ```bash
  sudo apt update && sudo apt install python3.10 python3-pip
  ```

#### 3. **Ollama (Local AI Server)**

Ollama runs AI models on your computer (no internet required after setup).

**Install Ollama:**

Visit https://ollama.com/download and follow instructions for your OS.

**Verify installation:**
```bash
ollama --version
```

**Download a model for text analysis:**
```bash
# Fast model (recommended for testing):
ollama pull qwen2.5:3b

# Better model (slower but more accurate):
ollama pull llama3.1:8b
```

#### 4. **Git**

**Check if you have it:**
```bash
git --version
```

**If missing, install:**
- **Ubuntu:** `sudo apt install git`
- **macOS:** `brew install git` or `xcode-select --install`

#### 5. **Ripgrep (Fast Search Tool)**

Used to quickly search through large directories.

**Install:**
- **Ubuntu:** `sudo apt install ripgrep`
- **macOS:** `brew install ripgrep`

**Verify:**
```bash
rg --version
```

---

## Installation

### Step 1: Clone this Repository

```bash
# Navigate to where you want to install (e.g., your projects folder)
cd ~/Documents/Projects

# Clone the repository
git clone https://github.com/TDProServices/conversation-analyzer.git

# Enter the directory
cd conversation-analyzer
```

### Step 2: Set Up Python Environment

**Option A: Using venv (Recommended for beginners)**
```bash
# Create a virtual environment (isolated Python setup)
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/macOS
# OR on Windows WSL:
source venv/bin/activate

# Your prompt should now show (venv)
```

**Option B: Using Docker** *(Coming soon - not yet available)*

### Step 3: Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

**Note:** If you see `ERROR: Could not find requirements.txt`, that's expected - the file will be created during development. For now, this is a placeholder.

---

## How to Use (When Complete)

> **Status:** This project is currently in development. These are planned features.

### Basic Usage

1. **Analyze a Claude Code conversation:**
   ```bash
   python -m conversation_analyzer analyze conversation.md
   ```

2. **Analyze a whole project directory:**
   ```bash
   python -m conversation_analyzer scan ~/Documents/Projects/my-project
   ```

3. **View results:**
   ```bash
   # Results are saved in:
   reports/analysis-2025-11-17.md
   ```

### Configuration

Create a `.conversation-analyzer.yaml` file:
```yaml
# Which Ollama model to use
model: qwen2.5:3b

# Directories to scan
scan_paths:
  - ~/Documents/Projects/

# File patterns to analyze
include_patterns:
  - "*.md"
  - "TODO.md"
  - ".claude/**/*.md"

# Minimum confidence to report (0-100%)
confidence_threshold: 70
```

---

## Project Structure

```
conversation-analyzer/
├── README.md              # This file
├── CLAUDE.md              # Development guidance
├── TODO.md                # Project task tracking
├── requirements.txt       # Python dependencies (to be created)
├── src/                   # Source code (to be created)
│   ├── __init__.py
│   ├── parser.py          # Conversation parser
│   ├── analyzer.py        # LLM-based analysis
│   ├── extractor.py       # TODO/bug extraction
│   └── reporter.py        # Report generation
├── tests/                 # Test suite (to be created)
└── examples/              # Example conversations (to be created)
```

---

## Troubleshooting

### "Command 'ollama' not found"

**Problem:** Ollama isn't installed or not in your PATH.

**Solution:**
1. Visit https://ollama.com/download
2. Install for your OS
3. Restart your terminal
4. Run `ollama --version` to verify

### "No module named 'conversation_analyzer'"

**Problem:** You haven't installed the package yet.

**Solution:**
```bash
# Make sure you're in the project directory
cd ~/Documents/Projects/conversation-analyzer

# Make sure virtual environment is active (you should see `(venv)` in prompt)
source venv/bin/activate

# Install in development mode
pip install -e .
```

**Note:** This will work once we create `setup.py` or `pyproject.toml`.

### "Ollama connection refused"

**Problem:** Ollama server isn't running.

**Solution:**
```bash
# Start Ollama (it usually auto-starts, but if not):
ollama serve

# In another terminal, test:
ollama list
```

### "Permission denied" errors

**Problem:** Don't have write access to directory.

**Solution:**
```bash
# Don't use sudo with pip! Instead:
# 1. Make sure you're in a virtual environment
source venv/bin/activate

# 2. Or install to user directory
pip install --user -r requirements.txt
```

---

## Development Status

### What's Done ✅
- [x] Project structure planned
- [x] Documentation framework created
- [x] Reusable prompts for workflow

### What's In Progress 🚧
- [ ] Technology research (Python project structure, tools)
- [ ] Database schema design
- [ ] Conversation parser implementation
- [ ] Ollama integration

### What's Next 📋
See [TODO.md](TODO.md) for detailed task list and priorities.

---

## Contributing

This is a personal project by Tanya Davis. If you have suggestions, please open an issue on GitHub.

---

## Technical Details

### Why These Technologies?

**Ollama (not OpenAI/Anthropic API):**
- Runs locally - your conversations stay private
- No internet required after setup
- No API costs
- Perfect for sensitive data (legal, medical, personal)

**Python:**
- Easy to read and maintain
- Rich ecosystem for text processing
- Good AI/ML library support

**SQLite:**
- No database server to set up
- Single file, easy to backup
- Fast enough for this use case
- Portable

**Markdown Reports:**
- Human-readable
- Works with git (text-based)
- Easy to search
- Can be version controlled

---

## Frequently Asked Questions

### Is this better than just searching my files?

Yes! Because it:
1. Understands context (using AI)
2. Finds implicit TODOs ("we should probably..." → finds these)
3. Deduplicates (doesn't report same TODO 10 times)
4. Prioritizes (urgent items ranked higher)
5. Cross-references (finds related items across projects)

### How much disk space does it need?

- Ollama models: ~2-8GB (one-time download)
- SQLite database: ~10-100MB (grows over time)
- Conversation Analyzer code: ~1MB

### Can I use it offline?

Yes! After initial setup (downloading Ollama models), it works 100% offline.

### Does it work with ChatGPT/Gemini conversations?

Not yet, but it's planned. Currently only supports Claude Code conversations.

### Will it modify my files?

No! It only reads files. All outputs go to `reports/` directory.

---

## Learn More

- **Development Guide:** See [CLAUDE.md](CLAUDE.md)
- **Detailed Tasks:** See [TODO.md](TODO.md)
- **Reusable Prompts:** See [REUSABLE-PROMPTS.md](REUSABLE-PROMPTS.md)

---

## Contact

**Tanya Davis**
TD Professional Services LLC
GitHub: [@TDProServices](https://github.com/TDProServices)

---

**Last Updated:** 2025-11-17
**Version:** 0.1.0-dev
