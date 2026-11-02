# Phase 2C.5 — Search Trace Benchmark

## Measurement

The frozen Phase 2C runner executed four paired conditions on the same 1,000 training-task IDs and recorded every program-level trial. It emitted one structured task-search trace per primary task/condition (4,000 total), then replayed each search once for integrity (4,000 replay searches, no additional trace records). Test-output fields were not parsed or used.

| Condition | Declared cap | Unique candidates available/task | Candidate trials evaluated | Candidates skipped after first-fit | Candidates omitted by budget | Valid traces | Successful traces / coverage | Invariants |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| S1 | 3 | 3 | 2,999 | 1 | 7,000 | 1,000/1,000 | 2/1,000 (0.20%) | 0 |
| S2 | 6 | 6 | 5,991 | 9 | 4,000 | 1,000/1,000 | 5/1,000 (0.50%) | 0 |
| S3 | 15 | 10 (finite DSL exhausted) | 9,964 | 36 | 0 | 1,000/1,000 | 10/1,000 (1.00%) | 0 |
| S4 | unrestricted (all 10) | 10 | 9,964 | 36 | 0 | 1,000/1,000 | 10/1,000 (1.00%) | 0 |

**Pruning:** no candidate-pruning algorithm or trace-pruning step exists in this path; both pruned counts are zero. First-fit skips are reported separately. S3's requested 15-slot cap is not a 15-candidate grammar: only ten unique Phase 13G programs exist, leaving five cap slots unfillable per task (5,000 aggregate unused slots).

## Reproducibility and integrity

- Primary/replay program sequence, inferred context, selected result, and trial count matched **4,000/4,000** task-condition searches.
- S3 (numeric cap 15) and S4 (all unique programs) produced identical task-level fingerprints on all 1,000 tasks: the finite candidate space is exhausted at ten.
- Phase 13G's 600 primary discovery searches and 6,000 stability permutations were also reconstructed from training demonstrations. Primary choices/trial counts and saved stability fractions matched on all 600 tasks; reconstructed stability work was 59,890 trials. The historical file only recorded ten permutations/task, not each candidate trial.
- Actual Phase 2C process peak RSS was 97.6 MiB under the enforced 2,048 MiB limit. Maximum individual search elapsed time was below 0.487 seconds under the declared 30-second limit. All B1–B6 config/registry/runtime/log checks passed.

## Files and interpretation

`search_execution_log.csv` has 4,000 task-condition rows; `candidate_trial_log.csv` preserves ordered program attempts and outcomes; `replay_validation.csv` contains 4,000 deterministic replay comparisons. `historical_stability_search_log.csv` and `historical_stability_task_audit.csv` hold the reconstruction of Phase 13G's stability loop.

Trace generation is one record per attempt and trace validation is independently checked. Successful traces equal exact demo fits; this does not measure task accuracy, transfer success, or reasoning depth. The Phase 13G historical `trace_schema_valid=True` flag remains a separate hard-coded flag and is not retroactively validated.