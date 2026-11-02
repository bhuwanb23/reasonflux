"""ASFT v1.1 Phase 1I frozen evaluation-governance rules.

This module validates protocol structure and classifies constructed outcome
fixtures. It does not run task benchmarks, statistical models, or experiments.
"""
from __future__ import annotations
from collections.abc import Mapping, Sequence
import math

EXPERIMENT_CLASSES = {
    "E1": "Exploratory — hypothesis generation; not primary-claim evidence.",
    "E2": "Development — benchmark/task/threshold tuning; not primary-claim evidence.",
    "E3": "Confirmatory — preregistered primary scientific test.",
    "E4": "Replication — independent verification under a frozen protocol.",
}
PRIMARY_CLAIM_CLASSES = {"E3", "E4"}
OUTCOME_STATES = {"supported", "contradicted", "inconclusive", "unavailable", "non_informative"}
REPLICATION_TYPES = {"R1", "R2", "R3", "R4"}
REPLICATION_LABELS = {
    "R1": "Within-generator independent seeds/panels/tasks",
    "R2": "Cross-generator independent task generator",
    "R3": "Cross-domain independent domain/tasks",
    "R4": "External benchmark under its independent protocol",
}
GENERALIZATION_REPLICATIONS = {"R2", "R3", "R4"}

REQUIRED_PREREG_FIELDS = (
    "experiment_id", "experiment_class", "research_question", "primary_hypothesis",
    "primary_endpoint", "secondary_endpoints", "diagnostic_metrics", "comparators",
    "independent_unit", "sample_size_rationale", "soi", "missingness_policy",
    "decision_rule", "splits", "budget_and_exposure", "replication_plan",
    "analysis_plan", "source_and_config_hashes", "outcome_access_plan",
    "interpretation_rules_version", "reporting_plan",
)
REQUIRED_REPORT_FIELDS = (
    "experiment_id", "experiment_class", "research_question", "hypothesis",
    "primary_result", "secondary_results", "negative_results", "unavailable_results",
    "limitations", "interpretation", "independent_unit_count", "missingness_count",
    "effect_estimate", "uncertainty_interval", "protocol_deviations", "source_lineage",
)
REQUIRED_GOVERNANCE = (
    "G1_frozen_protocol_unchanged", "G2_failed_gates_not_relabeled",
    "G3_negative_results_retained", "G4_exploratory_not_promoted",
    "G5_unavailable_not_failure", "G6_amendments_versioned",
    "G7_source_lineage_preserved", "sealed_outcomes_and_access_log",
    "corrections_append_only", "no_post_outcome_rule_changes",
)
ENDPOINT_ROLES = {"primary", "secondary", "diagnostic"}
ALLOWED_MISSINGNESS_POLICIES = {"complete_case_with_denominator", "predefined_multiple_imputation", "bounded_sensitivity", "composite_strategy_preregistered"}


def valid_experiment_class(code: str) -> bool:
    return code in EXPERIMENT_CLASSES


def supports_primary_claim(code: str) -> bool:
    return code in PRIMARY_CLAIM_CLASSES


def transition_allowed(old_class: str, new_class: str, *, outcomes_accessed: bool) -> bool:
    """E1/E2 evidence cannot be promoted; classification is frozen after access."""
    if outcomes_accessed and old_class != new_class:
        return False
    if old_class in {"E1", "E2"} and new_class in {"E3", "E4"}:
        return False
    return valid_experiment_class(old_class) and valid_experiment_class(new_class)


def _present(v: object) -> bool:
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, tuple, set, dict)):
        return len(v) > 0
    return True


def preregistration_status(record: Mapping[str, object]) -> str:
    """A template is complete only when every required field is populated."""
    missing = [k for k in REQUIRED_PREREG_FIELDS if not _present(record.get(k))]
    if missing:
        return "incomplete:" + ",".join(missing)
    if not valid_experiment_class(str(record["experiment_class"])):
        return "invalid_class"
    if not supports_primary_claim(str(record["experiment_class"])) and record.get("primary_claim"):
        return "class_cannot_support_primary_claim"
    if not isinstance(record["soi"], (int, float)) or not math.isfinite(float(record["soi"])) or float(record["soi"]) < 0:
        return "invalid_soi"
    if record["missingness_policy"] not in ALLOWED_MISSINGNESS_POLICIES:
        return "invalid_missingness_policy"
    return "complete"


def endpoint_status(endpoints: Sequence[Mapping[str, object]]) -> str:
    """Require one decision-driving endpoint and disjoint secondary/diagnostic roles."""
    if not endpoints:
        return "missing"
    roles = [e.get("role") for e in endpoints]
    ids = [e.get("endpoint_id") for e in endpoints]
    if any(r not in ENDPOINT_ROLES for r in roles):
        return "invalid_role"
    if any(not _present(i) for i in ids) or len(set(ids)) != len(ids):
        return "duplicate_or_missing_id"
    if roles.count("primary") != 1:
        return "require_exactly_one_primary"
    primary = next(e for e in endpoints if e.get("role") == "primary")
    if not _present(primary.get("definition")) or not _present(primary.get("direction")):
        return "incomplete_primary_definition"
    if primary.get("drives_decision") is not True:
        return "primary_not_decision_driving"
    if any(e.get("drives_decision") is True for e in endpoints if e is not primary):
        return "secondary_or_diagnostic_drives_decision"
    return "pass"


def statistical_record_status(record: Mapping[str, object]) -> str:
    """Validate independent-unit, denominator, interval, missingness, tie reporting."""
    required = ("independent_unit", "independent_unit_count", "row_count", "effect_estimate",
                "ci_low", "ci_high", "missing_count", "total_count", "exact_ties_reported",
                "zero_variance_reported")
    if any(k not in record or record[k] is None for k in required):
        return "unavailable"
    try:
        n=int(record["independent_unit_count"]); rows=int(record["row_count"])
        miss=int(record["missing_count"]); total=int(record["total_count"])
        est=float(record["effect_estimate"]); lo=float(record["ci_low"]); hi=float(record["ci_high"])
    except (TypeError, ValueError):
        return "invalid_numeric_record"
    if not _present(record["independent_unit"]) or n <= 0 or rows < n or total < 0 or miss < 0 or miss > total:
        return "invalid_denominator_or_units"
    if not all(math.isfinite(x) for x in (est,lo,hi)) or lo > hi or not (lo <= est <= hi):
        return "invalid_interval"
    if record["exact_ties_reported"] is not True or record["zero_variance_reported"] is not True:
        return "tie_or_zero_variance_not_reported"
    return "pass"


def missingness_status(*, total: int | None, missing: int | None, policy: str | None,
                       max_missing_rate: float | None) -> str:
    if total is None or missing is None or policy is None or max_missing_rate is None:
        return "unavailable"
    if total <= 0 or missing < 0 or missing > total:
        return "unavailable"
    if policy not in ALLOWED_MISSINGNESS_POLICIES or not 0 <= max_missing_rate <= 1:
        return "unavailable"
    return "unavailable" if missing / total > max_missing_rate else "pass"


def classify_outcome(effect: float | None, ci_low: float | None, ci_high: float | None,
                     soi: float, *, hypothesis: str = "positive_superiority",
                     valid: bool = True, informative: bool = True, available: bool = True,
                     independent_units: int | None = None, minimum_units: int = 1) -> str:
    """Classify a preregistered claim; positive effect means ASFT − comparator.

    For positive_superiority, ``supported`` requires the full interval above +SOI;
    ``contradicted`` requires the interval below +SOI (rules out the preregistered
    minimum meaningful benefit); overlaps are inconclusive. Identical decisions
    are non-informative. Fairness/integrity/data failures are unavailable.
    """
    if not available or not valid:
        return "unavailable"
    if not informative:
        return "non_informative"
    if independent_units is None or independent_units <= 0:
        return "unavailable"
    if independent_units < minimum_units:
        return "inconclusive"
    if effect is None or ci_low is None or ci_high is None:
        return "unavailable"
    try:
        est=float(effect); lo=float(ci_low); hi=float(ci_high); margin=float(soi)
    except (TypeError, ValueError):
        return "unavailable"
    if not all(math.isfinite(x) for x in (est,lo,hi,margin)) or lo > hi or not (lo <= est <= hi) or margin < 0:
        return "unavailable"
    if hypothesis == "positive_superiority":
        if lo > margin: return "supported"
        if hi < margin: return "contradicted"
        return "inconclusive"
    if hypothesis == "negative_superiority":
        if hi < -margin: return "supported"
        if lo > -margin: return "contradicted"
        return "inconclusive"
    if hypothesis == "equivalence":
        if lo > -margin and hi < margin: return "supported"
        if lo > margin or hi < -margin: return "contradicted"
        return "inconclusive"
    if hypothesis == "noninferiority":
        if lo > -margin: return "supported"
        if hi < -margin: return "contradicted"
        return "inconclusive"
    return "unavailable"


def replication_status(replication_type: str, *, independent_manifest: bool,
                       independent_source: bool, same_protocol: bool) -> str:
    if replication_type not in REPLICATION_TYPES:
        return "unavailable"
    if not independent_manifest or not independent_source:
        return "not_independent"
    if not same_protocol:
        return "protocol_deviation_requires_new_classification"
    return "valid_replication_type"


def combined_claim_status(confirmatory: str, replication: str, replication_type: str,
                          *, generalization_claim: bool = False) -> str:
    """No single positive result can support a replicated/general claim."""
    if confirmatory not in OUTCOME_STATES or replication not in OUTCOME_STATES:
        return "unavailable"
    if confirmatory == "unavailable" or replication == "unavailable":
        return "unavailable"
    if confirmatory == "non_informative" or replication == "non_informative":
        return "non_informative"
    if generalization_claim and replication_type not in GENERALIZATION_REPLICATIONS:
        return "inconclusive"
    if confirmatory == "supported" and replication == "supported":
        return "supported"
    if confirmatory == "contradicted" and replication == "contradicted":
        return "contradicted"
    if "supported" in {confirmatory, replication} and "contradicted" in {confirmatory, replication}:
        return "inconclusive"
    if "contradicted" in {confirmatory, replication} and "inconclusive" not in {confirmatory, replication}:
        return "contradicted"
    return "inconclusive"


def governance_status(audit: Mapping[str, bool | None]) -> str:
    if set(audit) != set(REQUIRED_GOVERNANCE):
        return "unavailable"
    if any(v is False for v in audit.values()):
        return "fail"
    if any(v is None for v in audit.values()):
        return "unavailable"
    return "pass"


def report_status(record: Mapping[str, object]) -> str:
    missing = [k for k in REQUIRED_REPORT_FIELDS if k not in record or not _present(record[k])]
    if missing:
        return "incomplete:" + ",".join(missing)
    if not record.get("negative_results"):
        return "negative_results_not_explicit"
    if not record.get("unavailable_results"):
        return "unavailable_results_not_explicit"
    return "complete"
