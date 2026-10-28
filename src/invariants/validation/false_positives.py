"""False-positive handling — variation survival (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.specification.policy import InvariantPolicy


def has_task_specific_literals(
    invariant: Invariant, policy: InvariantPolicy | None = None
) -> bool:
    """True when the pattern encodes color/shape/position literals."""
    policy = policy or InvariantPolicy()
    lowered = [str(step).lower() for step in invariant.pattern_signature]
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


def failed_variation_survival(invariant: Invariant) -> bool:
    """True when metadata records failed color/shape/position probes."""
    failed = (invariant.metadata or {}).get("failed_variations") or []
    if not failed:
        return False
    markers = {"color", "shape", "position"}
    return any(str(item).lower() in markers for item in failed)


def is_false_positive(
    invariant: Invariant, policy: InvariantPolicy | None = None
) -> list[str]:
    """Return false-positive reasons (empty list means not a false positive)."""
    reasons: list[str] = []
    if has_task_specific_literals(invariant, policy):
        reasons.append("task_specific_literal")
    if failed_variation_survival(invariant):
        reasons.append("failed_variation_survival")
    return reasons
