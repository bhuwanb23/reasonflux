# Phase 2A.7 — Representation Bottleneck Assessment

## Overall classification

**B2 — Moderate evidence that representation is a leading bottleneck hypothesis; representation as the primary causal root remains unresolved.**

This single ordinal rating is deliberately more cautious than the direct implementation finding. The **bounded 13G representation's low coverage** is strongly evidenced. The claim that representation, rather than search, candidate order, parameter inference, support thresholds, task distribution, or downstream mechanism behavior, is the *primary cause* is only moderately supported and not causally isolated.

## Evidence ladder

| Claim | Evidence grade | Basis |
|---|---|---|
| The deployed Phase 13G solution language is narrow and fully inventoried here. | **Strong** | Ten fixed whole-grid programs; helper/feature layer distinguished from candidates. |
| This bounded language/search found very few exact demonstration fits. | **Strong, descriptive** | Full scan: 3/600 discovery, 5/200 transfer, 2/200 holdout. `unsupported_v1` means no fit within this bounded implementation. |
| Low successful trace diversity prevented the frozen invariant pool from meeting support. | **Strong, direct pipeline explanation** | Three successful discovery programs, each supported by one task; minimum support is five; zero accepted invariants. |
| Representation limits are a plausible upstream cause of the no-activation cascade. | **Moderate-to-strong** | Candidate language omits explicit object, count-rule, grouping, relation, composition, and pattern-completion programs; observed fit rate is low. |
| Representation is the sole/primary reason for ARC failure. | **Unresolved** | Discovery budget mismatch, first-fit search, heuristic parameter inference, support gates, and no alternative condition confound attribution. |
| A richer representation will produce more coverage or invariants. | **Untested** | No alternative representation/reference high-coverage comparison exists. |
| Downstream ASFT mechanisms fail even when coverage/support are adequate. | **Untested by 13G** | Upstream trace/invariant pool never activated sufficiently; transfer/capability claims are unavailable rather than meaningfully negative. |

## Two distinct conclusions

1. **Implementation adequacy:** the Phase 13G bounded ARC implementation was not an adequate substrate for testing the invariant→skill→transfer→capability chain on these splits. This is a negative readiness finding for that implementation.
2. **Theory-level attribution:** the saved evidence does not show that representation alone caused the failure, nor that changing representation would validate IDT/SCT/transfer/CGM. That remains a falsifiable hypothesis.

## What remains unexplained by representation alone

- Why the first demo-consistent candidate fails test where it does; the search does not retain all alternatives.
- Whether a candidate exists within the ten programs but is missed by parameter inference or budget/order; candidate fit sets were not fully retained.
- Whether invariant support thresholds are appropriate when exact-fit support is sparse; threshold sensitivity was not tested as a separate, preregistered factor here.
- Why B2 memory can solve one transfer/holdout case while the learned ASFT chain does not activate; memory is a different mechanism and should remain a comparator.
- The exact contribution of the `KeyError: 'task_id'` report-serialization failure and same-holdout reuse; these are software/protocol issues, not representation effects.
- Whether exact task accuracy would rise under an alternative representation after matching search budget and candidate order.

## Falsifiable representation hypothesis for Phase 2

**H-R (representation-leading hypothesis):** Under the same ARC task IDs, demonstrations, test isolation, search algorithm, candidate/compute budget, support rules, and evaluator, a prospectively specified alternative representation will increase independently measured demonstration coverage and yield a richer repeated trace/candidate pool versus the corrected reference representation. This prediction does **not** require improved test accuracy; coverage, trace generation, candidate invariants, task accuracy, and downstream activation remain separate endpoints.

**Evidence against H-R / evidence for other bottlenecks:**

- If coverage remains low under materially distinct representations but improves under a search-only/budget/parameter-inference change, search is the stronger proximate explanation.
- If coverage and valid trace diversity rise above prespecified readiness thresholds but candidate invariants remain absent under frozen mining rules, the simple representation-only explanation is weakened; invariant formulation, miner configuration, or support thresholds become live explanations.
- If candidates/invariants activate but skills/transfer/capabilities do not, localize the failure downstream rather than citing representation by default.
- If a high-coverage reference condition cannot pass the same validation/scoring plumbing, protocol/evaluator integrity is unresolved.

These are future preregistered tests, not retrospective interpretations or targets for posthoc optimization.

## Interpretation ceiling

> **Phase 13G strongly demonstrates that its bounded ten-program implementation had extremely low exact-demo-fit coverage. It moderately supports representation as a leading upstream bottleneck hypothesis. It does not prove representation was the unique or primary causal root, and it does not show that a richer representation will make ASFT mechanisms work.**