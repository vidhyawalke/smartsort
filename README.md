# 🗂️ SmartSort — Automated File Organizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

**SmartSort** is a Python CLI tool that automatically organizes messy folders by sorting files into categorized subfolders based on their file type. It supports real-time folder watching, undo operations, dry-run previews, and fully customizable sorting rules.

> *Because life's too short for a messy Downloads folder.* 🧹

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📦 **Auto-sort by type** | Images → `Images/`, Documents → `Documents/`, Videos → `Videos/`, etc. |
| ⚙️ **Custom rules** | Define your own sorting rules via `config.json` |
| 👁️ **Watch mode** | Monitors a folder in real-time and sorts new files instantly |
| 🔍 **Dry run** | Preview what would happen without moving anything |
| ↩️ **Undo** | Reverse the last operation — every move is tracked |
| 🎨 **Beautiful CLI** | Colorful output with tables, panels, and progress feedback |
| 🔄 **Duplicate handling** | Automatically renames files to avoid overwriting |
| 🚫 **Ignore patterns** | Skip system files like `.DS_Store`, `Thumbs.db`, etc. |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smartsort.git
cd smartsort
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Organize a folder

```bash
# Organize your Downloads folder
python -m smartsort ~/Downloads

# Or on Windows
python -m smartsort C:\Users\YourName\Downloads
```

---

## 📖 Usage

### Organize a folder (one-shot)
```bash
python -m smartsort /path/to/folder
```

### Preview without moving (dry run)
```bash
python -m smartsort /path/to/folder --dry-run
```

### Watch mode (real-time sorting)
```bash
python -m smartsort /path/to/folder --watch
```

### Undo the last operation
```bash
python -m smartsort /path/to/folder --undo
```

### Use custom sorting rules
```bash
python -m smartsort /path/to/folder --config my_rules.json
```

### See all options
```bash
python -m smartsort --help
```

---

## ⚙️ Configuration

SmartSort uses a `config.json` file to define sorting rules. You can customize it to fit your workflow:

```json
{
    "categories": {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Audio": [".mp3", ".wav", ".flac", ".aac"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Code": [".py", ".js", ".html", ".css", ".java"],
        "My Custom Category": [".abc", ".xyz"]
    },
    "default_category": "Other",
    "ignore_patterns": [".DS_Store", "Thumbs.db", "desktop.ini"]
}
```

If no config file is provided, SmartSort uses sensible built-in defaults that cover 60+ file extensions across 10 categories.

---

## 🏗️ Project Structure

```
smartsort/
├── smartsort/
│   ├── __init__.py       # Package metadata
│   ├── __main__.py       # Module entry point
│   ├── cli.py            # CLI interface (argparse + rich)
│   ├── config.py         # Config loading & default rules
│   ├── organizer.py      # Core file organization logic
│   ├── undo.py           # Undo/history tracking
│   └── watcher.py        # Real-time folder monitoring
├── config.json           # Default sorting rules
├── requirements.txt      # Dependencies
├── setup.py              # Package setup
├── LICENSE               # MIT License
└── README.md             # You are here!
```

---

## 🛠️ Tech Stack

- **Python 3.10+** — Modern Python with type hints
- **[watchdog](https://pypi.org/project/watchdog/)** — Cross-platform file system monitoring
- **[rich](https://pypi.org/project/rich/)** — Beautiful terminal output with colors, tables & panels

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 💡 Ideas for Future Improvements

- [ ] Schedule automatic organization with cron/Task Scheduler
- [ ] Add file size-based sorting rules
- [ ] Support regex patterns for advanced matching
- [ ] Add a GUI with tkinter or PyQt
- [ ] Generate HTML reports with charts

---

<p align="center">
  Made with ❤️ and Python
</p>
