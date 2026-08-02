"""Tests for the database layer.

These pass. They are the kind of tests a team writes when things are working.
"""

from src.stable_cli import db


def test_schema_creates_all_tables(conn):
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    names = {row["name"] for row in rows}
    assert {
        "horses", "race_entries", "races", "riders", "stables", "vet_visits"
    } <= names


def test_seed_loads_horses(conn):
    count = conn.execute("SELECT COUNT(*) AS n FROM horses").fetchone()["n"]
    assert count == 15


def test_seed_loads_races(conn):
    count = conn.execute("SELECT COUNT(*) AS n FROM races").fetchone()["n"]
    assert count == 9


def test_every_stable_has_a_name(conn):
    rows = conn.execute("SELECT stable_id FROM stables WHERE name IS NULL").fetchall()
    assert rows == []


def test_build_in_memory_is_isolated():
    """Two in-memory databases don't share state."""
    a = db.build_in_memory()
    b = db.build_in_memory()
    try:
        a.execute("DELETE FROM horses")
        a.commit()
        assert a.execute("SELECT COUNT(*) AS n FROM horses").fetchone()["n"] == 0
        assert b.execute("SELECT COUNT(*) AS n FROM horses").fetchone()["n"] == 15
    finally:
        a.close()
        b.close()
