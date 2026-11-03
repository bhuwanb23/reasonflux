# R3 Implementation Contract — Phase 2F Object-Centric Alternative

## Status and boundary

This document carries forward the **specified** Phase 2F R3 condition; R3 remains not implemented. It is not a new representation proposal. Code must implement the locked Phase 2F grammar below and must not add relations, hierarchy, composition, or hidden operations. Items in `ambiguity_register.csv` require an approved, versioned specification addendum before implementation where the source spec is underspecified.

## Frozen representation core

- Input: rectangular integer-color grid; background is fixed at color `0`.
- Objects: same-color **4-connected** foreground components. Eight-connectivity and alternate background conventions are out of scope.
- Stable object IDs: canonical sort by `(top, left, color, mask lexicographic)` after parsing.
- Stored object fields: color; occupied-cell mask; bounding box; height/width; area; rational centroid; shape signature; border/contact flags.
- Relations: none. No relation graph, relational predicates, group nodes, or hierarchy.
- Candidate: exactly one object selector plus exactly one object action and its permitted finite parameters. No composition or conditionals.

## Selector vocabulary

The Phase 2F registry allows only:

1. exact color;
2. area rank among current objects;
3. exact normalized bounding-box aspect/shape signature;
4. border-contact boolean.

The selection cardinality, tie handling, normalization/canonicalization of shape, and cross-demonstration correspondence must be resolved in the approved addendum. Do not assume a stable object ID across different demonstration grids.

## Action vocabulary and bounds

- `move_selected_object`: integer `dy, dx` in `[-2, 2]`;
- `copy_selected_object`;
- `delete_selected_object`;
- `recolor_selected_object`: target color in `0..9`;
- `rotate_or_reflect_selected_object`: quarter-turn `k∈{1,2,3}` or horizontal/vertical reflection about the object bounding-box axes;
- `crop_selected_bbox`.

The Phase 2F spec requires invalid collision/out-of-grid candidates to be rejected and all parameters to be fit/verified from training demonstrations only. Exact raster semantics—especially movement occupancy, copy collisions, bounding-box rotation/reflection on even dimensions, recolor/background interactions, and crop output shape—must be resolved and frozen in the addendum, not selected by whichever semantics yield more fits.

## Search and data contract

- Candidate order and IDs are deterministic and canonical; first exact fit across all available training demonstrations wins.
- Evaluate at most ten complete candidate hypotheses/task, under the common Phase 2F time/memory budgets. A parameter assignment is part of the candidate hypothesis.
- Search may read training input/output demonstration pairs only. No test output is read, parsed, cached, or used to infer parameters.
- Store the full trial ledger separately from the one-per-task/condition trace.
- Distinguish invalid input, ambiguous/parser failure, invalid action, no-fit within registered language/budget, and resource exhaustion.
- “No fit” is not proof of semantic unrepresentability.

## Required tests before freezing

1. Parser behavior for empty/background-only grids, non-rectangular input, color boundaries, diagonal contact, same-color orthogonal contact, and deterministic IDs under repeated runs.
2. Object fields and canonical shape signatures have exact hand-checked fixtures after the relevant ambiguity entries are resolved.
3. Each selector's cardinality, tie rule, and cross-example parameterization are deterministic and unit-tested.
4. Each action has hand-checked exact grid outputs; invalid collision, out-of-grid, and degenerate cases have stable rejection codes.
5. Candidate ordering and IDs are stable across processes; ten-trial cap cannot be exceeded.
6. A forbidden test-output sentinel proves the parser/runner cannot access test outputs.
7. R3 runner output conforms to the shared semantic trace schema and remains distinct from the separate search ledger.
8. Grammar version and implementation SHA-256 are included in every run record.
