# Phase 13D preflight — transfer experiments

**Status (2026-10-31):** repository audit, protocol/config v1, experiment-local implementation, and stub contract tests are present. Contract tests pass (6 tests). No confirmation benchmark, training run, seed-level outcomes, or Phase 13D results have been executed. Contract fixtures previously generated/evaluated isolated toy tasks using labels 40 and 42; to protect untouched confirmation data, those labels are excluded and the frozen confirmation set is `[50,51,52,53,54,55,56,57,58,59]`. Hash freeze is still pending.

The existing `synthetic-v1`, EXP-03, Phase 13B, Phase 13C, and EXP-IDT-14 records are unchanged.

## Repository audit and risks

- The original Phase 13D artifact was a research outline in `phase_13d.md`; it did not define an executable multi-family transfer protocol.
- `experiments/exp03_transfer/run.py` and `reports/metrics/exp03_transfer.json` are legacy one-run EXP-03 evidence. Its reported `mean_ts` is copied from benefit and its `mean_ntr` is copied from reasoning reduction; it is not a valid multi-seed Phase 13D baseline and will not be pooled or overwritten.
- `src/evaluation/transfer_metrics.py::compute_ts` is only `after - before`; Phase 13D freezes its own bounded performance scale and retains separate exact accuracy and step-cost outcomes.
- `ReuseEngine` intentionally refuses cross-family skills when their claimed invariance is absent. A Phase-13D-only forced-application diagnostic measures counterfactual negative transfer; global retrieval/SCV behavior is unchanged.
- `TransferMemory` cannot supply the denominator for every failed/attempted application. Task-level rows are the primary attempt/failure record.
- The existing `GridSolver` can replay only one canonical operation through a normal `Skill`, and `compose=True` covers only a limited case. The new ordered-program interpreter is experiment-local; its costs are a synthetic reasoning-step model, not empirical compute.
- The four-family generator does not encode every phrase in the outline (e.g. triangle→square or arbitrary programs). Phase 13D uses explicitly declared grid/program recipes and makes no ARC claim. `count_groups = len(group_by_color(grid))` is a derived evaluation reducer, not a learned source skill.
- Phase 13C confirmed births only in reflection and rotation (22 each); counting/grouping had no births under its frozen gates. Phase 13D preserves this as a risk: if a required source skill is not learned, that endpoint remains unavailable or a no-match, as predeclared. No hand-inserted skills or weakened gates.
- There is no canonical DreamCoder implementation in the repository. B4 is a budget-matched recurring-operation compression **proxy**, not DreamCoder or a reproduction.

## Integrity and scope decisions

1. Use a new dataset label, `synthetic-transfer-v1`, and separate Phase 13D artifacts. Keep original `synthetic-v1` and all historical reports intact.
2. Exclude fixture labels 40 and 42; use the ten untouched confirmation seeds `[50,51,52,53,54,55,56,57,58,59]`. Train/test streams and cells use disjoint predeclared task offsets and audited IDs.
3. Retain all named experiments, four baselines, four ablations, per-task outcomes, missing skills, null metrics, failures, and unavailable cells. Empirical criteria are decision rules, not targets to tune toward.
4. Do not change global `compute_ts`, `ReuseEngine`, skill gates, SCV, utility definitions, or earlier artifacts. Local wrappers exist only for ordered programs/counterfactuals not expressible by safe production retrieval.
5. Report synthetic evidence only; no ARC external-validity claim.
6. New Python modules remain below 400 lines (largest Phase-13D module is currently 316 lines); all code is in `experiments/phase13d/`, configuration in `configs/`, tests in `tests/`, and docs under validation.

## Implementation and contract-test status

- Implemented local ordered task programs, exact grid/reducer outputs, per-operation cost accounting, matched arms, seed-cluster metrics, capability API hooks, aggregation, and a paper-package reporter.
- The contracts instantiate isolated deterministic task fixtures and stub skills; they do not call the training trace pipeline or ten-seed benchmark runner. They check exact interpreter outputs, negative-cost harm, disjoint task IDs, compression matching, metric/NTR formulas, null search counters, and no-learning baseline parity.
- `solver_search_candidates` remains null because the global solver has no canonical candidate-evaluation counter; Phase 13D reports actual local retrieval-candidate counts separately.

## Before confirmation execution

- Review and freeze `phase_13d_preregistration_v1.md` and `configs/phase13d_transfer_v1.yaml` together.
- Run the stub-only contracts, then use the CLI hash-freeze step to hash the protocol, config, Phase-13D code, tests, and runtime source tree.
- Run only after the hash manifest verifies; collect all ten seeds once and report every criterion passed, failed, or unavailable.
- Do not rerun Phase 13C stages, alter outcomes, or use exposed fixture seeds 40/42 as confirmation data.

**Important:** no scientifically honest implementation can guarantee all empirical criteria. Passing software contracts is distinct from empirical transfer, scientific validity, and ARC external validity.