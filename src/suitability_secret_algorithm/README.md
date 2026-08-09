# ⛔ LOCKED — src/suitability_secret_algorithm/

**In this repo, Claude cannot modify anything in this directory.** Enforced three ways:

1. `deny` rules in `.claude/settings.json` (`Write`/`Edit` on `src/suitability_secret_algorithm/**`)
2. A `PreToolUse` hook (`.claude/hooks/guard_suitability_secret_algorithm.py`)
3. This notice, which is the weakest of the three — a prompt is advice, not a rule

## Why this module and not others

## Why it is locked *here* — and why that is not the general rule

A `deny` rule is the **strongest** control, and this repo uses it so you can see the
mechanism work. It is not the recommended default for real algorithm code.

The general position (Day 1, red line 1) is that algorithm code needs **two** controls
rather than a ban:

1. **Review the plan, not the diff.** Plan mode, and make it state why its change
   preserves the rationale — before it writes anything.
2. **A validation suite** whose expected values come from an independent source of
   truth, not from the current implementation. See `RATIONALE.md` in this directory and
   `tests/test_suitability_secret_algorithm_validation.py`, which is exactly that.

`deny` is the right answer in one specific case: **when no validation suite exists yet.**
Then lock the path and treat building the suite as the actual task. That is the
condition, and it is the reason this directory is locked in a teaching repo.

The underlying failure mode is real either way:

- The logic here encodes a **rationale** — a set of decisions someone can defend on
  scientific grounds, with reasons for the weights and the thresholds.
- A capable model can read it, appear to understand it, and produce a change that
  looks like an improvement while being subtly wrong.
- That kind of wrong **does not reliably fail a test**. The output is still a
  plausible ranking. Nothing goes red. The diff looks tidy.
- So the control cannot be "review it carefully". It has to be structural.

## What you *can* do

Reading it is fine, and useful:

- "Explain how `suitability_score` weights its inputs, and what each weight implies."
- "What edge cases does this not handle?"
- "Write tests for the current behaviour, in `tests/`, without modifying this module."

That last one is legitimate and valuable — a characterisation suite is exactly how
you'd protect this code before a *human* changed it.

## Try to break the rule

Genuinely — the exercise on Day 3 asks you to. Ask Claude to improve the suitability
scorer and watch the write get blocked. A guardrail you've seen fail closed is a
guardrail you trust.
