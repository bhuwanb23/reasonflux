# Phase 1G.2 — ARC Representation Requirements

## Purpose and non-assumption

Define a representation that can be audited for ARC tasks without assuming that adding primitives improves performance or validates ASFT. The representation is a versioned candidate language plus task/grid parser, search procedure, program semantics, trace format, and resource contract. Coverage is measured as empirical compatibility under that frozen system—not as truth, intelligence, accuracy, or proof that a task's latent rule was captured.

## Historical v1.0 limits

The Phase 13G DSL comprised ten fixed single-step programs: identity, horizontal/vertical reflection, rotations 90/180/270, transpose, anti-transpose, constant translation, and bijective recoloring. It did not operationalize counting, grouping, object detection/segmentation, relations, pattern completion, or general compositions. It assumed rectangular discrete grids/color domains, exact demonstration fit, fixed candidate enumeration, and a three-candidate scored-arm budget—though discovery actually defaulted to ten.

## Minimum auditable specification for any v1.1 representation

Every representation variant must freeze and publish:

1. Input grammar: grid shape, color symbols, task-pair schema, empty/unknown handling, and validation failures.
2. Operation semantics: typed preconditions/postconditions, parameter ranges, deterministic behavior, output shape/color rules, and composition/order semantics.
3. Search semantics: program grammar, enumeration/ranking, deduplication, candidate budget per task/arm, timeout/memory caps, stopping rule, and exact candidate-trial counter.
4. Trace schema: attempted operations, candidate identity, intermediate states, demo-fit status, rejection/failure code, resource use, and replay hash.
5. Coverage protocol: distinguish budgeted search from exhaustive/reference scans; report all attempted tasks, operator reachability, fit success, and denominator.
6. Provenance: source/config/version hashes, tests for every operation, and a configuration-to-runtime parity assertion.

## Required phenomenon coverage audit

For every proposed variant, list support/limitations for:

- objects, connected components, and segmentation;
- counting and cardinality;
- grouping/category rules;
- spatial and relational structure;
- repetition, symmetry, and patterns;
- composition/sequencing of operations;
- color/symbol remapping and shape/size changes;
- context-dependent rules and exceptions.

These are audit questions, not a mandatory checklist of primitives. A representation may use alternative abstractions if they have clear semantics, bounded resources, and testable coverage. Do not label unrepresented tasks “impossible”; classify them as not covered under the searched language/budget, with latent representability unknown unless independently established.

## Representation comparisons

Use the frozen historical 10-program adapter as a reference baseline and, for a direct representation-bottleneck test, at least one materially distinct, independently justified representation variant or a preregistered high-coverage reference condition. Do not make the contrast “few primitives versus many primitives” without semantic justification. Compare variants on the same task IDs and candidate/compute budget; report a separate exhaustive diagnostic scan only when preregistered and clearly excluded from scored-arm outcomes. Hold search algorithm and data constant where possible. Any conclusion that representation is not the primary bottleneck requires adequate budgeted coverage plus observable downstream opportunities; if no such regime exists, root cause remains unresolved.

## Coverage vs accuracy

`Demo-fit coverage` is the fraction of tasks for which the frozen search finds at least one program matching every allowed demonstration pair. It is computed without test-output gold. It is **not** exact test accuracy, semantic correctness, or proof of full task representability. Record coverage by representation variant, split, annotation category, and candidate budget; report exact/partial task accuracy separately.