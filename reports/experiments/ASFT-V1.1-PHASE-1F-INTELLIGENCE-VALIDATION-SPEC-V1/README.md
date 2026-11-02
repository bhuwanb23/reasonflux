# ASFT v1.1 Phase 1F — Intelligence Validation Benchmark

**Phase ID:** `ASFT-V1.1-PHASE-1F`  
**Package:** `ASFT-V1.1-PHASE-1F-INTELLIGENCE-VALIDATION-SPEC-V1`  
**Scope:** historical audit, behavior-first specification, target-separation contracts, comparator/decision/retirement rules. No empirical task outcomes were generated.

## Start here

- [`phase1F_readiness_report.md`](phase1F_readiness_report.md) — executive status and readiness gates.
- [`intelligence_full_audit_report.md`](intelligence_full_audit_report.md) — integrated report and evidence boundary.
- [`intelligence_audit.md`](intelligence_audit.md) — Phase 13E/14E/14H/14I/14J historical audit.
- [`intelligence_definition.md`](intelligence_definition.md) — frozen external, behavior-first definition.
- [`intelligence_taxonomy.md`](intelligence_taxonomy.md) — I1–I6 constructs and measurements.
- [`intelligence_battery_spec.md`](intelligence_battery_spec.md) — independent tests A–F.
- [`adaptation_framework.md`](adaptation_framework.md) — shift/adaptation protocol.
- [`learning_framework.md`](learning_framework.md) — future learning curve and controls.
- [`intelligence_comparator_spec.md`](intelligence_comparator_spec.md) — required baselines, IG, chance/random.
- [`intelligence_metrics.md`](intelligence_metrics.md) — endpoint, SOI, prediction and status rules.
- [`intelligence_dataset_protocol.md`](intelligence_dataset_protocol.md) — split, leakage, and lock protocol.
- [`intelligence_preregistration_template.md`](intelligence_preregistration_template.md) — fields to freeze before confirmation.
- [`intelligence_retirement_rules.md`](intelligence_retirement_rules.md) — when to survive, weaken, retire, rename.
- [`construct_separation_audit.md`](construct_separation_audit.md) — can intelligence be measured with IG disabled?
- [`phase1F_readiness_checklist.csv`](phase1F_readiness_checklist.csv) — requirements and status.

## Contracts and provenance

- [`phase1F_contract_test_results.csv`](phase1F_contract_test_results.csv) — behavior-only API/schema, AULC, decision, and retirement tests.
- [`intelligence_battery_schema.csv`](intelligence_battery_schema.csv) — A–F target schema.
- [`ig_outcome_response_sanity.csv`](ig_outcome_response_sanity.csv) and [`intelligence_outcome_response_report.md`](intelligence_outcome_response_report.md) — constructed decision fixtures only, not evidence.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — historical-source and package provenance.

Run contract checks from repository root:

```bash
python experiments/phase1f/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1F-INTELLIGENCE-VALIDATION-SPEC-V1
```

**Status warning:** 44/44 contract PASS demonstrates only API/schema/code-path behavior. It does not establish intelligence validity, learning, adaptation, capability acquisition, or empirical RQ5 results.