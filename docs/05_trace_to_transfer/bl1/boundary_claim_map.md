# BL1-P0 — Boundary Claim Map

**Status:** P0 planning artifact; no empirical claim is supported. BL1 is terminated at P0 following the bounded prior-art review. No P1 or experiment is authorized.

## One claim chain only

> **Counterexamples → better boundary precision → maintained useful coverage**

| Link | Proposed meaning | Evidence required in a prospective test | Failure condition |
|---|---|---|---|
| **1. Counterexamples** | Given one fixed candidate skill and initial applicability boundary, the treatment receives labeled, independently identified cases where the skill was incorrectly permitted (false activations). The control is denied those labels; other data and resources are matched. | Auditable example provenance; frozen label rule; treatment/control exposure logs; evidence that only the allowed counterexample labels differ. | Counterexamples are selected or labeled using held-out outcomes, the arms receive unequal information/resources, or update lineage cannot be audited. |
| **2. Better boundary precision** | On contexts not used for fitting or updates, the treatment has higher applicability precision than the matched control. | Predictions committed before labels are revealed; paired per-context results; explicit TP/FP/abstention counts and uncertainty. | No meaningful improvement, an undefined precision caused by no activations, or an apparent gain caused by leakage or a changed comparator. |
| **3. Maintained useful coverage** | The precision improvement does not come from refusing nearly all contexts: the treatment retains an adequate fraction of truly applicable contexts. | Sensitivity/useful coverage, false activation rate, and all denominators reported with precision; a coverage floor frozen before evaluation. | The treatment falls below the predeclared coverage floor or suppresses activation so broadly that precision is uninformative. |

## Claim ceiling

Even a future pass on this chain would support only a bounded, domain-specific statement about counterexample feedback changing held-out applicability classification for the tested skill(s). It would not establish new capability, general transfer, intelligence growth, ARC performance, broad agent improvement, or Claims N/C/D/E.

## P0 decision

The mechanism and target are substantially covered by prior work on counterexample-guided refinement and, directly, learned option initiation sets from success/failure examples with explicit attention to set quality and useful coverage. Therefore this map is a record of the proposed one-chain hypothesis—not a novelty claim—and BL1 is terminated. No BL1-P1 is to be created.
