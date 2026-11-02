# Phase 1D.4 — Budget-Matching Protocol

## Common caps

Every competitive arm receives identical maximums per panel/query. The values below are a design baseline for development; they must be validated and frozen before confirmation. Equal caps do not mean equal realized usage—actual storage, compute, retrieval, and exposure are instrumented and reported.

| Resource | Common cap | Unit / enforcement |
|---|---:|---|
| Training exposure | 24 | Same training episodes/tasks and demonstrations per panel. |
| Persistent storage | 4,096 | Serialized bytes across all learned items, including indexes/metadata. |
| Candidate/item units | 24 | Total memory records, fragments, patterns, rules, or hybrid mixture; one common item cap. |
| Training construction compute | 50,000 | Deterministic solver/feature operations; instrumented counter, same ceiling. |
| Query/inference compute | 2,000 | Operations per future task; same base-solver inclusion rule. |
| Retrieval inspection | 4 | Maximum memory/pattern/skill items inspected per query; hybrid total, not per subsystem. |
| Future horizon | 12 per family | Same number of held-out task opportunities per family and arm in the design fixture. |

Oracle is excluded from competitive resource comparisons and reported only as an analysis ceiling. B5 No Learning has the same allowed compute cap but stores zero learned items; unused storage is not redistributed.

## Matching rules

1. Freeze task exposure, training examples, total serialized-byte cap, item count, construction-compute cap, query-compute cap, retrieval count, and future task horizon for every arm.
2. Hybrid M5's memory items and abstraction rules share one storage, item, construction, query-compute, and retrieval budget; there are no separate hidden allowances.
3. Count serialized indexes, embeddings, caches, and retrieval metadata as storage. Count failed retrieval attempts and validation checks as compute/retrieval work.
4. Log both available cap and realized use per arm/task. A policy that uses less may benefit via the frozen resource-cost model; it does not get extra opportunities.
5. Primary utility subtracts calibration-derived storage/compute costs using fixed conversion coefficients. Coefficients are calibrated without confirmatory outcomes and sensitivity-tested before lock.
6. If a system exceeds any hard cap, retain the run and mark the affected comparison invalid/unavailable; do not silently truncate one arm differently.

## Audit fields

`arm_id`, `panel_id`, `training_episode_count`, `stored_object_count`, `serialized_bytes`, `construction_ops`, `query_ops`, `retrieval_candidates_inspected`, `successful_retrievals`, `abstentions`, `task_opportunities`, `runtime/version`, and budget-overrun flags are mandatory. Byte and operation measurements are not inferred from object counts.