# Phase 13F — Baseline & Ablation Evidence

**Experiment:** `PHASE-13F-BASELINE-ABLATION-V1`  
**Status:** complete  
**Seeds:** 70, 71, 72, 73, 74, 75, 76, 77, 78, 79 (independent units, n=10)  
**Scope:** synthetic ReasonFlux grid tasks; no ARC/external validation.  
**Frozen config SHA-256:** `33e719b080d4fe4db99ce0ca142a7837ccf77ac04dc528693e21a2afb872906a`  
**Frozen source-tree SHA-256:** `b0fca9ac9ff0b1453fab83d61180a182b88b568a880592c0504fe20da3e3ce76`

## Outcome summary

The complete criterion table follows. For quick interpretation, the paired baseline differences (ASFT minus comparator) are:
- **B1_NO_LEARNING:** task utility Δ=-0.0363 (95% CI -0.0366 to -0.0361); CGR Δ=0.2872 (95% CI 0.2872 to 0.2872).
- **B2_MEMORY_SKILL_STORE:** task utility Δ=0.0749 (95% CI 0.0747 to 0.0751); CGR Δ=0.2872 (95% CI 0.2872 to 0.2872).
- **B3_RANDOM_SKILL_CREATION:** task utility Δ=0.0000 (95% CI 0.0000 to 0.0000); CGR Δ=0.0000 (95% CI 0.0000 to 0.0000).
- **B4_COMPRESSION_PROXY:** task utility Δ=0.0749 (95% CI 0.0747 to 0.0751); CGR Δ=0.0814 (95% CI 0.0814 to 0.0814).

Key component contrasts (positive Δ favors ASFT; metrics are not interchangeable):
- **A1_NO_IDT:** Δ utility=-0.0024 [CI -0.0027, -0.0022]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.0150 [CI 0.0129, 0.0171].
- **A2_NO_SCV:** Δ utility=0.0000 [CI 0.0000, 0.0000]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.0000 [CI 0.0000, 0.0000].
- **A2_1_RANDOM_SCV:** Δ utility=0.0000 [CI 0.0000, 0.0000]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.0000 [CI 0.0000, 0.0000].
- **A2_2_NO_LIFECYCLE:** Δ utility=0.0000 [CI 0.0000, 0.0000]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.0000 [CI 0.0000, 0.0000].
- **A2_3_NO_COMPOSITION:** Δ utility=0.0773 [CI 0.0773, 0.0773]; Δ composed-task utility=0.6188 [CI 0.6188, 0.6188]; Δ CGR=0.0364 [CI 0.0364, 0.0364].
- **A3_NO_CAPABILITY_LAYER:** Δ utility=0.0000 [CI 0.0000, 0.0000]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.2872 [CI 0.2872, 0.2872].
- **X1_NO_TRANSFER:** Δ utility=-0.0363 [CI -0.0366, -0.0361]; Δ composed-task utility=-0.3412 [CI -0.3412, -0.3412]; Δ CGR=0.2872 [CI 0.2872, 0.2872].
- **X4_NO_CAPABILITY_FORMATION:** Δ utility=0.0000 [CI 0.0000, 0.0000]; Δ composed-task utility=0.0000 [CI 0.0000, 0.0000]; Δ CGR=0.2872 [CI 0.2872, 0.2872].

Candidate selection / budget evidence (key for interpreting no-SCV and randomized controls):
- ASFT: mean constructed skills 4.0000; mean common eligible pool 4.0000.
- A1_1_FREQUENCY_ONLY: mean constructed skills 4.0000; mean common eligible pool 4.0000.
- A2_NO_SCV: mean constructed skills 4.0000; mean common eligible pool 4.0000.
- A2_1_RANDOM_SCV: mean constructed skills 4.0000; mean common eligible pool 4.0000.
- B3_RANDOM_SKILL_CREATION: mean constructed skills 3.0000; mean common eligible pool 4.0000.
- SENS_SCV_Q25: mean constructed skills 4.0000; mean common eligible pool 4.0000.
- SENS_SCV_Q75: mean constructed skills 0.0000; mean common eligible pool 4.0000.

Fixed sensitivity-point task-utility estimates:
- SENS_SCV_Q25: task utility 0.7899 (95% CI 0.7897 to 0.7901).
- ASFT: task utility 0.7899 (95% CI 0.7897 to 0.7901).
- SENS_SCV_Q75: task utility 0.8262 (95% CI 0.8262 to 0.8262).
- SENS_IS_7_5: task utility 0.7819 (95% CI 0.7638 to 0.8001).
- SENS_IS_10: task utility 0.7101 (95% CI 0.7098 to 0.7103).
- SENS_COMP_LOOSE: task utility 0.8054 (95% CI 0.8051 to 0.8056).
- SENS_COMP_STRICT: task utility 0.7744 (95% CI 0.7742 to 0.7747).

## Primary comparisons

Paired 95% t intervals use seed-level differences. ASFT beats a baseline only when both the task-utility and CGR paired lower bounds are positive, as preregistered. These are decisions, not narrative overrides.

| Comparison | Decision |
|---|---|
| ASFT_beats_B1_NO_LEARNING | fail_or_null |
| ASFT_beats_B2_MEMORY_SKILL_STORE | pass |
| ASFT_beats_B3_RANDOM_SKILL_CREATION | fail_or_null |
| ASFT_beats_B4_COMPRESSION_PROXY | pass |

## Component ablations

| Intervention | Outcome |
|---|---|
| component_effect_A1_NO_IDT | positive_on_at_least_one_preregistered_outcome |
| component_effect_A1_1_FREQUENCY_ONLY | mixed_or_unavailable |
| component_effect_A2_NO_SCV | mixed_or_unavailable |
| component_effect_A2_1_RANDOM_SCV | mixed_or_unavailable |
| component_effect_A2_2_NO_LIFECYCLE | mixed_or_unavailable |
| component_effect_A2_3_NO_COMPOSITION | positive_on_at_least_one_preregistered_outcome |
| component_effect_A3_NO_CAPABILITY_LAYER | positive_on_at_least_one_preregistered_outcome |
| component_effect_A3_1_NO_GROWTH_TRACKING | mixed_or_unavailable |
| component_effect_A3_2_INDEPENDENT_CAPABILITIES | mixed_or_unavailable |
| component_effect_X1_NO_TRANSFER | positive_on_at_least_one_preregistered_outcome |
| component_effect_X2_NO_SKILL_LIBRARY | positive_on_at_least_one_preregistered_outcome |
| component_effect_X3_NO_EXPERIENCE_MEMORY | mixed_or_unavailable |
| component_effect_X4_NO_CAPABILITY_FORMATION | positive_on_at_least_one_preregistered_outcome |

## Required evidence tables

- `tables/table_1_baselines.csv`: B1–B4 vs ASFT, means, SDs, CIs by metric.
- `tables/table_2_ablations.csv`: contribution and cross-component ablations.
- `tables/table_3_effect_sizes.csv`: paired differences, 95% CIs, Cohen dz, and Hedges g.
- `tables/table_4_sensitivity.csv`: fixed SCV, invariant-strength, and composition requirements.
- `master_result_matrix.csv`: IS, SU, TS, CGR, IG, and task utility across every arm.
- `candidate_selection.csv`: common eligible pool versus constructed/persistent skill counts by seed and arm.

## Figures

- [figure_1_asft_vs_baselines](figures/figure_1_asft_vs_baselines.svg)
- [figure_2_ablation_comparison](figures/figure_2_ablation_comparison.svg)
- [figure_3_contribution_effects](figures/figure_3_contribution_effects.svg)
- [figure_4_sensitivity](figures/figure_4_sensitivity.svg)

## Interpretation limits

IS is invariant strength (not a global intelligence score); it is not applicable to raw episodic memory and no-learning arms. SU/TS use repository skill utility and successful observed transfer. CGR/IG use the Phase 13E-frozen pathway and weights. B4 is a compression-only proxy, not canonical DreamCoder. A3 and X4's CGR/IG changes are structural consequences of removing capability formation/measurement, not task-performance gains; A3.1/A3.2 are not performance comparators. X3 tests retention after one-shot discovery; the current runner has no online invariant-mining loop, so a null difference is not evidence that memory is universally unnecessary. Paired standardized effect sizes can be very large when seed-difference SDs are near zero; prioritize raw paired differences and CIs. CIs are per-contrast and are not multiplicity-adjusted; secondary comparisons are exploratory. Attempt 01 was interrupted and is excluded; its manifests/note are preserved in `../PHASE-13F-BASELINE-ABLATION-V1-ATTEMPT-01-INTERRUPTED/`. Previous Phase 13C/13D/13E artifacts were not edited or pooled into the seed-level estimates.

## Raw records and audit

`run_records.json` preserves all candidate rejections and per-seed outcomes; `seed_round_arm.csv`, `task_level.csv`, `composition_task_level.csv`, `capability_formation.csv`, and `skill_lifecycle.csv` preserve analysis units. The pre-run manifest contains frozen config, preregistration, and source hashes.

## EXP-ABL mapping

Q1–Q2: Table 1 and Figure 1. Q3–Q4: A2/A1 arms and Tables 2–3. Q5–Q6: X1/A2.3 and composition rows. Q7: paired effect-size table, descriptive ranking only. Q8: A3/A3.2/X4, master matrix, and growth-measurement status.

Phase 13F results do not establish external ARC validity, and no criterion is promoted to a pass because it was expected to succeed.

## Posthoc analysis audit

Expanded the result interpretation and raw-difference contribution figure; corrected only report presentation. No metric formula, threshold, decision gate, runner, or task outcome changed. Saved-record SHA-256 `d07682b197bad3d3d5164ba1c90bfef3a17697500025667c3bd0631bc1db7d70`; posthoc analysis source SHA-256 `29d73705f953d65ab19f74bb7706237eb373fe6f6e6423f8037906c357785fdb`. Benchmark rerun: `False`.