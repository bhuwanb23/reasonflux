# Phase 1I.2 — Experiment Classification Framework

Every experiment is assigned exactly one class before data collection/outcome access. Class is part of the preregistration, report header, dataset manifest, and analysis output.

| Class | Name | Permitted purpose | May support a primary scientific claim? |
|---|---|---|---|
| **E1** | Exploratory | Generate hypotheses, inspect failure modes, identify candidate measures/relationships. Outcome-informed adaptation is allowed but must be labeled. | **No.** E1 results are hypothesis-generating only. |
| **E2** | Development | Tune generators, representation, thresholds, costs, annotation, sample-size assumptions, software, or benchmark pressure using development data. | **No.** E2 outcomes cannot be relabeled as confirmatory. |
| **E3** | Confirmatory | Test a prespecified primary hypothesis and endpoint on protected, outcome-blind confirmatory data. | **Yes, conditionally.** Must pass preregistration, integrity, fairness, statistical, and reporting gates. |
| **E4** | Replication | Independently verify a frozen E3 estimand/protocol on new data, seeds, generator, domain, or external benchmark. | **Yes.** Independent replication is required for generalized claims. |

## Class assignment rules

1. Register the class, claim, data source, outcome access status, and permitted analyst access before collection or unblinding.
2. If outcomes have already been inspected or used to choose any protocol element, the work is E1/E2. It cannot be promoted to E3/E4 by writing a preregistration afterward.
3. A frozen E3 study can be followed by an E4 replication, but the replication must have a distinct manifest and independent source of experimental units. Reusing the same exposed holdout with a repaired reporter is not replication.
4. E4 must state its replication type: R1 within-generator, R2 cross-generator, R3 cross-domain, or R4 external benchmark. A changed estimand or protocol deviation requires a new study classification and disclosure; it is not a silent replication.
5. Exploratory secondary results inside an E3/E4 study remain exploratory unless their family, multiplicity, and decision rules were preregistered.
6. Contracts, unit fixtures, synthetic outcome vectors, smoke tests, and code-path simulations are software/specification evidence—not E3/E4 experiment outcomes.

## Class transition rule

No E1/E2 result may be promoted to E3/E4 evidence. Any post-outcome class change, endpoint/threshold/split change, or protocol correction remains versioned and posthoc; it requires a new, independent E3/E4 dataset to test the revised claim. Preserve the earlier result and class unchanged.