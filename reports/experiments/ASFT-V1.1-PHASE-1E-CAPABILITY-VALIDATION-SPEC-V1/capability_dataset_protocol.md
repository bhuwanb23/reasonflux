# Phase 1E.8 — Dataset and Split Protocol

## Design and independent unit

A panel is an independently seeded agent/task-generation block with a pre-future measurement time t, predictor snapshot (B1–B5 simple baselines plus CGR_t), and a paired future battery A–F. The independent unit is the agent-run/task-family-seed panel; individual tasks, rounds, capability objects, and repeated probes are nested observations.

## Splits

| Split | Use | Restrictions |
|---|---|---|
| Development | Build task-family generators, evaluator rubric, capability thresholds, model family, leakage checks, and estimate variance. | No confirmatory or replication labels. |
| Confirmatory | One frozen EBCS evaluation and B1–B5 plus CGR_t predictive comparison. | No threshold/model/task tuning, battery replacement, or outcome-based exclusions. |
| Replication | Repeat the frozen protocol on disjoint task-family templates, seeds, and where possible generator/domain. | No tuning from confirmatory or replication results. |

Every battery test A–F appears in both confirmatory and replication; each subtype's required task families and domains are specified before run. Future task instances/templates remain unseen until the test window. Prior-performance features use separate earlier tasks, not the future target items. Experience, memory, and frequency predictors are computed from time-t material only.

## Temporal and family separation

At time t, freeze B1–B5 and CGR_t from all permitted prior evidence. Then lock the future battery manifest, task templates, seeds, evaluator, and target scoring code. Do not expose future task demonstrations or labels to any memory store, skill library, capability score update, or model-fitting process. Use disjoint task instances and near-duplicate detection across development/confirmatory/replication. Retention probes occur after the no-refresh delay; adaptation demonstrations are the only permitted post-shift evidence and are fixed by protocol.

## Independent target computation

Store policy outputs and evaluator gold separately. Compute raw task scores, six battery components, capability-unit labels, EBCS, and ΔEBCS without reading internal metric files. Hash and lock those outputs first; join CGR/C_t/IG predictor snapshots only after the outcome scoring is complete. This ordered pipeline is part of the construct-separation test.

## Manifest

Record split/task/family/template IDs and hashes, domain, generator/evaluator versions, agent seed, predictor snapshot time, B1–B5 and CGR_t derivation fields, CGR/C_t/IG hashes, task outputs, gold-store checksum, capability threshold version, budget use, missingness/exclusion reasons, lock time, and replication mapping. Confirmatory and replication manifests are disjoint and immutable.