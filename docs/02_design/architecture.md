# ASFT Repository Architecture

Engineering map for the Adaptive Skill Formation Theory prototype (Phase 11A).

## Design rule

Organize around **research contributions**, not algorithms:

| Contribution | Code modules |
| --- | --- |
| IDT | `src/traces`, `src/invariants` |
| SCT | `src/skills` |
| CGM | `src/capability` (representation), `src/evaluation` (growth + harness) |
| Transfer hypothesis | `src/transfer` |
| End-to-end ASFT | `src/pipelines` |

Shared knowledge objects live in `src/core`. Baselines stay under `baselines/` and must not mix with ASFT code. Notebooks are exploration only — no production logic.

## Core ontology and memory layers (Phase 11B)

Knowledge objects in `src/core/`:

| Object | Module | Role |
| --- | --- | --- |
| `Task` | `task.py` | Temporary problem instance |
| `ReasoningTrace` | `trace.py` | Raw learning material |
| `Invariant` | `invariant.py` | Recurring structure (observation) |
| `Concept` | `concept.py` | Lightweight semantic link (MVP) |
| `SkillCandidate` / `Skill` | `skill.py` | SCT promotion path |
| `CapabilityState` | `capability.py` | CGM system snapshot (L4) |
| `Capability` | `src/capability` | Capability clusters (L3, Phase 11E-1) |

Three memory layers (`src/core/memory.py`) mirror the ASFT thesis:

```
Experience Memory (tasks, traces)
 → Abstraction Memory (invariants, concepts)
 → Capability Memory (skills, CapabilityLibrary, capability state)
```

Module boundaries are typed in `src/core/contracts.py` (`TraceBatchProvider`, `ValidatedInvariantProvider`, `PromotedSkillProvider`, `SkillUsageStatsProvider`). Lifecycle enums and transitions live in `src/core/states.py`.

## Top-level layout

```
reasonflux/
├── configs/          # YAML — no hardcoded thresholds in source
├── datasets/         # synthetic first, ARC second
├── src/              # packages (core, solver, traces, invariants, skills, ...)
├── experiments/      # one folder per paper experiment
├── baselines/
├── tests/
├── reports/          # generated figures, tables, metrics, logs
├── notebooks/
├── papers/
└── docs/             # research phases + this engineering map
```

## Data flow

```
Task
 → Solver (src/solver)
 → Trace Logger
 → Trace Store
 → Trace Mining (normalize → segment → extract → aggregate → candidates)
 → Invariant Detector / Ranking (11C-3)
 → Skill Trigger
 → Skill Library
 → Reuse Engine (transfer + measured TS)
 → Capability Growth (C_t / CGR) and Intelligence (IG)
 → Evaluation Engine
 → Reports
```

Trace mining details: [docs/mining.md](mining.md). Invariant qualification:
[docs/invariants.md](invariants.md). Ranking & validation:
[docs/validation.md](validation.md). Transfer-aware discovery:
[docs/transfer.md](transfer.md). Failure modes & hard gate:
[docs/failure_modes.md](failure_modes.md). Skill creation (SCT):
[docs/skills.md](skills.md). Skill utility economics:
[docs/skill_economics.md](skill_economics.md). Skill lifecycle:
[docs/lifecycle.md](lifecycle.md). Skill composition:
[docs/composition.md](composition.md). Skill failure modes:
[docs/skill_failure_modes.md](skill_failure_modes.md). Capability representation:
[docs/capability.md](capability.md). Capability failure modes:
[docs/capability_failure_modes.md](capability_failure_modes.md).

## Module dependency graph

```
core
 ├─ traces
 ├─ invariants
 ├─ skills
 ├─ capability
 ├─ transfer
 └─ evaluation

pipelines  →  orchestrates the above

solver     →  produces experience (no dependency on evaluation)

evaluation must NOT depend on experiments
```

Module-level build spec, status per module, and the stub inventory:
[implementation_blueprint.md](implementation_blueprint.md). Its registry is
[`configs/modules.yaml`](../../configs/modules.yaml), enforced by tests.

## Configuration

| File | Role |
| --- | --- |
| `configs/default.yaml` | project paths, seed |
| `configs/thresholds.yaml` | IS / SCV decision thresholds |
| `configs/metrics.yaml` | metric name/formula registry |
| `configs/experiments.yaml` | experiment enable flags |

## v0.1 exclusions

LLMs, neural networks, meta-reasoner, concept graphs, ARC-3 agents, world models, autonomous planning.
