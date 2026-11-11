"""Reusable composition promotes to Skill with composed_from."""

from core import SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    advance_composition,
    promote_composition,
    retrieve_skills,
)
from skills.composition.evaluate import record_composition_outcome
from skills.composition.models import CompositionCandidate, CompositionState


def test_promote_sets_composed_from_and_is_retrievable():
    cfg = SkillConfig(
        compose_min_reuse_store=2,
        compose_min_reuse_promote=3,
        compose_min_confidence=0.0,
        cu_min=-1.0,
    )
    cand = CompositionCandidate(
        composition_id="reflect+count",
        skill_ids=["reflect", "count"],
        expected_utility=0.5,
        expected_transfer=0.4,
        composition_cost=0.1,
        metadata={
            "triggers": ["reflect", "count"],
            "reasoning_reduction": 0.3,
            "transfer_gain": 0.3,
            "reuse_potential": 0.5,
        },
    )
    for _ in range(3):
        record_composition_outcome(
            cand,
            success=True,
            transfer_gain=0.3,
            reasoning_reduction=0.3,
            task_family="arc",
            config=cfg,
        )
        advance_composition(cand, cfg)
    assert cand.state is CompositionState.REUSABLE

    lib = SkillLibrary()
    skill = promote_composition(cand, lib, cfg)
    assert skill is not None
    assert skill.metadata["composed_from"] == ["reflect", "count"]
    assert skill.state is SkillState.ACTIVE
    assert cand.state is CompositionState.PROMOTED
    assert retrieve_skills(lib)
    assert lib.get("reflect+count") is skill
