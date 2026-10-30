"""Capability portfolio metrics and CapabilityState sync (Phase 11E-1/2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from core.capability import CapabilityState
from capability.config import CapabilityConfig
from capability.library import CapabilityLibrary
from capability.models import CapabilityType
from capability.states import CapabilityLifecycle
from capability.utility import compute_capability_utility
from evaluation.growth_config import GrowthConfig
from evaluation.growth_metrics import (
    classify_growth_state,
    compute_cgr,
    compute_portfolio_capability,
)
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


@dataclass(slots=True)
class SystemCapabilitySnapshot:
    """System C_t plus optional CGR relative to a previous snapshot."""

    capability_score: float = 0.0
    cgr: float = 0.0
    growth_state: str = "emerging"
    portfolio: CapabilityPortfolioMetrics | None = None
    previous_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_score": self.capability_score,
            "cgr": self.cgr,
            "growth_state": self.growth_state,
            "previous_score": self.previous_score,
            "portfolio": self.portfolio.to_dict() if self.portfolio else None,
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


def compute_system_capability_state(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    *,
    config: CapabilityConfig | None = None,
    growth_config: GrowthConfig | None = None,
    previous_score: float | None = None,
    dt: float | None = None,
    refresh_portfolio: bool = True,
) -> SystemCapabilitySnapshot:
    """Compute system C_t and CGR (when previous_score is provided)."""
    gc = growth_config or GrowthConfig()
    portfolio = compute_capability_portfolio(
        capability_library, skill_library, config, refresh=refresh_portfolio
    )
    score = compute_portfolio_capability(
        capability_library,
        skill_library,
        config=config,
        growth_config=gc,
    )
    cgr = 0.0
    has_history = previous_score is not None
    if has_history:
        cgr = compute_cgr(
            current_c=score, previous_c=float(previous_score), dt=dt or gc.default_dt
        )
    state_label = classify_growth_state(
        cgr, growth_config=gc, has_history=has_history
    )
    return SystemCapabilitySnapshot(
        capability_score=score,
        cgr=cgr,
        growth_state=state_label,
        portfolio=portfolio,
        previous_score=previous_score,
    )


def sync_capability_state(
    state: CapabilityState,
    portfolio: CapabilityPortfolioMetrics,
    capability_ids: Sequence[str],
    *,
    growth: SystemCapabilitySnapshot | None = None,
    write_growth: bool = False,
) -> CapabilityState:
    """Write portfolio summary into CapabilityState.

    When ``write_growth`` is True and ``growth`` is provided, also store
    ``capability_score`` / ``cgr`` / ``growth_state`` (Phase 11E-2 opt-in).
    """
    state.growth_metrics = dict(state.growth_metrics or {})
    state.growth_metrics["mean_capu"] = float(portfolio.mean_capu)
    state.growth_metrics["core_count"] = float(portfolio.core_count)
    state.growth_metrics["emergent_count"] = float(portfolio.emergent_count)
    state.growth_metrics["capability_count"] = float(portfolio.n)
    state.growth_metrics["total_coverage"] = float(portfolio.total_coverage)
    meta = dict(state.metadata or {})
    meta["capability_ids"] = list(capability_ids)
    if write_growth and growth is not None:
        state.growth_metrics["capability_score"] = float(growth.capability_score)
        state.growth_metrics["cgr"] = float(growth.cgr)
        meta["growth_state"] = growth.growth_state
    state.metadata = meta
    return state
