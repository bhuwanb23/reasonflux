"""Invariant Discovery Theory (IDT) — specification, pattern mining, ranking.

Phase 11C-1 defines what qualifies as an invariant; mining algorithms build
on that specification in later phases.
"""

from core.invariant import Invariant, InvariantConfidence, InvariantEvidence, InvariantType
from invariants.specification import (
    MVP_INVARIANT_TYPES,
    HierarchyLevel,
    InvariantHierarchy,
    InvariantIdentity,
    InvariantPolicy,
    QualificationRule,
    QualificationViolation,
    RejectionCriterion,
    RejectionReason,
    apply_rejection_criteria,
    can_become_skill_candidate,
    classify_invariant_type,
    compute_confidence,
    confidence_from_evidence,
    hierarchy_level_for,
    qualify_invariant,
    require_qualification,
    summarize_specification,
)
from invariants.strength import (
    MINIMUM_INVARIANT_STRENGTH,
    compute_invariant_strength,
    is_above_threshold,
)

__all__ = [
    "MVP_INVARIANT_TYPES",
    "MINIMUM_INVARIANT_STRENGTH",
    "HierarchyLevel",
    "Invariant",
    "InvariantConfidence",
    "InvariantEvidence",
    "InvariantHierarchy",
    "InvariantIdentity",
    "InvariantPolicy",
    "InvariantType",
    "QualificationRule",
    "QualificationViolation",
    "RejectionCriterion",
    "RejectionReason",
    "apply_rejection_criteria",
    "can_become_skill_candidate",
    "classify_invariant_type",
    "compute_confidence",
    "compute_invariant_strength",
    "confidence_from_evidence",
    "hierarchy_level_for",
    "is_above_threshold",
    "qualify_invariant",
    "require_qualification",
    "summarize_specification",
]
