# Phase 2E.3 — Recurrence Benchmark

## Measurement

Recurrence is counted **before** support filtering or validation. The unit is an exact contiguous operation n-gram after the frozen trace normalizer, with per-trace deduplication. Frequency is distinct successful discovery trace/task support; fragments and total occurrences are reported separately. Transfer and holdout traces are not pooled into discovery mining.

| Source | Successful discovery traces | Unique signatures | Support ≥2 | Support ≥3 | Support ≥5 | Max support | Support distribution |
|---|---:|---:|---:|---:|---:|---:|---|
| Phase 13G historical | 3 | 22 | 4 | 4 | 0 | 3 | 18 signatures at 1; 4 at 3 |
| S1 | 1 | 10 | 0 | 0 | 0 | 1 | 10 at 1 |
| S2 | 2 | 16 | 4 | 0 | 0 | 2 | 12 at 1; 4 at 2 |
| S3 | 3 | 22 | 4 | 4 | 0 | 3 | 18 at 1; 4 at 3 |
| S4 | 3 | 22 | 4 | 4 | 0 | 3 | 18 at 1; 4 at 3 |

The four recurring historical/S3/S4 signatures are `validate_grid_schema`, `enumerate_candidate_programs`, `verify_demonstrations`, and `validate_grid_schema → enumerate_candidate_programs`. They each occur in all three successful discovery traces (3/3 successes; **3/600 = 0.50%** of discovery tasks). In S2, the same four signatures occur in both successful traces (2/2 successes; **2/600 = 0.33%** of discovery tasks). S1 has one successful trace, so it has no cross-task recurrence.

Thus **operational recurrence exists** before validation, but observed recurrent content is generic search/verification scaffolding. No transformation rule repeats; object/relational semantics are absent. The family labels attached to traces come from the selected program family and do not independently establish cross-semantic-family recurrence.

Full signature-level R1–R4 data are in `recurrence_by_signature.csv`; summary support distributions are in `recurrence_summary.csv`.