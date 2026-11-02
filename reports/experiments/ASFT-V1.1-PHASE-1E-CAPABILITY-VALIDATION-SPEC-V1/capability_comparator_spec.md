# Phase 1E.6 — Comparator Framework

## Required predictors

| ID | Predictor | Measurement at time t | Role |
|---|---|---|---|
| B1 | Past performance | Prior independent behavioral battery/task success on disjoint instances; no overlap with future target. | Strong lagged-behavior baseline. |
| B2 | Experience count | Number of training episodes/demonstrations/updates available by t, including eligible task exposure. | Exposure-only baseline. |
| B3 | Memory strength | Retrieval precision and coverage on a separate, held-out probe over time-t memory entries; store size/capacity is reported separately, not substituted after results. Probe answers never overlap future targets. | Tests accumulated experience/retrieval explanation. |
| B4 | Frequency statistics | Pre-time-t occurrence rate and reuse count for candidate patterns, computed only on training logs with frozen transforms. | Simple recurrence baseline. |
| B5 | Related-success recency | Time/episodes since the most recent success on a related training task family, with no future/test data. | Additional declared simple baseline. |
| B6 | Capability metric | Primary candidate: CGR_t. C_t, IG, IGR are secondary exploratory predictors, not substituted after results. | Tests incremental predictive validity. |

## Primary model comparison

- **M0 baseline model:** B1+B2+B3+B4+B5, with predeclared predictor transforms and panel/family structure.
- **M1 augmented model:** same M0 plus CGR_t.
- Primary comparison: held-out EBCS prediction MAE improvement `MAE(M0) − MAE(M1)` with a positive directional CGR coefficient.
- Report all B1–B5 single-variable models as diagnostics; compare the full M0, not only the weakest baseline, against M1.
- Model family, regularization/feature transforms, training procedure, and blocked validation are selected on development data and frozen before confirmation. No confirmatory re-fitting/tuning.

The target EBCS is computed from future task outputs without CGR/C_t/IG. The predictor table is joined only after outcome scoring is locked. A positive association between CGR and C_t is not a comparator result; it is internal metric coupling.

## Interpretive outcomes

- If M1 adds practical out-of-sample predictive value beyond M0 and the CGR slope is positive, CGR has incremental predictive evidence for this target population.
- If M1 is equivalent to M0 within the SOI, the benchmark may reject practically useful incremental predictive value for CGR under this protocol.
- If M1 is worse, or the CGR coefficient is reliably negative, the “higher CGR means more future behavior” interpretation is contradicted for this target/population.
- If B1–B5 outperform CGR alone but M1 adds nothing over M0, simpler explanations account for the predictive signal.

These are predictive—not causal—claims. Causality would require randomized manipulation of capability growth while holding the other inputs constant.