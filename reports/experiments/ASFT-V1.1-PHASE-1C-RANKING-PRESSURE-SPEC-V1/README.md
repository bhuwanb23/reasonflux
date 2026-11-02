# ASFT v1.1 Phase 1C — Ranking Pressure Benchmark

**Phase:** `ASFT-V1.1-PHASE-1C`  
**Package:** `ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1`  
**Purpose:** create a fair benchmark to test transfer-aware IDT ranking under measurable ranking pressure.  
**Scope:** retrospective failure audit, specification, and synthetic contract validation. No research ranking experiment or confirmatory task outcomes were run.

This package was built from scratch after the Phase 1B audit was accepted. It does not reuse the withdrawn Phase 1C draft.

## Start here

- [`phase1C_readiness_report.md`](phase1C_readiness_report.md) — completion decision and execution boundary.
- [`phase1C_full_audit_report.md`](phase1C_full_audit_report.md) — detailed retrospective audit, specification review, contract results, and limits.
- [`ranking_failure_audit.md`](ranking_failure_audit.md) — retrospective Phase 13B/14 tie audit.
- [`candidate_taxonomy.md`](candidate_taxonomy.md) — eight hidden primary types and controlled B/C quotas.
- [`future_value_definition.md`](future_value_definition.md) — independent portfolio endpoint.
- [`ranking_pressure_design.md`](ranking_pressure_design.md) — divergence definitions and pre-outcome gates.
- [`ranker_competition_spec.md`](ranker_competition_spec.md) — R1–R6 roles and fair comparison.
- [`transfer_ground_truth_protocol.md`](transfer_ground_truth_protocol.md) — truth separation and Oracle isolation.
- [`ranking_metrics.md`](ranking_metrics.md) — primary estimand, SOI, multiplicity, and secondary metrics.
- [`ranking_dataset_protocol.md`](ranking_dataset_protocol.md) — splits, unit, leakage controls, and manifest.
- [`ranking_preregistration_template.md`](ranking_preregistration_template.md) — run-specific fields to freeze before confirmation.
- [`phase1C_readiness_checklist.csv`](phase1C_readiness_checklist.csv) — status table.

## Synthetic contract artifacts

- [`phase1C_contract_test_results.csv`](phase1C_contract_test_results.csv) — 26/26 synthetic contract assertions.
- [`synthetic_pressure_report.md`](synthetic_pressure_report.md) and [`synthetic_pressure_validation.json`](synthetic_pressure_validation.json) — pressure fixture diagnostics.
- [`pairwise_rank_divergence.csv`](pairwise_rank_divergence.csv) — fixture-0 Top-K and full-order divergence matrix.
- [`outcome_response_sanity_report.md`](outcome_response_sanity_report.md) and [`outcome_response_sanity.csv`](outcome_response_sanity.csv) — constructed metric-response loss/tie/win cases.
- [`source_manifest.json`](source_manifest.json) / [`source_hashes.csv`](source_hashes.csv) — provenance and SHA-256 checks.

Re-run from the repository root:

```bash
python experiments/phase1c/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1
```

**Evidence warning:** The 100 panels use a fixed synthetic feature/type recipe; they are contract fixtures, not independent study batches or performance evidence. The Phase 1C design does not authorize confirmatory evaluation, Phase 4, or an SCT experiment.