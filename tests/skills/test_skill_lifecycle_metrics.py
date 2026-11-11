"""SA / SU / UG / RF / TS / HS lifecycle metrics."""

import pytest

from core import Skill, SkillState
from skills import SkillConfig, compute_lifecycle_metrics, refresh_skill_utility


def test_lifecycle_metric_values():
    skill = Skill(
        skill_id="m1",
        abstraction_gain=0.8,
        transfer_score=0.7,
        creation_cost=0.05,
        reuse_count=4,
        reuse_history=[{"impact": 1.0, "task_index": 2}] * 4,
        state=SkillState.ACTIVE,
        metadata={
            "birth_task": 0,
            "composition_potential": 0.5,
            "confidence": 0.6,
            "lifecycle": {"tasks_since_use": 2},
        },
    )
    refresh_skill_utility(skill)
    cfg = SkillConfig()
    metrics = compute_lifecycle_metrics(
        skill, task_clock=10, config=cfg, previous_su=skill.utility - 0.05
    )
    assert metrics.sa == pytest.approx(10.0)
    assert metrics.su == pytest.approx(skill.utility)
    assert metrics.ug == pytest.approx(0.05)
    assert metrics.rf == pytest.approx(4 / 10)
    assert metrics.ts == pytest.approx(0.7)
    assert 0.0 <= metrics.hs <= 1.0
    assert metrics.health is not None
