# T2T-S3-RA — Focused Replay Competence Resolution

**Version:** `T2T-S3-RA-v0.2.0`  
**Status:** implementation resolution complete; **independent review and execution readiness remain pending**  
**No S3 run, held-out-context generation/exposure, outcome calculation, or Claim N decision occurred.**

## Decision 1 — R4 is Option B

R4 is defined as a **source-derived Boolean compiler**, not an exact-row lookup. Its frozen input grammar is exactly six observable Boolean predicates, in this order:

1. `key_is_key`
2. `target_is_target`
3. `target_closed`
4. `agent_adjacent`
5. `path_clear`
6. `key_unlocks_selected_target`

`R4.fit` maps complete source traces to six-bit rows and effects. `SYNTHETIC_SOURCE` provenance is required by default; development traces require explicit `allow_development=True`. Conflicting labels for an identical row are rejected. It then compiles a minimum-internal-node binary decision tree consistent with all source rows; each predicate is tested at most once per path. Ties are broken by recursive tree serialization using the fixed feature order and false branch before true branch. Leaves emit exact success or exact no-effect. All selection uses source labels only. Incomplete required inputs or dangling references abstain before tree evaluation.

This hypothesis class can represent every Boolean function over the six predicates and can classify feature combinations not literally present as source rows. It is the strongest compiler **within this frozen predicate grammar**; it is not a claim that no larger source-derived program language exists. If its compiled tree reproduces I0, the protocol's N rule yields a legitimate N-FAIL; comparator expressivity is not to be reduced to seek a pass.

### Development-only competence checks

The software fixture supplies an all-true positive row plus a one-false source contrast for each of the six predicates, with the other five held true and the expected exact no-effect label. This deterministic contrast-coverage criterion is for compiler identifiability, not a population sample-size choice. The fitted minimum tree is checked over all 64 abstract six-bit rows against the predeclared conjunction. The frozen source cell requires the same feature-row coverage before any held-out exposure. This is an algorithmic unit check over Boolean feature assignments, not materialized world contexts, an S3 suite, or an experiment. A sparse two-trace fixture is also retained to show why source contrast coverage matters: its learned tree overgeneralizes to an open-target row. The run gate therefore includes prospective source-opportunity/competence review.

## Decision 2 — `context_id` is metadata only

`UnlockState.context_id` remains available for logs/provenance but is excluded from all predictor signatures and prediction inputs. R0 now replays on the exact ordered **observable state** and literal action only. A regression test changes the logging ID while holding the observation fixed and confirms the replay result is unchanged.

## Decision 3 — scoring implementation

`src/t2t_s3/scoring.py` now provides deterministic all-context and per-cell scoring. For each declared arm and eligible context it reports denominator, exact correct/wrong, coverage, abstention, invalid and missing counts. Missing predictions, abstentions, invalid predictions, and wrong predictions remain in the full denominator and score zero. Empty predeclared cells are retained with denominator zero and undefined accuracy/coverage. The scorer rejects duplicate or ineligible prediction records and unknown outcome labels. No composite score is created.

`eventlog.py` includes the cell ID on prediction and score events. The focused suite reports **11 passed** and `compileall` succeeds; these unit tests exercise denominator/error accounting on hand-built development records only. The scorer has not been applied to any S3 contexts.

**Unknown-required-state rule:** the simulator returns no effect label when a required field is unknown. Such cases are therefore specified as abstention-contract diagnostics, not primary scored outcomes. Owner confirmation is still required before any run; including them in the primary denominator would require a prospectively revised world/label contract, not hidden-state labels.

## Decision 4 — recipe-level transformation cells

[`transformation_cells_v1.json`](transformation_cells_v1.json) freezes a finite recipe-level role matrix:

- canonical source family;
- software-only development fixtures; and
- held-out identity, appearance, rigid layout/order, role-slot coordinate permutation, and composed surface families crossed with the declared complete-state semantic contrasts.

Cell IDs derive from the surface-family and semantic-family IDs. Recipes are deterministic: fresh injective ID relabeling; one-to-one appearance relabeling; fixed quarter-turn/translation/order reversal; and their composition. No context IDs, contexts, labels, sample sizes, or cell counts are assigned or materialized. Unknown-required diagnostics are explicitly outside the primary scored cells. This freezes the recipe cells, not the eventual finite list of evaluated contexts or run-specific denominators.

## Decision 5 — independent review and readiness

The R4 algorithm and development checks now address the earlier exact-row limitation. However, the required independent comparator review is still **unassigned**; the implementation author cannot self-sign that gate. No independent R4 fairness verdict is claimed. The role-level cell matrix also does not yet supply a source manifest, context counts, resource caps, or a complete run configuration.

### S3-RA disposition

**PARTIAL — package-level resolution implemented; execution readiness not demonstrated.** R4 is no longer ambiguous as an algorithm and its Boolean expressivity is software-checked. Independent review must still judge whether the six-predicate grammar and source opportunity are a fair primary comparator for the frozen estimand. The context-role recipes are frozen, while actual source/held-out manifests and counts remain unset by design.

Execution remains unauthorized. Before any future request, obtain independent review, owner confirmation of the unknown-required diagnostic policy, source/development/held-out manifests and counts, resource vector/caps, and separate explicit execution authorization. No ARC work is included.
