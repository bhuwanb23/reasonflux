# BL1 Claim Map v1 — Draft

**Status:** hypothesis map only; no claims supported by BL1 evidence.  
**Scope:** counterexample-guided applicability-boundary quality. Claims N, C, D, and E are outside this map.

| Claim | Current status | Candidate evidence needed | Failure condition / ceiling |
|---|---|---|---|
| **BL1-P (primary): Counterexample feedback improves held-out applicability precision while preserving useful coverage.** | **Untested.** S2 has one toy-fixture observation only (false activations 2/4→0/4; coverage 2/2). | Prospective matched comparison of the same candidate skill and initial boundary with versus without counterexample-label updates, evaluated on a frozen held-out suite. Report precision, useful coverage/recall, false activations, missed valid applications, abstentions, and full denominators. Freeze the coverage floor and precision criterion before held-out exposure. | No precision benefit; coverage falls below the predeclared useful-coverage criterion; gain comes from suppressing nearly all activations; or any post-outcome tuning/leakage. The S2 fixture alone does not establish BL1-P. |
| **BL1-M (mechanism, descriptive): Counterexample updates change the applicability boundary in the intended direction.** | **Untested.** | Log versions, source lineage, accepted/rejected counterexamples, and boundary changes; confirm updates are based only on permitted counterexample evidence. | Boundary changes are not reproducible, use hidden state, or cannot be linked to the counterexample records. This is mechanism audit evidence, not a substitute for BL1-P. |

## Metric definitions proposed for review

For held-out contexts with a known applicability target:

- `TP`: applicable context correctly permitted for activation.
- `FP`: inapplicable context permitted for activation (false activation).
- `FN`: applicable context rejected/abstained.
- `TN`: inapplicable context correctly rejected.
- Applicability precision: `TP / (TP + FP)`; undefined if no activations are issued.
- Useful coverage candidate: `TP / (TP + FN)` (recall over truly applicable contexts), reported alongside the all-context activation/abstention counts.

These definitions are candidates, not frozen metrics. The owner must decide whether this is the intended meaning of “useful coverage,” select a prospective coverage floor and any meaningful-effect criterion, and freeze the analysis before any held-out exposure. No values are supplied here.

## Claim boundaries

- No claim about predictive effects beyond replay, negative-transfer reduction, action efficiency, or end-to-end performance follows from BL1-P.
- No ARC-AGI-3 or publication claim follows from a synthetic result alone.
- Any future claim must state its domain, estimand, comparator, budget, and generalization ceiling explicitly.
