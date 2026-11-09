# Venue landscape for an ARC claim-audit paper

**Prepared:** 2026-10-28  
**Purpose:** initial venue-fit assessment, not an endorsement or a submission decision.  
**Manuscript at issue:** an archived, retrospective audit of one ARC-motivated research cycle; no new ARC benchmark run; not a replication of published external papers; methodology novelty not established.

## Executive recommendation

The most natural *contribution family* is **AI evaluation methodology / empirical evaluation audit**, not a stand-alone “negative results” article. The best-matching venue surfaced in this search is the NeurIPS **Evaluations & Datasets (E&D) Track**: its 2026 call explicitly welcomes analysis and auditing of evaluation practices, claim interpretation, critical analyses, and submissions that need not introduce a new model or beat a baseline [NeurIPS E&D CFP](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets). However, the 2026 abstract and full-paper deadlines were **May 4 and May 6, 2026**; that cycle is closed. Treat it as a strong fit signal for a future call, not as an available current submission route.

**TMLR** is a possible rolling journal route if the manuscript is strengthened into a technically rigorous, broadly useful contribution. TMLR emphasizes technical correctness over subjective significance and uses rolling submissions, but a retrospective narrative without a sufficiently clear method, artifact, or reusable finding could still be judged too narrow [TMLR](https://jmlr.org/tmlr/).

**NeurIPS 2026 ML Reproducibility Challenge is not a fit as currently framed.** It requires reproducibility to be central and focuses on published ML claims; its TMLR eligibility/acceptance deadline (September 30, 2026) has passed. This project audits its own research cycle rather than reproducing a set of published external papers [MLRC 2026 CFP](https://neurips.cc/Conferences/2026/CallForReproducibility).

## Venue matrix

| Route | Topical fit | Current status (2026-10-28) | Fit judgment for this manuscript |
|---|---|---|---|
| NeurIPS Evaluations & Datasets | Excellent topic match: evaluation is explicitly treated as a scientific object; critical analyses, audits, and claim interpretation are in scope | 2026 cycle closed (May 4/6 deadlines) | Strongest future-cycle target **if** the paper adds a clearly articulated, reusable evaluation contribution and does not overclaim a field-wide gap. Check the next call when published; do not assume scope/deadlines will be identical. |
| TMLR | Good if claims are technically sound and useful beyond a single lab's archive; rolling review | Rolling submission process listed on official site | Plausible, but the current draft needs a stronger stand-alone contribution than “our ideas did not work.” A documented claim-ladder artifact, transparent audit trail, and a carefully bounded synthesis may help; novelty/impact is not guaranteed. |
| NeurIPS ML Reproducibility Challenge 2026 | Low-to-moderate: reproducibility and claim auditing are adjacent | Closed; TMLR acceptance by Sep. 30 required | Poor fit unless the work is redesigned around replication/generalizability of published external claims, which would be a different project. |
| NeurIPS 2026 Main Track—Negative Results type | The record contains a negative synthetic result and failures, but this is not the recommended framing | 2026 submission deadline passed | Do not use simply because there is an N-FAIL. The manuscript's strongest potential story is evaluation/claim audit; main-track negative-result standards may not match that contribution. |
| Future ARC/reasoning or evaluation workshop | Potentially good audience fit; workshop calls may welcome case studies and audits | No specific open call verified in this search | Reassess when actual 2027 calls appear. A workshop may be a realistic first venue for a bounded retrospective case study, but do not imply acceptance criteria before the call is published. |

## What a venue-ready contribution would need

1. **Define the object being evaluated.** Present the claim ladder (mechanism occurrence → task-relevant utility → incremental superiority → external generalization) as an analysis lens, not as a validated general framework.
2. **Show it changes interpretation.** Map each major archived claim to a comparator, estimand, evidence category, and claim ceiling; include concrete examples of ranking, skill creation, invariant-vs-replay, and prior-art termination.
3. **Demonstrate auditability.** Link immutable source records; distinguish primary outcomes from later synthesis; disclose one-run limits, synthetic scope, low ARC adapter coverage, and prior-art review boundaries.
4. **Engage existing ARC evaluation literature.** ConceptARC, controlled compositional-generalization studies, ARC Prize technical reports, and recent surveys already discuss conceptual evaluation, ablations, transfer, benchmark limitations, and evaluation reliability. Do not claim that ARC has no evaluation layer.
5. **Avoid a prevalence claim without a corpus study.** The current literature screen is purposive and cannot establish that “most ARC research evaluates systems rather than claims.”
6. **Explain reusability.** Provide a clearly anonymized/portable claim-evidence table or checklist only if it can be shared without altering or exposing immutable archive artifacts. Do not turn this into a new benchmark or experiment.

## Bottom line

**Recommended order:**

- Target the paper's substance at the evaluation-methodology audience; use the NeurIPS E&D 2026 scope as a model, but wait for a live future call.
- Consider TMLR only after the claim-ladder and audit package are made genuinely reusable and the related-work review is strengthened.
- Do not route it to a reproducibility venue unless the central research question changes to reproduction of published external claims.
- Do not present it as a generic negative-results paper.

No venue decision is final without a target call, page limit, anonymization requirements, artifact policy, and current deadline check.

## Sources

- NeurIPS 2026 Evaluations & Datasets Call for Papers: https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets
- NeurIPS 2026 Call for Reproducibility Papers: https://neurips.cc/Conferences/2026/CallForReproducibility
- Transactions on Machine Learning Research official page: https://jmlr.org/tmlr/
