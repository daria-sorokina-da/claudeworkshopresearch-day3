"""VALIDATION tests for the suitability scorer.

Note the distinction from `test_algorithm.py`, and take it seriously:

  * `test_algorithm.py` is a CHARACTERISATION suite. Its expected values were read off
    the current implementation. It tells you whether behaviour changed. It cannot tell
    you whether behaviour is CORRECT — it would pass a confidently wrong rewrite.

  * This file is a VALIDATION suite. Every expected value below is derived from
    src/algorithm/RATIONALE.md — an independent statement of what the right answer is.
    These tests encode the *reasoning*, not the code.

That difference is the whole point of red line 1. A validation suite is what makes it
safe to let an AI assistant change algorithm code at all: it turns a rationale that
lives in prose into something executable.

When you add a rule to RATIONALE.md, add a test here. When the two disagree, the
rationale wins and one of them is a bug.
"""

from datetime import date

import pytest

from src.algorithm import suitability_score

BASE = dict(
    preferred_min_f=8, preferred_max_f=12, preferred_going="good",
    race_distance_f=10, race_going="good", recent_positions=[3],
)


def score(**overrides):
    return suitability_score(**{**BASE, **overrides})


# --- RATIONALE: distance is categorical, with a hard floor -------------------

def test_distance_two_furlongs_outside_range_scores_zero_on_that_term():
    """RATIONALE: a taper that never reaches zero lets an unsuitable horse pass.

    At 2f outside the range the distance term must be exactly 0, so the total cannot
    exceed the sum of the remaining weights (0.25 + 0.10 = 0.35).
    """
    assert score(race_distance_f=14) <= 0.35 + 1e-9


def test_a_horse_far_outside_its_range_cannot_pass_on_other_strengths():
    """RATIONALE: this is the specific failure the hard floor exists to prevent."""
    perfect_everything_else = score(
        race_distance_f=16, race_going="good", recent_positions=[1, 1, 1],
    )
    assert perfect_everything_else < 0.5, (
        "an unsuitable-distance horse accumulated a passing score from other terms"
    )


# --- RATIONALE: distance outweighs going ------------------------------------

def test_distance_matters_more_than_going():
    """RATIONALE: going can be compensated for; distance cannot."""
    wrong_going = score(race_going="heavy")
    wrong_distance = score(race_distance_f=13)
    assert wrong_distance < wrong_going


# --- RATIONALE: going is ordinal -------------------------------------------

def test_going_is_ordinal_not_categorical():
    """RATIONALE: firm→good is a smaller mismatch than firm→heavy.

    A categorical implementation would score these two identically. This test fails
    if someone "simplifies" the going comparison to equality.
    """
    one_step = score(preferred_going="firm", race_going="good")
    three_steps = score(preferred_going="firm", race_going="heavy")
    assert one_step > three_steps


def test_unknown_going_is_not_penalised_as_bad_going():
    """RATIONALE: missing data is not bad data."""
    unknown = score(race_going="unrecorded")
    bad = score(preferred_going="firm", race_going="heavy")
    assert unknown > bad


# --- RATIONALE: form is a tie-breaker, not a driver ------------------------

def test_form_cannot_outweigh_a_distance_mismatch():
    """RATIONALE: form is the noisiest input; raising its weight flatters backtests.

    Fails if W_RECENT_FORM is increased to 'improve accuracy'.
    """
    great_form_wrong_distance = score(race_distance_f=14, recent_positions=[1, 1, 1])
    poor_form_right_distance = score(race_distance_f=10, recent_positions=[9, 9, 9])
    assert poor_form_right_distance > great_form_wrong_distance


def test_no_form_is_neutral_not_bad():
    """RATIONALE: absence of form is not evidence of poor form."""
    assert score(recent_positions=[]) > score(recent_positions=[8, 9, 7])


# --- RATIONALE: lameness is veto-shaped -----------------------------------

def test_recent_lameness_is_not_averaged_away_by_strong_scores():
    """RATIONALE: expressed as a penalty precisely so it cannot be outvoted.

    Fails if FITNESS_PENALTY is converted into a weighted term.
    """
    best_case_but_lame = score(
        race_distance_f=10, race_going="good", recent_positions=[1, 1, 1],
        last_lameness_on=date(2026, 3, 1), race_date=date(2026, 3, 10),
    )
    mediocre_but_sound = score(recent_positions=[4, 4])
    assert best_case_but_lame < mediocre_but_sound


@pytest.mark.parametrize("days,penalised", [(0, True), (20, True), (21, False), (60, False)])
def test_lameness_window_boundary_is_21_days(days, penalised):
    """RATIONALE: 21 days is veterinary convention, not a tuned parameter."""
    from datetime import timedelta
    lame_on = date(2026, 3, 1)
    s = score(last_lameness_on=lame_on, race_date=lame_on + timedelta(days=days))
    clean = score()
    assert (s < clean) is penalised


# --- RATIONALE: the score is a bounded, comparable quantity ---------------

def test_score_stays_within_bounds_under_all_combinations():
    for dist in (4, 10, 20):
        for going in ("hard", "good", "heavy", "unrecorded"):
            for form in ([], [1], [10, 10]):
                s = score(race_distance_f=dist, race_going=going, recent_positions=form)
                assert 0.0 <= s <= 1.0
