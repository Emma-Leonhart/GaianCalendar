"""Tests for GaianDate."""
import pytest
from datetime import date, timedelta
from gaian_calendar import GaianDate


class TestConstruction:
    def test_basic(self):
        d = GaianDate(12026, 3, 15)
        assert d.year == 12026
        assert d.month == 3
        assert d.day == 15

    def test_repr(self):
        assert repr(GaianDate(12026, 3, 15)) == "GaianDate(12026, 3, 15)"

    def test_str(self):
        assert str(GaianDate(12026, 3, 15)) == "Aquarius 15, 12026 GE"

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            GaianDate(12025, 14, 1)  # Horus in non-leap year


class TestFromGregorian:
    def test_known_date(self):
        # ISO 2026 W01 starts Dec 29, 2025 — ISO year rolls before calendar year
        d = GaianDate.from_gregorian(date(2025, 12, 29))
        assert d == GaianDate(12026, 1, 1)
        # Jan 5, 2026 is ISO 2026 W02 → Sagittarius 8
        d2 = GaianDate.from_gregorian(date(2026, 1, 5))
        assert d2 == GaianDate(12026, 1, 8)

    def test_roundtrip(self):
        greg = date(2026, 7, 4)
        gaian = GaianDate.from_gregorian(greg)
        assert gaian.to_gregorian() == greg


class TestProperties:
    def setup_method(self):
        self.d = GaianDate(12026, 3, 15)

    def test_month_name(self):
        assert self.d.month_name == "Aquarius"

    def test_month_symbol(self):
        assert self.d.month_symbol == "♒"

    def test_weekday_name(self):
        assert self.d.weekday_name == "Monday"

    def test_weekday_symbol(self):
        assert self.d.weekday_symbol == "☽"

    def test_day_of_week(self):
        assert self.d.day_of_week == 1  # Monday

    def test_day_of_year(self):
        assert self.d.day_of_year == 71

    def test_is_leap_year(self):
        assert self.d.is_leap_year is True

    def test_non_leap(self):
        assert GaianDate(12025, 1, 1).is_leap_year is False


class TestArithmetic:
    def test_add_days(self):
        d = GaianDate(12026, 2, 28)  # last day of Capricorn
        result = d + timedelta(days=1)
        assert result == GaianDate(12026, 3, 1)  # first day of Aquarius

    def test_subtract_days(self):
        d = GaianDate(12026, 3, 1)
        result = d - timedelta(days=1)
        assert result == GaianDate(12026, 2, 28)

    def test_year_boundary_backward(self):
        d = GaianDate(12026, 1, 1)  # Sagittarius 1, 12026
        result = d - timedelta(days=1)
        assert result == GaianDate(12025, 13, 28)  # Ophiuchus 28, 12025

    def test_subtract_two_dates(self):
        d1 = GaianDate(12026, 1, 1)
        d2 = GaianDate(12026, 1, 8)
        assert d2 - d1 == timedelta(days=7)

    def test_add_week(self):
        d = GaianDate(12026, 3, 1)
        result = d + timedelta(weeks=1)
        assert result == GaianDate(12026, 3, 8)


class TestComparison:
    def test_equal(self):
        assert GaianDate(12026, 3, 15) == GaianDate(12026, 3, 15)

    def test_not_equal(self):
        assert GaianDate(12026, 3, 15) != GaianDate(12026, 3, 16)

    def test_less_than(self):
        assert GaianDate(12026, 1, 1) < GaianDate(12026, 1, 2)

    def test_greater_than(self):
        assert GaianDate(12026, 2, 1) > GaianDate(12026, 1, 28)

    def test_hash_equal(self):
        a = GaianDate(12026, 3, 15)
        b = GaianDate(12026, 3, 15)
        assert hash(a) == hash(b)

    def test_usable_as_dict_key(self):
        d = {GaianDate(12026, 1, 1): "New Year"}
        assert d[GaianDate(12026, 1, 1)] == "New Year"


class TestParse:
    def test_full_name(self):
        assert GaianDate.parse("Aquarius 15, 12026") == GaianDate(12026, 3, 15)

    def test_full_name_with_ge(self):
        assert GaianDate.parse("Aquarius 15, 12026 GE") == GaianDate(12026, 3, 15)

    def test_abbreviated_name(self):
        assert GaianDate.parse("Aqu 15, 12026") == GaianDate(12026, 3, 15)

    def test_slash_numeric(self):
        assert GaianDate.parse("3/15/12026") == GaianDate(12026, 3, 15)

    def test_iso_numeric(self):
        assert GaianDate.parse("12026-03-15") == GaianDate(12026, 3, 15)

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            GaianDate.parse("not a date")


class TestFromDayOfYear:
    def test_day_1(self):
        assert GaianDate.from_day_of_year(12026, 1) == GaianDate(12026, 1, 1)

    def test_day_71(self):
        assert GaianDate.from_day_of_year(12026, 71) == GaianDate(12026, 3, 15)

    def test_day_364(self):
        assert GaianDate.from_day_of_year(12026, 364) == GaianDate(12026, 13, 28)

    def test_horus_day(self):
        assert GaianDate.from_day_of_year(12026, 365) == GaianDate(12026, 14, 1)

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError):
            GaianDate.from_day_of_year(12025, 365)  # 12025 is not leap
