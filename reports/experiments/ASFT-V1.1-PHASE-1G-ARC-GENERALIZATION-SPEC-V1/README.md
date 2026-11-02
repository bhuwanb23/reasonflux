# ASFT v1.1 Phase 1G — ARC Generalization Benchmark

**Phase ID:** `ASFT-V1.1-PHASE-1G`  
**Package:** `ASFT-V1.1-PHASE-1G-ARC-GENERALIZATION-SPEC-V1`  
**Scope:** historical ARC audit, diagnostic benchmark specification, construct/protocol contracts. No new ARC evaluation was run.

## Start here

- [`phase1G_readiness_report.md`](phase1G_readiness_report.md) — executive decision and readiness gates.
- [`phase1G_full_audit_report.md`](phase1G_full_audit_report.md) — integrated audit, design, and evidence boundary.
- [`arc_failure_audit.md`](arc_failure_audit.md) — Phase 13G/14G/14H/14I/14J historical ARC audit.
- [`arc_failure_cascade.csv`](arc_failure_cascade.csv) — stage-by-stage observation, denominator, status, and limit.
- [`representation_requirements.md`](representation_requirements.md) — representation contract and “more primitives ≠ better” rule.
- [`coverage_benchmark_spec.md`](coverage_benchmark_spec.md) — separate coverage, trace, discovery, skill, transfer, capability, and accuracy definitions.
- [`discovery_benchmark_spec.md`](discovery_benchmark_spec.md) — trace and candidate discovery.
- [`invariant_benchmark_spec.md`](invariant_benchmark_spec.md) — candidate validity, precision, survival, and zero semantics.
- [`skill_benchmark_spec.md`](skill_benchmark_spec.md) — skill formation independently of transfer.
- [`transfer_benchmark_spec.md`](transfer_benchmark_spec.md) — eligibility, utility, negative transfer, memory qualifier.
- [`capability_benchmark_spec.md`](capability_benchmark_spec.md) — Phase 1E behavioral capability criteria.
- [`arc_accuracy_spec.md`](arc_accuracy_spec.md) — exact, partial, and family accuracy.
- [`protocol_integrity_framework.md`](protocol_integrity_framework.md) — budget, holdout, evaluation isolation, transparency, failure logging.
- [`arc_preregistration_template.md`](arc_preregistration_template.md) — fields to freeze before confirmation.
- [`phase1G_readiness_checklist.csv`](phase1G_readiness_checklist.csv) — requirements and status.

## Contracts and provenance

- [`phase1G_contract_test_results.csv`](phase1G_contract_test_results.csv) — 42/42 stage separation and protocol checks.
- [`arc_pipeline_metric_schema.csv`](arc_pipeline_metric_schema.csv) — stage metrics and denominator rules.
- [`outcome_response_sanity.csv`](outcome_response_sanity.csv) and [`outcome_response_report.md`](outcome_response_report.md) — code-path fixtures only, not task outcomes.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — audited historical sources and package hashes.

Run contracts from repository root:

```bash
python experiments/phase1g/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1G-ARC-GENERALIZATION-SPEC-V1
```

**Evidence warning:** passing contracts establish only that the benchmark can keep stage measures separate and reject known protocol-integrity failures at the API level. They do not establish ARC coverage, mechanism activation, transfer, capability growth, or task accuracy.