"""CLI entry point for Conversation Analyzer."""

import sys
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .config import Config
from .analyzer import ConversationAnalyzer

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Conversation Analyzer - Extract TODOs, bugs, and features from conversations and code."""
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def analyze(path, config, verbose):
    """Analyze files or directories for action items."""
    try:
        # Load config
        cfg = Config.load(config)

        # Find files to analyze
        path_obj = Path(path)
        if path_obj.is_file():
            files = [str(path_obj)]
        else:
            files = []
            # Find conversation files
            for pattern in cfg.sources.conversations:
                files.extend(path_obj.glob(pattern))
            files = [str(f) for f in files]

        if not files:
            console.print(f"[yellow]No files found to analyze in {path}[/yellow]")
            return

        console.print(f"[green]Analyzing {len(files)} file(s)...[/green]")

        # Analyze
        with ConversationAnalyzer(cfg) as analyzer:
            # Test Ollama connection
            if not analyzer.extractor.test_connection():
                console.print(
                    "[red]Error: Cannot connect to Ollama. Is it running?[/red]"
                )
                console.print("Start Ollama with: ollama serve")
                sys.exit(1)

            result = analyzer.analyze_files(files)

            # Display results
            console.print("\n[bold green]Analysis Complete![/bold green]")
            console.print(f"Sources Processed: {result.sources_processed}")
            console.print(f"Items Extracted: {result.items_extracted}")
            if result.items_deduplicated > 0:
                console.print(f"Duplicates Found: {result.items_deduplicated}")
            console.print(f"Duration: {result.duration_seconds:.2f}s")

            if result.errors:
                console.print(f"\n[yellow]Errors: {len(result.errors)}[/yellow]")
                if verbose:
                    for error in result.errors:
                        console.print(f"  - {error}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            raise
        sys.exit(1)


@cli.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
@click.option("--format", "-f", type=click.Choice(["markdown", "json"]), default="markdown")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
def report(config, format, output):
    """Generate a report from analyzed items."""
    try:
        cfg = Config.load(config)

        with ConversationAnalyzer(cfg) as analyzer:
            if not output:
                output = cfg.reporting.output_dir + f"/report.{format[:2]}"

            Path(output).parent.mkdir(parents=True, exist_ok=True)

            report_content = analyzer.generate_report(format, output)

            console.print(f"[green]Report generated: {output}[/green]")

            # Display preview if markdown
            if format == "markdown" and not output:
                console.print(report_content)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
def stats(config):
    """Show statistics from the database."""
    try:
        cfg = Config.load(config)

        with ConversationAnalyzer(cfg) as analyzer:
            stats = analyzer.get_stats()

            # Create table
            table = Table(title="Conversation Analyzer Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Count", style="green")

            table.add_row("Total Items", str(stats.get("total_items", 0)))

            # By type
            by_type = stats.get("by_type", {})
            for item_type, count in sorted(by_type.items()):
                table.add_row(f"  {item_type}", str(count))

            # By priority
            by_priority = stats.get("by_priority", {})
            if by_priority:
                table.add_row("", "")  # Separator
                for priority in ["high", "medium", "low"]:
                    count = by_priority.get(priority, 0)
                    table.add_row(f"  {priority.title()} Priority", str(count))

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--type", "-t", type=click.Choice(["TODO", "BUG", "FEATURE", "PROJECT"]))
@click.option("--priority", "-p", type=click.Choice(["high", "medium", "low"]))
@click.option("--limit", "-l", type=int, default=20)
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
def list(type, priority, limit, config):
    """List items from the database."""
    try:
        cfg = Config.load(config)

        with ConversationAnalyzer(cfg) as analyzer:
            items = analyzer.get_items(item_type=type, priority=priority, status="open")

            if not items:
                console.print("[yellow]No items found[/yellow]")
                return

            # Show up to limit
            items = items[:limit]

            for item in items:
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                type_emoji = {"TODO": "✅", "BUG": "🐛", "FEATURE": "✨", "PROJECT": "📦"}

                console.print(
                    f"\n{type_emoji.get(item.type, '')} {priority_emoji.get(item.priority, '')} "
                    f"[bold]{item.description}[/bold]"
                )
                console.print(f"  Type: {item.type} | Priority: {item.priority}")
                console.print(f"  Source: {item.source_file}")
                if item.source_line:
                    console.print(f"  Line: {item.source_line}")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.option("--config", "-c", type=click.Path(exists=True), help="Config file path")
def test_connection(config):
    """Test connection to Ollama."""
    try:
        cfg = Config.load(config)

        with ConversationAnalyzer(cfg) as analyzer:
            if analyzer.extractor.test_connection():
                console.print("[green]✓ Successfully connected to Ollama[/green]")
                console.print(f"Host: {cfg.ollama.host}")
                console.print(f"Model: {cfg.ollama.extraction_model}")
            else:
                console.print("[red]✗ Cannot connect to Ollama[/red]")
                console.print("Start Ollama with: ollama serve")
                sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
