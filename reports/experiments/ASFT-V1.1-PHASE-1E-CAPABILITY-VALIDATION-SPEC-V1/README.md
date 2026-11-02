# ASFT v1.1 Phase 1E — Capability Validation Benchmark

**Phase:** `ASFT-V1.1-PHASE-1E`  
**Package:** `ASFT-V1.1-PHASE-1E-CAPABILITY-VALIDATION-SPEC-V1`  
**Scope:** historical audit, benchmark specification, construct-separation interfaces, and decision-rule contracts. No battery tasks or empirical outcomes were run.

## Start here

- [`phase1E_readiness_report.md`](phase1E_readiness_report.md) — executive decision and hard gates.
- [`phase1E_full_audit_report.md`](phase1E_full_audit_report.md) — full source-level CGM audit and evidence boundary.
- [`capability_audit.md`](capability_audit.md) — 13E/14E/14H/14J audit.
- [`capability_definition.md`](capability_definition.md) — behavior-only definition and failure criteria.
- [`capability_taxonomy.md`](capability_taxonomy.md) — C1–C6 behavioral categories.
- [`capability_battery_spec.md`](capability_battery_spec.md) — independent A–F battery.
- [`capability_growth_framework.md`](capability_growth_framework.md) — behavioral growth versus internal score growth.
- [`capability_comparator_spec.md`](capability_comparator_spec.md) — B1–B5 simple baselines, CGR, and the M0/M1 comparison.
- [`capability_metrics.md`](capability_metrics.md) — EBCS, ΔMAE/SOI, decisions, and inference.
- [`capability_dataset_protocol.md`](capability_dataset_protocol.md) — splits, temporal separation, and manifest.
- [`construct_separation_audit.md`](construct_separation_audit.md) — explicit circularity/leakage audit.
- [`capability_preregistration_template.md`](capability_preregistration_template.md) — fields to freeze before confirmation.
- [`phase1E_readiness_checklist.csv`](phase1E_readiness_checklist.csv) — status table.
- [`provenance_validation.md`](provenance_validation.md) — link/hash/format QA results.

## Contract artifacts

- [`phase1E_contract_test_results.csv`](phase1E_contract_test_results.csv) — 31/31 API/schema/decision-rule contracts.
- [`capability_battery_schema.csv`](capability_battery_schema.csv) — A–F scoring inputs.
- [`outcome_response_sanity_report.md`](outcome_response_sanity_report.md) and [`outcome_response_sanity.csv`](outcome_response_sanity.csv) — constructed win/tie/loss decision branches only.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — provenance and hashes.

Re-run from repository root:

```bash
python experiments/phase1e/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1E-CAPABILITY-VALIDATION-SPEC-V1
```

**Evidence warning:** passing contracts show that outcome scoring can be defined without CGR and that result logic permits success, tie, loss, and unavailability. They do not establish capability growth, validate CGR, or constitute an independent task battery.