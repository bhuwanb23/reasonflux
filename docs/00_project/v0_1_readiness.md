# ASFT v0.1 — Readiness Assessment (Phase 11F)

Honest go/no-go for the MVP success checklist. Backed by
[`configs/modules.yaml`](../../configs/modules.yaml) and
`tests/test_spec_claim_traceability.py`.

## Verdict

**Specification: complete. Evidence: not yet.**

The architecture, models, metrics, and evaluation layer are implemented and green
(~413 tests). What is missing is not design — it is the producer side: nothing yet
writes real reasoning traces, and no single command chains Phase A → F.

| Dimension | Status |
| --- | --- |
| Research / theory | complete |
| Architecture | complete |
| Metrics + failure models | complete |
| Engineering specification | complete (this phase) |
| Phase A trace capture | **not started** |
| End-to-end pipeline | **not started** |
| Experiments / paper evidence | **not started** |

## MVP gate status

| Gate | Criterion (scope) | Verdict | Evidence |
| --- | --- | --- | --- |
| FOUNDATION | Tasks produce persisted traces retrievable by family (end-to-end) | **BLOCKED** | `TraceLogger.log` and `run_trace_pipeline` are stubs |
| IDT | Reflection + rotation invariants discovered above the IS floor (synthetic) | PASS | `tests/test_trace_miner.py::test_end_to_end_reflection_and_rotation_emerge` |
| SCT | Reflection skill promoted, low-value candidate rejected, skill reused (synthetic) | PASS | `tests/test_skill_pipeline_e2e.py::test_reflection_promoted_verify_rejected` |
| TRANSFER | Positive ITS outranks higher-frequency zero-transfer invariant (synthetic) | PASS | `tests/test_transfer_aware_ranking.py::test_high_its_outranks_zero_transfer_despite_lower_frequency` |
| CGM | Positive / zero / negative CGR and IG computed (harness) | PASS | `tests/test_cgr_e2e.py::test_positive_zero_negative_cgr_and_ig` |
| EVALUATION | A growth run passes the hard gate while the flat baseline fails, from one ASFT entry point (end-to-end) | **BLOCKED** | `run_full_asft_pipeline` is a stub |

Read the PASS rows precisely: they demonstrate the **mechanism** on synthetic
inputs. They do not demonstrate that ASFT learns from real experience, because no
component currently produces experience.

## Blockers, in dependency order

| # | Blocker | File | Unblocks |
| --- | --- | --- | --- |
| 1 | No trace producer | `src/traces/logger.py`, `src/pipelines/trace_pipeline.py` | Phase A; everything downstream |
| 2 | No trace persistence | `src/traces/trace_store.py` | reproducible experience memory |
| 3 | No phase pipelines | `src/pipelines/invariant_pipeline.py`, `skill_pipeline.py` | Phases B and C as commands |
| 4 | No skill application | `src/transfer/reuse_engine.py` | Phase D measured reuse |
| 5 | No single end-to-end run | `src/pipelines/full_asft_pipeline.py` | EVALUATION gate; paper evidence |
| 6 | No figures | `src/utils/visualization.py` | paper figures |

## Phase 12 build order (unblocks gates in this sequence)

1. **12A — Trace capture** (`TraceLogger`, `run_trace_pipeline`, `TraceStore`).
   Exit: a task batch produces traces that survive a save/load round-trip.
2. **12B — Phase B/C pipelines** (`run_invariant_pipeline`, `run_skill_pipeline`).
   Exit: traces → ranked invariants → promoted skills in one call each.
3. **12C — Reuse + transfer** (`ReuseEngine.apply`).
   Exit: a promoted skill is retrieved on a second family and TS > 0 is recorded.
4. **12D — End-to-end** (`run_full_asft_pipeline`).
   Exit: EVALUATION gate turns PASS; `exp05_end_to_end` runnable.
5. **12E — Evidence** (`plot_metric`, enable exp01–03, exp05).
   Exit: paper tables and figures regenerate from a fresh checkout.

Each step is one PR-sized unit and flips exactly one gate.

## What must not be built

See `non_goals` in [`configs/modules.yaml`](../../configs/modules.yaml): LLM
planner, autonomous agent, meta-reasoner, world model, recursive
self-improvement, concept graph engine, neural skill embeddings, ARC leaderboard
optimizer, multi-agent architecture, AGI framework.

These are enforced by test, not convention.

## Related documents

- [implementation_blueprint.md](../02_design/implementation_blueprint.md) — module registry and contracts
- [claim_traceability.md](../04_paper/claim_traceability.md) — claim → evidence chain
- [roadmap.md](roadmap.md) — phase timeline
