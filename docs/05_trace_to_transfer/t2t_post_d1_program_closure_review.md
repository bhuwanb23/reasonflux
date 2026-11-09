# T2T Post-D1 Program Closure Review

**Status:** Claim N track closed; BL1 planning package authorized only. No experiment is active.  
**Owner direction:** D1-B — preserve boundary learning as a distinct, unvalidated research question.  
**New phase created:** no. **Implementation/execution authorized:** no.

## Final claim state

| Claim | Final status | Evidence ceiling |
|---|---|---|
| A | **Partial synthetic support** | Known-generator synthetic evidence only; no ARC-AGI-3 skill-generation evidence. |
| N | **CLOSED — N-FAIL** | Frozen S3 finite synthetic predictive estimand; I0=105/105, R4=105/105, `Delta_N=0`. Behavioral increment was not tested. |
| B | **Toy-fixture observation only** | S2 deterministic finite fixture; not decision-grade evidence of general boundary-learning benefit. |
| C | **Untested** | No evidence that boundary improvements reduce harmful transfer in an interactive agent. |
| D | **Untested** | No causal evidence that reduced harm improves held-out action efficiency. |
| E | **Untested** | No ARC-AGI-3 full-method comparison against meaningful skill baselines. |

## Accepted S3 finding

The strongest completed research question asked whether an invariant representation adds predictive value beyond a strong source-derived replay/compiler baseline. Under the frozen S3 estimand, the answer was **no**: I0 and R4 tied at 105/105, giving `Delta_N=0` and N-FAIL. The protocol was frozen, R4 received an independent fairness PASS, one authorized execution completed with no deviations or reruns, and the result is interpretable for this finite synthetic suite.

This closes Claim N v1. Do not rerun S3, weaken or revise R4, regenerate contexts, search for a post-hoc subset, reinterpret N-FAIL as N-BLOCKED, or create N-v2 as a rescue attempt.

## Program disposition

**No evidence-validated successor program exists.** D1-B preserves one potentially interesting but unvalidated question: whether counterexample evidence improves held-out applicability precision while preserving useful coverage. The S2 observation is motivation only; it does not establish Claim B.

A later owner decision authorized a BL1 planning package only (`bl1/`). That package is a distinct prospective research direction, not evidence, an implementation, an experiment, or permission to access ARC data. Any implementation or evaluation requires a separate review and explicit authorization.

## Records to preserve

Retain as permanent research records:

- `claim_n_archive.md`
- `boundary_learning_question.md`
- `reports/competition/arc_prize_2026_claim_evidence_map_v1.md`
- `reports/experiments/T2T-S3-EXEC-2026-11-05-001/` (execution record, predictions, score events, reports, decision)
- Frozen S3 manifests, hashes, scoring contract, arms, and replay ladder
- `t2t_post_claim_n_decision_review.md`
- `bl1/bl1_program_charter_v1.md`, `bl1/bl1_claim_map_v1.md`, and `bl1/bl1_protocol_draft_v1.md` (planning-only drafts)

**End state:** Claim N answered and archived. BL1 planning is authorized; boundary learning remains unvalidated. No implementation, experiment, ARC work, or execution is authorized.
