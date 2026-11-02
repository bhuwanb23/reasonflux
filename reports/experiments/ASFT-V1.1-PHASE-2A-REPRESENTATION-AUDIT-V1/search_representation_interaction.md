# Phase 2A.6 — Search–Representation Interaction Audit

## Core distinction

A task that does not produce a candidate can fail for at least two different reasons:

- **Representation gap:** no candidate in the explicitly defined language can express the demonstration mapping.
- **Search/parameterization gap:** a candidate exists in the language but enumeration, parameter inference, ordering, or budget prevents the search from reaching it.

A third outcome must remain separate: **demo-fit but test mismatch** means a training-consistent candidate failed to generalize on the evaluated test input. That is not the same as no representation or no search success. For a bounded implementation, “not representable” can only mean “not representable within the fully enumerated, declared language/parameter set,” not a proof of impossibility in ARC.

## Phase 13G search path

1. `PROGRAMS` is a fixed ten-item ordered tuple.
2. `solve_task()` tries each unique program in order up to `budget`.
3. Parameter context for translation/recoloring is inferred from training demonstrations; exact replay is required.
4. The routine stops at the **first** demo fit. It does not retain all demo-consistent alternatives.
5. It immediately evaluates that first fit on test outputs and returns `task_exact`; if it fails, later demo-fit candidates are not tried.
6. If no fit is found within the supplied budget, result is `unsupported_v1` / `no_dsl_fit_within_budget`.

Therefore the historical records conflate limited expressivity, parameter inference, candidate ordering, and top-k search. The saved summary does not include the complete candidate-fit set needed to classify every no-fit as a representation gap or search miss.

## Budget and configuration mismatch

| Stage | Declared/configured | Actual source behavior | Consequence |
|---|---|---|---|
| Frozen setting | `per_task_candidate_budget=3` | `config.json` says 3. | Intended cap. |
| Discovery | Not a separately declared full scan | `discover(discovery_tasks)` calls `discover` with default `budget=10`. | Discovery and trace counts are from 10 candidates, not the configured 3. |
| Main scored arms | 3 candidate programs | `run_arms()` calls `solve_task(..., budget=3)`. | Arm scoring follows the declared budget. |
| Full-inventory coverage scans | 10 candidates by design | `_coverage_scan()` calls `budget=len(PROGRAMS)`. | Diagnostic ceiling is not the same as budgeted arm coverage. |
| Trace stability | 10 demo-order permutations | Each permutation calls `solve_task` with the same discovery budget (10 in saved call path). | Stability is an additional diagnostic search workload, not primary three-candidate coverage. |

The key Phase 13G issue is not merely a typo in a report: the saved discovery learning pool was built using a larger candidate scan than the frozen budget. Phase 2A does not repair historical records. Any future reference run must reconcile a single budget value across config, discovery, candidate generation, scoring, diagnostic reporting, and logged trial counts.

## What the historical data can separate

- The full ten-program coverage scan demonstrates that only 3/600 discovery tasks had any recorded exact fit under that bounded inventory and its parameter code. This supports a narrow implementation coverage limitation, but no-fit is not proof that a richer representation could not fit them.
- The first-three ordered discovery yield is source-inferable from the saved first-fit program labels: only the reflection fit is in the first three; this is not a newly executed budget-conformant run.
- The five transfer and two holdout full-inventory fits are separate demo-coverage observations; scored arms use three and separately report accuracy. Because `solve_task` combines demo fit and test scoring and the same routine is used, the execution/dataflow separation is not production-isolated.
- The three successful discovery traces have three different program signatures. Given min support five, the invariant pool is empty under the frozen policy. That is a representation/task-recurrence-plus-support result, not a search-only or IDT-only verdict.
- No independent representation alternative or reference high-coverage condition exists in Phase 13G. Hence the primary-representation hypothesis cannot be causally contrasted against a second representation.

## Dataflow and metric integrity caveats

1. **Coverage vs accuracy:** `demo_fit` uses training pairs only, but `coverage_scan()` calls `solve_task()`, which also evaluates test outputs. The coverage field is logically distinct; the historical execution path is not a test-answer-blind coverage-only runner.
2. **Trace validity:** `trace_schema_valid=True` is assigned literally in the discovery loop; it is not the output of a per-trace schema validator. The separate dataset preflight supports grid schema validity but is not equivalent to runtime validation of every trace object.
3. **Trace count:** `growth_series()` reports prefix length in `n_successful_traces`; Phase 14G identified this defect. Use discovery trace artifacts and `mining_statistics` for the successful count (3), not the mislabeled prefix field.
4. **Zero denominator:** `measure_program_transfer()` returns `transfer_score=0.0` if `applicable==0`, while aggregate transfer precision is `null` when its denominator is zero. A future pipeline must make all per-program and aggregate zero-denominator fields unavailable/`null`, with denominator `0` retained separately.
5. **First-fit ambiguity:** an early program that fits all demonstrations but fails test causes a test failure; the search does not continue to a later fitting program. The number of ambiguous demonstration-consistent programs is not reported.

## Required future decomposition (specification, not execution)

For each task and each representation, log a coverage-only, test-label-blind record containing:

- exact candidate-language/version and declared parameter space;
- search budget and actual candidates tried;
- candidate IDs attempted, rejected, and demo-consistent;
- whether enumeration was exhaustive within the declared bounded language;
- time/compute consumed and early-stop reason;
- input/demo schema validity;
- task-level `coverage_state`: `covered`, `not_found_within_declared_language`, `search_budget_exhausted`, `parameter_search_incomplete`, `ambiguous_demo_fit`, `invalid_input`, or `unknown`.

Then run a separate outcome evaluator on sealed test outputs to classify the selected candidate as correct/incorrect/unavailable. The evaluator must not be callable from the coverage-only path. For a factorial comparison, hold task IDs and compute/storage budgets constant while varying representation and search strategy separately; preregister representation × search interactions. A high-coverage reference condition can validate the coverage and evaluator plumbing but cannot replace external ARC coverage evidence.

## Assessment

The Phase 13G evidence is consistent with severe representation limits **and** contains direct search/protocol confounds. The 10-program full scan helps quantify the bounded-language ceiling; the 3-vs-10 mismatch, first-fit logic, bounded translation inference, mixed access path, and missing candidate set prevent a clean attribution. Phase 2A therefore classifies representation as a plausible leading bottleneck—not a proven unique or primary cause.