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
 → Invariant Detector
 → Invariant Ranking
 → Skill Trigger
 → Skill Library
 → Transfer Engine
 → Evaluation Engine
 → Reports
```

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
