# Phase 1F.3 — Intelligence Taxonomy

These are behaviorally distinct, separately scored dimensions. They are not inferred from the IG formula or collapsed into a single intelligence score.

| Type | Construct | Independent measure |
|---|---|---|
| I1 Learning Speed | Rate of acquiring competence from new examples. | Held-out accuracy curve at 0, 1, 3, and 5 examples; normalized learning-curve area and slope. |
| I2 Adaptation Ability | Recovery after rules/distributions change. | Held-out recovery curve and exposure-to-criterion after a fixed shift; pre-shift and no-shift controls. |
| I3 Transfer Ability | Benefit of prior learning on a disjoint family/domain. | Paired target-domain learning curve versus no-prior-transfer and random baselines. |
| I4 Compositional Learning | Acquisition of unseen combinations of known components. | Few-shot accuracy on held-out novel compositions against best-single-component controls. |
| I5 Generalization Ability | Competence on held-out instances, templates, environments, and delayed variants. | Novel-environment success and delayed generalization probes with no exact test exposure. |
| I6 Knowledge Efficiency | Competence gained per fixed example/token/compute budget. | External learning AULC or examples-to-criterion at a fixed resource cap; report absolute utility as well. |

Each dimension receives its own estimate, interval, denominator, and status. A dimension can be unavailable without imputing zero. A positive I1 result does not automatically establish I2–I6.