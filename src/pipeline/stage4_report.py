"""Stage 4 — render a plain-text report from the stage 3 summary.

Trusts its input completely. If stage 3 double-counted, this reports the doubled
numbers with no indication anything is wrong — which is the point.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build"


def run() -> Path:
    source = BUILD / "03_horse_summary.csv"
    target = BUILD / "04_report.txt"

    with open(source, newline="") as fh:
        rows = list(csv.DictReader(fh))

    lines = ["ROYAL STABLES — MEASUREMENT SUMMARY", "=" * 42, ""]
    lines.append(f"{'HORSE':<8}{'N':>6}{'MEAN_KG':>12}")
    for row in rows:
        lines.append(f"{row['horse_id']:<8}{row['n']:>6}{row['mean_kg']:>12}")
    lines.append("")
    lines.append(f"{len(rows)} rows in summary")

    target.write_text("\n".join(lines) + "\n")
    print(f"[stage4] wrote {target.name} ({len(rows)} rows)")
    return target


if __name__ == "__main__":
    run()
