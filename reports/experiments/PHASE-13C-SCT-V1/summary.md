# Phase 13C — SCT Validation (synthetic-sct-v1)

Confirmatory block: seeds 20–29. Calibration block: seeds 15–19.
Results are conditional on the current synthetic invariant/task generator; they do not validate ARC or repair Phase 13B.

- Strict SCT superiority gate: **False**
- Unique eligible candidate rows: 44

## Primary net value by creation policy

| Policy | Mean | SD | Normal 95% CI | Seed-bootstrap 95% CI |
|---|---:|---:|---:|---:|
| SCT | 0.345000 | 0.063246 | 0.305801–0.384199 | 0.305000–0.385000 |
| NEVER_CREATE | 0.000000 | 0.000000 | 0.000000–0.000000 | 0.000000–0.000000 |
| ALWAYS_CREATE | 0.345000 | 0.063246 | 0.305801–0.384199 | 0.305000–0.385000 |
| RANDOM_CREATE | 0.345000 | 0.063246 | 0.305801–0.384199 | 0.305000–0.385000 |
| MEMORY_ONLY | 1.325000 | 0.000000 | 1.325000–1.325000 | 1.325000–1.325000 |

## Paired SCT-minus-control contrasts

| Control | Mean | SD | Normal 95% CI | Seed-bootstrap 95% CI |
|---|---:|---:|---:|---:|
| NEVER_CREATE | 0.345000 | 0.063246 | 0.305801–0.384199 | 0.305000–0.385000 |
| ALWAYS_CREATE | 0.000000 | 0.000000 | 0.000000–0.000000 | 0.000000–0.000000 |
| RANDOM_CREATE | 0.000000 | 0.000000 | 0.000000–0.000000 | 0.000000–0.000000 |
| MEMORY_ONLY | -0.980000 | 0.063246 | -1.019199–-0.940801 | -1.020000–-0.940000 |

## SCV10 predictiveness (seed-cluster bootstrap)

| Predictor | Spearman ρ | 95% cluster-bootstrap CI | n candidates |
|---|---:|---:|---:|
| SCV10 | 0.700427 | 0.544724–0.930595 | 44 |
| frequency | 0.747752 | 0.708908–0.884802 | 44 |
| p_reuse | 0.883509 | 0.873660–0.936839 | 44 |
| AG | -0.074421 | -0.110075–0.000000 | 44 |
| TS | 0.000000 | 0.000000–0.000000 | 44 |

## Skill utility associations (descriptive, seed-cluster bootstrap)

| Association | Spearman ρ | 95% cluster-bootstrap CI |
|---|---:|---:|
| SU_vs_future_net_value | 0.936960 | 0.896692–1.000000 |
| SU_vs_reuse_count | 0.936960 | 0.897818–1.000000 |
| SU_vs_cross_family_transfer | 0.921589 | 0.903732–0.960374 |

## Sensitivity and ablations

Primary MC is a modeled normalized maintenance cost, not empirical compute cost.

| MC per eligible opportunity | SCT mean net value |
|---:|---:|
| 0.00 | 0.945000 |
| 0.03 | 0.645000 |
| 0.06 | 0.345000 |
| 0.12 | -0.255000 |

| Threshold | Mean net value |
|---|---:|
| high_q75 | 0.018333 |
| low_q25 | 0.418333 |
| medium_q50 | 0.018333 |
| primary | 0.345000 |

| Lifecycle mode | Mean net value |
|---|---:|
| lifecycle_enabled | 0.345000 |
| lifecycle_disabled | 0.345000 |
| enabled_minus_disabled | 0.000000 |

No-SCV ablation is the matched ALWAYS_CREATE arm. Composition is tested against paired best-single results and on a separate task stream.


## Candidate birth categories

| Category | Candidate rows |
|---|---:|
| reflection | 22 |
| rotation | 22 |

Detailed evidence: `skill_births.json`, `candidate_level.csv`, `matched_controls.csv`, `mc_sensitivity.csv`, `threshold_sensitivity.csv`, `reuse_statistics.csv`, `utility_trajectories.csv`, `lifecycle.csv`, `lifecycle_ablation.csv`, and `composition.csv`.

Nulls, rejected candidates, failed applications, no-match opportunities, and missing-family compositions are retained in the full record.
