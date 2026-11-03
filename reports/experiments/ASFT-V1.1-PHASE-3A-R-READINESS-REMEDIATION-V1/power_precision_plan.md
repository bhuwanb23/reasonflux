# Phase 3A-R — Calibration-Only Power and Precision Plan

**Gate 6 status: BLOCKED.** The independent unit can be specified from Phase 1C, but no matched calibration outcomes or valid variance estimate exists from which to simulate power/precision or freeze a final N.

## S1–S6 status

| Requirement | Current disposition | Reason |
|---|---|---|
| S1 Independent unit | **Specified, provisional** | Phase 1C defines one independently seeded candidate-discovery panel paired to a future-task family/seed block; candidate/task rows are nested, not independent. Retain panel/family-seed as the unit unless an approved amendment says otherwise. |
| S2 Variance estimate | **Missing** | No FNTU outcomes exist for the target candidate population. Phase 13B TU and Phase 13D synthetic `TS` use different constructs/endpoints and cannot estimate target variance. |
| S3 Precision target | **Partial** | Phase 1C SOI is +0.10 normalized net utility/slot/opportunity. It is not by itself a confidence-interval half-width/precision target; the latter is not frozen. |
| S4 Power/precision simulation | **Not run** | Requires calibration-only panel-level FNTU contrasts, endpoint/cost freeze, four-comparator multiplicity and a declared precision target. |
| S5 Final N | **Not frozen** | N=40 is the synthetic candidate-panel fixture size, not a justified number of independent panels. H and actual panel/family blocks are also unset. |
| S6 C1–C4 split assignment | **Not made** | No candidate/task registry or disjoint blocks; existing task IDs are previously audited and cannot serve as pristine C3/C4. |

## Prohibited shortcuts

Do not use the following as substitutes for calibration variance or power:

- Phase 1C's designed synthetic pressure panels or outcome-response sanity vectors;
- Phase 13B TU or EXP-IDT-14's constructed stress-test outcomes;
- Phase 13D synthetic-transfer `TS` rows, which answer another question on another endpoint;
- candidate/task rows treated as independent instead of panel/family-seed clusters;
- a favorable or convenient N copied from a different phase.

## Power workflow when Gates 1–5 are addressed

1. Before confirmatory access, define the independent panel/family-seed cluster and complete a disjoint C1 calibration / C2 development / C3 confirmatory / C4 replication assignment with file and membership hashes.
2. On C1 only, estimate the joint panel-level FNTU contrast variance, cross-policy covariance, cluster heterogeneity and missingness under the frozen independent evaluator. Preserve all panel rows and failures.
3. Run versioned simulations for the four paired R1−R2/R3/R4/R5 contrasts, Holm family-wise alpha 0.05, Phase 1C SOI +0.10, and a separately declared precision target. Use cluster-level resampling/simulation; no task/candidate pseudo-replication.
4. Select and freeze the smallest N meeting the declared joint power and/or precision criterion; show sensitivity to plausible variance/missingness assumptions. Hash code/config/seeds/results and obtain independent review before any C3 unlock.
5. Keep C2 for code/debug only. Do not use C3/C4 labels for feature tuning, variance estimation, or pool replacement. Replication uses disjoint task-family/template and seed blocks.

This is a workflow specification, not a completed calculation. Until matched C1 data exist, the final N is negotiable by necessity and Phase 3B must remain unauthorized.