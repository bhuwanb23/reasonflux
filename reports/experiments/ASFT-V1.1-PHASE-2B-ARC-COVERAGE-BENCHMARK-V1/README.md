# ASFT v1.1 Phase 2B — ARC Coverage Benchmark

**Phase:** `ASFT-V1.1-PHASE-2B`  
**Package:** `ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1`  
**Decision:** Phase 2B PASS for coverage-only measurement; Phase 2 overall remains BLOCKED.

## Start here

- [`phase2B_readiness_review.md`](phase2B_readiness_review.md) — gates, results, limitations, and final phase decision.
- [`historical_coverage_audit.md`](historical_coverage_audit.md) — what Phase 13G actually measured and its budget mismatch.
- [`coverage_definition.md`](coverage_definition.md) — frozen finite operational coverage definition.
- [`budgeted_coverage_report.md`](budgeted_coverage_report.md) — production-budget three-candidate result.
- [`fullscan_coverage_report.md`](fullscan_coverage_report.md) — ten-candidate diagnostic result.
- [`trace_yield_report.md`](trace_yield_report.md) — emitted/valid/successful traces, diversity, and mechanical density.
- [`coverage_failure_localization.md`](coverage_failure_localization.md) — F5 observed mixed attrition; F6 causal attribution unresolved.
- [`coverage_reporting_standard.md`](coverage_reporting_standard.md) — mandatory standardized reporting fields.

## Machine-readable outputs

- [`coverage_stage_framework.csv`](coverage_stage_framework.csv) — C1–C7 definitions and observed reach.
- [`task_stage_outcomes.csv`](task_stage_outcomes.csv) — one row per task, paired budgeted/fullscan stage outcomes, no test accuracy.
- [`coverage_summary_by_split.csv`](coverage_summary_by_split.csv) — split and aggregate denominators/rates.
- [`invariant_mining_summary.json`](invariant_mining_summary.json) — actual TraceMiner output and discovery support counts.
- [`run_manifest.json`](run_manifest.json) — frozen run hashes, split counts, and test-output isolation declaration.

## Reproduction and provenance

- Frozen protocol/config and runner: [`experiments/phase2b/preregistration.md`](../../../experiments/phase2b/preregistration.md), [`experiments/phase2b/config.json`](../../../experiments/phase2b/config.json), [`experiments/phase2b/coverage_benchmark.py`](../../../experiments/phase2b/coverage_benchmark.py).
- [`source_manifest.json`](source_manifest.json), [`source_hashes.csv`](source_hashes.csv), and [`provenance_validation.md`](provenance_validation.md) record lineage and QA.

## Headline and boundary

Budgeted found-fit coverage is **2/1,000 (0.20%)**; all-ten fullscan is **10/1,000 (1.00%)**. Trace records were generated and independently validated for all tasks, but only 2/1,000 budgeted traces and 10/1,000 fullscan traces were successful. Actual Phase13G TraceMiner output yielded zero invariants; later chain stages were blocked upstream. **Accuracy was not measured.** `No fit found` is bounded by the current programs/inference/budget and is not proof of semantic impossibility. No ARC task was scored for held-out accuracy, no performance claim or confirmatory theory conclusion is authorized.