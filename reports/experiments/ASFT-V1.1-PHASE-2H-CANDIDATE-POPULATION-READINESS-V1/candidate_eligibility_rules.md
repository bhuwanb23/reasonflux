# Phase 2H.3 — Candidate Eligibility Rules

## Candidate-layer scope decision

For the existing Phase 1C RQ1 benchmark, the ranked unit is an **outcome-blind invariant candidate** emitted by the trace-mining candidate-generation layer as an `Invariant` object. Raw fragments, mined patterns, structures, skill candidates, skills, capabilities, and ARC program-search hypotheses are not interchangeable candidate units. Ranking any of those instead would define a different benchmark and require an explicit protocol amendment (F3), not an implementation shortcut.

## Proposed benchmark eligibility contract

The following separation is required to avoid circular eligibility:

1. **Object/source:** a candidate must be an accepted `Invariant` proposal from the frozen production candidate-generation pipeline, with source trace/task lineage and generator/version identifiers.
2. **Pre-outcome construction:** generation, identity, deduplication, and structural eligibility use discovery/calibration material only. Hidden future value, held-out task labels, oracle values, and future transfer outcomes cannot determine candidate inclusion.
3. **Structural evidence:** the candidate has the frozen recurrence/support, stability, and cross-family evidence required by the selected policy version and has passed its generation rejection rules. Thresholds must be pinned to one version/config; they are not adjusted after observing yield or pressure.
4. **Feature eligibility:** all required comparator features have documented source, denominator, split, missingness status, and hash. An observed zero is retained as zero; unavailable measurement is NA with a reason and makes the affected policy/panel unavailable—never imputed.
5. **Transfer-neutral pool entry:** candidate inclusion must not require positive **future** transfer or future utility. A candidate with observed calibration opportunities and transfer score T=0 remains eligible; a candidate with no eligible calibration opportunities has T unavailable, not zero. Otherwise R1 would be tested on a pool preselected for its outcome.
6. **Identity/deduplication:** use a frozen canonical identity rule; keep source lineage/family evidence as attributes. Current `InvariantIdentity` hashes normalized origin and operation signature but omits family from the fingerprint. That can merge the same operation string across families; its suitability must be reviewed before a new pool is built.
7. **No downstream substitution:** skill intake/promotion and capability construction occur after invariant validation. They are not candidate eligibility rules for R1 ranking.

## Current rule/config discrepancies

The conceptual candidate layer is clear, but a single executable eligibility policy is not yet frozen across the audited paths:

- Phase 2D reports the audited ARC mining support floor as 5, consistency 1.0, and at least two task families; observed maximum distinct-task support was 3.
- The generic `InvariantPolicy` source default uses `min_frequency=3`, `min_consistency=0.6`, and two families, while Phase 2E explicitly evaluates relaxed support 2, current support 5, and strict support 6.
- `QUALIFICATION_RULES` also includes transfer utility; downstream promotion requires transfer/reasoning gates. The RQ1 benchmark, however, must retain transfer-poor candidates with observed T=0 and must not condition pool membership on held-out future transfer. Candidate generation, structural validation, transfer verification, and skill promotion therefore need distinct status fields.

**Phase 2H freezes the candidate-object boundary and no-future-outcome rule, but does not claim the numerical policy/config has been frozen for a future execution.** Before creating candidates, the owner must select/hash one admissible config, reconcile the active code defaults and actual-run config, and document whether the candidate set is at pre-transfer-validation or a later state. No threshold changes are authorized by this audit.

## Current status

No saved ARC object passes the proposed contract: the accepted candidate count is zero. These rules define how a future valid population should be audited; they do not retroactively convert the rejected relaxed proposals into eligible invariants.