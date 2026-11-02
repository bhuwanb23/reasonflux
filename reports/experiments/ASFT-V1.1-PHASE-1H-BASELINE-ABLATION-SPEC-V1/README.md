# ASFT v1.1 Phase 1H — Baseline & Ablation Governance

**Phase ID:** `ASFT-V1.1-PHASE-1H`  
**Package:** `ASFT-V1.1-PHASE-1H-BASELINE-ABLATION-SPEC-V1`  
**Scope:** cross-phase comparator taxonomy, ablation registry, fairness, activation/attribution, interpretation, and governance. No experiment outcomes were generated.

## Start here

- [`phase1H_readiness_report.md`](phase1H_readiness_report.md) — executive status and gates.
- [`phase1H_full_audit_report.md`](phase1H_full_audit_report.md) — integrated audit and specification.
- [`baseline_audit.md`](baseline_audit.md) — historical baseline audit across 13B–13G/14F.
- [`baseline_taxonomy.md`](baseline_taxonomy.md) — B1–B7 family definitions.
- [`mandatory_baselines.md`](mandatory_baselines.md) — BL1–BL7 required comparator registry.
- [`ablation_taxonomy.md`](ablation_taxonomy.md) — A1–A9 and claim map.
- [`mandatory_ablations.md`](mandatory_ablations.md) — manipulation and contribution rules.
- [`fairness_framework.md`](fairness_framework.md) — equal tasks, candidate pool, budgets, storage, compute, horizon, exposure, evaluator.
- [`comparator_activation_audit.md`](comparator_activation_audit.md) — decision divergence and degenerate-comparison rules.
- [`attribution_audit.md`](attribution_audit.md) — when causal/component attribution is justified.
- [`interpretation_rules.md`](interpretation_rules.md) — frozen outcome/claim limits.
- [`baseline_preregistration_template.md`](baseline_preregistration_template.md) — experiment-specific registry and lock fields.
- [`phase1H_readiness_checklist.csv`](phase1H_readiness_checklist.csv) — status by criterion.

## Contracts and provenance

- [`phase1H_contract_test_results.csv`](phase1H_contract_test_results.csv) — contract outcomes.
- [`phase1H_registry_schema.csv`](phase1H_registry_schema.csv) — baseline/ablation registry structure.
- [`outcome_response_sanity.csv`](outcome_response_sanity.csv) and [`outcome_response_report.md`](outcome_response_report.md) — constructed win/tie/loss/ablation/degeneracy paths only.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — source and package provenance.

Run contracts from repository root:

```bash
python experiments/phase1h/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1H-BASELINE-ABLATION-SPEC-V1
```

**Evidence warning:** contract PASS demonstrates only that governance rules and decision branches are implemented; it does not show that ASFT beats any baseline, that a component helps, or that any prior result is causal.