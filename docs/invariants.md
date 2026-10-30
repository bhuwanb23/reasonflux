# Invariant Specification (Phase 11C-1)

Executable specification for Contribution 1 — Invariant Discovery Theory (IDT).
Code: `src/invariants/specification.py`, `src/core/invariant.py`, `src/core/states.py`.
Policy thresholds: `configs/thresholds.yaml` (`invariants:`).

## Formal definition

An invariant is a **recurring reasoning structure that remains stable across
multiple successful task-solving experiences and contributes to future transfer**.

All four conditions are required: recurrence, stability, generality, transfer utility.

An invariant is **not** merely a frequent pattern. It is a structure that survives
variation and predicts future transfer.

## Qualification rules

| Rule | Predicate | Default threshold |
| --- | --- | --- |
| `recurrence` | `invariant.frequency >= min_frequency` | 3 |
| `stability` | `invariant.consistency >= min_consistency` | 0.6 |
| `generality` | distinct task families `>= min_task_families` | 2 |
| `transfer_utility` | `evidence.transfer_events >= min_transfer_events` | 1 |

`qualify_invariant(...)` returns every violation; `require_qualification(...)` raises.
An empty violation list means the candidate qualifies.

## Taxonomy

| Type | Meaning | MVP |
| --- | --- | --- |
| `operational` | recurring single operation | yes |
| `procedural` | recurring operation sequence | yes |
| `structural` | higher-level reasoning structure | no |
| `transfer` | structure reused across task families | no |

`classify_invariant_type(pattern, family_count, structural)` assigns the label.
A single operation stays `operational`; multi-step patterns spanning two or more
families become `transfer`.

## Rejection criteria (what is NOT an invariant)

| Criterion | Trigger |
| --- | --- |
| `rare_event` | appears fewer than `min_frequency` times |
| `task_specific_detail` | encodes color/shape/position literals |
| `universal_noise` | generality `>= 0.95` across many families (e.g. `VerifyOutput`) |
| `accidental_correlation` | metadata-only or empty pattern signature |

`apply_rejection_criteria(invariant)` returns the matching criterion names.

## Identity

`InvariantIdentity(origin, pattern_signature, task_families)` produces a stable
`fingerprint` (sha256 over normalized origin + pattern) and `invariant_id`
(`INV-<fingerprint>`). The same structure keeps the same id across runs.

Identity carries origin, pattern, task families, transfer history, and evidence —
so the system can always answer *why does this invariant exist?*

## Evidence model

`InvariantEvidence` records `observations`, `task_families`, `transfer_events`,
`reuse_events`. Without evidence there is no promotion.

`Invariant.record_observation(...)` keeps `frequency` and evidence in sync.

## Confidence model

`confidence_from_evidence(evidence, consistency)` blends recurrence, stability,
family breadth, and transfer evidence, then bands the score:

| Band | Score |
| --- | --- |
| `strong` | `>= strong_score` (0.7) |
| `moderate` | `>= moderate_score` (0.4) |
| `weak` | otherwise |

## Lifecycle

```
candidate → detected → validated → strong → transfer_verified → skill_candidate
                                                                      ↓
                                                                  archived
```

`archived` is terminal. `InvariantState` and `INVARIANT_TRANSITIONS` in
`src/core/states.py` enforce the allowed edges; illegal moves raise
`InvalidStateTransitionError`.

`can_become_skill_candidate(invariant)` is true only in `transfer_verified`
with transfer evidence and no qualification violations.

## Hierarchy

```
operations → patterns → invariants
```

`hierarchy_level_for(invariant)` maps a single operation to `operations`, a
two-step procedural pattern to `patterns`, and longer structures to `invariants`.
`InvariantHierarchy.build(...)` groups a collection by level.

## Ranking & validation (Phase 11C-3)

Candidates from mining must pass F×C×G×T×R ranking and promotion before SCT.
See [docs/validation.md](validation.md).

## Relationship to skills

```
Invariant (observation) → Ranking/Validation → SCT evaluation → Skill Candidate
```

## Relationship to transfer

Transfer is part of the definition, not only the evaluation. Without transfer an
invariant is an interesting pattern; with transfer it is reusable knowledge.

## Success criteria

Invariants recur, remain stable, generalize, predict transfer, and produce
reusable skills.

## Failure criteria

Invariants are unstable, do not transfer, random patterns perform equally well,
or derived skills are useless.
