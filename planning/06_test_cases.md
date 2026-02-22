# GaianCalendar — Test Cases

Known-good conversions to validate implementation against.

## Gregorian → Gaian Ground Truth

| Gregorian Date | ISO (year, week, day) | Gaian Date | Notes |
|---------------|----------------------|------------|-------|
| 2026-01-05 (Mon) | 2026 W01 Mon | Sagittarius 1, 12026 | First day of year |
| 2026-02-22 (Sun) | 2026 W08 Sun | Capricorn 28, 12026 | Last day of Capricorn |
| 2026-03-02 (Mon) | 2026 W10 Mon | Aquarius 8, 12026 | Mid-Aquarius |
| 2026-12-28 (Mon) | 2026 W53 Mon | Horus 1, 12026 | First day of Horus (leap year) |
| 2026-12-31 (Thu) | 2026 W53 Thu | Horus 4, 12026 | Horus in leap year |
| 2025-01-06 (Mon) | 2025 W02 Mon | Sagittarius 8, 12025 | Note: 2025 W01 starts Dec 30, 2024 |
| 2025-12-29 (Mon) | 2026 W01 Mon | Sagittarius 1, 12026 | ISO week-year rolls over early! |

> **Critical edge case**: The ISO week-year can differ from the calendar year in late December / early January.
> e.g., 2025-12-29 is in ISO year 2026, so it's Gaian year 12026.

## Gaian → Gregorian Ground Truth

| Gaian Date | Expected Gregorian |
|------------|-------------------|
| Sagittarius 1, 12026 | 2026-01-05 |
| Sagittarius 7, 12026 | 2026-01-11 |  (Sunday)
| Sagittarius 8, 12026 | 2026-01-12 |  (Monday, week 2)
| Aquarius 1, 12026 | 2026-03-02 |
| Horus 1, 12026 | 2026-12-28 |
| Horus 7, 12026 | 2027-01-03 |  (last day of Horus)

## Leap Year Tests

| Gaian Year | Is Leap? | Notes |
|------------|---------|-------|
| 12020 | True | ISO 2020 had 53 weeks |
| 12021 | False | |
| 12025 | False | |
| 12026 | True | ISO 2026 has 53 weeks |
| 12032 | True | |

## Day of Year Tests

| Month | Day | Expected DoY |
|-------|-----|-------------|
| 1 | 1 | 1 |
| 1 | 28 | 28 |
| 2 | 1 | 29 |
| 3 | 15 | 71 |
| 13 | 28 | 364 |
| 14 | 1 | 365 (leap only) |
| 14 | 7 | 371 (leap only) |

## Day of Week Tests (Perpetual)

| Day in month | Expected weekday | Name |
|-------------|-----------------|------|
| 1 | 1 | Monday |
| 7 | 7 | Sunday |
| 8 | 1 | Monday |
| 14 | 7 | Sunday |
| 15 | 1 | Monday |
| 28 | 7 | Sunday |

(This holds true for ALL months, ALL years — it's the perpetual property)

## Format Pattern Tests

Input: `GaianDate(12026, 3, 15)` (Aquarius 15, 12026 — a Monday)

| Pattern | Expected Output |
|---------|----------------|
| `"MMMM d, yyyy GE"` | `"Aquarius 15, 12026 GE"` |
| `"MMM d, yy"` | `"Aqu 15, 26"` |
| `"M/d/yyyy"` | `"3/15/12026"` |
| `"yyyy-MM-dd"` | `"12026-03-15"` |
| `"MMM*"` | `"♒"` |
| `"W"` | `"☽"` |
| `"WWW"` | `"Mon"` |
| `"WWWW"` | `"Monday"` |
| `"ddd"` | `"15th"` |
| `"DDD"` | `"071"` |

## Parse Tests

All should produce `GaianDate(12026, 3, 15)`:

| Input string |
|-------------|
| `"Aquarius 15, 12026"` |
| `"Aquarius 15, 12026 GE"` |
| `"Aqu 15, 12026"` |
| `"3/15/12026"` |
| `"12026-03-15"` |

## Arithmetic Tests

| Start | Operation | Expected |
|-------|-----------|---------|
| Aquarius 28, 12026 | `+ timedelta(1)` | Pisces 1, 12026 |
| Sagittarius 1, 12026 | `- timedelta(1)` | Ophiuchus 28, 12025 |
| Horus 7, 12026 | `+ timedelta(1)` | Sagittarius 1, 12027 |
| Pisces 1, 12026 | `- timedelta(1)` | Aquarius 28, 12026 |

## Edge Cases to Test

1. Last day of a non-leap year: Ophiuchus 28, 12025
2. First day of a year: Sagittarius 1, 12026
3. Gregorian year boundary (Dec 29 → ISO week 1 of next year)
4. Horus month in leap year (both first and last day)
5. Attempting to create Horus date in non-leap year → ValueError
6. Day 29 in any month → ValueError
