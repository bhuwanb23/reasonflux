# T2T Master Plan — From Trace to Transfer

## Purpose

Prepare a rigorous research program for counterexample-guided invariant skill formation in ARC-AGI-3. Work proceeds from novelty and definitions to algorithm/protocol design, and only later—under existing authorization—to implementation and evaluation.

## Plan status and semantics

`T2T-P0` through `T2T-P7` are **documentation/research-design work packages**, not additional readiness phases or run gates. “Complete” means the document is internally reviewed; it does not authorize scientific execution. Existing Phase 2I, Phase 3B, Phase 3D, hidden-outcome and data-integrity restrictions remain controlling.

## Dependency graph

`P0 Scope/claims → P1 Prior art → P2 Formal skill object → P3 Claim N/control fairness → P4 Boundary-learning algorithm → P5 Protocol design → P6 Implementation blueprint → P7 Reporting/evaluation plan`

P1 may force a revision or termination of the novelty claim before further design. P3 must be complete before saying the invariant representation adds value beyond replay. P4 must be specified before P5 can freeze the treatment. P5/P6 are plans only until separately authorized.

## Phase and subphase index

| Phase | Objective | Subphases | Output |
|---|---|---|---|
| **T2T-P0 — Scope and claim discipline** | Freeze the question, central claim, nonclaims and current evidence ceiling. | P0.1 Thesis; P0.2 Claim/evidence boundaries | Core idea and claim map |
| **T2T-P1 — Prior-art matrix** | Determine whether the proposed novelty wedge is genuinely differentiated. | P1.1 Source inventory; P1.2 Mechanism comparison; P1.3 Novelty decision | [`P1 review packet`](p1/README.md): source inventory, mechanism comparison and interim disposition; final owner-approved decision outstanding |
| **T2T-P2 — Formal skill object** | Specify what is learned, stored, updated and executed. | P2.1 Schema; P2.2 Invariant vs replay; P2.3 Evidence/lifecycle | Implementable object contract |
| **T2T-P3 — Claim N and fair replay controls** | Isolate whether invariant semantics add value beyond replay/compression. | P3.1 Raw replay; P3.2 Strong replay; P3.3 Isolation/budget matching | Control specification and Claim N decision rule |
| **T2T-P4 — Counterexample boundary algorithm** | Define candidate extraction, counterexample handling, scope revision and abstention. | P4.1 Candidate generation; P4.2 Counterexample taxonomy; P4.3 Scope/refinement; P4.4 Fallback | Pseudocode and failure semantics |
| **T2T-P5 — Experimental protocol design** | Specify future comparisons and measurement without running them. | P5.1 Arms/estimands; P5.2 Data and budgets; P5.3 Metrics; P5.4 Analysis/falsifiers | Protocol draft, not preregistration authorization |
| **T2T-P6 — Implementation blueprint** | Map the object and algorithm into modules/logging/tests. | P6.1 Architecture; P6.2 Event schema; P6.3 Contract tests | Engineering plan only |
| **T2T-P7 — Evaluation and reporting plan** | Define claim-to-result reporting, decision outcomes, and paper artifact needs. | P7.1 Claim decisions; P7.2 Reporting tables; P7.3 Reproducibility/paper alignment | Results shell and paper outline |

## Deliverable order

1. Finish P0 and use it as the immutable claim ceiling.
2. Complete P1 before calling the idea novel. If an equivalent method exists, narrow, differentiate, or stop.
3. Freeze the formal object and comparator semantics in P2–P3.
4. Specify algorithm and diagnostics in P4.
5. Draft—but do not execute—the protocol in P5; no hidden/test access and no confirmatory split assignment without authorization.
6. Create code architecture only after P1–P5 are coherent and the owner explicitly authorizes relevant work.
7. Run nothing until the applicable prior approvals/data/competition controls are satisfied. This plan itself grants no approval.

## Current document status (2026-11-03)

The folder now contains the top-level design drafts, eight phase briefs and all 25 subphase briefs. This is documentation coverage, not scientific completion: P1 is an initial prior-art matrix rather than a completed review; schema, algorithm, comparator and protocol choices remain drafts; protocol thresholds and sample size remain unset. No implementation, experiment, benchmark, ARC run, split assignment, or restricted-outcome access has occurred or is authorized by these documents.

## Stop/redirect conditions

- P1 finds the exact contribution already established: revise or abandon the novelty claim.
- P3 shows invariant and strong replay are operationally indistinguishable: do not claim invariant-specific value; consider a narrower compression/efficiency claim only if supported and novel.
- P4 cannot produce a reproducible boundary rule: do not proceed to an empirical claim about counterexample-guided scope.
- Any later result fails its predeclared criterion: report the failure and narrow the claim; never tune thresholds after seeing outcomes.
