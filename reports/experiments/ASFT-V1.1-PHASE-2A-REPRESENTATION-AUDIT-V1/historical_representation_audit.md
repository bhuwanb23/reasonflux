# Phase 2A.1 — Historical Representation Audit

**Phase:** `ASFT-V1.1-PHASE-2A`  
**Package:** `ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1`  
**Method:** read-only audit of Phase 13G's frozen config, source, saved tables, run records, and Phase 14G/14I/14J interpretation. No ARC tasks were rerun, no task JSON was opened for new scoring, and no official evaluation data was parsed or scored.

## Executive finding

Phase 13G used a **whole-grid, exact-match, ten-program symbolic inventory** over ARC input/output demonstrations. It did not use an object-centric scene graph, object-selection language, relation graph, general program AST, or compositional planner. Candidate programs were tried in a fixed order; training demonstrations had to fit exactly; exact task success required every test output in that task to match.

The directly observed representation limitation is severe: the full-inventory discovery scan found exact demonstration fits on **3/600** tasks, with one fitted transform each for reflection, rotation, and recoloring; transfer fit was **5/200** and holdout fit **2/200**. Of the 600 discovery tasks, 597 were logged `unsupported_v1` by that bounded search. The three successful signatures are singletons and remain below the frozen support threshold of five, so the invariant miner accepted no candidate. This is strong evidence that the **deployed bounded representation does not provide sufficient repeated coverage to activate the ASFT chain on these splits**.

It is **not proof** that the representation is the sole or primary root cause of ARC failure. The same record contains a material search/config mismatch: config says three candidate programs, `discover()` defaults to ten and is called without override; the separate coverage scan intentionally uses all ten; scored arms use three. Candidate ordering and first-fit stopping also affect which transformations are found. The system does not record all demo-consistent candidates or show what a materially richer representation would cover. Thus representation limits are a leading, plausible bottleneck; search policy, parameter inference, support thresholds, and task distribution remain entangled.

## 1. Exact historical representation

### Input and task unit

A task is represented by a list of training input/output grid pairs and test input/output pairs. A grid is a rectangular two-dimensional array of integer color IDs. `Grid` enforces nonempty rectangular rows but does not enforce ARC color range itself; the Phase 13G dataset preflight separately checked rectangularity and color-domain constraints. Each task is a task ID, not an individual grid pair.

The 13G solution language evaluates **one whole-grid candidate program at a time**. Program context is inferred from all training demonstrations and exact replay on those same demonstrations is required. The selected program is then tested on all test inputs. It is not a learned parser that constructs explicit objects and then reasons over their relations.

### Candidate program inventory (10 total)

1. `identity`
2. `reflect_horizontal` (mirror each row left-to-right)
3. `reflect_vertical` (reverse row order, top-to-bottom)
4. `rotate_90` (clockwise)
5. `rotate_180` (two internal 90° rotations; atomic search candidate)
6. `rotate_270` (three internal 90° rotations; atomic search candidate)
7. `transpose`
8. `anti_transpose`
9. `translate_constant` (one common `(dy, dx)` inferred from demonstrations; whole-grid non-wrapping shift; fill uses a source modal color; deterministic anchor search is capped at 16 positions)
10. `recolor_bijection` (one global one-to-one color mapping applied to every cell)

All candidates require exact training-demo equality. The search returns the **first** program in the supplied order that fits demonstrations. If that first fit later fails on test outputs, `solve_task` returns the test mismatch rather than continuing to a later demo-consistent program. Ambiguity among multiple fits is therefore not fully recorded as a candidate set or resolved by a separately validated rule.

### Important distinction: solver primitives vs helper functions

`src/solver/grid.py` also exposes `count_objects`, `group_by_color`, reflections, and `rotate_90`. In Phase 13G:

- `count_objects` is used only as an auxiliary feature for nearest-episode memory and structural buckets; it is **not** in the ten-program solution pool.
- `group_by_color` is available in the generic grid helper but is not called or enumerated as a Phase 13G ARC candidate program.
- The grid library's connected-component count is 4-connected and merges adjacent non-background colors into the same component; it is not color-aware object segmentation.

A helper existing somewhere in the repository is not evidence that Phase 13G's solver can search it as a transformation.

## 2. Search, trace, and budget behavior

- Frozen `config.json` declares `per_task_candidate_budget=3`.
- `run_arms()` applies budget 3 for transfer/holdout arm scoring.
- `discover()` has `budget=10` as its function default and `run_phase()` calls it without a budget argument; the saved discovery run therefore searches ten programs.
- `_coverage_scan()` intentionally evaluates all ten programs. These scans are diagnostic full-inventory counts, not the three-candidate arm coverage.
- Program order is fixed in `PROGRAMS`; under the declared first-three order, only the reflection fit among the three saved discovery fits is within the first three positions. This is a source-derived implication, not a new run.
- The successful-trace rate of 3/600 is from the full ten-program discovery scan; it must not be reported as the measured yield of a conformant three-program discovery run.

Trace records contain a compact declaration of `validate_grid_schema`, `enumerate_candidate_programs`, selected `apply_*`, and `verify_demonstrations`, or `candidate_budget_exhausted` for no-fit tasks. However, `runner.discover()` sets `trace_schema_valid=True` as a constant; the trace step name is not itself a measured validator call. The separate data preflight supports grid schema validity, but runtime trace validation should not rely on this hardcoded flag. `growth_series()` also writes `n_successful_traces=len(traces)` (prefix size 100–600), not the successful count; Phase 14G already identified this label defect. The true successful discovery trace count is three.

## 3. Saved coverage and downstream activation

| Split | Full 10-program exact demo-fit coverage | Meaning |
|---|---:|---|
| Discovery | `3/600 = 0.5%` | Three tasks had one reported fitting program each: reflection, rotation, recoloring. |
| Transfer | `5/200 = 2.5%` | Five full-inventory demo fits; not task accuracy. |
| Holdout | `2/200 = 1.0%` | Two full-inventory demo fits; not task accuracy. |

These are **bounded inventory exact-fit rates**, not ARC semantic-family prevalence and not evidence that all other tasks are unrepresentable. The saved taxonomy reports 597/600, 195/200, and 198/200 as `unsupported_v1` under the full-inventory scan, but `unsupported_v1` means no exact fit found by this program/parameter/search implementation—not a semantic diagnosis of task requirements.

Three discovery fits correspond to three different programs and have support `1` each. The frozen invariant support/min-frequency threshold is `5`, with minimum cross-trace support `5`; thus zero accepted invariants and zero skills follow from the observed pool and support policy. Zero capabilities then follow downstream. This is consistent with representation scarcity, but support threshold and lack of repeated task families are additional causes of non-activation.

The bounded arms have exact accuracy of `0/200` on transfer for ASFT/B1/B3/B4 and `1/200` for B2 memory; on holdout each of five arms scores `1/200`. Those are separate outcomes from demo-fit coverage. The same holdout was reused after attempt 01 generated predictions in memory; it is not pristine independent confirmation. This audit does not rescore these outcomes.

## 4. Coverage-measurement independence: metric vs execution path

The `demo_fit` boolean is computed from training demonstrations by `infer_context()` and exact replay; the boolean itself does not use the test target. That makes the **definition** of demonstration coverage separable from test accuracy.

Operationally, however, `coverage_scan()` calls `solve_task()`, which, after finding a demo fit, immediately evaluates test outputs and returns `task_exact` together with `demo_fit`. Thus the historical output pass combines coverage and test scoring in one execution path. The coverage field is logically independent, but the code path does not provide a strict “coverage-only, no test-label access” execution mode. A future coverage runner must stop after training-demo fit enumeration, emit coverage-only records, and keep test output access in a separate gated evaluator.

## 5. Evidence about representational limits

Evidence supporting concern:

- The actual candidate pool is explicitly limited to ten whole-grid transformations; it contains no object-selection, object grouping, counting-as-a-rule, relation, crop, pattern-completion, recursion, or general composition candidate.
- Demonstration fit is very low even under a ten-candidate scan: 3/600 discovery, 5/200 transfer, 2/200 holdout.
- Three discovered traces are singletons across three different transformations; no repeated signature reaches support five.
- The invariant→skill→capability chain therefore fails to activate on the saved split.
- The Phase 13G taxonomy explicitly marks counting, grouping, object detection, and pattern completion `not_operationalized_v1`; these labels are not estimated task prevalence.

Limits to the inference:

- The DSL is a bounded hand-selected library; a no-fit outcome is not an exhaustive proof that no program or abstraction exists.
- Translation inference is heuristic and capped, bijective recoloring is restrictive, and exact fit makes false negatives possible.
- First-fit ordering and budget mismatch limit the meaning of no-fit under the declared budget.
- No alternative representation or high-coverage reference condition was run.
- No representation-by-search factorial contrast isolates each cause.
- The three fit cases are too sparse and heterogeneous to test downstream invariant/skill theories; the zero-candidate result is not a meaningful negative test of those mechanisms.

## 6. Phase 13G failures: representation-related vs unresolved

| Failure/observation | Representation relation | Other plausible contributor / limit |
|---|---|---|
| 597/600 discovery tasks no full-inventory demo fit | Strongly consistent with bounded DSL coverage limitation. | Heuristic parameter inference, exact-fit requirement, task distribution, and hidden ambiguity remain inseparable. |
| 0 raw invariant patterns/candidates | Sparse/singleton successful traces leave no recurrence substrate. | Frozen support threshold 5 and miner configuration also block formation; no alternative lower threshold is tested here. |
| 0 skills | No eligible invariant candidates from which to form skills. | Promotion also requires ≥3 applicable transfer tasks and a qualification gate; downstream mechanism not independently tested. |
| 0 capability groups / IG unavailable | Downstream result expected when no validated skill pool exists. | Capability-unit definition requires ≥2 skills; unavailable is correct, not zero intelligence. |
| Very low exact accuracy across arms | Compatible with weak expressivity. | Does not isolate representation from search ordering, solver strategy, task difficulty, test-policy, or memory; B2's one solve is distinct. |
| Discovery 10 vs configured 3 | Not a representation property; a budget/protocol implementation defect. | Invalidates treating the saved discovery yield as a budget-matched reference estimate. |
| Attempt-01 serialization failure | Not a representation limitation. | Software/reporting failure; same holdout was reused in attempt 02. |
| No primary arm divergence on holdout | Mechanism pool never forms, so ASFT pathway cannot separate. | Endpoint is near floor and holdout reuse limits confirmatory interpretation. |

## 7. Historical assessment

**Representation as a limitation of the deployed 13G system:** strongly evidenced. The inventory is extremely narrow and the measured full-inventory demonstration-fit rate is low.

**Representation as the primary causal bottleneck among representation/search/data/support alternatives:** **not proven**. The budget/config mismatch, first-fit search, parameter inference, support thresholds, and absence of a reference alternative prevent causal separation.

**What 2A can conclude:** representation is a plausible and leading bottleneck hypothesis that is now operationally described and falsifiable. This is not a claim that representation alone caused ARC failure or that a richer representation will work.