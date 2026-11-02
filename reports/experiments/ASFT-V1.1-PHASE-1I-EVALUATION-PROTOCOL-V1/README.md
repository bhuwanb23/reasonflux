# ASFT v1.1 Phase 1I — Evaluation Protocol

**Phase ID:** `ASFT-V1.1-PHASE-1I`  
**Package:** `ASFT-V1.1-PHASE-1I-EVALUATION-PROTOCOL-V1`  
**Scope:** evaluation constitution for future v1.1 experiments. No empirical result was collected in Phase 1I.

## Start here

- [`phase1I_readiness_report.md`](phase1I_readiness_report.md) — immediate status, gates, and Phase 1 exit decision.
- [`phase1I_full_protocol_report.md`](phase1I_full_protocol_report.md) — integrated report.
- [`evaluation_audit.md`](evaluation_audit.md) — Phase 14A–14J evaluation audit and lessons carried forward.

## Protocol components

- [`experiment_classification_framework.md`](experiment_classification_framework.md) — E1 exploratory, E2 development, E3 confirmatory, E4 replication.
- [`preregistration_template.md`](preregistration_template.md) — before-outcome lock requirements.
- [`endpoint_framework.md`](endpoint_framework.md) — one primary endpoint; secondary/diagnostic separation.
- [`statistical_framework.md`](statistical_framework.md) — independent units, denominators, missingness, uncertainty, exact ties/zero variance.
- [`replication_framework.md`](replication_framework.md) — R1–R4 types and generalization rules.
- [`interpretation_framework.md`](interpretation_framework.md) — frozen interpretation limits.
- [`outcome_state_framework.md`](outcome_state_framework.md) — supported / contradicted / inconclusive / unavailable / non-informative.
- [`reporting_framework.md`](reporting_framework.md) — required reporting fields and anti-selective-reporting rule.
- [`governance_rules.md`](governance_rules.md) — G1–G13 governance rules and amendment controls.
- [`phase1I_readiness_checklist.csv`](phase1I_readiness_checklist.csv) — gate status.

## Contracts and code

- [`phase1I_contract_test_results.csv`](phase1I_contract_test_results.csv) — 67 contract results.
- [`outcome_state_sanity.csv`](outcome_state_sanity.csv) — constructed state fixtures only.
- [`phase1I_protocol_schema.csv`](phase1I_protocol_schema.csv) — required preregistration/report/governance fields.
- [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) — source lineage and SHA-256 fingerprints.

Run the specification contracts from repository root:

```bash
python experiments/phase1i/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1I-EVALUATION-PROTOCOL-V1
```

**Evidence boundary:** contracts test protocol logic and constructed fixtures; they do not run ASFT, validate any scientific construct, establish baseline superiority, or authorize confirmatory evaluation.