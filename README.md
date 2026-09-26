# SmartSort — Automated File Organizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

Run with `python -m smartsort /path/to/folder` from your terminal.

## What the project does

SmartSort is a Python CLI tool that automatically organizes messy folders by sorting files into categorized subfolders based on their file type.

Auto-sort by type — Images, Documents, Videos, Audio, Archives, and more are moved into named subfolders automatically

Custom rules — Define your own sorting categories and extensions via `config.json`

Watch mode — Monitors a folder in real time and sorts new files as they appear

Dry run — Preview what would be moved without changing anything on disk

Undo — Reverse the last sort operation; every move is logged and tracked

Duplicate handling — Files are renamed automatically to avoid overwriting existing ones

Ignore patterns — System files like `.DS_Store`, `Thumbs.db`, and `desktop.ini` are skipped by default

## Project Structure

```
smartsort/
├── smartsort/
│   ├── __init__.py       # Package metadata
│   ├── __main__.py       # Module entry point
│   ├── cli.py            # CLI interface (argparse + rich)
│   ├── config.py         # Config loading and default rules
│   ├── organizer.py      # Core file organization logic
│   ├── undo.py           # Undo and history tracking
│   └── watcher.py        # Real-time folder monitoring
├── config.json           # Default sorting rules
├── requirements.txt      # Dependencies
├── setup.py              # Package setup
└── README.md
```

## How users can get started with the project

Clone the repository and install dependencies:

```bash
git clone https://github.com/vidhyawalke/smartsort.git
cd smartsort
pip install -r requirements.txt
```

Organize a folder:

```bash
python -m smartsort /path/to/folder
```

Other available options:

```bash
python -m smartsort /path/to/folder --dry-run
python -m smartsort /path/to/folder --watch
python -m smartsort /path/to/folder --undo
python -m smartsort /path/to/folder --config my_rules.json
python -m smartsort --help
```

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Language   | Python 3.10+                      |
| Monitoring | watchdog                          |
| CLI Output | rich                              |
| Config     | JSON                              |

## Getting Help

If you run into issues or have questions, open a [GitHub Issue](https://github.com/vidhyawalke/smartsort/issues) in this repository.

## Maintainer

Built and maintained by [Vidhya Walke](https://github.com/vidhyawalke).

Contributions, bug reports, and suggestions are welcome via pull request or issue.
