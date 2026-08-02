# Royal Stables — Claude Code Workshop for Researchers

**The Day 3 lab repository.** A deliberately half-finished Python + SQL project about a
fairy-tale horse stable.

> **The lab started on Day 2**, in
> [`claudeworkshopresearch-lab-days2-3`](https://github.com/daria-sorokina-da/claudeworkshopresearch-lab-days2-3)
> — Part 0, repo onboarding, and the EDA exercise. **The codebase there is identical to
> this one**; the two repos differ only in which exercises their `EXERCISE.md` covers.
> Exercises 1–2 ran on Day 2; Exercises 3–12 run today.
>
> **You don't need to have been on Day 2.** Part 0 of [EXERCISE.md](EXERCISE.md) has two
> paths: copy your Day 2 `CLAUDE.md` across in one command, or build one from scratch in
> ten minutes. Everything after Part 0 is the same either way.

## What shape it is

Structurally it is the same shape as your work: a relational schema with integrity
problems, messy measurement data, a CLI, a pipeline, a monitoring service, a legacy
script, a small classifier, and some repetitive front-end code.

**There is no real data in this repository.** Everything is invented.

## ⛔ One directory is off limits

`src/algorithm/` — the race-suitability algorithm. Claude must not modify it. This is
enforced by `deny` rules in `.claude/settings.json` and by a `PreToolUse` hook, not
by asking nicely. It stands in for any code of yours whose correctness rests on a
rationale that isn't written in the file — matching logic, a validated method, a
threshold from a standard. See
[`src/algorithm/README.md`](src/algorithm/README.md) for why, and
[EXERCISE.md](EXERCISE.md) for the exercise that proves it works.

## Setup

```bash
git clone <your fork>
cd claudeworkshopresearch-day3
python -m venv .venv && source .venv/bin/activate   # or your usual approach
pip install -r requirements.txt
cp .env.example .env
python -m src.stable_cli.cli build                  # creates stables.db
pytest
```

Then get a `CLAUDE.md` in place — either copy your Day 2 one across, or generate and
correct a fresh one. [EXERCISE.md](EXERCISE.md) Part 0 covers both paths:

```bash
cp ../claudeworkshopresearch-lab-days2-3/CLAUDE.md .   # if you have it
# otherwise: run /init in a Claude session, then correct the draft by hand
```

**The database is SQLite** — no install, no server. It ships inside Python as the
`sqlite3` module and the whole database is one file, `stables.db`. Delete it and re-run
`build` any time you want a clean slate; it's gitignored.

**A database MCP is wired up for you.** `.mcp.json` is committed to the repo, so on a
fresh clone Claude gets a `stables-db` server pointed at `stables.db` — schema-aware
querying without writing inspection code each time. Run `/mcp` in a Claude session to
confirm it connected. It needs [`uv`](https://docs.astral.sh/uv/) on your PATH for
`uvx`; if it doesn't start, every exercise still works without it.

SQL in the exercises deliberately avoids dialect-specific syntax. Where Oracle or
BigQuery would behave differently, `EXERCISE.md` says so.

Perl is needed only for the conversion exercise (`perl -v` to check).

## What's in here

| Path | What it is | Exercise |
|---|---|---|
| `specs/stable_ledger.md` | A spec with no implementation | 3 — spec- and test-driven build |
| `sql/schema.sql`, `sql/seed.sql` | Under-constrained schema, data with planted violations | 4 — SQL data-quality checks |
| `src/stable_cli/` | CLI over the database. Contains one planted bug | 5 — off-by-one bug hunt |
| `legacy/stable_ledger.pl` | Real-flavoured legacy Perl, plus fixtures | 6 — Perl → Python |
| `web/` | Static yard board with repetitive JS and CSS | 7 — unfamiliar technologies |
| `src/algorithm/` | ⛔ Off limits | 8 — proving the red line |
| `src/pipeline/` | Four stages, not idempotent, not atomic | 9 — pipelines |
| `src/monitor/` | Directory watcher with the five classic bugs | 9 — monitoring |
| `src/ml/` | A classifier that reports 1.000 accuracy and is worthless | 10 — a little ML |
| `data/race_results.csv`, `data/measurements.csv` | Deliberately messy datasets — Day 2's EDA exercise | Optional self-practice |
| `analysis/slow_aggregate.py` | Correct and needlessly slow | Optional self-practice |

## A note on the planted bugs

Every bug in here is intentional and is *not* marked in the code. `pytest` passes on a
fresh clone — the existing suite is green despite a real bug in the reporting code,
which is the ordinary way bugs survive a test suite.

Please don't read the bug list in EXERCISE.md before you have gone looking.

## The five red lines

1. Never let it modify code whose correctness isn't visible in the code — here, `src/algorithm/`.
2. Never trust an unchecked statistic — keep the code as well as the number.
3. Never paste secrets or sensitive data into a prompt.
4. Never use `--dangerously-skip-permissions` on a real repo.
5. Always read the diff before accepting it.

## Licence

CC BY 4.0 — see [LICENSE.md](LICENSE.md).
