# GaianCalendar — Public API Design

This document specifies the exact public interface for v0.1.

## Import Structure

```python
# Primary import — everything users need at top level
from gaian_calendar import GaianDate, GaianMonth, GaianWeekday

# Or just
import gaian_calendar
gaian_calendar.GaianDate.today()
```

All public classes live in `gaian_calendar/__init__.py` (re-exported from submodules).

---

## `GaianDate`

The core type. Immutable. Comparable. Mirrors `datetime.date` ergonomics where appropriate.

### Construction

```python
# Direct construction (year, month, day)
d = GaianDate(12026, 3, 15)       # Aquarius 15, 12026 GE

# From today's Gregorian date
d = GaianDate.today()

# From a datetime.date
from datetime import date
d = GaianDate.from_gregorian(date(2026, 2, 22))

# Parsing from string
d = GaianDate.parse("Aquarius 15, 12026")
d = GaianDate.parse("3/15/12026")
d = GaianDate.parse("12026-03-15")

# From day of year
d = GaianDate.from_day_of_year(12026, 71)   # day 71 of 12026
```

### Properties

```python
d.year          # int: 12026
d.month         # int: 3
d.day           # int: 15
d.day_of_week   # int: 1–7 (1=Monday, 7=Sunday)
d.day_of_year   # int: 1–364 (1–371 in leap years)
d.is_leap_year  # bool: True if year has Horus month (53 ISO weeks)
d.month_name    # str: "Aquarius"
d.month_symbol  # str: "♒"
d.weekday_name  # str: "Monday"
d.weekday_symbol # str: "☽"
```

### Conversion

```python
d.to_gregorian()     # datetime.date: date(2026, 3, 9)
```

### Arithmetic

```python
from datetime import timedelta

d + timedelta(days=7)   # GaianDate one week later
d - timedelta(days=1)   # GaianDate one day earlier
d2 - d1                 # timedelta between two GaianDates
```

### Comparison

```python
d1 == d2   # bool
d1 < d2    # bool
d1 <= d2   # bool
# All 6 comparison operators work (via __eq__, __lt__ and functools.total_ordering)
```

### String representation

```python
str(d)    # "Aquarius 15, 12026 GE"   (default format)
repr(d)   # "GaianDate(12026, 3, 15)"
```

### Formatting

Pattern-based formatting (subset of the C# GaianDateFormat patterns):

```python
d.format("MMMM d, yyyy")     # "Aquarius 15, 12026"
d.format("MMM d, yy")        # "Aqu 15, 26"
d.format("MMM*")             # "♒"           (symbol only)
d.format("W WWW d")          # "☽ Mon 15"    (symbol + abbrev weekday + day)
d.format("WWWW, MMMM d, yyyy GE")  # "Monday, Aquarius 15, 12026 GE"
d.format("ddd")              # "15th"         (ordinal)
d.format("DDD")              # "071"          (day of year, zero-padded to 3)
d.format("yyyy-MM-dd")       # "12026-03-15"  (ISO-like numeric)
d.format("M/d/yyyy")         # "3/15/12026"
```

#### Format Token Reference

| Token | Meaning | Example |
|-------|---------|---------|
| `yyyy` | 5-digit Gaian year | `12026` |
| `yy` | Last 2 digits of ISO year | `26` |
| `MMMM` | Full month name | `Aquarius` |
| `MMM` | Abbreviated month name | `Aqu` |
| `MM` | Zero-padded month number | `03` |
| `M` | Month number | `3` |
| `MMM*` | Month symbol | `♒` |
| `dd` | Zero-padded day | `15` |
| `d` | Day number | `15` |
| `ddd` | Ordinal day | `15th` |
| `dddd` | Day as word | `Fifteenth` |
| `WWWW` | Full weekday name | `Monday` |
| `WWW` | Abbreviated weekday | `Mon` |
| `W` | Weekday symbol | `☽` |
| `DDD` | Day of year, zero-padded | `071` |
| `GE` | Literal "GE" suffix | `GE` |

---

## `GaianMonth`

A value type representing a Gaian month.

```python
from gaian_calendar import GaianMonth

m = GaianMonth(3)            # Month 3 (Aquarius)
m = GaianMonth.from_name("Aquarius")
m = GaianMonth.from_name("Aqu")    # Abbreviated

m.number     # int: 3
m.name       # str: "Aquarius"
m.symbol     # str: "♒"
m.element    # str: "Air"
m.abbrev     # str: "Aqu"

# All 14 months available as class constants:
GaianMonth.SAGITTARIUS   # GaianMonth(1)
GaianMonth.CAPRICORN     # GaianMonth(2)
GaianMonth.AQUARIUS      # GaianMonth(3)
# ... through ...
GaianMonth.OPHIUCHUS     # GaianMonth(13)
GaianMonth.HORUS         # GaianMonth(14) — intercalary

str(m)   # "Aquarius"
repr(m)  # "GaianMonth(3)"
```

---

## `GaianWeekday`

```python
from gaian_calendar import GaianWeekday

w = GaianWeekday(1)     # Monday

w.number   # int: 1
w.name     # str: "Monday"
w.symbol   # str: "☽"
w.planet   # str: "Moon"
w.abbrev   # str: "Mon"
w.is_sabbath  # bool: True for Friday(5), Saturday(6), Sunday(7)

# Constants:
GaianWeekday.MONDAY    # GaianWeekday(1)
GaianWeekday.TUESDAY   # GaianWeekday(2)
# ... etc.
```

---

## Module-level helpers

```python
from gaian_calendar import is_leap_year

is_leap_year(12026)   # True
is_leap_year(12025)   # False
```

---

## Error Handling

Invalid input raises `ValueError` with a descriptive message:

```python
GaianDate(12026, 14, 8)   # ValueError: day 8 out of range for Horus month (max 7)
GaianDate(12025, 14, 1)   # ValueError: month 14 (Horus) only exists in leap years
GaianDate(12026, 3, 29)   # ValueError: day 29 out of range for month 3 (max 28)
GaianDate.parse("bad input")  # ValueError: cannot parse 'bad input' as GaianDate
```

---

## Usage Examples (what the README will show)

```python
from gaian_calendar import GaianDate

# Today's Gaian date
today = GaianDate.today()
print(today)           # e.g. "Aquarius 22, 12026 GE"
print(today.day_of_year)  # e.g. 78

# Convert from Gregorian
from datetime import date
d = GaianDate.from_gregorian(date(2026, 2, 22))
print(d)               # "Aquarius 22, 12026 GE"
print(d.to_gregorian())   # 2026-02-22

# Date arithmetic
from datetime import timedelta
next_week = d + timedelta(weeks=1)
print(next_week)       # "Aquarius 29, 12026 GE"  ... wait, max is 28
                       # actually "Pisces 1, 12026 GE"

# Check leap year
print(d.is_leap_year)  # True (12026 has Horus month)

# Format
print(d.format("WWWW, MMMM d, yyyy GE"))  # "Sunday, Aquarius 22, 12026 GE"
print(d.format("MMM* DDD"))               # "♒ 078"
```
