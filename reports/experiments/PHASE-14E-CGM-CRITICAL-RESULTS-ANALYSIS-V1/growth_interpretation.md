# Growth Interpretation

## Phase 13E within-cohort result

C_t is non-decreasing in all 10 ASFT seeds. Mean seed-level CGR is `0.2946` (95% CI `[0.2857,0.3036]`). This supports repeated movement in the frozen capability-score measure in the Phase 13E synthetic cohort.

The round path is not a steady accumulation of new capability objects: mean CGR is `0.8405` at round 1 (the initial transition from previous C_t=0), then `0.1194`, `0.1523`, and `0.0663`. Capability count stays one at all rounds. This is best described as score growth of a persistent portfolio, with an initialization jump and subsequent changes in skill-member evidence.

## Cross-phase limit

Corrected Phase 13D mean CGR is `-0.060` over nine evaluable seeds. Phase 13D and 13E use separate frozen seed blocks and experimental contexts, so do not average them or declare the formula invalid. The sign change means robust growth across generators/contexts is not established.

## Prediction: distinguish two questions

- TS→CGR in Phase 13E: `r=-0.5027`, 95% Fisher CI `[-0.8601,0.1857]`; uncertain, not evidence that transfer drives growth.
- C_t at round t→next-round task utility in Phase 13E: `r=0.0498`, 95% cluster-bootstrap CI `[0.0163,0.0922]`; passes its preregistered directional criterion but is tiny and within the same generator.

The latter is some predictive association; it is not a causal effect, not the same as TS→CGR, and not evidence of practically meaningful/general prediction.
