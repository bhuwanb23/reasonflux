# ASFT v1.1 Phase 2D — Trace Generation Audit

**Package:** `ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1`  
**Decision:** Phase 2D PASS for audit; Phase 2 remains BLOCKED.  
**Scope:** Saved Phase 2C search logs plus Phase 13G historical serialized traces/outcomes. No new ARC search, test-output parsing, test scoring, or accuracy measurement.

## Start here

- [`phase2D_readiness_review.md`](phase2D_readiness_review.md) — outcome, gates, limitations, and decision.
- [`historical_trace_audit.md`](historical_trace_audit.md) — Phase 13G trace generation, retrospective validation, success yield, and invariant attrition.
- [`trace_taxonomy.md`](trace_taxonomy.md) — frozen T1–T6 classifications and distinctions.
- [`trace_lifecycle_report.md`](trace_lifecycle_report.md) — counts and stage-to-stage attrition.
- [`trace_yield_report.md`](trace_yield_report.md) — generated, valid, and successful trace counts.
- [`trace_diversity_report.md`](trace_diversity_report.md) — solution signature, structural, operation, and template diversity.
- [`trace_quality_report.md`](trace_quality_report.md) — demonstration fit, replay consistency, support, and unavailable generality.
- [`invariant_readiness_audit.md`](invariant_readiness_audit.md) — actual miner replay and I3 decision.
- [`trace_failure_localization.md`](trace_failure_localization.md) — observed failure stage and causal limits.
- [`trace_reporting_standard.md`](trace_reporting_standard.md) — requirements for subsequent trace reporting.

## Machine-readable evidence

- [`trace_audit_records.csv`](trace_audit_records.csv) — 4,000 task-condition reconstructed trace records from saved Phase 2C logs.
- [`historical_trace_validation.csv`](historical_trace_validation.csv) — retrospective structural and replay checks for 600 Phase 13G saved records.
- [`trace_taxonomy_counts.csv`](trace_taxonomy_counts.csv), [`trace_lifecycle_summary.csv`](trace_lifecycle_summary.csv), [`trace_diversity_summary.csv`](trace_diversity_summary.csv), [`trace_quality_summary.csv`](trace_quality_summary.csv), and [`invariant_readiness_summary.csv`](invariant_readiness_summary.csv) — grouped metrics.
- [`historical_trace_validation_summary.json`](historical_trace_validation_summary.json), [`trace_mining_details.json`](trace_mining_details.json), and [`trace_audit_manifest.json`](trace_audit_manifest.json) — machine-readable audit status and miner stages.

## Key result

Phase 13G emitted 600 trace records: all 600 saved records pass retrospective structural validation, but only 3 (0.50%) fit their training demonstrations. The generation-time schema flag was hard-coded. The unchanged miner received those three successes, produced 30 fragments and zero raw patterns/candidates. In Phase 2C conditions, successful traces are 2/1,000, 5/1,000, 10/1,000, and 10/1,000; discovery support remains at most one against a support threshold of five. Invariant readiness is **I3 — Not Ready**. Generality, test accuracy, transfer success, capability, and causal mechanism validation are not established.

## Provenance and QA

[`source_manifest.json`](source_manifest.json), [`source_hashes.csv`](source_hashes.csv), and [`provenance_validation.md`](provenance_validation.md) record lineage, hashes, package checks, and scope constraints. The Phase 2D audit runner is [`experiments/phase2d/trace_audit.py`](../../../experiments/phase2d/trace_audit.py).