"""Invariant specification (Phase 11C-1).

Formal definition, qualification rules, taxonomy, rejection criteria,
evidence/confidence, identity, lifecycle, and hierarchy.

This module contains *specification logic* (predicates over invariants and
evidence). Mining/ranking algorithms live in later phases.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

from core.invariant import (
    MVP_INVARIANT_TYPES,
    Invariant,
    InvariantConfidence,
    InvariantEvidence,
    InvariantType,
)
from core.states import InvariantState

__all__ = [
    "MVP_INVARIANT_TYPES",
    "Invariant",
    "InvariantConfidence",
    "InvariantEvidence",
    "InvariantType",
    "HierarchyLevel",
    "HierarchyNode",
    "InvariantHierarchy",
    "InvariantIdentity",
    "InvariantPolicy",
    "QualificationRule",
    "QualificationViolation",
    "RejectionCriterion",
    "RejectionReason",
    "SPECIFICATION",
    "apply_rejection_criteria",
    "classify_invariant_type",
    "compute_confidence",
    "confidence_from_evidence",
    "can_become_skill_candidate",
    "hierarchy_level_for",
    "qualify_invariant",
    "require_qualification",
    "summarize_specification",
]


# ---------------------------------------------------------------------------
# Formal definition
# ---------------------------------------------------------------------------

#: The four conditions an invariant must satisfy (all required).
QUALIFICATION_RULES: tuple[str, ...] = (
    "recurrence",
    "stability",
    "generality",
    "transfer_utility",
)

SPECIFICATION: dict[str, Any] = {
    "definition": (
        "An invariant is a recurring reasoning structure that remains stable "
        "across multiple successful task-solving experiences and contributes "
        "to future transfer."
    ),
    "qualification_rules": QUALIFICATION_RULES,
    "taxonomy": [t.value for t in InvariantType],
    "mvp_supported_types": sorted(t.value for t in MVP_INVARIANT_TYPES),
    "lifecycle": [
        InvariantState.CANDIDATE.value,
        InvariantState.DETECTED.value,
        InvariantState.VALIDATED.value,
        InvariantState.TRANSFER_VERIFIED.value,
        InvariantState.SKILL_CANDIDATE.value,
    ],
    "confidence_levels": [c.value for c in InvariantConfidence],
    "hierarchy": ["operations", "patterns", "invariants"],
}


# ---------------------------------------------------------------------------
# Policy (thresholds)
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class InvariantPolicy:
    """Thresholds governing qualification, rejection, and confidence.

    Defaults encode the Phase 11C-1 rules; values are overridable from
    ``configs/thresholds.yaml``.
    """

    # Rule 1 — recurrence
    min_frequency: int = 3
    # Rule 2 — stability
    min_consistency: float = 0.6
    # Rule 3 — generality
    min_task_families: int = 2
    min_generality: float = 0.0
    # Rule 4 — transfer utility
    require_transfer_evidence: bool = True
    min_transfer_events: int = 1

    # Rejection — universal noise
    universal_noise_generality: float = 0.95
    # Rejection — task-specific detail markers
    task_specific_terms: tuple[str, ...] = (
        "red",
        "blue",
        "green",
        "yellow",
        "triangle",
        "square",
        "circle",
        "row 0",
        "col 0",
    )

    # Confidence bands
    moderate_score: float = 0.4
    strong_score: float = 0.7

    def __post_init__(self) -> None:
        if self.min_frequency < 1:
            raise ValueError("min_frequency must be >= 1")
        if not 0.0 <= self.min_consistency <= 1.0:
            raise ValueError("min_consistency must be in [0, 1]")
        if self.min_task_families < 1:
            raise ValueError("min_task_families must be >= 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvariantPolicy:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        if "task_specific_terms" in payload:
            payload["task_specific_terms"] = tuple(payload["task_specific_terms"])
        return cls(**payload)


# ---------------------------------------------------------------------------
# Taxonomy
# ---------------------------------------------------------------------------


def classify_invariant_type(
    pattern_signature: Sequence[str],
    task_family_count: int = 1,
    structural: bool = False,
) -> InvariantType:
    """Classify an invariant per the 11C-1 taxonomy.

    - single operation                        → operational
    - multi-step sequence within one family   → procedural
    - multi-step sequence marked structural   → structural
    - multi-step pattern spanning >= 2 task families → transfer

    Transfer is a cross-family qualifier: a single operation reused across
    families remains operational (its transfer value is captured by evidence,
    not by its taxonomy label).
    """
    steps = [s for s in pattern_signature if str(s).strip()]
    if len(steps) <= 1:
        return InvariantType.OPERATIONAL
    if task_family_count >= 2:
        return InvariantType.TRANSFER
    if structural:
        return InvariantType.STRUCTURAL
    return InvariantType.PROCEDURAL


# ---------------------------------------------------------------------------
# Evidence & confidence
# ---------------------------------------------------------------------------


def confidence_from_evidence(
    evidence: InvariantEvidence,
    consistency: float,
    policy: InvariantPolicy | None = None,
) -> InvariantConfidence:
    """Derive a confidence category from evidence (11C-1 confidence model).

    Score blends recurrence, stability (consistency), family breadth, and
    transfer evidence, each normalized to [0, 1].
    """
    policy = policy or InvariantPolicy()
    recurrence = min(1.0, evidence.observations / max(policy.min_frequency * 3, 1))
    stability = max(0.0, min(1.0, consistency))
    breadth = min(1.0, evidence.task_family_count / max(policy.min_task_families * 2, 1))
    transfer = min(1.0, evidence.transfer_events / 3.0)
    score = (recurrence + stability + breadth + transfer) / 4.0
    return _confidence_for_score(score, policy)


def compute_confidence(
    invariant: Invariant, policy: InvariantPolicy | None = None
) -> InvariantConfidence:
    """Compute the confidence category for an invariant."""
    return confidence_from_evidence(invariant.evidence, invariant.consistency, policy)


def _confidence_for_score(score: float, policy: InvariantPolicy) -> InvariantConfidence:
    if score >= policy.strong_score:
        return InvariantConfidence.STRONG
    if score >= policy.moderate_score:
        return InvariantConfidence.MODERATE
    return InvariantConfidence.WEAK


# ---------------------------------------------------------------------------
# Qualification (the four rules)
# ---------------------------------------------------------------------------


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
    predicate: Any  # Callable[[Invariant, InvariantPolicy], str | None]

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
    families = _family_set(inv)
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
    """Return all failed qualification rules (empty list means qualified).

    Also enforces the MVP taxonomy scope unless ``allow_unsupported_type``.
    """
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


# ---------------------------------------------------------------------------
# Rejection criteria
# ---------------------------------------------------------------------------


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
    predicate: Any  # Callable[[Invariant, InvariantPolicy], bool]

    def matches(self, invariant: Invariant, policy: InvariantPolicy) -> bool:
        return bool(self.predicate(invariant, policy))


def _is_rare(inv: Invariant, policy: InvariantPolicy) -> bool:
    return inv.frequency < policy.min_frequency


def _is_task_specific(inv: Invariant, policy: InvariantPolicy) -> bool:
    if len(_family_set(inv)) < policy.min_task_families:
        return False  # already covered by generality; not a "detail" signal
    lowered = [str(step).lower() for step in inv.pattern_signature]
    for step in lowered:
        for term in policy.task_specific_terms:
            token = term.lower()
            if step == token or step.startswith(f"{token}_") or step.endswith(f"_{token}"):
                return True
            if f" {token} " in f" {step} ":
                return True
        # literal values inside the signature (e.g. "reflect:red_triangle")
        if ":" in step:
            value = step.split(":", 1)[1]
            if any(term.lower() in value for term in policy.task_specific_terms):
                return True
    return False


def _is_universal_noise(inv: Invariant, policy: InvariantPolicy) -> bool:
    return inv.generality >= policy.universal_noise_generality and len(_family_set(inv)) >= policy.min_task_families


def _is_accidental_correlation(inv: Invariant, policy: InvariantPolicy) -> bool:
    """Non-reasoning structure: metadata-only signatures or non-operation steps."""
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
        description="Appears everywhere (e.g. VerifyOutput) and carries little transfer.",
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


# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class InvariantIdentity:
    """Stable identity for an invariant (origin + pattern + families).

    The fingerprint is deterministic over the normalized pattern so the same
    reasoning structure keeps the same id across runs.
    """

    origin: str
    pattern_signature: tuple[str, ...]
    task_families: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.origin or not str(self.origin).strip():
            raise ValueError("origin must be a non-empty string")
        if not self.pattern_signature:
            raise ValueError("pattern_signature must not be empty")

    @property
    def fingerprint(self) -> str:
        payload = {
            "origin": self.origin.strip().lower(),
            "pattern": [str(s).strip().lower() for s in self.pattern_signature],
        }
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]

    @property
    def invariant_id(self) -> str:
        return f"INV-{self.fingerprint}"

    @classmethod
    def from_invariant(cls, invariant: Invariant) -> InvariantIdentity:
        return cls(
            origin=invariant.origin or "unknown",
            pattern_signature=tuple(invariant.pattern_signature),
            task_families=tuple(sorted(_family_set(invariant))),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "origin": self.origin,
            "pattern_signature": list(self.pattern_signature),
            "task_families": list(self.task_families),
            "fingerprint": self.fingerprint,
            "invariant_id": self.invariant_id,
        }


# ---------------------------------------------------------------------------
# Lifecycle advancement
# ---------------------------------------------------------------------------


def can_become_skill_candidate(
    invariant: Invariant,
    policy: InvariantPolicy | None = None,
) -> bool:
    """True when an invariant has transfer-verified evidence for SCT handoff."""
    return (
        invariant.state == InvariantState.TRANSFER_VERIFIED
        and invariant.evidence.transfer_events >= (policy or InvariantPolicy()).min_transfer_events
        and not qualify_invariant(invariant, policy)
    )


# ---------------------------------------------------------------------------
# Hierarchy: operations → patterns → invariants
# ---------------------------------------------------------------------------


class HierarchyLevel(str):
    """Level names in the invariant hierarchy."""

    OPERATION = "operations"
    PATTERN = "patterns"
    INVARIANT = "invariants"


def hierarchy_level_for(invariant: Invariant) -> str:
    """Map an invariant to its hierarchy level."""
    steps = [s for s in invariant.pattern_signature if str(s).strip()]
    if len(steps) <= 1:
        return HierarchyLevel.OPERATION
    if invariant.invariant_type is InvariantType.PROCEDURAL and len(steps) == 2:
        return HierarchyLevel.PATTERN
    return HierarchyLevel.INVARIANT


@dataclass(slots=True)
class HierarchyNode:
    """A node in the operation → pattern → invariant hierarchy."""

    level: str
    label: str
    members: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "label": self.label, "members": list(self.members)}


@dataclass(slots=True)
class InvariantHierarchy:
    """Groups invariants by hierarchy level."""

    nodes: list[HierarchyNode] = field(default_factory=list)

    @classmethod
    def build(cls, invariants: Iterable[Invariant]) -> InvariantHierarchy:
        grouped: dict[str, list[str]] = {
            HierarchyLevel.OPERATION: [],
            HierarchyLevel.PATTERN: [],
            HierarchyLevel.INVARIANT: [],
        }
        for inv in invariants:
            level = hierarchy_level_for(inv)
            grouped.setdefault(level, []).append(inv.invariant_id)
        nodes = [
            HierarchyNode(level=level, label=level, members=members)
            for level, members in grouped.items()
            if members
        ]
        return cls(nodes=nodes)

    def members_at(self, level: str) -> list[str]:
        for node in self.nodes:
            if node.level == level:
                return list(node.members)
        return []

    def to_dict(self) -> dict[str, Any]:
        return {"nodes": [n.to_dict() for n in self.nodes]}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _family_set(invariant: Invariant) -> set[str]:
    families = set(invariant.task_families) | set(invariant.evidence.task_families)
    return {f for f in families if f}


def summarize_specification() -> dict[str, Any]:
    """Return the machine-readable Phase 11C-1 specification."""
    return {
        **SPECIFICATION,
        "qualification_rule_details": [
            {"name": r.name, "description": r.description}
            for r in QUALIFICATION_RULE_SET
        ],
        "rejection_criteria": [
            {"name": c.name, "description": c.description} for c in REJECTION_CRITERIA
        ],
    }
