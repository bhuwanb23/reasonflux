# Phase 1F — Construct-Separation and Circularity Audit

## Required answer: can intelligence be measured without IG?

**YES, by design.** The external target is evaluator-scored future task behavior: learning curves, adaptation recovery, held-out environment success, few-shot acquisition, cross-domain learning, and delayed generalization/retention. Those outcomes are computed from task inputs, system outputs, hidden evaluator gold/rubrics, exposure logs, and resource logs. They can be scored with IG disabled and without importing the IG computation.

If any battery target cannot be computed without IG/IGR/IE/CGR/C_t or uses them to define task success, the benchmark fails construct separation and the outcome is unavailable.

## Separation table

| Stage | Allowed inputs | Forbidden inputs |
|---|---|---|
| Test task generation | Frozen generator, task seeds, preregistered distributions and shifts | IG/IGR/IE, desired IG ranking, capability labels, future gold |
| System execution | Task inputs, allowed demonstrations, fixed budgets and existing state | Future answers, IG-selected task/evidence budget, evaluator labels |
| Task scoring | Output, task input, independent evaluator gold/rubric | IG/IGR/IE/CGR/C_t/TS/capability score |
| AULC/adaptation/transfer/retention targets | Externally scored task outcomes and exposure/resource logs | Any internal intelligence or capability metric |
| Intelligence-claim status | Locked A–F estimates, uncertainty, integrity and replication results | Internal score movement as success label |
| RQ5 prediction analysis | Locked external targets joined after lock with B1–B6/R7 predictors | Outcome-driven predictor/task/threshold change |

## Automated contract evidence

`intelligence_benchmark.py` exposes behavior-only `score_task_output`, `learning_curve_auc`, and `behavioral_delta` APIs. Its outcome validator denies IG, IGR, IE, CGR, C_t, capability/intelligence scores, and internal transfer fields. The 40-contract suite verifies signature/schema boundaries, the AULC calculation, IG win/tie/loss/inconclusive/unavailable paths, and retirement decision paths.

## Limit of current proof

The current module is an interface/contract prototype, not the production task/evaluator pipeline. It does not establish access control, a sealed gold store, absence of shared-state leakage, or behavior of a real solver. Before execution, system-level tests must run the scoring pipeline with the IG implementation absent, verify outcomes are unchanged, and independently audit task selection, budgets, and data access. Until then, construct separation is **specified and unit-checked**, not production-secured.