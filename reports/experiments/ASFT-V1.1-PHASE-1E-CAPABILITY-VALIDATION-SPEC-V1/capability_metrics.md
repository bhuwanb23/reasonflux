# Phase 1E.7 — Capability Metrics and Decision Rules

## Primary external target

`EBCS_future` is the equal-weight macro-average across the six externally scored battery components A–F, with each component first averaged across its predeclared task families. It is computed solely from system outputs, evaluator gold/rubric, and task manifests. It is not a transform or relabeling of C_t, CGR, IG, IGR, IE, object count, or skill utility.

The primary predictor is `CGR_t`, measured at time t using only permitted pre-future data. The primary comparison is the out-of-sample mean absolute error improvement:

`ΔMAE = MAE(M0) − MAE(M0 + CGR_t)`

where M0 includes past behavioral performance, experience count, memory strength, frequency statistics, and related-success recency. Positive ΔMAE means adding CGR reduced prediction error. The primary analysis also reports the CGR coefficient sign and interval; a positive coefficient is required for a “higher capability growth predicts more behavior” interpretation.

## SOI and outcomes

**SOI:** `0.02` absolute EBCS MAE reduction (two percentage points). This design target must be reviewed/frozen with development/calibration data before confirmation; no post-outcome adjustment.

- **Metric wins / primary support:** adjusted 95% lower bound for ΔMAE exceeds +SOI and CGR's slope is positive with its adjusted lower bound above zero.
- **Equivalent tie:** the 95% interval for ΔMAE lies entirely inside `[-SOI,+SOI]`; no practically meaningful incremental predictive value is detected under this protocol.
- **Metric loses:** adjusted 95% upper bound for ΔMAE is below `−SOI`, or the CGR slope is reliably negative while the hypothesized positive direction is required.
- **Inconclusive:** valid estimate but interval overlaps the SOI/equivalence boundaries or predictor direction is uncertain.
- **Unavailable:** construct-separation, leakage, sample-integrity, missingness, or model-freeze gate fails.

**CGR uselessness statement:** an equivalent tie supports “CGR adds no practically meaningful predictive value beyond the prespecified simple baseline for this target population and range.” It does not prove CGR is useless in every setting.

## Behavioral growth endpoint

Report `ΔEBCS = EBCS_future − EBCS_disjoint_baseline` and change in the number of task families passing the behavioral capability gate. Capability growth is supported only if externally measured change exceeds its preregistered SOI under matched budgets, is retained at delay, and is not merely a rise in internal scores. CGR is not used to calculate ΔEBCS or determine which families pass.

## Secondary metrics

Task success, transfer, family breadth, delayed retention, composition, adaptation, cross-domain success, family count, net utility, memory precision, failure types, C_t/IG/IGR predictive comparisons, and model calibration. All are labeled secondary/exploratory unless separately preregistered. Report all component scores; do not let a favorable composite hide a failed battery component.

## Unit, uncertainty, and multiplicity

Independent unit is the agent-run/task-family-seed panel. Tasks and repeated rounds are nested. Use blocked out-of-sample prediction and cluster-level intervals/resampling by panel; no task-level pseudo-replication. Primary M0-vs-M1 comparison is one confirmatory test at family-wise α=.05. If separate C_t/IG models are confirmatory, multiplicity must be added before data access. Exact independent N is pending calibration-only power/precision analysis.

## Missingness and capability labels

`NOT_APPLICABLE`, `FAILED`, `ABSTAINED`, and `MISSING` are distinct. Fixed failure utilities apply to failed behavior; missing tasks remain missing. The endpoint is unavailable if >5% of paired future outcomes are missing or arm-specific missingness differs by >2 percentage points. Report counts and reasons.