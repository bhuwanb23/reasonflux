# Phase 13D Transfer v1 — results

> **Post-run correction required:** the frozen reporter had a pairwise-key lookup defect for ASFT vs B2/B3/B4 and ASFT vs best-single, and its composition summary did not require source-component coverage or active composition. The original `criteria.json`/aggregate are preserved for audit, but their baseline/composition dashboard fields are not authoritative. Use `posthoc_analysis.md`, `posthoc_corrected_criteria.json`, and `posthoc_pairwise_baselines.csv`, which recompute from saved seed/task rows without rerunning or changing outcomes.

**Seeds:** 10; **task-level rows:** 14400.
**Dataset:** synthetic-transfer-v1. This is not ARC evidence. B4 is a compression proxy, not DreamCoder.

## Frozen criteria

```json
{
  "ASFT_pooled_vs_baselines": {
    "B1_NO_LEARNING": {
      "ci95": [
        null,
        null
      ],
      "mean": null,
      "n": 0,
      "positive_seeds": 0,
      "sd": null,
      "stable_positive": false,
      "status": "unavailable"
    },
    "B2_MEMORY_ONLY": {
      "ci95": [
        null,
        null
      ],
      "mean": null,
      "n": 0,
      "positive_seeds": 0,
      "sd": null,
      "stable_positive": false,
      "status": "unavailable"
    },
    "B3_RANDOM_SKILLS": {
      "ci95": [
        null,
        null
      ],
      "mean": null,
      "n": 0,
      "positive_seeds": 0,
      "sd": null,
      "stable_positive": false,
      "status": "unavailable"
    },
    "B4_COMPRESSION_PROXY": {
      "ci95": [
        null,
        null
      ],
      "mean": null,
      "n": 0,
      "positive_seeds": 0,
      "sd": null,
      "stable_positive": false,
      "status": "unavailable"
    }
  },
  "ablation_degradation": {
    "A1_NO_INVARIANTS": {
      "ci95": [
        0.016727272727272716,
        0.019999999999999987
      ],
      "mean": 0.018909090909090896,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.0034497574474564134,
      "stable_positive": true,
      "status": "passed"
    },
    "A2_NO_SCT": {
      "ci95": [
        0.0,
        0.0
      ],
      "mean": 0.0,
      "n": 10,
      "positive_seeds": 0,
      "sd": 0.0,
      "stable_positive": false,
      "status": "failed"
    },
    "A3_NO_PERSISTENCE": {
      "ci95": [
        0.015054545454545442,
        0.017999999999999988
      ],
      "mean": 0.017018181818181807,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.0031047817027107724,
      "stable_positive": true,
      "status": "passed"
    },
    "A4_NO_COMPOSITION": {
      "ci95": [
        0.0,
        0.0
      ],
      "mean": 0.0,
      "n": 10,
      "positive_seeds": 0,
      "sd": 0.0,
      "stable_positive": false,
      "status": "failed"
    }
  },
  "association_status": {
    "IS_vs_TS": "failed",
    "SU_vs_TS": "failed",
    "TS_vs_CGR": "passed"
  },
  "composition_structural_vs_B1": {
    "per_experiment": {
      "EXP-TR-07": {
        "beats_baseline": true,
        "ci95": [
          0.014000000000000012,
          0.020000000000000018
        ],
        "mean": 0.018000000000000016,
        "n": 10,
        "paired_cohens_dz": 2.8460498941515415,
        "per_seed": [
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.0,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018
        ],
        "sd": 0.006324555320336764
      },
      "EXP-TR-08": {
        "beats_baseline": true,
        "ci95": [
          0.014000000000000012,
          0.020000000000000018
        ],
        "mean": 0.018000000000000016,
        "n": 10,
        "paired_cohens_dz": 2.8460498941515415,
        "per_seed": [
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.0,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018
        ],
        "sd": 0.006324555320336764
      },
      "EXP-TR-09": {
        "beats_baseline": true,
        "ci95": [
          0.020000000000000018,
          0.020000000000000018
        ],
        "mean": 0.020000000000000018,
        "n": 10,
        "paired_cohens_dz": null,
        "per_seed": [
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018,
          0.020000000000000018
        ],
        "sd": 0.0
      },
      "EXP-TR-10": {
        "beats_baseline": true,
        "ci95": [
          0.03399999999999992,
          0.039999999999999925
        ],
        "mean": 0.03799999999999992,
        "n": 10,
        "paired_cohens_dz": 6.008327554319903,
        "per_seed": [
          0.039999999999999925,
          0.039999999999999925,
          0.039999999999999925,
          0.039999999999999925,
          0.039999999999999925,
          0.019999999999999907,
          0.039999999999999925,
          0.039999999999999925,
          0.039999999999999925,
          0.039999999999999925
        ],
        "sd": 0.006324555320336764
      },
      "EXP-TR-11": {
        "beats_baseline": true,
        "ci95": [
          0.03400000000000003,
          0.040000000000000036
        ],
        "mean": 0.038000000000000034,
        "n": 10,
        "paired_cohens_dz": 6.008327554319921,
        "per_seed": [
          0.040000000000000036,
          0.040000000000000036,
          0.040000000000000036,
          0.040000000000000036,
          0.040000000000000036,
          0.020000000000000018,
          0.040000000000000036,
          0.040000000000000036,
          0.040000000000000036,
          0.040000000000000036
        ],
        "sd": 0.006324555320336764
      }
    },
    "summary": {
      "ci95": [
        0.0232,
        0.028000000000000004
      ],
      "mean": 0.026400000000000003,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.005059644256269412,
      "stable_positive": true,
      "status": "passed"
    }
  },
  "composition_structural_vs_best_single": {
    "RCR_difference": {
      "ci95": [
        0.02828282828282828,
        0.0404040404040404
      ],
      "mean": 0.03636363636363636,
      "n": 10,
      "positive_seeds": 9,
      "sd": 0.012776879435023755,
      "stable_positive": true
    },
    "TS_difference": {
      "ci95": [
        null,
        null
      ],
      "mean": null,
      "n": 0,
      "positive_seeds": 0,
      "sd": null,
      "stable_positive": false
    },
    "exact_accuracy_difference": {
      "ci95": [
        0.0,
        0.0
      ],
      "mean": 0.0,
      "n": 10,
      "sd": 0.0
    },
    "status": "unavailable"
  },
  "criteria_are_descriptive_not_guaranteed": true,
  "negative_transfer": {
    "forced_accuracy_NTR": 0.0,
    "forced_diagnostic_n": 190,
    "forced_harm_rate": 1.0,
    "safe_reflection_rejection_rate": 1.0,
    "safe_reflection_retrieval_n": 90,
    "safe_reflection_retrieval_unavailable_n": 10,
    "status": "passed"
  },
  "overall_criteria_status": {
    "ablation_degradation": "failed",
    "capability_growth_association": "passed",
    "composition_and_structural_transfer_vs_no_learning": "passed",
    "composition_and_structural_value_vs_best_single": "unavailable",
    "invariant_skill_transfer_association": "failed",
    "negative_transfer_detected_correctly": "passed",
    "outperform_all_mandatory_baselines": "unavailable",
    "positive_reasoning_cost_reduction": "passed",
    "positive_transfer_across_taxonomies": "passed",
    "successful_skill_reuse": "passed"
  },
  "positive_RCR_normalized_raw": {
    "ci95": [
      0.13197887970615244,
      0.15794306703397612
    ],
    "mean": 0.14928833792470156,
    "n": 10,
    "positive_seeds": 10,
    "sd": 0.02736865651706793,
    "stable_positive": true,
    "status": "passed"
  },
  "positive_TS_by_taxonomy": {
    "compositional": {
      "TS_approximately_zero": false,
      "ci95": [
        0.016000000000000014,
        0.020000000000000018
      ],
      "mean": 0.018666666666666682,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.004216370213557843,
      "stable_positive": true,
      "status": "passed"
    },
    "moderate": {
      "TS_approximately_zero": false,
      "ci95": [
        0.011333333333333343,
        0.013333333333333345
      ],
      "mean": 0.012666666666666677,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.0021081851067789215,
      "stable_positive": true,
      "status": "passed"
    },
    "near": {
      "TS_approximately_zero": false,
      "ci95": [
        0.01133333333333328,
        0.013333333333333272
      ],
      "mean": 0.012666666666666607,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.0021081851067789098,
      "stable_positive": true,
      "status": "passed"
    },
    "structural": {
      "TS_approximately_zero": false,
      "ci95": [
        0.033999999999999975,
        0.03999999999999998
      ],
      "mean": 0.03799999999999998,
      "n": 10,
      "positive_seeds": 10,
      "sd": 0.006324555320336764,
      "stable_positive": true,
      "status": "passed"
    }
  },
  "positive_success_gated_RCR": {
    "ci95": [
      0.13197887970615244,
      0.15794306703397612
    ],
    "mean": 0.14928833792470156,
    "n": 10,
    "positive_seeds": 10,
    "sd": 0.02736865651706793,
    "stable_positive": true,
    "status": "passed"
  },
  "seed_count": 10,
  "successful_reuse_observed": true
}
```

## Correlations

```json
{
  "IS_vs_TS": {
    "ci95": [
      -0.13180725482391617,
      1.1503928309212791e-17
    ],
    "n": 114,
    "n_clusters": 10,
    "r": -0.04237359723307037,
    "status": "cluster_bootstrap_descriptive"
  },
  "SU_vs_TS": {
    "ci95": [
      -0.07254762501100125,
      3.4499101875375955e-17
    ],
    "n": 114,
    "n_clusters": 10,
    "r": -0.012945593956343641,
    "status": "cluster_bootstrap_descriptive"
  },
  "TS_vs_CGR": {
    "ci95": [
      0.48203723570562534,
      0.4842001247062523
    ],
    "n": 36,
    "n_clusters": 9,
    "r": 0.4833925171277064,
    "status": "cluster_bootstrap_descriptive"
  }
}
```

## Evidence package

Figures: figure_01_transfer_taxonomy.svg, figure_02_TS_by_family.svg, figure_03_reasoning_cost_reduction.svg, figure_04_transfer_growth.svg, figure_05_positive_negative_transfer.svg

Tables: table_near.csv, table_moderate.csv, table_compositional.csv, table_structural.csv, table_matched_baselines.csv, table_matched_ablations.csv

Search candidate evaluations remain null where the legacy solver exposes no canonical counter. All task/seed outcomes, including failures and unavailable cells, are in the JSONL and seed-level records.
