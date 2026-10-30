"""Capability lifecycle advance (Phase 11E-1)."""

from __future__ import annotations

from core.states import SkillState
from capability.config import CapabilityConfig
from capability.evidence import transfer_event_count
from capability.models import Capability
from capability.scores import refresh_capability_scores
from capability.states import CapabilityLifecycle
from capability.utility import compute_capability_utility
from skills.library import SkillLibrary


def _member_is_anchor(capability: Capability, library: SkillLibrary) -> bool:
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        if skill.state is SkillState.CORE:
            return True
        if (skill.metadata or {}).get("capability_anchor"):
            return True
    return False


def advance_capability(
    capability: Capability,
    *,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
    previous_utility: float | None = None,
    total_families: int | None = None,
) -> Capability:
    """Advance lifecycle using CapU, confidence, coverage, and transfer evidence."""
    config = config or CapabilityConfig()
    if capability.state is CapabilityLifecycle.ARCHIVED:
        return capability

    prev = (
        float(previous_utility)
        if previous_utility is not None
        else float(capability.utility or 0.0)
    )
    breakdown = compute_capability_utility(
        capability, library, config, total_families=total_families
    )
    refresh_capability_scores(capability, library, config)
    transfers = transfer_event_count(capability, library)
    meta = dict(capability.metadata or {})
    ug = breakdown.capu - prev
    meta["previous_utility"] = breakdown.capu
    meta["utility_growth"] = ug

    # Decline on sustained CapU drop (at most one transition this call).
    if ug <= float(config.decline_ug) and capability.state not in (
        CapabilityLifecycle.EMERGING,
        CapabilityLifecycle.ARCHIVED,
    ):
        if capability.state is not CapabilityLifecycle.DECLINING:
            capability.transition_to(CapabilityLifecycle.DECLINING)
            meta["low_utility_streak"] = 1
        else:
            streak = int(meta.get("low_utility_streak", 0) or 0) + 1
            meta["low_utility_streak"] = streak
            if (
                breakdown.capu < float(config.min_utility)
                and streak >= int(config.archive_low_utility_periods)
            ):
                capability.transition_to(CapabilityLifecycle.ARCHIVED)
        capability.metadata = meta
        return capability

    meta["low_utility_streak"] = 0

    # Ghost guard: no transfer → cannot leave emerging toward established.
    has_transfer = transfers >= int(config.min_transfer_events)
    # At most one forward transition per advance call.
    if capability.state is CapabilityLifecycle.EMERGING:
        if has_transfer and breakdown.capu >= float(config.min_utility):
            capability.transition_to(CapabilityLifecycle.DEVELOPING)
    elif capability.state is CapabilityLifecycle.DEVELOPING:
        if (
            has_transfer
            and capability.confidence >= float(config.min_confidence)
            and capability.coverage >= float(config.min_coverage)
        ):
            capability.transition_to(CapabilityLifecycle.ESTABLISHED)
    elif capability.state is CapabilityLifecycle.ESTABLISHED:
        if (
            capability.strength >= float(config.core_min_strength)
            and capability.confidence >= float(config.core_min_confidence)
        ) or _member_is_anchor(capability, library):
            capability.transition_to(CapabilityLifecycle.CORE)
    elif capability.state is CapabilityLifecycle.DECLINING and ug > 0:
        capability.transition_to(CapabilityLifecycle.DEVELOPING)

    capability.metadata = meta
    return capability
