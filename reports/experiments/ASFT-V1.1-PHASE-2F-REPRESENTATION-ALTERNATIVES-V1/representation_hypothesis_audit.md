# Phase 2F.1 — Representation Hypothesis Audit

## Question and claim boundary

The hypothesis under audit is not “a richer representation is better.” It is: **under identical tasks, demonstrations, search policy/budget, evaluator, and downstream mechanisms, does a materially different representation increase found-fit coverage and cause more of the invariant→skill→transfer→capability chain to become eligible?** Phase 2F defines how to test this. It performs no new ARC comparison and does not establish representation as the primary cause.

## Evidence bearing on the hypothesis

| Phase | Evidence supporting a representation limitation | Evidence that limits a representation-only conclusion |
|---|---|---|
| **13G / 2A** | The deployed language is ten whole-grid programs, without explicit object selection, relational rules, or general composition. The all-ten scan found demo fits on 3/600 discovery, 5/200 transfer, 2/200 holdout. | Discovery used cap10 despite config3; scored arms use cap3; first-fit stops at the first demo fit; translation inference is heuristic. No alternative representation was tested. “No fit” is bounded, not semantic impossibility. |
| **2B** | The ten-program finite scan found 10/1,000 demo fits (1%). Trace records were valid, but invariants remained zero. | At cap3, 2/1,000 fit; eight additional fits appeared at larger caps. This demonstrates a search-budget effect within the current representation. |
| **2C** | S4 fullscan remains 10/1,000 (1%) on the fixed ten-program DSL. | With the same representation, demo fits rise 2→5→10 per 1,000 across S1→S2→S3/S4. Search allowance materially affects found coverage. S3/S4 are identical because the DSL has ten programs. |
| **2D** | Successful trace yield stays low (2/5/10/10 per 1,000); downstream invariant inputs are only 1/2/3/3 discovery traces. | Trace records are valid; failure after trace emission is not itself evidence of a representation defect. Generality beyond demos was not measured. |
| **2E** | Current support5 is unreachable with max observed support3; no production invariants emerge. | Support filtering is a separate downstream gate. Relaxed support reveals generic trace-control patterns, not semantic ARC rules. Therefore 0 invariants cannot be attributed to representation alone. |

## Current evidence grade

- **Strong descriptive evidence:** the deployed bounded representation plus its implemented parameter inference/search has low exact training-demonstration coverage on the audited task set.
- **Moderate support for representation as a contributing/leading hypothesis:** the inventory omits useful classes of object, relation, grouping, and composition operations.
- **Primary causal status:** **unresolved**. Search cap/order, parameter inference, task mix, parser quality, trace recurrence, support rules, and invariant formulation are not isolated by the historical comparison.
- **Alternative representation effect:** **unknown**. No alternative was implemented or compared.
- **Downstream counterfactual:** **unknown**. Existing data do not show whether a large coverage gain would activate invariants or whether failures persist downstream.

## What would support or weaken the hypothesis

- A paired, test-output-blind increase in found-fit coverage under a frozen alternative, with code/budget parity and independent replication, supports a representation effect on coverage.
- If coverage increases but repeated traces/candidate invariants do not, representation may be a **contributing** bottleneck while support/miner/semantic trace content remains limiting.
- If validated invariant candidates rise but skill/transfer/capability eligibility stays blocked, the failure localizes farther downstream.
- If the alternative fails to improve coverage, that weakens only that specified alternative under its declared search budget; it does not prove all richer representations are ineffective.
- A protocol, parser, search-budget, or adapter mismatch makes the contrast **unavailable**, not evidence against the representation.

## Decision

The representation hypothesis remains **falsifiable and unresolved**. Phase 2F freezes a comparison framework and explicit alternatives; it does not select a winning representation or estimate an ARC accuracy effect.