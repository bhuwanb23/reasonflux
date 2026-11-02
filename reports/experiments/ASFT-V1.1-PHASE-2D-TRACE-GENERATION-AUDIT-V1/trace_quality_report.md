# Phase 2D.6 — Trace Quality Benchmark

Quality is assessed without invariant strength, skill scores, capability scores, test labels, or accuracy.

| Metric | Operational result | Boundary |
|---|---|---|
| **Q1 Demonstration fit** | 2/1,000 S1; 5/1,000 S2; 10/1,000 S3/S4. | Exact equality on all training demonstrations only. |
| **Q2 Consistency** | 100% of successful selected traces independently replay exactly across their training demonstrations. | No selected program exists for no-fit traces; consistency there is not estimable, not zero. |
| **Q3 Generality** | `NOT_MEASURED_TEST_OUTPUT_BLIND`. | Applying to held-out/test inputs or measuring unseen-task generalization was outside this audit. |
| **Q4 Support** | Maximum discovery support for a program operation or exact program/context signature is 1 in every condition; threshold is 5. | Support is distinct discovery task IDs, not number of candidate trials or trace records. |
| **Q5 Reuse potential** | One program label (`recolor_bijection`) appears in both discovery and transfer in fullscan; exact context recurrence is 0. | Potential only; not transfer accuracy, a trained skill, or observed successful reuse. |

All current no-fit records are structurally valid search-attempt traces, but they do not contain a partial solution. The taxonomy's T3 “Partial Trace” is not emitted by this builder. Historical Phase 13G's 600 serialized traces pass retrospective structural validation, but its generation-time `trace_schema_valid` field was hard-coded; validation quality at generation time is therefore unknown.

No metric above uses invariant/skill scores. No ARC test output was read, and no accuracy or causal mechanism outcome is claimed.