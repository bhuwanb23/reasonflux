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
| **T2T-P1 — Prior-art matrix** | Determine whether the proposed novelty wedge is genuinely differentiated. | P1.1 Source inventory; P1.2 Mechanism comparison; P1.3 Novelty decision | [`P1 review packet`](p1/README.md): completed bounded source inventory, mechanism comparison and owner-selected comparative reframe; not novelty clearance |
| **T2T-P2 — Formal skill object** | Specify what is learned, stored, updated and executed. | P2.1 Schema; P2.2 Invariant vs replay; P2.3 Evidence/lifecycle | [Versioned object contract, JSON Schema and fixtures](p2/README.md); documentation complete with explicit open design choices |
| **T2T-P3 — Claim N and fair replay controls** | Isolate whether invariant semantics add value beyond replay/compression. | P3.1 Raw replay; P3.2 Strong replay; P3.3 Isolation/budget matching | [Versioned fair replay contract, estimands, ablations and falsifiers](p3/README.md); documentation complete with open protocol choices |
| **T2T-P4 — Counterexample boundary algorithm** | Define candidate extraction, counterexample handling, scope revision and abstention. | P4.1 Candidate generation; P4.2 Counterexample taxonomy; P4.3 Scope/refinement; P4.4 Fallback | [Versioned deterministic boundary algorithm, taxonomy, data rules and fallback fixtures](p4/README.md); documentation complete with open domain/protocol choices |
| **T2T-P5 — Experimental protocol design** | Specify future comparisons and measurement without running them. | P5.1 Arms/estimands; P5.2 Data and budgets; P5.3 Metrics; P5.4 Analysis/falsifiers | [Versioned claim-specific protocol proposal](p5/README.md); documentation complete, not preregistration or authorization |
| **T2T-P6 — Implementation blueprint** | Map the object and algorithm into modules/logging/tests. | P6.1 Architecture; P6.2 Event schema; P6.3 Contract tests | [Versioned architecture, event schema and synthetic contract-test plan](p6/README.md); documentation complete, not implementation/authorization |
| **T2T-P7 — Evaluation and reporting plan** | Define claim-to-result reporting, decision outcomes, and paper artifact needs. | P7.1 Claim decisions; P7.2 Reporting tables; P7.3 Reproducibility/paper alignment | [Versioned claim decisions, blank results shell and submission/reproducibility checklist](p7/README.md); documentation complete, not results or authorization |

## Deliverable order

1. Finish P0 and use it as the immutable claim ceiling.
2. Complete P1 before calling the idea novel. If an equivalent method exists, narrow, differentiate, or stop.
3. Document the formal object contract in P2 and specify fair replay/comparator semantics in P3; keep unresolved representation choices explicit rather than guessing.
4. Specify algorithm and diagnostics in P4.
5. Complete P5 as a reviewable protocol draft; do not execute it. No hidden/test access or confirmatory split assignment without separate authorization.
6. P6's build plan is complete; any code architecture or engineering execution still requires explicit owner authorization after P1–P5 and applicable project controls are reviewed.
7. Complete P7 as a claim-linked reporting/reproducibility design; do not treat its results shell as evidence or its checklist as submission approval.
8. T2T-S1 was approved and the user separately authorized T2T-S2. The S2 prototype produced a finite B pass; Claim N is blocked for decision-grade interpretation because the baseline/model changed after the initial pilot and the N holdout was reused. See [`s2/results_v1.md`](s2/results_v1.md). Do not proceed to ARC or another implementation step automatically.
9. Any fresh N test, boundary-only continuation, or ARC work requires a new prospective scope/decision and applicable approvals. This plan itself grants no approval.
10. The T2T-S3 Claim N implementation package is recorded at [`s3/README.md`](s3/README.md). The user authorized implementation and development-fixture software checks only; S3 evaluation, held-out-context generation/exposure, outcome calculation, and Claim N decision remain unauthorized, and execution requires separate approval.

## Current document status (2026-11-04)

The folder contains the top-level design drafts, eight phase briefs and all 25 subphase briefs. P1 is **closed for the owner-approved idea-stage scope**: the recommendation is no-go on the standalone novelty claim, and the owner selected the comparative reframe direction on 2026-11-03; this is not novelty clearance, and SAGE/independent-review limitations remain. P2 is **complete for documentation/design scope**: its versioned object contract, JSON Schema and interoperability fixtures are reconciled across P2.1–P2.3. P3 is **complete for documentation/design scope**: its versioned fair replay contract, control arms, budget vector, estimands, ablations and falsifiers are reconciled across P3.1–P3.3; exact protocol choices remain open. P4 is **complete for documentation/design scope**: its versioned candidate/triage/refinement/fallback contract and synthetic decision fixtures are reconciled across P4.1–P4.4; exact ontology, thresholds, manifests and runtime caps remain open. P5 is **complete for documentation/design scope**: its versioned claim-specific protocol proposal and P5.1–P5.4 records are reconciled; alpha/confidence level, effect margins, sample size/power, cohort, split, metrics operating points, resource caps, and required approvals remain unset. P6 is **complete for documentation/design scope**: versioned architecture, event-schema proposal and synthetic contract-test plan are reconciled across P6.1–P6.3; no implementation or tests were run. P7 is **complete for documentation/design scope**: versioned claim decisions, blank result shell, failure/cost accounting, and reproducibility/submission checklist are reconciled across P7.1–P7.3; no results or submission artifacts were produced or verified. After P7, a separate user-authorized local/synthetic Step 1 implemented event-schema validation and an append-only journal; it is tracked in [`implementation/step1_event_journal_plan.md`](implementation/step1_event_journal_plan.md) and does not authorize method execution or ARC/data access. T2T-S1 was approved by the user, and S2 was separately authorized. The S2 key/door prototype is recorded in [`s2/README.md`](s2/README.md): the initial N pilot was followed by a stronger replay/model version using the same N holdout, so N is **BLOCKED** for decision-grade interpretation; B passed only on the finite synthetic fixture. The revised raw N score is a tie, not an independent confirmation. No ARC-AGI-3 implementation/run, competition data, split assignment, restricted outcome access, or broader T2T method has occurred or is authorized by this documentation. A T2T-S3 Claim N implementation package was built under explicit implementation-only authorization; its development-fixture software tests passed, independent competence review is pending, and no S3 evaluation or Claim N decision is authorized.

## Stop/redirect conditions

- P1 finds the exact contribution already established: revise or abandon the novelty claim.
- P3 shows invariant and strong replay are operationally indistinguishable: do not claim invariant-specific value; consider a narrower compression/efficiency claim only if supported and novel.
- P4 cannot produce a reproducible boundary rule: do not proceed to an empirical claim about counterexample-guided scope.
- Any later result fails its predeclared criterion: report the failure and narrow the claim; never tune thresholds after seeing outcomes.
