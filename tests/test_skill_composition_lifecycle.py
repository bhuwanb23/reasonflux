"""Candidate → validated → reusable; single-use not stored as reusable."""

from skills import SkillConfig, advance_composition
from skills.composition.evaluate import record_composition_outcome
from skills.composition.models import CompositionCandidate, CompositionState


def test_lifecycle_requires_reuse_before_reusable():
    cfg = SkillConfig(
        compose_min_successes_validate=1,
        compose_min_reuse_store=2,
        compose_min_confidence=0.0,
        cu_min=0.0,
    )
    cand = CompositionCandidate(
        composition_id="a+b",
        skill_ids=["a", "b"],
        expected_utility=0.5,
        composition_cost=0.05,
        metadata={"reasoning_reduction": 0.3, "transfer_gain": 0.3, "reuse_potential": 0.4},
    )
    record_composition_outcome(
        cand, success=True, transfer_gain=0.3, reasoning_reduction=0.3, config=cfg
    )
    advance_composition(cand, cfg)
    assert cand.state is CompositionState.VALIDATED

    # Still only one use — not reusable / stored.
    assert int(cand.evidence["uses"]) == 1
    assert cand.state is not CompositionState.REUSABLE

    record_composition_outcome(
        cand, success=True, transfer_gain=0.3, reasoning_reduction=0.3, config=cfg
    )
    advance_composition(cand, cfg)
    assert cand.state is CompositionState.REUSABLE
    assert cand.metadata.get("capability_candidate") is True


def test_high_ncr_discards():
    cfg = SkillConfig(compose_ncr_limit=0.3, cu_min=-1.0)
    cand = CompositionCandidate(
        composition_id="a+b",
        skill_ids=["a", "b"],
        composition_cost=0.05,
    )
    record_composition_outcome(cand, success=False, config=cfg)
    record_composition_outcome(cand, success=False, config=cfg)
    advance_composition(cand, cfg)
    assert cand.state is CompositionState.DISCARDED
