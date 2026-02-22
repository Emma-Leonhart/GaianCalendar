"""
Static data: month and weekday metadata for the Gaian Calendar.
"""

MONTHS: list[dict] = [
    {"number": 1,  "name": "Sagittarius", "abbrev": "Sag", "symbol": "♐", "element": "Fire",    "iso_weeks": (1,  4)},
    {"number": 2,  "name": "Capricorn",   "abbrev": "Cap", "symbol": "♑", "element": "Earth",   "iso_weeks": (5,  8)},
    {"number": 3,  "name": "Aquarius",    "abbrev": "Aqu", "symbol": "♒", "element": "Air",     "iso_weeks": (9,  12)},
    {"number": 4,  "name": "Pisces",      "abbrev": "Pis", "symbol": "♓", "element": "Water",   "iso_weeks": (13, 16)},
    {"number": 5,  "name": "Aries",       "abbrev": "Ari", "symbol": "♈", "element": "Fire",    "iso_weeks": (17, 20)},
    {"number": 6,  "name": "Taurus",      "abbrev": "Tau", "symbol": "♉", "element": "Earth",   "iso_weeks": (21, 24)},
    {"number": 7,  "name": "Gemini",      "abbrev": "Gem", "symbol": "♊", "element": "Air",     "iso_weeks": (25, 28)},
    {"number": 8,  "name": "Cancer",      "abbrev": "Can", "symbol": "♋", "element": "Water",   "iso_weeks": (29, 32)},
    {"number": 9,  "name": "Leo",         "abbrev": "Leo", "symbol": "♌", "element": "Fire",    "iso_weeks": (33, 36)},
    {"number": 10, "name": "Virgo",       "abbrev": "Vir", "symbol": "♍", "element": "Earth",   "iso_weeks": (37, 40)},
    {"number": 11, "name": "Libra",       "abbrev": "Lib", "symbol": "♎", "element": "Air",     "iso_weeks": (41, 44)},
    {"number": 12, "name": "Scorpius",    "abbrev": "Sco", "symbol": "♏", "element": "Water",   "iso_weeks": (45, 48)},
    {"number": 13, "name": "Ophiuchus",   "abbrev": "Oph", "symbol": "⛎", "element": "Healing", "iso_weeks": (49, 52)},
    {"number": 14, "name": "Horus",       "abbrev": "Hor", "symbol": "𓅃", "element": None,      "iso_weeks": (53, 53)},
]

WEEKDAYS: list[dict] = [
    {"number": 1, "name": "Monday",    "abbrev": "Mon", "symbol": "☽", "planet": "Moon"},
    {"number": 2, "name": "Tuesday",   "abbrev": "Tue", "symbol": "♂", "planet": "Mars"},
    {"number": 3, "name": "Wednesday", "abbrev": "Wed", "symbol": "☿", "planet": "Mercury"},
    {"number": 4, "name": "Thursday",  "abbrev": "Thu", "symbol": "♃", "planet": "Jupiter"},
    {"number": 5, "name": "Friday",    "abbrev": "Fri", "symbol": "♀", "planet": "Venus"},
    {"number": 6, "name": "Saturday",  "abbrev": "Sat", "symbol": "♄", "planet": "Saturn"},
    {"number": 7, "name": "Sunday",    "abbrev": "Sun", "symbol": "☉", "planet": "Sun"},
]

# Ordinal suffixes for days 1–28
_ORDINAL_SUFFIXES = {1: "st", 2: "nd", 3: "rd"}

def ordinal(n: int) -> str:
    """Return ordinal string: 1 → '1st', 2 → '2nd', 15 → '15th'."""
    suffix = _ORDINAL_SUFFIXES.get(n % 10, "th")
    # Special case: 11th, 12th, 13th (not 11st, 12nd, 13rd)
    if 11 <= n % 100 <= 13:
        suffix = "th"
    return f"{n}{suffix}"

_NUMBER_WORDS = [
    "", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh",
    "Eighth", "Ninth", "Tenth", "Eleventh", "Twelfth", "Thirteenth",
    "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth", "Eighteenth",
    "Nineteenth", "Twentieth", "Twenty-first", "Twenty-second", "Twenty-third",
    "Twenty-fourth", "Twenty-fifth", "Twenty-sixth", "Twenty-seventh", "Twenty-eighth",
]

def number_word(n: int) -> str:
    """Return word form: 1 → 'First', 15 → 'Fifteenth'."""
    if 1 <= n <= 28:
        return _NUMBER_WORDS[n]
    raise ValueError(f"number_word only supports 1–28, got {n}")

# Fast lookup maps
_MONTH_BY_NUMBER: dict[int, dict] = {m["number"]: m for m in MONTHS}
_MONTH_BY_NAME: dict[str, dict] = {}
for _m in MONTHS:
    _MONTH_BY_NAME[_m["name"].lower()] = _m
    _MONTH_BY_NAME[_m["abbrev"].lower()] = _m

_WEEKDAY_BY_NUMBER: dict[int, dict] = {w["number"]: w for w in WEEKDAYS}

def get_month(number: int) -> dict:
    if number not in _MONTH_BY_NUMBER:
        raise ValueError(f"Invalid month number: {number}")
    return _MONTH_BY_NUMBER[number]

def get_month_by_name(name: str) -> dict:
    key = name.lower().rstrip(".")
    if key not in _MONTH_BY_NAME:
        raise ValueError(f"Unknown month name: {name!r}")
    return _MONTH_BY_NAME[key]

def get_weekday(number: int) -> dict:
    if number not in _WEEKDAY_BY_NUMBER:
        raise ValueError(f"Invalid weekday number: {number}")
    return _WEEKDAY_BY_NUMBER[number]
