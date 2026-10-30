"""Component growth deltas: TG, CCG, CompG, UG (Phase 11E-2)."""

from __future__ import annotations

from typing import Any

from capability.config import CapabilityConfig
from capability.coverage import compute_coverage
from capability.models import Capability
from skills.library import SkillLibrary


def _from_prev(
    previous: Capability | dict[str, Any] | float | None,
    key: str,
    *,
    default: float = 0.0,
) -> float:
    if previous is None:
        return default
    if isinstance(previous, (int, float)):
        return float(previous)
    if isinstance(previous, Capability):
        return float(getattr(previous, key, default) or default)
    if isinstance(previous, dict):
        if key in previous:
            return float(previous[key] or default)
        return default
    return default


def mean_transfer_score(
    capability: Capability, library: SkillLibrary | None = None
) -> float:
    """Mean member-skill transfer_score (CapU TS component)."""
    if library is None:
        return float(capability.metadata.get("mean_ts", 0.0) or 0.0) if capability.metadata else 0.0
    vals: list[float] = []
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is not None:
            vals.append(float(skill.transfer_score or 0.0))
    return sum(vals) / len(vals) if vals else 0.0


def transfer_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
    *,
    library: SkillLibrary | None = None,
) -> float:
    """TG = TS_t − TS_{t−1} (mean transfer_score delta)."""
    current = mean_transfer_score(capability, library)
    if isinstance(previous, Capability):
        prev = mean_transfer_score(previous, library)
    else:
        prev = _from_prev(previous, "mean_ts")
        if isinstance(previous, dict) and "mean_ts" not in previous and "transfer_support" in previous:
            # Back-compat for older snapshots that stored event counts.
            prev = _from_prev(previous, "transfer_support")
    return current - prev


def coverage_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
    *,
    library: SkillLibrary,
    total_families: int | None = None,
    config: CapabilityConfig | None = None,
) -> float:
    """CCG = CCov_t − CCov_{t−1}."""
    current = compute_coverage(
        capability, library=library, total_families=total_families, config=config
    )
    if isinstance(previous, Capability):
        prev = compute_coverage(
            previous, library=library, total_families=total_families, config=config
        )
    else:
        prev = _from_prev(previous, "coverage")
    return float(current) - float(prev)


def _composition_count(capability: Capability, library: SkillLibrary | None) -> float:
    if library is None:
        meta = capability.metadata or {}
        return float(meta.get("composition_count", 0.0) or 0.0)
    n = 0
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        m = skill.metadata or {}
        if m.get("composed_from") or m.get("capability_candidate"):
            n += 1
    return float(n)


def composition_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
    *,
    library: SkillLibrary | None = None,
) -> float:
    """CompG = Compositions_t − Compositions_{t−1}."""
    current = _composition_count(capability, library)
    if isinstance(previous, Capability):
        prev = _composition_count(previous, library)
    else:
        prev = _from_prev(previous, "composition_count")
    return current - prev


def utility_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
) -> float:
    """UG = CapU_t − CapU_{t−1} (or last two utility_history entries)."""
    current = float(capability.utility or 0.0)
    if previous is None:
        hist = list(capability.utility_history or [])
        if len(hist) >= 2:
            return float(hist[-1].get("utility", 0.0)) - float(
                hist[-2].get("utility", 0.0)
            )
        return current
    if isinstance(previous, Capability):
        return current - float(previous.utility or 0.0)
    if isinstance(previous, (int, float)):
        return current - float(previous)
    if isinstance(previous, dict):
        if "utility" in previous:
            return current - float(previous["utility"] or 0.0)
        return current - 0.0
    return current


def component_snapshot(
    capability: Capability,
    *,
    library: SkillLibrary,
    total_families: int | None = None,
    config: CapabilityConfig | None = None,
) -> dict[str, float]:
    """Capture TG/CCG/CompG/UG baselines for a later delta."""
    cov = compute_coverage(
        capability, library=library, total_families=total_families, config=config
    )
    return {
        "mean_ts": mean_transfer_score(capability, library),
        "coverage": float(cov),
        "composition_count": _composition_count(capability, library),
        "utility": float(capability.utility or 0.0),
    }
