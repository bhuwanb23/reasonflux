# Phase 2E.2 — Invariant Taxonomy

This audit uses the requested I1–I6 taxonomy. The categories describe the **evidence required**; a repeated operation string alone does not qualify as an ARC invariant.

| ID | Category | Evidence required | Current trace evidence/status |
|---|---|---|---|
| **I1 Exact Structural Invariant** | Same grounded operation/structure signature recurs across distinct successful tasks, with preserved input/output meaning. | Exact operation n-grams recur, but observed repeats are trace instrumentation (`validate_grid_schema`, `enumerate_candidate_programs`, `verify_demonstrations`). **Observed procedural recurrence; no meaningful ARC invariant established.** |
| **I2 Transform Invariant** | A transformation relation is preserved under independently varied inputs or demonstrations, not merely the same `apply_*` label. | No transformation label recurs among the three Phase 13G discovery successes; transformation semantics beyond demo fit are unavailable. |
| **I3 Object Invariant** | Object identity/attributes and their persistence or transformation are represented and recur across tasks. | Trace steps contain no grounded object state/identity. **Not represented; not measurable.** |
| **I4 Relational Invariant** | Explicit relation among objects/parts is encoded and recurs. | No object relations are recorded. **Not represented; not measurable.** |
| **I5 Compositional Invariant** | A meaningful sequence of independently grounded subrules composes consistently across tasks. | A common two-step control-flow prefix recurs, but it describes validator/search scaffolding, not grounded subrules. **Pattern detected; semantic composition unestablished.** |
| **I6 Cross-Task Invariant** | A grounded invariant recurs across distinct tasks and independently annotated semantic task families. | Operation signatures span multiple task IDs, but family labels are transformation/program labels and thus outcome-derived. **Cross-task operation recurrence measured; independent cross-family invariant unavailable.** |

## Reporting rule

Report raw operation-pattern recurrence as `observed pattern`, not `invariant`. To call a pattern an invariant requires grounded semantics, recurrence across distinct task IDs, stability/consistency, independent family support, and separately measured validation/utility. A miner's enum label (`operational`, `procedural`, `structural`, `transfer`) is implementation taxonomy—not independent evidence for I1–I6.