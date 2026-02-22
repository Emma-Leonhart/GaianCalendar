"""Tests for GaianMonth and GaianWeekday."""
import pytest
from gaian_calendar import GaianMonth, GaianWeekday


class TestGaianMonth:
    def test_number(self):
        assert GaianMonth(3).number == 3

    def test_name(self):
        assert GaianMonth(3).name == "Aquarius"

    def test_symbol(self):
        assert GaianMonth(3).symbol == "♒"

    def test_element(self):
        assert GaianMonth(3).element == "Air"

    def test_horus_element_none(self):
        assert GaianMonth(14).element is None

    def test_horus_is_intercalary(self):
        assert GaianMonth(14).is_intercalary is True

    def test_regular_not_intercalary(self):
        assert GaianMonth(1).is_intercalary is False

    def test_from_name_full(self):
        assert GaianMonth.from_name("Aquarius") == GaianMonth(3)

    def test_from_name_abbrev(self):
        assert GaianMonth.from_name("Aqu") == GaianMonth(3)

    def test_from_name_case_insensitive(self):
        assert GaianMonth.from_name("aquarius") == GaianMonth(3)

    def test_from_name_invalid(self):
        with pytest.raises(ValueError):
            GaianMonth.from_name("Martius")

    def test_constant_aquarius(self):
        assert GaianMonth.AQUARIUS == GaianMonth(3)

    def test_constant_horus(self):
        assert GaianMonth.HORUS == GaianMonth(14)

    def test_str(self):
        assert str(GaianMonth(3)) == "Aquarius"

    def test_repr(self):
        assert repr(GaianMonth(3)) == "GaianMonth(3)"

    def test_comparison(self):
        assert GaianMonth(1) < GaianMonth(2)
        assert GaianMonth(13) > GaianMonth(12)

    def test_invalid_number(self):
        with pytest.raises(ValueError):
            GaianMonth(15)
        with pytest.raises(ValueError):
            GaianMonth(0)


class TestGaianWeekday:
    def test_number(self):
        assert GaianWeekday(1).number == 1

    def test_name(self):
        assert GaianWeekday(1).name == "Monday"

    def test_symbol(self):
        assert GaianWeekday(1).symbol == "☽"

    def test_planet(self):
        assert GaianWeekday(1).planet == "Moon"

    def test_sabbath_friday(self):
        assert GaianWeekday(5).is_sabbath is True

    def test_sabbath_saturday(self):
        assert GaianWeekday(6).is_sabbath is True

    def test_sabbath_sunday(self):
        assert GaianWeekday(7).is_sabbath is True

    def test_not_sabbath_monday(self):
        assert GaianWeekday(1).is_sabbath is False

    def test_constant_monday(self):
        assert GaianWeekday.MONDAY == GaianWeekday(1)

    def test_constant_sunday(self):
        assert GaianWeekday.SUNDAY == GaianWeekday(7)

    def test_str(self):
        assert str(GaianWeekday(1)) == "Monday"

    def test_repr(self):
        assert repr(GaianWeekday(1)) == "GaianWeekday(1)"

    def test_comparison(self):
        assert GaianWeekday(1) < GaianWeekday(7)

    def test_invalid_number(self):
        with pytest.raises(ValueError):
            GaianWeekday(8)
        with pytest.raises(ValueError):
            GaianWeekday(0)
