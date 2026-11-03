# Common Semantic Trace Adapter Contract — Phase 2I-A WP2

## Status

WP2 implementation and synthetic TraceMiner parity tests pass, now using the frozen WP4 runtime config; the reflection aliases were corrected to match cell effects and regression-tested. The versioned code contract is `src/traces/semantic_adapter.py`; the schema identifier is `ASFT-2I-SEMANTIC-TRACE-V1`. This contract preserves operation vocabulary for the unchanged Phase 2E miner while keeping arm/candidate provenance outside the mining projection. No ARC traces have been generated.

## Shared four-event trace

For a **successful first exact fit on all training demonstrations only**, each arm emits the same ordered four-step schema:

1. `validate_input`
2. `construct_representation`
3. `apply_<operation_family>` — candidate-specific semantic action
4. `verify_demonstrations`

The trace has at most four steps. No exact-fit candidate means no primary reasoning trace; parser/search failures and the full trial ledger remain separate. The trace `outcome.result` is `null`; no grid, expected output, or candidate parameters are copied into it.

## Frozen operation mapping implemented

| R1 registered operation | Common action family | Scope |
|---|---|---|
| `identity` | `identity` | grid |
| `reflect_horizontal` (flips left/right) | `flip_left_right` | grid |
| `reflect_vertical` (flips top/bottom) | `flip_top_bottom` | grid |
| `rotate_90/180/270` | corresponding `rotate_90/180/270` | grid |
| `transpose` | `transpose` | grid |
| `anti_transpose` | `anti_transpose` | grid |
| `translate_constant` | `translate` | grid |
| `recolor_bijection` | `recolor` | grid |

| R3 registered operation | Common action family | Scope |
|---|---|---|
| `move(dy,dx)` | `translate` | object |
| `copy` | `copy` | object |
| `delete` | `delete` | object |
| `recolor(color)` | `recolor` | object |
| `rotate(k)` | `rotate_90/180/270` for k=1/2/3 | object |
| reflection about horizontal axis (flips top/bottom) | `flip_top_bottom` | object |
| reflection about vertical axis (flips left/right) | `flip_left_right` | object |
| `crop_bbox` | `crop` | object |

Unknown operations fail closed; raw operator strings are never passed through to the miner. Candidate parameters (coordinates, colors, IDs) are omitted from mined operation tokens. Reflection aliases are defined by the actual cell effect, not by similarly named axes: R1 `reflect_horizontal` reverses columns and pairs with R3 reflection about the vertical axis; R1 `reflect_vertical` reverses rows and pairs with R3 reflection about the horizontal axis. Tests explicitly assert both cross-axis effect pairs and reject the same-word/wrong-effect pairing. A zero-offset R3 `move` is projected as the canonical `identity` effect; nonzero offsets remain `translate`. The shared action family is retained even when the operations are only partially equivalent (for example, global versus selected-object recoloring); scope remains a semantic field rather than an arm label.

## Scope, provenance, and leakage boundary

- The raw `ReasoningStep.inputs` for the candidate action retain only the common semantic field `target_scope` (`grid` or `object`). The current frozen normalizer mines `step.operation` strings, not step inputs; scope therefore remains auditable in the raw trace without becoming an arm-specific mined token.
- The raw trace metadata contains only the schema version until WP3 supplies an independent family. No representation ID, solver program, candidate ID, grammar/code hash, parameters, task-family label, or test/output data is placed in trace operations or metadata.
- `TraceProvenance` is a separate sidecar holding task/arm/candidate/hash/trial lineage. It is never passed to `TraceMiner`.
- `mining_projection()` requires an explicit independently annotated family label and emits only that label plus schema version in metadata. It does not infer family from task ID or representation.
- `TraceOutcome.result` is null. HCC, when built, uses its own isolated synthetic namespace and cannot be projected into ARC data.

## Technical decision and stop condition

The common operation tokens preserve the action family; target scope is retained in the common event schema/raw trace but is intentionally not mined because the frozen miner mines operation strings only. This avoids injecting an R1/R3 arm token while preserving the scope distinction for audit. If owner/reviewer judgment is that scope must enter the mined signature for the original RQ1 construct, do not alter the frozen miner or append scope post hoc: stop and request a protocol decision.

## WP2 validation

Automated tests cover R1/R3 equivalent-family pairs, effect-based reflection parity, zero-offset identity, scope retention, four-step cap, independent trace validation, no raw parameter/output leakage, separate provenance, required external family projection, fail-closed unknown operations, and identical normalized operations/pattern/candidate results through the same `TraceMiner` using the frozen WP4 runtime configuration on synthetic paired traces. This parity test is not a positive-yield criterion; complete four-event traces can be overaggregated by common control events under the approved `min_core_length=1` setting, producing no candidates in that test fixture. WP5 therefore uses explicitly oracle-selected one-action synthetic miner fixtures to verify candidate-stage plumbing, not to claim end-to-end production integration. Synthetic family labels are test fixtures only; ARC-family maps, actual search coverage, and whole-run artifact allowlists remain open gates.
