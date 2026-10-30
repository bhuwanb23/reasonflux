"""Capability lifecycle states and transitions (Phase 11E-1)."""

from __future__ import annotations

from enum import Enum


class CapabilityLifecycle(str, Enum):
    """Per-capability lifecycle (distinct from SystemCapabilityPhase)."""

    EMERGING = "emerging"
    DEVELOPING = "developing"
    ESTABLISHED = "established"
    CORE = "core"
    DECLINING = "declining"
    ARCHIVED = "archived"


CAPABILITY_LIFECYCLE_TRANSITIONS: dict[
    CapabilityLifecycle, frozenset[CapabilityLifecycle]
] = {
    CapabilityLifecycle.EMERGING: frozenset(
        {
            CapabilityLifecycle.EMERGING,
            CapabilityLifecycle.DEVELOPING,
            CapabilityLifecycle.DECLINING,
            CapabilityLifecycle.ARCHIVED,
        }
    ),
    CapabilityLifecycle.DEVELOPING: frozenset(
        {
            CapabilityLifecycle.DEVELOPING,
            CapabilityLifecycle.ESTABLISHED,
            CapabilityLifecycle.DECLINING,
            CapabilityLifecycle.ARCHIVED,
        }
    ),
    CapabilityLifecycle.ESTABLISHED: frozenset(
        {
            CapabilityLifecycle.ESTABLISHED,
            CapabilityLifecycle.CORE,
            CapabilityLifecycle.DECLINING,
            CapabilityLifecycle.ARCHIVED,
        }
    ),
    CapabilityLifecycle.CORE: frozenset(
        {
            CapabilityLifecycle.CORE,
            CapabilityLifecycle.ESTABLISHED,
            CapabilityLifecycle.DECLINING,
            CapabilityLifecycle.ARCHIVED,
        }
    ),
    CapabilityLifecycle.DECLINING: frozenset(
        {
            CapabilityLifecycle.DECLINING,
            CapabilityLifecycle.DEVELOPING,
            CapabilityLifecycle.ARCHIVED,
        }
    ),
    CapabilityLifecycle.ARCHIVED: frozenset({CapabilityLifecycle.ARCHIVED}),
}


class InvalidCapabilityTransitionError(ValueError):
    """Raised when a capability lifecycle transition is illegal."""


def can_capability_transition(
    current: CapabilityLifecycle, new: CapabilityLifecycle
) -> bool:
    allowed = CAPABILITY_LIFECYCLE_TRANSITIONS.get(current)
    return bool(allowed and new in allowed)


def assert_capability_transition(
    current: CapabilityLifecycle, new: CapabilityLifecycle
) -> None:
    if not can_capability_transition(current, new):
        raise InvalidCapabilityTransitionError(
            f"Invalid capability transition: {current.value!r} → {new.value!r}"
        )
