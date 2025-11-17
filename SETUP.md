# Setup Guide for Conversation Analyzer

**Last Updated:** 2025-11-17
**For:** Beginner/Novice developers
**Time Required:** ~15-30 minutes (depending on internet speed for downloads)

---

## Quick Start (TL;DR)

```bash
# 1. Clone and enter directory
git clone https://github.com/TDProServices/conversation-analyzer.git
cd conversation-analyzer

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Verify installation
conversation-analyzer --version
conversation-analyzer check

# 5. Run tests
pytest
```

---

## Detailed Setup Instructions

### Step 1: Verify Prerequisites

Before starting, make sure you have these installed (see [README.md](README.md) for installation instructions):

**Check each prerequisite:**

```bash
# Python 3.10+
python3 --version
# Should show: Python 3.10.x or higher

# pip
pip --version
# Should show: pip 23.x or higher

# git
git --version
# Should show: git version 2.x or higher

# Ollama (for LLM)
ollama --version
# Should show: ollama version x.x.x

# ripgrep (for fast file search)
rg --version
# Should show: ripgrep x.x.x
```

**If any command fails,** see README.md "Prerequisites" section for installation instructions.

---

### Step 2: Clone Repository

```bash
# Navigate to where you keep projects
cd ~/Documents/Projects  # Or your preferred location

# Clone from GitHub
git clone https://github.com/TDProServices/conversation-analyzer.git

# Enter the directory
cd conversation-analyzer

# Verify you're in the right place
ls
# You should see: README.md, CLAUDE.md, pyproject.toml, etc.
```

---

### Step 3: Create Virtual Environment

**What is a virtual environment?**
A virtual environment is an isolated Python setup just for this project. It prevents conflicts with other Python projects.

**Why do we need it?**
Without it, installing packages can break other Python tools on your system.

**Create and activate:**

```bash
# Create virtual environment (one-time setup)
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# On Windows (Git Bash):
source venv/Scripts/activate
```

**How to tell it's activated:**
Your command prompt should now show `(venv)` at the beginning:
```
(venv) user@computer:~/conversation-analyzer$
```

**To deactivate later:** Type `deactivate` (but keep it active for now)

---

### Step 4: Install Dependencies

**Option A: Install Everything (Recommended for Development)**

```bash
# This installs both production and development dependencies
pip install -e ".[dev]"

# Breakdown of what this does:
# - pip: Python package installer
# - install: Command to install packages
# - -e: "Editable" mode - install as development (changes reflect immediately)
# - .: Current directory (conversation-analyzer)
# - [dev]: Include development dependencies (testing, linting)
```

**Wait for installation to complete** (may take 1-5 minutes depending on internet speed)

**Option B: Install Only Production Dependencies**

```bash
# If you only want to run the tool (not develop it)
pip install -e .
```

**Option C: Using requirements.txt (Alternative)**

```bash
# Production dependencies only
pip install -r requirements.txt

# Development dependencies too
pip install -r requirements-dev.txt
```

---

### Step 5: Download Ollama Models

**Required for analysis to work:**

```bash
# Download fast model (primary, ~2GB)
ollama pull qwen2.5:3b

# Optional: Download more accurate model (fallback, ~4.7GB)
ollama pull llama3.1:8b
```

**This will take time** depending on your internet speed:
- qwen2.5:3b: ~2-10 minutes
- llama3.1:8b: ~5-20 minutes

**Verify models downloaded:**
```bash
ollama list
# Should show:
# qwen2.5:3b      ...
# llama3.1:8b     ... (if you downloaded it)
```

---

### Step 6: Verify Installation

**Check that everything works:**

```bash
# Check version
conversation-analyzer --version
# Should show: conversation-analyzer, version 0.1.0

# Check help
conversation-analyzer --help
# Should show: Usage: conversation-analyzer [OPTIONS] COMMAND [ARGS]...

# Check system requirements
conversation-analyzer check
# This will verify Ollama is running and models are available
```

---

### Step 7: Run Tests

**Make sure everything is working:**

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

**Expected output:**
```
====== test session starts ======
collected X items

tests/test_cli.py ....                  [100%]

====== X passed in X.XXs ======
```

**If tests fail:** Check that you activated the virtual environment and installed dependencies.

---

### Step 8: Configuration (Optional)

**Create your config file:**

```bash
# Copy example config
cp .conversation-analyzer.yaml.example .conversation-analyzer.yaml

# Edit with your preferences
nano .conversation-analyzer.yaml  # or vim, code, etc.
```

**Key settings to customize:**
- `scan_paths`: Where your projects are located
- `confidence_threshold`: How confident the AI should be (70-90% recommended)
- `models.primary`: Which Ollama model to use

See `.conversation-analyzer.yaml.example` for all options with detailed comments.

---

## Troubleshooting

### "python3: command not found"

**Problem:** Python isn't installed or not in PATH.

**Solution:**
- Install Python 3.10+ (see README.md)
- On Windows, make sure "Add to PATH" was checked during installation
- Restart terminal after installing

---

### "No module named 'conversation_analyzer'"

**Problem:** Package isn't installed, or virtual environment not activated.

**Solution:**
```bash
# Make sure venv is activated (you should see (venv) in prompt)
source venv/bin/activate

# Reinstall
pip install -e ".[dev]"
```

---

### "Connection refused" when checking Ollama

**Problem:** Ollama service isn't running.

**Solution:**
```bash
# Start Ollama (usually auto-starts, but if not)
ollama serve

# In another terminal, verify
ollama list
```

---

### "Permission denied" errors during pip install

**Problem:** Trying to install system-wide without proper permissions.

**Solution:**
**Never use `sudo pip`!** This can break your system Python.

Instead:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Then install
pip install -e ".[dev]"
```

---

### Virtual environment won't activate on Windows

**Problem:** PowerShell execution policy blocks scripts.

**Solution:**
```powershell
# Option 1: Use Command Prompt instead
venv\Scripts\activate.bat

# Option 2: Change execution policy (PowerShell, as admin)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
venv\Scripts\activate
```

---

### Tests fail with "ollama.exceptions.ResponseError"

**Problem:** Ollama not running or model not downloaded.

**Solution:**
```bash
# Start Ollama
ollama serve

# Download required model
ollama pull qwen2.5:3b

# Run tests again
pytest
```

---

## Development Workflow

**Daily workflow:**

```bash
# 1. Navigate to project
cd ~/Documents/Projects/conversation-analyzer

# 2. Activate virtual environment
source venv/bin/activate

# 3. Pull latest changes (if working with others)
git pull origin main

# 4. Make your changes to code

# 5. Run tests
pytest

# 6. Run linters
ruff check src/
black src/
mypy src/

# 7. Commit your work
git add .
git commit -m "your message"
git push

# 8. Deactivate when done
deactivate
```

---

## Updating Dependencies

**When to update:**
- Security vulnerabilities found
- New features in dependencies you need
- Every few months for general maintenance

**How to update:**

```bash
# Update all packages to latest compatible versions
pip install --upgrade -e ".[dev]"

# Update requirements files
pip list --format=freeze > requirements.txt
```

**After updating:** Run tests to make sure nothing broke!

---

## Uninstalling

**To remove everything:**

```bash
# 1. Deactivate virtual environment
deactivate

# 2. Remove directory
cd ..
rm -rf conversation-analyzer

# 3. Uninstall Ollama models (if you want to free space)
ollama rm qwen2.5:3b
ollama rm llama3.1:8b
```

---

## Next Steps

Once setup is complete:

1. **Read the User Guide** (coming in Phase 4)
2. **Try analyzing a conversation:** `conversation-analyzer analyze <file.md>`
3. **Check TODO.md** for current development status
4. **Read CLAUDE.md** if you want to contribute

---

## Getting Help

**If you're stuck:**

1. **Check this guide's Troubleshooting section** (above)
2. **See README.md** for detailed prerequisite installation
3. **Check CLAUDE.md** for development guidance
4. **Search GitHub Issues:** https://github.com/TDProServices/conversation-analyzer/issues
5. **Create a new issue** with:
   - Your OS and Python version
   - Full error message
   - What you tried
   - Output of `conversation-analyzer check`

---

**Setup Complete!** 🎉

You're ready to start using conversation-analyzer.

See README.md for usage examples and features.
