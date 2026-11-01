# Current ReasonFlux Repository and Phase 13B Review

**Review date:** 2026-10-31, Asia/Kolkata  
**Repository:** `bhuwanb23/reasonflux`, branch `main`  
**Base commit pulled:** `8f0213878998e2cea492d564469d4ee1936fc5c5` (`feat: add cross-family reuse rate metric and update related tests`)  
**Current workspace:** local Phase 13B changes are uncommitted; see the repository's `git status`.

## Executive status

The checkout contains a substantial synthetic ASFT prototype, experiment runners, baselines, evidence artifacts, and 519 tests after the additions made in this review. The prototype's core mechanisms work under their tests. Phase 13A's gate is a passing one-seed synthetic readiness smoke check, not formal multi-seed or ARC validation.

Phase 13B is still **not a successful validation** on its original `synthetic-v1` benchmark. I corrected a free-output-step issue in reuse cost accounting and added per-seed baseline-ranking diagnostics and paired differences. The original evidence runner and strict closure gate still return **`success: false`** because ASFT ties frequency-only and no-transfer on every seed. The gate was not weakened and the original task generation was not changed. A separate EXP-IDT-14 confounded-frequency stress test was added; it passes on its controlled no-op intervention but is exploratory and does not replace the original gate.

After the cost correction:

- ASFT, frequency-only, no-transfer: mean held-out TU **0.0958085** each across seeds 0–4.
- Random pattern: **0.0631134**.
- ASFT minus frequency-only and ASFT minus no-transfer: **0.0** paired difference on all seeds.
- The three informed methods produce the identical semantic order on all five seeds: reflection, rotation, counting, grouping.
- Corrected mean transfer score / utility are **TS=0.017619**, **TU=0.065726**.

The evidence/reporting work is now complete enough to characterize the current run, but the research criterion is not met. Do not describe Phase 13B as complete or claim transfer-aware ranking superiority.

## Architecture and data flow

```text
synthetic GridTask generator
  -> GridSolver emits operation-labelled ReasoningSteps
  -> TraceLogger / TraceStore
  -> normalize + segment + frequent-pattern mine
  -> invariant candidates / IS + validation / ranking
  -> skill creation / SCV / trigger / library / lifecycle
  -> ReuseEngine applies a macro to target tasks
  -> transfer records / capability + growth metrics
  -> experiment records, tables, figures
```

Main packages:

- `src/core/`: task, trace, invariant, skill, capability and state contracts.
- `src/solver/`: deterministic four-family synthetic task generator and rule-aware solver (reflection, rotation, counting, grouping).
- `src/traces/`: trace logging, normalization, segmentation, similarity and storage.
- `src/invariants/`: pattern mining, candidate generation, validation/ranking, robustness and transfer-aware logic.
- `src/skills/`: skill economics, creation/promotion, library, retrieval, lifecycle, composition and failure controls.
- `src/transfer/`: transfer records/memory, reuse engine and transfer metrics.
- `src/capability/`, `src/evaluation/`: capability/growth metrics, robustness, reporting/statistics and baselines.
- `experiments/`: EXP-01–05, Phase 13A/13B runners and gates, plus exploratory EXP-IDT-14.
- `configs/`: task/seed policy, thresholds, labels and metrics.
- `reports/`: committed experiment records and generated evidence/figures.
- `docs/03_implementation/validation/`: Phase 13A–13H plans. C–H are plans, not completed result packages in this checkout.

## Phase 13B evidence after correction

The runner evaluates `synthetic-v1` over seeds `[0,1,2,3,4]`.

| Measure | Mean | SD | 95% normal CI |
|---|---:|---:|---:|
| Discovery rate, each of four families | 1.000 | 0.000 | 1.000–1.000 |
| IP / IR | 1.000 / 1.000 | 0 / 0 | 1.000–1.000 |
| IS | 5.856 | 0.238 | 5.648–6.064 |
| Pearson / Spearman IS–TS | 1.000 / ~1.000 | ~0 / ~0 | ~1–1 |
| TS | 0.017619 | 0.000869 | 0.016857–0.018381 |
| TU | 0.065726 | 0.003188 | 0.062931–0.068520 |
| VST | 1.000 | 0.000 | 1.000–1.000 |
| Noise/top-rank stability | 0.720 | 0.110 | 0.624–0.816 |

Baseline results:

| Ranking | Mean held-out TU | SD | 95% normal CI |
|---|---:|---:|---:|
| ASFT transfer-aware | 0.095809 | 0.000736 | 0.095163–0.096454 |
| Frequency-only | 0.095809 | 0.000736 | 0.095163–0.096454 |
| No-transfer | 0.095809 | 0.000736 | 0.095163–0.096454 |
| Random pattern | 0.063113 | 0.007712 | 0.056354–0.069873 |

The ASFT-random gap is real in the current generator but does not satisfy the mandatory superiority criterion against frequency/no-transfer. The identical rankings indicate this benchmark does not currently provide transfer-discriminative choices among the four semantic candidates.

Per-seed diagnostics and paired effects are in `reports/experiments/idt_evidence/table_3_baselines_by_seed.json`; aggregate evidence is in `reports/experiments/idt_evidence/summary.json` and `summary.md`; gate output is in `reports/experiments/idt_evidence/closure.json`.

### Supplemental EXP-IDT-14

A separate confounded-frequency stress test (seeds 10–14) injects a zero-cost `normalize_grid` no-op into 3/4 discovery families, leaving the original benchmark untouched. It yields ASFT top-1 TU **0.164866** (SD 0.001100; 95% normal CI 0.163902–0.165831), frequency-only/IS-only **0**, random **0.059557**; the transfer-aware rank wins on every seed. At top-2 it also leads; from top-3 onward the ranking curves tie. This demonstrates mechanism sensitivity to this designed confound in the simulator only. Since the experiment was conceived after the original tie and explicitly injects the nuisance pattern, treat it as exploratory—not confirmatory IDT validation. Records/protocol are under `reports/experiments/EXP-IDT-14/`, `configs/idt_confounded_benchmark.yaml` and `docs/03_implementation/validation/phase_13b_exp14_protocol.md`.

## Measurement fix made

`GridSolver.solve(..., macro_ops=...)` previously allowed a reflection/rotation macro used on a counting/grouping task to skip the explicit `count_objects`/`group_by_color` reasoning step, even though `_output_for` still computed the output. That gave reuse free work and overstated reasoning reduction. The reused path now emits and charges the target-family output operation when the macro does not itself contain it. A regression test covers both symmetric counting and grouping tasks and checks the one-step reduction against the search baseline.

This fixes that accounting omission. Transfer utility dropped after correction; the baseline tie remained. The metric is still simulator-level step count, not wall-clock/compute saved by a general ARC agent.

## Scientific interpretation limits

1. **Known synthetic mechanism:** task family, reference transform and operation vocabulary come from the four-family generator/solver. This is a controlled mechanism experiment, not open-ended ARC invariant discovery.
2. **Component-level labels:** the expected reflection/rotation signatures are multi-operation concepts, while mined candidates may be individual operations. Current hit/quality checks accept a component overlap. Report these as component-level synthetic discovery, not as blinded validation of complete semantic invariants.
3. **Small correlation population:** the IS–TS correlation population averages 4.4 promoted candidates per seed. Perfect correlations on that small, constructed sample are fragile; they do not establish general predictive power.
4. **No baseline distinction:** the transfer-aware and non-transfer rankings are identical in the current pool. A strict gate failure must remain a failure.
5. **No ARC external validity:** `datasets/arc/` is only a `.gitkeep`; no ARC task adapter, Kaggle notebook/submission, or ARC results were found. Phase 13G remains future work.
6. **Intervals:** the repository reports normal-approximation CIs over five seed aggregates. Treat them as descriptive; they are not task-level uncertainty and are weak with this small number of seeds.

## Documentation alignment

- `docs/04_paper/claim_traceability.md` says only `exp04_growth` is enabled, while `configs/experiments.yaml` enables EXP-01 through EXP-07 and disables only ARC EXP-08.
- `docs/00_project/roadmap.md` still says Phase 12 is next, despite active Phase 13A/13B evidence.
- Some project notes still say 501 tests; the current full suite after this review is 519.
- The Phase 13A runner is smoke-mode and one-seed, so keep “readiness smoke pass” distinct from formal validation.

## Verification and reproduction

```bash
python -m pytest -q
# 519 passed in 2.58s after current changes

python -m compileall -q experiments tests src/evaluation/metrics_registry.py src/solver/executor.py
# passed

git diff --check
# passed
```

The `ruff` executable is not installed in this workspace, so I did not claim a ruff/linter pass. No linter configuration was otherwise identified in the project metadata.

**Verification incident:** an initial full-suite run invoked the configured five-seed `run_exp14(write=False)` through its aggregation test. That duplicate execution wrote no report artifacts and was not used as experiment evidence. I changed the aggregation test to use stubbed per-seed results, then reran the suite (519 passed) so it no longer reruns the five-seed benchmark. The published EXP-IDT-14 report remains post-processed from the saved final record; do not count the incidental replay as replication or confirmation.

To regenerate the Phase 13B package, `run_idt_evidence(write=True)` updates the reports; `check_phase13b_gates.py` should then return false until the baseline condition is met. The no-write checker call is:

```python
from experiments.check_phase13b_gates import main
main(write=False)
```

## Workspace integrity and changes

- Pulled to base commit `8f02138`; this review's code/docs/report changes are local and uncommitted.
- Changed code: `src/solver/executor.py`, `experiments/idt_experiments.py`, `experiments/check_phase13b_gates.py`, `src/evaluation/metrics_registry.py`.
- Added/updated tests: `tests/test_solver.py`, `tests/test_idt_experiments.py`.
- Added the Phase 13B results note at `docs/03_implementation/validation/phase_13b_results.md` and refreshed the Phase 13B evidence reports/figures.
- Added EXP-IDT-14 protocol, config, runner, tests, and reports as a separate exploratory stress test; seeds 5–9 pilots are disclosed and excluded, and the saved final seed set is 10–14.
- Updated the experiment registry and this review with the supplemental status; original Phase 13B artifacts/gate remain intact.
- The pre-existing untracked `validation/` scaffold has been preserved and its `CURRENT_REPO_REVIEW.md` updated; no files were removed from it.

## Recommended next experiment

Do not alter the original `synthetic-v1` generator or reinterpret EXP-IDT-14 to claim it passed Phase 13B. The next evidence capable of strengthening the broader IDT claim must be confirmatory: preregister an independently justified held-out benchmark and confound/task distribution before inspecting results, freeze the task split, metrics/top-k and minimum effect, retain per-task paired outcomes, and preserve every baseline. If transfer-aware ranking ties, keep the null result and narrow the claim. Phase 13B remains blocked as a successful validation until evidence meets the existing strict criterion.
