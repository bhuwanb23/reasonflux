# Phase 2C.7 — Search vs Representation Assessment

## Competing hypotheses

| Hypothesis | Evidence from Phase 2B/2C | Assessment |
|---|---|---|
| **H1 Representation bottleneck** | Even the all-ten finite scan finds exact demo fits on only 10/1,000 tasks; no repeated discovery signature reaches support five. | Consistent with a severe bounded representation/inference ceiling, but not isolated from parameter heuristics or task distribution. No richer representation was tested. |
| **H2 Search bottleneck** | With identical DSL, demos, order, and inference, coverage rises from 2/1,000 at cap3 to 5/1,000 at cap6 and 10/1,000 at all ten. Eight fullscan-found tasks are absent under S1. | Supported for found-fit coverage within the current ten-program implementation. Candidate order and allowance demonstrably affect discovery. |
| **H3 Mixed bottleneck** | Increased search recovers fits, but fullscan stays at 1%; successful discovery signatures remain singleton and TraceMiner returns zero invariants. | Best description of observed *pipeline attrition*: both budget/order and bounded coverage/support limits are visible. |
| **H4 Unresolved** | No factorial comparison with a richer representation, alternative parameter inference, candidate ordering, or high-coverage positive control; no test accuracy. | Primary causal attribution remains unresolved. H4 applies to the causal/root-cause question even while the local budget effect is measured. |

## What has been separated

For the C1 found-fit endpoint, the budget contrast is paired and controlled: same task demonstrations, unchanged Phase 13G candidate inventory and parameter code, fixed order, and exact-fit definition; candidate allowance alone changes. Thus the *within-implementation effect of candidate cap on found demo fits* is measured. The search trace logs further distinguish candidates generated, evaluated, omitted by budget, and skipped after first fit.

The representation effect is **not** causally separated. “Fullscan” searches all ten programs but does not expand the representation, parameter inference, or compositional depth. No-fit remains a bounded-search outcome. The score curve cannot identify what a richer scene representation, relational DSL, alternative inference, or different support threshold would do.

## Attribution decision

**F5 / H3 — mixed observed bottleneck pattern; F6 / H4 — root cause unresolved.** Search limits plausibly suppress some coverage. The low all-ten coverage and absence of repeated traces prevent downstream invariant activation. Neither observation establishes a single primary cause, and ARC coverage failure is not theory success or theory failure.

## Prospective discriminating design

A future preregistered comparison should cross:

- **Representation:** R0 unchanged Phase 13G bounded DSL versus a specified richer, object/relational representation.
- **Search:** matched caps/order policy (e.g. 3, 6, all available unique candidates), with equal compute/time/memory rules and candidate-trial accounting.
- **Plumbing control:** a high-coverage control that proves trace→invariant→skill interfaces can activate without changing outcome labels.
- **Outcomes:** training-demo coverage and each C1–C7 stage via test-blind runner; accuracy only in a separate sealed and independently authorized evaluation.

Pre-register candidate generation, parameter inference, trace construction, support thresholds, resource budgets, task splits, and condition allocation. Hold representation and search changes in separate factors. If more search raises coverage within R0 but R1 adds further coverage at matched budgets, both factors contribute. If R0 flatlines while R1 rises, evidence favors a representation contribution. If coverage rises but invariant activation remains absent, representation alone is insufficient. If both remain low, causal interpretation remains unresolved.