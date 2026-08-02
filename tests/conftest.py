import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.stable_cli import db  # noqa: E402


@pytest.fixture
def conn():
    """A fresh in-memory database, schema + seed, per test."""
    connection = db.build_in_memory()
    yield connection
    connection.close()
