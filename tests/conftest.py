"""Pytest configuration and fixtures."""

import pytest
import tempfile
import os
from pathlib import Path

from conversation_analyzer.config import Config
from conversation_analyzer.database import Database
from conversation_analyzer.models import Item


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_db(temp_dir):
    """Create a temporary database for tests."""
    db_path = os.path.join(temp_dir, "test.db")
    db = Database(db_path)
    yield db
    db.close()


@pytest.fixture
def test_config(temp_dir):
    """Create a test configuration."""
    config = Config()
    config.database.path = os.path.join(temp_dir, "test.db")
    config.ollama.host = "http://localhost:11434"
    config.ollama.extraction_model = "nuextract"
    config.extraction.confidence_threshold = 0.5
    return config


@pytest.fixture
def sample_item():
    """Create a sample item for testing."""
    return Item(
        type="TODO",
        description="Fix the login bug",
        priority="high",
        priority_score=0.8,
        source_context="We need to fix the login bug urgently",
        confidence=0.9,
        source_type="conversation",
        source_file="test.md",
    )


@pytest.fixture
def sample_items():
    """Create multiple sample items for testing."""
    return [
        Item(
            type="BUG",
            description="SQL injection vulnerability",
            priority="high",
            priority_score=0.95,
            source_context="FIXME: SQL injection in login",
            confidence=0.95,
            source_type="code",
            source_file="auth.py",
            source_line=42,
        ),
        Item(
            type="TODO",
            description="Update documentation",
            priority="medium",
            priority_score=0.5,
            source_context="TODO: update the docs",
            confidence=0.9,
            source_type="conversation",
            source_file="chat.md",
        ),
        Item(
            type="FEATURE",
            description="Add dark mode",
            priority="low",
            priority_score=0.3,
            source_context="Maybe add dark mode someday",
            confidence=0.7,
            source_type="conversation",
            source_file="chat.md",
        ),
    ]


@pytest.fixture
def fixtures_dir():
    """Get path to fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_conversation(fixtures_dir):
    """Get path to sample conversation."""
    return str(fixtures_dir / "conversations" / "sample_simple.md")


@pytest.fixture
def sample_code(fixtures_dir):
    """Get path to sample code file."""
    return str(fixtures_dir / "code" / "sample_code.py")


class MockOllamaClient:
    """Mock Ollama client for testing without Ollama."""

    def __init__(self, config=None):
        self.config = config

    def generate(self, prompt, model=None, temperature=None, max_retries=3):
        """Mock generate method."""
        # Return mock extraction result
        return '{"items": [{"type": "TODO", "description": "Test item", "priority": "medium", "source_context": "test", "confidence": 0.8}]}'

    def chat(self, messages, model=None, temperature=None, max_retries=3):
        """Mock chat method."""
        return self.generate("", model, temperature)

    def extract_json(self, prompt, model=None, temperature=None):
        """Mock extract_json method."""
        import json

        return json.loads(self.generate(prompt, model, temperature))

    def test_connection(self):
        """Mock connection test."""
        return True

    def is_model_available(self, model_name):
        """Mock model availability check."""
        return True


@pytest.fixture
def mock_ollama(monkeypatch):
    """Mock Ollama client for testing."""
    from conversation_analyzer.extraction import ollama_client

    monkeypatch.setattr(ollama_client, "OllamaClient", MockOllamaClient)
    return MockOllamaClient
