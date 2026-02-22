"""Tests for the formatting engine."""
import pytest
from gaian_calendar import GaianDate


class TestFormat:
    def setup_method(self):
        # Aquarius 15, 12026 — a Monday, day of year 71
        self.d = GaianDate(12026, 3, 15)

    def test_full_default(self):
        assert str(self.d) == "Aquarius 15, 12026 GE"

    def test_yyyy(self):
        assert self.d.format("yyyy") == "12026"

    def test_yy(self):
        assert self.d.format("yy") == "26"

    def test_MMMM(self):
        assert self.d.format("MMMM") == "Aquarius"

    def test_MMM(self):
        assert self.d.format("MMM") == "Aqu"

    def test_MMM_star(self):
        assert self.d.format("MMM*") == "♒"

    def test_MM(self):
        assert self.d.format("MM") == "03"

    def test_M(self):
        assert self.d.format("M") == "3"

    def test_dd(self):
        assert self.d.format("dd") == "15"

    def test_d(self):
        assert self.d.format("d") == "15"

    def test_ddd(self):
        assert self.d.format("ddd") == "15th"

    def test_dddd(self):
        assert self.d.format("dddd") == "Fifteenth"

    def test_WWWW(self):
        assert self.d.format("WWWW") == "Monday"

    def test_WWW(self):
        assert self.d.format("WWW") == "Mon"

    def test_W(self):
        assert self.d.format("W") == "☽"

    def test_DDD(self):
        assert self.d.format("DDD") == "071"

    def test_GE_literal(self):
        assert self.d.format("GE") == "GE"

    def test_combined_pattern(self):
        assert self.d.format("MMMM d, yyyy GE") == "Aquarius 15, 12026 GE"

    def test_iso_like(self):
        assert self.d.format("yyyy-MM-dd") == "12026-03-15"

    def test_slash_numeric(self):
        assert self.d.format("M/d/yyyy") == "3/15/12026"

    def test_symbol_doy(self):
        assert self.d.format("MMM* DDD") == "♒ 071"

    def test_weekday_full(self):
        assert self.d.format("WWWW, MMMM d, yyyy GE") == "Monday, Aquarius 15, 12026 GE"

    def test_ordinal_first(self):
        assert GaianDate(12026, 1, 1).format("ddd") == "1st"

    def test_ordinal_second(self):
        assert GaianDate(12026, 1, 2).format("ddd") == "2nd"

    def test_ordinal_third(self):
        assert GaianDate(12026, 1, 3).format("ddd") == "3rd"

    def test_ordinal_eleventh(self):
        assert GaianDate(12026, 1, 11).format("ddd") == "11th"

    def test_ordinal_twelfth(self):
        assert GaianDate(12026, 1, 12).format("ddd") == "12th"

    def test_word_first(self):
        assert GaianDate(12026, 1, 1).format("dddd") == "First"

    def test_word_twenty_eighth(self):
        assert GaianDate(12026, 1, 28).format("dddd") == "Twenty-eighth"

    def test_literal_characters_pass_through(self):
        assert self.d.format("MMMM 'the' d") == "Aquarius 'the' 15"
