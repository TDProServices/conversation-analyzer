"""Unit tests for parsers."""

import pytest
from conversation_analyzer.parsers.conversation import ConversationParser
from conversation_analyzer.parsers.code import CodeParser


class TestConversationParser:
    """Test conversation parser."""

    def test_can_parse_markdown(self):
        """Test that parser recognizes markdown files."""
        parser = ConversationParser()
        assert parser.can_parse("test.md")
        assert parser.can_parse("test.markdown")
        assert not parser.can_parse("test.txt")

    def test_can_parse_json(self):
        """Test that parser recognizes JSON files."""
        parser = ConversationParser()
        assert parser.can_parse("test.json")

    def test_parse_simple_conversation(self, sample_conversation):
        """Test parsing a simple conversation."""
        parser = ConversationParser()
        chunks = parser.parse(sample_conversation)

        assert len(chunks) > 0
        assert chunks[0].source_type == "conversation"
        assert len(chunks[0].text) > 0

    def test_get_source_type(self):
        """Test getting source type."""
        parser = ConversationParser()
        assert parser.get_source_type() == "conversation"


class TestCodeParser:
    """Test code parser."""

    def test_can_parse_python(self):
        """Test that parser recognizes Python files."""
        parser = CodeParser()
        assert parser.can_parse("test.py")
        assert not parser.can_parse("test.txt")

    def test_can_parse_javascript(self):
        """Test that parser recognizes JavaScript files."""
        parser = CodeParser()
        assert parser.can_parse("test.js")
        assert parser.can_parse("test.ts")
        assert parser.can_parse("test.jsx")

    def test_parse_code_with_comments(self, sample_code):
        """Test parsing code file with comments."""
        parser = CodeParser()
        chunks = parser.parse(sample_code)

        assert len(chunks) > 0
        # Should find TODO/FIXME/BUG comments
        assert any("TODO" in chunk.text or "FIXME" in chunk.text for chunk in chunks)

    def test_get_source_type(self):
        """Test getting source type."""
        parser = CodeParser()
        assert parser.get_source_type() == "code"

    def test_extract_line_numbers(self, sample_code):
        """Test that line numbers are extracted."""
        parser = CodeParser()
        chunks = parser.parse(sample_code)

        # Check that line numbers are present
        for chunk in chunks:
            assert chunk.source_line is not None
            assert chunk.source_line > 0
