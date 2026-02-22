"""Tests for core calendar arithmetic in _convert.py."""
import pytest
from datetime import date
from gaian_calendar._convert import (
    gregorian_to_gaian,
    gaian_to_gregorian,
    is_leap_year,
    day_of_year,
    day_of_week,
    validate_date,
)


# ---------------------------------------------------------------------------
# Leap year
# ---------------------------------------------------------------------------

class TestLeapYear:
    def test_12026_is_leap(self):
        assert is_leap_year(12026) is True

    def test_12025_not_leap(self):
        assert is_leap_year(12025) is False

    def test_12020_is_leap(self):
        assert is_leap_year(12020) is True

    def test_12021_not_leap(self):
        assert is_leap_year(12021) is False

    def test_12032_is_leap(self):
        assert is_leap_year(12032) is True


# ---------------------------------------------------------------------------
# Gregorian → Gaian
# ---------------------------------------------------------------------------

class TestGregorianToGaian:
    def test_first_day_of_12026(self):
        # ISO 2026 W01 starts Dec 29, 2025 (the ISO year starts before calendar year)
        # 2025-12-29 is ISO 2026 W01 Mon → Sagittarius 1, 12026
        assert gregorian_to_gaian(date(2025, 12, 29)) == (12026, 1, 1)
        # 2026-01-05 is ISO 2026 W02 Mon → Sagittarius 8, 12026
        assert gregorian_to_gaian(date(2026, 1, 5)) == (12026, 1, 8)

    def test_last_day_of_capricorn(self):
        # 2026-02-22 is ISO 2026 W08 Sun → Capricorn 28, 12026
        assert gregorian_to_gaian(date(2026, 2, 22)) == (12026, 2, 28)

    def test_first_day_horus(self):
        # 2026-12-28 is ISO 2026 W53 Mon → Horus 1, 12026
        assert gregorian_to_gaian(date(2026, 12, 28)) == (12026, 14, 1)

    def test_last_day_horus(self):
        # 2026-12-31 is ISO 2026 W53 Thu → Horus 4, 12026
        assert gregorian_to_gaian(date(2026, 12, 31)) == (12026, 14, 4)

    def test_iso_year_rollover(self):
        # 2025-12-29 is ISO year 2026 W01 Mon → Sagittarius 1, 12026
        assert gregorian_to_gaian(date(2025, 12, 29)) == (12026, 1, 1)

    def test_roundtrip(self):
        d = date(2026, 6, 15)
        y, m, day = gregorian_to_gaian(d)
        assert gaian_to_gregorian(y, m, day) == d


# ---------------------------------------------------------------------------
# Gaian → Gregorian
# ---------------------------------------------------------------------------

class TestGaianToGregorian:
    def test_sagittarius_1_12026(self):
        # ISO 2026 W01 Mon = Dec 29, 2025 (ISO week-year starts before calendar year)
        assert gaian_to_gregorian(12026, 1, 1) == date(2025, 12, 29)

    def test_sagittarius_7_12026(self):
        # ISO 2026 W01 Sun = Jan 4, 2026
        assert gaian_to_gregorian(12026, 1, 7) == date(2026, 1, 4)

    def test_aquarius_1_12026(self):
        # ISO 2026 W09 Mon = Feb 23, 2026
        assert gaian_to_gregorian(12026, 3, 1) == date(2026, 2, 23)

    def test_horus_1_12026(self):
        assert gaian_to_gregorian(12026, 14, 1) == date(2026, 12, 28)

    def test_roundtrip_all_days_in_year(self):
        for doy in range(1, 365):
            month = (doy - 1) // 28 + 1
            day = (doy - 1) % 28 + 1
            greg = gaian_to_gregorian(12025, month, day)
            back = gregorian_to_gaian(greg)
            assert back == (12025, month, day), f"Failed at doy={doy}"


# ---------------------------------------------------------------------------
# Day of year
# ---------------------------------------------------------------------------

class TestDayOfYear:
    def test_first_day(self):
        assert day_of_year(1, 1) == 1

    def test_last_regular_day(self):
        assert day_of_year(13, 28) == 364

    def test_mid_year(self):
        assert day_of_year(3, 15) == 71

    def test_horus_first(self):
        assert day_of_year(14, 1) == 365

    def test_horus_last(self):
        assert day_of_year(14, 7) == 371

    def test_second_month_start(self):
        assert day_of_year(2, 1) == 29


# ---------------------------------------------------------------------------
# Day of week (perpetual)
# ---------------------------------------------------------------------------

class TestDayOfWeek:
    def test_day_1_is_monday(self):
        assert day_of_week(1) == 1

    def test_day_7_is_sunday(self):
        assert day_of_week(7) == 7

    def test_day_8_is_monday(self):
        assert day_of_week(8) == 1

    def test_day_14_is_sunday(self):
        assert day_of_week(14) == 7

    def test_day_15_is_monday(self):
        assert day_of_week(15) == 1

    def test_day_28_is_sunday(self):
        assert day_of_week(28) == 7


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestValidation:
    def test_valid_date(self):
        validate_date(12026, 3, 15)  # should not raise

    def test_horus_in_non_leap_raises(self):
        with pytest.raises(ValueError, match="leap"):
            validate_date(12025, 14, 1)

    def test_day_29_raises(self):
        with pytest.raises(ValueError):
            validate_date(12026, 3, 29)

    def test_horus_day_8_raises(self):
        with pytest.raises(ValueError):
            validate_date(12026, 14, 8)

    def test_month_0_raises(self):
        with pytest.raises(ValueError):
            validate_date(12026, 0, 1)

    def test_day_0_raises(self):
        with pytest.raises(ValueError):
            validate_date(12026, 3, 0)
