"""Stage 2 — clean the ingested measurements.

Handles some of the mess in the data and silently ignores the rest. Which parts it
ignores is worth working out before you change anything.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build"

LB_TO_KG = 0.45359237


def run() -> Path:
    source = BUILD / "01_raw_measurements.csv"
    target = BUILD / "02_clean_measurements.csv"

    kept, dropped = 0, 0
    with open(source, newline="") as fh_in, open(target, "w", newline="") as fh_out:
        reader = csv.DictReader(fh_in)
        writer = csv.DictWriter(fh_out, fieldnames=["taken_at", "horse_id", "value_kg"])
        writer.writeheader()

        for row in reader:
            raw = (row.get("value") or "").strip()
            if not raw:
                dropped += 1
                continue
            try:
                value = float(raw)
            except ValueError:
                dropped += 1
                continue

            unit = (row.get("unit") or "kg").strip().lower()
            if unit == "lb":
                value *= LB_TO_KG
            elif unit not in ("kg", ""):
                # Unknown unit. Kept anyway, on the assumption it's kilograms.
                # That assumption is not stated anywhere the caller can see it.
                pass

            writer.writerow({
                "taken_at": row["taken_at"],
                "horse_id": row["horse_id"],
                "value_kg": round(value, 2),
            })
            kept += 1

    print(f"[stage2] kept {kept}, dropped {dropped} -> {target.name}")
    return target


if __name__ == "__main__":
    run()
