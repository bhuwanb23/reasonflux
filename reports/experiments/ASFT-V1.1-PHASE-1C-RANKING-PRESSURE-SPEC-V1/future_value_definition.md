# Phase 1C.3 — Independent Future-Value Definition

## Primary target

The ranking target is **Future Net Transfer Utility at K**, abbreviated `FNTU@K`. It measures the value of a selected portfolio on the same untouched future task suite, relative to a paired no-candidate baseline. It is not derived from IDT, frequency, reuse, or compression ranking scores.

Let `S_m` be the K candidates selected by method `m`, `H` the fixed number of held-out future task opportunities, `U(S,t)` the predeclared task utility for portfolio `S` on future task `t`, `U(∅,t)` the utility with no selected candidates, and `C(S)` the frozen creation/storage/maintenance cost in the same calibrated utility units. Then:

`FNTU@K(m) = [Σ_{t∈H}(U(S_m,t) − U(∅,t)) − λ C(S_m)] / (K × H)`.

`U` is built from task correctness and a bounded task-quality score; actual compute/resource savings may enter only through the fixed calibration-derived conversion `λ`. The exact utility map, cost components, `λ`, and denominators are locked before any confirmation outcomes are exposed. A later phase must calibrate these on calibration-only material; no empirical calibration has been performed for Phase 1C.

## Portfolio and transfer controls

- Each method selects exactly K candidates from the same N-card panel, with the same storage/selection budget and the same future task suite.
- Future tasks are from disjoint task instances and held-out family/template blocks, not the candidate's own source task. Local reuse is a diagnostic; the primary target is cross-family future transfer.
- Evaluate the selected set as a set against the same no-candidate baseline. This captures interactions and avoids assuming candidate utilities are additive.
- Apply all K candidates to the same horizon H; no method receives extra retries, task opportunities, or score feedback.
- The per-panel statistic is one paired portfolio contrast per method. Candidates/tasks nested in a panel are not independent experimental units.

## Secondary candidate-level truth

For diagnostics, define candidate `i` standalone held-out value as the same paired future utility difference for `S={i}`, less its cost. It supports Precision@K, Recall@K, NDCG@K, and transfer-recall diagnostics, but does **not** replace the portfolio primary endpoint. “Useful” is `standalone future net value > 0` under the frozen rule; equality is not positive.

## Forbidden circularity

Future utility, future transfer count, future compression benefit, Oracle scores, held-out task labels, or any post-confirmation metric cannot enter candidate generation, feature calibration, ranker tuning, tie-breaking, or pressure validation. IDT's calibration score is a predictor; future utility is its independent outcome. Oracle is computed only after rank lists and pressure logs are sealed.

## Unavailable/missing outcomes

Distinguish `NOT_APPLICABLE` (a genuine zero task benefit under the fixed evaluation rule), `FAILED` (a policy attempt that earns the predefined failure utility), and `MISSING` (a data/system failure). Do not silently convert missing to zero. The primary is unavailable if outcome integrity fails or more than 5% of paired task rows are missing, or if missingness differs across policies by more than 2 percentage points; report exact counts and retain all rows. The threshold is a protocol rule, not an observed result.