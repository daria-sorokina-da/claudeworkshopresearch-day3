"""Horse-to-race suitability scoring.

⛔ OFF LIMITS. Do not modify this module with an AI assistant. See README.md.

The weights below are not arbitrary and are not tunable by inspection. Each was
chosen for a stated reason, recorded here, and changing one without revisiting the
reason produces a scorer that still returns plausible numbers and is wrong.

This is the workshop's stand-in for a real algorithm of that kind. The property that
matters is not that it's complicated — it's that its correctness lives in the
*justification*, not in the code, and a model cannot see the justification.
"""

from __future__ import annotations

from datetime import date
from typing import Iterable

# --- Weights -----------------------------------------------------------------
#
# DISTANCE_FIT: dominant term. A horse outside its distance range is not merely
#   less suited, it is unsuitable — hence the largest weight and the hard floor
#   in _distance_fit rather than a gentle taper.
#
# GOING_FIT: secondary. Ground conditions matter, but a well-suited horse on
#   imperfect ground still runs; hence roughly half the distance weight.
#
# RECENT_FORM: deliberately small. Form is the noisiest input we have and the
#   most tempting to over-weight. It is a tie-breaker, not a driver.
#
# FITNESS_PENALTY: subtractive, not a weight. A recent lameness is a veto-shaped
#   input; expressing it as a penalty keeps it from being averaged away.

W_DISTANCE_FIT = 0.50
W_GOING_FIT = 0.25
W_RECENT_FORM = 0.10
FITNESS_PENALTY = 0.40

# Days after a recorded lameness during which a horse is considered compromised.
# 21 days is the veterinary convention used by this yard, not a tuned parameter.
LAMENESS_WINDOW_DAYS = 21


def _distance_fit(preferred_min_f: int, preferred_max_f: int, race_distance_f: int) -> float:
    """1.0 inside the horse's range, tapering to a hard 0.0 two furlongs outside.

    The floor is deliberate. A taper that never reaches zero lets an unsuitable
    horse accumulate a passing score from the other terms.
    """
    if preferred_min_f <= race_distance_f <= preferred_max_f:
        return 1.0

    if race_distance_f < preferred_min_f:
        overshoot = preferred_min_f - race_distance_f
    else:
        overshoot = race_distance_f - preferred_max_f

    if overshoot >= 2:
        return 0.0
    return 1.0 - (overshoot / 2.0)


def _going_fit(preferred_going: str, race_going: str) -> float:
    """Ordinal closeness on the going scale.

    Going is ordinal, not categorical: firm-to-good is a smaller mismatch than
    firm-to-heavy. Treating it as categorical (equal/not-equal) is the most common
    way to get this wrong.
    """
    scale = ["hard", "firm", "good", "soft", "heavy"]
    try:
        a = scale.index(preferred_going.lower())
        b = scale.index(race_going.lower())
    except ValueError:
        return 0.5  # unknown going — assume neutral rather than penalise

    steps = abs(a - b)
    return max(0.0, 1.0 - (steps * 0.35))


def _recent_form(recent_positions: Iterable[int]) -> float:
    """Mean of up to the last three finishes, normalised so 1st = 1.0, 6th+ = 0.0.

    Capped at three runs on purpose. A longer window smooths out exactly the recent
    change in form this term exists to detect.
    """
    positions = [p for p in list(recent_positions)[:3] if p and p > 0]
    if not positions:
        return 0.5  # no form is not bad form

    scores = [max(0.0, (6 - p) / 5.0) for p in positions]
    return sum(scores) / len(scores)


def suitability_score(
    *,
    preferred_min_f: int,
    preferred_max_f: int,
    preferred_going: str,
    race_distance_f: int,
    race_going: str,
    recent_positions: Iterable[int],
    last_lameness_on: date | None = None,
    race_date: date | None = None,
) -> float:
    """Return a suitability score in [0.0, 1.0]. Higher is more suitable."""
    score = (
        W_DISTANCE_FIT * _distance_fit(preferred_min_f, preferred_max_f, race_distance_f)
        + W_GOING_FIT * _going_fit(preferred_going, race_going)
        + W_RECENT_FORM * _recent_form(recent_positions)
    )

    if last_lameness_on and race_date:
        days_since = (race_date - last_lameness_on).days
        if 0 <= days_since < LAMENESS_WINDOW_DAYS:
            score -= FITNESS_PENALTY

    return max(0.0, min(1.0, score))


def rank_entries(entries: list[dict]) -> list[dict]:
    """Score and sort entries, most suitable first.

    Ties are broken by horse_id purely so the order is deterministic — it carries
    no meaning and must not be read as a preference.
    """
    scored = []
    for entry in entries:
        scored.append({**entry, "suitability": suitability_score(**entry["factors"])})

    return sorted(scored, key=lambda e: (-e["suitability"], e.get("horse_id", 0)))
