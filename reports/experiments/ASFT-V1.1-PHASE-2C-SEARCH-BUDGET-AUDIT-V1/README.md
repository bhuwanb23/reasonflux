# ASFT v1.1 Phase 2C — Search & Budget Audit

**Phase:** `ASFT-V1.1-PHASE-2C`  
**Package:** `ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1`  
**Decision:** Phase 2C PASS for audit, runtime integrity, and search-sensitivity measurement; Phase 2 overall remains BLOCKED.

## Start here

- [`phase2C_readiness_review.md`](phase2C_readiness_review.md) — questions, gates, results, and boundaries.
- [`historical_search_audit.md`](historical_search_audit.md) — exact Phase 13G declared/executed/logged search paths and budget mismatch.
- [`search_representation_assessment.md`](search_representation_assessment.md) — H1–H4 assessment and next discriminating design.
- [`search_trace_report.md`](search_trace_report.md) — candidate/trace/replay integrity metrics.
- [`budget_sensitivity_report.md`](budget_sensitivity_report.md) — S1–S4 paired coverage result.
- [`runtime_integrity_framework.md`](runtime_integrity_framework.md) — R1–R4 hashing and B1–B6 fail-closed protocol.
- [`search_reporting_standard.md`](search_reporting_standard.md) — frozen future reporting requirements.

## Required deliverables

- [`search_inventory.csv`](search_inventory.csv)
- [`budget_registry.yaml`](budget_registry.yaml)
- [`historical_search_audit.md`](historical_search_audit.md)
- [`runtime_integrity_framework.md`](runtime_integrity_framework.md)
- [`search_trace_report.md`](search_trace_report.md)
- [`budget_sensitivity_report.md`](budget_sensitivity_report.md)
- [`search_representation_assessment.md`](search_representation_assessment.md)
- [`search_reporting_standard.md`](search_reporting_standard.md)
- [`phase2C_readiness_review.md`](phase2C_readiness_review.md)

## Machine-readable execution evidence

- [`search_execution_log.csv`](search_execution_log.csv) — 4,000 primary task-condition rows with B1–B6 values and outcomes.
- [`candidate_trial_log.csv`](candidate_trial_log.csv) — ordered candidate programs, fit decisions, inferred context, and per-task fingerprints.
- [`replay_validation.csv`](replay_validation.csv) — 4,000 cold-cache deterministic replay comparisons, including B1–B6 logging.
- [`historical_stability_search_log.csv`](historical_stability_search_log.csv) and [`historical_stability_task_audit.csv`](historical_stability_task_audit.csv) — train-demo-only reconstruction of Phase 13G's 10 stability permutations/task.
- [`historical_transfer_probe_reconstruction.csv`](historical_transfer_probe_reconstruction.csv) and [`historical_transfer_probe_reconstruction.json`](historical_transfer_probe_reconstruction.json) — train-demo-only reconstruction of program-specific transfer probes.
- [`historical_search_work_reconstruction.json`](historical_search_work_reconstruction.json) — component breakdown of reconstructed Phase 13G solver calls and candidate trials; explicitly not an original run log.
- [`budget_sensitivity_summary.csv`](budget_sensitivity_summary.csv) and [`budget_sensitivity_by_split.csv`](budget_sensitivity_by_split.csv)
- [`budget_audit_record.json`](budget_audit_record.json), [`runtime_integrity_record.json`](runtime_integrity_record.json), [`run_manifest.json`](run_manifest.json), and [`invariant_mining_summary.json`](invariant_mining_summary.json)

## Reproduction and source lineage

Frozen files and runners: [`experiments/phase2c/config.json`](../../../experiments/phase2c/config.json), [`experiments/phase2c/budget_registry.yaml`](../../../experiments/phase2c/budget_registry.yaml), [`experiments/phase2c/preregistration.md`](../../../experiments/phase2c/preregistration.md), [`experiments/phase2c/search_budget_benchmark.py`](../../../experiments/phase2c/search_budget_benchmark.py), and [`experiments/phase2c/replay_historical_stability.py`](../../../experiments/phase2c/replay_historical_stability.py). Phase 2B comparison package: [`ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1`](../ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/README.md).

[`source_manifest.json`](source_manifest.json), [`source_hashes.csv`](source_hashes.csv), and [`provenance_validation.md`](provenance_validation.md) contain package lineage and final QA.

## Headline

Coverage rises from **2/1,000 (0.20%) at cap 3**, to **5/1,000 (0.50%) at cap 6**, to **10/1,000 (1.00%) across all ten unique programs**. Search allowance matters for found demonstration fits, but the finite fullscan remains sparse and yields zero invariants. **Accuracy was not measured**; no causal claim that representation or search is the sole/primary ARC failure cause is established.