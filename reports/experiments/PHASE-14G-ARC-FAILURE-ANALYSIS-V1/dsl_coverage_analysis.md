# DSL Coverage Analysis

## Exact demonstration-fit coverage from the full inventory

| Split | Tasks | Full 10-program exact demo fits | Fit rate | Not fitting |
|---|---:|---:|---:|---:|
| Discovery | 600 | 3 | 0.5% | 597 |
| Transfer | 200 | 5 | 2.5% | 195 |
| Holdout | 200 | 2 | 1.0% | 198 |

The supported operation families are narrow: discovery has one reflection, one rotation, and one recoloring; transfer has one rotation, two transpose/anti-transpose, one translation, and one recoloring; holdout has one reflection and one rotation. These are program-family results, not authoritative semantic ARC labels. Counting, grouping, object detection, and pattern completion were not operationalized in v1; their counts are “not estimated,” not zero.

## Coverage is not arm accuracy

The full coverage scan tests the entire fixed program inventory. Main scored arms have a three-candidate budget. Therefore the full-inventory fit rates are a ceiling on demo representability under this DSL, not a guarantee that each arm considers those programs. Actual task-exact outcomes are lower: ASFT transfer `0/200`; B2 episodic-memory transfer `1/200`; every holdout arm `1/200`.

There is also a discovery-stage budget mismatch: the frozen config declares three candidates per task, while saved `runner.py` calls `discover()` with its default budget of ten. The three reported successful discovery programs are reflection (third in fixed order), rotation (sixth), and recoloring (tenth); only the reflection case is within the declared first-three limit. This is a source-based audit of saved results, not a rerun. Consequently, `3/600` should be labeled full-inventory discovery fit yield, not fit yield under the declared per-task budget.

The user-provided “0.5% or lower on each split” needs correction: the corresponding full-inventory rates are **0.5%, 2.5%, and 1.0%**. They remain extremely low, but the transfer rate is not lower than discovery.

## Interpretation

This strongly supports low coverage of the tested DSL over these splits. It does not quantify total ARC semantic coverage, because no authoritative ARC family labels exist and excluded concepts were not operationalized. Nor does low DSL fit isolate representation from problem complexity: a richer candidate language, a different trace grammar, or changed thresholds would be a new experiment, not an explanation verified by this saved run.
