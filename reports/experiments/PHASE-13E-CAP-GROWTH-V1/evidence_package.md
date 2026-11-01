# Phase 13E Capability Growth Evidence Package

**Experiment:** `PHASE-13E-CAP-GROWTH-V1`  
**Confirmation status:** complete  
**Seeds:** 60, 61, 62, 63, 64, 65, 66, 67, 68, 69  
**Benchmark scope:** synthetic ReasonFlux grid tasks only; no ARC/external validation.  
**Frozen config SHA-256:** `ca6847d1684a1afd1f80ace426b8e6f7d35804d5378cdadca63780cdd241cc84`  
**Frozen source-tree SHA-256:** `71f2a2aa663e2026e9acd707ace581b54b3f666dbe491841280a09aed711ca67`

## Preregistered primary outcomes (ASFT)

| Metric | n seeds | Mean | SD | 95% CI low | 95% CI high |
|---|---|---|---|---|---|
| ct | 10 | 1.0227 | 0.0667 | 0.9750 | 1.0705 |
| cgr | 10 | 0.2946 | 0.0125 | 0.2857 | 0.3036 |
| capu | 10 | 1.0227 | 0.0667 | 0.9750 | 1.0705 |
| portfolio_coverage | 10 | 1.0000 | 0.0000 | 1.0000 | 1.0000 |
| ig | 10 | 0.2294 | 0.0069 | 0.2245 | 0.2343 |
| igr | 10 | 0.0090 | 0.0000 | 0.0090 | 0.0091 |
| ie | 10 | 0.0043 | 0.0002 | 0.0041 | 0.0044 |
| task_utility | 10 | 0.7902 | 0.0003 | 0.7900 | 0.7904 |
| ie_slope | 10 | -0.0039 | 0.0004 | -0.0042 | -0.0037 |

## Preregistered criterion decisions

| Criterion | Decision | Observed | 95% CI low | Reason |
|---|---|---|---|---|
| TS_to_CGR_directional_association | not_positive_or_unavailable | -0.5027 | -0.8601 |  |
| SU_to_CGR_directional_association | positive_descriptive | 0.9930 | 0.9695 |  |
| coverage_to_IG_directional_association | positive_descriptive | 0.4085 | -0.2977 |  |
| composition_to_IG_directional_association | not_positive_or_unavailable | unavailable | unavailable |  |
| capability_utility_to_transfer_directional_association | not_positive_or_unavailable | -0.5766 | -0.8850 |  |
| capability_utility_to_reuse_directional_association | positive_descriptive | 0.6702 | 0.0703 |  |
| replicated_capability_emergence | pass | 10/10 seeds with a capability persisting across consecutive rounds | unavailable |  |
| EXP-CAP-12_postcomposition_capability_count_growth | descriptive_not_a_pass_gate | 0/10 seeds had more capabilities in round 4 than round 2 with a successful held-out composition | unavailable |  |
| EXP-CAP-14_higher_order_emergent_capability | unavailable_no_valid_higher_order_cluster | 0 seed-capability occurrences with accepted emergent type | unavailable |  |
| positive_CGR | pass | 0.2946 | 0.2857 |  |
| positive_IG | pass | 0.2294 | 0.2245 |  |
| positive_IGR | pass | 0.0090 | 0.0090 |  |
| positive_coverage_growth | pass | 0.2500 | 0.2500 |  |
| positive_utility_growth | pass | 0.2946 | 0.2857 |  |
| positive_IE_trend | fail_or_null | -0.0039 | -0.0042 |  |
| ASFT_beats_B1_NO_LEARNING | fail_or_null | final_ct Δ=1.1785 (95% CI lower=1.1428); mean_task_utility_all_tasks Δ=-0.0361 (95% CI lower=-0.0363) | unavailable |  |
| ASFT_beats_B2_SKILL_STORAGE_ONLY | pass | final_ct Δ=1.1785 (95% CI lower=1.1428); mean_task_utility_all_tasks Δ=0.0773 (95% CI lower=0.0773) | unavailable |  |
| ASFT_beats_B3_RANDOM_SKILL_CREATION | pass | final_ct Δ=0.1603 (95% CI lower=0.1235); mean_task_utility_all_tasks Δ=0.0776 (95% CI lower=0.0770) | unavailable |  |
| ASFT_beats_B4_COMPRESSION_PROXY | pass | final_ct Δ=0.3455 (95% CI lower=0.3246); mean_task_utility_all_tasks Δ=0.0752 (95% CI lower=0.0750) | unavailable |  |
| ablation_reduces_growth_A1_NO_IDT | pass | 0.0595 | 0.0420 |  |
| ablation_reduces_growth_A2_NO_SCT | fail_or_null | 0.0000 | 0.0000 |  |
| ablation_reduces_growth_A3_NO_SKILL_LIBRARY | pass | 0.2946 | 0.2857 |  |
| ablation_reduces_growth_A4_NO_COMPOSITION | pass | 0.0350 | 0.0305 |  |
| composition_creates_value | fail_or_null_or_unavailable | -0.1429 | -0.1429 |  |
| A5_NO_CGM | unavailable_by_design | unavailable | unavailable | A5 preserves ASFT behavior and masks all growth measurements |
| growth_predicts_future_performance | pass | 0.0498 | 0.0163 |  |
| trajectory_monotonicity_descriptive | descriptive_not_a_pass_gate | 10/10 seeds | unavailable |  |
| EXP-CAP-20_natural_saturation | descriptive_not_a_pass_gate | 0/10 seeds saturated in both final rounds by the frozen CGM classifier | unavailable |  |
| EXP-CAP-19_fragmentation | descriptive_not_a_pass_gate | 0/10 ASFT seeds had a frozen representation-audit fragmentation failure | unavailable |  |
| EXP-CAP-21_regression_probe | reported_not_a_cohort_pass_gate | 2/10 evaluated probes detected decline | unavailable |  |
| EXP-CAP-22_dummy_skill_invariance | reported_not_a_cohort_pass_gate | 10/10 evaluated probes unchanged | unavailable |  |

## Correlations and prediction

| Association | n seeds | Pearson r | Fisher CI low | Fisher CI high | Status |
|---|---|---|---|---|---|
| TS_to_CGR | 10 | -0.5027 | -0.8601 | 0.1857 | available |
| SU_to_CGR | 10 | 0.9930 | 0.9695 | 0.9984 | available |
| coverage_to_IG | 10 | 0.4085 | -0.2977 | 0.8257 | available |
| composition_to_IG | 10 | unavailable | unavailable | unavailable | unavailable_constant_or_insufficient |
| capability_utility_to_transfer | 10 | -0.5766 | -0.8850 | 0.0833 | available |
| capability_utility_to_reuse | 10 | 0.6702 | 0.0703 | 0.9141 | available |

Future prediction (C_t at round t → task utility in round t+1): **r=0.0498**, 95% cluster-bootstrap CI [0.0163, 0.0922], status `available` (10 seed clusters maximum).

## Figures

- [figure_1_capability_trajectory](figures/figure_1_capability_trajectory.svg)
- [figure_2_cgr](figures/figure_2_cgr.svg)
- [figure_3_coverage](figures/figure_3_coverage.svg)
- [figure_4_capability_utility](figures/figure_4_capability_utility.svg)
- [figure_5_composition_growth](figures/figure_5_composition_growth.svg)
- [figure_6_ig_igr](figures/figure_6_ig_igr.svg)

## Tables and raw evidence

- `tables/table_1_capability_evolution.csv` — Table 1, capability evolution.
- `tables/table_2_coverage_statistics.csv` — Table 2, coverage statistics.
- `tables/table_3_utility_statistics.csv` — Table 3, capability/skill utility and intelligence metrics.
- `tables/table_4_baseline_comparison.csv` — Table 4, paired mandatory baseline contrasts.
- `tables/table_5_ablation_comparison.csv` — Table 5, paired ablation contrasts.
- `tables/table_6_correlations.csv` — Table 6, preregistered correlations and future prediction.
- `seed_round_arm.csv`, `task_level.csv`, `composition_task_level.csv`, `capability_formation.csv`, `skill_lifecycle.csv`, `robustness_probes.csv`, and `seed_summary.csv` retain seed/task/round-level data.
- `run_records.json` retains candidate rejections, all seed outputs, and task-level records; `frozen_run_manifest.json` preserves hashes recorded before seed 60 and `run_manifest.json` records completion status.

## Interpretation and caveats

Capability formation is counted only after the existing proposal and validity checks. Empty or unavailable portfolios are not assigned favorable synthetic values. The two IG pathways in the repository remain distinct; only `growth_metrics.compute_ig` with the preregistered GrowthConfig weights is confirmatory. Positive correlations are descriptive at n=10 and do not establish causality. A5_NO_CGM is intentionally behavior-matched and its growth metrics are masked, so it is not a performance comparator. B4_COMPRESSION_PROXY is not canonical DreamCoder. The adversarial dummy-skill test and seeded regression probe are reported separately from learned outcomes. Prior Phase 13C/13D evidence and its limitations remain unchanged. Posthoc audit: Corrected IE-slope aggregation and criterion-table rendering of observed paired contrasts; no runner, seed generation, task outcome, metric formula, or threshold changed. Saved-record SHA-256 `4099e98cc7b609b64e9da29566b2c46b0a5747b0b52afa2e4a936a2cfb5c2188`; posthoc analysis source SHA-256 `975e28ca62c2983e335c9a99f09c1f2fbd92afcc42f3a4dc8ea4534f26aa13ce`. Benchmark rerun: `False`.

## EXP-CAP-01–22 mapping

| Experiments | Evidence in this package |
|---|---|
| 01–02 formation and membership | `capability_formation.csv`, capability counts, states, member categories, category purity, target-family Jaccard |
| 03–05 trajectory, CGR, seed stability | Figures 1–2, Table 1, seed-level CI and monotonicity |
| 06–08 coverage | Figure 3, Table 2, family support and round deltas |
| 09–11 utility and reuse/transfer | Figure 4, Table 3, task rows linking capability-related utility to transfer/reuse |
| 12–14 composition and higher order | Figure 5, composition task data and composition lifecycle; unavailable components remain explicitly unavailable |
| 15–18 IG, IGR, efficiency, prediction | Figure 6, Table 3, Table 6, `analysis.json` |
| 19–22 fragmentation, saturation, regression, metric gaming | `fragmentation_ratio` and API audit in `seed_round_arm.csv`; `saturation_ratio` by round; copied-portfolio removal and 20-dummy-skill probes in `robustness_probes.csv` |

## Frozen files

The protocol and config were frozen before confirmation. This package does not alter Phase 13C/13D run records or historical evidence.