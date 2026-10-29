# Skill Lifecycle Management (Phase 11D-3)

Skills are living capability assets: they grow, become core anchors, go dormant,
retire, archive, and can reactivate. Code under `src/skills/lifecycle/`,
`retirement.py`, `reactivation.py`. Thresholds: `configs/thresholds.yaml`
(`skills:` lifecycle keys).

**Principle:** Create → Monitor → Evaluate → Grow / Rest → Retire → Possibly
Reactivate. Retirement is not deletion.

## Nine stages

| Stage | `SkillState` | Role |
| --- | --- | --- |
| Candidate | `candidate` | Under SCV evaluation |
| Promoted | `promoted` | Birth into capability memory |
| Active | `active` | In use |
| Growing | `growing` | Positive utility growth (UG) |
| Core | `core` | Capability anchor |
| Dormant | `dormant` | Unused but still useful |
| Retired | `retired` | Insufficient utility (kept in library) |
| Archived | `archived` | Long-retired evidence vault |
| Reactivated | *(event)* | Retired/Archived/Dormant → Active |

## FSM transitions

See `SKILL_TRANSITIONS` in `src/core/states.py`.

**FSM change note (11D-3):** `RETIRED → ACTIVE` and `ARCHIVED → ACTIVE` are
**legal at the FSM level** so reactivation can run. Evidence gates
(`reactivate_min_evidence`, `reactivate_min_expected_su`, zombie guard) live in
`reactivate_skill`, not in `assert_transition`. Earlier tests that forbade
retired revival were updated accordingly.

## Health and aging

```
HS = w_u·SU_norm + w_r·reuse_norm + w_t·TS + w_c·confidence
RW = exp(−λ · t)   # t = tasks since last use
```

`apply_recency(HS, RW)` discounts stale evidence. Bands: healthy / stable /
weak / critical (`health_*` thresholds).

## Biography

`build_biography(skill)` / `append_biography_event(...)` track birth, growth,
peak utility, transfers, failures, retirement, reactivations. All state changes
should go through `apply_lifecycle` so biography stays consistent.

## Lifecycle metrics

| Symbol | Meaning |
| --- | --- |
| SA | Skill age (task ticks) |
| SU | Skill utility (from 11D-2) |
| UG | SU_t − SU_{t−1} |
| RF | reuse / age |
| TS | Transfer score |
| HS | Health (recency-weighted) |

## Policies (high level)

- **Grow:** Active → Growing when `UG > growing_ug`
- **Core:** Growing → Core when SU/TS/reuse/NR gates hold for `core_growth_periods`
- **Decline:** Growing/Core → Active on sustained negative UG
- **Dormant:** Active-tier → Dormant when unused ≥ `dormant_after_tasks` and SU ≥ `su_min`
- **Retire:** when low-SU streak, low reuse/TS, and age ≥ `retire_min_age_tasks`
- **Archive:** Retired → Archived after `archive_after_tasks`
- **Reactivate:** evidence + expected SU; zombie guard blocks repeated failed revivals

Streaks live in `metadata["lifecycle"]`.

## Failure-mode guards (11D-3 only)

| Mode | Guard |
| --- | --- |
| Immortal skills | Retirement on sustained low SU |
| Premature retirement | `retire_min_age_tasks` |
| Dormancy trap | Dormant stays in library; reactivation path |
| Zombie skills | `reactivate_max_attempts` without raised utility |

## File map

| Module | Role |
| --- | --- |
| `lifecycle/health.py` | HS + bands + recency |
| `lifecycle/aging.py` | RW, tasks_since_use, ticks |
| `lifecycle/biography.py` | Timeline |
| `lifecycle/metrics.py` | SA/SU/UG/RF/TS/HS |
| `lifecycle/policy.py` | `decide_lifecycle` |
| `lifecycle/apply.py` | `evaluate_lifecycle` / `apply_lifecycle` |
| `lifecycle/sweep.py` | Library pass |
| `retirement.py` | `retire_skills` (no delete) |
| `reactivation.py` | Evidence-gated revival |

## Non-goals

Composition engine (11D-4), full failure taxonomy / safeguards suite (11D-5),
re-deriving SU math (consume 11D-2).
