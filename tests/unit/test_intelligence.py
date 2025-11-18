"""Unit tests for intelligence features."""

import pytest
from conversation_analyzer.intelligence.scorer import PriorityScorer
from conversation_analyzer.intelligence.linker import EntityLinker
from conversation_analyzer.config import PriorityScoringConfig, EntityLinkingConfig


class TestPriorityScorer:
    """Test priority scoring."""

    def test_calculate_score_urgency_keywords(self):
        """Test that urgency keywords increase score."""
        config = PriorityScoringConfig()
        scorer = PriorityScorer(config)

        item = {
            "description": "URGENT: Fix the bug",
            "source_context": "This is urgent",
            "priority": "medium",
            "type": "BUG",
        }

        score = scorer.calculate_score(item)
        assert score > 0.5  # Should be higher than base

    def test_calculate_score_security_keywords(self):
        """Test that security keywords increase score."""
        config = PriorityScoringConfig()
        scorer = PriorityScorer(config)

        item = {
            "description": "SQL injection vulnerability",
            "source_context": "Security issue found",
            "priority": "high",
            "type": "BUG",
        }

        score = scorer.calculate_score(item)
        assert score >= 0.75  # Should be high priority

    def test_get_priority(self):
        """Test converting score to priority label."""
        config = PriorityScoringConfig()
        scorer = PriorityScorer(config)

        assert scorer.get_priority(0.9) == "high"
        assert scorer.get_priority(0.6) == "medium"
        assert scorer.get_priority(0.3) == "low"

    def test_recalculate_priority(self):
        """Test recalculating priority."""
        config = PriorityScoringConfig()
        scorer = PriorityScorer(config)

        item = {
            "description": "Critical security bug",
            "source_context": "Blocks all users",
            "priority": "low",  # Wrong initial priority
            "type": "BUG",
        }

        priority, score = scorer.recalculate_priority(item)
        assert priority == "high"  # Should be corrected
        assert score > 0.7


class TestEntityLinker:
    """Test entity linking."""

    def test_extract_file_paths(self):
        """Test extracting file paths from text."""
        config = EntityLinkingConfig()
        linker = EntityLinker(config)

        text = "Fix bug in src/auth.py and tests/test_auth.py"
        entities = linker.extract_entities(text)

        assert "files" in entities
        assert "src/auth.py" in entities["files"]

    def test_extract_function_names(self):
        """Test extracting function names."""
        config = EntityLinkingConfig()
        linker = EntityLinker(config)

        text = "Call authenticate() and login() functions"
        entities = linker.extract_entities(text)

        assert "functions" in entities
        assert "authenticate" in entities["functions"]
        assert "login" in entities["functions"]

    def test_extract_component_names(self):
        """Test extracting component names."""
        config = EntityLinkingConfig()
        linker = EntityLinker(config)

        text = "Update UserService and AuthController classes"
        entities = linker.extract_entities(text)

        assert "components" in entities
        assert "UserService" in entities["components"]
        assert "AuthController" in entities["components"]

    def test_link_items(self):
        """Test linking related items."""
        config = EntityLinkingConfig()
        linker = EntityLinker(config)

        items = [
            {
                "id": 1,
                "description": "Fix bug in auth.py",
                "source_context": "auth.py has an issue",
            },
            {
                "id": 2,
                "description": "Update auth.py tests",
                "source_context": "auth.py tests need updating",
            },
            {
                "id": 3,
                "description": "Unrelated item",
                "source_context": "Something else entirely",
            },
        ]

        linked = linker.link_items(items)

        # Items 1 and 2 should be linked (both mention auth.py)
        assert "related_to" in linked[0]
        assert 2 in linked[0]["related_to"]
