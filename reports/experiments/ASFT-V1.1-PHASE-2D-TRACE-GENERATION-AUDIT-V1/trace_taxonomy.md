# Phase 2D.2 — Trace Taxonomy

The six labels below are **non-exclusive flags**, not six mutually exclusive bins. T2 is structural validity; T4 is exact demonstration success; T5 and T6 are downstream support/reuse annotations. A trace can be T2+T4, and possibly T5/T6. Report both primary status and overlay flags.

| ID | Frozen class | Operational rule | What it does not mean |
|---|---|---|---|
| **T1 Invalid Trace** | Serialized/executed record fails structural validator, required fields, task identity, or outcome/operation consistency. | Not equivalent to task no-fit or a failed candidate. |
| **T2 Valid Trace** | Trace record parses and satisfies the independent structural/identity validator; input grid schema is valid. | Not success, correctness on unseen inputs, or useful reasoning. |
| **T3 Partial Trace** | Explicit trace records a candidate/operation that executed but did not complete the full demonstration rule. | A failed candidate search not represented in the trace is not a partial trace. Current builder does not emit this class. |
| **T4 Successful Trace** | Selected program exactly reproduces every training demonstration, independently replayed. | Not held-out accuracy, transfer success, or proof of the inferred rule. |
| **T5 High-Support Trace** | Successful discovery trace whose program-operation signature appears in at least five distinct discovery task IDs, matching the frozen Phase 13G support floor. | Not an invariant candidate; consistency, family breadth, and miner policy still apply. |
| **T6 Transfer-Relevant Trace** | Program operation appears among successful discovery and transfer traces; report exact program+parameter-context overlap separately. | Not transfer accuracy, skill promotion, or demonstrated reuse. |

## Phase 2D classification convention

For the Phase 2C-derived audit, every task/condition has a primary trace: no-fit traces are T2 only; exact-fit traces are T2+T4. T1=0 after independent structural validation; T3=0 because the existing trace builder does not record partial candidates. T5 uses **discovery support only**. T6 uses program-level overlap as a hypothesis flag, while exact program/context overlap is reported separately.

For Phase 13G, `trace_schema_valid=True` in the original runner was hard-coded. Phase 2D independently validates the saved serialized records retrospectively and labels this as post hoc schema audit—not generation-time validation.