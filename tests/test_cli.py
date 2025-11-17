"""
Tests for CLI module

These tests verify the command-line interface works correctly.
"""

import pytest
from click.testing import CliRunner
from conversation_analyzer.cli import main


class TestCLI:
    """Test suite for CLI commands"""

    def test_version(self):
        """Test that --version flag works"""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help(self):
        """Test that --help flag works"""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Conversation Analyzer" in result.output

    def test_analyze_command_exists(self):
        """Test that analyze command is registered"""
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", "--help"])
        assert result.exit_code == 0
        assert "Analyze a single conversation file" in result.output

    def test_scan_command_exists(self):
        """Test that scan command is registered"""
        runner = CliRunner()
        result = runner.invoke(main, ["scan", "--help"])
        assert result.exit_code == 0
        assert "Scan directory" in result.output

    def test_check_command_exists(self):
        """Test that check command is registered"""
        runner = CliRunner()
        result = runner.invoke(main, ["check", "--help"])
        assert result.exit_code == 0
        assert "Check system requirements" in result.output


# Add more tests as implementation progresses
