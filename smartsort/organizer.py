"""
Core file organizer module for SmartSort.

Contains the main logic for scanning a folder, categorizing files
by their extension, and moving them into organized subfolders.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime

from .config import load_config, build_extension_map
from .undo import save_history


def get_category(filename: str, ext_map: dict, default_category: str) -> str:
    """
    Determine which category a file belongs to based on its extension.

    Args:
        filename: The name of the file (e.g., 'photo.jpg').
        ext_map: A dict mapping extensions to category names.
        default_category: Category for unrecognized extensions.

    Returns:
        The category name (e.g., 'Images', 'Documents').
    """
    ext = Path(filename).suffix.lower()
    return ext_map.get(ext, default_category)


def generate_unique_path(dest: Path) -> Path:
    """
    Generate a unique file path if the destination already exists.
    Appends a number like 'file (1).txt', 'file (2).txt', etc.

    Args:
        dest: The desired destination path.

    Returns:
        A Path that does not conflict with existing files.
    """
    if not dest.exists():
        return dest

    stem = dest.stem
    suffix = dest.suffix
    parent = dest.parent
    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def should_ignore(filename: str, ignore_patterns: list[str]) -> bool:
    """
    Check if a file should be ignored during organization.

    Args:
        filename: The name of the file.
        ignore_patterns: List of filenames/patterns to ignore.

    Returns:
        True if the file should be skipped.
    """
    return filename in ignore_patterns


def organize_folder(
    folder_path: str,
    config_path: str | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Organize all files in a folder into categorized subfolders.

    Scans the target folder, determines a category for each file
    based on its extension, and moves it into the appropriate subfolder.

    Args:
        folder_path: Path to the folder to organize.
        config_path: Optional path to a custom config.json.
        dry_run: If True, only preview — don't actually move files.

    Returns:
        A summary dict with keys:
            - 'total_files': Total files processed
            - 'moved': Number of files moved
            - 'skipped': Number of files skipped
            - 'categories': Dict of {category: count}
            - 'moves': List of (source, destination) tuples
            - 'errors': List of error messages
    """
    folder = Path(folder_path).resolve()

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    # Load config and build extension map
    config = load_config(config_path)
    ext_map = build_extension_map(config)
    default_category = config.get("default_category", "Other")
    ignore_patterns = config.get("ignore_patterns", [])

    # Summary tracking
    summary = {
        "total_files": 0,
        "moved": 0,
        "skipped": 0,
        "categories": {},
        "moves": [],
        "errors": [],
        "timestamp": datetime.now().isoformat(),
        "folder": str(folder),
        "dry_run": dry_run,
    }

    # Scan only top-level files (not subdirectories)
    files = [f for f in folder.iterdir() if f.is_file()]
    summary["total_files"] = len(files)

    for file_path in files:
        filename = file_path.name

        # Skip ignored files
        if should_ignore(filename, ignore_patterns):
            summary["skipped"] += 1
            continue

        # Determine category
        category = get_category(filename, ext_map, default_category)

        # Build destination path
        category_dir = folder / category
        dest_path = generate_unique_path(category_dir / filename)

        if dry_run:
            # Just record what would happen
            summary["moves"].append((str(file_path), str(dest_path)))
            summary["categories"][category] = (
                summary["categories"].get(category, 0) + 1
            )
            summary["moved"] += 1
        else:
            try:
                # Create category directory if it doesn't exist
                category_dir.mkdir(exist_ok=True)

                # Move the file
                shutil.move(str(file_path), str(dest_path))

                summary["moves"].append((str(file_path), str(dest_path)))
                summary["categories"][category] = (
                    summary["categories"].get(category, 0) + 1
                )
                summary["moved"] += 1

            except (OSError, shutil.Error) as e:
                error_msg = f"Failed to move {filename}: {e}"
                summary["errors"].append(error_msg)
                summary["skipped"] += 1

    # Save move history for undo (unless dry run)
    if not dry_run and summary["moves"]:
        save_history(folder, summary["moves"], summary["timestamp"])

    return summary


def organize_single_file(
    file_path: str,
    target_folder: str,
    config_path: str | None = None,
    dry_run: bool = False,
) -> dict | None:
    """
    Organize a single file into the appropriate category subfolder.
    Used by the watcher for real-time organization.

    Args:
        file_path: Path to the file to organize.
        target_folder: The base folder where categories are created.
        config_path: Optional path to a custom config.json.
        dry_run: If True, only preview — don't actually move.

    Returns:
        A dict with 'source', 'destination', 'category' if moved,
        or None if skipped.
    """
    file = Path(file_path).resolve()
    folder = Path(target_folder).resolve()

    if not file.exists() or not file.is_file():
        return None

    config = load_config(config_path)
    ext_map = build_extension_map(config)
    default_category = config.get("default_category", "Other")
    ignore_patterns = config.get("ignore_patterns", [])

    if should_ignore(file.name, ignore_patterns):
        return None

    category = get_category(file.name, ext_map, default_category)
    category_dir = folder / category
    dest_path = generate_unique_path(category_dir / file.name)

    if dry_run:
        return {
            "source": str(file),
            "destination": str(dest_path),
            "category": category,
        }

    try:
        category_dir.mkdir(exist_ok=True)
        shutil.move(str(file), str(dest_path))

        # Save to history
        save_history(
            folder,
            [(str(file), str(dest_path))],
            datetime.now().isoformat(),
        )

        return {
            "source": str(file),
            "destination": str(dest_path),
            "category": category,
        }

    except (OSError, shutil.Error):
        return None
