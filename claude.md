# gaian-calendar

## What This Is

A pure-Python PyPI library for the **Gaian Calendar** — a perpetual 13-month solar calendar.

- PyPI name: `gaian-calendar`
- Import name: `gaian_calendar`
- Display name: **GaianCalendar**
- Reference implementations: `C:\Users\Immanuelle\Documents\Github\order.life\build.py` and `C:\Users\Immanuelle\AndroidStudioProjects\DateTimeNodaTimeExperiments\GaianNodaTimeWrappers\`
- Packaging model: mirrors `C:\Users\Immanuelle\Documents\Github\cleanvibe` exactly

## Workflow Guidelines

- **Commit early and often.** Every meaningful change should be committed.
- **Keep this CLAUDE.md up to date** with architectural decisions and conventions.
- **Do not enter planning mode** — edit files and commit instead.
- See `planning/` for design documents (written before implementation).

## Architecture

- **Flat package layout**: `gaian_calendar/` at repo root
- **Zero runtime dependencies** (stdlib only: `datetime`, `functools`, `re`)
- **Python 3.9+ minimum**
- **pyproject.toml only** (no setup.py)

### Key Files (once implemented)

| File | Purpose |
|------|---------|
| `gaian_calendar/__init__.py` | Public re-exports + `__version__` |
| `gaian_calendar/_data.py` | Month/weekday constants (names, symbols, elements) |
| `gaian_calendar/_convert.py` | Core calendar math (gregorian↔gaian, leap year) |
| `gaian_calendar/_format.py` | Pattern-based formatting engine |
| `gaian_calendar/date.py` | `GaianDate` class |
| `gaian_calendar/month.py` | `GaianMonth` class |
| `gaian_calendar/weekday.py` | `GaianWeekday` class |
| `tests/` | pytest test suite |

### Calendar Math (Core Algorithm)

```python
# Gregorian → Gaian
iso_year, iso_week, iso_weekday = d.isocalendar()
month = (iso_week - 1) // 4 + 1
day   = ((iso_week - 1) % 4) * 7 + iso_weekday
gaian_year = iso_year + 10_000

# Gaian → Gregorian
iso_week = (month - 1) * 4 + (day - 1) // 7 + 1
iso_weekday = (day - 1) % 7 + 1
date.fromisocalendar(gaian_year - 10_000, iso_week, iso_weekday)
```

## Planning Documents

All design decisions are documented in `planning/`:
1. `01_overview.md` — what we're building and why
2. `02_calendar_rules.md` — the math and all conversion formulas
3. `03_api_design.md` — full public API specification
4. `04_module_structure.md` — file layout and module responsibilities
5. `05_packaging.md` — pyproject.toml, CI/CD, PyPI publishing
6. `06_test_cases.md` — ground-truth test cases for validation

## Publishing

- GitHub Actions publishes to PyPI on GitHub release
- OIDC trusted publishing (no secrets needed)
- Follows cleanvibe's `.github/workflows/publish.yml` exactly
