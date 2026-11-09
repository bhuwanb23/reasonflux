# S3-E Resource Vector v1

**Status:** owner-approved resource rules recorded; execution remains unauthorized.  
**Applies to:** I0 and R0–R4, with identical opportunity and interface constraints.

## Frozen per-context opportunities

| Resource / access | Frozen value or rule |
|---|---|
| Prediction opportunities | Exactly 1 prediction per arm per context. No retries or second submissions. |
| World accesses | Exactly 1 evaluator-owned world access per context, shared for scoring and performed only after all arm predictions for that context have been recorded. No arm may query the outcome oracle. |
| State observation | Identical observable state to every arm; no hidden fields. |
| Action schema | Identical action schema to every arm. |
| Predicate access | Same six frozen observable predicates and underlying observable interface; no additional predicates for any arm. Representation/algorithm differences remain those already frozen in R0–R4 and I0. |
| Source manifest | Same source context manifest and, at the later authorized fitting stage, the same source evidence/labels are available to every arm under its declared fitting rule. No arm receives additional source traces. |
| Held-out access | Prediction-only access to the held-out context inputs. No effect labels or world-oracle result before prediction records are frozen. |
| Adaptive refit | Prohibited. |
| Post-held-out updates | Prohibited. |
| Additional metadata | No arm receives extra context metadata. `context_id` is logging/provenance only and excluded from replay matching and predictor inputs. |
| Additional transformation information | Prohibited after manifest freeze. Every arm receives the same held-out state/action observations; no arm receives a privileged transformation label unless the frozen protocol provides it equally to all. |

## Determinism and environment

Owner-approved environment decision: use the existing deterministic world, frozen transformation recipes, R0–R4, I0, and scoring implementation; introduce no environment variation. The workspace runtime observed while recording this v1 is Python **3.13.16** and pytest **9.0.3**. This is an environment fingerprint, not permission to upgrade/downgrade or vary dependencies. Record exact source/package hashes and the actual run environment before any separate execution authorization; any mismatch requires owner review before run.

## Audit and stop conditions

- Log one prediction opportunity per arm/context and the single evaluator-owned world access after prediction commitment.
- Verify identical manifest access and state/action schema for every arm.
- If a retry, extra source trace, hidden label exposure, extra predicate, adaptive refit, post-holdout update, or arm-specific transformation information occurs, stop and mark the run protocol-invalid; do not calculate or report Claim N.
- This vector freezes resource opportunities, not unprovided numerical compute/time caps. No CPU, memory, wall-time, token, or other cap is invented here; any such cap must be separately owner-approved before execution.
