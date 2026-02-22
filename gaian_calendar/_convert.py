"""
Core Gaian Calendar arithmetic: conversions, validation, derived properties.
All functions work with plain ints and datetime.date — no class dependencies.
"""
from datetime import date


# ---------------------------------------------------------------------------
# Leap year
# ---------------------------------------------------------------------------

def _iso_weeks_in_year(iso_year: int) -> int:
    """Return 52 or 53: the number of ISO weeks in the given ISO week-year."""
    # Dec 28 is always in the last real ISO week of the year (never week 1 of next)
    return date(iso_year, 12, 28).isocalendar()[1]


def is_leap_year(gaian_year: int) -> bool:
    """Return True if the Gaian year has a Horus month (53 ISO weeks)."""
    return _iso_weeks_in_year(gaian_year - 10_000) == 53


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_date(year: int, month: int, day: int) -> None:
    """Raise ValueError if (year, month, day) is not a valid Gaian date."""
    if year < 10_001 or year > 19_999:
        raise ValueError(f"Year {year} out of supported range (10001–19999)")
    leap = is_leap_year(year)
    max_month = 14 if leap else 13
    if month < 1 or month > max_month:
        if month == 14 and not leap:
            raise ValueError(
                f"Month 14 (Horus) only exists in leap years; {year} is not a leap year"
            )
        raise ValueError(f"Month {month} out of range (1–{max_month}) for year {year}")
    max_day = 7 if month == 14 else 28
    if day < 1 or day > max_day:
        raise ValueError(
            f"Day {day} out of range for month {month} "
            f"({'Horus, max 7' if month == 14 else 'max 28'})"
        )


# ---------------------------------------------------------------------------
# Conversion: Gregorian ↔ Gaian
# ---------------------------------------------------------------------------

def gregorian_to_gaian(d: date) -> tuple[int, int, int]:
    """Convert a Gregorian date to a (gaian_year, month, day) tuple."""
    iso_year, iso_week, iso_weekday = d.isocalendar()
    month = (iso_week - 1) // 4 + 1          # 1–14
    week_in_month = (iso_week - 1) % 4        # 0–3
    day = week_in_month * 7 + iso_weekday     # 1–28 (or 1–7 for Horus)
    gaian_year = iso_year + 10_000
    return gaian_year, month, day


def gaian_to_gregorian(year: int, month: int, day: int) -> date:
    """Convert a Gaian date to a Gregorian datetime.date."""
    iso_year = year - 10_000
    iso_week = (month - 1) * 4 + (day - 1) // 7 + 1   # 1–53
    iso_weekday = (day - 1) % 7 + 1                    # 1–7
    return date.fromisocalendar(iso_year, iso_week, iso_weekday)


# ---------------------------------------------------------------------------
# Derived properties
# ---------------------------------------------------------------------------

def day_of_year(month: int, day: int) -> int:
    """Return the day-of-year (1–364, or up to 371 for Horus days)."""
    if month <= 13:
        return (month - 1) * 28 + day
    else:  # Horus (month 14)
        return 364 + day


def day_of_week(day: int) -> int:
    """Return ISO weekday (1=Monday … 7=Sunday). Same for all years — perpetual."""
    return (day - 1) % 7 + 1
