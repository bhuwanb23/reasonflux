# Phase 2E.4 — Candidate Generation Audit

## Pipeline counts

`Patterns Generated` below means patterns surviving the miner's distinct-trace `min_frequency` and `min_cross_trace` filters. Candidate proposals are structures mapped to invariant objects **before** generation rejection. Accepted candidates are the proposals remaining after the frozen rejection criteria.

| Source | Support floor | Traces | Fragments | Raw patterns | Structures | Candidate proposals | Accepted | Rejected |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Phase 13G | Current 5 | 3 | 30 | 0 | 0 | 0 | 0 | 0 |
| Phase 13G | Relaxed 2 | 3 | 30 | 4 | 2 | 2 | 0 | 2 |
| Phase 13G | Strict 6 | 3 | 30 | 0 | 0 | 0 | 0 | 0 |
| S1 | Relaxed 2 / Current 5 / Strict 6 | 1 | 10 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 | 0 |
| S2 | Relaxed 2 / Current 5 / Strict 6 | 2 | 20 | 4 / 0 / 0 | 2 / 0 / 0 | 2 / 0 / 0 | 0 | 2 at S2 |
| S3 | Relaxed 2 / Current 5 / Strict 6 | 3 | 30 | 4 / 0 / 0 | 2 / 0 / 0 | 2 / 0 / 0 | 0 | 2 at S2 |
| S4 | Relaxed 2 / Current 5 / Strict 6 | 3 | 30 | 4 / 0 / 0 | 2 / 0 / 0 | 2 / 0 / 0 | 0 | 2 at S2 |

Every relaxed proposal is rejected by the candidate policy's `universal_noise` criterion. In the current and strict settings, support filtering occurs earlier: no raw pattern reaches structure aggregation or candidate generation. S1 has no recurrence across distinct traces even under the relaxed threshold.

The relaxed proposals are the recurring control-flow fragments described in the recurrence report, not grounded ARC-rule candidates. The rejection uses family labels associated with solution programs, so the `universal_noise` label is reported as a software outcome, not an independently validated content judgment.

## Candidate yield

Relaxed proposal yield is 2 proposals / 3 successful traces (0.667) for Phase 13G and S3/S4, and 2 / 2 (1.0) for S2. **Accepted candidate yield is zero in every condition.** Under the frozen/current path, candidate input to validation is zero; candidate-to-invariant survival is `NOT_ESTIMABLE_ZERO_CANDIDATES`, not a measured 0% validation rate. The full threshold-by-source ledger and reason counts are in `candidate_generation_audit.csv`; item-level signatures are in `candidate_and_validation_details.csv`.