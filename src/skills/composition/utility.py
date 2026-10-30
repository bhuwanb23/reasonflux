"""Composition Utility CU (Phase 11D-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from skills.composition.models import CompositionCandidate
from skills.config import SkillConfig


@dataclass(slots=True)
class CompositionUtilityBreakdown:
    """CU = TransferGain + ReasoningReduction + ReusePotential − CompositionCost."""

    transfer_gain: float = 0.0
    reasoning_reduction: float = 0.0
    reuse_potential: float = 0.0
    composition_cost: float = 0.0
    cu: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "transfer_gain": self.transfer_gain,
            "reasoning_reduction": self.reasoning_reduction,
            "reuse_potential": self.reuse_potential,
            "composition_cost": self.composition_cost,
            "cu": self.cu,
        }


def composition_cost_for(
    skill_count: int, config: SkillConfig | None = None
) -> float:
    config = config or SkillConfig()
    n = max(2, int(skill_count))
    return float(config.compose_cost_base) * float(n - 1)


def compute_cu(
    candidate: CompositionCandidate,
    *,
    transfer_gain: float | None = None,
    reasoning_reduction: float | None = None,
    reuse_potential: float | None = None,
    config: SkillConfig | None = None,
) -> CompositionUtilityBreakdown:
    """Score Composition Utility and write metadata cu_breakdown."""
    config = config or SkillConfig()
    meta = dict(candidate.metadata or {})
    tg = (
        float(transfer_gain)
        if transfer_gain is not None
        else float(meta.get("transfer_gain", candidate.expected_transfer))
    )
    rr = (
        float(reasoning_reduction)
        if reasoning_reduction is not None
        else float(meta.get("reasoning_reduction", 0.0))
    )
    rp = (
        float(reuse_potential)
        if reuse_potential is not None
        else float(meta.get("reuse_potential", candidate.expected_utility))
    )
    cost = float(candidate.composition_cost)
    if cost <= 0:
        cost = composition_cost_for(len(candidate.skill_ids), config)
        candidate.composition_cost = cost
    cu = tg + rr + rp - cost
    breakdown = CompositionUtilityBreakdown(
        transfer_gain=tg,
        reasoning_reduction=rr,
        reuse_potential=rp,
        composition_cost=cost,
        cu=float(cu),
    )
    candidate.cu = breakdown.cu
    meta["cu_breakdown"] = breakdown.to_dict()
    candidate.metadata = meta
    return breakdown
