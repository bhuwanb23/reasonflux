"""Capability Growth Metrics (CGM) — measurement and reports."""

from evaluation.growth_checks import (
    GrowthEvidence,
    GrowthFailure,
    RobustnessResult,
    audit_growth,
    build_growth_evidence,
    detect_coverage_inflation,
    detect_growth_without_utility,
    detect_metric_gaming,
    detect_skill_count_illusion,
    detect_transfer_illusion,
)
from evaluation.growth_components import (
    component_snapshot,
    composition_growth,
    coverage_growth,
    mean_transfer_score,
    transfer_growth,
    utility_growth,
)
from evaluation.growth_config import GrowthConfig
from evaluation.growth_metrics import (
    GROWTH_STATES,
    capability_score,
    classify_growth_state,
    compute_ca,
    compute_cg_rate,
    compute_cgr,
    compute_ig,
    compute_portfolio_capability,
    compute_saturation_ratio,
)
from evaluation.skill_metrics import compute_su, skill_utility_breakdown
from evaluation.transfer_metrics import compute_ts
from evaluation.intelligence import (
    intelligence_score,
    compute_igr,
    compute_ia,
    compute_ie,
    compute_elasticity,
)
from evaluation.intelligence_state import (
    IntelligenceState,
    IntelligencePortfolioMetrics,
    compute_system_intelligence_state,
)
from evaluation.intelligence_graph import (
    build_intelligence_graph,
    IntelligenceGraph,
    out_degree,
)
from evaluation.intelligence_checks import (
    audit_intelligence,
    detect_skill_hoarding,
    detect_transfer_collapse,
    detect_fragmentation_persistence,
    detect_composition_failure,
)

__all__ = [
    "GROWTH_STATES",
    "GrowthConfig",
    "GrowthEvidence",
    "GrowthFailure",
    "RobustnessResult",
    "audit_growth",
    "build_growth_evidence",
    "capability_score",
    "classify_growth_state",
    "component_snapshot",
    "composition_growth",
    "compute_ca",
    "compute_cg_rate",
    "compute_cgr",
    "compute_ig",
    "compute_portfolio_capability",
    "compute_saturation_ratio",
    "compute_su",
    "compute_ts",
    "coverage_growth",
    "detect_coverage_inflation",
    "detect_growth_without_utility",
    "detect_metric_gaming",
    "detect_skill_count_illusion",
    "detect_transfer_illusion",
    "mean_transfer_score",
    "skill_utility_breakdown",
    "transfer_growth",
    "utility_growth",
    "intelligence_score",
    "compute_igr",
    "compute_ia",
    "compute_ie",
    "compute_elasticity",
    "IntelligenceState",
    "IntelligencePortfolioMetrics",
    "compute_system_intelligence_state",
    "build_intelligence_graph",
    "IntelligenceGraph",
    "out_degree",
    "audit_intelligence",
    "detect_skill_hoarding",
    "detect_transfer_collapse",
    "detect_fragmentation_persistence",
    "detect_composition_failure",
]
