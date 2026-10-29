"""Promotion, birth event, ACTIVE in library."""

from core import Invariant, InvariantEvidence, InvariantState, SkillState
from skills import SkillLibrary, from_invariant, promote_skill


def _inv():
    return Invariant(
        invariant_id="INV-r",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.8,
        transfer_contribution=0.8,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=20, transfer_events=3),
        metadata={"reasoning_value": 0.7},
    )


def test_promote_creates_active_skill_and_birth():
    inv = _inv()
    lib = SkillLibrary()
    result = promote_skill(from_invariant(inv), invariant=inv, library=lib)
    assert result.promoted
    assert result.skill is not None
    assert result.skill.state is SkillState.ACTIVE
    assert result.birth is not None
    assert result.birth.source_invariant_id == "INV-r"
    assert lib.get(result.skill.skill_id) is result.skill
    assert "confidence" in result.skill.metadata


def test_promote_rejects_non_candidate():
    inv = _inv()
    inv.state = InvariantState.VALIDATED
    result = promote_skill(from_invariant(inv), invariant=inv, library=SkillLibrary())
    assert not result.promoted
