# Phase 2A.8 — Representation Requirements for Phase 2B–2F (v2)

**Status:** design requirements only. No alternative representation, solver, budget, or ARC outcome was implemented or tested in Phase 2A.

## Objective

Make the representation hypothesis testable while keeping representation, search, support policy, and evaluator separable. A richer representation is not presumed better; the comparison must permit no coverage gain, a coverage gain without invariant candidates, and a coverage/invariant gain without accuracy improvement.

## Required conditions

### R0-H — Historical Phase 13G implementation (audit reference only)

- Frozen ten-program language listed in `primitive_inventory.csv`.
- Historical source/config mismatch is preserved: discovery used default ten; scored arms used three; full scans used ten.
- R0-H is not an eligible matched reference for new causal comparisons until all future stages share one prospective budget and execution logs prove parity. Do not relabel historical values as if they came from a corrected run.

### R0 — Corrected bounded reference representation

- Preserve the ten Phase 13G programs and their exact parameter semantics as an unchanged reference representation.
- Use one frozen configuration value for the program-trial budget across discovery/coverage, trace generation, transfer, and task scoring; record configured, runtime, and logged budget from the same source. Phase 2C must select and verify the numeric budget; Phase 2A does not choose it.
- Keep exact demonstration fit, first-fit/ambiguity handling, parameter inference, and candidate ordering separately logged. Any change to search order or parameterization is a search factor/version, not an unmarked representation change.

### R1 — Object-centric relational representation candidate

Build a separate, versioned representation from the same training demonstrations with explicitly documented:

1. **Segmentation policy:** color-aware 4-connected components (same-color connectivity) as the primary variant; background treatment fixed before development. Any 8-connected or alternate-background variant is a separate E2 development variant, not chosen after confirmatory outcomes.
2. **Object records:** stable within-task object IDs, color, occupied cells/mask, bounding box, height, width, area, centroid, shape signature, and border/contact flags.
3. **Relation graph:** documented directed/undirected predicates such as above/below/left/right, adjacency, overlap, same-color, containment, alignment, relative size, and distance. Each predicate has an operational definition and tests.
4. **Transformation constructors:** bounded object-level move, copy, delete, recolor, rotate/reflect, group/count, crop/compose, plus a finite rule grammar. No arbitrary code execution, unbounded recursion, or hidden external model.
5. **Traceability:** every generated candidate maps to parsed objects/relations and source demonstration evidence; failed parsing and ambiguous segmentation are explicit states.
6. **Search cap:** grammar size, candidate enumeration, compute/time, and stopping rule are capped and logged. Search policy is versioned separately from representation.

R1 is a comparator proposal, not a claim that object-centric parsing is the correct ARC representation. The exact relation predicates/grammar and numeric search budget must be completed and validated on development-only material before E3/confirmatory use.

### HCC — High-coverage reference condition

Create a controlled set of procedurally generated or manually specified tasks whose generating transformation is known and is expressible in R0 and/or R1. Use it only as a positive control for parser, coverage-only measurement, trace serialization, candidate generation, and evaluator plumbing. Keep it separate from public ARC task results; success on HCC is not ARC generalization evidence.

## Comparison design requirements

- Prefer a prospective **representation × search** design: R0 vs R1 crossed with a frozen standard search and a separately defined search/parameter-recovery condition, with identical tasks, demonstrations, test-label seals, resource caps, and evaluator. If a full factorial is infeasible, run paired common-support contrasts and clearly mark what is not identified.
- Hold support thresholds/mining rules constant when testing representation, or preregister a distinct support-policy factor. Do not tune the invariant threshold to whichever representation generates more candidates after seeing outcomes.
- Use the same development/confirmatory/replication split IDs for both representations where the task population is shared. Freeze annotations, code, config, and output hashes before opening confirmatory targets.
- Measure each stage separately: input validity; representable/demo-fit coverage; candidates attempted; full demo-consistent candidate set; selected candidate; trace validity; repeated candidate support; accepted invariants; skill eligibility; transfer applicability; capability units; exact task accuracy.
- A coverage-only runner may read training demonstrations but must not read test outputs. A separate sealed evaluator scores outputs after the relevant lock.
- Preserve unsupported/no-fit, ambiguous, parser-failure, search-budget-exhausted, no-support, and unavailable states; do not collapse them into one zero.

## Required outcome possibilities

The design must permit all of the following without changing rules:

- R1 does not improve coverage over R0.
- R1 improves demo-fit coverage but traces are not stable or do not recur.
- Coverage/traces improve but invariant candidates remain zero under frozen support rules—evidence against “representation caused everything.”
- Invariants appear but skills/transfer fail—failure localizes downstream.
- Coverage and mechanism activation improve but exact accuracy does not.
- R0 search improvements recover fits without changing the representation—search is implicated.
- An implementation or protocol mismatch makes a contrast unavailable/invalid.

## Minimum preregistration before any ARC confirmation

Name representation versions; segmentation/attribute/relation definitions; grammar and candidate hashes; one budget source of truth; search algorithm/order; task split and labels; coverage/trace/activation endpoints; independent unit; support rules; test-output access sequence; uncertainty/sample-size plan; alternative/high-coverage condition; failure-state definitions; and R1–R4 replication requirements. Phase 2A does not authorize that confirmation.