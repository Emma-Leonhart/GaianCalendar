"""GaianDate — the core date type for the Gaian Calendar."""
from __future__ import annotations
import functools
import re
from datetime import date, timedelta
from ._convert import (
    gregorian_to_gaian,
    gaian_to_gregorian,
    is_leap_year,
    validate_date,
    day_of_year,
    day_of_week,
)
from ._data import get_month, get_weekday
from ._format import format_date
from .month import GaianMonth
from .weekday import GaianWeekday


@functools.total_ordering
class GaianDate:
    """
    An immutable Gaian Calendar date.

    Gaian year = ISO week-year + 10,000.
    13 months of 28 days; month 14 (Horus) has 7 days in leap years only.
    """

    __slots__ = ("_year", "_month", "_day")

    def __init__(self, year: int, month: int, day: int) -> None:
        validate_date(year, month, day)
        self._year = year
        self._month = month
        self._day = day

    # ------------------------------------------------------------------
    # Alternate constructors
    # ------------------------------------------------------------------

    @classmethod
    def today(cls) -> GaianDate:
        """Return the current Gaian date in local time."""
        return cls.from_gregorian(date.today())

    @classmethod
    def from_gregorian(cls, d: date) -> GaianDate:
        """Convert a Gregorian datetime.date to a GaianDate."""
        year, month, day = gregorian_to_gaian(d)
        return cls(year, month, day)

    @classmethod
    def from_day_of_year(cls, year: int, doy: int) -> GaianDate:
        """Construct from a Gaian year and day-of-year (1–364 or 1–371 in leap years)."""
        leap = is_leap_year(year)
        max_doy = 371 if leap else 364
        if not 1 <= doy <= max_doy:
            raise ValueError(f"Day of year {doy} out of range (1–{max_doy}) for year {year}")
        if doy <= 364:
            month = (doy - 1) // 28 + 1
            day = (doy - 1) % 28 + 1
        else:
            month = 14
            day = doy - 364
        return cls(year, month, day)

    @classmethod
    def parse(cls, s: str) -> GaianDate:
        """
        Parse a Gaian date string. Supported formats:
          - "Aquarius 15, 12026"
          - "Aquarius 15, 12026 GE"
          - "Aqu 15, 12026"
          - "3/15/12026"
          - "12026-03-15"
        """
        s = s.strip().rstrip(" GE").strip().rstrip(",").strip()

        # ISO-like numeric: 12026-03-15
        m = re.fullmatch(r"(\d{5})-(\d{1,2})-(\d{1,2})", s)
        if m:
            return cls(int(m.group(1)), int(m.group(2)), int(m.group(3)))

        # Slash numeric: 3/15/12026 or 03/15/12026
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{5})", s)
        if m:
            return cls(int(m.group(3)), int(m.group(1)), int(m.group(2)))

        # Named: "Aquarius 15, 12026" or "Aqu 15, 12026"
        m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2}),?\s*(\d{5})", s)
        if m:
            from ._data import get_month_by_name
            month_data = get_month_by_name(m.group(1))
            return cls(int(m.group(3)), month_data["number"], int(m.group(2)))

        raise ValueError(f"Cannot parse {s!r} as a GaianDate")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @property
    def day_of_week(self) -> int:
        """ISO weekday: 1 (Monday) … 7 (Sunday)."""
        return day_of_week(self._day)

    @property
    def day_of_year(self) -> int:
        """1–364, or up to 371 in leap years."""
        return day_of_year(self._month, self._day)

    @property
    def is_leap_year(self) -> bool:
        """True if this year has a Horus month."""
        return is_leap_year(self._year)

    @property
    def month_name(self) -> str:
        return get_month(self._month)["name"]

    @property
    def month_symbol(self) -> str:
        return get_month(self._month)["symbol"]

    @property
    def month_abbrev(self) -> str:
        return get_month(self._month)["abbrev"]

    @property
    def weekday_name(self) -> str:
        return get_weekday(self.day_of_week)["name"]

    @property
    def weekday_symbol(self) -> str:
        return get_weekday(self.day_of_week)["symbol"]

    @property
    def weekday_abbrev(self) -> str:
        return get_weekday(self.day_of_week)["abbrev"]

    @property
    def gaian_month(self) -> GaianMonth:
        return GaianMonth(self._month)

    @property
    def gaian_weekday(self) -> GaianWeekday:
        return GaianWeekday(self.day_of_week)

    # ------------------------------------------------------------------
    # Conversion
    # ------------------------------------------------------------------

    def to_gregorian(self) -> date:
        """Convert to a Gregorian datetime.date."""
        return gaian_to_gregorian(self._year, self._month, self._day)

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def format(self, pattern: str) -> str:
        """Format using a pattern string. See planning/03_api_design.md for tokens."""
        return format_date(self._year, self._month, self._day, pattern)

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def __add__(self, other: object) -> GaianDate:
        if isinstance(other, timedelta):
            greg = self.to_gregorian() + other
            return GaianDate.from_gregorian(greg)
        return NotImplemented

    def __radd__(self, other: object) -> GaianDate:
        return self.__add__(other)

    def __sub__(self, other: object) -> GaianDate | timedelta:
        if isinstance(other, timedelta):
            greg = self.to_gregorian() - other
            return GaianDate.from_gregorian(greg)
        if isinstance(other, GaianDate):
            return self.to_gregorian() - other.to_gregorian()
        return NotImplemented

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GaianDate):
            return (self._year, self._month, self._day) == (other._year, other._month, other._day)
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, GaianDate):
            return (self._year, self._month, self._day) < (other._year, other._month, other._day)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self._year, self._month, self._day))

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"GaianDate({self._year}, {self._month}, {self._day})"

    def __str__(self) -> str:
        return self.format("MMMM d, yyyy GE")
