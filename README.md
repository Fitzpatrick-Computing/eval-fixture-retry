# fixit

A tiny toolkit for reliable one-liners. The current release ships one
module: `fixit.retry`, a small retry helper for flaky callables.

## Layout

- `fixit/` — the package
- `tests/` — the test suite

## Running the tests

From the repository root:

```
python3 -m pytest -q
```

Python >= 3.9, no third-party runtime dependencies (pytest is only needed
to run the tests).
