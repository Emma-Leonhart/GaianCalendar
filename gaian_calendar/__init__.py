"""
gaian_calendar — Python library for the Gaian Calendar.

A perpetual 13-month solar calendar based on ISO week-year arithmetic.
Gaian year = ISO week-year + 10,000.
"""

__version__ = "0.1.0"

from .date import GaianDate
from .month import GaianMonth
from .weekday import GaianWeekday
from ._convert import is_leap_year

__all__ = [
    "GaianDate",
    "GaianMonth",
    "GaianWeekday",
    "is_leap_year",
    "__version__",
]
