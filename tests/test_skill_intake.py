"""Stage 1 intake for promotable invariants."""

from core import Invariant, InvariantEvidence, InvariantState
from skills import SkillConfig, intake_invariant, is_promotable_invariant


def _inv(state, *, freq=10, c=0.9, g=0.5, t=0.7, obs=10):
    return Invariant(
        invariant_id="INV-r",
        pattern_signature=["apply_reflection"],
        frequency=freq,
        consistency=c,
        generality=g,
        transfer_contribution=t,
        state=state,
        evidence=InvariantEvidence(observations=obs, transfer_events=2),
    )


def test_only_skill_candidate_is_promotable():
    assert is_promotable_invariant(_inv(InvariantState.SKILL_CANDIDATE))
    assert not is_promotable_invariant(_inv(InvariantState.VALIDATED))


def test_intake_accepts_strong_skill_candidate():
    result = intake_invariant(_inv(InvariantState.SKILL_CANDIDATE))
    assert result.accepted


def test_intake_rejects_low_frequency():
    result = intake_invariant(
        _inv(InvariantState.SKILL_CANDIDATE, freq=1, obs=1),
        SkillConfig(),
    )
    assert not result.accepted
    assert "frequency" in result.reasons or "evidence" in result.reasons
