# Phase 2F.3 — Representation Taxonomy

Each comparison names the exact layer changed. A taxonomy label is not a performance claim. Several alternatives compose layers; those contrasts cannot identify a single component unless paired with the incremental contrasts below.

| Type | Definition | Phase 2F registry mapping | Contrast needed |
|---|---|---|---|
| **T1 Primitive Expansion** | Adds finite, explicitly specified whole-grid operators/parameterizations while retaining a raster state and no object graph. | **R2** | R1 vs R2, same trial/resource cap. |
| **T2 Object-Centric** | Parses grids into stable object records and applies selectors/actions to objects; no relation predicates are used by the rule grammar. | **R3** | R1 vs R3 measures the bundled parser+object-action alternative; object extraction cost/failure is separately logged. |
| **T3 Relation-Centric** | Uses explicit object nodes and a finite typed relation graph; rules condition actions on a relation predicate. | **R4** | R3 vs R4 isolates the incremental relation layer, because R4 reuses R3's object parser. |
| **T4 Hierarchical** | Represents cells/components, objects, and groups at bounded levels with group attributes/actions. | **R5** | R3 vs R5 isolates the hierarchy/group layer as specified. |
| **T5 Compositional** | Represents a bounded sequence/AST of existing primitives as one complete candidate program. | **R6** | R1 vs R6 isolates bounded composition over the same atomic whole-grid inventory. |
| **T6 Hybrid** | Combines object, relation, hierarchy, and bounded composition. | **R7** | Compare only after component contrasts; any gain is multi-factor and cannot be attributed to one layer. |

## Reference conditions and naming crosswalk

- **R0 (Phase 2F):** exact historical Phase 13G ARC representation/execution record; audit reference only. It retains the discovery budget mismatch and is not an eligible matched comparator.
- **R1 (Phase 2F):** current ten-program bounded production representation under Phase 2C's corrected, test-output-blind S4 protocol. R0 and R1 share the same solution primitives; R0 vs R1 is **not** a representation contrast.
- **HCC:** a high-coverage known-rule plumbing control, not an ARC representation or ARC evidence.
- Phase 2A used `R1` as a short name for its object-centric relational proposal. Phase 2F decomposes that proposal into **R3** (object-centric base) plus **R4** (incremental relation extension). Phase 2A's corrected bounded reference maps to Phase 2F **R1**. Use only Phase 2F IDs in new logs.

## Orthogonal implementation dimensions

Always record: primitive/operator inventory; input and scene/object schema; segmentation/background assumptions; relation predicates; hierarchy/group policy; composition grammar; parameter inference; candidate enumeration order; search depth; per-task trial and compute budgets; trace schema; and downstream adapters. A difference in any of these must be named. A general helper present in the codebase is not a representation primitive unless the registered search can propose and execute it.