"""Lifecycle state enums and allowed transitions (Phase 11B-2 / 11B-4)."""

from __future__ import annotations

from enum import Enum


class SkillState(str, Enum):
    """Skill lifecycle states (Phase 11D-3)."""

    CANDIDATE = "candidate"
    PROMOTED = "promoted"
    ACTIVE = "active"
    GROWING = "growing"
    CORE = "core"
    DORMANT = "dormant"
    RETIRED = "retired"
    ARCHIVED = "archived"


class InvariantState(str, Enum):
    """Invariant lifecycle states (Phase 11C-1 stages).

    Forward path: candidate → detected → validated → strong →
    transfer_verified → skill_candidate, with archived as terminal.
    """

    CANDIDATE = "candidate"
    DETECTED = "detected"
    VALIDATED = "validated"
    STRONG = "strong"
    TRANSFER_VERIFIED = "transfer_verified"
    SKILL_CANDIDATE = "skill_candidate"
    ARCHIVED = "archived"


class SystemCapabilityPhase(str, Enum):
    """System-level capability phase for CGM analysis."""

    COLD_START = "cold_start"
    EMERGING_SKILLS = "emerging_skills"
    TRANSFER_ENABLED = "transfer_enabled"
    CAPABILITY_GROWTH = "capability_growth"


class TraceLifecyclePhase(str, Enum):
    """Trace lifecycle phases (11B-4)."""

    CREATED = "created"
    STORED = "stored"
    USED_FOR_MINING = "used_for_mining"
    ARCHIVED = "archived"


# Allowed forward transitions (and self-stay). Phase 11D-3 reactivation:
# RETIRED/ARCHIVED → ACTIVE is legal at FSM level; evidence gates live in
# skills.reactivation.reactivate_skill.
SKILL_TRANSITIONS: dict[SkillState, frozenset[SkillState]] = {
    SkillState.CANDIDATE: frozenset(
        {SkillState.CANDIDATE, SkillState.PROMOTED, SkillState.RETIRED}
    ),
    SkillState.PROMOTED: frozenset(
        {SkillState.PROMOTED, SkillState.ACTIVE, SkillState.RETIRED}
    ),
    SkillState.ACTIVE: frozenset(
        {
            SkillState.ACTIVE,
            SkillState.GROWING,
            SkillState.DORMANT,
            SkillState.RETIRED,
        }
    ),
    SkillState.GROWING: frozenset(
        {
            SkillState.GROWING,
            SkillState.ACTIVE,
            SkillState.CORE,
            SkillState.DORMANT,
            SkillState.RETIRED,
        }
    ),
    SkillState.CORE: frozenset(
        {
            SkillState.CORE,
            SkillState.ACTIVE,
            SkillState.GROWING,
            SkillState.DORMANT,
            SkillState.RETIRED,
        }
    ),
    SkillState.DORMANT: frozenset(
        {SkillState.DORMANT, SkillState.ACTIVE, SkillState.RETIRED}
    ),
    SkillState.RETIRED: frozenset(
        {SkillState.RETIRED, SkillState.ARCHIVED, SkillState.ACTIVE}
    ),
    SkillState.ARCHIVED: frozenset({SkillState.ARCHIVED, SkillState.ACTIVE}),
}

INVARIANT_TRANSITIONS: dict[InvariantState, frozenset[InvariantState]] = {
    InvariantState.CANDIDATE: frozenset(
        {InvariantState.CANDIDATE, InvariantState.DETECTED, InvariantState.ARCHIVED}
    ),
    InvariantState.DETECTED: frozenset(
        {InvariantState.DETECTED, InvariantState.VALIDATED, InvariantState.ARCHIVED}
    ),
    InvariantState.VALIDATED: frozenset(
        {
            InvariantState.VALIDATED,
            InvariantState.STRONG,
            InvariantState.TRANSFER_VERIFIED,
            InvariantState.ARCHIVED,
        }
    ),
    InvariantState.STRONG: frozenset(
        {
            InvariantState.STRONG,
            InvariantState.TRANSFER_VERIFIED,
            InvariantState.ARCHIVED,
        }
    ),
    InvariantState.TRANSFER_VERIFIED: frozenset(
        {
            InvariantState.TRANSFER_VERIFIED,
            InvariantState.SKILL_CANDIDATE,
            InvariantState.ARCHIVED,
        }
    ),
    InvariantState.SKILL_CANDIDATE: frozenset(
        {InvariantState.SKILL_CANDIDATE, InvariantState.ARCHIVED}
    ),
    InvariantState.ARCHIVED: frozenset({InvariantState.ARCHIVED}),
}

CAPABILITY_PHASE_TRANSITIONS: dict[SystemCapabilityPhase, frozenset[SystemCapabilityPhase]] = {
    SystemCapabilityPhase.COLD_START: frozenset(
        {SystemCapabilityPhase.COLD_START, SystemCapabilityPhase.EMERGING_SKILLS}
    ),
    SystemCapabilityPhase.EMERGING_SKILLS: frozenset(
        {
            SystemCapabilityPhase.EMERGING_SKILLS,
            SystemCapabilityPhase.TRANSFER_ENABLED,
        }
    ),
    SystemCapabilityPhase.TRANSFER_ENABLED: frozenset(
        {
            SystemCapabilityPhase.TRANSFER_ENABLED,
            SystemCapabilityPhase.CAPABILITY_GROWTH,
        }
    ),
    SystemCapabilityPhase.CAPABILITY_GROWTH: frozenset({SystemCapabilityPhase.CAPABILITY_GROWTH}),
}

TRACE_PHASE_TRANSITIONS: dict[TraceLifecyclePhase, frozenset[TraceLifecyclePhase]] = {
    TraceLifecyclePhase.CREATED: frozenset(
        {TraceLifecyclePhase.CREATED, TraceLifecyclePhase.STORED}
    ),
    TraceLifecyclePhase.STORED: frozenset(
        {TraceLifecyclePhase.STORED, TraceLifecyclePhase.USED_FOR_MINING}
    ),
    TraceLifecyclePhase.USED_FOR_MINING: frozenset(
        {TraceLifecyclePhase.USED_FOR_MINING, TraceLifecyclePhase.ARCHIVED}
    ),
    TraceLifecyclePhase.ARCHIVED: frozenset({TraceLifecyclePhase.ARCHIVED}),
}


class InvalidStateTransitionError(ValueError):
    """Raised when a lifecycle transition is not allowed."""


def can_transition(current: Enum, new: Enum, table: dict) -> bool:
    """Return True if transition current → new is allowed."""
    allowed = table.get(current)
    if allowed is None:
        return False
    return new in allowed


def assert_transition(current: Enum, new: Enum, table: dict, kind: str) -> None:
    """Raise InvalidStateTransitionError if transition is illegal."""
    if not can_transition(current, new, table):
        raise InvalidStateTransitionError(
            f"Invalid {kind} transition: {current.value!r} → {new.value!r}"
        )
