# ASFT Implementation Roadmap

## Status

| Phase | Content | Status |
| --- | --- | --- |
| 0–9 | Research, theory, eval/paper blueprint | Complete (docs) |
| 10 | Engineering blueprint | Complete (docs) |
| 11A | Repository & code architecture scaffold | Complete |
| 11B–11E | Core models, IDT, SCT, transfer, CGM, capability robustness | Complete |
| 11F | Implementation-ready blueprint | Complete |
| 11 | Trace capture → end-to-end pipeline → evidence | **Complete** |
| 12 | Scale + ablation tables + ARC validation | Next |
| 13+ | Experiments, results, paper | After Phase 12 |

Per-gate status: [v0_1_readiness.md](v0_1_readiness.md).
Module registry: [implementation_blueprint.md](../02_design/implementation_blueprint.md).
Completion notes: [phase_11_completion.md](../03_implementation/notes/phase_11_completion.md).

## MVP build order — all complete

1. Core models (`src/core`) — Phase 11B
2. Invariant mining, validation, ranking, robustness (`src/invariants`) — 11C
3. Skill candidate → economics → promotion → library → lifecycle → composition (`src/skills`) — 11D
4. Transfer memory, scores, graph, transfer-aware ranking (`src/transfer`) — 11C-4
5. Capability representation, growth, intelligence, robustness (`src/capability`, `src/evaluation`) — 11E
6. Layered evaluation harness, baselines, ablations, reports (`src/evaluation/harness`) — 11E-4/5
7. Trace producer + solver (`src/solver`, `src/traces`) — 11 completion
8. Phase pipelines (`run_trace/invariant/skill_pipeline`) — 11 completion
9. Skill application (`ReuseEngine.apply`) — 11 completion
10. End-to-end entry point (`run_full_asft_pipeline`) — 11 completion
11. Figures + experiment runners (`plot_metric`, exp01–05) — 11 completion

## Version plan

| Version | Scope |
| --- | --- |
| v0.1 | Research prototype — synthetic tasks, IDT + SCT + CGM, paper evidence |
| v0.2 | Concept layer |
| v1.0 | ARC integration |

## Immediate next step

**Phase 12 — scale and external validity.** The pipeline runs end to end on
synthetic grids and beats all baselines. What remains before paper submission:

1. Point the Task System at `datasets/arc/` (the solver interface already takes
   any `GridTask`).
2. Run multiple seeds and report confidence intervals.
3. Add the A1–A5 ablation table to `exp05` (the transforms already exist in
   `evaluation/harness/baselines.py`).
