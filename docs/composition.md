# Skill Composition (Phase 11D-4)

Skills become building blocks: sequential compositions form higher-level
capabilities. Code under `src/skills/composition/`. Thresholds:
`configs/thresholds.yaml` (`skills:` compose_* / cu_min).

**Principle:** Compose only when no individual skill can cover the task
(`SC < TR`). A composition of skills is powerful; isolated skill count is not.

## Hierarchy

| Level | Form | Implementation |
| --- | --- | --- |
| L0 | Atomic skill | Existing `Skill` |
| L1 | Sequential pair | `skill_ids` length 2 |
| L2 | Sequential multi | length 3 (hard cap `compose_max_skills`) |
| L3 | Capability candidate | `metadata["capability_candidate"]=True` (flag only) |

MVP implements **sequential composition only**. Parallel / conditional /
recursive are out of scope.

## Trigger

`should_compose(requirements, skills)`:

- If any single skill’s `trigger_conditions` cover all requirements → do **not** compose
- Else propose ordered pairs/triples that jointly cover requirements

## Composition Utility

```
CU = TransferGain + ReasoningReduction + ReusePotential − CompositionCost
```

`CompositionCost = compose_cost_base × (n_skills − 1)`. Keep when `CU ≥ cu_min`.

## Lifecycle

```
Candidate → Validated → Reusable → Promoted Skill
         ↘ Discarded (low CU / high NCR)
```

- Do **not** store after a single use (`compose_min_reuse_store`)
- Promote to `Skill` when reuse ≥ `compose_min_reuse_promote` with
  `metadata["composed_from"]`, `execution_policy="compose:…"`

## Graph

`CompositionGraph` records successful directed edges `A→B` for sequential order.
Returned on `ComposeResult` (standalone; no SkillLibrary API break).

## Failure-mode guards (11D-4)

| Mode | Guard |
| --- | --- |
| Explosion | necessity trigger + max candidates + max chain length |
| Redundant | identical ids / consecutive same category / same signature |
| Negative | NCR > `compose_ncr_limit` or low CU → discard |
| Over-specialization | too many `:` literal triggers in merged signature |

## File map

| Module | Role |
| --- | --- |
| `composition/models.py` | Candidate + states |
| `composition/utility.py` | CU |
| `composition/trigger.py` | SC < TR gate |
| `composition/propose.py` | Sequential proposals + guards |
| `composition/evaluate.py` | Evidence, confidence, NCR |
| `composition/lifecycle.py` | Advance + promote |
| `composition/graph.py` | Success edges |
| `composition/compose.py` | `try_compose` orchestrator |

## Non-goals

Parallel / conditional / recursive composition; re-deriving SU math.
Skill failure modes and safeguards: [skill_failure_modes.md](skill_failure_modes.md).
