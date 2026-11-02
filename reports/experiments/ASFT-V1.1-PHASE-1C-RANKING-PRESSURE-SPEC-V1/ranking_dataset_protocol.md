# Phase 1C.8 — Ranking Dataset and Split Protocol

## Unit and panel construction

A panel is one independently seeded candidate-discovery block paired with a fixed future-task block. It contains N=40 eligible unique candidate structures, a common feature-card snapshot, K=8 decisions per ranker, and H common held-out opportunities. Candidate duplicates are removed only by exact canonical representation/hash before ranks; no semantic family is deduplicated after observing a policy's order. Candidate IDs are split-specific opaque hashes; arrival order is randomized independently of labels.

The independent unit for primary inference is the panel cluster (including its task-family/seed block). Candidate rows and task opportunities nested within it are not independent observations. Power/precision uses the number of independent panel clusters, not N×H.

## Required splits

| Split | Permitted use | Prohibited use |
|---|---|---|
| Calibration | Fit/freeze normalization, cost conversion, R1 calibration transfer score, reuse/compression feature computation, and variance inputs. | Confirmatory endpoint selection or tuning against confirmatory outcomes. |
| Development | Debug generator/runner, verify quota/pressure mechanics, compare preregistered pressure gates, and calibrate sample size. | Final superiority claim; access to confirmatory/replication labels. |
| Confirmatory | One frozen evaluation of R1–R5 and post-lock R6 Oracle. | Any tuning, threshold changes, pool curation, K changes, or replacement by outcome direction. |
| Replication | Repeat frozen design on disjoint task-family/template and seed blocks. | Tuning either confirmatory or replication methods. |

Candidate discovery history and future test history must be disjoint task instances. Family-level separation is enforced where the claim is cross-family transfer. Candidate semantics may recur across splits only under the preregistered identity rule; all source/task provenance is retained for leakage audits. No task, demonstration, trace, near-duplicate template, solver output, or future label may cross from confirmation/replication into feature calibration.

## Pool eligibility and pressure

All confirmatory cards are assembled and hashed before outcomes. Hidden generator labels/recipe counts verify that the synthetic stress generator follows B/C quotas; no future task scores are read for pool construction. Pressure is run on the complete prospective confirmatory pools before outcome access. If any frozen pressure gate fails, do not drop that panel silently or inspect its outcomes; mark the study pressure gate blocked/unavailable and follow only an already preregistered resolution.

## Required manifest and audit trail

Record split assignments, task and family IDs, candidate canonical hashes, opaque IDs, source traces, generator/code/config hashes, feature derivation inputs, random seeds, rank lists, Top-K lists, pressure metrics, outcome-store checksum/access log, evaluation code hash, missingness reasons, and ranker resource counters. Freeze manifest and access protocol before confirmation.

## Scope

Phase 1C defines the split rules; it has not generated calibration, development, confirmatory, or replication datasets. Sample size, real task runner, and sealed outcome-store implementation remain later execution gates.