"""GaianMonth — a month in the Gaian Calendar."""
from __future__ import annotations
import functools
from ._data import get_month, get_month_by_name, MONTHS


@functools.total_ordering
class GaianMonth:
    """Represents one of the 13 or 14 Gaian months."""

    __slots__ = ("_number",)

    def __init__(self, number: int) -> None:
        if not 1 <= number <= 14:
            raise ValueError(f"Month number must be 1–14, got {number}")
        self._number = number

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return get_month(self._number)["name"]

    @property
    def abbrev(self) -> str:
        return get_month(self._number)["abbrev"]

    @property
    def symbol(self) -> str:
        return get_month(self._number)["symbol"]

    @property
    def element(self) -> str | None:
        """Elemental association. None for Horus (month 14)."""
        return get_month(self._number)["element"]

    @property
    def is_intercalary(self) -> bool:
        """True only for Horus (month 14)."""
        return self._number == 14

    # ------------------------------------------------------------------
    # Alternate constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_name(cls, name: str) -> GaianMonth:
        """Parse a month by full name or abbreviation (case-insensitive)."""
        data = get_month_by_name(name)
        return cls(data["number"])

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"GaianMonth({self._number})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GaianMonth):
            return self._number == other._number
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, GaianMonth):
            return self._number < other._number
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._number)

    # ------------------------------------------------------------------
    # Class constants (set after class definition)
    # ------------------------------------------------------------------

    SAGITTARIUS = None
    CAPRICORN   = None
    AQUARIUS    = None
    PISCES      = None
    ARIES       = None
    TAURUS      = None
    GEMINI      = None
    CANCER      = None
    LEO         = None
    VIRGO       = None
    LIBRA       = None
    SCORPIUS    = None
    OPHIUCHUS   = None
    HORUS       = None


GaianMonth.SAGITTARIUS = GaianMonth(1)
GaianMonth.CAPRICORN   = GaianMonth(2)
GaianMonth.AQUARIUS    = GaianMonth(3)
GaianMonth.PISCES      = GaianMonth(4)
GaianMonth.ARIES       = GaianMonth(5)
GaianMonth.TAURUS      = GaianMonth(6)
GaianMonth.GEMINI      = GaianMonth(7)
GaianMonth.CANCER      = GaianMonth(8)
GaianMonth.LEO         = GaianMonth(9)
GaianMonth.VIRGO       = GaianMonth(10)
GaianMonth.LIBRA       = GaianMonth(11)
GaianMonth.SCORPIUS    = GaianMonth(12)
GaianMonth.OPHIUCHUS   = GaianMonth(13)
GaianMonth.HORUS       = GaianMonth(14)
