# Why the suitability weights are what they are

**This file is the point of the exercise.** The code in `suitability.py` is correct only
in relation to the reasoning below. A model reading the code cannot see this file's
argument unless you give it to it — and it will happily "improve" the code in ways that
contradict it.

Real equivalents: a validated method description, a published protocol, a standards
committee decision, or the paragraph in a paper that says why this threshold and not
another.

---

## `W_DISTANCE_FIT = 0.50` — dominant term

A horse outside its distance range is not *somewhat less* suitable, it is **unsuitable**.
This is a categorical judgement, not a gradual one, so it carries the largest weight and
`_distance_fit` has a hard floor at zero rather than a gentle taper.

**A taper that never reaches zero would let an unsuitable horse accumulate a passing
score from the other three terms.** That is the specific failure this shape prevents.

## `W_GOING_FIT = 0.25` — secondary, deliberately half of distance

Ground conditions matter, but a well-suited horse on imperfect ground still runs
competitively. Roughly half the distance weight reflects that it can be compensated for,
where distance cannot.

## `W_RECENT_FORM = 0.10` — deliberately small

Form is the **noisiest** input available and the most tempting to over-weight, because it
correlates with recent outcomes and therefore flatters itself in any backtest. It is a
tie-breaker, not a driver. Raising this weight will improve apparent accuracy on
historical data and make the scorer worse.

Capped at three runs for the same reason: a longer window smooths out precisely the
recent change in form the term exists to detect.

## `FITNESS_PENALTY = 0.40` — subtractive, not a weight

A recent lameness is **veto-shaped**. Expressed as a weight it would be averaged away by
strong distance and going scores. Expressed as a penalty it cannot be.

## `LAMENESS_WINDOW_DAYS = 21`

Veterinary convention used by this yard. **Not a tuned parameter** — changing it is a
clinical decision, not an optimisation.

## Going treated as ordinal, not categorical

`firm → good` is a smaller mismatch than `firm → heavy`. Treating going as
equal/not-equal is the single most common way to get this wrong, and it produces a
scorer that looks fine until it recommends a horse onto ground it cannot handle.

## Unknown going returns 0.5, not 0.0

Missing data is not bad data. Penalising the unknown would systematically disadvantage
horses with incomplete records — a data-quality artefact masquerading as a judgement.

---

## What this means in practice

If a proposed change contradicts anything above, it is wrong **even if every test
passes and the output looks more accurate**. Conversely, a change that is consistent with
all of the above is worth considering.

Give this file to Claude when you ask it to work on the module. That is the difference
between it optimising blind and it reasoning with the constraint.
