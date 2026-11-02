# Phase 1I.6 — Replication Framework

Replication is an independent E4 experiment, not a second analysis of the same outcomes. All replication datasets, seeds, task pools, code/config/analysis versions, and outcome-access logs are identified before replication outcomes are accessed.

| Type | Definition | Claims it can support | Independence requirement |
|---|---|---|---|
| **R1 — Within-generator** | New independent seeds/panels/tasks sampled from the same frozen generator and population. | Reproducibility within that generator/domain. | No reused panels, exposed test labels, or seed reshuffling of the original panel; independent manifest and experimental units. |
| **R2 — Cross-generator** | A materially independent task generator or generative process tests the same estimand/construct. | Generalization across generators that share the target construct. | Independent generator implementation/specification and data lineage; same registered endpoint/estimand or a prospectively harmonized one. |
| **R3 — Cross-domain** | New task domain or operational environment with independently developed data. | Cross-domain generalization within the specified construct. | Independent domain sampling and evaluator; disclose changes needed to instantiate the protocol. |
| **R4 — External benchmark** | Independent external benchmark, evaluator, or public benchmark split under its governing protocol. | External benchmark performance, within the benchmark's scope. | Separate benchmark provenance, compliance with access rules, no repeated exposed holdout; never claim broader validation than the benchmark warrants. |

## Rules

1. One positive E3 result is a single-study result, **not** a generalized finding. Generalization claims require relevant R2, R3, or R4 replication; R1 supports within-generator reproducibility only.
2. E4 uses the same frozen hypothesis direction, primary endpoint, SOI, estimator, baselines, budgets, splits/access rules, and interpretation unless a deviation was preregistered before outcomes. If it materially changes the estimand, report as a new study, not a strict replication.
3. Replication data must be disjoint from development/confirmatory data and independent at the unit level. Different task IDs drawn from one leaked/shared template family may not be independent; document generator/template dependencies.
4. Do not pool E3 and E4 outcomes posthoc merely to obtain significance. Report each separately and give the preregistered combined inference if one was specified.
5. **Concordant support:** the registered confirmatory and replication tests both support the same claim; generalization additionally requires R2/R3/R4 of relevant scope.
6. **Conflict:** one supported and one contradicted result yields an inconclusive/heterogeneous overall claim, not a cherry-picked pass. Investigate only with a new E1/E2 study, then register a new E3/E4 test.
7. **Unavailable/non-informative replication:** does not corroborate the claim. It remains unavailable/non-informative, not a failed empirical effect.
8. Same-holdout repair/rerun, repeated analyst access, or reused outcomes cannot be relabeled as independent replication. Disclose all prior exposure.

## Claim-specific replication

- Mechanism superiority: repeat the fair comparator/ablation contrast with informative decision divergence.
- Measurement/construct validity: repeat against independent external behavior targets, not merely the same internal score components.
- ARC/external claims: use independent, protocol-conformant task manifests and report coverage, activation, accuracy, and unavailability separately; a low-coverage no-activation result does not replicate downstream theory links.
- Universal or cross-domain language requires multiple relevant independent replications; one R4 benchmark still supports only that benchmark's population and evaluation protocol.