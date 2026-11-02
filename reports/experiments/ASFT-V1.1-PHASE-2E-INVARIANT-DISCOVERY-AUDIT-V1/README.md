# ASFT v1.1 Phase 2E — Invariant Discovery Audit

**Package:** `ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1`  
**Decision:** Phase 2E PASS as an audit; empirical invariant readiness is not established; Phase 2 remains BLOCKED.  
**Scope:** Saved Phase 13G traces and saved Phase 2C discovery logs; no new ARC search, test-output parsing, test scoring, or historical outcome changes.

## Start here

- [`phase2E_readiness_review.md`](phase2E_readiness_review.md) — research questions, gates, findings, and decision.
- [`historical_invariant_audit.md`](historical_invariant_audit.md) — where Phase 13G lost invariant yield.
- [`invariant_taxonomy.md`](invariant_taxonomy.md) — I1–I6 evidence definitions.
- [`recurrence_benchmark.md`](recurrence_benchmark.md) — pre-filter pattern recurrence and support distribution.
- [`candidate_generation_audit.md`](candidate_generation_audit.md) — patterns, structures, proposals, rejections, and candidate yield.
- [`support_threshold_audit.md`](support_threshold_audit.md) — current 5, relaxed 2, and strict 6 sensitivity.
- [`invariant_validation_audit.md`](invariant_validation_audit.md) — production validation denominator and separate diagnostic bypass.
- [`discovery_yield_report.md`](discovery_yield_report.md) — end-to-end per-task and per-trace yields.
- [`invariant_failure_localization.md`](invariant_failure_localization.md) — observed bottlenecks and attribution limits.
- [`invariant_reporting_standard.md`](invariant_reporting_standard.md) — required future reporting fields.

## Machine-readable evidence

- [`recurrence_by_signature.csv`](recurrence_by_signature.csv) and [`recurrence_summary.csv`](recurrence_summary.csv) — R1–R4 signature support before miner thresholds.
- [`candidate_generation_audit.csv`](candidate_generation_audit.csv) — threshold sweep by source and stage.
- [`candidate_and_validation_details.csv`](candidate_and_validation_details.csv) — patterns, structures, candidate proposals/rejections, and clearly separated validator diagnostic.
- [`validation_diagnostic_summary.csv`](validation_diagnostic_summary.csv) — validator stage counts; same-trace diagnostic only.
- [`phase2E_audit_manifest.json`](phase2E_audit_manifest.json) — scope and audit status.

## Headline

Only 1–3 successful discovery traces entered the miner per condition. The current support floor of five is unreachable; it yields zero raw patterns. Relaxing support to two produces repeated operation n-grams and two candidate proposals, but those are generic search/verification scaffolding and are rejected by the generation policy. The audit establishes measurable recurrence and threshold attrition—not that meaningful invariants exist or that the miner succeeds on adequate semantic inputs.

## Protocol and provenance

The frozen retrospective protocol is [`experiments/phase2e/preregistration.md`](../../../experiments/phase2e/preregistration.md); the audit runner is [`experiments/phase2e/invariant_audit.py`](../../../experiments/phase2e/invariant_audit.py). Final lineage and QA are recorded in [`source_manifest.json`](source_manifest.json), [`source_hashes.csv`](source_hashes.csv), and [`provenance_validation.md`](provenance_validation.md).