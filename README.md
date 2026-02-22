# GaianCalendar

A pure-Python library for the **Gaian Calendar** — a perpetual 13-month solar calendar based on ISO week-year arithmetic.

```python
from gaian_calendar import GaianDate

today = GaianDate.today()
print(today)                    # e.g. "Aquarius 22, 12026 GE"
print(today.day_of_year)        # e.g. 78
print(today.is_leap_year)       # True
print(today.format("WWWW, MMMM d, yyyy GE"))  # "Sunday, Aquarius 22, 12026 GE"
```

---

## Status

**Pre-release — planning phase.** See [`planning/`](planning/) for design documents.

---

## What is the Gaian Calendar?

The Gaian Calendar is a perpetual reform calendar with these properties:

- **13 regular months** of exactly 28 days (4 weeks × 7 days), named after zodiac constellations
- **1 intercalary month** (Horus, 7 days) in leap years only — years with ISO week 53
- **Perpetual**: every calendar date always falls on the same weekday, every year
- **Year numbering**: Gaian year = ISO week-year + 10,000 (so 2026 CE = 12026 GE)
- **Zero weekday drift**: recurring events stay on the same day of week indefinitely

The 13 months in order: Sagittarius · Capricorn · Aquarius · Pisces · Aries · Taurus · Gemini · Cancer · Leo · Virgo · Libra · Scorpius · Ophiuchus · (Horus in leap years)

---

## Installation

```bash
pip install gaian-calendar
```

*(Not yet published — coming soon)*

---

## Usage

```python
from datetime import date, timedelta
from gaian_calendar import GaianDate, GaianMonth, is_leap_year

# Today
d = GaianDate.today()

# From Gregorian
d = GaianDate.from_gregorian(date(2026, 2, 22))
print(d)                  # "Aquarius 22, 12026 GE"
print(d.to_gregorian())   # 2026-02-22

# Properties
print(d.year)             # 12026
print(d.month)            # 3
print(d.day)              # 22
print(d.month_name)       # "Aquarius"
print(d.month_symbol)     # "♒"
print(d.weekday_name)     # "Sunday"
print(d.weekday_symbol)   # "☉"
print(d.day_of_year)      # 78
print(d.is_leap_year)     # True

# Arithmetic
next_week = d + timedelta(weeks=1)
yesterday = d - timedelta(days=1)
delta = d - GaianDate(12026, 1, 1)   # timedelta

# Parsing
d = GaianDate.parse("Aquarius 22, 12026")
d = GaianDate.parse("12026-03-22")
d = GaianDate.parse("3/22/12026")

# Formatting
d.format("MMMM d, yyyy GE")          # "Aquarius 22, 12026 GE"
d.format("MMM* DDD")                 # "♒ 078"
d.format("yyyy-MM-dd")               # "12026-03-22"
d.format("ddd")                      # "22nd"

# Leap year check
is_leap_year(12026)    # True
is_leap_year(12025)    # False

# Month info
from gaian_calendar import GaianMonth
m = GaianMonth.AQUARIUS
print(m.symbol)    # "♒"
print(m.element)   # "Air"
```

---

## Similar Libraries

This library is modeled after:
- [`hijridate`](https://pypi.org/project/hijridate/) — Islamic Hijri calendar
- [`pyluach`](https://pypi.org/project/pyluach/) — Hebrew calendar

---

## License

MIT
