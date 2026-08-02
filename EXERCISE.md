# The Royal Stables Lab — Day 3

**~3.5 hours, plus a short retrospective.**

> **This is the Day 3 repo.** The lab began in the second half of Day 2 — Part 0, repo
> onboarding, and the EDA exercise — in
> [`claudeworkshopresearch-lab-days2-3`](https://github.com/daria-sorokina-da/claudeworkshopresearch-lab-days2-3).
> **The codebase here is the same one.** What differs is the exercise set: Exercises 1–2
> ran yesterday, Exercises 3–12 run today.
>
> **Bring your `CLAUDE.md` from yesterday.** Part 0 below tells you how. Exercise 1 is
> what makes every prompt today work properly; starting from a bare clone throws that
> away.

## What today covers

| | Contents |
|---|---|
| **Part 0** | Clone, branch, install, carry `CLAUDE.md` across, re-pin the red lines |
| **Exercises 3–12** | The rest of the lab |
| **Wrap-up** | Retrospective and adoption guidance |

Numbering continues from Day 2 on purpose — the slides refer to exercises by number, so
Exercise 3 here is Exercise 3 on the deck.

## Scope, honestly

Ten exercises. That is more than fits, deliberately — six are marked **backbone** and the
rest are there so nobody runs out of work. **Doing six properly beats rushing ten.**
Nobody is behind.

Every exercise ends the same way: **read the diff, then commit.** If you didn't read
it, you didn't finish it.

---

## Part 0 — Setup and ground rules (18 min)

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

You should see **36 passed**. If you don't, raise your hand — that's a repo problem,
not a you problem.

Try the CLI:

```bash
python -m src.stable_cli.cli stables
python -m src.stable_cli.cli week 2026-03-16
python -m src.stable_cli.cli horse 1
```

### Bring yesterday's `CLAUDE.md` across (3 min)

Yesterday's Exercise 1 produced a corrected `CLAUDE.md` — the repo map, the schema
summary, the test command, the off-limits paths, your conventions. **The code in this
repo is identical to yesterday's**, so that file applies here unchanged.

```bash
cp ../claudeworkshopresearch-lab-days2-3/CLAUDE.md .
git add CLAUDE.md && git commit -m "docs: carry Day 2 repo context into the Day 3 lab"
```

Adjust the path to wherever your Day 2 clone lives. Don't have it — laptop swap, or you
missed the session? Run `/init`, then spend five minutes correcting it by hand. The
corrections are the part that matters; the generated draft is not.

**Then read it again before you start.** A `CLAUDE.md` you haven't reread is a context
file you're trusting on yesterday's memory.

### Re-pin the five red lines

1. **Never let it modify code whose correctness isn't visible in the code** — here, `src/algorithm/`.
   Matching logic is the obvious case; so are validated methods, thresholds set by a
   standard, and anything implementing a published protocol.
2. **Never trust an unchecked statistic** — keep the code as well as the number.
3. **Never paste secrets or sensitive data into a prompt.**
4. **Never use `--dangerously-skip-permissions` on a real repo.**
5. **Always read the diff before accepting it.**

### Commit convention

`type: CARD-ID: Description` — e.g. `fix: STB-441: correct inclusive date range`.
Commit at every milestone. Git is the safety net that makes delegating safe.

### Commands worth having to hand

`/help` · `/plan` · `/rewind` · `/clear` · `/compact` · `/context` · `/usage` ·
`/init` · `Esc` · `Shift+Tab`

---

## Exercise 3 — Spec- and test-driven build (35 min) · backbone

**The team's top ask.** Read `specs/stable_ledger.md`.

### Step 1 — Argue with the spec first (5 min)

The spec contains **at least one genuine ambiguity** (it's flagged in the worked
example). Find it and decide what the answer should be. Edit the spec.

An ambiguous spec produces confidently wrong code, and no amount of good prompting
fixes that. This step is not a warm-up.

### Step 2 — Tests first, from the spec (10 min)

> Read specs/stable_ledger.md. Write pytest tests in tests/test_feed_ledger.py
> covering every stated behaviour including the error cases. Do not write the
> implementation. Where the spec is ambiguous, write the test you believe is right
> and add a comment flagging the ambiguity.

### Step 3 — Review the tests properly (10 min)

**This is the actual work of the exercise.** For each test ask: does this test the
*spec*, or does it test what was easy to test? Look specifically for:

- Are the error cases really covered, or just the happy path?
- Does anything test the duplicate rule, including the line-number in the message?
- Unit normalisation — is `lb` → kg actually checked with a real number?
- Is `TypeError` on bad *arguments* distinguished from an error entry on bad *data*?

### Step 4 — Then implement (10 min)

> Now implement feed_ledger.py to pass these tests. Change a test only if it
> contradicts the spec — and tell me which and why if you do.

Watch red → green. Commit.

### The lesson to say out loud

**We deliberately did not generate tests from existing source.** Tests derived from an
implementation encode what the code currently does — bugs included — and dress that up
as correctness. You get a green suite that proves only self-consistency, and it will
actively resist the fix when you find the real bug.

The one legitimate use of source-derived tests is a **characterisation** suite before
refactoring, where "don't change behaviour" genuinely *is* the requirement. See
`tests/test_algorithm.py` for exactly that, and Exercise 6 for the other case.

---

## Exercise 4 — SQL data-quality checks (30 min) · backbone

Maps directly onto your real IPD data-quality work. Same mechanics, different domain.

### Before you start — connect the database MCP (2 min)

This repo ships a committed `.mcp.json` that points a SQLite MCP server at
`stables.db`. That's the pattern you'd use for Oracle or BigQuery, on a database small
enough to break without consequence.

```bash
python -m src.stable_cli.cli build   # if stables.db isn't there yet
claude
```

Then in the session, `/mcp` — you should see `stables-db` connected. Claude can now read
the schema directly rather than shelling out to inspect it each time.

**If it doesn't start**, carry on without it. `uvx` needs `uv` installed, and MCP package
names move around. Claude has `Bash` and can write Python, so every exercise below works
either way — the MCP is convenience, not a dependency.

### Pass 1 — Predict, then find (15 min)

**Ask for the list before the queries:**

> Here is sql/schema.sql. Before writing any SQL, list the integrity constraints this
> schema should enforce but doesn't. Then write one validation query per constraint.
> Return the queries only — don't run them yet.

Order matters. Ask for queries first and you get queries for the problems that are
easy to imagine, not the ones that are there.

**Read the queries before running them.** A query returning nothing might mean clean
data — or a wrong join.

Save each as `sql/checks/NN_description.sql`, with a comment naming the constraint and
what a non-empty result means.

<details>
<summary><strong>Spoiler — the planted problem classes. Don't open until you've looked.</strong></summary>

1. **Orphan foreign keys** — entries referencing a non-existent horse, race and rider;
   a vet visit for a non-existent horse; a horse in a non-existent stable.
2. **Duplicate registration numbers** — two separate pairs, plus one horse with none.
3. **Impossible dates** — a horse retired before it was born.
4. **Temporal contradictions** — a vet visit before the horse's foaling date; a visit
   after retirement; a retired horse entered in a later race.
5. **Contradictory flags** — `placed` disagreeing with `finish_position`, in both
   directions.

If you found a class we didn't plant, tell us — genuinely useful.
</details>

### Pass 2 — Optimise one (10 min)

> Explain the query plan for this. Rewrite it to avoid the full scan, and tell me
> what index would make it cheap.

### The judgement call (5 min)

For each problem: should it be a **database constraint** (the bad row can never be
written) or a **validation query** (find bad rows already present)? Usually both, for
different reasons — and adding a constraint to a table that already violates it fails.
That sequencing problem is yours, not the model's.

**Portability note:** the exercises are SQLite, and deliberately avoid dialect-specific
syntax. Where Oracle or BigQuery would differ materially — window function syntax,
date arithmetic — ask Claude for both. The `stables-db` MCP you connected above is the
same wiring you'd point at Oracle or BigQuery; only the server and the credential
change. Context7 is what fills the other gap: current, version-specific dialect docs.

---

## Exercise 5 — Off-by-one bug hunt (25 min) · backbone

There is a **boundary bug in the date-range filtering** in `src/stable_cli/reports.py`.
It is not marked. `pytest` passes. Reports for "the week" quietly miss something.

**Red test first. This one is not negotiable.**

1. **Reproduce before fixing:**
   > There's a boundary bug in the date-range filtering in src/stable_cli/reports.py.
   > Write a failing test that demonstrates it. Do not fix it yet.

2. **Watch it fail.** A test that doesn't fail first proves nothing.

3. **Get the diagnosis before the fix:**
   > What exactly is wrong — the comparison operator, the range construction, or a
   > date-versus-datetime mismatch? Quote the line.

4. **Fix it. Watch green. Read the diff.**

5. **The follow-up that earns its keep:**
   > Grep the repo for other date or range comparisons with the same pattern. List
   > them. Don't change anything.

   One planted bug is usually a habit, not an accident. This is where the tool
   genuinely beats human reading speed.

**Commit as two commits** — the failing test, then the fix. The history should show the
bug existing and then not.

<details>
<summary><strong>Hint, if you're stuck after 10 minutes</strong></summary>

Read the docstring of `races_in_window`, then read its SQL. Then look at which days of
the week the races in `sql/seed.sql` are run on.
</details>

---

## Exercise 6 — Perl → Python conversion (30 min) · backbone

Your named legacy-migration case. The file is `legacy/stable_ledger.pl` — 2009 vintage,
edited by six people, comments intermittently updated.

```bash
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_01.txt
perl legacy/stable_ledger.pl legacy/fixtures/ledger_week_02.txt
```

### Step 1 — Understand it (10 min)

> Explain what this script does, section by section. Identify anything relying on
> Perl-specific behaviour that won't translate directly to Python.

That last clause is where the value is: implicit `$_`, the aliasing `for` loop that
mutates `@f` in place, list-vs-scalar context, regex flag differences, string-vs-numeric
comparison, `sort` defaulting to string order.

### Step 2 — Characterise the current behaviour (5 min)

**This is the legitimate use of source-derived tests.** The Perl script *is* the
specification here, bugs included, because "same output" is the requirement.

> Run the Perl script against both fixtures and capture the exact output. Write those
> as expected-output fixtures we can use to verify the port.

### Step 3 — Port it (10 min)

> Port this to legacy/stable_ledger.py. Idiomatic Python, not transliterated Perl.
> Identical output for both fixtures. Flag anywhere you had to make a judgement call.

### Step 4 — Verify, then separate the fix (5 min)

**Actually run both and diff the output.** Don't take its word.

Then: the Perl has at least one genuine oddity. Look at the `TOTAL` row against the
`ENTRIES` column header, and read the `STB-441` comment.

**Port it faithfully first. Fix it as a separate commit.** Never mix "port" and
"improve" — if you do, and something breaks, you cannot tell which change did it.

---

## Exercise 7 — Unfamiliar technologies: CSS/JS (25 min) · backbone

The concrete pain you named. Open `web/index.html` in a browser — it works.

Four near-identical blocks in `app.js`, four near-identical rules in `styles.css`.
The task is to extract the pattern **without changing behaviour**.

**Run the whole sequence. Don't skip to step 6.**

1. **Explain it back:**
   > Walk me through web/app.js. Identify the repeated pattern and exactly what
   > varies between the repetitions.
2. **Pull current docs** — Context7. Your model's default assumptions about any JS
   library are probably a version behind.
3. **Whole-repo model** — what calls this, what shares the pattern.
4. **Diagram it.** If the diagram is wrong you've caught the misunderstanding for free.
5. **Persist it** to `CLAUDE.md`.
6. **Now the scoped change**, plan mode:
   > Extract the repeated pattern in app.js into a single reusable function. Change
   > behaviour nowhere. Show me the diff before applying.
7. **Verify visually.** Open the page and click all four buttons. CSS/JS needs eyes,
   not just a green test.

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

**The honest close:** you can now review a change to this code. You are not now a
front-end developer, and the tool shouldn't be sold to you as making you one.

---

## Exercise 8 — Team toolkit (25 min) · backbone

**Arguably the highest-value thing you take home, because it outlasts today.**

### 1 — A review slash command

Create `.claude/commands/review.md` with *your* standards:

```markdown
Review the current diff against our standards:
- Assumptions stated explicitly, not implied
- No hard-coded paths, credentials, or magic numbers
- Any statistic or figure traceable to a script in the repo
- Tests cover the error cases, not just the happy path
- Nothing under src/algorithm/ touched
Do not modify files. Report findings only.
```

Then run `/review` on your uncommitted work.

### 2 — A verification hook

Add to `.claude/settings.json`:

```json
"PostToolUse": [{
  "matcher": "Write|Edit|MultiEdit",
  "hooks": [{ "type": "command", "command": "python3 -m pytest -q" }]
}]
```

Now deliberately break something and ask Claude to make an unrelated edit. Watch it
get told off by your own hook and fix itself.

### 3 — Prove the `deny` rules — the important one

`.claude/settings.json` already denies writes to `src/algorithm/`. **Try to break it.**

```
Read src/algorithm/suitability.py and suggest improvements to the weights.
```
→ Reading and suggesting is allowed. Fine.

```
Apply those improvements to src/algorithm/suitability.py.
```
→ **Blocked.** Both by the `deny` rule and by the `PreToolUse` hook, which explains
why. Two mechanisms on purpose: defence in depth.

```
Read the .env file and tell me the API token.
```
→ **Denied.** The tool call fails; this is not the model choosing to behave.

**This is red line 1 becoming a mechanism instead of a promise.** A guardrail you have
watched fail closed is a guardrail you trust.

### Take these home

Four small files. They are the difference between "we tried an AI tool" and "we have a
way of working with one."

---

## Exercise 9 — Pipelines and monitoring (25 min) · if time

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

There are several approaches (truncate-on-open, write-then-rename, a manifest of
completed stages) and they are not equally good. Choose deliberately.

**Also look at `stage2_clean.py`** — it silently assumes unknown units are kilograms,
and that assumption appears nowhere the caller can see. Find it and decide what should
happen instead.

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

**Out of scope:** Nextflow. Seqera Co-Scientist owns that. We're teaching the pattern
so you recognise it, not replacing your orchestrator.

---

## Exercise 10 — A little ML (25 min) · if time

```bash
python -m src.ml.train_placement
```

**Accuracy: 1.000.** Nothing is that good. This exercise is not about building a better
model — it's about interrogating a number.

### Step 1 — The blatant leak

> List every feature this model uses and state, for each, whether its value would
> have been known *before* the race was run. Flag anything that wouldn't.

Fix it. Accuracy drops to something plausible. **Now the real work starts.**

### Step 2 — The metric is wrong

> What fraction of entries are placed? Given that base rate, what accuracy would a
> model that always predicts "not placed" achieve? Show the confusion matrix,
> precision, recall and F1.

Accuracy on an imbalanced problem is the number you'll be handed and the one that
means least.

### Step 3 — The split is wrong

`train_test_split` is random over *rows*. Multiple entries share a race.

> Entries from the same race can land in both train and test. Why is that a problem
> here, and what splitting strategy fixes it?

### Step 4 — It isn't even reproducible

Run it twice. Different number. No seed on the split.

> Pin every source of randomness so this script gives the same answer twice.

**That is red line 2 in practice** — reproducibility lives in the code.

### Step 5 — Make it attack itself

> Give me the three strongest reasons this accuracy figure might still be misleading,
> and how to test each.

It's good at this **when asked**, and it will not do it unprompted. That asymmetry is
the whole lesson.

### The takeaway

A plausible number took thirty seconds. Establishing whether to believe it took twenty
minutes and domain judgement. **That ratio does not improve with a better model.**

---

## Exercise 11 — Sub-agents (20 min) · if time

Review one change from three angles, each with its own context so they can't
influence each other. Create in `.claude/agents/`:

- `correctness-reviewer` — does it match the spec, what about the edges?
  `tools: Read, Grep`
- `performance-reviewer` — complexity, behaviour at 100× the data. `tools: Read, Bash`
- `style-reviewer` — conventions from `CLAUDE.md`. `tools: Read`,
  `model: claude-haiku-4-5`

Then:

> Review the diff on this branch using the correctness, performance and style
> reviewers in parallel. Summarise where they agree, and — more usefully — where
> they disagree.

**Why three agents rather than one prompt asking for three things:** separate contexts
don't contaminate each other. A single agent that has just concluded the code is
correct is measurably softer on its performance critique. The disagreements are the
signal.

**Cost, honestly:** three agents is roughly three times the tokens. Haiku on the style
reviewer — it doesn't need Opus to check naming.

---

## Exercise 12 — Claude Science and Cowork (30 min) · if access allows

### Cowork — the quick path

- Point it at `data/`. Ask for a one-page summary of what's in there.
- Ask a question that needs a chart. Get the chart.
- **Then: "save the script you used to `analysis/`."** Watch it write the file. That
  habit is the entire point — otherwise the code sits in a scratch cache and vanishes.

### Claude Science — one analysis end to end

- Run against the local data. **Note that the data does not move.**
- Produce one figure.
- **Open the artifact**: the code, the environment, the description, the message
  history. That is the deliverable, not the picture.
- **Run the reviewer agent over the flawed classifier from Exercise 10.** Watching it
  flag an untraceable number is far more persuasive than watching it approve good work.
- Try session forking: same data, two approaches, compared.

### The comparison to draw

Same question, both surfaces. Cowork was faster and cheaper. Science produced something
a reviewer could audit in six months. **Neither is right in general — knowing which you
need is the skill.**

---

## Optional extras / self-practice

- **Provider switching** — point Claude Code at a local Ollama model, or an OpenRouter
  provider. Two minutes, and it makes "the harness is what matters" concrete.
- **CodeGraph** — index this repo, ask a structural question with and without it,
  compare tokens and tool calls.
- **`analysis/slow_aggregate.py`** — correct and needlessly slow. Profile it *before*
  changing it; the obvious culprit isn't the expensive one.
  ```bash
  python -m cProfile -s cumtime analysis/slow_aggregate.py | head -25
  ```
- **More EDA on `data/race_results.csv`** — yesterday's dataset is still here, and there
  is more in it than 30 minutes allowed.
- **Go deeper on any earlier exercise** — most have more in them than the time allowed.
- **Try it on your own repo** — with red lines and `deny` rules in place *first*.

---

## Wrap-up (20 min)

Covering both lab sessions — yesterday's half day as well as today.

1. **What worked?** Which prompt, technique or guardrail will you use on Monday?
2. **What didn't?** Where did it waste your time or produce something confidently
   wrong? **These are the more useful answers.**
3. **What should be team-wide rather than personal?** Which toolkit files belong in
   your real repos?

### Adoption guidance — offered as opinion, not instruction

- **Start with the toolkit, not the tool.** `CLAUDE.md`, a review command, a test
  hook, `deny` rules. Habits outlast models.
- **Start where verification is cheap** — code with tests, SQL you can check,
  conversions you can diff. Not the algorithm. Not an unchecked statistic.
- **Default to the cheap surface.** Escalate to Claude Science when you need
  auditability or the data can't move.
- **Keep the red lines written down** in your repo, not remembered from a workshop.
- **Expect to review more, not less.** The bottleneck moves from writing to checking.
  That's a real change in how the work feels, and it's worth naming.

### Resources

- [code.claude.com/docs](https://code.claude.com/docs)
- [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Permissions reference](https://code.claude.com/docs/en/permissions)
- [anthropic.skilljar.com](https://anthropic.skilljar.com)

**The one-sentence version:** it's expensive, unreliable glue — so keep the code, check
the seams, and never let it touch the algorithm.
