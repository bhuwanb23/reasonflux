# Phase 2D.3 — Trace Lifecycle Audit

Counts use **task ID per search condition** for task-level survival. Candidate-slot counts are reported separately and are not mixed into task denominators. Discovery-only successful traces are the input to TraceMiner; transfer/holdout successes do not inflate its support.

| Condition | Candidate slots generated | Candidate trials evaluated | Tasks / trace records | Valid traces | Successful traces | Successful discovery traces → TraceMiner | Raw patterns / invariants | Skills |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Phase 13G historical discovery | 6,000 main; 60,000 stability slots separately | 5,989 main; 59,890 stability trials reconstructed | 600 / 600 | 600 retrospective structural validation; historical flag unverified | 3 (0.50%) | 3 | 0 / 0 | 0 |
| S1 cap 3 | 3,000 | 2,999 | 1,000 / 1,000 | 1,000 | 2 (0.20%) | 1 | 0 / 0 | 0 |
| S2 cap 6 | 6,000 | 5,991 | 1,000 / 1,000 | 1,000 | 5 (0.50%) | 2 | 0 / 0 | 0 |
| S3 cap 15, finite pool 10 | 10,000 | 9,964 | 1,000 / 1,000 | 1,000 | 10 (1.00%) | 3 | 0 / 0 | 0 |
| S4 all ten | 10,000 | 9,964 | 1,000 / 1,000 | 1,000 | 10 (1.00%) | 3 | 0 / 0 | 0 |

## Attrition and conditional rates

- **Candidate pool → search attempt:** 100% of task-condition units in S1–S4 had a nonempty candidate pool and at least one candidate trial.
- **Search attempt → trace emitted:** 100%; a structured no-fit trace is also emitted.
- **Trace emitted → structurally valid:** 100% in the independently audited Phase 2C-derived records.
- **Valid → successful:** 0.20%, 0.50%, 1.00%, 1.00% for S1–S4. This is exact demonstration fit, not accuracy.
- **Successful discovery trace → invariant candidate:** 0% in all conditions. Miner input counts were 1, 2, 3, and 3; no candidate emerged.
- **Invariant → skill candidate:** `NOT_ESTIMABLE_ZERO_INVARIANTS`; the skill stage had no input and was not run.

The historical 597/600 no-fit records are valid attempt records but are filtered out before invariant mining. In Phase 2D-derived runs, success traces were reconstructed from Phase 2C logs and fed to the unchanged Phase 13G TraceMiner; Phase 13G outcomes were not changed. Full task-level rows are in `trace_audit_records.csv`; miner stages are in `invariant_readiness_summary.csv`.