# Phase 2I-A R3 Grammar Addendum v1 — Frozen

**Status:** OWNER APPROVED; FROZEN FOR WP1 IMPLEMENTATION  
**Approval:** User approval recorded 2026-11-02 (Asia/Calcutta).  
**Purpose:** close R3 grammar ambiguities before WP1 code. This freezes specification choices only; it does not authorize an ARC candidate-production run.  
**Source contract:** Phase 2F registry R3. This addendum supplies deterministic interpretations only where its finite grammar was underspecified. The R3 implementation and grammar/code hashes must be recorded after WP1 tests pass.

## 1. Object parser and shape signature

1. Input grids must be nonempty rectangular integer matrices. A background-only grid is valid and parses to an empty object list; it is not a parser error.
2. Foreground objects remain same-color 4-connected components with background color 0, exactly as Phase 2F specifies.
3. Each object's mask is stored in its tight bounding box. Define its canonical shape signature as `(height, width, row-major bit string)` where `1` marks occupied cells. This removes absolute position and color only; it is orientation-sensitive and does not quotient by rotations or reflections. Thus aspect ratio and orientation remain part of the exact signature.
4. Stable object IDs retain the specified ordering `(top, left, color, mask lexicographic)`. IDs are local to one grid/demo and are never matched across demonstrations.

## 2. Selector cardinality and ties

A valid candidate must select exactly one object in every training input grid, independently by the same frozen selector and parameters. Zero matches or more than one match makes that candidate invalid for that demonstration; the solver may not break ties using object ID, position, output, or a hidden rule.

- `exact_color(c)`: foreground objects of color `c`; valid only when exactly one object matches.
- `area_rank(k)`: rank **distinct object areas** descending (`k=1` is the largest distinct area); valid only when exactly one object has the selected ranked area. Tied objects at that rank are ambiguous/invalid.
- `bbox_shape(signature)`: exact canonical signature match; valid only when exactly one object matches.
- `border_contact(value)`: object touching any grid edge iff `value=true`; valid only when exactly one object has the requested value.

Selector parameters are fixed across demonstrations; selected object IDs may differ between demos. The candidate is rejected if its selector is ambiguous in any demonstration.

## 3. Action raster semantics

All actions operate on the uniquely selected object. Unless an action is `crop`, the output grid dimensions are unchanged. `foreground occupancy` means any nonzero cell. If an action relocates or transforms an object, first remove the selected object's source cells, then place the result; overlap with any other foreground cell is invalid. Any out-of-grid result is invalid. Invalid hypotheses are logged with stable reason codes and do not count as fits.

- `move(dy,dx)`: translate every occupied cell by one shared integer pair, each in `[-2,2]`; vacated cells become background 0.
- `copy(dy,dx)`: preserve the source and add an identical same-color mask at one shared offset, each in `[-2,2]`. Any overlap with any pre-existing foreground cell—including the source object—invalidates the copy. Offset `(0,0)` therefore has a stable collision rejection. **This reuses the move offset domain because the R3 registry lists copy but gives no copy parameter range.**
- `delete`: set the selected cells to 0.
- `recolor(c)`: set all selected cells to one shared target color `c∈{0,…,9}`; `c=0` is permitted by the registered range and therefore erases those cells.
- `rotate(k)`: clockwise quarter turns, `k∈{1,2,3}`, using local mask coordinates; the transformed bounding box is anchored at the selected object's original top-left. For a local cell `(r,col)` in an `h×w` mask, 90° maps to `(col,h−1−r)`, 180° to `(h−1−r,w−1−col)`, and 270° to `(w−1−col,r)`.
- `reflect_horizontal_axis`: map `(r,col)` to `(h−1−r,col)` (flip top/bottom).
- `reflect_vertical_axis`: map `(r,col)` to `(r,w−1−col)` (flip left/right).
- `crop_bbox`: return the original grid slice in the selected object's tight bounding box, preserving all colors/background cells inside that rectangle; no extra padding.

The action parameter(s) are shared across all demonstrations. The same serialized selector+action hypothesis must exactly reproduce every training output pair to count as a fit. No example-specific parameter fitting is permitted.

## 4. Canonical enumeration and candidate IDs

To make the ten-trial cutoff reproducible:

- Candidate AST serialization is canonical JSON with sorted keys, compact separators, integer parameters, and normalized selector/action names; candidate ID is `R3-` plus the full SHA-256 digest of that serialization.
- Parameter domains are formed without training outputs: colors are 1–9 for color selectors; shapes are unique parsed shapes in training **input** grids; area ranks are `1..max_objects_in_any_training_input`; border values are `[false,true]`; action parameters use the frozen ranges above.
- Enumerate the finite selector × action × parameter product in ascending canonical-JSON byte order. Evaluate only the first ten hypotheses, in that order; do not reorder by fit, predicted output, task family, or ARC yield. Log every evaluated candidate ID and stop reason. A later exact fit beyond trial ten is recorded as budget-limited, not found.

This order is reproducible but consequential under the ten-trial cap; it must be approved before code and never revised after seeing yield.

## 5. Parser/status distinctions

- Invalid input shape/type → `INVALID_INPUT`.
- Valid background-only grid → `PARSED_NO_OBJECTS` (search has no applicable selector; not parser failure).
- Any selector ambiguity/no match → candidate-level `SELECTOR_NOT_UNIQUE` or `SELECTOR_NO_MATCH`.
- Action collision/out-of-bounds → candidate-level stable invalid reason.
- No exact fit among the first ten → `NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET`.
- Time/memory cap → separate resource-limit status.

No failure status may be collapsed into a generic success trace or a semantic impossibility claim.

## 6. Approval record and remaining boundaries

The owner approved the five decision groups above as written on **2026-11-02**. This document is the frozen, versioned grammar addendum for WP1. Its SHA-256 is recorded in the Phase 2I-A package manifest/provenance after finalization; implementation code/grammar hashes remain pending until WP1 validation.

This addendum closes R3 grammar decisions only. It does not resolve the separate WP2 semantic trace mapping, WP3 family ontology/labels, WP4 runtime policy/identity, or later HCC/runner implementation. The Phase 2I ARC candidate-production run remains unauthorized.
