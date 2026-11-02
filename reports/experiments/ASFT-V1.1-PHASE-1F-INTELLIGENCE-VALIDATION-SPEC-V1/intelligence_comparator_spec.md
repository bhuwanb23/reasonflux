# Phase 1F.7 — Comparator Framework

## Required predictors and controls

| ID | Comparator | Time-t measurement | Interpretation |
|---|---|---|---|
| B1 | Past performance | Prior external task success/learning profile on disjoint tasks; no future target overlap. | Strong lagged-behavior baseline. |
| B2 | Experience count | Training episodes, demonstrations, eligible tasks, and updates available by t. | Exposure-only explanation. |
| B3 | Capability score | Preserve legacy internal C_t as a separately named predictor; also include prior independent behavior-based capability profile when available. Never use either as the future target. | Tests whether IG adds beyond a capability score; flags internal-metric overlap. |
| B4 | Memory strength | Held-out retrieval precision/coverage over time-t memory, with store capacity/size reported separately. | Tests memory/retrieval explanation. |
| B5 | Transfer metrics | Prior external held-out transfer success plus legacy internal TS in a separately marked model. | Tests whether prior transfer explains future learning. |
| B6 | IG | Frozen IG_t from records through time t. Primary candidate; no formula changes. | Tests incremental predictive validity. |
| R7 | Random/chance baseline | Fixed-seed chance policy/guessing under the same output and resource limits; also use within-split permutation of IG values as a chance-prediction diagnostic. | Establishes a non-learning floor and guards against spurious prediction. |

IGR_t is a separately preregistered key-secondary predictor, tested against the same external primary endpoint with Holm familywise adjustment alongside the IG_t primary test. IE remains exploratory. Neither secondary metric may replace or rescue a failed IG_t primary result after outcomes. B3 C_t and B5 TS are explicitly labeled legacy internal predictors, not independent outcomes; the strongest primary claim requires IG to add information even beyond these declared alternatives.

## Primary comparison

- **M0:** B1+B2+B3+B4+B5, with predictor transforms/model family selected using development only. Preserve external behavior-based capability/transfer measures and the legacy C_t/TS features separately; do not hide their internal provenance.
- **M1:** same M0 plus IG_t.
- **Primary contrast:** blocked, out-of-sample `ΔMAE = MAE(M0) − MAE(M1)` for Test A Future Learning Rate AULC, with positive IG coefficient.
- Compare every required baseline individually and the full M0; do not claim IG wins by beating only chance or the weakest baseline.
- Random/permutation baselines are additional diagnostics, not substitutes for the full M0.

## Interpretation

IG adds predictive evidence only if it improves future external behavioral targets beyond past performance, exposure, capability, memory, and transfer, with positive direction and replication. If simpler variables beat IG or IG adds no meaningful value, that is a valid negative result. Predictive validity is not causal validity.