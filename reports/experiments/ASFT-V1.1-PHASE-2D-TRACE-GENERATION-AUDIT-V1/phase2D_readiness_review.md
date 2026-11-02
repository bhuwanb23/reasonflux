# ASFT v1.1 Phase 2D — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2D`  
**Package:** `ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1`  
**Method:** retrospective Phase 13G trace validation plus analysis/reconstruction of saved Phase 2C test-output-blind search logs. No new ARC search, task score, test-output parsing, or accuracy evaluation.

## Executive decision

- **Phase 2D: PASS for trace taxonomy, lifecycle/yield/diversity/quality measurement, invariant-readiness audit, and operational failure localization.**
- **Phase 2 overall remains BLOCKED.** Phase 2D does not authorize confirmatory tests or establish ARC performance, capability, or intelligence.
- **Headline:** Phase 13G emitted 600 discovery trace records but only 3 successful traces (0.50%). Retrospective structural validation of the saved records passes 600/600, while the original generation-time `trace_schema_valid` flag was hard-coded. The actual miner received three success traces, created 30 fragments, then zero raw patterns, structures, or candidates. Its behavior on adequate, diverse inputs remains untested.
- In Phase 2C conditions, 1,000 valid trace records per condition yield only 2/5/10/10 successful traces across S1–S4. Discovery inputs to TraceMiner are 1/2/3/3, with maximum support one and zero invariant candidates. **Invariant readiness: I3 — Not Ready.**
- **Localization:** F6 mixed observed bottlenecks; F7 primary causal attribution unresolved.
- Accuracy and generalization beyond demonstrations were not measured.

## Research questions

| Question | Answer | Boundary |
|---|---|---|
| R2D-1 — How many traces generated? | 600 historical; 1,000 per Phase 2C condition. | Stability replays create search calls, not extra traces. Conditions reuse the same task IDs. |
| R2D-2 — How many valid? | 600 saved historical records pass retrospective structural validation; all 1,000 per new condition pass independent audit. | Historical runtime validity was not independently checked at generation time. |
| R2D-3 — How many successful? | Historical 3/600; Phase 2C-derived 2/1,000, 5/1,000, 10/1,000, 10/1,000. | Exact training-demo fit, not test accuracy. |
| R2D-4 — Enough traces for invariants? | **No. I3 Not Ready.** | Only 1–3 successful discovery traces; each signature support1, below support5. |
| R2D-5 — Main failure source? | Mixed measured attrition at successful yield and recurrence/support. | Representation versus search root cause and miner behavior on positive controls remain unresolved. |

## Readiness gates

| Gate | Status | Evidence |
|---|---|---|
| T1 — Trace taxonomy frozen | **PASS** | `trace_taxonomy.md` defines T1–T6 as non-exclusive flags and separates no-fit from partial. |
| T2 — Lifecycle measurable | **PASS** | `trace_lifecycle_report.md` and CSV show counts, survival, attrition, and blocked conditional stages. |
| T3 — Yield measurable | **PASS** | Saved Phase 2C conditions provide candidate slots, attempts, valid/successful traces, and rates. |
| T4 — Diversity measurable | **PASS with semantic limit** | Solution signatures, structural buckets, operation labels, and templates reported; structural buckets are not semantic ARC families. |
| T5 — Quality measurable | **PASS for demo-level metrics** | Fit, consistency, support, reuse potential measured without invariant/skill scores; generality is explicitly unavailable. |
| T6 — Invariant readiness defined | **PASS** | Actual TraceMiner replay, support counts, fragment/pattern/candidate stages, and I1–I3 status recorded. |
| T7 — Failure localization operational | **PASS for observed stage; causal attribution unresolved** | First large attrition is valid→successful; support/diversity also below threshold; no automatic miner blame. |

## Final decision

**Phase 2D PASS for the trace-generation audit.** The evidence answers the central question: the miner received a very small, low-support set of successful discovery traces; zero invariant candidates therefore cannot be interpreted as a test of miner performance on adequate trace input. Search cap increases improve trace yield, but fullscan still supplies only three successful discovery traces with singleton support. Phase 2 overall stays **BLOCKED**; no confirmatory ARC or ASFT efficacy claim is made.