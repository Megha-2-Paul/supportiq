# Contributing

1. Create a focused feature branch.
2. Use Python 3.10+ and install development dependencies with pip install -e ".[dev]".
3. Add or update tests for behavior changes.
4. Run pytest and ruff check . before opening a pull request.
5. Never commit secrets, private customer data, downloaded datasets, local databases, or generated model artifacts.
6. Document data provenance, licensing, and evaluation methodology for new datasets or models.
7. Keep predictions and routing recommendations human-reviewable; do not add unreviewed high-impact automation.
