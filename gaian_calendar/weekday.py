"""GaianWeekday — a weekday in the Gaian Calendar."""
from __future__ import annotations
import functools
from ._data import get_weekday, WEEKDAYS


@functools.total_ordering
class GaianWeekday:
    """Represents one of the 7 Gaian weekdays (1=Monday … 7=Sunday)."""

    __slots__ = ("_number",)

    def __init__(self, number: int) -> None:
        if not 1 <= number <= 7:
            raise ValueError(f"Weekday number must be 1–7, got {number}")
        self._number = number

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return get_weekday(self._number)["name"]

    @property
    def abbrev(self) -> str:
        return get_weekday(self._number)["abbrev"]

    @property
    def symbol(self) -> str:
        return get_weekday(self._number)["symbol"]

    @property
    def planet(self) -> str:
        return get_weekday(self._number)["planet"]

    @property
    def is_sabbath(self) -> bool:
        """Friday (5), Saturday (6), and Sunday (7) are sabbath days."""
        return self._number >= 5

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"GaianWeekday({self._number})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GaianWeekday):
            return self._number == other._number
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, GaianWeekday):
            return self._number < other._number
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._number)

    # ------------------------------------------------------------------
    # Class constants
    # ------------------------------------------------------------------

    MONDAY    = None  # set below
    TUESDAY   = None
    WEDNESDAY = None
    THURSDAY  = None
    FRIDAY    = None
    SATURDAY  = None
    SUNDAY    = None


# Attach constants after class definition
GaianWeekday.MONDAY    = GaianWeekday(1)
GaianWeekday.TUESDAY   = GaianWeekday(2)
GaianWeekday.WEDNESDAY = GaianWeekday(3)
GaianWeekday.THURSDAY  = GaianWeekday(4)
GaianWeekday.FRIDAY    = GaianWeekday(5)
GaianWeekday.SATURDAY  = GaianWeekday(6)
GaianWeekday.SUNDAY    = GaianWeekday(7)
