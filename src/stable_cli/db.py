"""Database helpers for the Royal Stables demo.

SQLite so the repo is self-contained. The SQL exercises are written to be portable;
where Oracle or BigQuery would differ, EXERCISE.md says so.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "sql" / "schema.sql"
SEED_PATH = REPO_ROOT / "sql" / "seed.sql"
DEFAULT_DB_PATH = REPO_ROOT / "stables.db"


def connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Open a connection with row access by name and foreign keys OFF.

    Foreign keys are deliberately left off. The seed data contains orphan rows on
    purpose, and enforcing constraints at load time would hide the very problems the
    data-quality exercise is about. Turning them on is part of the exercise.
    """
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def build(db_path: Path | str | None = None) -> Path:
    """(Re)create the database from schema.sql and seed.sql. Destructive."""
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    if path.exists():
        path.unlink()

    conn = sqlite3.connect(path)
    try:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.executescript(SEED_PATH.read_text())
        conn.commit()
    finally:
        conn.close()
    return path


def build_in_memory() -> sqlite3.Connection:
    """An in-memory database for tests. Same schema and seed."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_PATH.read_text())
    conn.executescript(SEED_PATH.read_text())
    conn.commit()
    return conn
