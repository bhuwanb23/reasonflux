"""Recency weight and tasks_since_use (Phase 11D-3)."""

import math

import pytest

from core import Skill, SkillState
from skills import SkillConfig
from skills.lifecycle.aging import (
    last_used_index,
    note_task_tick,
    recency_weight,
    tasks_since_use,
)


def test_recency_weight_formula():
    cfg = SkillConfig(decay_lambda=0.01)
    assert recency_weight(0, cfg) == pytest.approx(1.0)
    t = 10.0
    assert recency_weight(t, cfg) == pytest.approx(math.exp(-0.01 * t))


def test_last_used_index_from_history():
    skill = Skill(
        skill_id="a1",
        state=SkillState.ACTIVE,
        reuse_history=[{"task_index": 3}, {"task_index": 7}],
        transfer_history=[{"task_index": 5}],
    )
    assert last_used_index(skill) == 7


def test_tasks_since_use_ticks():
    skill = Skill(skill_id="a2", state=SkillState.ACTIVE)
    assert note_task_tick(skill, used=False) == 1
    assert note_task_tick(skill, used=False) == 2
    assert tasks_since_use(skill) == 2
    assert note_task_tick(skill, used=True) == 0
    assert tasks_since_use(skill) == 0
