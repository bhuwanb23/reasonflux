# ASFT v1.1 Phase 1E — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1E`  
**Package:** `ASFT-V1.1-PHASE-1E-CAPABILITY-VALIDATION-SPEC-V1`  

## Executive decision

- **PASS for specification layer.**
- **PASS for construct-separation/decision-rule contract layer.**
- **BLOCKED for empirical execution.**
- **RQ4 untested.**

No Phase 1E task battery, task generator, or confirmatory/replication outcomes were run. These statuses distinguish a specified and unit-checked benchmark from a scientific result.

## Historical capability audit

Phase 13E reported positive frozen internal scores: mean C_t `1.0227`, mean CGR `0.2946` (95% CI `[0.2857,0.3036]`), C_t monotonic in 10/10 seeds. It also retained one `cap-cross-domain` object across rounds; capability count stayed at one after formation and no accepted higher-order capability occurrences were found. The phase's C_t is a weighted internal portfolio score built from skill utility, transfer, coverage, and composition components. It can rise while the object count remains constant.

Corrected Phase 13D mean CGR was `−0.060` across nine evaluable seeds. Phase 14E records a very small same-cohort association from C_t to next-round task utility (`r=0.0498`, cluster-bootstrap 95% CI `[0.0163,0.0922]`) that passed its preregistered directional criterion. That result is preserved, but it is not an independent external capability battery, is not causal, and is not the same as TS→CGR. Phase 13E TS→CGR was `r=−0.5027` with an interval spanning zero. Phase 14H identifies Transfer→Capability Growth as the first major missing causal bridge; Phase 14J concludes robust capability growth and intelligence growth are not established.

**What the historical record did not establish:** independent behavioral breadth, durable generalization across unseen tasks/domains, capability emergence beyond one persistent object, causal transfer-driven growth, or intelligence growth.

## Construct separation and circularity

**Capability can be measured without CGR/C_t/IG:** yes, by the specified battery. The target is evaluator-scored task behavior (correctness/quality, transfer, breadth, retention, composition, adaptation). EBCS is computed from those six independent outcomes. The battery scorer, behavioral growth function, and capability-unit gate accept behavioral/evaluator fields only; the contracts reject internal metric fields from outcome payloads.

The capability metric is then treated as a **predictor**, with primary CGR_t compared against past performance, experience count, memory strength, frequency statistics, and related-success recency. The battery does not use CGR to select tasks, define success, set thresholds, or score outputs. This is currently API/schema evidence, not a production security audit; the real task/evaluator pipeline and sealed gold store are pending.

## Capability and outcome-response checks

The package's 31/31 contracts verify behavior-only scoring interfaces and the decision rule's ability to return `metric_wins`, `equivalent_tie`, `metric_loses`, `inconclusive`, or `unavailable`. The listed win/tie/loss intervals are **synthetic decision-rule fixtures only**—not predictive model fits or task outcomes. They show the analysis logic does not hardwire success; they do not show CGR actually wins, ties, or loses on a real battery.

The proposed primary target is Future External Behavioral Capability Score (EBCS) on tests A–F. The primary predictive comparison is out-of-sample MAE improvement from adding CGR_t to a simple model containing past performance, experience, memory strength, frequency, and related-success recency. SOI is +0.02 EBCS MAE reduction; exact sample size and cost coefficients remain calibration-stage fields.

## Readiness gates

| Gate | Status | Evidence / outstanding work |
|---|---|---|
| Gate 1 — Contracts | **PASS, interface scope** | 31/31 construct-separation and decision-rule assertions. |
| Gate 2 — Independent capability battery | **SPECIFIED; NOT IMPLEMENTED** | A–F behavior-only battery and success rules documented; no tasks/evaluator run. |
| Gate 3 — Task generator/base solver | **PENDING** | Build disjoint task families, gold outputs, and same-budget baseline/policy runners. |
| Gate 4 — Sample size | **PENDING** | Calibration-only cluster-level power/precision simulation; freeze N before confirmation. |
| Gate 5 — Frozen analysis | **PENDING** | Freeze B1–B5 simple-baseline features, CGR_t, M0/M1 models, MAE/SOI, intervals, multiplicity, missingness. |
| Gate 6 — Replication | **SPECIFIED; NOT GENERATED** | Disjoint family/template/domain replication required. |
| Gate 7 — Construct validation | **PENDING** | Demonstrate battery score can be computed with CGM module absent; independent review and system-level leakage audit. |
| Sealed outcome store | **PENDING** | Gold separation, access control, and lock proof not implemented. |

## Final decision

> **Capability benchmark specification exists. The contract layer passes. Empirical capability growth, capability-metric validity, and CGR's incremental predictive value have not been demonstrated.**

The benchmark is explicitly designed to allow CGR to win, tie, lose, or be unavailable, and to conclude that CGR adds no practically meaningful prediction beyond simpler variables for the prespecified target population. No Phase 1E confirmatory testing, Phase 3 IDT evaluation, or SCT experiment is authorized by this readiness report.