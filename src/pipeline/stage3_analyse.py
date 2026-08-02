"""Stage 3 — aggregate cleaned measurements per horse.

Two problems here, both deliberate, both the kind that survive code review:

  1. It APPENDS to its output file. Re-running the stage double-counts.
  2. It writes incrementally with no temporary file, so a mid-stage failure leaves a
     partial output that looks like a complete one.

The exercise is to make it idempotent and atomic. Ask Claude to state its approach
before it writes any code.
"""

from __future__ import annotations

import csv
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build"

# Set FAIL_AT_ROW to an integer to simulate a mid-stage crash:
#     FAIL_AT_ROW=200 python3 -m src.pipeline.stage3_analyse
FAIL_AT_ROW = os.environ.get("FAIL_AT_ROW")


def run() -> Path:
    source = BUILD / "02_clean_measurements.csv"
    target = BUILD / "03_horse_summary.csv"

    totals: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)

    with open(source, newline="") as fh:
        for index, row in enumerate(csv.DictReader(fh), start=1):
            if FAIL_AT_ROW and index == int(FAIL_AT_ROW):
                raise RuntimeError(
                    f"simulated failure at row {index} — "
                    "check what state build/ is in now"
                )
            totals[row["horse_id"]] += float(row["value_kg"])
            counts[row["horse_id"]] += 1

    # Append mode. Re-running this stage appends a second set of rows.
    is_new = not target.exists()
    with open(target, "a", newline="") as fh:
        writer = csv.writer(fh)
        if is_new:
            writer.writerow(["horse_id", "n", "mean_kg"])
        for horse_id in sorted(totals, key=lambda h: int(h)):
            mean = totals[horse_id] / counts[horse_id]
            writer.writerow([horse_id, counts[horse_id], round(mean, 2)])

    print(f"[stage3] wrote {len(totals)} groups -> {target.name}")
    return target


if __name__ == "__main__":
    run()
