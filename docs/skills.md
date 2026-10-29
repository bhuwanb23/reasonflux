# Skill Creation Trigger Theory (Phase 11D-1)

Bridge from IDT promotable invariants to reusable skills. Code under `src/skills/`.
Thresholds: `configs/thresholds.yaml` (`skills:`).

**Principle:** A skill is not created because a pattern exists. It is created only
when validated evidence shows the invariant can repeatedly reduce future
reasoning cost through transferable reuse.

## Definition

A **skill** is a reusable executable capability derived from a validated
invariant that consistently reduces future reasoning cost across multiple tasks.

**Not a skill:** one-off solutions, high-frequency / low-transfer patterns
(e.g. VerifyOutput), or stored exact-output memory.

## Pipeline (7 stages)

```
Promotable Invariant (11C SKILL_CANDIDATE)
 → Intake
 → SkillCandidate (under evaluation)
 → Economic evaluation (SCV)
 → Transfer evaluation (ITS)
 → Promotion + birth event
 → SkillLibrary (Active)
 → Monitoring hooks
```

Public entry: `create_skills_from_invariants(...)`.

## SCV

```
SCV = Reuse × AG × TS − CreationCost
```

Create when `SCV > skill_creation_threshold` (default `0.0`).

## Five qualification tests

1. Frequency support  
2. Consistency support  
3. Transfer support (`TS ≥ min_its`)  
4. Reasoning reduction (AG / reasoning value)  
5. Economic viability (SCV)

Plus: evidence minimum, NTR ≤ limit, duplicate similarity block.

## Birth, evidence, confidence

- `SkillBirthRecord` — when / why / from which invariant  
- `SkillEvidence` — discovery / transfer / utility / negative  
- `compute_skill_confidence` — f(evidence, transfer, consistency)

## MVP categories

reflection · rotation · counting · grouping (signature heuristics)

## File map

| Module | Role |
| --- | --- |
| `config.py` | `SkillConfig` |
| `intake.py` | Stage 1 |
| `candidate.py` | Stage 2 factory |
| `trigger.py` | SCV gate |
| `qualification.py` | Five tests |
| `birth.py` / `evidence.py` | Birth + confidence |
| `promotion.py` | Promote to Active |
| `library.py` | Capability memory |
| `pipeline.py` | End-to-end SCT |
| `monitoring.py` | Stage 7 hooks (+ SU refresh) |
| `retrieval.py` | Condition match, SU ranking |
| `utility.py` / `utility_components.py` | SU + economic status (11D-2) |
| `competition.py` / `portfolio.py` | Rank / portfolio metrics |
| `economics.py` | EFU vs lifetime cost (advisory) |
| `retirement.py` | Retire/archive decisions (no delete) |
| `reactivation.py` | Evidence-gated revival + zombie guard |
| `lifecycle/` | Health, aging, biography, policy, sweep |
| `composition/` | Sequential compose, CU, graph, promote |

## Skill utility (11D-2)

See [skill_economics.md](skill_economics.md). `SU = (RCG+TV+CP+RV)−(CC+MC+NR)`.
Monitoring refreshes `skill.utility`; retrieval prefers higher SU.

## Lifecycle (11D-3)

See [lifecycle.md](lifecycle.md). Growing / Core / Dormant / Retired / Archived
plus reactivation. Default retrieval is the active tier (ACTIVE/GROWING/CORE).

## Composition (11D-4)

See [composition.md](composition.md). Sequential pairs/triples when no single
skill covers the task; promote reusable compositions to Skills.

## Non-goals

Skill failure catalogue (11D-5). Parallel/conditional/recursive composition later.
