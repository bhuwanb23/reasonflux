# Phase 2D.4 — Trace Yield Benchmark

This audit reuses the frozen Phase 2C test-output-blind search runs; it performs no new candidate search, ARC test scoring, or accuracy evaluation. One trace is emitted per task/condition, including no-fit cases.

| Condition | Tasks | Candidate programs available | Candidate trials | Valid traces | Successful traces | T4 success / emitted trace | Successful traces per task |
|---|---:|---:|---:|---:|---:|---:|---:|
| Phase 13G historical discovery | 600 | 6,000 main candidate slots | 5,989 main (stability replay work separate) | 600 retrospectively structurally validated; run-time validity flag not trustworthy | 3 | 0.50% | 0.005 |
| S1 / cap 3 | 1,000 | 3,000 | 2,999 | 1,000 | 2 | 0.20% | 0.002 |
| S2 / cap 6 | 1,000 | 6,000 | 5,991 | 1,000 | 5 | 0.50% | 0.005 |
| S3 / cap 15, pool 10 | 1,000 | 10,000 | 9,964 | 1,000 | 10 | 1.00% | 0.010 |
| S4 / all ten | 1,000 | 10,000 | 9,964 | 1,000 | 10 | 1.00% | 0.010 |

The four Phase 2C conditions are repeated views of the same 1,000 task IDs, not 4,000 independent tasks. The Phase 13G stability permutation searches create no additional trace records. `trace generation rate` is therefore 100% but not substantively informative by itself; **successful trace yield** is only 0.2–1.0% depending on search cap.

Coverage, test accuracy, transfer success, and capability are separate outcomes. `Accuracy = NOT_MEASURED_BY_DESIGN`.