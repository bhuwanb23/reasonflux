"""SCV trigger create vs reject."""

import pytest

from core import SkillCandidate, compute_scv
from skills import SkillConfig, SkillCreationTrigger


def test_compute_scv_matches_core():
    cand = SkillCandidate(
        candidate_id="sc1",
        source_invariant_id="inv1",
        expected_reuse=0.8,
        abstraction_gain=0.7,
        transfer_score=0.6,
        creation_cost=0.1,
    )
    trigger = SkillCreationTrigger()
    assert trigger.compute_scv(cand) == pytest.approx(
        compute_scv(0.8, 0.7, 0.6, 0.1)
    )


def test_should_create_respects_threshold():
    cand = SkillCandidate(
        candidate_id="sc1",
        source_invariant_id="inv1",
        reuse=0.5,
        abstraction_gain=0.5,
        transfer_score=0.5,
        creation_cost=0.1,
    )
    assert SkillCreationTrigger(SkillConfig(skill_creation_threshold=0.0)).should_create(
        cand
    )
    assert not SkillCreationTrigger(
        SkillConfig(skill_creation_threshold=2.0)
    ).should_create(cand)


def test_strict_threshold():
    cand = SkillCandidate(
        candidate_id="sc1",
        source_invariant_id="inv1",
        reuse=1.0,
        abstraction_gain=1.0,
        transfer_score=1.0,
        creation_cost=0.0,
    )
    trigger = SkillCreationTrigger(
        SkillConfig(skill_creation_threshold=0.0, skill_creation_threshold_strict=2.0)
    )
    assert trigger.should_create(cand)
    assert not trigger.should_create(cand, strict=True)
