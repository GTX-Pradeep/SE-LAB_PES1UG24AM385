# Lab 7: Fuzz Testing (Hypothesis) - Ride Share Fare

**SRN:** PES1UG24AM385

| File | What it is |
|------|------------|
| `ride_share_fare.py` | Fixed application (hardened input validation) |
| `ride_share_fare_original_buggy.py` | Original buggy code, kept for reference |
| `test_ride_share_fare.py` | Hypothesis fuzz tests for all three functions |
| `Lab7_FuzzTesting_PES1UG24AM385.pdf` | Report with screenshots for every step |
| `screenshots/` | Individual screenshots |

## Run
```
pip install hypothesis pytest
python ride_share_fare.py
python -m pytest test_ride_share_fare.py -v
```

## Bugs found by fuzzing
- `None` input crashed all three functions (`AttributeError`)
- Empty input / missing `:` or `|` separator: `ValueError` on unpacking
- Empty number (`':'`, `''` in CSV): `ValueError` on conversion
- Empty cab name, negative distance and negative fares were accepted
- Also hardened: `nan`, `inf`, `1e400`, negative promo, extra separators, float overflow

## Fix
Each function checks that the input is a string and has the right number of parts, converts numbers through a helper that rejects empty, non-numeric, non-finite and negative values, and returns `None` for invalid input. `main()` prints a friendly message instead of crashing.

Result: 3 failed before the fix, 3 passed after it.
