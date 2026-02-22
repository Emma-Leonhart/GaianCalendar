# GaianCalendar — Packaging & Publishing

## Pattern Source

Follows `cleanvibe` exactly. See `C:\Users\Immanuelle\Documents\Github\cleanvibe` for reference.

## pyproject.toml (planned)

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gaian-calendar"
version = "0.1.0"
description = "Python library for the Gaian Calendar — a perpetual 13-month solar calendar based on ISO week-year arithmetic."
readme = "README.md"
license = "MIT"
requires-python = ">=3.9"
authors = [
    { name = "Immanuelle" },
]
keywords = ["calendar", "gaian", "date", "alternative calendar", "perpetual calendar", "ISO week"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

[project.urls]
Homepage = "https://github.com/Immanuelle/gaian-calendar"
Issues = "https://github.com/Immanuelle/gaian-calendar/issues"
```

Note: No `[project.scripts]` — this is a library, not a CLI tool.
Note: No `requires` (dependencies) — zero runtime dependencies.

## GitHub Actions: Publish Workflow

`.github/workflows/publish.yml` — copy from cleanvibe, identical pattern:
- Trigger: GitHub release published
- OIDC trusted publishing (no secrets)
- `python -m build` → PyPI publish

## Building & Testing Locally

```bash
# Install build tools
pip install build

# Build distributions
python -m build
# Creates dist/gaian_calendar-0.1.0-py3-none-any.whl
# Creates dist/gaian-calendar-0.1.0.tar.gz

# Test install locally
pip install dist/gaian_calendar-0.1.0-py3-none-any.whl

# Run tests
python -m pytest tests/
```

## Version Strategy

- Start at `0.1.0`
- Patch bumps (`0.1.x`) for bug fixes
- Minor bumps (`0.x.0`) for new features (e.g., GaianDateTime in v0.2)
- `__version__` in `gaian_calendar/__init__.py` is the single source of truth

## PyPI Trusted Publishing Setup

Before first publish, configure on PyPI:
1. Create account / project on pypi.org
2. Add trusted publisher: GitHub repo `Immanuelle/gaian-calendar`, workflow `publish.yml`
3. Create a GitHub release to trigger publish

## Comparison: hijridate vs pyluach vs GaianCalendar

| Feature | hijridate | pyluach | GaianCalendar (planned) |
|---------|-----------|---------|------------------------|
| Dependencies | none | none | none |
| Date type | `HijriDate` | `HebrewDate` | `GaianDate` |
| Today | `.today()` | `.today()` | `.today()` |
| From Gregorian | `.fromisoformat()` | `.from_pydate()` | `.from_gregorian()` |
| To Gregorian | `.to_gregorian()` | `.to_pydate()` | `.to_gregorian()` |
| Arithmetic | `timedelta` | `timedelta` | `timedelta` |
| Formatting | `.datetuple()` | `.hebrew_month_name()` | `.format(pattern)` |
| Parsing | `.fromisoformat()` | — | `.parse(string)` |
