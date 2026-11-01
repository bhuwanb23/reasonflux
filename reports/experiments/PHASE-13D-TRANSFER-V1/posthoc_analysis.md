# Phase 13D post-hoc reporting correction

This analysis reads the saved `task_level.jsonl` and per-seed checkpoint records only. It does not regenerate tasks, rerun a solver, change the frozen protocol, or alter any outcome.

## Why this addendum exists

The frozen report aggregator stored policy-versus-B1 contrasts but its criterion dashboard looked up ASFT-versus-B2/B3/B4 and ASFT-versus-best-single under keys it had not created. Those comparisons appeared as `n=0`/unavailable. In addition, the frozen dashboard treated partial transfer on complex programs as evidence of composition without checking source-component coverage or actual composition activation. The raw task and seed records are intact; this addendum recomputes pairwise statistics and reports coverage explicitly.

## Corrected decision status

```json
{
  "IS_and_SU_association_with_TS": "failed",
  "TS_CGR_association": "passed",
  "ablation_degradation": "failed",
  "full_composition_and_structural_transfer": "unavailable_missing_component_skills",
  "negative_transfer_detection": "passed",
  "outperform_all_mandatory_baselines": "failed",
  "positive_cost_reduction_success_gated": "passed",
  "positive_transfer_across_all_requested_cells": "unavailable",
  "skill_reuse_observed": "passed"
}
```

## Main interpretation

- The training pipeline produced only reflection and rotation skills in all ten seeds. No counting or grouping source skill was born; EXP-TR-03, EXP-TR-06, and all composition/structural cells therefore lack the preregistered required source skills.
- The full composition/structural arm had zero composition candidates and zero active composition applications. Positive TS on EXP-TR-07–11 is partial multi-skill/individual-operation reuse with missing operations solved by the reference fallback, not evidence that a composed skill transferred.
- A4 (no composition) matches ASFT on the EXP-TR-07–11 TS outcomes; no incremental composition effect was observed. The composition endpoint remains unavailable because all required component-skill coverage was absent.
- ASFT-versus-B1/B2/B3/B4 direct paired results are in `posthoc_corrected_criteria.json` and `posthoc_pairwise_baselines.csv`. The compression proxy is still not DreamCoder.
- Capability-growth summary: mean per-seed CGR -0.060000 across 9 evaluable seeds (trend: negative); the positive TS↔CGR correlation is associational and does not imply positive net growth.
- Original `criteria.json`, `aggregate_metrics.json`, and frozen code remain untouched for audit. This addendum is the corrected comparison view; the hash manifest still identifies the frozen run source.

Reanalysis code: `posthoc_reanalysis.py`; this file is not part of the preregistered runtime hash set. No new seed was opened.
