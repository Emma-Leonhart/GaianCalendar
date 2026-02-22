# Gaian Calendar — Mathematical Rules Reference

This document is the authoritative specification for all calendar arithmetic in the library.
All implementation must match these rules exactly.

## Epoch & Year Numbering

- Gaian year = ISO week-year + 10,000
- ISO week-year 2025 → Gaian year **12025 GE**
- ISO week-year 2026 → Gaian year **12026 GE**

## Month Structure

13 regular months of exactly 28 days each (4 ISO weeks × 7 days).
1 intercalary month (Horus) of 7 days, present only in leap years (ISO 53-week years).

| Month # | Name | Symbol | Element | ISO Weeks |
|---------|------|--------|---------|-----------|
| 1  | Sagittarius | ♐ | Fire    | 1–4   |
| 2  | Capricorn   | ♑ | Earth   | 5–8   |
| 3  | Aquarius    | ♒ | Air     | 9–12  |
| 4  | Pisces      | ♓ | Water   | 13–16 |
| 5  | Aries       | ♈ | Fire    | 17–20 |
| 6  | Taurus      | ♉ | Earth   | 21–24 |
| 7  | Gemini      | ♊ | Air     | 25–28 |
| 8  | Cancer      | ♋ | Water   | 29–32 |
| 9  | Leo         | ♌ | Fire    | 33–36 |
| 10 | Virgo       | ♍ | Earth   | 37–40 |
| 11 | Libra       | ♎ | Air     | 41–44 |
| 12 | Scorpius    | ♏ | Water   | 45–48 |
| 13 | Ophiuchus   | ⛎ | Healing | 49–52 |
| 14 | Horus       | 𓅃 | —      | 53    |

**Horus (month 14)** has days 1–7 only, and only exists in leap years.

## Weekdays

The Gaian Calendar is perpetual — every calendar date falls on the same weekday every year.

| # | Name      | Symbol | Planet  |
|---|-----------|--------|---------|
| 1 | Monday    | ☽      | Moon    |
| 2 | Tuesday   | ♂      | Mars    |
| 3 | Wednesday | ☿      | Mercury |
| 4 | Thursday  | ♃      | Jupiter |
| 5 | Friday    | ♀      | Venus   |
| 6 | Saturday  | ♄      | Saturn  |
| 7 | Sunday    | ☉      | Sun     |

**Sabbath days**: Friday, Saturday, Sunday

## Core Conversion Formulas

### Gregorian date → Gaian date

```python
from datetime import date

def gregorian_to_gaian(d: date) -> tuple[int, int, int]:
    """Returns (gaian_year, gaian_month, gaian_day)"""
    iso_year, iso_week, iso_weekday = d.isocalendar()
    month = (iso_week - 1) // 4 + 1            # 1–14
    week_in_month = (iso_week - 1) % 4         # 0–3
    day = week_in_month * 7 + iso_weekday      # 1–28 (or 1–7 for Horus)
    gaian_year = iso_year + 10_000
    return gaian_year, month, day
```

### Gaian date → Gregorian date

```python
from datetime import date

def gaian_to_gregorian(gaian_year: int, month: int, day: int) -> date:
    """Converts Gaian date to Gregorian."""
    iso_year = gaian_year - 10_000
    iso_week = (month - 1) * 4 + (day - 1) // 7 + 1   # 1–53
    iso_weekday = (day - 1) % 7 + 1                    # 1–7
    return date.fromisocalendar(iso_year, iso_week, iso_weekday)
```

`date.fromisocalendar` is stdlib, available Python 3.8+.

### Leap year detection

```python
def is_leap_year(gaian_year: int) -> bool:
    """True if the year has a Horus month (53 ISO weeks)."""
    iso_year = gaian_year - 10_000
    # Python's datetime doesn't expose this directly; use date arithmetic:
    # Dec 28 is always in the last ISO week. If Dec 31 is also week 53, it's a leap year.
    dec_28 = date(iso_year, 12, 28)
    return dec_28.isocalendar()[1] == 52 and date(iso_year, 12, 31).isocalendar()[1] == 53
    # Simpler: a year has 53 ISO weeks if Jan 1 is Thursday,
    # or if it's a leap year and Jan 1 is Wednesday or Thursday.
```

Actually the simplest approach:

```python
def _iso_weeks_in_year(iso_year: int) -> int:
    """Returns 52 or 53."""
    # Dec 28 is always in week 52 or 53 (never week 1 of next year)
    return date(iso_year, 12, 28).isocalendar()[1]

def is_leap_year(gaian_year: int) -> bool:
    return _iso_weeks_in_year(gaian_year - 10_000) == 53
```

### Day of year

```python
def day_of_year(gaian_month: int, gaian_day: int) -> int:
    """Returns 1–364 (or up to 371 in leap years)."""
    if gaian_month <= 13:
        return (gaian_month - 1) * 28 + gaian_day
    else:  # Horus (month 14)
        return 364 + gaian_day
```

### Day of week (perpetual property)

```python
def day_of_week(gaian_day: int) -> int:
    """Returns 1 (Mon) to 7 (Sun). Same for ALL years — perpetual calendar."""
    return (gaian_day - 1) % 7 + 1
```

## Validation Rules

| Field | Valid range |
|-------|-------------|
| Year  | 10_001 – 19_999 (practical limit; underlying `date` supports 1 CE – 9999 CE) |
| Month (non-leap) | 1 – 13 |
| Month (leap year) | 1 – 14 |
| Day (months 1–13) | 1 – 28 |
| Day (month 14, Horus) | 1 – 7 |

## Known Leap Years (near present)

ISO years with 53 weeks:
2004, 2009, 2015, 2020, 2026, 2032, 2037, 2043, 2048...

So **Gaian 12026 GE** is a leap year (has Horus month).

## Perpetual Calendar Property

Because the Gaian calendar is anchored to ISO weeks, and ISO week-year resets at the same weekday each year, **Sagittarius 1 is always Monday, Aquarius 15 is always Monday**, etc.

This is a deliberate design feature: recurring events never drift across weekdays.
