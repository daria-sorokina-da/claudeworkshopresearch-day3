"""Characterisation tests for the off-limits algorithm module.

These exist to protect src/algorithm/ — they record what it currently does so that
any change is visible. Writing tests for that module is allowed and encouraged;
changing the module is not.
"""

from datetime import date

from src.algorithm import suitability_score, rank_entries


def test_perfect_fit_scores_high():
    score = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[1, 2, 1],
    )
    assert score > 0.8


def test_distance_far_outside_range_zeroes_the_distance_term():
    score = suitability_score(
        preferred_min_f=5, preferred_max_f=7, preferred_going="firm",
        race_distance_f=16, race_going="firm", recent_positions=[1, 1, 1],
    )
    assert score < 0.5


def test_going_mismatch_reduces_score():
    firm = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="firm",
        race_distance_f=10, race_going="firm", recent_positions=[3],
    )
    heavy = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="firm",
        race_distance_f=10, race_going="heavy", recent_positions=[3],
    )
    assert heavy < firm


def test_recent_lameness_applies_a_penalty():
    clean = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[1],
    )
    lame = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[1],
        last_lameness_on=date(2026, 3, 1), race_date=date(2026, 3, 10),
    )
    assert lame < clean


def test_lameness_outside_the_window_is_not_penalised():
    inside = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[1],
        last_lameness_on=date(2026, 3, 1), race_date=date(2026, 3, 10),
    )
    outside = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[1],
        last_lameness_on=date(2026, 3, 1), race_date=date(2026, 4, 30),
    )
    assert outside > inside


def test_no_form_is_treated_as_neutral_not_bad():
    none = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[],
    )
    bad = suitability_score(
        preferred_min_f=8, preferred_max_f=12, preferred_going="good",
        race_distance_f=10, race_going="good", recent_positions=[8, 9, 7],
    )
    assert none > bad


def test_score_is_bounded():
    for positions in ([1, 1, 1], [10, 10, 10], []):
        score = suitability_score(
            preferred_min_f=8, preferred_max_f=12, preferred_going="good",
            race_distance_f=10, race_going="good", recent_positions=positions,
        )
        assert 0.0 <= score <= 1.0


def test_rank_entries_sorts_most_suitable_first():
    entries = [
        {"horse_id": 1, "factors": {
            "preferred_min_f": 5, "preferred_max_f": 7, "preferred_going": "firm",
            "race_distance_f": 16, "race_going": "heavy", "recent_positions": [8]}},
        {"horse_id": 2, "factors": {
            "preferred_min_f": 12, "preferred_max_f": 16, "preferred_going": "heavy",
            "race_distance_f": 16, "race_going": "heavy", "recent_positions": [1]}},
    ]
    ranked = rank_entries(entries)
    assert ranked[0]["horse_id"] == 2
    assert ranked[0]["suitability"] > ranked[1]["suitability"]
