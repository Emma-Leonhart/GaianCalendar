"""
Pattern-based formatting for Gaian dates.

Tokens (processed in order of decreasing length to avoid partial matches):
  yyyy    5-digit Gaian year          12026
  yy      Last 2 digits of ISO year   26
  MMMM    Full month name             Aquarius
  MMM*    Month symbol                ♒
  MMM     Abbreviated month name      Aqu
  MM      Zero-padded month number    03
  M       Month number                3
  dddd    Day as word                 Fifteenth
  ddd     Ordinal day                 15th
  dd      Zero-padded day             15
  d       Day number                  15
  WWWW    Full weekday name           Monday
  WWW     Abbreviated weekday         Mon
  W       Weekday symbol              ☽
  DDD     Day of year, zero-padded    071
  GE      Literal suffix              GE
"""
import re
from ._data import get_month, get_weekday, ordinal, number_word
from ._convert import day_of_year, day_of_week

# Ordered list of (token, handler) — longer tokens must come before shorter prefixes
_TOKENS = [
    "yyyy", "yy",
    "MMMM", "MMM*", "MMM", "MM", "M",
    "dddd", "ddd", "dd", "d",
    "WWWW", "WWW", "W",
    "DDD",
    "GE",
]

# Build a regex that matches any token OR a single character (for literals)
_TOKEN_PATTERN = re.compile(
    "(" + "|".join(re.escape(t) for t in _TOKENS) + r"|.)",
    re.DOTALL,
)


def format_date(year: int, month: int, day: int, pattern: str) -> str:
    """Format a Gaian date using a pattern string."""
    iso_year = year - 10_000
    month_data = get_month(month)
    dow = day_of_week(day)
    weekday_data = get_weekday(dow)
    doy = day_of_year(month, day)

    parts: list[str] = []
    for token in _TOKEN_PATTERN.findall(pattern):
        if token == "yyyy":
            parts.append(str(year))
        elif token == "yy":
            parts.append(f"{iso_year % 100:02d}")
        elif token == "MMMM":
            parts.append(month_data["name"])
        elif token == "MMM*":
            parts.append(month_data["symbol"])
        elif token == "MMM":
            parts.append(month_data["abbrev"])
        elif token == "MM":
            parts.append(f"{month:02d}")
        elif token == "M":
            parts.append(str(month))
        elif token == "dddd":
            parts.append(number_word(day))
        elif token == "ddd":
            parts.append(ordinal(day))
        elif token == "dd":
            parts.append(f"{day:02d}")
        elif token == "d":
            parts.append(str(day))
        elif token == "WWWW":
            parts.append(weekday_data["name"])
        elif token == "WWW":
            parts.append(weekday_data["abbrev"])
        elif token == "W":
            parts.append(weekday_data["symbol"])
        elif token == "DDD":
            parts.append(f"{doy:03d}")
        elif token == "GE":
            parts.append("GE")
        else:
            parts.append(token)  # literal character

    return "".join(parts)
