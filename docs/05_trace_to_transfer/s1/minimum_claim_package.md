# T2T-S1.1 — Minimum Claim Package

**ID:** `T2T-S1.1-MinimumClaims-v1.0.0-draft`  
**Purpose:** precommit the minimum defensible paper/claim outcomes before any mechanism results exist. This is a recommended decision policy for owner review, not a claim that any outcome occurred.

## Decision principles

1. The present standalone novelty claim for counterexample-guided applicability-boundary refinement remains a **no-go** under P1. A positive mechanism result does not erase that prior-art finding.
2. Claim N and Claim B are separate. A success on one does not rescue a failure on the other or license a combined claim.
3. Claim E is end-to-end method/baseline performance and remains unknown unless separately evaluated. N/B mechanism evidence cannot be described as E evidence.
4. Any paper must make the narrowest claim supported by the result. A result that is inconclusive, unobservable, or invalid does not count as a pass.
5. The S1.2 and S1.3 operational definitions control what “N succeeds” and “B succeeds” mean for this decision table; do not change them after outcomes.

## Outcome decisions

| Outcome | Recommended decision | Permitted framing | Not permitted |
|---|---|---|---|
| **O1: N succeeds; B succeeds; E unknown** | **Yes, write a bounded mechanism paper**, subject to independent novelty review and valid, reproducible evidence. | Report the tested predictive increment beyond strong replay and the separately tested boundary-measurability/refinement result. State that Claim E is unknown and that no ARC-AGI-3 superiority is established. | Claiming full-method efficacy, ARC performance, broad novelty of guard refinement, or that N/B imply E. |
| **O2: N succeeds; B fails** | **Yes, but narrow to N only**, if the comparative contribution survives novelty review. Remove counterexample-boundary improvement from the contribution and abstract. | A result about invariant-derived prediction beyond the frozen strong-replay comparator, limited to the tested domain. | Retaining B/C language, presenting the joint mechanism as validated, or using a B failure as a minor caveat while keeping it in the headline claim. |
| **O3: N fails; B succeeds** | **No paper under the current combined T2T framing by default.** Consider a separate boundary-only study only if a distinct, novelty-cleared question is identified before more work. | At most, a bounded report that the boundary outcome was measurable/improved in the tested synthetic mechanism, if the evidence is valid. | Calling the result support for invariant value or general novelty of counterexample-driven guard refinement. P1 directly warns against the latter. |
| **O4: N fails; B fails** | **Terminate the current T2T direction. Do not proceed to S2 or ARC evaluation.** Preserve/report the null or negative result if a valid test was run. | A transparent feasibility failure/negative result. | Moving thresholds, changing the primary metric, choosing a new toy family after seeing results, or relabeling failure as “promising.” |

## Non-binary and invalid outcomes

The table applies only to valid, interpretable S1/S2 evidence. If comparison integrity fails, the key state/effect is unobservable, or uncertainty is too large to determine success/failure, record **INCONCLUSIVE/BLOCKED**, not N/B success or failure. Do not force an O1–O4 label. Revisit the design only through a separately documented decision made without outcome-driven metric changes.

## S2 gate implied by this package

- If a properly controlled S2 test supports N, S2 may continue to test N even if B fails, but the project must drop B from the minimum claim package.
- If N is unresolved and B alone appears positive, do not automatically proceed: first resolve whether a distinct boundary-only research question survives P1 and obtain explicit owner approval.
- If both N and B fail, stop the current direction.
- A positive result is not permission for ARC-AGI-3 access or a run.

**Approval status:** the user reviewed and approved S1.1's O1–O4 framework on 2026-11-04 as part of approving S1. This records the recommended default policy for future outcome classification; it is not a present paper commitment. S2 was separately authorized afterward.
