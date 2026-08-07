"""
CLI entry point for SmartSort.

Provides a user-friendly command-line interface with colorful output
using the rich library. Supports organize, watch, undo, and dry-run modes.
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import __version__
from .organizer import organize_folder
from .undo import undo_last
from .watcher import watch_folder


console = Console()


BANNER = r"""
   ___                     _   ___            _
  / __|_ __  __ _ _ _ ___ | |_/ __|___ _ _ __| |_
  \__ \ '  \/ _` | '_/ -_)|  _\__ \/ _ \ '_|  _|
  |___/_|_|_\__,_|_| \___| \__|___/\___/_|  \__|
"""


def print_banner() -> None:
    """Display the SmartSort banner."""
    console.print(
        Panel(
            Text(BANNER, style="bold cyan")
            + Text(f"\n  v{__version__} -- Automated File Organizer", style="dim"),
            border_style="bright_blue",
        )
    )


def print_summary(summary: dict) -> None:
    """
    Display a colorful summary of the organize operation.

    Args:
        summary: The summary dict returned by organize_folder().
    """
    mode = "[bold yellow]DRY RUN[/]" if summary["dry_run"] else "[bold green]COMPLETE[/]"

    console.print()

    # Stats panel
    stats_text = (
        f"[>] Folder:      [cyan]{summary['folder']}[/]\n"
        f"[>] Total files:  [bold]{summary['total_files']}[/]\n"
        f"[>] Moved:        [bold green]{summary['moved']}[/]\n"
        f"[>] Skipped:      [dim]{summary['skipped']}[/]\n"
        f"[>] Status:       {mode}"
    )

    console.print(
        Panel(stats_text, title="[bold][Summary][/]", border_style="green")
    )

    # Categories table
    if summary["categories"]:
        table = Table(
            title="Files by Category",
            show_header=True,
            header_style="bold magenta",
            border_style="bright_blue",
        )
        table.add_column("Category", style="cyan", min_width=15)
        table.add_column("Files", style="green", justify="right")

        # Sort by count (descending)
        sorted_cats = sorted(
            summary["categories"].items(), key=lambda x: x[1], reverse=True
        )
        for category, count in sorted_cats:
            table.add_row(f"  {category}", str(count))

        console.print(table)

    # Errors
    if summary["errors"]:
        console.print()
        for error in summary["errors"]:
            console.print(f"  [bold red][X][/] {error}")

    # Dry run reminder
    if summary["dry_run"]:
        console.print()
        console.print(
            "[bold yellow][i] This was a dry run. "
            "No files were actually moved.[/]"
        )
        console.print(
            "[dim]    Run without --dry-run to apply changes.[/]"
        )

    console.print()


def print_undo_summary(summary: dict) -> None:
    """
    Display the undo operation results.

    Args:
        summary: The summary dict returned by undo_last().
    """
    console.print()

    if summary["errors"] and summary["restored"] == 0:
        console.print(
            Panel(
                "[bold yellow][!] " + summary["errors"][0] + "[/]",
                border_style="yellow",
            )
        )
        return

    stats_text = (
        f"[<] Operation:    Undo (from {summary['timestamp']})\n"
        f"[+] Restored:     [bold green]{summary['restored']}[/]\n"
        f"[X] Failed:       [bold red]{summary['failed']}[/]"
    )

    console.print(
        Panel(stats_text, title="[bold][Undo Summary][/]", border_style="cyan")
    )

    if summary["errors"]:
        for error in summary["errors"]:
            console.print(f"  [bold red][X][/] {error}")

    console.print()


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="smartsort",
        description="SmartSort -- Automatically organize files into categorized folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  smartsort ~/Downloads              Organize Downloads folder\n"
            "  smartsort ~/Downloads --dry-run     Preview without moving\n"
            "  smartsort ~/Downloads --watch       Watch for new files\n"
            "  smartsort ~/Downloads --undo        Undo last operation\n"
            "  smartsort . --config rules.json     Use custom rules\n"
        ),
    )

    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Path to the folder to organize (default: current directory).",
    )

    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch the folder and auto-sort new files in real-time.",
    )

    parser.add_argument(
        "--undo", "-u",
        action="store_true",
        help="Undo the last organize operation.",
    )

    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Preview what would happen without moving any files.",
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to a custom config.json with sorting rules.",
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"SmartSort v{__version__}",
    )

    return parser


def main() -> None:
    """Main entry point for the SmartSort CLI."""
    parser = create_parser()
    args = parser.parse_args()

    print_banner()

    folder = str(Path(args.folder).resolve())

    try:
        if args.undo:
            # Undo mode
            console.print("[bold cyan][<] Undoing last operation...[/]\n")
            summary = undo_last(folder)
            print_undo_summary(summary)

        elif args.watch:
            # Watch mode
            watch_folder(folder, args.config)

        else:
            # Organize mode (one-shot)
            if args.dry_run:
                console.print("[bold yellow][~] Running in dry-run mode...[/]\n")
            else:
                console.print("[bold green][>] Organizing files...[/]\n")

            summary = organize_folder(folder, args.config, args.dry_run)
            print_summary(summary)

    except FileNotFoundError as e:
        console.print(f"[bold red][X] Error:[/] {e}")
        sys.exit(1)
    except NotADirectoryError as e:
        console.print(f"[bold red][X] Error:[/] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow][!] Interrupted.[/] Goodbye!")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red][X] Unexpected error:[/] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
