# Issues Found – school_transport.py

Line numbers refer to the **original** file (`school_transport_original.py`).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B602 | Security | **High** | 24 | `subprocess.run("echo ... " + route, shell=True)` — a route like `R1; rm -rf ~` would run arbitrary shell commands | Removed the shell call entirely; the alert is printed with `print()` (no shell needed just to echo text) |
| 2 | SQL injection | Bandit B608 | Security | **Medium** | 9 | INSERT built with an f-string from user data — a name like `O'Brien` breaks it and crafted input can change the query | Use a parameterised query with `?` placeholders and a tuple of values |
| 3 | Bare `except:` | Pylint W0702 / Flake8 E722 | Bug | Medium | 30–31 | Swallows every exception (even `KeyboardInterrupt`) and hides real bugs | Catch only `sqlite3.Error` |
| 4 | File not closed safely / no encoding | Pylint R1732, W1514 | Bug | Medium | 18–21 | `open()` without `with` leaks the file handle if `write` fails; encoding depends on the OS | `with open(path, "w", encoding="utf-8") as out:` |
| 5 | `assert` used for program logic | Bandit B101 | Security / Bug | Low | 38 | Asserts are removed when Python runs with `-O`, so the check silently disappears | Replaced with `if ... : raise ValueError(...)` |
| 6 | `subprocess` import | Bandit B404 | Security | Low | 1 | Importing subprocess flagged as risky | Import removed (no longer needed after fix 1) |
| 7 | Unused argument `driver` | Pylint W0613 | Code smell | Low | 13 | `routeRoster(route, driver)` never uses `driver` | Removed the parameter and updated callers |
| 8 | SUM returns `None` | Logic (found during review) | Bug | Low | 29 | `SUM(fee)` for a route with no riders returns `None`, not `0` | `return row[0] or 0` |
| 9 | Non snake_case function names | Pylint C0103 | Style | Low | 8, 13, 17, 23, 27 | `enrollRider`, `routeRoster`, ... violate PEP 8 naming | Renamed to `enroll_rider`, `route_roster`, `export_roster`, `dispatch_alert`, `fee_collected` |
| 10 | Missing docstrings | Pylint C0114, C0116 | Style | Low | 1, 8, 13, 17, 23, 27, 34 | No module or function docstrings | Added docstrings |
| 11 | Code runs on import | Review | Design | Low | 44 | `main()` runs whenever the module is imported | Wrapped in `if __name__ == "__main__":` |
| 12 | Lines too long | Flake8 E501 / Pylint C0301 | Style | Low | 5, 9, 14, 29 | Lines over 79 characters | Split the long lines |
| 13 | Missing whitespace after `,` | Flake8 E231 | Style | Low | 8 | `def enrollRider(student,route,stop,fee)` | Added spaces after commas |
| 14 | Expected 2 blank lines | Flake8 E302 | Style | Low | 23 | Only one blank line before a function | Added the second blank line |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.00 / 10 (18 messages) | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **No issues identified** |
| Flake8 | 9 violations | **0** |

Program output is unchanged (`dispatching bus R1`, `['Zoya']`, and `route_r1.txt` is written).
