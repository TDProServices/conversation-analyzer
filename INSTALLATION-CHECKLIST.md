# Installation Checklist

**Purpose:** Quick verification that all prerequisites are installed correctly
**Time Required:** 5-10 minutes
**For:** Beginners setting up for the first time

---

## ✅ Pre-Installation Checklist

### 1. Python 3.10 or Higher

```bash
python3 --version
```

**Expected output:** `Python 3.10.x` or higher (3.11, 3.12 also work)

**If failed:**
- **Ubuntu/Debian:** `sudo apt install python3.10 python3-pip python3-venv`
- **macOS:** `brew install [email protected]`
- **Windows:** Download from https://www.python.org/downloads/ (check "Add to PATH")

---

### 2. pip (Python Package Installer)

```bash
pip --version
# OR
python3 -m pip --version
```

**Expected output:** `pip 23.x` or higher

**If failed:**
```bash
python3 -m ensurepip --upgrade
```

---

### 3. git (Version Control)

```bash
git --version
```

**Expected output:** `git version 2.x` or higher

**If failed:**
- **Ubuntu/Debian:** `sudo apt install git`
- **macOS:** `brew install git` (or install Xcode Command Line Tools)
- **Windows:** Download from https://git-scm.com/download/win

---

### 4. Ollama (Local LLM Server)

```bash
ollama --version
```

**Expected output:** `ollama version x.x.x`

**If failed:**
- **Linux:** `curl -fsSL https://ollama.com/install.sh | sh`
- **macOS:** `brew install ollama` OR download from https://ollama.com/download
- **Windows:** Download from https://ollama.com/download

**Verify Ollama is running:**
```bash
ollama list
```

**If "connection refused":**
```bash
ollama serve
```

**Download required models:**
```bash
ollama pull qwen2.5:3b        # Primary (2GB, fast)
ollama pull llama3.1:8b       # Optional (4.7GB, more accurate)
```

---

### 5. Ripgrep (Fast File Search)

```bash
rg --version
```

**Expected output:** `ripgrep x.x.x`

**If failed:**
- **Ubuntu/Debian:** `sudo apt install ripgrep`
- **macOS:** `brew install ripgrep`
- **Windows:** `choco install ripgrep` OR `scoop install ripgrep`

**Alternative:** Project will work without ripgrep, but file scanning will be slower

---

## ✅ Project Installation Checklist

### 1. Clone Repository

```bash
cd ~/Documents/Projects  # Or your preferred location
git clone https://github.com/TDProServices/conversation-analyzer.git
cd conversation-analyzer
```

**Verify:** You should see `README.md`, `CLAUDE.md`, `pyproject.toml`, etc.

```bash
ls
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

**Verify:** `venv/` directory created

```bash
ls venv/
# Should show: bin/ (or Scripts/ on Windows), lib/, etc.
```

---

### 3. Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Verify:** Your prompt should show `(venv)` at the beginning

```bash
which python
# Should show: /path/to/conversation-analyzer/venv/bin/python
```

---

### 4. Install Dependencies

```bash
pip install -e ".[dev]"
```

**This will take 1-5 minutes.** You should see packages installing:
- ollama
- mistune
- click
- pytest
- ruff
- black
- mypy
- etc.

**Verify:**
```bash
pip list | grep conversation-analyzer
# Should show: conversation-analyzer 0.1.0 (with your path)
```

---

### 5. Verify CLI Installation

```bash
conversation-analyzer --version
```

**Expected output:** `conversation-analyzer, version 0.1.0`

```bash
conversation-analyzer --help
```

**Expected output:** Usage information with commands (analyze, scan, report, check)

---

### 6. Run System Check

```bash
conversation-analyzer check
```

**Expected output:** Should verify:
- ✅ Ollama is running
- ✅ Models are available (qwen2.5:3b)
- ✅ Python version correct
- ⚠️ Note: This command is scaffolded (Phase 4), may show "Implementation pending"

---

### 7. Run Tests

```bash
pytest
```

**Expected output:**
```
====== test session starts ======
collected X items

tests/test_cli.py ....                  [100%]

====== X passed in X.XXs ======
```

**If any tests fail:** Check that venv is activated and dependencies installed

---

### 8. Run Linters

```bash
# Check code style
ruff check src/ tests/

# Check formatting
black --check src/ tests/

# Type check
mypy src/
```

**Expected:** Should run without errors (mypy may have warnings, that's OK)

---

### 9. Optional: Create Configuration File

```bash
cp .conversation-analyzer.yaml.example .conversation-analyzer.yaml
```

**Edit with your preferences:**
```bash
nano .conversation-analyzer.yaml
# OR
code .conversation-analyzer.yaml
```

---

## ✅ Final Verification

### All Systems Go!

If you've completed all steps above successfully:

✅ Python 3.10+ installed
✅ pip working
✅ git installed
✅ Ollama installed and running
✅ qwen2.5:3b model downloaded
✅ Ripgrep installed (optional)
✅ Repository cloned
✅ Virtual environment created and activated
✅ Dependencies installed
✅ CLI command works
✅ Tests pass
✅ Linters run clean

**You're ready to go!** 🎉

---

## 🆘 Troubleshooting Checklist

### Problem: "python3: command not found"

- [ ] Python installed? `python --version` (try without the 3)
- [ ] PATH configured? (Windows: check "Add to PATH" was selected)
- [ ] Terminal restarted after installation?

### Problem: "pip: command not found"

- [ ] Try `python3 -m pip` instead
- [ ] Try `python -m pip` instead
- [ ] Run `python3 -m ensurepip --upgrade`

### Problem: "(venv) not showing in prompt"

- [ ] Did you run `source venv/bin/activate`? (Linux/macOS)
- [ ] Did you run `venv\Scripts\activate`? (Windows)
- [ ] Try deactivating (`deactivate`) and activating again

### Problem: "conversation-analyzer: command not found"

- [ ] Virtual environment activated? (should see `(venv)`)
- [ ] Dependencies installed? `pip list | grep conversation-analyzer`
- [ ] Try `python -m conversation_analyzer.cli --help`

### Problem: "Connection refused" (Ollama)

- [ ] Ollama installed? `ollama --version`
- [ ] Ollama running? `ollama serve` (in separate terminal)
- [ ] Firewall blocking port 11434?

### Problem: Tests failing

- [ ] Virtual environment activated?
- [ ] Dependencies installed? `pip install -e ".[dev]"`
- [ ] Ollama running?
- [ ] Models downloaded? `ollama list`

### Problem: Permission denied

- [ ] Using virtual environment? (NEVER `sudo pip`)
- [ ] Own the directory? `ls -la` (should show your username)
- [ ] On Windows: running as Administrator? (usually not needed)

---

## 📚 Next Steps After Installation

1. **Read README.md** - Understand what the tool does
2. **Read SETUP.md** - Detailed setup guide (you just completed this!)
3. **Check TODO.md** - See current development status
4. **Try example conversations** - `examples/conversations/*.md`
5. **Wait for Phase 4** - CLI implementation coming soon!

---

## 🔄 Updating Installation

### Update Dependencies

```bash
# Activate venv
source venv/bin/activate

# Pull latest code
git pull origin main

# Update dependencies
pip install --upgrade -e ".[dev]"

# Run tests
pytest
```

### Update Ollama Models

```bash
ollama pull qwen2.5:3b
ollama pull llama3.1:8b
```

---

## 📞 Getting Help

If you're still stuck after checking this list:

1. **Check SETUP.md Troubleshooting section**
2. **Search GitHub Issues:** https://github.com/TDProServices/conversation-analyzer/issues
3. **Create new issue** with:
   - Your OS (Ubuntu 22.04, macOS 14, Windows 11, etc.)
   - Python version (`python3 --version`)
   - Error message (full text)
   - What you tried
   - Output of `conversation-analyzer check` (if CLI works)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Status:** Complete checklist for Phase 3 setup
