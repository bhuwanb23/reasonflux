"""Phase 1H frozen baseline, ablation, fairness and outcome-rule contracts."""
from __future__ import annotations
from collections.abc import Mapping, Sequence

BASELINE_TAXONOMY = {
    "B1_NO_LEARNING": "No learned mechanism; retains a fair fixed base solver and task access.",
    "B2_MEMORY_RETRIEVAL": "Episodic or structured memory/retrieval; implementation subtype must be named.",
    "B3_RANDOM": "Random ranking, selection, or action over the same eligible pool and budget.",
    "B4_FREQUENCY": "Frequency-only recurrence/reuse statistics from training data only.",
    "B5_COMPRESSION": "Compression-oriented alternative with exact algorithm named; proxy is not canonical DreamCoder.",
    "B6_HEURISTIC_HYBRID": "Declared simple heuristic (B6a) or explicit hybrid such as memory+frequency (B6b).",
    "B7_ORACLE": "Oracle/upper-bound analysis only; never a deployable competitor or outcome-informed selector.",
}
MANDATORY_BASELINES = (
    "BL1_NO_LEARNING", "BL2_MEMORY_RETRIEVAL", "BL3_RANDOM", "BL4_FREQUENCY",
    "BL5_COMPRESSION", "BL6_HYBRID_MEMORY_FREQUENCY", "BL7_ORACLE_ANALYSIS_ONLY",
)
ABLATIONS = (
    "A1_NO_IDT", "A2_NO_SCT", "A3_NO_SCV", "A4_NO_TRANSFER",
    "A5_NO_CAPABILITY_LAYER", "A6_NO_LIFECYCLE", "A7_NO_COMPOSITION",
    "A8_NO_MEMORY", "A9_NO_ARC_EXTENSION",
)
CLAIM_ABLATION_MAP = {
    "IDT/ranking": ("A1_NO_IDT",),
    "SCT/formation": ("A2_NO_SCT",),
    "SCV/selection": ("A3_NO_SCV",),
    "transfer": ("A4_NO_TRANSFER",),
    "capability measurement/formation": ("A5_NO_CAPABILITY_LAYER",),
    "lifecycle": ("A6_NO_LIFECYCLE",),
    "composition": ("A7_NO_COMPOSITION",),
    "memory contribution": ("A8_NO_MEMORY",),
    "ARC extension": ("A9_NO_ARC_EXTENSION",),
}
FAIRNESS_DIMENSIONS = (
    "same_tasks", "same_candidate_pool", "same_budget", "same_storage_cap",
    "same_compute_cap", "same_horizon", "same_exposure", "same_evaluator",
    "config_runtime_match",
)


def fairness_status(checks: Mapping[str, bool | None]) -> str:
    """Known mismatch fails; missing audit evidence is unavailable, never pass."""
    if set(checks) != set(FAIRNESS_DIMENSIONS):
        return "unavailable"
    values=[checks[k] for k in FAIRNESS_DIMENSIONS]
    if any(v is False for v in values):
        return "fail"
    if any(v is None for v in values):
        return "unavailable"
    return "pass"


def comparator_activation_status(decision_vectors: Mapping[str, Sequence[object]],
                                 opportunity_counts: Mapping[str, int], *,
                                 common_candidate_pool: bool = True) -> str:
    """Flag degeneracy, opportunity mismatch, and decision divergence explicitly."""
    arms=set(decision_vectors)
    if len(arms)<2 or set(opportunity_counts)!=arms:
        return "unavailable"
    if not common_candidate_pool:
        return "unmatched_candidate_pool"
    counts=[int(opportunity_counts[a]) for a in arms]
    if any(n<=0 for n in counts):
        return "unavailable"
    if len(set(counts))!=1:
        return "unmatched_opportunities"
    vectors=[tuple(decision_vectors[a]) for a in sorted(arms)]
    if len({len(v) for v in vectors})!=1 or len(vectors[0])!=counts[0]:
        return "unmatched_decision_horizon"
    if all(v==vectors[0] for v in vectors[1:]):
        return "non_informative_identical_decisions"
    return "informative_decision_divergence"


def baseline_comparison_decision(effect: float, ci_low: float, ci_high: float,
                                 soi: float = 0.02, *, available: bool = True) -> str:
    """Positive effect is ASFT minus comparator; loser and tie are both possible."""
    if not available:
        return "unavailable"
    if ci_low > soi:
        return "asft_wins"
    if ci_high < -soi:
        return "baseline_wins"
    if ci_low >= -soi and ci_high <= soi:
        return "equivalent_tie"
    return "inconclusive"


def gated_comparison_decision(effect: float, ci_low: float, ci_high: float,
                              fairness: str, activation: str, soi: float = 0.02,
                              *, available: bool = True) -> str:
    """Do not attribute a win if fairness or comparator divergence is absent."""
    if not available or fairness == "unavailable":
        return "unavailable"
    if fairness != "pass":
        return "comparison_invalid"
    if activation == "non_informative_identical_decisions":
        return "non_informative_comparison"
    if activation in {"unmatched_candidate_pool", "unmatched_opportunities", "unmatched_decision_horizon"}:
        return "comparison_invalid"
    if activation != "informative_decision_divergence":
        return "unavailable"
    return baseline_comparison_decision(effect,ci_low,ci_high,soi,available=True)


def ablation_contribution_decision(full_minus_ablation: float, ci_low: float,
                                   ci_high: float, soi: float = 0.02, *,
                                   manipulation_verified: bool = True,
                                   available: bool = True) -> str:
    """Positive means full system outperforms ablated system on frozen endpoint."""
    if not available or not manipulation_verified:
        return "unavailable"
    if ci_low > soi:
        return "positive_contribution_under_tested_conditions"
    if ci_high < -soi:
        return "negative_contribution_ablation_better_under_tested_conditions"
    if ci_low >= -soi and ci_high <= soi:
        return "no_measurable_contribution_under_tested_conditions"
    return "inconclusive"


def governance_status(*, preregistered: bool | None,
                      config_locked_before_outcomes: bool | None,
                      endpoints_locked_before_outcomes: bool | None,
                      splits_locked_before_outcomes: bool | None,
                      no_posthoc_changes: bool | None) -> str:
    checks=(preregistered,config_locked_before_outcomes,endpoints_locked_before_outcomes,
            splits_locked_before_outcomes,no_posthoc_changes)
    if any(v is False for v in checks):
        return "fail"
    if any(v is None for v in checks):
        return "unavailable"
    return "pass"
