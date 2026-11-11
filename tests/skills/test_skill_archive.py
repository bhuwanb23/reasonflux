"""Retired → Archived after window; evidence preserved."""

from core import Skill, SkillState
from skills import SkillConfig, apply_lifecycle, evaluate_lifecycle, refresh_skill_utility


def test_retired_archives_after_window_preserves_evidence():
    skill = Skill(
        skill_id="ar1",
        state=SkillState.RETIRED,
        creation_cost=0.5,
        metadata={
            "evidence": {"discovery": [{"k": 1}], "utility": [], "transfer": [], "negative": []},
            "biography": {"birth": {"skill_id": "ar1"}, "retirement": {"kind": "retired"}},
            "lifecycle": {"retired_tasks": 19, "age_tasks": 40},
        },
    )
    refresh_skill_utility(skill)
    cfg = SkillConfig(archive_after_tasks=20)
    decision = evaluate_lifecycle(skill, task_clock=50, config=cfg)
    assert decision.action == "archive"
    apply_lifecycle(skill, decision, config=cfg)
    assert skill.state is SkillState.ARCHIVED
    assert skill.metadata["evidence"]["discovery"] == [{"k": 1}]
    assert skill.metadata["biography"]["retirement"]["kind"] == "archived"
