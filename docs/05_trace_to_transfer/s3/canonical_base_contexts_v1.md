# Canonical Base Contexts v1

**Status:** frozen context-construction specification for count-only manifest materialization.  
**Scope:** observable state/action construction only. This file assigns no success/no-effect labels, predictions, scores, or Claim N status.

## 1. Shared conventions

- Use the `UnlockState` / `UnlockObject` / `UnlockAction` fields in `src/t2t_s3/world.py`; states contain only visible object records, coordinates, action bindings, and `path_clear`.
- `context_id` is metadata only, is not a predictor input, and never participates in replay matching.
- No `Effect`, `observed_effect`, `expected_effect`, prediction, score, or outcome field is created in any manifest.
- Source contexts are exactly the seven source contrasts below. Their feature vectors are deterministic input features only; source effect labels are not generated in this preparation step.
- Held-out primary templates use replicate indices `r = 0, 1, 2`. Set `x0 = 100*r`, `y0 = -50*r`; the agent is at `(x0,y0)`. These offsets create distinct observable contexts without changing adjacency relations.
- Every primary held-out template has four objects, in this order before any surface recipe: key `K-r`, targets `T1-r` and `T2-r`, distractor `D-r`. All IDs are unique. `K-r.opens_target_id` is a visible ID reference. The action uses a visible key/target ID except in the explicit wrong-role and absent-key contrasts.
- For adjacent-target templates, target slots are `(x0+1,y0)` and `(x0,y0+1)`; key slot is `(x0+4,y0)`; distractor slot is `(x0+5,y0)`. For nonadjacent-target templates, target slots are `(x0+3,y0)` and `(x0,y0+3)`; key slot is `(x0+6,y0)`; distractor slot is `(x0,y0+6)`. The two target slots are always distinct and neither overlaps the agent, key, or distractor.
- Colors/shapes are ordinary visible strings. Use `blue/key`, `red/box`, `gold/box`, and `green/mark` for key, T1, T2, and distractor respectively, except in `NEG-WRONG-ROLE`, where the distractor deliberately shares the key's `blue/key` appearance. No hidden fields are used.

## 2. Exact source contexts

Each row uses the stated state/action and has exactly one unique context ID `SRC-{contrast_id}` and trace ID `TRACE-SRC-{contrast_id}`. All source states are complete, all references resolve, and `path_clear` is a Boolean. The six-predicate vector is computed from the serialized state/action and must equal the listed vector. Object order is the order shown; omitted objects are absent.

| Contrast ID | State/action construction | Required feature vector (ordered: key-is-key, target-is-target, target-closed, adjacent, path-clear, relation) |
|---|---|---|
| `ALL_TRUE` | Agent `(0,0)`, path `true`; `K1: KEY, opens=T1`; `T1: TARGET, closed=true, (1,0)`; action `(K1,T1)`. | `true,true,true,true,true,true` |
| `ONLY_FALSE_KEY_IS_KEY` | Agent `(0,0)`, path `true`; `K1: KEY, opens=T1`; `T1: TARGET, closed=true, (1,0)`; `D1: DISTRACTOR, opens=T1, closed=null, (0,1)`; action `(D1,T1)`. | `false,true,true,true,true,true` |
| `ONLY_FALSE_TARGET_IS_TARGET` | Agent `(0,0)`, path `true`; `K1: KEY, opens=D1`; `D1: DISTRACTOR, closed=true, (1,0)`; `T1: TARGET, closed=true, (0,1)`; action `(K1,D1)`. | `true,false,true,true,true,true` |
| `ONLY_FALSE_TARGET_CLOSED` | Agent `(0,0)`, path `true`; `K1: KEY, opens=T1`; `T1: TARGET, closed=false, (1,0)`; action `(K1,T1)`. | `true,true,false,true,true,true` |
| `ONLY_FALSE_AGENT_ADJACENT` | Agent `(0,0)`, path `true`; `K1: KEY, opens=T1`; `T1: TARGET, closed=true, (2,0)`; action `(K1,T1)`. | `true,true,true,false,true,true` |
| `ONLY_FALSE_PATH_CLEAR` | Agent `(0,0)`, path `false`; `K1: KEY, opens=T1`; `T1: TARGET, closed=true, (1,0)`; action `(K1,T1)`. | `true,true,true,true,false,true` |
| `ONLY_FALSE_KEY_UNLOCKS_SELECTED_TARGET` | Agent `(0,0)`, path `true`; `K1: KEY, opens=T2`; `T1: TARGET, closed=true, (1,0)`; `T2: TARGET, closed=true, (0,1)`; action `(K1,T1)`. | `true,true,true,true,true,false` |

The source feature gate is validated from state/action only. It does not attach or compute effect labels.

## 3. Held-out primary semantic templates

For each semantic family, instantiate `r=0,1,2` using the shared IDs/slots above, then apply exactly one frozen surface recipe per held-out cell. Default values are `path_clear=true`, `K-r.opens_target_id=T1-r`, and both targets are closed and adjacent. Apply only the listed override:

| Semantic family | Overrides from default |
|---|---|
| `POS-VALID` | None. Action `(K-r,T1-r)`. Both targets closed and adjacent. |
| `NEG-WRONG-RELATION` | Set `K-r.opens_target_id=T2-r`; action remains `(K-r,T1-r)`. |
| `NEG-TARGET-OPEN` | Set both targets `closed=false`; action `(K-r,T1-r)`. |
| `NEG-NONADJACENT` | Use the nonadjacent target slots; both targets remain `closed=true`; action `(K-r,T1-r)`. |
| `NEG-BLOCKED-PATH` | Set `path_clear=false`; action `(K-r,T1-r)`. |
| `NEG-WRONG-ROLE` | Keep the real key relation `K-r.opens_target_id=T1-r`; give `D-r` the same `opens_target_id=T1-r` and same `blue/key` appearance as the key; action `(D-r,T1-r)`. All references resolve. |
| `NEG-ABSENT-KEY` | Keep `K-r.opens_target_id=T1-r`; action `(K-MISSING-r,T1-r)`, where `K-MISSING-r` is absent from the state. |

Every template has two targets with matching closed-state and adjacency facts, in distinct coordinate slots: both are closed/adjacent for all rows except `NEG-TARGET-OPEN` (both open/adjacent) and `NEG-NONADJACENT` (both closed/nonadjacent). This makes all seven semantic templates eligible for H-ROLE and H-COMPOSED. This specification does not assign outcome labels.

## 4. Surface application and IDs

For every held-out primary semantic template and replicate, apply the corresponding existing recipe constructor in `src/t2t_s3/generator.py`:

- `H-ID`: `identity_shift_recipe`.
- `H-APP`: `appearance_shift_recipe`.
- `H-LAYOUT`: `layout_shift_recipe`.
- `H-ROLE`: `role_layout_recipe`.
- `H-COMPOSED`: `composed_surface_recipe`.

Object-reference fields are transformed with the recipe's ID map. Action IDs are transformed by the same map; for the intentionally absent `K-MISSING-r`, create the corresponding fresh absent ID using the recipe's ID prefix, leaving it absent from the object list. The H-ROLE recipe is constructed on the complete base state before any diagnostic unknown masking. Its eligibility is verified for every primary cell/replicate; the fixed failure policy is STOP and report, not substitute or rebalance.

After transform, set the embedded state `context_id` equal to the final manifest context ID. Use these deterministic IDs:

- Source: `SRC-{contrast_id}`.
- Primary held-out: `HO-{surface_family}-{semantic_family}-R{replicate_index}`.
- Diagnostic: `DG-{surface_family}-UNKNOWN-R{replicate_index}`.

The arrays in each state retain the recipe's output object order; do not sort object records after transformation.

## 5. Diagnostic templates

For each of the five surface families, create exactly two diagnostic contexts (`r=0,1`) from the `POS-VALID` base template. Apply the respective surface recipe while the state is complete; then set the required field `path_clear=null` and preserve it as unknown. Mark `endpoint_scope=DIAGNOSTIC_ONLY`, `semantic_family=UNKNOWN-REQUIRED-DIAGNOSTIC`, and reason `UNKNOWN_REQUIRED_STATE`. Do not infer or attach an effect. Masking occurs after H-ROLE/H-COMPOSED recipe construction because those recipe constructors require a complete base state.

## 6. Construction validation (no outcome evaluation)

Allowed checks are schema/semantic validation of IDs, roles, feature vectors, complete-vs-diagnostic state fields, resolved references, cell membership, recipe determinism, and H-ROLE eligibility. `source_only_features` may be used to check the six source feature bits. Do not call `RelationalUnlockWorld.step`, fit any arm, generate predictions, or compute a score. The manifest generation process must not produce effect labels.
