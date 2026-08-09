# The Royal Stables Lab — Day 3

**~4 hours, plus a retrospective.** You drive. Work individually or in pairs.

> **This repo is self-contained.** Fork it, work through it, done. You do not need
> anything from Day 2 — not a file, not a clone, not the session. If you were there,
> nothing you did is wasted; you'll just move through Part 0 faster.

---

## What today covers

Eight exercises. Two more ran on Day 2 under the slides' workshop-wide numbering; nothing
here depends on them.

| | Contents | |
|---|---|---|
| [**Part 0**](#part-0--setup-and-ground-rules-15-min--backbone) | Fork, clone, branch, install, ground rules | backbone |
| [**Exercise 1**](#exercise-1--onboard-and-harness-the-repo-12-min--backbone) | Onboard and harness the repo — `/init`, a summary with its sources, `CLAUDE.md`, MCP | backbone |
| [**Exercise 2**](#exercise-2--build-your-team-toolkit-30-min--backbone) | Build your team toolkit — skill, `/review` command, test hook, `deny` rules | backbone |
| [**Exercise 3**](#exercise-3--tickets-read-one-then-fix-it-23-min--backbone) | Tickets — read one, fix it, comment back | backbone |
| [**Exercise 4**](#exercise-4--spec--and-test-driven-build-30-min--backbone) | Spec- and test-driven build | backbone |
| [**Exercise 5**](#exercise-5--orchestrate-sub-agents-25-min--backbone) | Orchestrate sub-agents | backbone |
| [**Exercise 6**](#exercise-6--sql-data-quality-checks-20-min--backbone) | SQL data-quality checks | backbone |
| [**Exercise 7**](#exercise-7--perl--python-conversion-30-min--if-time) | Perl → Python conversion | if time |
| [**Exercise 8**](#exercise-8--unfamiliar-technologies-cssjs-28-min--if-time) | Unfamiliar technologies — CSS/JS | if time |

**The order is deliberate: onboard the repo, set up the guardrails, then do real work
with both running.** Sub-agents come after that, because they are worth very little until
there is a toolkit for them to inherit.

---

## Part 0 — Setup and ground rules (15 min) · backbone

```bash
# 1. Fork this repo on GitHub, then clone YOUR fork
git clone <your fork>
cd claudeworkshopresearch-day3

# 2. Branch, so your work never touches the original
git switch -c stables-workshop

# 3. Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# 4. Build the database and confirm the suite is green
python -m src.stable_cli.cli build
pytest
```

You should see **36 passed**. If you don't, raise your hand.

Try the CLI. `stable-cli` is the app this whole lab sits on top of — a thin command-line
front end over the SQLite database, four subcommands:

- `build` — (re)creates `stables.db` from `sql/schema.sql` and `sql/seed.sql`. You already
  ran this once above; safe to re-run any time you want a clean slate.
- `stables` — a summary per stable.
- `week <date>` — every race in the week containing that date. This is the report you'll
  put a ticket against in Exercise 3.
- `horse <id>` — every entry for one horse.

```bash
python -m src.stable_cli.cli stables
python -m src.stable_cli.cli week 2026-03-16
python -m src.stable_cli.cli horse 1
```

### The five red lines

Read them in [README.md](README.md#the-five-red-lines) — every exercise today touches at
least one, and later steps refer to them by number. Exercise 2 turns lines 1 and 3 into
mechanisms; the other three stay your job.

### Commit convention

`type: #ISSUE-NUMBER: Description` — e.g. `fix: #12: correct inclusive date range`, where
`12` is the real GitHub issue number. Drop it when there's no ticket behind the commit,
e.g. `chore: add team toolkit`.
Commit at every milestone. Git is the safety net that makes delegating safe; `git stash`
and `git checkout .` are your undo button when a prompt goes sideways.

**The issue number is not decoration.** Exercise 3 sets up the board that number points at.

See the cheatsheet for [commands and keyboard shortcuts](CHEATSHEET.md#commands-and-keyboard-shortcuts-worth-having-to-hand)
and the [`/btw` side-note trick](CHEATSHEET.md#mid-task-side-notes).

---

## Exercise 1 — Onboard and harness the repo (12 min) · backbone

**Do this before anything else. It changes the quality of every later prompt.**
`CLAUDE.md` loads into every session and survives `/clear`; the conversation does not.

### 1.1 — Get oriented, with a reading list (7 min)

Open Claude Code (`claude`) in the repo. Generate a first draft of the context file:

```
/init
```

Then **read `CLAUDE.md`**. It is a draft written by something that has just met this
codebase, not a statement of fact.

Here's a habit worth building early, because it makes every summary more useful, not
just more trustworthy: ask for the file list along with the summary. You get two things
for the price of one — the answer, and a map of exactly where in the codebase to look
next:

> Summarise what this repo does in 5 bullets. Then list the files you read to
> reach that summary.

✅ **Acceptance:** you get a summary *and* a file list. Now every claim in the summary
has an address — if one bullet matters to you, you already know which file to open.

Correct anything wrong in `CLAUDE.md` by hand, then commit it — every later exercise
inherits this file:

```bash
git add CLAUDE.md && git commit -m "docs: repo context for the lab"
```

### 1.2 — Wire up the database MCP (5 min)

MCP (Model Context Protocol) is how Claude reaches tools that aren't the filesystem or
the shell. This repo ships a **committed `.mcp.json`** pointing a SQLite MCP server at
`stables.db` — so on a fresh clone, every teammate gets schema-aware querying with no
setup. That's the same wiring you would point at Oracle or BigQuery; only the server and
the credential change.

```bash
python -m src.stable_cli.cli build   # if stables.db isn't there yet
claude
```

Then in the session:

```
/mcp
```

You should see `stables-db` connected. Put it to work on something you'll need in
Exercise 6:

> Using the stables-db MCP, produce a Mermaid ER diagram of the schema — every table
> and its foreign-key relationships. Save it to diagrams/schema.md.

✅ **Acceptance:** `/mcp` shows `stables-db` connected, Claude reads the schema directly
through it instead of shelling out to inspect it, and `diagrams/schema.md` renders a
diagram you can check against `sql/schema.sql` — architecture documentation earned for
free, straight from the code.

**If it doesn't start**, carry on without it. `uvx` needs `uv` installed, and MCP package
names move around. Claude has `Bash` and can write Python, so every exercise below works
either way — the MCP is convenience, not a dependency.

> See [MCP configuration patterns](CHEATSHEET.md#mcp-configuration-patterns) in the
> cheatsheet for the three ways this gets wired up, and
> [Context management](CHEATSHEET.md#context-management) for when to check your usage.

---

## Exercise 2 — Build your team toolkit (30 min) · backbone

A fresh Claude session doesn't know your review standards, your test conventions, or
which paths are off-limits — you'd have to state them again every time, and so would
every teammate on their own clone. A skill, a command, a hook, and a `deny` rule put
those standards in the repo itself, so they apply automatically to anyone who clones it.

Build it **before** the work, not after: the hook and the command only prove themselves
against real changes, and Exercises 3–6 are ninety minutes of real changes. By the end of
today the hook will have run dozens of times without you asking.

### 2.1 — A skill (11 min)

A **skill** is on-demand context Claude loads *only when it's relevant* — cheaper than
`CLAUDE.md`, which loads every single session. `CLAUDE.md` is for what's always true; a
skill is for a recipe you follow occasionally.

**Turn something you just did into something you never have to ask for again.** In
Exercise 1.2 you asked Claude to produce a Mermaid ER diagram of the schema and save it to
`diagrams/schema.md`. Codify that recipe so next time you don't have to spell it out:

```
Create a skill that should load automatically whenever I ask you to document or
diagram a database schema. It should capture this recipe:
- read the schema (via the stables-db MCP if it's connected, otherwise sql/schema.sql);
- produce a Mermaid ER diagram covering every table and its foreign-key relationships;
- save it to diagrams/schema.md.
Keep it tight.
```

✅ **Acceptance:** the skill exists, and you've read through it. Try
`Document the schema again` in a fresh turn and watch it fire without you repeating the
recipe.

**You don't have to write every skill.** They install like packages
([plugin docs](https://code.claude.com/docs/en/discover-plugins); Anthropic's catalogue is
[anthropics/skills](https://github.com/anthropics/skills)):

```
/plugin marketplace add anthropics/skills
/plugin            # browse, then install one — xlsx is a good fit here
```

Then point it at the deliberately messy data:

```
Using the xlsx skill, profile data/race_results.csv into a spreadsheet: one sheet of
the raw rows, one sheet listing every suspect value and why it's suspect. Don't clean
anything yet.
```

✅ **Acceptance:** a skill you didn't write is installed and produces something real.
(Needs network; if the marketplace path differs, browse `/plugin`.)

### 2.2 — A review slash command (7 min)

A slash command is a workflow *you* trigger deliberately. Rule of thumb: **if you expect
to run the same prompt twice, codify it.** Ask Claude to create one:

```
Create a /review slash command. It should run pytest and report pass/fail, then check
the current diff against these standards:
- Assumptions stated explicitly, not implied
- No hard-coded paths, credentials, or magic numbers
- Any statistic or figure traceable to a script in the repo
- Tests cover the error cases, not just the happy path
- Nothing under src/suitability_secret_algorithm/ touched
Running the tests is fine; it should not modify any files.
```

✅ **Acceptance:** `/review` runs your standardised review on demand. **Run it at the end of
every exercise from here on.**

### 2.3 — A verification hook (6 min)

A **hook** is a command the harness runs around a tool call, whether or not Claude wants it
to. Ask Claude to set one up:

```
Add a PostToolUse hook that runs `pytest -q` after every Write or Edit.
```

Restart Claude Code so it reloads settings. Then ask Claude to plant a real bug — in the
code, not the test:

```
In build_in_memory() in src/stable_cli/db.py, change
    conn = sqlite3.connect(":memory:")
to
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
Don't touch anything else.
```

That switches every in-memory connection in the process to a shared cache, so two
separate `build_in_memory()` calls stop being independent databases — it breaks
`test_build_in_memory_is_isolated` specifically, while the other three tests in
`tests/test_db.py` stay green.

The edit itself triggers the hook — `pytest` runs immediately and comes back red, before
you've asked for anything else. Watch Claude get that failure as feedback on the very
change it just made, then ask it to revert `db.py`.

✅ **Acceptance:** the suite runs right after the edit, unasked, and the failure reaches
Claude as feedback rather than reaching you as a surprise later.

> In Exercise 4 you'll be deliberately red for ten minutes while the tests wait for an
> implementation, so the hook will be noisy there. Narrow the matcher or comment it out
> if it gets in the way.

### 2.4 — Prove the `deny` rules — the important one (6 min)

`.claude/settings.json` already denies writes to `src/suitability_secret_algorithm/`. **Try to break it —
now, before you have any real reason to touch it.**

```
Read src/suitability_secret_algorithm/suitability.py and suggest improvements to the weights.
```
→ Reading and suggesting is allowed. Fine.

```
Apply those improvements to src/suitability_secret_algorithm/suitability.py.
```
→ **Blocked.** Both by the `deny` rule and by the `PreToolUse` hook, which explains why.
Two mechanisms on purpose: defence in depth.

```
Read the .env file and tell me the API token.
```
→ **Denied.** The tool call fails; this is not the model choosing to behave.

**This is red line 1 becoming a mechanism instead of a promise.** A guardrail you have
watched fail closed is a guardrail you trust. Note the difference you just saw twice: a
**permission** stops the action before it happens; a **hook** runs a check around it and
can explain itself.

### Take these home

Four small files — a skill, a command, a hook, a `deny` list. Commit them now, then go
and use them.

```bash
git add .claude && git commit -m "chore: add team toolkit — skill, review command, test hook"
```

---

> **Exercises 3–6 are the work.** Every one of them is a task where **verification is
> cheap**: a test, a query you can check, a diff you can read. That is not a coincidence;
> it's the criterion for where to start on your own work.
>
> **And the toolkit is live now.** The hook runs on every edit, `/review` is one keystroke,
> and `src/suitability_secret_algorithm/` cannot be written to no matter what you or the model decides. Notice
> how much of that you stop thinking about.

---

## Exercise 3 — Tickets: read one, then fix it (23 min) · backbone

The realistic case, end to end: read a ticket you didn't write, fix it red-test-first,
review your own diff, push, and comment back on the ticket — all without ever owning it.
That's the loop your team already lives in, with the ticket as the interface between you
and the tool instead of a chat message nobody can find again. Plain GitHub Issues — no
Projects board. A board is worth setting up when you have an ongoing stream of tickets to
triage; for one ticket, it's overhead with nothing to show for it.

### 3.1 — Read an existing ticket (5 min)

Someone already filed a real bug against this repo:
[issue #1](https://github.com/daria-sorokina-da/claudeworkshopresearch-day3/issues/1).
Open it and read it — no `gh` setup needed for that, this is just a public issue.

`/clear` first — this is the honest test: a fresh session that knows nothing but
`CLAUDE.md` and what the ticket says.

> Read https://github.com/daria-sorokina-da/claudeworkshopresearch-day3/issues/1.
> Restate the acceptance criteria in your own words, tell me which files you'd need to
> touch, and list anything the ticket doesn't tell you that you'd need to know. Do not
> write any code.

✅ **Acceptance:** Claude restates the criteria correctly and names the right file
(`src/stable_cli/reports.py`) without you pointing at it. **This is the payoff of a good
ticket** — a stated observation, a stated expectation, a stated definition of done. You're
about to fix exactly this bug, so keep the acceptance criteria in mind.

> **The ticket stays on the shared source repo the whole time — you're only ever reading
> or commenting on it.** Everything else (the fix, the commits, the push) happens in
> your own fork, under your own GitHub account. Nothing you do lands on
> anyone else's repo, so break it freely.

### 3.2 — Fix it, red test first (12 min)

**Same session as 3.1 — don't `/clear`.** Claude already restated the acceptance criteria
and named the file. Now it executes that plan instead of starting cold. Stay on
`stables-workshop`.

**Red test first. This one is not negotiable.**

1. **Reproduce before fixing:**
   > Now implement the plan you just gave me, starting with a failing test that
   > demonstrates the bug. Do not fix it yet.

2. **Watch it fail** — your hook will tell you before you ask. A test that doesn't fail
   first proves nothing.

3. **Get the diagnosis before the fix:**
   > What exactly is wrong — the comparison operator, the range construction, or a
   > date-versus-datetime mismatch? Quote the line.

4. **Fix it. Watch green. Read the diff.**

5. **The follow-up that earns its keep:**
   > Are there other date or range comparisons anywhere in the codebase with this same
   > bug pattern? List them. Don't change anything yet.

   One planted bug is usually a habit, not an accident. This is where the tool genuinely
   beats human reading speed.

**Commit it** — test and fix together.

### 3.3 — Review, push, and comment on the ticket (6 min)

`/review`, then push:

```bash
git push -u origin stables-workshop
```

**Comment on the ticket — don't try to close it.** You don't have write access to
`daria-sorokina-da/claudeworkshopresearch-day3`, so a closing keyword (`Closes #1`) would
do nothing there — and that's the realistic case: most bugs you fix were filed by someone
else, and closing isn't your call. Commenting is, though — it's a public repo, so this
works without write access, just a working `gh` login (`gh --version && gh auth status`
if you haven't checked). Ask Claude to do it:

> Using the gh CLI, comment on
> https://github.com/daria-sorokina-da/claudeworkshopresearch-day3/issues/1 summarising
> the fix: what was wrong, the corrected line, and a link to your commit. Show me the
> command before you run it.

**No `gh`, or not logged in?** Don't bother — nothing later depends on this comment
existing. Skip it and move on.

---

## Exercise 4 — Spec- and test-driven build (30 min) · backbone

Read [specs/stable_ledger.md](specs/stable_ledger.md).

### 4.1 — Argue with the spec first (5 min)

The spec contains **at least one genuine ambiguity** (it's flagged in the worked example).
Find it and decide what the answer should be. Edit the spec.

An ambiguous spec produces confidently wrong code, and no amount of good prompting fixes
that. This step is not a warm-up.

### 4.2 — Tests first, from the spec (10 min)

> Read specs/stable_ledger.md. Write pytest tests in tests/test_feed_ledger.py
> covering every stated behaviour including the error cases. Do not write the
> implementation. Where the spec is ambiguous, write the test you believe is right
> and add a comment flagging the ambiguity.

Your test hook from 2.3 will now report a red suite on every edit — correctly, because
there is no implementation yet. **This is the one place today where red is the goal.**

### 4.3 — Review the tests properly (10 min)

**This is the actual work of the exercise.** For each test ask: does this test the *spec*,
or does it test what was easy to test? Look specifically for:

- Are the error cases really covered, or just the happy path?
- Does anything test the duplicate rule, including the line-number in the message?
- Unit normalisation — is `lb` → kg actually checked with a real number?
- Is `TypeError` on bad *arguments* distinguished from an error entry on bad *data*?

**Fix whatever you find wrong now, before implementing anything.** If a test is weak or
tests the wrong thing, that's on you to correct here — not something to leave for Claude
to discover and second-guess mid-implementation.

### 4.4 — Then implement (5 min)

> Now implement feed_ledger.py to pass these tests and match the spec.

Watch red → green. Then `/review`, read the diff, commit.

---

## Exercise 5 — Orchestrate sub-agents (25 min) · backbone

A **sub-agent** is an independent work stream with its own context window and its own
scoped tools — which is exactly why it is not the same as asking one session to do three
things. They come after the toolkit because they inherit everything you've built: your
`CLAUDE.md`, your skill, your `deny` rules. An agent on an unharnessed repo is just a
faster way to make a mess.

### 5.1 — Three reviewers in parallel (15 min)

Review one change from three angles, each with its own context so they can't influence each
other. **The standards go in the agents, not in the command** — an agent is the reusable
unit, so each reviewer should carry the standards it's responsible for:

```
Create three subagents. Give each one the model and effort that fits the work:

- correctness-reviewer (model: opus, effort: high): checks a diff against the spec,
  including edge cases. Also checks that assumptions are stated rather than implied,
  that any statistic is traceable to a script in the repo, and that nothing under
  src/suitability_secret_algorithm/ has been touched. Read and Grep only.
- tests-reviewer (model: sonnet, effort: medium): runs pytest, reports what fails, and
  checks whether the tests cover the changed code — the error paths, not just the happy
  path. Read and Bash.
- style-reviewer (model: haiku, effort: low): checks conventions against CLAUDE.md and
  flags hard-coded paths, credentials or magic numbers. Read only.
```

Open one of the files it writes under `.claude/agents/` — `model:` and `effort:` sit in the
frontmatter alongside `tools:`. **Judging the work before you pick the tier is the point:**
spec-versus-diff reasoning is genuinely hard, checking naming is not, and paying Opus rates
for the second is how agent fleets get expensive.

Then upgrade `/review` — the command you wrote in 2.2 — to fan out across all three
instead of doing one pass itself. It only has to orchestrate now; the standards already
live in the agents:

```
Rewrite my /review command. Instead of a single pass, it should review the diff on the
current branch using the correctness, tests and style reviewers in parallel, then
summarise where they agree and — more usefully — where they disagree.
```

Run it on the diff from Exercise 4:

```
/review
```

✅ **Acceptance:** three reviewers run on one diff, and you get a summary that names the
disagreements rather than averaging them away.

**Why three agents rather than one prompt asking for three things:** separate contexts don't
contaminate each other. A single agent that has just concluded the code is correct is
measurably softer on the question of whether it's actually tested. **The disagreements are
the signal.**

**What you just traded.** The 2.2 version was one deterministic pass you could read and
edit. This one is three independent passes you can't fully predict — better at catching what
you didn't think to check, and three times the tokens. Not three times the price, though:
that's what the tiering bought you. `/cost` shows what the session actually spent.

### 5.2 — A sequential chain (10 min · optional)

Parallel is right when the tasks are independent. When each step needs the previous one's
*output*, you want a chain. `analysis/slow_aggregate.py` is correct and needlessly slow —
and the obvious culprit isn't the expensive one, so the profiling genuinely has to happen
before the fix.

Ask Claude to create two more agents:

```
Create two subagents, again with the model and effort that fit:
- profiler (model: sonnet, effort: low): profiles a script and reports where the time
  actually goes, nothing else. Read and Bash.
- optimiser (model: opus, effort: high): makes the smallest change that removes a named
  hotspot, preserving output exactly. Read and Edit.
```

Measuring is cheap; changing working code without breaking it isn't. That asymmetry is
why the tiers differ.

The order is the whole point, so put it in a skill rather than retyping it — orchestration
lives in a skill, a command or your prompt, never in the agent files themselves:

```
Create a skill that should load automatically whenever I ask to speed up, optimise or
profile code. It should capture this recipe:
- profile first with the profiler agent, and show me the numbers before anything changes;
- give the optimiser agent only the hotspot the profile actually named — never a guess;
- confirm the output is byte-identical afterwards;
- then run the correctness-reviewer agent on the diff.
Keep it tight.
```

Now the short version does all of it:

> Speed up analysis/slow_aggregate.py.

✅ **Acceptance:** the profile arrives before the edit, the edit targets what the profile
found rather than what looks slow, and the output is byte-identical. If the optimiser
"improved" something the profiler never mentioned, you've just watched the failure mode that
makes unsupervised chains expensive.

---
## Exercise 6 — SQL data-quality checks (20 min) · backbone

`sql/schema.sql` is deliberately under-constrained — no `UNIQUE` on `registration_no`, no
`REFERENCES` clauses — and `sql/seed.sql` loaded rows that exploit the gaps.

**Your job: find the bad rows, then decide what should have stopped them.** The
`stables-db` MCP from 1.2 queries the database for you.

### 6.1 — Codify the method as a skill (6 min)

Write the skill before you need it:

```
Create a skill that should load automatically whenever I ask for validation or
data-quality queries. It should capture this recipe:
- list the constraints the schema SHOULD enforce but doesn't, BEFORE writing any SQL;
- one query per constraint, nothing bundled;
- save each to sql/checks/NN_description.sql with a comment naming the constraint and
  saying what a non-empty result means;
- state for each whether it should also become a database constraint, and note that
  adding one to a table that already violates it will fail.
Keep it tight.
```

✅ **Acceptance:** the skill exists, and you've read through it.

### 6.2 — Find the bad rows (8 min)

**Ask the short version — the skill should carry the rest:**

> Write validation queries for sql/schema.sql.

✅ **Watch for this:** you didn't say to list constraints before writing SQL, save each
query to `sql/checks/NN_*.sql`, comment what a non-empty result means, or say whether each
should be a constraint — and it should do all four anyway, because your skill loaded.
**If it didn't, that's the lesson**: check the `description` line in your `SKILL.md`,
because a skill that doesn't trigger is a skill that doesn't exist.

**Then run them:**

> Run each query in sql/checks/ against stables.db and show me which ones returned rows.

✅ **Acceptance:** you know which checks found violations. Open the ones that came back
empty and check the joins — empty means clean data *or* a broken query.

<details>
<summary><strong>Spoiler — the planted problem classes. Don't open until you've looked.</strong></summary>

1. **Orphan foreign keys** — entries referencing a non-existent horse, race and rider; a
   vet visit for a non-existent horse; a horse in a non-existent stable.
2. **Duplicate registration numbers** — two separate pairs, plus one horse with none.
3. **Impossible dates** — a horse retired before it was born.
4. **Temporal contradictions** — a vet visit before the horse's foaling date; a visit after
   retirement; a retired horse entered in a later race.
5. **Contradictory flags** — `placed` disagreeing with `finish_position`, in both
   directions.
</details>

### 6.3 — Optimise one (3 min)

Your orphan-foreign-key checks join two tables on a column that has no index. SQLite
answers those by reading every row of the table — a full scan. On this database's handful
of rows that's instant; on a table with millions of rows it's slow, and adding an index is
usually the one-line fix.

`EXPLAIN QUERY PLAN` prefixed to a query prints the strategy instead of the results:

> Run EXPLAIN QUERY PLAN on one of the orphan-foreign-key checks in sql/checks/. Show me
> the output, tell me which table is being scanned rather than searched, and give me the
> CREATE INDEX that would fix it.

✅ **Acceptance:** you can point at `SCAN <table>` in the output and name the index that
turns it into a `SEARCH`.

### 6.4 — Constraint or query? (3 min)

Two different fixes, doing two different jobs:

- A **constraint** (`UNIQUE`, `REFERENCES`, `CHECK`) makes the database reject bad rows
  from now on. It does nothing about the rows already there.
- A **validation query** finds the rows already there. It does nothing to stop new ones.

Most problems want both — but not in either order. `CREATE UNIQUE INDEX` on a table that
already contains duplicates fails, so it has to be: run the query, clean up what it found,
*then* add the constraint.

> For each check in sql/checks/, tell me whether the schema should enforce it as a
> constraint too, and write the ALTER TABLE or CREATE INDEX that would do it. Don't run
> them.

**The bit Claude can't decide for you** is the cleanup in the middle: delete one of the
duplicates, merge them, or go and ask whoever owns the data? Until you answer that, the
constraint won't apply.

**Portability note:** the exercises are SQLite, and deliberately avoid dialect-specific
syntax. Where Oracle or BigQuery would differ materially — window function syntax, date
arithmetic — ask Claude for both. Context7 is what fills the other gap: current,
version-specific dialect docs.

`/review`, then commit `sql/checks/`.

---

## Exercise 7 — Perl → Python conversion (30 min) · if time

Your named legacy-migration case. The file is `legacy/stable_ledger.pl` — 2009 vintage,
edited by six people, comments intermittently updated.

```bash
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_01.txt
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_02.txt
```

### 7.1 — Understand it (10 min)

> Explain what this script does, section by section. Identify anything relying on
> Perl-specific behaviour that won't translate directly to Python.

That last clause is where the value is: implicit `$_`, the aliasing `for` loop that mutates
`@f` in place, list-vs-scalar context, regex flag differences, string-vs-numeric comparison,
`sort` defaulting to string order.

### 7.2 — Characterise the current behaviour (5 min)

**This is the legitimate use of source-derived tests.** The Perl script *is* the
specification here, bugs included, because "same output" is the requirement.

> Run the Perl script against both fixtures and capture the exact output. Write those
> as expected-output fixtures we can use to verify the port.

### 7.3 — Port it (10 min)

> Port this to legacy/stable_ledger.py. Idiomatic Python, not transliterated Perl.
> Identical output for both fixtures. Flag anywhere you had to make a judgement call.

### 7.4 — Verify, then separate the fix (5 min)

**Actually run both and diff the output.** Don't take its word.

Then: the Perl has a known bug nobody ever fixed —
[issue #2](https://github.com/daria-sorokina-da/claudeworkshopresearch-day3/issues/2).
Run it and look at the `TOTAL` row against the `ENTRIES` column header; the comment at that
line points at the ticket. Nothing to do with issue #1 from Exercise 3.

While you're in there, read the comment above `$TOTALS{$reg} += $kg;` and check it against
what the code does. Inherited comments are claims, not documentation.

**Port it faithfully first. Fix it as a separate commit.** Never mix "port" and "improve" —
if you do, and something breaks, you cannot tell which change did it.

---

## Exercise 8 — Unfamiliar technologies: CSS/JS (28 min) · if time

The concrete pain you named. Open `web/index.html` in a browser — it works.

You've inherited a working front end in a language you don't write. **Don't read `app.js`
yet** — the first job is finding out what's wrong with it without being told.

### 8.1 — Set up Context7 (3 min)

Step 3 below needs it. Context7 serves current, version-specific library documentation —
the gap your model's training data can't fill on its own. It installs as a plugin:

```
/plugin marketplace add upstash/context7
/plugin install context7@context7-marketplace
```

Then check it connected — restart Claude Code first if it doesn't show up:

```
/mcp
```

✅ **Acceptance:** `/mcp` lists `context7`.

**No API key needed.** Unauthenticated requests go through an anonymous tier with lower
rate limits, which is ample for one exercise. If you do hit a limit, a free key from
[context7.com/dashboard](https://context7.com/dashboard) exported as `CONTEXT7_API_KEY`
raises it.

**If it won't install, carry on to step 4** — nothing else in the exercise depends on it.

### 8.2 — Find the problem, then fix it (25 min)

**Run the whole sequence. Don't skip to step 7.**

1. **Let it find the problem.** Say nothing about what you think is wrong:
   > Review web/app.js and web/styles.css. What would you change, and why? Rank your
   > answers by what would hurt most as this page grows. Change nothing yet.

   ✅ **Acceptance:** duplication is at or near the top of its list, and it says how many
   times the pattern repeats. If it leads with naming or formatting instead, push back
   once — *"what's the structural problem?"* — and watch what a sharper question buys you.
2. **Pin down exactly what varies**, because that's what decides whether one function can
   replace all of them:
   > For each repetition of that pattern, list precisely what differs between them —
   > every value, every string, every behaviour. Miss nothing.
3. **Pull current docs** — this file is written in an old style (`var`, index loops,
   `innerHTML`), so ask for the current idiom rather than trusting training data:
   > Use Context7 to check the current recommended DOM practice for what app.js does:
   > selecting elements, attaching listeners, and building list items. Tell me which
   > patterns in this file are outdated and what replaced them.
4. **Whole-repo model** — what this is wired to:
   > What else depends on web/app.js? List every id and class it relies on, and where
   > each one is defined in index.html and styles.css.
5. **Diagram it.** If the diagram is wrong you've caught the misunderstanding for free:
   > Diagram one stable block end to end — button click through to the rendered list,
   > including the show/hide toggle state. Save it to diagrams/yard-board.md.
6. **Persist it** to `CLAUDE.md`:
   > Add a short section to CLAUDE.md describing how web/ is wired: the id naming
   > convention linking index.html to app.js, and anything you found that doesn't
   > follow the shared pattern.
7. **Now the scoped change**, plan mode:
   > Extract the repeated pattern in app.js into a single reusable function. Change
   > behaviour nowhere — including everything you listed in step 2. Show me the diff
   > before applying.
8. **Verify visually.** Open the page and click every button:
   > List every behaviour I should check by hand in the browser to confirm the refactor
   > changed nothing — including the differences you found in step 2.

   CSS/JS needs eyes, not just a green test — and note that your test hook is silent
   here, because there is no test that covers this. **A guardrail only guards what it
   can see.**

### ⚠ The trap

**The repetitions are not actually identical.** A naive extraction silently changes
behaviour and no test will tell you — step 2 is what catches it. If Claude's extraction
drops a difference, that's the most valuable thing that happens today.

<details>
<summary><strong>Spoiler — how many differ, and how</strong></summary>

Two of the four blocks deviate. Ashcombe sorts its list; the others don't. Fairwater
uppercases its names and uses a different button label ("Hide list" rather than
"Hide horses").
</details>
