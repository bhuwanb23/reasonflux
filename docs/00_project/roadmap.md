# ASFT Implementation Roadmap

## Status

| Phase | Content | Status |
| --- | --- | --- |
| 0–9 | Research, theory, eval/paper blueprint | Complete (docs) |
| 10 | Engineering blueprint | Complete (docs) |
| 11A | Repository & code architecture scaffold | Complete |
| 11B–11E | Core models, IDT, SCT, transfer, CGM, capability robustness | Complete (libraries + tests) |
| 11F | Implementation-ready blueprint | Complete (spec) |
| 12 | Trace capture → end-to-end pipeline → evidence | Next |
| 13+ | Experiments, results, paper | After Phase 12 |

Honest per-gate status: [v0_1_readiness.md](v0_1_readiness.md).
Module registry and stub inventory:
[implementation_blueprint.md](../02_design/implementation_blueprint.md).

## MVP build order

Completed through Phase 11E:

1. Core models (`src/core`) — Phase 11B
2. Invariant mining, validation, ranking, robustness (`src/invariants`) — 11C
3. Skill candidate → economics → promotion → library → lifecycle → composition (`src/skills`) — 11D
4. Transfer memory, scores, graph, transfer-aware ranking (`src/transfer`) — 11C-4
5. Capability representation, growth, intelligence, robustness (`src/capability`, `src/evaluation`) — 11E
6. Layered evaluation harness, baselines, ablations, reports (`src/evaluation/harness`) — 11E-4/5

Remaining for v0.1 (Phase 12):

7. Trace producer (`TraceLogger`, `TraceStore`, `run_trace_pipeline`)
8. Phase pipelines (`run_invariant_pipeline`, `run_skill_pipeline`)
9. Skill application (`ReuseEngine.apply`)
10. Single end-to-end entry point (`run_full_asft_pipeline`)
11. Figures + experiment runners (`plot_metric`, exp01–03, exp05)

## Version plan

| Version | Scope |
| --- | --- |
| v0.1 | Research prototype — synthetic tasks, IDT + SCT + CGM, paper evidence |
| v0.2 | Concept layer |
| v1.0 | ARC integration |

## Immediate next step

**Phase 12A — Trace capture** ([v0_1_readiness.md](v0_1_readiness.md#phase-12-build-order-unblocks-gates-in-this-sequence)):
implement `TraceLogger`, `TraceStore`, and `run_trace_pipeline` so tasks produce
persisted reasoning traces. Every other gate depends on it.
