# Phase 2B.5 — Full-Scan Coverage Benchmark

## Diagnostic condition

Unchanged Phase 13G representation and inference; all ten ordered candidate programs searched, stopping at the first exact fit. This mode diagnoses the finite implementation's observed ceiling. It is not a production-budget condition, task-performance result, or theoretical ceiling on ARC representability.

## Results

| Split | Tasks | C1 bounded fit / C3 successful trace | Fullscan demo-fit rate | Valid traces | C4 invariant tasks |
|---|---:|---:|---:|---:|---:|
| Discovery | 600 | 3 | 0.50% | 600/600 | 0 |
| Transfer | 200 | 5 | 2.50% | 200/200 | 0 |
| Holdout | 200 | 2 | 1.00% | 200/200 | 0 |
| **All** | **1,000** | **10** | **1.00%** | **1,000/1,000** | **0** |

The fullscan counts exactly reproduce the saved Phase 13G demonstration-fit totals (3/600, 5/200, 2/200). Program outcomes among the ten fits: two recoloring, two 180-degree rotation, two transpose, and one each vertical reflection, 270-degree rotation, translation, and horizontal reflection. There are eight distinct program-plus-inferred-context signatures among the ten tasks.

The TraceMiner received only the three successful discovery traces. Each belonged to a different program signature with support **1**, below the frozen minimum support of **5**; it emitted zero invariant candidates.

## Budget contrast

The three-candidate condition found 2/1,000 fits while fullscan found 10/1,000 under the same representation, demonstrations, inference code, and program order. Eight of the ten fullscan-fit task IDs were not found inside the first-three budget. This is a descriptive, paired search-budget effect for this finite implementation; it does not establish that search is the only bottleneck or that broader search would solve more ARC tasks. The first-three condition found 2/10 fullscan-fit tasks.

## Limits

A no-fit result means no exact fit was found under these ten programs, fixed parameter inference, order, and search limits. No semantic ARC-family labels were available, and the scan did not enumerate alternate fits after a first fit. No test outputs were parsed or scored. Accuracy and ASFT efficacy remain unmeasured.