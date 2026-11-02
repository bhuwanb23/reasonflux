# Phase 1F.8 — Endpoints, Metrics, and Decisions

## Primary endpoint

**Test A Future Learning Rate AULC**: normalized trapezoidal area under externally scored accuracy at fixed exposures `[0,1,3,5]`, averaged within family first and then equally across preregistered future task families. Range `[0,1]`; higher is better. This is the sole primary endpoint for the confirmatory RQ5 prediction test.

## Primary predictive estimand

Primary predictor is frozen `IG_t`; `IGR_t` is a separately preregistered key-secondary predictor evaluated against the same endpoint with Holm familywise adjustment; IE is exploratory. IGR cannot replace or rescue the primary IG test. Compare M0 (past performance, experience count, capability score, memory strength, transfer metrics) with M1 (M0 + IG_t):

`ΔMAE = MAE(M0) − MAE(M1)`.

Positive ΔMAE means IG reduces held-out prediction error. A positive IG slope is required to support “higher IG predicts better future learning.”

**SOI:** `0.02` absolute normalized-AULC MAE reduction for Test A. For secondary outcomes, use the same `0.02` normalized-scale incremental held-out MAE reduction when an outcome is normalized to `[0,1]`; for non-normalized measures (e.g., examples-to-criterion), specify a scale-specific SOI during development and freeze it before confirmation. None may be changed after confirmatory outcomes.

## Outcome-response states

- **Cohort-level IG win:** adjusted 95% lower bound for ΔMAE > +SOI and positive IG slope with adjusted lower bound >0. This is a within-cohort decision only.
- **RQ5 claim survives:** cohort-level primary win in both confirmatory and disjoint replication data, plus a replicated win on at least one additional transfer/generalization/adaptation endpoint, as specified in `intelligence_retirement_rules.md`.
- **Equivalent tie:** the primary ΔMAE interval lies wholly inside `[-SOI,+SOI]`; adequately powered equivalent results in confirmation and replication can trigger retirement rules.
- **IG loses:** adjusted upper bound for ΔMAE < −SOI or IG slope is reliably negative under the preregistered positive-direction hypothesis.
- **Inconclusive:** valid estimate but interval crosses decision boundaries, direction is uncertain, or the result is not independently replicated.
- **Unavailable:** leakage, target dependence on IG, implementation/integrity failure, invalid split, or missingness threshold breach.

## Secondary endpoints

B adaptation recovery AULC/examples-to-criterion; C novel-environment success; D few-shot acquisition/compositional learning; E cross-domain target learning; F generalization retention/relearning savings. Also report learning slopes, sample efficiency, persistence, random-baseline gaps, calibration, IG stability/variance/drift, C_t/IGR/IE results, and resource cost. These cannot replace a failed primary endpoint post hoc. Freeze multiplicity control before confirmation.

## Unit and uncertainty

Independent unit: agent-run × task-family-seed panel (with domain and time block recorded); repeated task items/exposure points are nested. Use family/domain-blocked out-of-sample prediction and cluster-aware intervals/resampling at the independent panel level. Do not treat repeated trials as independent N. Exact N requires development-only precision/power calibration.

## Missingness and status

Keep `FAILED`, `ABSTAINED`, `NOT_APPLICABLE`, and `MISSING` distinct. Missing scores are not zero. Primary endpoint is unavailable if >5% paired AULC records are missing or between-arm missingness differs by >2 percentage points; report reasons and sensitivity bounds. No confirmatory exclusions based on IG or outcome values.