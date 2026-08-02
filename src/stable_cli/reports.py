"""Reporting queries for stable-cli.

Contains one planted bug. It is not marked. Existing tests pass.
"""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta


def races_in_window(
    conn: sqlite3.Connection,
    start: date,
    end: date,
) -> list[sqlite3.Row]:
    """Return races run between `start` and `end`, inclusive of both endpoints."""
    cursor = conn.execute(
        """
        SELECT race_id, name, run_on, distance_f, going
        FROM races
        WHERE run_on >= ? AND run_on < ?
        ORDER BY run_on
        """,
        (start.isoformat(), end.isoformat()),
    )
    return cursor.fetchall()


def week_of(day: date) -> tuple[date, date]:
    """Return the (Monday, Sunday) pair for the week containing `day`."""
    monday = day - timedelta(days=day.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def weekly_race_count(conn: sqlite3.Connection, day: date) -> int:
    """How many races were run in the week containing `day`."""
    start, end = week_of(day)
    return len(races_in_window(conn, start, end))


def placings_for_horse(conn: sqlite3.Connection, horse_id: int) -> list[sqlite3.Row]:
    """Every race entry for one horse, most recent first."""
    cursor = conn.execute(
        """
        SELECT e.entry_id, r.name AS race_name, r.run_on,
               e.finish_position, e.placed
        FROM race_entries e
        JOIN races r ON r.race_id = e.race_id
        WHERE e.horse_id = ?
        ORDER BY r.run_on DESC
        """,
        (horse_id,),
    )
    return cursor.fetchall()


def stable_summary(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    """Horse count and placed-entry count per stable."""
    cursor = conn.execute(
        """
        SELECT s.name AS stable,
               COUNT(DISTINCT h.horse_id) AS horses,
               COALESCE(SUM(e.placed), 0) AS placed_entries
        FROM stables s
        LEFT JOIN horses h ON h.stable_id = s.stable_id
        LEFT JOIN race_entries e ON e.horse_id = h.horse_id
        GROUP BY s.stable_id, s.name
        ORDER BY s.name
        """
    )
    return cursor.fetchall()
