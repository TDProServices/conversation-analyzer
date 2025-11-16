# Installation Guide

## Prerequisites

- **Python:** 3.10 or higher
- **Operating System:** Linux, macOS, or Windows
- **RAM:** 8GB minimum (16GB recommended for larger models)
- **Disk Space:** 5GB+ for Ollama and models

## Step 1: Install Ollama

Ollama is required for local LLM processing.

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### macOS

```bash
brew install ollama
```

### Windows

Download and install from [ollama.com](https://ollama.com/)

### Verify Installation

```bash
ollama --version
```

### Start Ollama Service

```bash
ollama serve
```

Leave this running in a separate terminal.

## Step 2: Pull Required Models

Pull the NuExtract model (optimized for information extraction):

```bash
ollama pull nuextract
```

This will download ~2.4GB. The download may take several minutes depending on your connection.

**Optional:** Pull llama3.1 for more complex analysis:

```bash
ollama pull llama3.1:8b
```

## Step 3: Clone the Repository

```bash
git clone https://github.com/TDProServices/conversation-analyzer.git
cd conversation-analyzer
```

## Step 4: Set Up Python Environment

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

## Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `ollama` - Ollama Python client
- `langchain` and `langchain-ollama` - LLM orchestration
- `pydantic` - Data validation
- `sentence-transformers` - Embeddings for deduplication
- `click` and `rich` - CLI framework
- `pytest` and `deepeval` - Testing frameworks
- Other supporting libraries

### Optional: Install in Development Mode

If you want to make changes to the code:

```bash
pip install -e ".[dev]"
```

## Step 6: Configure the Application

### Copy Example Environment File

```bash
cp .env.example .env
```

### Edit Configuration (Optional)

The default `config.yaml` should work out of the box. You can customize:

```yaml
ollama:
  host: "http://localhost:11434"
  extraction_model: "nuextract"
  # Change to "llama3.1:8b" for better quality (slower)

database:
  path: "data/database/analyzer.db"

reporting:
  output_dir: "data/reports"
  formats: ["markdown", "json"]
```

## Step 7: Verify Installation

Test the connection to Ollama:

```bash
python -m conversation_analyzer test-connection
```

You should see:
```
✓ Successfully connected to Ollama
Host: http://localhost:11434
Model: nuextract
```

## Troubleshooting

### Cannot connect to Ollama

**Error:** `Cannot connect to Ollama`

**Solution:**
1. Ensure Ollama is running: `ollama serve`
2. Check the host in config.yaml matches where Ollama is running
3. Try: `curl http://localhost:11434/api/tags` to test connection

### Model not found

**Error:** `Model nuextract not found`

**Solution:**
```bash
ollama pull nuextract
```

### Import errors

**Error:** `ModuleNotFoundError: No module named 'sentence_transformers'`

**Solution:**
```bash
pip install -r requirements.txt
```

Ensure your virtual environment is activated.

### Permission errors

**Error:** `Permission denied` when creating data directories

**Solution:**
```bash
sudo chown -R $USER:$USER conversation-analyzer
```

Or run from a directory where you have write permissions.

### Out of memory

**Error:** Process killed or out of memory errors

**Solution:**
- Use a smaller model: Configure `extraction_model: "nuextract"` (default)
- Close other applications
- Increase system swap space
- Use a machine with more RAM

## Updating

To update to the latest version:

```bash
git pull
pip install -r requirements.txt --upgrade
```

## Uninstalling

### Remove Python Environment

```bash
deactivate  # Exit venv
rm -rf venv
```

### Remove Data

```bash
rm -rf data/
```

### Uninstall Ollama Models

```bash
ollama rm nuextract
ollama rm llama3.1:8b
```

### Uninstall Ollama

**Linux:**
```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
```

**macOS:**
```bash
brew uninstall ollama
```

## Next Steps

See [USAGE.md](USAGE.md) for how to use the Conversation Analyzer.
