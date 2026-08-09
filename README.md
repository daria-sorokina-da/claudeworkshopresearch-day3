# Royal Stables — Claude Code Workshop for Researchers

**The Day 3 lab repository.** A deliberately half-finished Python + SQL project about a
fairy-tale horse stable.

> **Self-contained.** Fork it, work through [EXERCISE.md](EXERCISE.md), done. You need
> nothing from any earlier session.

## How the lab runs

**Part 0** (setup), then **eleven exercises numbered 3–13** — the slides number exercises
across the whole workshop and 1–2 ran on Day 2. Six are marked *backbone*.

The toolkit is Exercise 4 rather than a late-afternoon extra on purpose: the test hook, the
`/review` command and the `deny` rules only prove themselves against real changes, and
Exercises 5–7 are real changes that put them to work. A five-minute step after Exercise 7
sends you back to revise the toolkit from what actually happened.

## What shape it is

Structurally it is the same shape as your work: a relational schema with integrity
problems, messy measurement data, a CLI, a pipeline, a monitoring service, a legacy
script, a small classifier, and some repetitive front-end code.

**There is no real data in this repository.** Everything is invented.

## ⛔ One directory is off limits

`src/suitability_secret_algorithm/` — the race-suitability scorer. Claude must not modify it. This is
enforced by `deny` rules in `.claude/settings.json` and by a `PreToolUse` hook, not
by asking nicely. It stands in for any code of yours whose correctness rests on a
rationale that isn't written in the file — matching logic, a validated method, a
threshold from a standard. See
[`src/suitability_secret_algorithm/README.md`](src/suitability_secret_algorithm/README.md) for why, and Exercise 4.4 of
[EXERCISE.md](EXERCISE.md) for the step that proves it works.

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

Then onboard the repo — run `/init` in a Claude session and **correct the draft by hand**.
Exercise 3 of [EXERCISE.md](EXERCISE.md) walks through it and is worth the half hour: every
later prompt inherits that file.

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

**The [GitHub CLI](https://cli.github.com) is needed for Exercise 5**, the ticket exercise
— `gh --version` to check. Do this before the session if you can:

```bash
gh auth login
```

Then, **from inside your clone**, two fork defaults that need changing:

```bash
gh repo set-default <your-username>/claudeworkshopresearch-day3   # forks ambiguate with upstream
gh repo edit --enable-issues                                      # forks disable issues
```

Exercise 5 has a documented web-UI fallback if `gh` won't cooperate, and no other exercise
needs it.

## What's in here

| Path | What it is | Exercise |
|---|---|---|
| `src/suitability_secret_algorithm/` | ⛔ Off limits | 4 — proving the red line |
| `data/race_results.csv`, `data/measurements.csv` | Deliberately messy datasets | 4 — published skill · self-practice EDA |
| *(GitHub, not the repo)* | An issue you file yourself | 5 — ticket-driven work |
| `specs/stable_ledger.md` | A spec with no implementation | 6 — spec- and test-driven build |
| `sql/schema.sql`, `sql/seed.sql` | Under-constrained schema, data with planted violations | 7 — SQL data-quality checks |
| `src/stable_cli/` | CLI over the database. Contains one planted bug | 8 — off-by-one bug hunt |
| `legacy/stable_ledger.pl` | Real-flavoured legacy Perl, plus fixtures | 9 — Perl → Python |
| `web/` | Static yard board with repetitive JS and CSS | 10 — unfamiliar technologies |
| `analysis/slow_aggregate.py` | Correct and needlessly slow | 11 — sub-agent chain |
| `src/pipeline/` | Four stages, not idempotent, not atomic | 12 — pipelines |
| `src/monitor/` | Directory watcher with the five classic bugs | 12 — monitoring |
| `src/ml/` | A classifier that reports 1.000 accuracy and is worthless | 13 — a little ML |

## A note on the planted bugs

Every bug in here is intentional and is *not* marked in the code. `pytest` passes on a
fresh clone — the existing suite is green despite a real bug in the reporting code,
which is the ordinary way bugs survive a test suite.

Please don't read the bug list in EXERCISE.md before you have gone looking.

## The five red lines

1. Never let it modify code where a plausible-looking diff isn't the same as a correct one — where correctness depends on something outside the file, like a validated method or a standard's threshold. Here, that's `src/suitability_secret_algorithm/`, a race-suitability scorer whose weights each encode a defended clinical judgement (see `src/suitability_secret_algorithm/RATIONALE.md`).
2. Never trust an unchecked statistic — keep the code as well as the number.
3. Never paste secrets or sensitive data into a prompt.
4. Never use `--dangerously-skip-permissions` on a real repo.
5. Always read the diff before accepting it.

## Licence

CC BY 4.0 — see [LICENSE.md](LICENSE.md).
