# Phase 1E — Construct-Separation and Circularity Audit

## Required answer

**Can capability be measured without an ASFT metric? Yes, by design.** The independent target is the evaluator-scored task behavior in the A–F battery. Task correctness is computed from predicted outputs and hidden gold/rubric; EBCS macro-averages those external outcomes. Neither function accepts C_t, CGR, IG, IGR, IE, or capability-object metadata.

## Separation table

| Stage | Permitted inputs | Forbidden inputs |
|---|---|---|
| Task/battery generation | Frozen task-family generator, task seeds, permitted training exposure | CGR/C_t/IG, capability labels, desired arm ranking |
| Policy execution | Task inputs, allowed experience/memory/skills, fixed budgets | Future gold answers, future performance scores, evaluator labels |
| Task scoring | System output, evaluator gold/rubric, task ID | Any internal capability metric or predictor value |
| Capability-unit classification | Raw family performance, confidence, retention, utility, transfer outcomes | C_t/CGR/IG, object count/size, capability name |
| EBCS and ΔEBCS | Six external battery outcome components and disjoint baseline | CGM metric store or internal score history |
| RQ4 predictive analysis | Locked EBCS target + B1–B5 simple-baseline/CGR predictor table joined after lock | Outcome-driven predictor/threshold changes |

## Automated checks in current package

The contract code exposes `score_task_output(predicted, gold)`, `external_battery_score(outcomes)`, `behavioral_growth(pre_score, future_score)`, and `behavioral_capability_pass(...)`. Their signatures accept behavioral/evaluator fields only. The schema validator rejects `CGR`, `C_t`, `IG`, `IGR`, `IE`, and `capability_score` in the outcome payload. The contract test suite verifies these API boundaries and checks that capability success can be achieved or denied from behavior fields alone.

## Limit of the proof

These are interface/schema checks, not production security. Phase 1E has not implemented the task generator, actual policy APIs, independent gold store, or sealed production pipeline. A later system-level audit must prove that no hidden metric path or shared state bypasses these function boundaries. If the independent behavioral target cannot be computed with the CGM module removed/disabled, the benchmark fails and must not proceed.