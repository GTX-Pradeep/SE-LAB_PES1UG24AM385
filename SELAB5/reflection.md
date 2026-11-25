# Reflection – Lab 5: Static Code Analysis

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
The easiest were the Flake8 style issues (missing spaces after commas, blank lines, long lines) and the Pylint docstring/naming warnings — they are mechanical and the tool tells you exactly what to change. The hardest were the security issues from Bandit. The `shell=True` call needed me to think about *why* a shell was used at all and replace it with a safe alternative, and the SQL injection needed the query rewritten with placeholders. Renaming functions to snake_case also needed care because every caller had to be updated.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
B404 (importing `subprocess`) is close to a false positive: importing the module is not dangerous by itself, only how it is used. B101 (`assert`) is also low risk in a demo `main()`, but it is still a valid point because asserts vanish under `python -O`. Pylint's line limit (100) and Flake8's (79) also differ, so the same line can be "fine" for one tool and an error for the other.

**3. How would you integrate static analysis tools into your software development workflow?**
Run Flake8 and Pylint automatically in the editor and as a **pre-commit hook**, so bad code is caught before it is committed. In **CI (e.g. GitHub Actions)**, run Pylint, Flake8 and Bandit on every push/pull request and fail the build if Bandit finds Medium/High issues or the Pylint score drops below a threshold (e.g. 9.5). Shared config files (`.pylintrc`, `.flake8`) keep the whole team on the same rules.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**
- **Security:** the shell-injection (High) and SQL-injection (Medium) holes are gone; Bandit reports no issues.
- **Robustness:** the file is always closed (`with`), only database errors are caught, the fee check no longer disappears under `-O`, and an empty route returns `0` instead of `None`.
- **Readability:** PEP 8 names, docstrings and consistent formatting make the code easier to read; the unused `driver` parameter was removed.
- **Measurable:** Pylint went from 4.00/10 to 10.00/10 and Flake8 from 9 violations to 0, while the program output stayed the same.
