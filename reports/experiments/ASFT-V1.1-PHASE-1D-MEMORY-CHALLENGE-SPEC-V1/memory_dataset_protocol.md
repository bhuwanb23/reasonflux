# Phase 1D.7 — Dataset and Split Protocol

## Independent unit

The independent unit is a **panel**: one generator seed/block containing the same training exposure, all six challenge families, one common resource cap, and a paired set of future tasks for every arm. Individual memory items, rules, and tasks nested in a panel are not independent samples. Confirmatory inference clusters at panel/generator-seed level.

## Splits

| Split | Use | Restrictions |
|---|---|---|
| Development | Build/debug task generator and arm interfaces; verify family construct; validate counters and leakage audits; select fixed utility/cost mappings and sample-size assumptions. | No confirmatory or replication task labels. Any tuning stops before confirmation. |
| Confirmatory | One frozen evaluation of B1a–c, B2, B3, B4, B5; B6 Oracle only post-lock. | No tuning, model/prompt changes, memory policy changes, threshold changes, task replacement, or outcome-driven exclusions. |
| Replication | Repeat frozen protocol on disjoint seed/task/template and family instantiations. | No tuning from confirmation or replication outcomes. |

Every family A–F appears in both confirmatory and replication. Within each split, the p×s transition grid is represented as preregistered. Family distributions and weights are fixed in advance; family A is separately reported and is not included in the primary B–F macro-average.

## Training/test task separation

Training exposure is identical across arms and generated from allowed training tasks. Test task IDs, templates, answers, demonstrations, traces, and near-duplicate solutions are not put into any memory or abstraction store, except the explicit Family A exact-repeat treatment. Family A uses a designated training/test pair from a known repeat generator, with the solution entering memory only through the training demonstration. That exception is keyed, allowlisted, and excluded from any claim of generalization.

For B–F, source and target task instances/templates are disjoint under the frozen canonicalization rule; D/E require the stated structural/family shift. Candidate/rule IDs and task IDs are split-specific opaque identifiers. Replication is disjoint by generator seed and task/template block, not merely renamed copies.

## Task creation and quotas

The family definitions and exact-repeat/context-shift grid are generator parameters, not labels assigned after observing arm results. Every planned family/condition cell is retained, even when a system fails or cannot retrieve. No post-outcome balancing or family enrichment is allowed. Report realized counts and any unavailable task rows before interpreting utility.

## Manifest fields

Record panel/seed, split, family/condition, source/task/template hashes, allowed Family A pair link, training exposure IDs, memory/rule object IDs and provenance, per-arm budget cap and use, all retrieval/skill logs, evaluator/code/config hashes, output/gold-store checksum, missingness reason, lock time, and replication mapping.