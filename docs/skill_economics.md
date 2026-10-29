# Skill Utility & Economics (Phase 11D-2)

Post-birth economics: why a skill is worth keeping and how much value it creates.
Code under `src/skills/utility*.py`, `competition.py`, `portfolio.py`, `economics.py`.
Thresholds: `configs/thresholds.yaml` (`skills:` SU block).

**Principle:** Useful skills = better system. Skills are economic assets; existence
alone does not justify retention.

## Skill Utility

```
SU = (RCG + TV + CP + RV) − (CC + MC + NR)
```

| Term | Meaning |
| --- | --- |
| RCG | Reasoning cost gain (`abstraction_gain` or rc_before/after) |
| TV | Transfer success × task coverage |
| CP | Composition potential |
| RV | Normalized reuse × average impact |
| CC | Creation cost |
| MC | Maintenance (base + storage) |
| NR | Negative transfer rate × impact |

`refresh_skill_utility(skill)` writes `skill.utility`, `metadata.utility_breakdown`,
and `metadata.economic_status`.

## Economic status (metadata)

`unproven` → `useful` → `core` | `declining` | `retirement_candidate`

Retirement **execution** lives in 11D-3 lifecycle (`retire_skills` /
`decide_lifecycle`); 11D-2 still sets `retirement_candidate` when `SU < su_min`
as an economic signal.

## Competition

Retrieval and `rank_by_utility` prefer higher SU. `select_dominant` soft-caps to
`library_capacity` (no hard delete).

## Portfolio metrics

| Metric | Formula |
| --- | --- |
| ASU | mean active utilities |
| TSU | max utility |
| PU | sum of positive utilities |
| UG | ASU_now − ASU_prev |
| NTB | mean NR |

## Promotion economics (advisory)

`expected_future_utility(candidate) > lifetime_cost(candidate)` — does **not**
replace SCV birth gates (11D-1).

## Relationship to SCV

| | 11D-1 SCV | 11D-2 SU |
| --- | --- | --- |
| When | At birth | Ongoing |
| Formula | R×TS×AG−CC | (RCG+TV+CP+RV)−(CC+MC+NR) |
| Decision | Create? | Keep / rank / retire-flag? |

## Non-goals

CGR learning. Lifecycle FSM: [lifecycle.md](lifecycle.md). Composition CU:
[composition.md](composition.md).
