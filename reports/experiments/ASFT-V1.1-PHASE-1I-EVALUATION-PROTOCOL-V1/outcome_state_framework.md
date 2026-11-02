# Phase 1I — Five-State Outcome Framework (Additional Required Section)

Every benchmark claim and every primary comparison returns exactly one state. State is assigned under the preregistered primary endpoint, effect direction, SOI, independent unit, uncertainty procedure, missingness rule, and integrity/activation checks. State thresholds cannot change after outcomes.

| State | Meaning | Required handling |
|---|---|---|
| **Supported** | Valid, informative evidence meets the registered criterion for the claim (e.g. full interval beyond the meaningful-effect SOI; or a registered equivalence hypothesis has an interval wholly within SOI). | State exact claim scope, endpoint, effect/interval, N independent units, denominators, and required replication. |
| **Contradicted** | Valid, informative evidence rules out the registered meaningful claim or supports its registered opposite. For positive superiority, a CI entirely below the minimum meaningful benefit contradicts that superiority claim; it does not prove the mechanism can never help. | Keep the failed gate and negative result. Identify direction and scope; no posthoc rescue by another endpoint. |
| **Inconclusive** | Data are valid and informative, but the interval crosses a decision boundary, independent-unit precision is insufficient, or confirmatory/replication findings conflict. | Report effect/interval and what would be needed to resolve uncertainty. Do not call it a tie or failure. |
| **Unavailable** | A valid estimate cannot be formed or interpreted: endpoint/denominator absent, required data missing, integrity/fairness failure, prespecified missingness gate exceeded, or measure masked by design. | Explain exact unavailable stage/reason. Never impute zero or treat as a failed outcome. |
| **Non-informative** | A measurable comparison exists, but does not identify the claimed contrast: identical decisions/selections, no meaningful activation/choice opportunity, or degenerate benchmark pressure for that mechanism. | Report descriptive scores separately; do not claim win, tie, equivalence, or null mechanism effect from the non-informative contrast. Redesign only in a new prospective E1/E2/E3 protocol. |

## Decision order

1. **Integrity and availability:** if outcome is absent or protocol/fairness/data integrity fails, state `unavailable`.
2. **Identifiability/activation:** if the mechanism contrast had no decision divergence or opportunity, state `non-informative` for that mechanism claim.
3. **Statistical informativeness:** use registered independent-unit minimum, endpoint, denominator, missingness strategy, multiplicity, effect interval, and SOI.
4. **Claim classification:** assign supported/contradicted/inconclusive under the frozen hypothesis mode.
5. **Replication/generalization:** combine E3/E4 only under the registered synthesis plan; single positive E3 cannot support a generalization claim.

Where a score endpoint is observed but a component-selection contrast is degenerate, report both facts: e.g. “endpoint score X was measured; the selection-mechanism comparison was non-informative because both policies selected the same set.” Do not use one state to hide the other.

## Directional superiority rule (generic template)

Let effect be ASFT minus comparator, `δ` the frozen SOI, and `[L,U]` the registered uncertainty interval. For a positive-superiority claim:

- `supported` if `L > δ`;
- `contradicted` if `U < δ` (the registered meaningful benefit is ruled out);
- `inconclusive` otherwise.

For opposite-direction, equivalence, or noninferiority hypotheses, use their preregistered symmetric rules. This logic is a framework; each study must set its own justified SOI and method before outcomes. Exact tie with zero variance does not automatically mean equivalence; identical decisions yield non-informative status for the mechanism claim.