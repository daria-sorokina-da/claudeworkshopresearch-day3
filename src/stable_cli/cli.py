"""stable-cli entry point.

    python -m src.stable_cli.cli build
    python -m src.stable_cli.cli week 2026-03-16
    python -m src.stable_cli.cli horse 1
    python -m src.stable_cli.cli stables
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime

from . import db, reports


def _parse_day(text: str) -> date:
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise SystemExit(f"Not a valid date (expected YYYY-MM-DD): {text!r}")


def cmd_build(_args: argparse.Namespace) -> int:
    path = db.build()
    print(f"Built {path}")
    return 0


def cmd_week(args: argparse.Namespace) -> int:
    day = _parse_day(args.day)
    conn = db.connect()
    try:
        start, end = reports.week_of(day)
        rows = reports.races_in_window(conn, start, end)
        print(f"Races in the week {start} to {end} (inclusive): {len(rows)}")
        for row in rows:
            print(f"  {row['run_on']}  {row['name']}  ({row['distance_f']}f, {row['going']})")
    finally:
        conn.close()
    return 0


def cmd_horse(args: argparse.Namespace) -> int:
    conn = db.connect()
    try:
        rows = reports.placings_for_horse(conn, args.horse_id)
        if not rows:
            print(f"No entries found for horse_id {args.horse_id}")
            return 0
        for row in rows:
            flag = "placed" if row["placed"] else "-"
            print(f"  {row['run_on']}  {row['race_name']}: "
                  f"position {row['finish_position']} ({flag})")
    finally:
        conn.close()
    return 0


def cmd_stables(_args: argparse.Namespace) -> int:
    conn = db.connect()
    try:
        for row in reports.stable_summary(conn):
            print(f"  {row['stable']:<14} horses={row['horses']:<3} "
                  f"placed_entries={row['placed_entries']}")
    finally:
        conn.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stable-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("build", help="(re)create the database from schema + seed").set_defaults(func=cmd_build)

    p_week = sub.add_parser("week", help="races in the week containing a date")
    p_week.add_argument("day", help="a date in the week, YYYY-MM-DD")
    p_week.set_defaults(func=cmd_week)

    p_horse = sub.add_parser("horse", help="every entry for one horse")
    p_horse.add_argument("horse_id", type=int)
    p_horse.set_defaults(func=cmd_horse)

    sub.add_parser("stables", help="summary per stable").set_defaults(func=cmd_stables)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
