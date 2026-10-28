"""Four qualification rules for invariant candidacy (Phase 11C-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.invariant import Invariant
from invariants.specification._util import family_set
from invariants.specification.policy import InvariantPolicy


@dataclass(slots=True)
class QualificationViolation:
    """One failed qualification rule."""

    rule: str
    reason: str

    def to_dict(self) -> dict[str, str]:
        return {"rule": self.rule, "reason": self.reason}


@dataclass(slots=True)
class QualificationRule:
    """A single named predicate used by the qualification pipeline."""

    name: str
    description: str
    predicate: Any

    def check(
        self, invariant: Invariant, policy: InvariantPolicy
    ) -> QualificationViolation | None:
        reason = self.predicate(invariant, policy)
        if reason is None:
            return None
        return QualificationViolation(rule=self.name, reason=reason)


def _rule_recurrence(inv: Invariant, policy: InvariantPolicy) -> str | None:
    if inv.frequency < policy.min_frequency:
        return (
            f"frequency {inv.frequency} < min_frequency {policy.min_frequency} "
            "(one-off observation is not an invariant)"
        )
    return None


def _rule_stability(inv: Invariant, policy: InvariantPolicy) -> str | None:
    if inv.consistency < policy.min_consistency:
        return (
            f"consistency {inv.consistency} < min_consistency "
            f"{policy.min_consistency} (structure is not stable)"
        )
    return None


def _rule_generality(inv: Invariant, policy: InvariantPolicy) -> str | None:
    families = family_set(inv)
    if len(families) < policy.min_task_families:
        return (
            f"task families {len(families)} < min_task_families "
            f"{policy.min_task_families} (too task-specific)"
        )
    if inv.generality < policy.min_generality:
        return f"generality {inv.generality} < min_generality {policy.min_generality}"
    return None


def _rule_transfer_utility(inv: Invariant, policy: InvariantPolicy) -> str | None:
    if not policy.require_transfer_evidence:
        return None
    if inv.evidence.transfer_events < policy.min_transfer_events:
        return (
            f"transfer events {inv.evidence.transfer_events} < "
            f"min_transfer_events {policy.min_transfer_events} "
            "(no evidence of future transfer)"
        )
    return None


QUALIFICATION_RULE_SET: tuple[QualificationRule, ...] = (
    QualificationRule(
        name="recurrence",
        description="The structure appears repeatedly.",
        predicate=_rule_recurrence,
    ),
    QualificationRule(
        name="stability",
        description="The structure remains consistent across occurrences.",
        predicate=_rule_stability,
    ),
    QualificationRule(
        name="generality",
        description="The structure appears beyond a single instance/family.",
        predicate=_rule_generality,
    ),
    QualificationRule(
        name="transfer_utility",
        description="The structure contributes to future task transfer.",
        predicate=_rule_transfer_utility,
    ),
)


def qualify_invariant(
    invariant: Invariant,
    policy: InvariantPolicy | None = None,
    *,
    allow_unsupported_type: bool = False,
) -> list[QualificationViolation]:
    """Return all failed qualification rules (empty list means qualified)."""
    policy = policy or InvariantPolicy()
    violations = [
        violation
        for rule in QUALIFICATION_RULE_SET
        if (violation := rule.check(invariant, policy)) is not None
    ]
    if not allow_unsupported_type and not invariant.is_mvp_supported:
        violations.append(
            QualificationViolation(
                rule="taxonomy_scope",
                reason=(
                    f"invariant type {invariant.invariant_type.value!r} is not in "
                    "the v0.1 MVP scope (operational, procedural)"
                ),
            )
        )
    return violations


def require_qualification(
    invariant: Invariant,
    policy: InvariantPolicy | None = None,
    *,
    allow_unsupported_type: bool = False,
) -> Invariant:
    """Raise ValueError unless the invariant qualifies; return it otherwise."""
    violations = qualify_invariant(
        invariant, policy, allow_unsupported_type=allow_unsupported_type
    )
    if violations:
        detail = "; ".join(f"{v.rule}: {v.reason}" for v in violations)
        raise ValueError(f"Invariant {invariant.invariant_id!r} is unqualified — {detail}")
    return invariant
