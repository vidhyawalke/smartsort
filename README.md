# SmartSort — Automated File Organizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

## What the project does

SmartSort is a Python CLI tool that automatically organizes messy folders by sorting files into categorized subfolders based on their file type. It supports real-time folder watching, undo operations, dry-run previews, and fully customizable sorting rules via a config file.

## Why the project is useful

Managing a cluttered Downloads or Desktop folder wastes time and makes it hard to find what you need. SmartSort takes care of that automatically. It handles duplicates, lets you preview changes before they happen, watches folders in real time, and can be fully customized to match your personal workflow, all from the command line with no manual effort.

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
# Preview without moving files
python -m smartsort /path/to/folder --dry-run

# Watch a folder in real time
python -m smartsort /path/to/folder --watch

# Undo the last operation
python -m smartsort /path/to/folder --undo

# Use a custom config file
python -m smartsort /path/to/folder --config my_rules.json

# See all options
python -m smartsort --help
```

## Where users can get help with your project

If you run into issues or have questions, open an issue on the [GitHub repository](https://github.com/vidhyawalke/smartsort/issues). You can also refer to the configuration section in this file for help customizing sorting rules.

## Who maintains and contributes to the project

SmartSort is maintained by [vidhyawalke](https://github.com/vidhyawalke). Contributions are welcome. Fork the repository, create a feature branch, commit your changes, and open a pull request.
