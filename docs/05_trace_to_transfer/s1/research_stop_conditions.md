# T2T-S1.5 — Research Stop Conditions

**ID:** `T2T-S1.5-StopConditions-v1.0.0-draft`  
**Purpose:** distinguish a claim failure from an invalid/inconclusive test and specify when not to build S2 or continue the T2T direction.

## Claim-level kill criteria

| ID | Condition | Decision |
|---|---|---|
| **K1 — N indistinguishable from replay** | I0 fails the S1.2 all-context exact-effect-accuracy criterion against competent, frozen R1-Max, or a valid comparison shows no positive increment. | Kill Claim N for the tested domain/conditions. If N is required by the minimum-claim package, do not proceed with the combined T2T thesis. Beating R0 but not R1-Max does not rescue N. |
| **K2 — No boundary improvement** | I1's counterexample-updated boundary does not reduce false activations on fresh contexts under the S1.3 measurement rule, or it does so only by rejecting applicable contexts/abstaining broadly. | Kill Claim B for the tested domain/conditions. Do not call mere guard mutation “learning” or “improvement.” |
| **K3 — Boundary change does not reduce harm** | A later valid study shows better boundary classification but no predeclared reduction in harmful transfer/negative transfer. | Kill the harm-reduction link (Claim C); retain B only as a boundary-measurement result if B itself meets its rule. Do not equate false-activation reduction with lower task-level harm. |
| **K4 — Costs erase value** | Under a prospectively frozen cost vector/cap/frontier, no relevant operating point provides the required mechanism value within the accepted resource envelope. | Stop the proposed full method at that envelope. Do not construct an after-the-fact weighted utility to justify it. A narrower low-cost hypothesis would need a new pre-outcome decision. |
| **K5 — Not observable / not identifiable** | The state/action/effect fields required to distinguish the relation or boundary are unavailable, ambiguous, hidden, or not reliably adjudicable under the permitted observation interface. | Mark the claim BLOCKED/UNMEASURABLE for that domain. Do not impute hidden state or use evaluator outcomes to reconstruct it. Stop until a lawful observable representation is prospectively justified. |
| **K6 — Replay subsumes the distinction** | A competent replay/compiler stress test reproduces I0's predictions under the same information and resources, or the proposed invariant is only a re-description of a macro/slot rule. | Kill invariant-specific Claim N unless a different, independently specified observable increment is proposed before new outcomes. Do not relabel the baseline after the result. |
| **K7 — No defensible contribution after prior art** | The only positive result is a generic counterexample-to-guard refinement already covered by P1's prior-art review, with no novelty-cleared comparative contribution. | Do not present a method-novelty paper. Reframe as a bounded empirical comparison only if independently justified; otherwise stop paper development. |

## Stop, hold, and inconclusive are different

- **STOP / KILL:** a valid, interpretable test contradicts the predeclared claim criterion, or the program-level minimum outcome is not met.
- **HOLD / BLOCKED:** essential observations, permissions, baseline implementation, or design decisions are missing. Do not call this a scientific failure or proceed as if the condition were satisfied.
- **INCONCLUSIVE:** the test is valid but uncertainty/coverage is insufficient to decide the frozen criterion. Do not switch metrics, relax the claim, or expand the cohort after viewing outcomes without a new prospective version and authorization.
- **INVALID:** leakage, outcome-informed tuning, broken data-role separation, baseline mismatch, or integrity failure prevents interpretation. Preserve the record; do not count it as either success or clean falsification.

## Program-level gate

A future S2 proposal may be considered only after:

1. the owner accepts/revises the S1.1 O1–O4 minimum-claim package;
2. the S1.2 endpoint and the toy world's role/limitations are accepted;
3. the replay definition and competence-review plan are frozen;
4. relevant observability and outcome/source separation are demonstrable using synthetic-only inputs;
5. any numerical cost limits and later inferential criteria are prospectively resolved rather than guessed; and
6. a new, explicit S2 scope is authorized.

Suggested decision: proceed to S2 only if at least one central claim has a plausible, observable test and the minimum-claim package permits a publishable narrow outcome. N and B must remain separately evaluated. If both fail, terminate this direction. If only B appears promising, resolve novelty independently before building a boundary-only method.

S2 authorization, if later granted, would still be synthetic-only and would not authorize ARC-AGI-3 data, tasks, splits, evaluators, benchmark claims, paper submission, or competition activity.
