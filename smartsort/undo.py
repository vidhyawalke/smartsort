"""
Undo module for SmartSort.

Tracks file move operations in a JSON history file so they
can be reversed. The history file is stored in the organized folder.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path


HISTORY_FILENAME = ".smartsort_history.json"


def _get_history_path(folder: Path) -> Path:
    """Get the path to the history file for a given folder."""
    return folder / HISTORY_FILENAME


def load_history(folder: Path) -> list[dict]:
    """
    Load the move history from the history file.

    Args:
        folder: The folder that was organized.

    Returns:
        A list of history entries, each with 'timestamp' and 'moves'.
    """
    history_path = _get_history_path(folder)

    if not history_path.exists():
        return []

    try:
        with open(history_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(
    folder: Path, moves: list[tuple[str, str]], timestamp: str
) -> None:
    """
    Append a new operation to the move history.

    Args:
        folder: The folder that was organized.
        moves: List of (source, destination) path tuples.
        timestamp: ISO format timestamp of the operation.
    """
    history = load_history(folder)

    entry = {
        "timestamp": timestamp,
        "moves": [{"from": src, "to": dst} for src, dst in moves],
    }
    history.append(entry)

    history_path = _get_history_path(folder)
    try:
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"[!] Warning: Could not save history: {e}")


def undo_last(folder_path: str) -> dict:
    """
    Undo the most recent organize operation by moving files back.

    Args:
        folder_path: Path to the folder that was organized.

    Returns:
        A summary dict with keys:
            - 'restored': Number of files restored
            - 'failed': Number of files that couldn't be restored
            - 'timestamp': Timestamp of the undone operation
            - 'details': List of (destination, source) tuples restored
            - 'errors': List of error messages
    """
    folder = Path(folder_path).resolve()
    history = load_history(folder)

    if not history:
        return {
            "restored": 0,
            "failed": 0,
            "timestamp": None,
            "details": [],
            "errors": ["No history found. Nothing to undo."],
        }

    # The last entry in the list is the most recent operation
    last_entry = history.pop()

    summary = {
        "restored": 0,
        "failed": 0,
        "timestamp": last_entry["timestamp"],
        "details": [],
        "errors": [],
    }

    for move in last_entry["moves"]:
        # Flip direction: "to" is where it lives now, "from" is where it should go back
        src = Path(move["to"])   # Current location (where it was moved TO)
        dst = Path(move["from"])  # Original location (where it came FROM)

        if not src.exists():
            summary["errors"].append(
                f"File not found at {src} — may have been moved or deleted."
            )
            summary["failed"] += 1
            continue

        try:
            # Ensure original parent directory exists
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            summary["details"].append((str(src), str(dst)))
            summary["restored"] += 1
        except (OSError, shutil.Error) as e:
            summary["errors"].append(f"Failed to restore {src.name}: {e}")
            summary["failed"] += 1

    # Remove any category folders that are now empty after restoring files
    _cleanup_empty_dirs(folder)

    # Save updated history (without the undone entry)
    history_path = _get_history_path(folder)
    try:
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except IOError:
        pass

    return summary


def _cleanup_empty_dirs(folder: Path) -> None:
    """Remove empty subdirectories after an undo operation."""
    for item in folder.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            try:
                item.rmdir()
            except OSError:
                pass
