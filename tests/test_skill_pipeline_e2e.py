"""End-to-end SCT: promotable invariants → Active skills."""

from core import Invariant, InvariantEvidence, InvariantState, SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    create_skills_from_invariants,
    record_reuse,
    retrieve_skills,
)


def _reflection():
    return Invariant(
        invariant_id="INV-ref",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.8,
        transfer_contribution=0.8,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=20, transfer_events=4),
        metadata={"reasoning_value": 0.7},
    )


def _verify_output():
    return Invariant(
        invariant_id="INV-ver",
        pattern_signature=["verify_output"],
        frequency=50,
        consistency=1.0,
        generality=1.0,
        transfer_contribution=0.0,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=50, transfer_events=0),
        metadata={"reasoning_value": 0.0},
    )


def test_reflection_promoted_verify_rejected():
    lib = SkillLibrary()
    result = create_skills_from_invariants(
        [_reflection(), _verify_output()], library=lib
    )
    ids = {s.source_invariant_id for s in result.promoted}
    assert "INV-ref" in ids
    assert "INV-ver" not in ids
    assert result.birth_records
    assert result.statistics.promoted >= 1
    rejected_ids = {inv.invariant_id for inv, _ in result.rejected}
    assert "INV-ver" in rejected_ids


def test_scv_threshold_blocks_creation():
    result = create_skills_from_invariants(
        [_reflection()],
        config=SkillConfig(skill_creation_threshold=100.0),
    )
    assert result.promoted == []
    assert result.rejected


def test_ntr_blocks_creation():
    result = create_skills_from_invariants(
        [_reflection()],
        ntr_by_invariant={"INV-ref": 0.9},
    )
    assert result.promoted == []
    assert any("negative_transfer" in reasons for _, reasons in result.rejected)


def test_duplicate_second_skill_blocked():
    lib = SkillLibrary()
    first = create_skills_from_invariants([_reflection()], library=lib)
    assert len(first.promoted) == 1
    twin = Invariant(
        invariant_id="INV-ref-2",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.8,
        transfer_contribution=0.8,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=20, transfer_events=4),
        metadata={"reasoning_value": 0.7},
    )
    second = create_skills_from_invariants([twin], library=lib)
    assert second.promoted == []
    assert any("duplicate" in r for _, r in second.rejected)


def test_retrieve_and_monitor_active_skill():
    lib = SkillLibrary()
    result = create_skills_from_invariants([_reflection()], library=lib)
    skill = result.promoted[0]
    assert skill.state is SkillState.ACTIVE
    hits = retrieve_skills(lib, ["apply_reflection"])
    assert hits and hits[0].skill_id == skill.skill_id
    record_reuse(skill, task_id="t1")
    assert skill.reuse_count == 1
