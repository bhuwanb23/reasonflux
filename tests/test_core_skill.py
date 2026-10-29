"""Tests for SkillCandidate and Skill."""

import pytest

from core import (
    Skill,
    SkillCandidate,
    SkillState,
    compute_scv,
)


def test_compute_scv():
    assert compute_scv(reuse=2, abstraction_gain=3, transfer_score=4, creation_cost=1) == 23.0


def test_skill_candidate_auto_scv():
    cand = SkillCandidate(
        candidate_id="SC-1",
        source_invariant_id="INV-1",
        reuse=2.0,
        abstraction_gain=1.5,
        transfer_score=2.0,
        creation_cost=1.0,
    )
    assert cand.scv == pytest.approx(5.0)


def test_skill_from_candidate_and_lifecycle():
    cand = SkillCandidate(
        candidate_id="SC-1",
        source_invariant_id="INV-1",
        concept_id="reflection",
        trigger_conditions=["symmetry_detected"],
        execution_policy="apply_reflection",
        reuse=3.0,
        abstraction_gain=2.0,
        transfer_score=1.0,
        creation_cost=0.5,
    )
    skill = Skill.from_candidate(cand)
    assert skill.state == SkillState.PROMOTED
    assert skill.scv == pytest.approx(cand.scv)
    skill.transition_to(SkillState.ACTIVE)
    skill.transition_to(SkillState.DORMANT)
    skill.transition_to(SkillState.RETIRED)
    skill.transition_to(SkillState.ARCHIVED)
    skill.transition_to(SkillState.ACTIVE)
    assert skill.state == SkillState.ACTIVE


def test_skill_dict_round_trip():
    skill = Skill(
        skill_id="SK-1",
        source_invariant_id="INV-1",
        execution_policy="apply_rotation",
        reuse_count=2,
        scv=1.5,
        state=SkillState.ACTIVE,
        transfer_history=[{"task": "t2", "ts": 0.3}],
    )
    restored = Skill.from_dict(skill.to_dict())
    assert restored.skill_id == skill.skill_id
    assert restored.state == SkillState.ACTIVE
    assert restored.transfer_history == skill.transfer_history


def test_candidate_rejects_empty_source():
    with pytest.raises(ValueError, match="source_invariant_id"):
        SkillCandidate(candidate_id="SC-1", source_invariant_id="")
