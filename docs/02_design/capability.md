# Capability Representation (Phase 11E-1)

Foundation of Contribution 3 (CGM). A **capability** is a stable, reusable,
transferable collection of skills that enables performance across a family of
tasks. Code under `src/capability/`. Thresholds: `configs/thresholds.yaml`
(`capability:`).

**Principle:** Skills are not capabilities. ASFT measures intelligence as the
evolving structure of capabilities, not task scores or raw skill counts.

## Hierarchy

| Level | Object | Implementation |
| --- | --- | --- |
| L0 | Experiences | traces / tasks |
| L1 | Invariants | `src/invariants` |
| L2 | Skills | `src/skills` |
| L3 | Capability clusters | `Capability` |
| L4 | System capability state | existing `CapabilityState` |

## Types

`atomic` · `composite` · `cross_domain` · `emergent`

Multi-membership is allowed: one skill may belong to several capabilities.

## Scores

```
CCov = |supported_families| / max(total_families, ccov_family_norm)
CapU = w_su·mean(SU) + w_ts·mean(TS) + w_cov·CCov + w_comp·comp_bonus
```

**Strength** = maturity (skill count, reuse, transfer, CapU stability).  
**Confidence** = evidence / transfer / consistency (independent of CapU).

## Lifecycle

```
emerging → developing → established → core
                ↘ declining → archived
```

Ghost guard: no transfer evidence → cannot become established.

## Portfolio and graph

`CapabilityLibrary` + `CapabilityGraph` (shared_skill / transfer / composition
edges). `compute_capability_portfolio` syncs `mean_capu`, `core_count`,
`capability_ids` into `CapabilityState`. Opt-in CGR sync via
`write_growth=True` (11E-2); opt-in IG/IGR/stage via `write_intel=True` (11E-3).

## Constraints and representation failures

Valid capability: ≥1 skill, transfer evidence, CapU floor, supporting evidence.

| Failure | Detection |
| --- | --- |
| Fragmentation | too many tiny capabilities |
| Monolith | one capability owns ≥ `monolith_skill_fraction` of skills |
| Overlap | Jaccard membership ≥ `overlap_similarity` |
| Ghost | claim without transfer |

## File map

| Module | Role |
| --- | --- |
| `config.py` | `CapabilityConfig` |
| `states.py` | lifecycle FSM |
| `models.py` | `Capability` |
| `coverage.py` / `utility.py` / `scores.py` | CCov, CapU, strength/confidence |
| `evidence.py` | evidence buckets |
| `lifecycle.py` | advance |
| `library.py` / `graph.py` / `portfolio.py` | memory structures |
| `constraints.py` / `failures.py` | validity + representation guards |
| `emerge.py` | propose from skill library |

## Intelligence (11E-3)

Intelligence ≠ capability stock. Measured as IG / IGR / IA / IE / elasticity in
`src/evaluation/intelligence*.py`. See [metrics.md](metrics.md).

## Failure modes (11E-5)

Capability ecosystem hardening (CF1–CF10, CHS/CS, hard growth gate, recovery):
[capability_failure_modes.md](capability_failure_modes.md).

## Non-goals

Paper-scale experiment checklist beyond CGM measurement; interactive dashboards;
re-deriving CapU / CGR / IG formulas.
