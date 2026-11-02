# Phase 2A.5 — Missing Concept Audit

## Scope and rule

This audit identifies concepts absent from, auxiliary-only in, or only partially represented by the **Phase 13G bounded ARC solution/search path**. It does not assert that any absent concept is required by a particular ARC task or estimate how often ARC tasks use it. Such prevalence claims would require independent semantic annotation and are not supported by the saved Phase 13G taxonomy.

Evidence standard: a concept is marked absent from the solution DSL only when it is missing from the frozen ten-program `PROGRAMS` list and corresponding `apply_program`/candidate logic. A related repository helper counts only if Phase 13G actually invokes it as a candidate rule; generic helper availability is reported separately.

## Findings by concept

| Concept | Phase 13G status | Direct evidence | Consequence / boundary |
|---|---|---|---|
| **Object detection / segmentation** | Not a solution primitive | No object IDs, masks, or bounding boxes in candidate records/programs. `count_objects` is used as a scalar feature. | No object-level selection or transform. Do not infer that raw grid cells were semantically segmented. |
| **Object identity / permanence** | Not operationalized | Tasks are static I/O demonstrations; no cross-frame object tracking IDs or state-transition model. | Cannot express persistent identity across transformation steps; ARC prevalence unknown. |
| **Object attributes** | Partially available as grid statistics | Raw colors, dimensions, density, and 4-connected component count exist as global/mean features. | No per-object color/size/shape/position attribute record or conditional object rule. |
| **Counting** | Not an output rule | `count_objects` returns 4-connected non-background components; `group_by_color` returns color pixel counts. Neither is in `PROGRAMS`; count helper is auxiliary to memory features. | The system can compute a coarse statistic but cannot generate an output according to a count relation. No task prevalence estimate. |
| **Grouping** | Not an output rule | Generic `group_by_color` helper exists in `src/solver/grid.py`, but Phase 13G does not invoke or enumerate it. | Presence in a library is not phase-level solver expressivity; no group objects or group transforms. |
| **Spatial relations** | Not explicit | Grid coordinates preserve low-level position; `structural_bucket` reports same/changed shape, palette, and component count. No above/below/adjacent/contained predicates or graph. | Pixel geometry may incidentally encode a relation but the program search cannot state or condition on symbolic relations. |
| **Pattern representation/completion** | Not operationalized | No repetition detector or completion/fill program in the ten candidates. | No evidence that the miner tested a representative pattern-completion language. |
| **Composition / nesting** | Not general | `solve_task` selects a single atomic program. `rotate_180` and `rotate_270` are fixed atoms implemented using repeated rotations. | There is no general searchable sequence, nested expression, branching, or reusable subprogram composition. |
| **Crop / expand / resize** | Absent as explicit operators | No crop/pad/scale program; only fixed rotations/transposes can alter dimensions. | Shape-changing tasks beyond these fixed transforms may fail; no prevalence estimate. |
| **Conditional or relational rules** | Absent | No branching/if-then program grammar or binding variables. | Candidate library cannot express “if object has property X, do Y” or relationally conditioned operations. |
| **Color roles / non-bijective recoloring** | Partially represented | One global bijective map is inferred across all cells. | Cannot merge colors, recolor selected objects, infer semantic color roles, or combine recoloring with geometry in one program. |
| **Translation parameter search** | Partial and heuristic | Constant shift inferred by bounding-box displacement, then rare-color anchor offsets; at most 16 source anchors sampled. | No unrestricted object motion, path search, wrapping, or varying shifts; no-fit may be a parameter-search false negative. |
| **Symmetry** | Transform partly present; detection is diagnostic only | Whole-grid horizontal/vertical reflection programs; a separate `symmetry_demo_property` Boolean flags mirror-symmetric grids. | Property flag is not used by candidate search, does not establish a symmetry rule, and does not measure semantic symmetry-task prevalence. |
| **Hierarchy / part-whole structure** | Absent | No nested objects, component membership, or parent-child representation in `Grid` or the Phase 13G DSL. | Cannot express hierarchical composition; no claim about ARC task requirements. |
| **Recursion / iterative rule application** | Absent as a language feature | Only three fixed rotation atoms; no loops or recursive grammar. | Repetition within a fixed operation is not general recursion. |
| **Task-family semantics** | Unknown / not available | Phase 13G taxonomy derives labels from which bounded program fit; ARC has no authoritative family labels in this package. | `unsupported_v1` cannot be treated as a semantic class; no semantic coverage census is justified. |

## What the missing-concept list does—and does not—mean

It documents the implementation's representational envelope, not the complete ontology of ARC and not a list of proven causes of every failure. Some absent concepts may not be needed for many sampled tasks. Some apparent gaps may be addressable by a richer parameterization of existing transforms. Conversely, adding an object or relation helper will not automatically make the corresponding phenomenon expressible as a task-solving rule.

The next comparison must distinguish at least three layers:

1. **Perceptual/structural extraction:** what objects, attributes, and relations are represented?
2. **Rule/program language:** what transformations and compositions can be stated?
3. **Search/selection:** can the implemented search find a fitting candidate within a validated budget?

A coverage change between representations is interpretable only if these layers, budgets, and test-label access are audited separately.