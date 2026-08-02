"""Tests for the reporting layer.

All of these pass. That is worth sitting with for a moment: the reporting code
contains a real bug, and this suite is green.

The tests are not dishonest — each one was written by someone checking that the
thing they had just built worked. They simply never picked the input that exposes
the problem. That is the ordinary way bugs survive a test suite.
"""

from datetime import date

from src.stable_cli import reports


def test_week_of_returns_monday_to_sunday():
    monday, sunday = reports.week_of(date(2026, 3, 18))  # a Wednesday
    assert monday == date(2026, 3, 16)
    assert sunday == date(2026, 3, 22)
    assert monday.weekday() == 0
    assert sunday.weekday() == 6


def test_week_of_is_stable_for_a_monday():
    monday, sunday = reports.week_of(date(2026, 3, 16))
    assert monday == date(2026, 3, 16)
    assert sunday == date(2026, 3, 22)


def test_races_in_window_finds_a_single_race(conn):
    rows = reports.races_in_window(conn, date(2026, 3, 16), date(2026, 3, 20))
    assert len(rows) == 1
    assert rows[0]["name"] == "Ashcombe Novice Stakes"


def test_races_in_window_is_empty_when_no_races(conn):
    rows = reports.races_in_window(conn, date(2026, 5, 1), date(2026, 5, 31))
    assert rows == []


def test_races_in_window_orders_by_date(conn):
    rows = reports.races_in_window(conn, date(2026, 3, 1), date(2026, 3, 20))
    dates = [row["run_on"] for row in rows]
    assert dates == sorted(dates)


def test_weekly_race_count_for_a_quiet_week(conn):
    assert reports.weekly_race_count(conn, date(2026, 3, 16)) == 1


def test_weekly_race_count_is_zero_out_of_season(conn):
    assert reports.weekly_race_count(conn, date(2026, 5, 6)) == 0


def test_placings_for_horse_returns_entries(conn):
    rows = reports.placings_for_horse(conn, 1)
    assert len(rows) >= 3
    assert all("race_name" in row.keys() for row in rows)


def test_placings_for_horse_is_empty_for_unknown_horse(conn):
    assert reports.placings_for_horse(conn, 4242) == []


def test_stable_summary_covers_every_stable(conn):
    rows = reports.stable_summary(conn)
    assert len(rows) == 4
    assert {row["stable"] for row in rows} == {
        "Ashcombe", "Fairwater", "Northgate", "Willowmere"
    }
