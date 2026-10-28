# ASFT Repository Architecture

Engineering map for the Adaptive Skill Formation Theory prototype (Phase 11A).

## Design rule

Organize around **research contributions**, not algorithms:

| Contribution | Code modules |
| --- | --- |
| IDT | `src/traces`, `src/invariants` |
| SCT | `src/skills` |
| CGM | `src/evaluation` |
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
| `CapabilityState` | `capability.py` | CGM snapshot |

Three memory layers (`src/core/memory.py`) mirror the ASFT thesis:

```
Experience Memory (tasks, traces)
 → Abstraction Memory (invariants, concepts)
 → Capability Memory (skills, capability state)
```

Module boundaries are typed in `src/core/contracts.py` (`TraceBatchProvider`, `ValidatedInvariantProvider`, `PromotedSkillProvider`, `SkillUsageStatsProvider`). Lifecycle enums and transitions live in `src/core/states.py`.

## Top-level layout

```
reasonflux/
├── configs/          # YAML — no hardcoded thresholds in source
├── datasets/         # synthetic first, ARC second
├── src/              # packages (core, traces, invariants, skills, ...)
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
 → Trace Logger
 → Trace Store
 → Trace Mining (normalize → segment → extract → aggregate → candidates)
 → Invariant Detector / Ranking (11C-3)
 → Skill Trigger
 → Skill Library
 → Transfer Engine
 → Evaluation Engine
 → Reports
```

Trace mining details: [docs/mining.md](mining.md). Invariant qualification:
[docs/invariants.md](invariants.md). Ranking & validation:
[docs/validation.md](validation.md).

## Module dependency graph

```
core
 ├─ traces
 ├─ invariants
 ├─ skills
 ├─ transfer
 └─ evaluation

pipelines  →  orchestrates the above

evaluation must NOT depend on experiments
```

## Configuration

| File | Role |
| --- | --- |
| `configs/default.yaml` | project paths, seed |
| `configs/thresholds.yaml` | IS / SCV decision thresholds |
| `configs/metrics.yaml` | metric name/formula registry |
| `configs/experiments.yaml` | experiment enable flags |

## v0.1 exclusions

LLMs, neural networks, meta-reasoner, concept graphs, ARC-3 agents, world models, autonomous planning.
