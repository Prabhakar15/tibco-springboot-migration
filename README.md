# tibco_migration

A tiny example Python project with a simple `calc` module and unit tests.

Quick start (PowerShell on Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python -m pytest -q
```

Files:
- `tibco_migration/calc.py` — sample functions `add` and `divide`.
- `tests/test_calc.py` — pytest unit tests.

Next steps:
- Add type-checking (mypy) and CI.
- Add packaging metadata if you want to publish.
