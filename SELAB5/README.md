# Lab 5: Static Code Analysis — School Bus Transport Register

**Assigned repo:** `SETAPESU26/L5_24_school_transport`
**File analysed:** `school_transport.py`
**Tools:** Pylint, Bandit, Flake8

## Objective
Use static analysis tools to find and fix quality, security and style problems in a Python
program without changing what the program does.

## About the program
A register for school bus routes. It enrols riders on routes, exports route rosters to a file,
sends dispatch alerts and totals the fees collected per route (SQLite in-memory database).

## Setup
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install pylint bandit flake8
```

## How to run
```bash
python school_transport.py
```
Expected output:
```
dispatching bus R1
['Zoya']
```
It also creates `route_r1.txt` containing the riders on route R1.

## Running the analysis
```bash
pylint school_transport.py > pylint_report.txt
bandit -r school_transport.py > bandit_report.txt
flake8 school_transport.py > flake8_report.txt
```

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.00 / 10 | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **No issues identified** |
| Flake8 | 9 violations | **0** |

## Key fixes
1. **Shell injection (Bandit B602, High):** removed `subprocess.run(..., shell=True)`; the alert is printed instead.
2. **SQL injection (Bandit B608, Medium):** the INSERT now uses a parameterised query with `?` placeholders.
3. **Assert used for logic (Bandit B101):** replaced with `if ...: raise ValueError(...)`.
4. **Bare `except:` (Pylint W0702 / Flake8 E722):** now catches only `sqlite3.Error`.
5. **Unsafe file handling (Pylint R1732, W1514):** uses `with open(..., encoding="utf-8")`.
6. **Style:** snake_case names, docstrings, unused `driver` parameter removed, `if __name__ == "__main__":` guard, PEP 8 line length and spacing.

The full list is in [`issues.md`](issues.md).

## Commits
1. Fix Bandit security issues
2. Fix Pylint issues (score 10/10)
3. Fix Flake8 formatting issues

## Folder structure
```
LAB5/
├── README.md
├── school_transport.py            # final, fixed code
├── school_transport_original.py   # original code from the assigned repo
├── issues.md                      # issue table
├── reflection.md                  # answers to reflection questions
├── reports_before/                # pylint / bandit / flake8 reports on original code
├── reports_after/                 # reports on fixed code
└── stages/                        # code after each fix stage (one per commit)
```
