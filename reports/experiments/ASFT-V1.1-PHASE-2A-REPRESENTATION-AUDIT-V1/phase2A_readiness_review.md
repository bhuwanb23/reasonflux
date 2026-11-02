# ASFT v1.1 Phase 2A — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-2A`  
**Package:** `ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1`  
**Objective:** audit exactly what the Phase 13G ARC representation can/cannot express and make representation-vs-search hypotheses falsifiable.  
**Method:** read-only source/output audit; no new ARC task processing or benchmark execution.

## Executive decision

- **PASS for Phase 2A audit/specification layer.**
- **Primitive inventory:** PASS, complete for the Phase 13G source-defined solution DSL and auxiliary representation/feature/trace layers.
- **Empirical ARC mechanism execution:** NOT RUN in 2A.
- **Phase 2 overall ARC Foundation Readiness:** **BLOCKED** pending the later phase gates; Phase 2A does not certify readiness for confirmatory ARC mechanism tests.

## Phase 2A exit questions

| Question | Answer | Boundary |
|---|---|---|
| Q1 — Primitive inventory complete? | **Yes, within audited Phase 13G source scope.** | 10/10 candidate programs inventoried; auxiliary features, generic helpers, and trace labels are separated from solution primitives. This is not a complete ontology of ARC concepts. |
| Q2 — Coverage map complete? | **Yes, at the bounded operational level.** | Saved full-inventory rates are mapped by split; unsupported remains “no fit under this implementation,” not semantic “not representable.” |
| Q3 — Missing concepts identified? | **Yes, with source evidence.** | Each gap is tied to absence from candidate list/API use; no task prevalence is guessed. |
| Q4 — Search vs representation separated? | **Partially diagnosed; historical confounds identified.** | Full-inventory vs three-candidate scans, first-fit logic, parameter heuristics, and test-output coupling are documented. Causal separation still requires Phase 2B–2F. |
| Q5 — Representation bottleneck assessed? | **Yes: B2, moderate evidence as leading hypothesis; root cause unresolved.** | Low bounded coverage is strongly observed; primary-cause attribution is not. |
| Q6 — Alternative comparison condition defined? | **Yes, specified; not implemented.** | R0 corrected reference, R1 object-centric relation representation, and HCC positive control requirements are frozen here; Phase 2B–2F must build/test them. |

## Phase 2A readiness gates

| Gate | Status | Evidence |
|---|---|---|
| R1 — Representation inventory | **PASS — source-complete audit** | `primitive_inventory.csv` covers 10/10 Phase13G solution programs plus auxiliary features/helpers/trace operations. |
| R2 — Coverage measurement exists | **PASS — operational definition and historical outputs; isolation caveat** | Demo-fit to training demonstrations is separate from test accuracy as a field; historical `coverage_scan()` also computes test accuracy in the same solver call. |
| R3 — Expressivity analysis | **PASS — inventory mapped** | `expressivity_matrix.csv` states what each primitive can/cannot express and labels bounded evidence vs missing features. |
| R4 — Search interaction audit | **PASS — retrospective diagnosis; historical protocol defect remains** | First-fit and parameter limits documented; config=3 vs discovery default=10 is an unresolved historical mismatch. |
| R5 — Alternative condition | **PASS — specified only** | `representation_requirements_v2.md` defines R0, R1, HCC, and matched factorial comparison; no condition implemented yet. |
| R6 — Representation hypothesis falsifiable | **PASS — prospective hypotheses and discriminating results defined** | Assessment states outcomes that would support/reject representation-primary explanation, including coverage-improves/invariants-still-fail. |

## Phase 2 overall readiness snapshot (R1–R10)

This is a status audit, not an assertion that Phase 2A completes later work.

| Phase 2 gate | Historical/2A status | Readiness meaning |
|---|---|---|
| R1 — Representation inventory | **PASS, audit scope** | Phase13G language documented; alternative representation remains to implement. |
| R2 — Coverage independent of accuracy | **PARTIAL** | Metric defined from demo fit, but historical execution path computes test accuracy in `solve_task()`; coverage-only sealed runner remains required. |
| R3 — Budget integrity | **FAIL in historical 13G; unresolved** | Frozen config says three; discovery searches ten; arms search three; full scan ten. No correction or rerun in 2A. |
| R4 — Trace generation threshold/readiness | **FAIL for sufficient successful substrate; not a scientific success threshold** | 600 trace records exist, but only 3 successful demo-fit traces among 600 under ten-program discovery. This is a readiness floor issue, not “ASFT failed” as a causal theory conclusion. |
| R5 — Invariant candidate availability | **FAIL historically** | Zero accepted candidates under frozen support rules; no SCT/transfer test can proceed from this pool. |
| R6 — Support-denominator integrity | **PARTIAL / needs code contract** | Aggregate transfer precision is null at denominator 0; per-program `transfer_score` becomes numeric zero when applicability is zero. Future code must preserve denominator 0 and `unavailable` consistently. |
| R7 — Holdout integrity | **FAIL for pristine independent confirmation** | Attempt 02 reused same holdout after attempt 01 generated predictions in memory; no new holdout used in 2A. |
| R8 — Representation alternative or high-coverage reference | **PENDING** | Specified as R1/HCC in 2A; no actual alternative/high-coverage condition has been run. |
| R9 — Failure localization | **PARTIAL** | Stage cascade is documented, but hardcoded trace-valid flag, mislabeled successful-trace prefix count, and search/representation conflation remain. |
| R10 — ARC Foundation Ready | **BLOCKED** | Multiple prior gates are unmet; Phase 2A is an audit completion, not permission for Phase 10-style confirmatory ARC testing. |

## Central assessment

> Phase 13G strongly demonstrates that the **deployed bounded ten-program representation** had very low exact demonstration-fit coverage and did not supply a repeated candidate pool. Phase 2A moderately supports representation as a leading upstream bottleneck hypothesis. It does not establish representation as the unique or primary root cause, and it does not show that a richer representation will make ASFT work.

Most importantly, Phase 2A specifies a genuinely falsifiable alternative: if coverage and trace diversity improve but invariants remain absent under frozen support rules, the “representation caused everything” explanation weakens. If coverage is low under R0 but rises under R1 at the same search/resource budget, the representation hypothesis gains support. If a search-only change recovers candidates with R0, search is implicated. These future comparisons must be preregistered and use separate coverage and sealed-accuracy paths.

## Exit decision

**Phase 2A: PASS for representation audit completion.** The bounded representation, expressivity, missing concepts, historical coverage, search interactions, bottleneck grade, and alternative-condition requirements are documented. **Phase 2 remains in progress.** Budget, trace-support, candidate, denominator, holdout, alternative implementation, and failure-localization readiness gates remain open. No ARC mechanism confirmation is authorized by this phase.