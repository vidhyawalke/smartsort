"""
SmartSort — Automated File Organizer
====================================

A Python CLI tool that watches a folder and automatically organizes
files into categorized subfolders by type.

Features:
    - Auto-sort files by extension into categorized folders
    - Real-time folder watching with watchdog
    - Undo support to reverse the last operation
    - Dry-run mode to preview changes
    - Custom rules via config.json

Usage:
    python -m smartsort <folder_path>
    python -m smartsort <folder_path> --watch
    python -m smartsort --undo
"""

__version__ = "1.0.0"
__author__ = "VIDHYA"
