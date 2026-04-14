# 🔍 Log File Analyzer

A command-line tool that parses raw server log files, extracts structured data using regular expressions, and exports clean reports as CSV and JSON.

Built as a Python learning project covering **file I/O**, **regex**, and **testing with pytest**.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/tested%20with-pytest-orange?logo=pytest)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Sample Output](#sample-output)
- [Running Tests](#running-tests)
- [Log Format](#log-format)
- [Skills Demonstrated](#skills-demonstrated)

---

## ✨ Features

- Parses raw `.log` files using regular expressions
- Extracts timestamp, log level, error code, and message from each line
- Skips malformed or corrupted lines gracefully
- Exports structured data to `.csv`
- Exports data and summary report to `.json`
- Prints a clean summary to the console
- Accepts input file path as a command-line argument

---

## 📁 Project Structure

```
log-file-analyzer/
│
├── main.py               # Main script
├── test_main.py          # Pytest test suite
│
├── data/
│   └── app.log           # Sample log file to test with
│
├── output/
│   ├── parsed_logs.csv   # Generated CSV output
│   └── report.json       # Generated JSON output + summary
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/log-file-analyzer.git
cd log-file-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Only `pytest` is required. All other modules (`re`, `csv`, `json`, `argparse`) are part of Python's standard library.

---

## 💻 Usage

Run the analyzer on the included sample log file:

```bash
python main.py --input data/app.log
```

Or point it at your own log file:

```bash
python main.py --input /path/to/your/file.log
```

Output files will be saved to the `/output` folder automatically.

---

## 📊 Sample Output

### Console summary

```
=============================
 Log File Analysis Summary
=============================
Total lines processed : 25
Successfully parsed   : 23
Malformed / skipped   : 2

INFO     : 9
WARNING  : 6
ERROR    : 8

Most common error code: 500 (3 occurrences)
=============================
Output saved to: output/parsed_logs.csv
Output saved to: output/report.json
```

### CSV output (parsed_logs.csv)

| timestamp           | level   | code | message                                          |
|---------------------|---------|------|--------------------------------------------------|
| 2024-03-15 08:01:12 | INFO    | 200  | Application started successfully                 |
| 2024-03-15 08:07:23 | WARNING | 301  | Redirect loop detected on /home endpoint         |
| 2024-03-15 08:12:09 | ERROR   | 500  | Internal server error in payment module          |

### JSON output (report.json)

```json
{
  "summary": {
    "total": 25,
    "parsed": 23,
    "skipped": 2,
    "errors": 8,
    "warnings": 6,
    "info": 9
  },
  "entries": [
    {
      "timestamp": "2024-03-15 08:01:12",
      "level": "INFO",
      "code": "200",
      "message": "Application started successfully"
    }
  ]
}
```

---

## 🧪 Running Tests

```bash
pytest test_main.py -v
```

The test suite covers:

- Valid lines return a correctly structured dictionary
- All four fields (timestamp, level, code, message) are extracted accurately
- Malformed and empty lines return `None` without crashing
- Messages containing colons are captured in full
- Edge cases: `None` input, whitespace-only strings, partial lines

---

## 📄 Log Format

The tool expects log lines in this format:

```
[YYYY-MM-DD HH:MM:SS] LEVEL (code=XXX): Message here
```

**Examples:**
```
[2024-03-15 08:01:12] INFO (code=200): Application started successfully
[2024-03-15 08:18:47] ERROR (code=503): Connection to database timed out after 30s
[2024-03-15 08:21:05] WARNING (code=404): Resource not found at /api/v1/users/9981
```

Lines that do not match this format are skipped and counted as malformed.

---

## 🛠 Skills Demonstrated

| Skill | Where used |
|---|---|
| Regular expressions (`re`) | Parsing each log line into fields |
| File I/O — CSV (`csv`) | Writing structured rows to a `.csv` file |
| File I/O — JSON (`json`) | Writing data and summary to a `.json` file |
| Error handling (`try/except`) | Gracefully skipping malformed lines |
| CLI arguments (`argparse`) | Accepting `--input` path from the terminal |
| Unit testing (`pytest`) | 16 tests covering valid, malformed, and edge cases |

---

## 📜 License

MIT — free to use, modify, and share.
