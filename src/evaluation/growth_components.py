"""Component growth deltas: TG, CCG, CompG, UG (Phase 11E-2)."""

from __future__ import annotations

from typing import Any

from capability.config import CapabilityConfig
from capability.coverage import compute_coverage
from capability.evidence import transfer_event_count
from capability.models import Capability
from skills.library import SkillLibrary


def _snapshot_float(previous: Capability | dict[str, Any] | float | None, key: str) -> float:
    if previous is None:
        return 0.0
    if isinstance(previous, (int, float)):
        return float(previous)
    if isinstance(previous, Capability):
        return float(getattr(previous, key, 0.0) or 0.0)
    return float((previous or {}).get(key, 0.0) or 0.0)


def transfer_support(
    capability: Capability, library: SkillLibrary | None = None
) -> float:
    """Scalar transfer support used for TG."""
    return float(transfer_event_count(capability, library))


def transfer_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
    *,
    library: SkillLibrary | None = None,
) -> float:
    """TG = TS_t − TS_{t−1} (transfer event support delta)."""
    current = transfer_support(capability, library)
    if isinstance(previous, Capability):
        prev = transfer_support(previous, library)
    elif isinstance(previous, dict) and "transfer_support" in previous:
        prev = float(previous["transfer_support"])
    else:
        prev = _snapshot_float(previous, "transfer_support")
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
        prev = float(previous.coverage or 0.0)
    elif isinstance(previous, dict) and "coverage" in previous:
        prev = float(previous["coverage"])
    else:
        prev = _snapshot_float(previous, "coverage")
    return float(current) - prev


def _composition_count(capability: Capability, library: SkillLibrary | None) -> float:
    if library is None:
        # Fall back to evidence / metadata flags on the capability itself.
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
    elif isinstance(previous, dict) and "composition_count" in previous:
        prev = float(previous["composition_count"])
    else:
        prev = _snapshot_float(previous, "composition_count")
    return current - prev


def utility_growth(
    capability: Capability,
    previous: Capability | dict[str, Any] | float | None,
) -> float:
    """UG = CapU_t − CapU_{t−1} (or last two utility_history entries)."""
    current = float(capability.utility or 0.0)
    if isinstance(previous, Capability):
        prev = float(previous.utility or 0.0)
    elif isinstance(previous, dict) and "utility" in previous:
        prev = float(previous["utility"])
    elif isinstance(previous, (int, float)):
        prev = float(previous)
    else:
        hist = list(capability.utility_history or [])
        if len(hist) >= 2:
            return float(hist[-1].get("utility", 0.0)) - float(
                hist[-2].get("utility", 0.0)
            )
        prev = 0.0
    return current - prev


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
        "transfer_support": transfer_support(capability, library),
        "coverage": float(cov),
        "composition_count": _composition_count(capability, library),
        "utility": float(capability.utility or 0.0),
    }
