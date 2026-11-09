# T2T-D1 — Post-Claim-N Decision Review

**Review status:** complete; owner selected **D1-B** on 2026-11-05.  
**New phase created:** no.  
**S3 rerun authorized:** no.  
**Claim N v1:** permanently closed as N-FAIL; see `claim_n_archive.md`.

## 1. Decision-grade result

The single authorized S3 execution completed without protocol deviations or reruns. The frozen finite suite produced:

- I0: **105/105** exact predictions.
- R4: **105/105** exact predictions.
- `Delta_N = Accuracy(I0) - Accuracy(R4) = 0`.
- Frozen rule: `Delta_N <= 0` → **N-FAIL**.

This is an interpretable failure of Claim N v1 for the frozen synthetic estimand. It is not N-BLOCKED, and it is not evidence that every possible invariant representation must fail. The result shows that I0 did not add predictive value beyond the frozen source-derived R4 compiler in this suite.

Primary records: `reports/experiments/T2T-S3-EXEC-2026-11-05-001/claim_n_decision.md`, `delta_n_report.json`, and `s3_execution_record.json`.

## 2. What failed

- **Claim N v1:** the claim that an explicit invariant representation adds predictive value beyond the strongest frozen replay/compiler did not survive its first decision-grade synthetic test.
- **The N-led novelty/advantage argument:** do not continue presenting invariant-specific predictive value beyond replay as supported by this project.
- **Any attempt to rescue this result by changing R4, changing counts/contexts, selecting a subset, or redefining the result as blocked:** prohibited. The valid classification is N-FAIL for the frozen finite suite.

## 3. What survives

- **Claim A:** partial synthetic support in a known generator only; no ARC-AGI-3 evidence.
- **Claim B:** one deterministic toy-fixture pass in S2 only. It is not decision-grade evidence of general boundary-learning benefit.
- **Claims C, D, and E:** untested.
- **Reusable artifacts:** the formal skill object, replay ladder, invariant implementation, scoring/event contracts, manifests, and the clean negative S3 result remain useful as engineering and research records. Their existence is not evidence that the method is effective.
- **Scientific information:** a source-derived Boolean replay compiler matched I0 on all 105 frozen contexts. This is a meaningful finite-domain equivalence result and a limit on the current claim.

Updated statuses are recorded in `reports/competition/arc_prize_2026_claim_evidence_map_v1.md` and `docs/05_trace_to_transfer/current_evidence.md`.

## 4. Project options

| Option | Decision | Consequence and evidence boundary |
|---|---|---|
| **D1-A — Terminate T2T** | Close the current T2T line. | Appropriate if the program's purpose was specifically to establish Claim N. Preserve the artifacts and negative result; do not run further work under the current claim. |
| **D1-B — Narrow to boundary learning** | End Claim N and retain boundary learning as the only possible future research target. | B has only a toy-fixture pass. A future boundary-learning study would need its own prospective scope and authorization; this review does not establish B or authorize that study. |
| **D1-C — Redefine Claim N** | Not recommended as a response to this result. | A replacement claim is permissible only if genuinely distinct—not a post-hoc rescue—and requires a new claim, protocol, comparator, and suite. It is not a rerun and is not authorized here. |

## 5. Recommendation

**Recommend D1-B, conditionally:** close Claim N v1 as failed and, if the owner wants to retain a research line, narrow it to the independent boundary-learning question. The reason is that S3 did not test Claim B, while S2 contains a limited toy-fixture observation worth distinguishing from N. This is a direction choice, not a claim that boundary learning is established or novel.

If the owner's objective was exclusively to support invariant value beyond replay, choose **D1-A** instead. Do not choose D1-C to preserve the original conclusion after N-FAIL.

## 6. What remains scientifically interesting

A distinct boundary-learning question remains falsifiable: **does counterexample evidence improve held-out applicability precision at useful coverage, compared with an otherwise matched replay/control policy?** S2's toy result motivates the question but does not answer it. Claims about reduced negative transfer, action efficiency, or full-method superiority (C/D/E) remain separate and untested; none should be inferred from the S3 result.

## 7. Stop conditions and owner action

- No S3 rerun, R4 weakening, context regeneration, post-hoc subset, or outcome-informed modification.
- Do not create a new T2T phase or protocol until the owner records D1-A, D1-B, or D1-C.
- Owner decision is recorded: **D1-B**. Preserve only the boundary-learning question in `boundary_learning_question.md`; do not create a new phase, implement, or execute without a separate future owner decision.
