"""Skill biography timeline (Phase 11D-3)."""

from core import Skill, SkillState
from skills import apply_lifecycle, build_biography, evaluate_lifecycle, refresh_skill_utility
from skills.lifecycle.biography import append_biography_event
from skills import SkillConfig


def test_biography_birth_growth_transfer_failure_retirement():
    skill = Skill(
        skill_id="b1",
        source_invariant_id="INV-1",
        state=SkillState.ACTIVE,
        abstraction_gain=0.5,
        creation_cost=0.05,
        reuse_count=2,
        metadata={"composition_potential": 0.4},
    )
    refresh_skill_utility(skill)
    bio = build_biography(skill)
    assert bio["birth"]["skill_id"] == "b1"

    append_biography_event(skill, "transfer", {"target": "fam-a"})
    append_biography_event(skill, "failure", {"reason": "ntr"})
    cfg = SkillConfig(growing_ug=0.01)
    decision = evaluate_lifecycle(
        skill, previous_su=skill.utility - 0.1, config=cfg
    )
    apply_lifecycle(skill, decision, config=cfg)

    # Force retire path via biography helper for retirement entry.
    skill.transition_to(SkillState.DORMANT)
    skill.transition_to(SkillState.RETIRED)
    append_biography_event(skill, "retired", {"reason": "low_su"})

    bio = build_biography(skill)
    assert bio["growth_events"]
    assert bio["transfer_events"]
    assert bio["failures"]
    assert bio["retirement"] is not None
    assert bio["peak_utility"] is not None
