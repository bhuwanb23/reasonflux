"""Five qualification tests, NTR, duplicates."""

from core import Invariant, InvariantEvidence, InvariantState, Skill, SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    from_invariant,
    qualify_candidate,
)


def _promotable(**kwargs):
    base = dict(
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
    base.update(kwargs)
    return Invariant(**base)


def test_qualify_passes_strong_candidate():
    inv = _promotable()
    cand = from_invariant(inv)
    result = qualify_candidate(cand, invariant=inv, library=SkillLibrary())
    assert result.qualified


def test_ntr_blocks_qualification():
    inv = _promotable()
    cand = from_invariant(inv)
    result = qualify_candidate(
        cand, invariant=inv, library=SkillLibrary(), ntr=0.9, config=SkillConfig()
    )
    assert not result.qualified
    assert "negative_transfer" in result.reasons


def test_duplicate_blocks_qualification():
    inv = _promotable()
    cand = from_invariant(inv)
    lib = SkillLibrary()
    existing = Skill(
        skill_id="existing",
        source_invariant_id="other",
        trigger_conditions=["find_symmetry", "apply_reflection"],
        state=SkillState.ACTIVE,
    )
    lib.add(existing)
    result = qualify_candidate(cand, invariant=inv, library=lib)
    assert not result.qualified
    assert "duplicate" in result.reasons
