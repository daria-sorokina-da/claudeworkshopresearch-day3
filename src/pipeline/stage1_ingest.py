"""Stage 1 — ingest raw CSVs into build/.

Copies and normalises nothing. Intentionally the simplest stage.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
BUILD = ROOT / "build"


def run() -> list[Path]:
    BUILD.mkdir(exist_ok=True)
    written = []
    for name in ("race_results.csv", "measurements.csv"):
        source = DATA / name
        target = BUILD / f"01_raw_{name}"
        shutil.copyfile(source, target)
        written.append(target)
    print(f"[stage1] ingested {len(written)} files -> {BUILD}")
    return written


if __name__ == "__main__":
    run()
