# Phase 1F.9 — Dataset and Split Protocol

## Independent unit and ordering

Independent unit is an agent-run × task-family-seed panel; exposure points, tasks, rounds, outputs, and memory probes are nested. Freeze predictors at time t, then evaluate future external tests. Task-family/template/domain seeds and gold labels remain unseen at predictor time. No future prompts, demonstrations, or answers enter memory, capability stores, C_t, IG, or model tuning.

## Three-way split

| Split | Permitted use | Prohibited use |
|---|---|---|
| Development | Build task generators/rubrics, select model family, calibrate thresholds/SOI/resource limits, estimate cluster variance and required N. | No confirmatory claims. Never carry development labels into final future targets. |
| Confirmatory | One frozen primary AULC prediction test and preregistered secondary battery outcomes. | No model/threshold/task changes, outcome-driven exclusions, or interim efficacy peeking. |
| Replication | Repeat the frozen battery, scoring, predictor features, and analysis on disjoint task templates, seeds, and preferably domains. | No tuning from confirmatory or replication outcomes. |

A–F are represented in both confirmatory and replication. Exposure/training tasks, future probes, and replication templates are partitioned by family and near-duplicate checks. Adaptation shifts and future learning tasks remain unseen until their scheduled tests.

## Metric separation and target lock

1. Compute B1–B5 and IG_t from data available only through time t; log source and timestamps.
2. Lock the future task manifest, gold/rubric stores, resource/exposure plan, and scoring-code hashes.
3. Run policies without future gold or IG-dependent task selection.
4. Score A–F from behavior only; compute AULC/profile without importing the IG module.
5. Hash/lock outcomes and missingness before joining IG, C_t, TS, and comparator snapshots.
6. Conduct the preregistered predictive analysis; release all outcomes and statuses by test/family.

## Required manifest fields

Split/test/family/template/domain IDs and hashes; generator/evaluator/rubric versions; agent and task seeds; time-t predictor snapshot; B1–B6 derivation and provenance; memory/experience/transfer logs; future task prompts and gold hashes; exposure points; resource caps/actual use; output/scoring records; missingness/exclusion reasons; access/lock timestamps; model and analysis code hashes; independent-unit mapping; replication mapping. Confirmatory and replication manifests must be disjoint and immutable.