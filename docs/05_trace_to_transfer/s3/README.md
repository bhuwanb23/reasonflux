# T2T-S3-RA — Replay Competence & Execution-Readiness Resolution

**Status:** implementation-only resolution package completed; **S3 execution remains unauthorized**. No held-out contexts were generated or exposed, no S3 outcomes were calculated, and Claim N remains unresolved.  
**Prior review:** S3-R v1 was **BLOCKED**; its report is preserved at [`s3_review_v1.md`](s3_review_v1.md).

## Resolution decisions and artifacts

- [`s3_plan.md`](s3_plan.md) — current R0–R4/I0 contract. R4 is now explicitly Option B: a minimum-node source-derived Boolean decision tree over the frozen six predicates.
- [`transformation_cells_v1.json`](transformation_cells_v1.json) — finite recipe-level source/development/held-out cell families; no contexts, IDs, counts, or labels are materialized.
- [`competence_review.md`](competence_review.md) — independent comparator review packet; reviewer remains unassigned.
- [`s3_ra_resolution.md`](s3_ra_resolution.md) — decisions, checks, and remaining gates for this focused resolution.
- [`freeze_manifest.json`](freeze_manifest.json) — implementation and protocol hashes; it is a review candidate freeze, not an execution authorization.
- `src/t2t_s3/arms.py` — R4 minimum binary decision-tree compiler; metadata-only `context_id`; all arms retain complete source trace-ID provenance.
- `src/t2t_s3/scoring.py` — all-context and per-cell denominator, exact accuracy, coverage, and wrong/abstain/invalid/missing accounting.
- `src/t2t_s3/generator.py` and `transforms.py` — named deterministic recipe builders and one-to-one remapping validation.
- `src/t2t_s3/eventlog.py` — outcome-free prediction logs and cell-linked per-context score events.

## R4 definition

R4 uses six fixed observable Boolean predicates: the five unary/type/precondition features plus `key_unlocks_selected_target`. It compiles the minimum-internal-node binary decision tree consistent with complete source traces. Each predicate may appear at most once per path; ties use fixed feature order, then false-branch before true-branch recursive serialization. This grammar can represent every Boolean function over the six predicates. Held-out labels, hidden state, and post-result updates are not used.

Development-fixture software checks include source contrasts for each precondition and verify the compiled tree on all 64 **abstract feature rows**. This is an implementation competence check only; it is not an S3 context suite, execution, or Claim N result.

## Still required before any run

1. Independent review of R4's source-only capability, minimal-tree algorithm/tie-break, and fairness.
2. Owner confirmation that unknown-required-state diagnostics are outside the primary scored denominator because the no-hidden-state simulator cannot assign them an exact effect label.
3. Source/development/held-out context manifests, context counts, eligible denominator, and source coverage specification.
4. Resource vector/caps and full run configuration.
5. Separate explicit execution authorization.

The frozen recipe families are ID relabeling, appearance relabeling, rigid layout/order change, role-slot coordinate permutation, and their composition, crossed with complete-state semantic controls. The current freeze covers code/protocol artifacts only. Recipe cells do not contain data; score code has been checked on development fixtures only. No S3 run or ARC work is authorized.
