"""
Configuration module for SmartSort.

Handles loading sorting rules from config.json and provides
sensible defaults when no config file is available.
"""

from __future__ import annotations

import json
from pathlib import Path


# Default rules mapping file extensions to category folder names.
# Used when no config.json is provided or as a fallback.
DEFAULT_RULES = {
    "categories": {
        "Images": [
            ".jpg", ".jpeg", ".png", ".gif", ".svg",
            ".webp", ".ico", ".bmp", ".tiff", ".heic",
        ],
        "Documents": [
            ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".ppt", ".pptx", ".txt", ".csv", ".rtf", ".odt",
        ],
        "Videos": [
            ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ],
        "Audio": [
            ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ],
        "Archives": [
            ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ],
        "Code": [
            ".py", ".js", ".ts", ".html", ".css", ".java",
            ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php",
            ".swift", ".kt",
        ],
        "Data": [
            ".json", ".xml", ".yaml", ".yml", ".sql",
            ".db", ".sqlite", ".toml", ".ini", ".cfg",
        ],
        "Executables": [
            ".exe", ".msi", ".bat", ".sh", ".cmd", ".app", ".dmg",
        ],
        "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
        "Design": [".psd", ".ai", ".sketch", ".fig", ".xd", ".blend"],
    },
    "default_category": "Other",
    "ignore_patterns": [
        ".smartsort_history.json",
        ".gitkeep",
        "desktop.ini",
        "Thumbs.db",
        ".DS_Store",
    ],
}


def load_config(config_path: str | None = None) -> dict:
    """
    Load sorting rules from a JSON config file.

    Args:
        config_path: Path to a custom config.json file.
                     If None, looks for config.json in the current directory.
                     Falls back to DEFAULT_RULES if no file is found.

    Returns:
        A dictionary with 'categories', 'default_category', and 'ignore_patterns'.
    """
    if config_path:
        path = Path(config_path)
    else:
        # Look for config.json next to the package
        path = Path(__file__).parent.parent / "config.json"

    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_config = json.load(f)

            # Merge with defaults — user config takes priority
            merged = DEFAULT_RULES.copy()
            merged.update(user_config)
            return merged

        except (json.JSONDecodeError, IOError) as e:
            print(f"[!] Warning: Could not load config from {path}: {e}")
            print("   Falling back to default rules.")
            return DEFAULT_RULES.copy()

    return DEFAULT_RULES.copy()


def build_extension_map(config: dict) -> dict[str, str]:
    """
    Build a flat mapping from file extension to category name.

    Args:
        config: The full config dictionary with a 'categories' key.

    Returns:
        A dict like {'.jpg': 'Images', '.pdf': 'Documents', ...}
    """
    ext_map = {}
    for category, extensions in config["categories"].items():
        for ext in extensions:
            ext_map[ext.lower()] = category
    return ext_map
