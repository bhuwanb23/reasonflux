"""Capability portfolio metrics and CapabilityState sync (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from core.capability import CapabilityState
from capability.config import CapabilityConfig
from capability.library import CapabilityLibrary
from capability.models import Capability, CapabilityType
from capability.states import CapabilityLifecycle
from capability.utility import compute_capability_utility
from skills.library import SkillLibrary


@dataclass(slots=True)
class CapabilityPortfolioMetrics:
    mean_capu: float = 0.0
    total_coverage: float = 0.0
    core_count: int = 0
    emergent_count: int = 0
    n: int = 0

    def to_dict(self) -> dict[str, float | int]:
        return {
            "mean_capu": self.mean_capu,
            "total_coverage": self.total_coverage,
            "core_count": self.core_count,
            "emergent_count": self.emergent_count,
            "n": self.n,
        }


def compute_capability_portfolio(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    config: CapabilityConfig | None = None,
    *,
    refresh: bool = True,
) -> CapabilityPortfolioMetrics:
    """Aggregate CapU / coverage over non-archived capabilities."""
    config = config or CapabilityConfig()
    caps = [
        c
        for c in capability_library.list_capabilities()
        if c.state is not CapabilityLifecycle.ARCHIVED
    ]
    if refresh:
        for cap in caps:
            compute_capability_utility(cap, skill_library, config)
    if not caps:
        return CapabilityPortfolioMetrics()
    mean_capu = sum(float(c.utility) for c in caps) / len(caps)
    total_coverage = sum(float(c.coverage) for c in caps)
    # Soft-cap reported coverage at 1.0 for portfolio summary.
    total_coverage = min(1.0, total_coverage)
    core_count = sum(1 for c in caps if c.state is CapabilityLifecycle.CORE)
    emergent_count = sum(
        1 for c in caps if c.capability_type is CapabilityType.EMERGENT
    )
    return CapabilityPortfolioMetrics(
        mean_capu=mean_capu,
        total_coverage=total_coverage,
        core_count=core_count,
        emergent_count=emergent_count,
        n=len(caps),
    )


def sync_capability_state(
    state: CapabilityState,
    portfolio: CapabilityPortfolioMetrics,
    capability_ids: Sequence[str],
) -> CapabilityState:
    """Write portfolio summary into CapabilityState (not CGR — that is 11E-2)."""
    state.growth_metrics = dict(state.growth_metrics or {})
    state.growth_metrics["mean_capu"] = float(portfolio.mean_capu)
    state.growth_metrics["core_count"] = float(portfolio.core_count)
    state.growth_metrics["emergent_count"] = float(portfolio.emergent_count)
    state.growth_metrics["capability_count"] = float(portfolio.n)
    state.growth_metrics["total_coverage"] = float(portfolio.total_coverage)
    meta = dict(state.metadata or {})
    meta["capability_ids"] = list(capability_ids)
    state.metadata = meta
    return state
