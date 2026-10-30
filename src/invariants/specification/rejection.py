"""Rejection criteria — what is NOT an invariant (Phase 11C-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.invariant import Invariant
from invariants.specification._util import family_set
from invariants.specification.policy import InvariantPolicy


class RejectionReason(str):
    """Named reasons an invariant candidate is rejected."""

    RARE_EVENT = "rare_event"
    TASK_SPECIFIC = "task_specific_detail"
    UNIVERSAL_NOISE = "universal_noise"
    ACCIDENTAL_CORRELATION = "accidental_correlation"


@dataclass(slots=True)
class RejectionCriterion:
    """A single rejection rule with a name and predicate."""

    name: str
    description: str
    predicate: Any

    def matches(self, invariant: Invariant, policy: InvariantPolicy) -> bool:
        return bool(self.predicate(invariant, policy))


def _is_rare(inv: Invariant, policy: InvariantPolicy) -> bool:
    return inv.frequency < policy.min_frequency


def _is_task_specific(inv: Invariant, policy: InvariantPolicy) -> bool:
    if len(family_set(inv)) < policy.min_task_families:
        return False
    lowered = [str(step).lower() for step in inv.pattern_signature]
    for step in lowered:
        for term in policy.task_specific_terms:
            token = term.lower()
            if step == token or step.startswith(f"{token}_") or step.endswith(f"_{token}"):
                return True
            if f" {token} " in f" {step} ":
                return True
        if ":" in step:
            value = step.split(":", 1)[1]
            if any(term.lower() in value for term in policy.task_specific_terms):
                return True
    return False


def _is_universal_noise(inv: Invariant, policy: InvariantPolicy) -> bool:
    return (
        inv.generality >= policy.universal_noise_generality
        and len(family_set(inv)) >= policy.min_task_families
    )


def _is_accidental_correlation(inv: Invariant, policy: InvariantPolicy) -> bool:
    if not inv.pattern_signature:
        return True
    return all(str(step).startswith("meta:") for step in inv.pattern_signature)


REJECTION_CRITERIA: tuple[RejectionCriterion, ...] = (
    RejectionCriterion(
        name=RejectionReason.RARE_EVENT,
        description="Appeared once / too rarely to be recurring.",
        predicate=_is_rare,
    ),
    RejectionCriterion(
        name=RejectionReason.TASK_SPECIFIC,
        description="Encodes task-specific details (color, shape, position).",
        predicate=_is_task_specific,
    ),
    RejectionCriterion(
        name=RejectionReason.UNIVERSAL_NOISE,
        description="Appears everywhere and carries little transfer.",
        predicate=_is_universal_noise,
    ),
    RejectionCriterion(
        name=RejectionReason.ACCIDENTAL_CORRELATION,
        description="Not a reasoning structure (coincidental co-occurrence).",
        predicate=_is_accidental_correlation,
    ),
)


def apply_rejection_criteria(
    invariant: Invariant, policy: InvariantPolicy | None = None
) -> list[str]:
    """Return names of rejection criteria the invariant violates."""
    policy = policy or InvariantPolicy()
    return [c.name for c in REJECTION_CRITERIA if c.matches(invariant, policy)]
