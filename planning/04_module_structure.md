# GaianCalendar — Module Structure

## Directory Layout

```
gaian-calendar/               ← repo root (this repo)
├── gaian_calendar/           ← Python package (flat layout, matches import name)
│   ├── __init__.py           ← public re-exports + __version__
│   ├── _data.py              ← month/weekday constants (names, symbols, elements)
│   ├── _convert.py           ← core calendar math (gregorian↔gaian, leap year)
│   ├── _format.py            ← pattern-based formatting engine
│   ├── date.py               ← GaianDate class
│   ├── month.py              ← GaianMonth class
│   └── weekday.py            ← GaianWeekday class
├── tests/
│   ├── test_convert.py       ← unit tests for calendar math
│   ├── test_date.py          ← unit tests for GaianDate
│   ├── test_format.py        ← unit tests for formatting patterns
│   └── test_parse.py         ← unit tests for string parsing
├── planning/                 ← planning docs (this directory)
├── .github/
│   └── workflows/
│       └── publish.yml       ← PyPI publish on GitHub release
├── .gitignore
├── CLAUDE.md
├── LICENSE                   ← MIT
├── README.md
└── pyproject.toml
```

## Module Responsibilities

### `gaian_calendar/__init__.py`
- Sets `__version__ = "0.1.0"`
- Re-exports: `GaianDate`, `GaianMonth`, `GaianWeekday`, `is_leap_year`
- The only thing users need to import from

### `gaian_calendar/_data.py`
- Pure data, no logic
- `MONTHS`: list of 14 dicts with `name`, `abbrev`, `symbol`, `element`, `iso_weeks`
- `WEEKDAYS`: list of 7 dicts with `name`, `abbrev`, `symbol`, `planet`
- `ORDINALS`: dict mapping 1–28 to "1st", "2nd", ... "28th"
- `NUMBER_WORDS`: dict mapping 1–28 to "First", "Second", ... "Twenty-eighth"

### `gaian_calendar/_convert.py`
- `gregorian_to_gaian(d: date) -> tuple[int, int, int]` → (year, month, day)
- `gaian_to_gregorian(year: int, month: int, day: int) -> date`
- `is_leap_year(gaian_year: int) -> bool`
- `day_of_year(month: int, day: int) -> int`
- `day_of_week(day: int) -> int`
- `validate_date(year: int, month: int, day: int) -> None` (raises ValueError)

### `gaian_calendar/_format.py`
- `format_date(d: GaianDate, pattern: str) -> str`
- Tokenizes pattern string and substitutes tokens
- Handles literal "GE" suffix, all format tokens from api_design.md

### `gaian_calendar/date.py`
- `class GaianDate` — immutable date value
- Stores `_year`, `_month`, `_day` as private ints
- All properties computed lazily where appropriate
- `__add__`, `__sub__`, `__eq__`, `__lt__` etc.
- `functools.total_ordering` for comparison

### `gaian_calendar/month.py`
- `class GaianMonth` — thin wrapper around month number 1–14
- Class constants for all 14 months
- `from_name()` classmethod for parsing

### `gaian_calendar/weekday.py`
- `class GaianWeekday` — thin wrapper around weekday number 1–7
- Class constants for all 7 weekdays
- `is_sabbath` property (Fri/Sat/Sun)

## Zero Dependencies

All stdlib modules used:
- `datetime` (for `date`, `timedelta`, `date.fromisocalendar()`, `.isocalendar()`)
- `functools` (for `total_ordering`)
- `re` (for format pattern tokenizing)
- `typing` (for type hints, though we use native syntax where possible)

No third-party packages.

## Python Version Target

Python 3.9+ (same as cleanvibe).

Key 3.8+ feature we rely on: `date.fromisocalendar()` (added in 3.8).
Key 3.9+ features: built-in generics in type hints (`list[int]` vs `List[int]`).
