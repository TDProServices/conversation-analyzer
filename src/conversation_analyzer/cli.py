"""
Command-line interface for conversation-analyzer

This module provides the main CLI entry point for the tool.
Uses Click for argument parsing per research findings (RESEARCH.md).
"""

import click
from . import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """
    Conversation Analyzer - Extract TODOs, bugs, and features from conversations.

    This tool analyzes Claude Code conversations and project files using local
    LLM models (Ollama) to automatically discover action items you may have missed.

    Examples:
        # Analyze a single conversation file
        conversation-analyzer analyze conversation.md

        # Scan entire project directory
        conversation-analyzer scan ~/Documents/Projects/my-project

        # Generate report from database
        conversation-analyzer report --output report.md
    """
    pass


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option(
    "--model",
    default="qwen2.5:3b",
    help="Ollama model to use (default: qwen2.5:3b)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for results (default: stdout)",
)
def analyze(file_path: str, model: str, output: str | None):
    """
    Analyze a single conversation file.

    FILE_PATH: Path to the conversation markdown file to analyze
    """
    click.echo(f"Analyzing {file_path} with model {model}...")
    click.echo("⚠️  Implementation pending (Phase 4)")
    # TODO: Implement conversation analysis
    # 1. Load conversation from file_path
    # 2. Parse with mistune
    # 3. Extract TODOs/bugs/features with Ollama
    # 4. Save to database
    # 5. Generate report to output or stdout


@main.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option(
    "--pattern",
    default="**/*.md",
    help="File pattern to match (default: **/*.md)",
)
@click.option(
    "--model",
    default="qwen2.5:3b",
    help="Ollama model to use",
)
def scan(directory: str, pattern: str, model: str):
    """
    Scan directory for conversations and analyze all matches.

    DIRECTORY: Path to directory to scan recursively
    """
    click.echo(f"Scanning {directory} for {pattern}...")
    click.echo(f"Using model: {model}")
    click.echo("⚠️  Implementation pending (Phase 4)")
    # TODO: Implement directory scanning
    # 1. Find all files matching pattern
    # 2. Filter for conversation files
    # 3. Analyze each with analyze() logic
    # 4. Generate consolidated report


@main.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="reports/analysis-report.md",
    help="Output file for report",
)
@click.option(
    "--format",
    type=click.Choice(["markdown", "json", "html"]),
    default="markdown",
    help="Report format",
)
def report(output: str, format: str):
    """
    Generate report from analyzed conversations in database.
    """
    click.echo(f"Generating {format} report to {output}...")
    click.echo("⚠️  Implementation pending (Phase 4)")
    # TODO: Implement report generation
    # 1. Load findings from SQLite database
    # 2. Deduplicate and prioritize
    # 3. Generate report in specified format
    # 4. Save to output file


@main.command()
def check():
    """
    Check system requirements and configuration.

    Verifies:
    - Ollama is installed and running
    - Required models are available
    - Database is accessible
    - Configuration is valid
    """
    click.echo("Checking system requirements...")

    # Check Ollama
    click.echo("  [  ] Ollama service... (checking)")
    click.echo("  [  ] Models available... (checking)")
    click.echo("  [  ] Database accessible... (checking)")
    click.echo("⚠️  Implementation pending (Phase 4)")

    # TODO: Implement system checks
    # 1. Try connecting to Ollama (http://localhost:11434)
    # 2. List available models
    # 3. Check if qwen2.5:3b is downloaded
    # 4. Verify database can be created/accessed
    # 5. Load and validate config


if __name__ == "__main__":
    main()
