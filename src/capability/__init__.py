"""Capability Representation — Phase 11E-1 (CGM foundation)."""

from capability.config import CapabilityConfig
from capability.constraints import ConstraintResult, validate_capability
from capability.coverage import compute_coverage
from capability.emerge import accept_capabilities, propose_capabilities_from_library
from capability.evidence import (
    CapabilityEvidence,
    append_growth_evidence,
    append_transfer_evidence,
    seed_from_skills,
)
from capability.failures import (
    RepresentationFailure,
    audit_representation,
    detect_fragmentation,
    detect_ghost,
    detect_monolith,
    detect_overlap,
)
from capability.graph import CapabilityGraph
from capability.library import CapabilityLibrary
from capability.lifecycle import advance_capability
from capability.models import Capability, CapabilityType
from capability.portfolio import (
    CapabilityPortfolioMetrics,
    SystemCapabilitySnapshot,
    compute_capability_portfolio,
    compute_system_capability_state,
    sync_capability_state,
)
from capability.scores import compute_confidence, compute_strength, refresh_capability_scores
from capability.states import (
    CAPABILITY_LIFECYCLE_TRANSITIONS,
    CapabilityLifecycle,
    InvalidCapabilityTransitionError,
    assert_capability_transition,
    can_capability_transition,
)
from capability.utility import CapabilityUtilityBreakdown, compute_capability_utility

__all__ = [
    "CAPABILITY_LIFECYCLE_TRANSITIONS",
    "Capability",
    "CapabilityConfig",
    "CapabilityEvidence",
    "CapabilityGraph",
    "CapabilityLibrary",
    "CapabilityLifecycle",
    "CapabilityPortfolioMetrics",
    "CapabilityType",
    "CapabilityUtilityBreakdown",
    "ConstraintResult",
    "InvalidCapabilityTransitionError",
    "RepresentationFailure",
    "SystemCapabilitySnapshot",
    "accept_capabilities",
    "advance_capability",
    "append_growth_evidence",
    "append_transfer_evidence",
    "assert_capability_transition",
    "audit_representation",
    "can_capability_transition",
    "compute_capability_portfolio",
    "compute_capability_utility",
    "compute_confidence",
    "compute_coverage",
    "compute_strength",
    "compute_system_capability_state",
    "detect_fragmentation",
    "detect_ghost",
    "detect_monolith",
    "detect_overlap",
    "propose_capabilities_from_library",
    "refresh_capability_scores",
    "seed_from_skills",
    "sync_capability_state",
    "validate_capability",
]
