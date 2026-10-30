"""IDT robustness — failure modes, metrics, hard gate (Phase 11C-5)."""

from invariants.robustness.compatibility import (
    CompatibilityMatrix,
    are_compatible,
    compatibility_score,
)
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.diversity import (
    compute_tfd_from_tasks,
    low_diversity_warning,
    meets_multi_family,
)
from invariants.robustness.escalation import (
    EscalationResult,
    FailureLevel,
    apply_escalation_metadata,
    evaluate_escalation,
    record_ntr_violation,
)
from invariants.robustness.explosion import ier_level, monitor_ier, should_restrict_promotion
from invariants.robustness.hard_gate import HardGateResult, confirm_hard_gate, evaluate_hard_gate
from invariants.robustness.illusions import compute_wts, difficulty_factor, meaningful_transfer_weight
from invariants.robustness.metrics import (
    compute_ier,
    compute_tc,
    compute_tfd,
    compute_vst,
    variation_counts_from_metadata,
)
from invariants.robustness.saturation import diminishing_transfer_utility
from invariants.robustness.similarity import jaccard_similarity, should_merge_signatures
from invariants.robustness.trace_quality import trace_weight, weight_from_steps
from invariants.robustness.vst import passes_vst, vst_for_invariant

__all__ = [
    "CompatibilityMatrix",
    "EscalationResult",
    "FailureLevel",
    "HardGateResult",
    "RobustnessConfig",
    "apply_escalation_metadata",
    "are_compatible",
    "compatibility_score",
    "compute_ier",
    "compute_tc",
    "compute_tfd",
    "compute_tfd_from_tasks",
    "compute_vst",
    "compute_wts",
    "confirm_hard_gate",
    "difficulty_factor",
    "diminishing_transfer_utility",
    "evaluate_escalation",
    "evaluate_hard_gate",
    "ier_level",
    "jaccard_similarity",
    "low_diversity_warning",
    "meaningful_transfer_weight",
    "meets_multi_family",
    "monitor_ier",
    "passes_vst",
    "record_ntr_violation",
    "should_merge_signatures",
    "should_restrict_promotion",
    "trace_weight",
    "variation_counts_from_metadata",
    "vst_for_invariant",
    "weight_from_steps",
]
