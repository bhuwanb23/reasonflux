# Phase 2C.1 — Historical Phase 13G Search and Budget Audit

## Executive finding

The principal mismatch is confirmed: **the frozen config declares 3 candidate trials per task, while discovery executes 10 per solver call** because `runner.discover()` defaults to `budget=10` and `run_phase()` calls it without an override. The scored arms use 3; coverage scans use 10. Phase 14 correctly cautioned that this mismatch does not explain all low ARC coverage, but it makes the declared discovery budget an invalid description of what ran.

The search is a deterministic, one-level, fixed-order enumeration of ten whole-grid programs. It infers parameters from training demonstrations, accepts the first exact fit, and stops. No composition, AST search, backtracking, or candidate-set ambiguity resolution is implemented.

## B1–B6: configured, executed, logged

| Budget | Config/declared | Executed in Phase 13G | Logged / evidence | Audit status |
|---|---|---|---|---|
| **B1 Candidate budget** | 3 candidate trials/task (`dsl.per_task_candidate_budget`, `reasoning_cost.budget`) | Discovery: 10 main candidates and up to 10 in each of 10 stability permutations. Scored arms: 3. Transfer program probes: one candidate for each of 10 programs/task; fullscan: 10. | Scored-arm `candidate_trials` in 2,000 task-outcome rows. Discovery main trial count is recoverable as trace outcome cost. Stability per-permutation trials were not in original logs; Phase 2C replay reconstructs 59,890. Coverage-scan task-level trial counts were not retained. | **Mismatch; partial logging** |
| **B2 Search depth** | No explicit depth field | One flat candidate program at a time; no composition/deeper program AST | Source implementation identifies depth=1; no depth log per task | Consistent structure, missing explicit budget/log field |
| **B3 Trace budget** | 10 stability permutations; no global trace cap specified | 600 discovery traces (one/task); 6,000 extra stability searches with no additional traces | `discovery_trace_quality.csv` and `discovery_traces.jsonl`; `stability_n=10` for each task. Schema flag is hard-coded `True`, not a validator. | Trace count observable; stability search work only partly logged |
| **B4 Runtime budget** | No per-task or total wall-clock cap found | No runtime cap enforced by the solver | No per-task runtime budget/usage in task outcome logs | **Unavailable / not configured, not zero** |
| **B5 Memory budget** | No explicit memory cap found | No memory cap enforced by the solver | No memory budget/usage in task outcome logs | **Unavailable / not configured, not zero** |
| **B6 Evaluation budget** | Split plan: 600 discovery / 200 transfer / 200 holdout; 5 arms per transfer/holdout task | 2,000 scored arm rows (1,000 per 200-task split); additional discovery stability, transfer-probe, and coverage-scan searches | `task_outcomes.csv` logs 2,000 scored rows and candidate trials; scans/probes have incomplete task-level logs. Official evaluation was not scored. | Task split visible; total search/evaluation pathway not represented by one budget record |

## Reconstructed work (clearly separated from original logs)

- **Discovery main pass:** 600 searches at cap 10; 600 primary trace records; 3 successful demo-fit traces. Saved trace outcomes contain 5,989 total candidate trials, max 10/task.
- **Stability diagnostics:** code runs 10 additional shuffled-demo searches per discovery task (6,000 searches, each cap 10). A Phase 2C training-demo-only deterministic replay reproduced all 600 primary choices, trial counts, and saved stability values exactly; it reconstructed 59,890 permutation candidate trials. Original Phase 13G logs recorded the permutation count but not per-permutation program/trial logs.
- **Scored transfer/holdout arms:** 2,000 task-arm rows; 5 arms × 200 tasks on each split; logged candidate trials sum to 2,998 transfer and 2,996 holdout. Each arm is capped at 3.
- **Transfer program probe:** code makes 10 one-program searches on each of 200 transfer tasks (2,000 candidate attempts). Five program/task demo-fit cases trigger an additional baseline call capped at 3 (15 more trials); this count was reconstructed from training demonstrations, not preserved as a historical per-task log.
- **Coverage scan:** code scans 200 transfer and 200 holdout tasks with all ten programs. Its per-task trial counts were not saved. The later Phase 2C test-output-blind replay reconstructs 1,988 + 1,987 = 3,975 candidate trials for these 400 tasks; this is a reconstruction, not an original log.

Across these enumerated paths, the source-derived/reconstructed total is **11,005 solver calls and 77,863 candidate trials**. The breakdown is in `historical_search_work_reconstruction.json`; transfer probe applicability is in `historical_transfer_probe_reconstruction.csv/.json`. This is not a contemporaneous Phase 13G run-log total; missing logs and conditional calls are marked above. It excludes non-search helper work and should not be mistaken for a budget-compliant Phase 13G run.

## Evaluation-integrity findings

`solve_task()` checks test outputs immediately after the first training-demo fit, then stops even if the test answer is wrong. `discover()` also calls it for each of ten stability permutations, although stability uses only selected program names. `measure_program_transfer()` performs program-specific and conditional baseline solves; `_coverage_scan()` also calls the test-scoring `solve_task()` path. Therefore historical “coverage scan” and search diagnostics are not production-isolated from test-output access, even when the reported coverage field is demo-fit.

The Phase 13G run manifest discloses the failed serialization and same-holdout reuse. No new Phase 2C scoring repairs that history. This report makes no claim that official evaluation data were never downloaded; official evaluation was not scored or used as feedback.

## Conclusion

The budget discrepancy is real and consequential for search coverage, but it is **not a full explanation** of ARC failure. Phase 2C sensitivity results show more candidate allowance recovers additional demo fits, while fullscan coverage remains low and the invariant pool remains empty. Runtime and memory budgets were not configured historically, so their historical values are unavailable, not zero.