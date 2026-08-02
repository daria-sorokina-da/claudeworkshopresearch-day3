"""Run all four stages in order.

    python3 -m src.pipeline.run

No resume support, no state tracking, no cleanup between runs. Run it twice and read
build/04_report.txt carefully — the report will be wrong and will not say so.
"""

from __future__ import annotations

from . import stage1_ingest, stage2_clean, stage3_analyse, stage4_report


def main() -> int:
    stage1_ingest.run()
    stage2_clean.run()
    stage3_analyse.run()
    stage4_report.run()
    print("[run] pipeline complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
