"""Aggregate measurements per horse per month. Correct, and unnecessarily slow.

Optional exercise. Profile it before changing it — the interesting part is that the
obvious culprit is not the expensive one.

    python3 -m cProfile -s cumtime analysis/slow_aggregate.py | head -25
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "measurements.csv"


def load_rows(path: Path) -> list[dict]:
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def parse_month(taken_at: str) -> str | None:
    """Return 'YYYY-MM', or None if the timestamp isn't in the expected format."""
    if "T" in taken_at and len(taken_at) >= 7:
        return taken_at[:7]
    return None


def monthly_means(rows: list[dict]) -> dict[tuple[str, str], float]:
    """Mean value per (horse_id, month).

    Deliberately naive: rebuilds the filtered list for every group, so the cost is
    quadratic in the number of groups. With a handful of horses over four months
    it's tolerable; the shape is what matters.
    """
    horse_ids = []
    for row in rows:
        if row["horse_id"] not in horse_ids:
            horse_ids.append(row["horse_id"])

    months = []
    for row in rows:
        month = parse_month(row["taken_at"])
        if month and month not in months:
            months.append(month)

    result = {}
    for horse_id in horse_ids:
        for month in months:
            values = []
            for row in rows:
                if row["horse_id"] != horse_id:
                    continue
                if parse_month(row["taken_at"]) != month:
                    continue
                raw = row["value"]
                if raw in ("", None):
                    continue
                try:
                    values.append(float(raw))
                except ValueError:
                    continue
            if values:
                result[(horse_id, month)] = sum(values) / len(values)
    return result


def main() -> None:
    rows = load_rows(DATA)
    means = monthly_means(rows)
    for (horse_id, month), mean in sorted(means.items()):
        print(f"horse {horse_id:>3}  {month}  mean={mean:8.2f}")
    print(f"\n{len(means)} groups from {len(rows)} rows")


if __name__ == "__main__":
    main()
