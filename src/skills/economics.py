"""Promotion economics helpers — EFU vs lifetime cost (Phase 11D-2).

Advisory only: does not replace the 11D-1 SCV birth gate.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.skill import SkillCandidate
from skills.config import SkillConfig


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


@dataclass(slots=True)
class EconomicsProjection:
    """Expected future utility vs lifetime cost for a candidate."""

    expected_future_utility: float
    lifetime_cost: float
    worthwhile: bool

    def to_dict(self) -> dict:
        return {
            "expected_future_utility": self.expected_future_utility,
            "lifetime_cost": self.lifetime_cost,
            "worthwhile": self.worthwhile,
        }


def expected_future_utility(
    candidate: SkillCandidate, config: SkillConfig | None = None
) -> float:
    """Project post-birth SU proxy from candidate fields."""
    config = config or SkillConfig()
    reuse = float(candidate.reuse or candidate.expected_reuse or 0.0)
    ts = float(candidate.transfer_score or candidate.expected_transfer or 0.0)
    ag = float(candidate.abstraction_gain or 0.0)
    cp = float((candidate.metadata or {}).get("composition_potential", config.default_cp))
    # Mirror SU benefits without observed histories: RCG≈AG, TV≈TS, RV≈reuse, CP.
    return _clamp01(ag) + _clamp01(ts) + _clamp01(cp) + _clamp01(reuse)


def lifetime_cost(
    candidate: SkillCandidate, config: SkillConfig | None = None
) -> float:
    """Creation + expected maintenance (NR assumed zero at birth)."""
    config = config or SkillConfig()
    cc = float(candidate.creation_cost)
    if cc < 0:
        cc = config.default_creation_cost
    return max(0.0, cc + float(config.base_maintenance))


def evaluate_promotion_economics(
    candidate: SkillCandidate, config: SkillConfig | None = None
) -> EconomicsProjection:
    """True when ExpectedFutureUtility > LifetimeCost."""
    config = config or SkillConfig()
    efu = expected_future_utility(candidate, config)
    cost = lifetime_cost(candidate, config)
    return EconomicsProjection(
        expected_future_utility=efu,
        lifetime_cost=cost,
        worthwhile=efu > cost,
    )
