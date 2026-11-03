# Terms and Decisions — T2T

This is the working vocabulary for the idea-stage documents. Ambiguities must be resolved before any protocol is frozen.

## Core objects

- **Interaction trace:** ordered permitted observations, actions, observed transitions/effects, costs, and provenance for a run.
- **Candidate invariant:** a falsifiable relation over normalized state/action/effect evidence that is proposed to recur across contexts. A frequent string or operation label alone is not an invariant.
- **Counterexample:** a sourced observation/transition that contradicts the candidate’s predicted effect under its current preconditions. Record it; do not silently drop it.
- **Applicability boundary:** the observable condition set under which a candidate’s predicted behavior is supported. It may be narrow or uncertain; abstention is valid.
- **Skill:** versioned executable conditional procedure derived from an invariant, with parameters, preconditions, expected effects, termination/fallback, and evidence lineage.
- **Replay baseline:** uses source traces/scripts without the proposed cross-context invariant and counterexample-based boundary mechanism. Raw and strong parameterized/compressed variants must be specified separately.
- **Negative transfer:** a skill invocation that causes a preregistered harmful deviation relative to its matched control, such as avoidable extra actions, lost progress, invalid execution, or lower outcome.

## Evidence labels

- **Observed:** directly present in an allowed interaction log.
- **Inferred:** hypothesis derived from observed events.
- **Predicted:** frozen expectation produced before an action/target outcome.
- **Counterexample:** observed event inconsistent with the current prediction under stated conditions.
- **Outcome:** evaluator-provided result, stored separately and unavailable to the earlier creation/promotion decision.

## Decisions still open

1. State abstraction / object correspondence for ARC-AGI-3.
2. Whether a candidate must recur across levels, games, or both.
3. How to distinguish noise, unobserved preconditions, and true invariant falsification.
4. Minimum positive and negative evidence; no thresholds are set here.
5. Whether candidate skills are deterministic macros, conditional policies, or small predictive programs.
6. How to compare “same state” counterfactuals when the official environment cannot fork a game.
7. How to separate action-efficiency score from tokens, wall time, and skill-construction cost without an arbitrary composite.

These decisions are design questions, not permission to inspect hidden outcomes or to start a run.
