# Test index

Tests are grouped into subfolders by subsystem under `tests/`. Pytest discovers them recursively (`testpaths = ["tests"]` in `pyproject.toml`). No test code was changed; only file locations and path references were updated.

Total test files: **178**

Run the whole suite:

```bash
python -m pytest -q
```

Run one group:

```bash
python -m pytest -q tests/phase13 tests/phase2ia tests/t2t
```
