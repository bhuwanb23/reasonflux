"""End-to-end sequential composition: reflect+count."""

from core import Skill, SkillState
from skills import SkillConfig, SkillLibrary, try_compose
from skills.composition.compose import ComposeOutcome
from skills.composition.models import CompositionState


def test_reflect_count_compose_e2e():
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="reflect",
            state=SkillState.ACTIVE,
            trigger_conditions=["reflect"],
            utility=0.5,
            transfer_score=0.5,
            metadata={"mvp_category": "reflection", "composition_potential": 0.6},
        )
    )
    lib.add(
        Skill(
            skill_id="count",
            state=SkillState.ACTIVE,
            trigger_conditions=["count"],
            utility=0.4,
            transfer_score=0.4,
            metadata={"mvp_category": "counting", "composition_potential": 0.5},
        )
    )
    cfg = SkillConfig(
        compose_min_reuse_store=2,
        compose_min_reuse_promote=3,
        compose_min_confidence=0.0,
        cu_min=0.0,
    )
    graph = None
    registry: dict = {}
    last = None
    for i in range(3):
        last = try_compose(
            lib,
            ["reflect", "count"],
            config=cfg,
            graph=graph,
            registry=registry,
            outcome=ComposeOutcome(
                success=True,
                transfer_gain=0.3,
                reasoning_reduction=0.25,
                task_family=f"fam{i % 2}",
            ),
            max_apply=1,
        )
        graph = last.graph
        assert last.triggered

    assert last is not None
    assert last.graph is not None
    assert last.graph.edge_count() >= 1
    # After enough reuse, promotion may have occurred.
    assert last.promoted or any(
        c.state in (CompositionState.REUSABLE, CompositionState.PROMOTED)
        for c in last.candidates
    )
    assert len(lib) >= 2  # atomic skills retained; composed may add a third
    assert len(lib) <= cfg.library_capacity
