# GaianCalendar – Project Overview

## What We're Building

A pure-Python library published to PyPI under the name **`gaian-calendar`**, importable as `gaian_calendar`, that provides date types and conversion utilities for the **Gaian Calendar** — a perpetual 13-month solar calendar based on ISO week-year arithmetic.

Modeled after:
- [`hijridate`](https://pypi.org/project/hijridate/) — Islamic (Hijri) calendar conversions
- [`pyluach`](https://pypi.org/project/pyluach/) — Hebrew calendar library

Both of those libraries offer:
- A date type that mirrors `datetime.date` ergonomics
- Conversion to/from Gregorian
- Formatting and parsing
- Arithmetic (add days, compare dates, etc.)

This library does the same for the Gaian Calendar.

## Name

| Context | Value |
|---------|-------|
| PyPI package name | `gaian-calendar` |
| Python import name | `gaian_calendar` |
| Display / brand name | **GaianCalendar** |
| Version at first publish | `0.1.0` |

## Scope for v0.1

- `GaianDate` — core date type (year, month, day)
- Conversion: `GaianDate.today()`, `GaianDate.from_gregorian(date)`, `.to_gregorian()`
- Properties: `.year`, `.month`, `.day`, `.day_of_year`, `.day_of_week`, `.month_name`, `.is_leap_year`
- Arithmetic: `+`/`-` with `timedelta`, comparison operators
- Formatting: `str()` default, `.format(pattern)` custom
- Parsing: `GaianDate.parse(string)` for multiple formats
- Month and weekday name constants with symbols

## What's Out of Scope for v0.1

- `GaianDateTime` (date + time) — v0.2
- Timezone-aware `GaianZonedDateTime` — v0.2
- Julian Day Number conversions — v0.2
- Localization / non-English month names — future
- CLI interface — not planned (this is a library, not a tool)

## Reference Implementations

| Language | Location |
|----------|----------|
| Python (site generator) | `C:\Users\Immanuelle\Documents\Github\order.life\build.py` |
| C# / NodaTime | `C:\Users\Immanuelle\AndroidStudioProjects\DateTimeNodaTimeExperiments\GaianNodaTimeWrappers\` |

## Packaging Model

Follow `cleanvibe` exactly:
- `pyproject.toml` only (no `setup.py`)
- Flat layout (`gaian_calendar/` inside repo root)
- Zero runtime dependencies (stdlib only)
- Python 3.9+ minimum
- GitHub Actions for PyPI publish on release
- MIT license
