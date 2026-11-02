# Phase 2B.4 — Budgeted Coverage Benchmark

## Condition

Unchanged Phase 13G DSL and inference; frozen program order; first **3** candidates only, matching the declared production/search budget. Exact fit requires all training demonstrations to match. Paired fullscan results are reported separately. The coverage-only runner parsed training demonstrations, emitted a trace for each attempt, independently validated trace/schema and fit, and did not parse/use test-output fields or compute accuracy.

## Results

| Split | Tasks | C1 bounded fit / C3 successful trace | Coverage / successful trace rate | Trace emitted & independently valid | C4 invariant tasks | C5 skill | C6 transfer eligible | C7 capability eligible |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Discovery | 600 | 1 | 0.1667% | 600/600 (100%) | 0 | 0 | 0 | 0 |
| Transfer | 200 | 0 | 0% | 200/200 (100%) | 0 | 0 | 0 | 0 |
| Holdout | 200 | 1 | 0.50% | 200/200 (100%) | 0 | 0 | 0 | 0 |
| **All** | **1,000** | **2** | **0.20%** | **1,000/1,000 (100%)** | **0** | **0** | **0** | **0** |

The two budgeted fits are `reflect_vertical` on one discovery task and `reflect_horizontal` on one holdout task. Trial limit is three, and mean trials were 3.000 (discovery), 3.000 (transfer), 2.995 (holdout), 2.999 (all).

## Interpretation

- The finite production-budget condition found two exact demonstration fits. This is coverage, not test accuracy.
- Every task received a generated trace, including explicit budget-exhausted/no-fit records. Trace emission being 100% does not mean 100% successful reasoning; independently successful traces were 2/1,000.
- One successful discovery trace cannot meet the invariant miner's support threshold of five. Thus no invariant candidate was emitted. The skill builder and transfer/capability stages were not run because their upstream pool was empty; conditional downstream rates are not estimable.
- Holdout is retained only as descriptive coverage in this non-confirmatory diagnostic; Phase 13G's reuse means no pristine holdout or confirmatory inference is claimed.

The full task-level row set is in `task_stage_outcomes.csv`; all split-level metrics are in `coverage_summary_by_split.csv`. Accuracy is `NOT_MEASURED_BY_DESIGN`.