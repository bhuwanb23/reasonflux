"""Skill health score HS and bands (Phase 11D-3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.skill import Skill
from skills.config import SkillConfig
from skills.utility import compute_su


@dataclass(slots=True)
class HealthScore:
    """HS ∈ [0, 1] with band and component breakdown."""

    value: float
    band: str  # healthy | stable | weak | critical
    components: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "band": self.band,
            "components": dict(self.components),
        }


def _band(value: float, config: SkillConfig) -> str:
    if value >= config.health_healthy:
        return "healthy"
    if value >= config.health_stable:
        return "stable"
    if value >= config.health_weak:
        return "weak"
    return "critical"


def compute_health(
    skill: Skill, config: SkillConfig | None = None
) -> HealthScore:
    """HS = w_u·SU_norm + w_r·reuse_norm + w_t·TS + w_c·confidence."""
    config = config or SkillConfig()
    su = float(
        skill.utility
        if (skill.metadata or {}).get("utility_breakdown")
        else compute_su(skill, config)
    )
    # Soft-normalize SU around core_su so values map roughly into [0, 1].
    su_norm = max(0.0, min(1.0, su / max(config.core_su, 1e-9)))
    reuse_n = max(
        0.0, min(1.0, int(skill.reuse_count or 0) / max(config.reuse_norm, 1e-9))
    )
    ts = max(0.0, min(1.0, float(skill.transfer_score or 0.0)))
    confidence = max(
        0.0,
        min(1.0, float((skill.metadata or {}).get("confidence", 0.0) or 0.0)),
    )
    raw = (
        config.health_w_u * su_norm
        + config.health_w_r * reuse_n
        + config.health_w_t * ts
        + config.health_w_c * confidence
    )
    value = max(0.0, min(1.0, float(raw)))
    components = {
        "su_norm": su_norm,
        "reuse_norm": reuse_n,
        "ts": ts,
        "confidence": confidence,
    }
    return HealthScore(value=value, band=_band(value, config), components=components)


def apply_recency(score: HealthScore, rw: float) -> HealthScore:
    """Multiply HS by recency weight so stale evidence cannot dominate."""
    rw = max(0.0, min(1.0, float(rw)))
    value = max(0.0, min(1.0, score.value * rw))
    components = dict(score.components)
    components["recency_weight"] = rw
    # Band uses absolute thresholds on the discounted value; config defaults
    # mirror healthy/stable/weak cutoffs without needing a SkillConfig here.
    if value >= 0.75:
        band = "healthy"
    elif value >= 0.5:
        band = "stable"
    elif value >= 0.25:
        band = "weak"
    else:
        band = "critical"
    return HealthScore(value=value, band=band, components=components)
