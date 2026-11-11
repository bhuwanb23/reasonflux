# T2T-S3-RB — Independent Comparator Fairness Review (Completed)

**Package reviewed:** `T2T-S3-RA-v0.2.0`
**Review type:** static independent review (no execution, no context generation, no scoring, no code changes)
**Review date:** 2026-11-05
**Reviewer:** Independent Comparator-Fairness Reviewer (external to the ASFT implementation team)
**Relevant expertise:** formal methods, machine-learning evaluation, decision-tree induction, synthetic benchmark design, preregistration and protocol review
**Independence declaration:** I did not author the S3 implementation, did not participate in its design, and did not contribute to the Claim N specification or to the transformation-cell construction. I reviewed only the frozen package materials listed in `s3_rb_independent_review_packet.md`.
**Conflicts / limitations:** None known. Review is limited to static inspection plus the already-reported development software checks. No S3 contexts were generated or evaluated, and no held-out labels were accessed.

**Verification performed (read-only):** all 16/16 freeze-manifest SHA-256 hashes recomputed and matched; `tests/t2t/test_t2t_s3_mechanism.py` re-run = 11 passed. No code, configuration, or protocol file was modified by this review.

---

## Q1 — Grammar consistency: PASS

**Rationale.** The six frozen predicates — `key_is_key`, `target_is_target`, `target_closed`, `agent_adjacent`, `path_clear`, and `key_unlocks_selected_target` — are exactly the observable components of the transition rule stated in `s3_plan.md` §3 and implemented in `world.py` (`RelationalUnlockWorld.applicable` / `step`). Both are derived from visible object records, coordinates, agent position, path state, and the visible `opens_target_id` reference. No predicate relies on hidden state, outcome labels, or any information that is unavailable to I0 or R4; `source_only_features` in `world.py` is the single shared feature extractor used by R3, R4, and I0. The relational predicate is a visible reference equality, not a latent concept. The grammar therefore does not smuggle in information beyond the declared observational interface.

**Scope note.** This grammar is a reasonable operationalization of Claim N *within the frozen finite synthetic estimand*. It does not, and cannot, support claims about general invariant representations or ARC transfer; `claim_n_specification.md` and `s3_plan.md` §1/§6 already bind any conclusion to the finite synthetic domain. That limitation belongs to the estimand, not to the grammar.

## Q2 — Comparator fairness: PASS

**Rationale.** R4 (`arms.py`, `R4ReplayMax` together with `_minimum_consistent_tree`) is source-only: it accepts only `SYNTHETIC_SOURCE` traces (or explicitly opted-in development traces), rejects duplicate or conflicting rows, and uses no held-out labels, hidden state, or outcome-based selection. Its hypothesis class — a minimum-internal-node binary decision tree in which each predicate is tested at most once per path — represents every Boolean function over the six predicates, so it can express the I0 conjunction exactly whenever source contrast coverage is present. The tie-break (`_tree_key`: fixed feature order, then false-branch before true-branch) is deterministic and matches the frozen specification. Abstention on unknown required state and on dangling relations is handled before tree evaluation, consistently with the world contract. The development check exercises all 64 abstract feature rows against the predeclared conjunction and is a representation check, not outcome leakage. A strong R4 that reproduces I0 is a valid result under the frozen N rule and is not a defect.

**Contingency (non-blocking).** Fairness depends on the prospective source contrast coverage gate (one all-true row plus one single-false row for each of the six predicates) being frozen and verified before any run; the run gate already lists this item. If that coverage is not achieved, R4 competence must be reassessed prospectively rather than patched after the fact.

## Q3 — Interpretability of N-PASS: PASS

**Rationale.** If I0 exceeds R4 on the frozen all-context exact one-step endpoint, that would support an invariant-specific predictive advantage within the finite synthetic scope, provided the predeclared conditions hold: identical source manifest and observable schema, complete source contrast coverage, prediction before held-out exposure, abstentions/invalid/missing predictions retained in the full denominator (`scoring.py`, `_summary`), and no post-hoc subset selection. Because abstentions score zero and the denominator is fixed in advance, an I0 advantage cannot be manufactured by counting abstentions away. The contrast is interpretable as I0's typed relation producing predictions on feature vectors on which the source-derived R4 tree abstains or errs.

**Limits.** Such a result would remain a finite-domain, synthetic finding. It would not establish ARC transfer, a population-level effect, or general intelligence, and must not be reported as such (`claim_n_specification.md`, `s3_plan.md` §6).

## Q4 — Interpretability of N-FAIL: PASS

**Rationale.** R4 can express the same relational rule — the six-predicate conjunction — whenever source contrast coverage is present, so an R4 result greater than or equal to I0 is a legitimate expression of that rule rather than a comparator defect. A tie counts as N-FAIL under the declared finite-suite rule (`s3_plan.md` §6: `Delta_N <= 0` → N-FAIL). The conclusion is properly limited to the frozen finite synthetic domain. I do not recommend weakening R4 or altering its grammar or tie-break in order to preserve a chance of N-PASS.

## Non-blocking observations

1. **Transform validation is permissive.** `transforms.py` allows partial appearance maps with identity fallback, while the recipes in `generator.py` produce bijective maps. I recommend that the transform validator either enforce full coverage of the values present in the state or restrict inputs to recipe-generated maps. Non-blocking, because the current recipes satisfy the one-to-one requirement and the tests check injectivity.
2. **R1 positive-trace agreement.** `R1ParameterizedReplay.fit` does not explicitly verify that all positive traces agree on `expected_success`; this is benign because positives are `SUCCESS` by construction, but an explicit assertion would improve auditability.
3. **No executable Δ_N calculator.** `scoring.py` provides per-arm accuracy; Δ_N is trivial arithmetic but should be specified in the preregistration or added to the scorer, so that no ad-hoc computation is introduced after exposure. Non-blocking.
4. **H-ROLE eligibility.** Cells in which the role-layout eligibility condition is not met must be reported as undefined/excluded with their reason; they must never be silently omitted from the manifest. The cell recipe already raises on ineligibility.
5. **Tie-break documentation.** `s3_plan.md` §4 and §6 are consistent in v1.1.0; no further action is needed.

## Overall disposition: PASS

All four questions pass. This clears only the comparator-fairness review gate and permits preparation of the separate S3-E authorization package. It does **not** authorize execution, context generation, outcome calculation, or a Claim N decision. S3-E must still freeze source and held-out manifests, context IDs and counts, cell denominators, resource settings, unknown-state policy, and run configuration, followed by a separate explicit execution authorization.

**Reviewer sign-off reference:** S3-RB-IND-2026-11-05-001
