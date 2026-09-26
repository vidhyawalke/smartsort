"""
Folder watcher module for SmartSort.

Uses the watchdog library to monitor a folder for new files
and automatically organize them in real-time.
"""

from __future__ import annotations

import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .organizer import organize_single_file


class SmartSortHandler(FileSystemEventHandler):
    """
    Handles file system events for the SmartSort watcher.

    When a new file is created in the watched folder, it is
    automatically organized into the appropriate category subfolder.
    """

    def __init__(self, target_folder: str, config_path: str | None = None):
        """
        Initialize the handler.

        Args:
            target_folder: The folder being watched.
            config_path: Optional path to a custom config.json.
        """
        super().__init__()
        self.target_folder = target_folder
        self.config_path = config_path

        # Track recently processed files to avoid duplicates
        self._recently_processed: set[str] = set()

    def on_created(self, event: FileCreatedEvent) -> None:
        """Called when a new file is created in the watched folder."""
        if event.is_directory:
            return

        file_path = event.src_path

        # Skip if we just processed this file (watchdog can fire multiple events)
        if file_path in self._recently_processed:
            return

        # Only handle files dropped directly in the watched folder, not in subfolders
        file = Path(file_path)
        watched = Path(self.target_folder).resolve()
        if file.parent.resolve() != watched:
            return

        # Give the OS a moment to finish writing the file before we try to move it
        time.sleep(0.5)

        # Check file still exists (it might have been a temp file)
        if not file.exists():
            return

        self._recently_processed.add(file_path)

        # Organize the file
        try:
            from rich.console import Console

            console = Console()

            result = organize_single_file(
                file_path, self.target_folder, self.config_path
            )

            if result:
                console.print(
                    f"  [+] [bold green]{file.name}[/] -> "
                    f"[cyan]{result['category']}/[/]"
                )
            else:
                console.print(
                    f"  [~] [dim]{file.name} -- skipped[/]"
                )

        except Exception as e:
            print(f"  [X] Error processing {file.name}: {e}")

        # Prevent the tracking set from growing without bound in long sessions
        if len(self._recently_processed) > 1000:
            self._recently_processed.clear()


def watch_folder(
    folder_path: str, config_path: str | None = None
) -> None:
    """
    Start watching a folder for new files and auto-organize them.

    This function blocks until the user presses Ctrl+C.

    Args:
        folder_path: Path to the folder to watch.
        config_path: Optional path to a custom config.json.
    """
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    folder = Path(folder_path).resolve()

    if not folder.exists():
        console.print(f"[bold red][X] Folder not found:[/] {folder}")
        return
    if not folder.is_dir():
        console.print(f"[bold red][X] Not a directory:[/] {folder}")
        return

    # Create the event handler and observer
    handler = SmartSortHandler(str(folder), config_path)
    observer = Observer()
    observer.schedule(handler, str(folder), recursive=False)

    console.print()
    console.print(
        Panel(
            f"[*] Watching: [bold cyan]{folder}[/]\n"
            f"[+] New files will be auto-sorted into category folders.\n"
            f"[!] Press [bold red]Ctrl+C[/] to stop.",
            title="[bold green]SmartSort Watch Mode[/]",
            border_style="green",
        )
    )
    console.print()

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n[bold yellow][!] Watcher stopped.[/] Goodbye!")

    observer.join()
