"""False-positive handling — variation survival (Phase 11C-3 / 11C-5)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.vst import passes_vst, vst_for_invariant
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
    """True when metadata records failed color/shape/position/count probes."""
    failed = (invariant.metadata or {}).get("failed_variations") or []
    if not failed:
        return False
    markers = {"color", "shape", "position", "count"}
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
    if not passes_vst(invariant, RobustnessConfig()):
        reasons.append("low_vst")
    return reasons
