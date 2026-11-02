# ASFT v1.1 Phase 1D — Memory Challenge Benchmark

**Phase:** `ASFT-V1.1-PHASE-1D`  
**Package:** `ASFT-V1.1-PHASE-1D-MEMORY-CHALLENGE-SPEC-V1`  
**Scope:** retrospective memory audit, benchmark specification, and schema/design contracts only. No Phase 1D task outcomes or experiment were run.

## Start here

- [`phase1D_readiness_report.md`](phase1D_readiness_report.md) — completion decision and remaining execution gates.
- [`phase1D_full_audit_report.md`](phase1D_full_audit_report.md) — full evidence review, source-level correction, and readiness audit.
- [`memory_audit.md`](memory_audit.md) — decomposition of the Phase 13C memory result.
- [`memory_taxonomy.md`](memory_taxonomy.md) — M1–M5 representation distinctions.
- [`challenge_family_spec.md`](challenge_family_spec.md) — six problem families and expected mechanism pressure.
- [`budget_matching_protocol.md`](budget_matching_protocol.md) — common storage/compute/retrieval/task caps.
- [`memory_comparator_spec.md`](memory_comparator_spec.md) — required arms and primary comparisons.
- [`memory_metrics.md`](memory_metrics.md) — HNU endpoint, SOI, inference, diagnostics, and missingness.
- [`memory_dataset_protocol.md`](memory_dataset_protocol.md) — split design, unit, and replication.
- [`leakage_control_protocol.md`](leakage_control_protocol.md) — storage/retrieval/exposure audit and Family A exception.
- [`memory_preregistration_template.md`](memory_preregistration_template.md) — run-specific fields to freeze.
- [`phase1D_readiness_checklist.csv`](phase1D_readiness_checklist.csv) — completion statuses.

## Contract artifacts

- [`phase1D_contract_test_results.csv`](phase1D_contract_test_results.csv) — design/schema checks only.
- [`challenge_family_design_matrix.csv`](challenge_family_design_matrix.csv) — family definitions and intended challenge.
- [`budget_caps.csv`](budget_caps.csv) — common resource ceilings.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — provenance and SHA-256 inventory.

Run the contracts from repository root:

```bash
python experiments/phase1d/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1D-MEMORY-CHALLENGE-SPEC-V1
```

**Evidence boundary:** a contract pass is not a task outcome. The Phase 1D task solver, budget instrumentation, calibrated cost model, sample size, sealed outcome store, and confirmatory/replication datasets remain pending.