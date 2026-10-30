# ASFT Implementation Roadmap

## Status

| Phase | Content | Status |
| --- | --- | --- |
| 0–9 | Research, theory, eval/paper blueprint | Complete (docs) |
| 10 | Engineering blueprint | Complete (docs) |
| 11A | Repository & code architecture scaffold | Complete (this repo layout) |
| 11B+ | Data models, algorithms, pipelines | Next |
| 12+ | Experiments, results, paper | After implementation |

## MVP build order (from Phase 11A)

1. Core models (`src/core`) — Phase 11B
2. Trace Logger (`src/traces/logger.py`)
3. Trace Store (`src/traces/trace_store.py`)
4. Invariant Detector (`src/invariants/`)
5. IS metrics (`src/invariants/strength.py`, evaluation)
6. Skill Trigger (`src/skills/trigger.py`)
7. Skill Library (`src/skills/library.py`)
8. Transfer Engine (`src/transfer/`)
9. Evaluation Engine (`src/evaluation/`)
10. Experiments (`experiments/exp01` … `exp05`)

## Version plan

| Version | Scope |
| --- | --- |
| v0.1 | Research prototype — synthetic tasks, IDT + SCT + CGM |
| v0.2 | Concept layer |
| v1.0 | ARC integration |

## Immediate next step

**Phase 11B** ([docs/plan/phase_11b.md](plan/phase_11b.md)): specify and implement `Task`, `ReasoningTrace`, `Invariant`, `Skill`, `CapabilityState`, module interfaces, and serialization.
