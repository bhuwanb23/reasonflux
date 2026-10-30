"""Skill health score components, bands, and recency (Phase 11D-3)."""

import pytest

from core import Skill, SkillState
from skills import SkillConfig, compute_health, refresh_skill_utility
from skills.lifecycle.health import apply_recency


def _strong_skill(**kwargs) -> Skill:
    base = dict(
        skill_id="h1",
        abstraction_gain=0.9,
        transfer_score=0.9,
        creation_cost=0.05,
        reuse_count=8,
        reuse_history=[{"impact": 1.0}] * 8,
        transfer_history=[
            {"success": True, "target_family": f"f{i}"} for i in range(4)
        ],
        state=SkillState.ACTIVE,
        metadata={"confidence": 0.9, "composition_potential": 0.6},
    )
    base.update(kwargs)
    skill = Skill(**base)
    refresh_skill_utility(skill)
    return skill


def test_health_components_and_band():
    skill = _strong_skill()
    hs = compute_health(skill, SkillConfig())
    assert 0.0 <= hs.value <= 1.0
    assert set(hs.components) >= {"su_norm", "reuse_norm", "ts", "confidence"}
    assert hs.band in ("healthy", "stable", "weak", "critical")
    assert hs.band in ("healthy", "stable")


def test_health_critical_when_empty():
    skill = Skill(
        skill_id="h0",
        state=SkillState.ACTIVE,
        creation_cost=1.0,
        metadata={"confidence": 0.0, "composition_potential": 0.0},
    )
    refresh_skill_utility(skill)
    hs = compute_health(skill, SkillConfig())
    assert hs.band in ("weak", "critical")


def test_recency_discounts_stale_evidence():
    skill = _strong_skill()
    hs = compute_health(skill)
    discounted = apply_recency(hs, rw=0.1)
    assert discounted.value == pytest.approx(hs.value * 0.1)
    assert discounted.value < hs.value
    assert "recency_weight" in discounted.components
