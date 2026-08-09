# The Royal Stables Lab — Day 3

**~4 hours, plus a retrospective.** You drive. Work individually or in pairs.

> **This repo is self-contained.** Fork it, work through it, done. You do not need
> anything from Day 2 — not a file, not a clone, not the session. If you were there,
> nothing you did is wasted; you'll just move through Part 0 faster.

---

## What today covers

Eleven exercises, numbered 3–13 because the slides number them across the whole
workshop and 1–2 ran on Day 2. Nothing here depends on them.

| | Contents | |
|---|---|---|
| **Part 0** | Fork, clone, branch, install, pin the red lines | 15 min |
| **Exercise 3** | Onboard and harness the repo — `/init`, a summary with its sources, diagram, `CLAUDE.md`, MCP | backbone |
| **Exercise 4** | Build your team toolkit — skill, `/review` command, test hook, `deny` rules | backbone |
| **Exercise 5** | Tickets — read one, fix it, comment back | backbone |
| **Exercise 6** | Spec- and test-driven build | backbone |
| **Exercise 7** | SQL data-quality checks | backbone |
| **Exercise 8** | Perl → Python conversion | if time |
| **Exercise 9** | Unfamiliar technologies — CSS/JS | if time |
| **Exercise 10** | Orchestrate sub-agents | backbone |
| **Exercise 11** | Pipelines and monitoring | extra |
| **Exercise 12** | A little ML | extra |
| **Exercise 13** | Claude Science and Cowork | extra |

**The order is deliberate: onboard the repo, set up the guardrails, then do real work
with both running.** Sub-agents come after that, because they are worth very little until
there is a toolkit for them to inherit.

---

## Timeline

Wall-clock assumes a 09:15 start — shift it to suit.

| Time | | Minutes |
|---|---|---|
| 09:15 | **Part 0** — Setup and ground rules | 15 |
| 09:30 | **Exercise 3** — Onboard and harness the repo | 30 |
| 10:00 | **Exercise 4** — Build your team toolkit | 30 |
| 10:30 | **Exercise 5** — Tickets | 23 |
| 10:53 | **Exercise 6** — Spec- and test-driven build | 30 |
| 11:23 | **Break** | 15 |
| 11:38 | **Exercise 7** — SQL data-quality checks | 20 |
| 11:58 | **Come back to the toolkit** — revise it | 5 |
| 12:03 | **Exercise 10** — Orchestrate sub-agents | 25 |
| 12:28 | **Wrap-up** and retrospective | 20 |
| 12:48 | **Extras** — Exercises 8 and 9 first, then 11–13 | remaining time |

---

## Part 0 — Setup and ground rules (15 min)

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
  put a ticket against in Exercise 5.
- `horse <id>` — every entry for one horse.

```bash
python -m src.stable_cli.cli stables
python -m src.stable_cli.cli week 2026-03-16
python -m src.stable_cli.cli horse 1
```

### The five red lines

The spine of the whole workshop. Every exercise today touches at least one.

1. **Never let it modify code where a plausible-looking diff isn't the same as a correct
   one** — where you can't tell right from wrong just by reading the change, because the
   correctness depends on something outside the file: a threshold set by a published
   standard, a matching algorithm validated against real data, a method someone signed
   off on. Here, that's `src/suitability_secret_algorithm/` — a horse race-suitability scorer whose
   weights (distance fit, going fit, recent form, a fitness penalty) each encode a
   specific clinical or scientific judgement, defended line-by-line in
   `src/suitability_secret_algorithm/RATIONALE.md`.
2. **Never trust an unchecked statistic** — keep the code as well as the number.
3. **Never paste secrets or sensitive data into a prompt.** Anything you put in context
   has left your environment, whatever the data policy says.
4. **Never use `--dangerously-skip-permissions` on a real repo.**
5. **Always read the diff before accepting it.** Confident-and-wrong is the main failure mode.

Exercise 4 turns lines 1 and 3 into mechanisms. The other three stay your job.

### Commit convention

`type: #ISSUE-NUMBER: Description` — e.g. `fix: #12: correct inclusive date range`, where
`12` is the real GitHub issue number. Drop it when there's no ticket behind the commit,
e.g. `chore: add team toolkit`.
Commit at every milestone. Git is the safety net that makes delegating safe; `git stash`
and `git checkout .` are your undo button when a prompt goes sideways.

**The issue number is not decoration.** Exercise 5 sets up the board that number points at.

See the cheatsheet for [commands and keyboard shortcuts](CHEATSHEET.md#commands-and-keyboard-shortcuts-worth-having-to-hand)
and the [`/btw` side-note trick](CHEATSHEET.md#mid-task-side-notes).

---

## Exercise 3 — Onboard and harness the repo (30 min) · backbone

**Do this before anything else. It changes the quality of every later prompt.**
`CLAUDE.md` loads into every session and survives `/clear`; the conversation does not.

### 3.1 — Get oriented, with a reading list (7 min)

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
Keep pairing summaries with their sources all day; it turns a paragraph into a
starting point.

### 3.2 — Diagram the data flow from the code, not the README (5 min)

> Produce a Mermaid diagram of how data moves from the raw CSVs through to the
> final report. Base it only on the code. Save it to diagrams/data-flow.md.

Open the file in a Markdown preview — the diagram renders. Architecture docs for free,
straight from the code — and worth committing, since `diagrams/` isn't scratch space,
it's documentation the next person benefits from too.

### 3.3 — Plan mode: look before you leap (5 min)

```
/plan

I want this repo to be easier for a new researcher to find their way around.
What should go in CLAUDE.md? Just propose it — don't write anything yet.
```

Steer the plan in plain language before approving — *"stick to the schema, the test
command and the conventions; keep it short and factual."* This separates **thinking
from doing**, and it is the cheapest place to catch a wrong assumption.

> **Where do plan files go?** By default, `~/.claude/plans/` — one global folder shared
> across every repo you work in. This repo overrides that with `"plansDirectory": ".temp"`
> in `.claude/settings.json`, so plans land in `.temp/` here instead — gitignored, so
> they never get committed. See [Plan mode](CHEATSHEET.md#plan-mode) in the cheatsheet
> for more on that setting.

### 3.4 — Make the context permanent in CLAUDE.md (8 min)

**Prove it loads** with the question any actual newcomer asks on day one:

```
/clear

Without reading or searching any files: what's our commit message convention here?
```

✅ **Acceptance:** Claude answers instantly, with no tool calls, and gives you
`type: #ISSUE-NUMBER: Description` (from Part 0) — not a generic guess like "conventional
commits." That's the actual proof: the answer was already sitting in context from
`CLAUDE.md`, not fetched by a fresh scan of the repo, and it's specific enough that
Claude couldn't have pattern-matched its way to it. If it reaches for `Read` or `Grep`
before answering, or gives you something generic instead, that's a real gap — go add
the convention to `CLAUDE.md` by hand.

`CLAUDE.md` reloads automatically after `/clear`. You wrote it once; every future
session and every teammate on a fresh clone inherits it.

```bash
git add CLAUDE.md && git commit -m "docs: repo context for the lab"
```

### 3.5 — Wire up the database MCP (5 min)

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
Exercise 7:

> Using the stables-db MCP, produce a Mermaid ER diagram of the schema — every table
> and its foreign-key relationships. Save it to diagrams/schema.md.

✅ **Acceptance:** `/mcp` shows `stables-db` connected, Claude reads the schema directly
through it instead of shelling out to inspect it, and `diagrams/schema.md` renders a
diagram you can check against `sql/schema.sql` — another piece of architecture
documentation earned for free, alongside the data-flow diagram from 3.2.

**If it doesn't start**, carry on without it. `uvx` needs `uv` installed, and MCP package
names move around. Claude has `Bash` and can write Python, so every exercise below works
either way — the MCP is convenience, not a dependency.

> See [MCP configuration patterns](CHEATSHEET.md#mcp-configuration-patterns) in the
> cheatsheet for the three ways this gets wired up, and
> [Context management](CHEATSHEET.md#context-management) for when to check your usage.

---

## Exercise 4 — Build your team toolkit (30 min) · backbone

A fresh Claude session doesn't know your review standards, your test conventions, or
which paths are off-limits — you'd have to state them again every time, and so would
every teammate on their own clone. A skill, a command, a hook, and a `deny` rule put
those standards in the repo itself, so they apply automatically to anyone who clones it.

Build it **before** the work, not after: the hook and the command only prove themselves
against real changes, and Exercises 5–8 are ninety minutes of real changes. By the end of
today the hook will have run dozens of times without you asking.

### 4.1 — A skill (11 min)

A **skill** is on-demand context Claude loads *only when it's relevant* — cheaper than
`CLAUDE.md`, which loads every single session. `CLAUDE.md` is for what's always true; a
skill is for a recipe you follow occasionally.

**Turn something you just did into something you never have to ask for again.** In
Exercise 3.5 you asked Claude to produce a Mermaid ER diagram of the schema and save it to
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

### 4.2 — A review slash command (7 min)

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

### 4.3 — A verification hook (6 min)

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

> In Exercise 6 you'll be deliberately red for ten minutes while the tests wait for an
> implementation, so the hook will be noisy there. Narrow the matcher or comment it out
> if it gets in the way.

### 4.4 — Prove the `deny` rules — the important one (6 min)

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

> **Exercises 5–8 are the work.** Every one of them is a task where **verification is
> cheap**: a test, a query you can check, a diff you can read. That is not a coincidence;
> it's the criterion for where to start on your own work.
>
> **And the toolkit is live now.** The hook runs on every edit, `/review` is one keystroke,
> and `src/suitability_secret_algorithm/` cannot be written to no matter what you or the model decides. Notice
> how much of that you stop thinking about.

---

## Exercise 5 — Tickets: read one, then fix it (23 min) · backbone

The realistic case, end to end: read a ticket you didn't write, fix it red-test-first,
review your own diff, push, and comment back on the ticket — all without ever owning it.
That's the loop your team already lives in, with the ticket as the interface between you
and the tool instead of a chat message nobody can find again. Plain GitHub Issues — no
Projects board. A board is worth setting up when you have an ongoing stream of tickets to
triage; for one ticket, it's overhead with nothing to show for it.

### 5.1 — Read an existing ticket (5 min)

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

### 5.2 — Fix it, red test first (12 min)

**Same session as 5.1 — don't `/clear`.** Claude already restated the acceptance criteria
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

### 5.3 — Review, push, and comment on the ticket (6 min)

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

## Exercise 6 — Spec- and test-driven build (30 min) · backbone

Read [specs/stable_ledger.md](specs/stable_ledger.md).

### 6.1 — Argue with the spec first (5 min)

The spec contains **at least one genuine ambiguity** (it's flagged in the worked example).
Find it and decide what the answer should be. Edit the spec.

An ambiguous spec produces confidently wrong code, and no amount of good prompting fixes
that. This step is not a warm-up.

### 6.2 — Tests first, from the spec (10 min)

> Read specs/stable_ledger.md. Write pytest tests in tests/test_feed_ledger.py
> covering every stated behaviour including the error cases. Do not write the
> implementation. Where the spec is ambiguous, write the test you believe is right
> and add a comment flagging the ambiguity.

Your test hook from 4.3 will now report a red suite on every edit — correctly, because
there is no implementation yet. **This is the one place today where red is the goal.**

### 6.3 — Review the tests properly (10 min)

**This is the actual work of the exercise.** For each test ask: does this test the *spec*,
or does it test what was easy to test? Look specifically for:

- Are the error cases really covered, or just the happy path?
- Does anything test the duplicate rule, including the line-number in the message?
- Unit normalisation — is `lb` → kg actually checked with a real number?
- Is `TypeError` on bad *arguments* distinguished from an error entry on bad *data*?

**Fix whatever you find wrong now, before implementing anything.** If a test is weak or
tests the wrong thing, that's on you to correct here — not something to leave for Claude
to discover and second-guess mid-implementation.

### 6.4 — Then implement (5 min)

> Now implement feed_ledger.py to pass these tests and match the spec.

Watch red → green. Then `/review`, read the diff, commit.

---

## ☕ Break — 15 minutes

---

## Exercise 7 — SQL data-quality checks (20 min) · backbone

The same mechanics you'd use on any real relational dataset with integrity problems, just
a different domain. The `stables-db` MCP from 3.5 does some of the work for you; the rest
is a recipe worth codifying before you run it, not after.

### 7.1 — Write the recipe, then use it (12 min)

**Write the skill first.** You're about to write SQL data-quality checks on this
database — the same kind of integrity checking you'd run on any real relational dataset
with messy, incomplete records. Codify the method now, so the skill does the remembering
instead of you:

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

**Ask for the list before the queries:**

> Here is sql/schema.sql. Before writing any SQL, list the integrity constraints this
> schema should enforce but doesn't. Then write one validation query per constraint.
> Return the queries only — don't run them yet.

✅ **Watch for this:** you didn't tell it to save each query to `sql/checks/NN_*.sql`, or to
comment what a non-empty result means, or to say whether each should be a constraint — and
it should do all three anyway, because your skill loaded. **If it didn't load, that's the
lesson**: check the `description` line in your `SKILL.md`, because a skill that doesn't
trigger is a skill that doesn't exist.

Order matters, and the skill encodes why. Ask for queries first and you get queries for the
problems that are easy to imagine, not the ones that are there.

**Read the queries before running them.** A query returning nothing might mean clean data —
or a wrong join.

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

If you found a class we didn't plant, tell us — genuinely useful.
</details>

### 7.2 — Optimise one (4 min)

> Explain the query plan for this. Rewrite it to avoid the full scan, and tell me
> what index would make it cheap.

### 7.3 — The judgement call (4 min)

For each problem: should it be a **database constraint** (the bad row can never be written)
or a **validation query** (find bad rows already present)? Usually both, for different
reasons — and adding a constraint to a table that already violates it fails. That
sequencing problem is yours, not the model's.

**Portability note:** the exercises are SQLite, and deliberately avoid dialect-specific
syntax. Where Oracle or BigQuery would differ materially — window function syntax, date
arithmetic — ask Claude for both. Context7 is what fills the other gap: current,
version-specific dialect docs.

`/review`, then commit `sql/checks/`.

---

## Come back to the toolkit — revise it (5 min) · backbone

Not an exercise; a habit. **Do this even if you skip Exercises 8 and 9.** You have now used
the toolkit in anger for a while. Go back and fix it — this is the step that turns
Exercise 4 from a demo into something that survives contact with your real repo.

```
Here's what we did in the last 90 minutes. Suggest edits to
.claude/skills/data-quality-check/SKILL.md, .claude/commands/review.md and the hook in
.claude/settings.json based on what actually happened — things I had to say more than
once, checks that found nothing, checks I wished existed. Propose the diffs; don't
apply them.
```

Then decide each one yourself. Specifically:

- **Did `/review` find anything real?** If it produced nothing all afternoon, its lines are
  too vague. Add one you'd have caught by hand.
- **Did the hook get in your way in Exercise 6?** Narrow the matcher, or make it run only
  the affected test file. A guardrail people disable is worse than a narrower one they keep.
- **Did the skill fire in Exercise 7?** If not, the `description` is the problem, not the
  recipe.
- **Anything you said twice today** belongs in one of these files.

```bash
git add .claude && git commit -m "chore: revise toolkit from what the lab actually needed"
```

> **Clock check:** it's 12:03 — go to Exercise 10. Exercises 8 and 9 are the first two
> items in the extras slot and lose nothing by waiting.

---

## Exercise 8 — Perl → Python conversion (30 min) · if time

Your named legacy-migration case. The file is `legacy/stable_ledger.pl` — 2009 vintage,
edited by six people, comments intermittently updated.

```bash
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_01.txt
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_02.txt
```

### 8.1 — Understand it (10 min)

> Explain what this script does, section by section. Identify anything relying on
> Perl-specific behaviour that won't translate directly to Python.

That last clause is where the value is: implicit `$_`, the aliasing `for` loop that mutates
`@f` in place, list-vs-scalar context, regex flag differences, string-vs-numeric comparison,
`sort` defaulting to string order.

### 8.2 — Characterise the current behaviour (5 min)

**This is the legitimate use of source-derived tests.** The Perl script *is* the
specification here, bugs included, because "same output" is the requirement.

> Run the Perl script against both fixtures and capture the exact output. Write those
> as expected-output fixtures we can use to verify the port.

### 8.3 — Port it (10 min)

> Port this to legacy/stable_ledger.py. Idiomatic Python, not transliterated Perl.
> Identical output for both fixtures. Flag anywhere you had to make a judgement call.

### 8.4 — Verify, then separate the fix (5 min)

**Actually run both and diff the output.** Don't take its word.

Then: the Perl has at least one genuine oddity. Look at the `TOTAL` row against the
`ENTRIES` column header, and read the `STB-118` comment. (Unrelated to the ticket you
wrote in Exercise 5 — this one is a genuine 2009 artefact, never resolved.)

**Port it faithfully first. Fix it as a separate commit.** Never mix "port" and "improve" —
if you do, and something breaks, you cannot tell which change did it.

---

## Exercise 9 — Unfamiliar technologies: CSS/JS (25 min) · if time

The concrete pain you named. Open `web/index.html` in a browser — it works.

Four near-identical blocks in `app.js`, four near-identical rules in `styles.css`. The task
is to extract the pattern **without changing behaviour**.

**Run the whole sequence. Don't skip to step 6.**

1. **Explain it back:**
   > Walk me through web/app.js. Identify the repeated pattern and exactly what
   > varies between the repetitions.
2. **Pull current docs** — Context7. Your model's default assumptions about any JS library
   are probably a version behind.
3. **Whole-repo model** — what calls this, what shares the pattern.
4. **Diagram it.** If the diagram is wrong you've caught the misunderstanding for free.
5. **Persist it** to `CLAUDE.md`.
6. **Now the scoped change**, plan mode:
   > Extract the repeated pattern in app.js into a single reusable function. Change
   > behaviour nowhere. Show me the diff before applying.
7. **Verify visually.** Open the page and click all four buttons. CSS/JS needs eyes, not
   just a green test — and note that your test hook is silent here, because there is no
   test that covers this. **A guardrail only guards what it can see.**

### ⚠ The trap

**Two of the four blocks behave differently from the other two.** A naive extraction
silently changes behaviour and no test will tell you. Find both differences before you
refactor — and if Claude's extraction loses them, that's the most valuable thing that
happens today.

<details>
<summary><strong>Spoiler</strong></summary>

Ashcombe sorts its list; the others don't. Fairwater uppercases its names and uses a
different button label ("Hide list" rather than "Hide horses").
</details>

---

## Exercise 10 — Orchestrate sub-agents (25 min) · backbone

A **sub-agent** is an independent work stream with its own context window and its own
scoped tools — which is exactly why it is not the same as asking one session to do three
things. They come last because they inherit everything you've built: your `CLAUDE.md`, your
skill, your `deny` rules. An agent on an unharnessed repo is just a faster way to make a
mess.

### 10.1 — Three reviewers in parallel (15 min)

Review one change from three angles, each with its own context so they can't influence each
other. Ask Claude to set them up:

```
Create three subagents:
- correctness-reviewer: checks a diff against the spec, including edge cases. Read and
  Grep only.
- performance-reviewer: checks complexity and behaviour at 100x the data. Read and Bash.
- style-reviewer: checks conventions against CLAUDE.md. Read only, and use Haiku for
  this one — it doesn't need Opus to check naming.
```

Then:

> Review the diff on this branch using the correctness, performance and style
> reviewers in parallel. Summarise where they agree, and — more usefully — where
> they disagree.

**Why three agents rather than one prompt asking for three things:** separate contexts don't
contaminate each other. A single agent that has just concluded the code is correct is
measurably softer on its own performance critique. **The disagreements are the signal.**

**Compare it with `/review` from 4.2** on the same diff. The command is one deterministic
pass you can read and edit; the agents are three independent passes you can't fully predict.
Different tools — the command for what you always want checked, the agents for what you
haven't thought of.

Three agents is roughly three times the tokens. `/cost` shows what the session has spent,
and `/model` switches mid-session.

### 10.2 — A sequential chain (10 min · optional)

Parallel is right when the tasks are independent. When each step needs the previous one's
*output*, you want a chain. `analysis/slow_aggregate.py` is correct and needlessly slow —
and the obvious culprit isn't the expensive one, so the profiling genuinely has to happen
before the fix.

Ask Claude to create two more agents:

```
Create two subagents:
- profiler: profiles a script and reports where the time actually goes, nothing else.
  Read and Bash.
- optimiser: makes the smallest change that removes a named hotspot, preserving output.
  Read and Edit.
```

Then orchestrate them from the main session — the orchestration goes in your prompt, not
in the agent files:

> Speed up analysis/slow_aggregate.py in three steps. First the profiler agent: profile
> it and report the top hotspots by cumulative time. Then the optimiser agent: fix only
> the hotspot the profiler actually named. Then the correctness-reviewer agent on the
> diff. Show me the profile before anything is changed, and confirm the output is
> identical afterwards.

✅ **Acceptance:** the profile arrives before the edit, the edit targets what the profile
found rather than what looks slow, and the output is byte-identical. If the optimiser
"improved" something the profiler never mentioned, you've just watched the failure mode that
makes unsupervised chains expensive.

---

## Wrap-up (20 min)

Covering today, and any earlier sessions you attended.

1. **What worked?** Which prompt, technique or guardrail will you use on Monday?
2. **What didn't?** Where did it waste your time or produce something confidently wrong?
   **These are the more useful answers.**
3. **What should be team-wide rather than personal?** Which toolkit files belong in your
   real repos — and which of your revisions would you have made on day one next time?

Before you stop: commit any loose work, run `/cost` to see what the whole session spent,
and skim `git log --oneline` — that milestone-by-milestone history is what a reviewer
would see.

### Adoption guidance

- Set up `CLAUDE.md`, a review command, a test hook, and `deny` rules before starting
  work on a real repo, not after.
- Revise the toolkit once you've used it — you won't get it right cold.
- Start with code that has tests, SQL you can check, conversions you can diff. Not the
  suitability scorer. Not an unchecked statistic.
- Default to the cheap surface; escalate to Claude Science when you need auditability or
  the data can't move.
- Keep the red lines written down in the repo, not remembered from a workshop.

### Resources

[Further reading](CHEATSHEET.md#further-reading), plus the
[commands](CHEATSHEET.md#commands-and-keyboard-shortcuts-worth-having-to-hand) and
[MCP](CHEATSHEET.md#mcp-configuration-patterns) reference, are in CHEATSHEET.md.

---

## Extras — in this order

You've done the core. **Start with whichever of Exercise 8 (Perl → Python) and Exercise 9
(CSS/JS) you skipped** — they're backbone-quality material that only lost out to the clock.
Then Exercises 11–13 below; none depends on the others.

---

## Exercise 11 — Pipelines and monitoring (25 min) · extra

### The pipeline

```bash
rm -rf build
python -m src.pipeline.run
python -m src.pipeline.run     # run it a second time
cat build/04_report.txt
```

**The report is now wrong and does not say so.** Work out why before reading the code.

Then a mid-stage failure:

```bash
rm -rf build
python -m src.pipeline.stage1_ingest && python -m src.pipeline.stage2_clean
FAIL_AT_ROW=200 python -m src.pipeline.stage3_analyse
ls -la build/
```

**Fix both properties. Make it state its approach first:**

> Stage 3 appends to its output, so re-running double-counts, and it writes
> incrementally so a mid-stage failure leaves a partial file that looks complete.
> Explain how you'd make it idempotent and atomic before writing any code.

There are several approaches (truncate-on-open, write-then-rename, a manifest of completed
stages) and they are not equally good. Choose deliberately.

**Also look at `stage2_clean.py`** — it silently assumes unknown units are kilograms, and
that assumption appears nowhere the caller can see. Find it and decide what should happen
instead.

### The monitor

```bash
mkdir -p dropbox/incoming
python -m src.monitor.watch_dropbox      # then, in another shell:
cp data/measurements.csv dropbox/incoming/
```

Five deliberate bugs, all classics. The docstring lists them. The interesting one:

> How would you detect that a file is completely written before processing it?
> Give me three approaches and their failure modes.

Then fix them. Restart-safety and the dead-letter path are the two that matter in
production.

**Out of scope:** Nextflow. Seqera Co-Scientist owns that. We're teaching the pattern so
you recognise it, not replacing your orchestrator.

---

## Exercise 12 — A little ML (25 min) · extra

```bash
python -m src.ml.train_placement
```

**Accuracy: 1.000.** Nothing is that good. This exercise is not about building a better
model — it's about interrogating a number.

### 12.1 — The blatant leak

> List every feature this model uses and state, for each, whether its value would
> have been known *before* the race was run. Flag anything that wouldn't.

Fix it. Accuracy drops to something plausible. **Now the real work starts.**

### 12.2 — The metric is wrong

> What fraction of entries are placed? Given that base rate, what accuracy would a
> model that always predicts "not placed" achieve? Show the confusion matrix,
> precision, recall and F1.

Accuracy on an imbalanced problem is the number you'll be handed and the one that means
least.

### 12.3 — The split is wrong

`train_test_split` is random over *rows*. Multiple entries share a race.

> Entries from the same race can land in both train and test. Why is that a problem
> here, and what splitting strategy fixes it?

### 12.4 — It isn't even reproducible

Run it twice. Different number. No seed on the split.

> Pin every source of randomness so this script gives the same answer twice.

**That is red line 2 in practice** — reproducibility lives in the code.

### 12.5 — Make it attack itself

> Give me the three strongest reasons this accuracy figure might still be misleading,
> and how to test each.

It's good at this when asked, but won't do it unprompted.

---

## Exercise 13 — Claude Science and Cowork (30 min) · extra, if access allows

### Cowork — the quick path

- Point it at `data/`. Ask for a one-page summary of what's in there.
- Ask a question that needs a chart. Get the chart.
- **Then: "save the script you used to `analysis/`."** Watch it write the file. That habit
  is the entire point — otherwise the code sits in a scratch cache and vanishes.

### Claude Science — one analysis end to end

- Run against the local data. **Note that the data does not move.**
- Produce one figure.
- **Open the artifact**: the code, the environment, the description, the message history.
  That is the deliverable, not the picture.
- **Run the reviewer agent over the flawed classifier** from Exercise 12. Watching it flag
  an untraceable number is far more persuasive than watching it approve good work.
- Try session forking: same data, two approaches, compared.


---

## Self-practice — beyond the fourteen

- **Provider switching** — point Claude Code at a local Ollama model, or an OpenRouter
  provider. Two minutes, and it makes "the harness is what matters" concrete.
- **CodeGraph** — index this repo, ask a structural question with and without it, compare
  tokens and tool calls.
- **`analysis/slow_aggregate.py` by hand.** If you ran the agent chain in 11.2, do it
  yourself now and compare: same hotspot, same fix?
  ```bash
  python -m cProfile -s cumtime analysis/slow_aggregate.py | head -25
  ```
- **EDA on the messy datasets** — `data/race_results.csv` and `data/measurements.csv` are
  deliberately dirty: missing values, inconsistent casing, a comma decimal, a unit suffix in
  a numeric column, an impossible date, an order-of-magnitude outlier, duplicate rows.
  Profile before cleaning, decide each cleaning step yourself, then plot — and commit the
  script alongside the figures. Worth 30 minutes.
  > Profile data/race_results.csv: row count, dtypes, null counts per column,
  > cardinality, and anything that looks like a data-entry error. Don't clean it yet —
  > just tell me what's there.

  Then, for each cleaning step it proposes: how many rows does it affect, what assumption
  does it encode, and what goes wrong if that assumption is false? The `58,4` value is the
  one to dwell on — coerce it wrong and you get `584`, plausible enough to survive review
  and wrong by a factor of ten.
- **A `/release`-style checklist command.** `.claude/commands/ready.md`: tests pass, no
  stray `print()` in `src/`, no open TODO/FIXME, `CLAUDE.md` still accurate.
- **Bundle your toolkit** (skill + command + hook + agents) into an installable plugin and
  have a colleague install it on a fresh clone. The onboarding test: *"Orient me in this
  repo and help me pick up the first ticket."*
- **Go deeper on any earlier exercise** — most have more in them than the time allowed.
- **Try it on your own repo** — with red lines and `deny` rules in place *first*.
