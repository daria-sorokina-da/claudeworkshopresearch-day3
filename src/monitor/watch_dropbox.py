"""A directory-watching service. Naive on purpose.

    mkdir -p dropbox/incoming
    python3 -m src.monitor.watch_dropbox
    # then, in another shell:
    cp data/measurements.csv dropbox/incoming/

Known problems, all deliberate, all the classic ones:

  1. Processes a file the moment it appears — including one still being written.
  2. Remembers processed files in memory only. Restart and everything is reprocessed.
  3. Ignores files that arrived while the service was stopped.
  4. A file that raises during processing is retried forever, blocking the queue.
  5. No dead-letter path.

The exercise is to fix 1-5. Ask Claude how it will detect a complete file *before*
letting it write code — there are several approaches and they are not equally good.
"""

from __future__ import annotations

import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INCOMING = ROOT / "dropbox" / "incoming"
POLL_SECONDS = 2.0


def process(path: Path) -> int:
    """Pretend to process a file. Returns the number of data lines."""
    with open(path, newline="") as fh:
        lines = fh.readlines()
    if len(lines) <= 1:
        raise ValueError(f"{path.name} has no data rows")
    return len(lines) - 1


def watch() -> None:
    INCOMING.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()  # in memory only

    print(f"[monitor] watching {INCOMING} every {POLL_SECONDS}s — Ctrl+C to stop")
    while True:
        for path in sorted(INCOMING.glob("*.csv")):
            if path.name in seen:
                continue
            try:
                count = process(path)
            except Exception as exc:  # noqa: BLE001
                # Not added to `seen`, so this retries on every poll, forever.
                print(f"[monitor] ERROR {path.name}: {exc}")
                continue
            seen.add(path.name)
            print(f"[monitor] processed {path.name}: {count} rows")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        watch()
    except KeyboardInterrupt:
        print("\n[monitor] stopped")
