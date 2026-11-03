# Future Experimental Protocol Design — Not Authorized

This is a protocol-design document only. It is not a preregistration, split assignment, run approval, or permission to access confirmatory or hidden outcomes.

## Research estimands

- **Primary end-to-end:** intention-to-treat difference in official ARC-AGI-3 score between invariant+counterexample treatment and specified controls over the full assigned cohort.
- **Claim N:** incremental predictive/behavioral/end-to-end value of invariant representation beyond strong replay under matched resources.
- **Claim B:** difference in boundary quality when counterexample information is included versus withheld, with candidate-generation evidence otherwise fixed.
- **Claims C/D:** negative-transfer incidence and overall outcome change; report them separately. Avoid post-treatment conditioning on “skill invoked” as a causal estimate.

## Candidate arms

- No learned skills.
- Raw trace/script replay.
- Strong parameterized/compressed replay.
- Simple recurrence-based skill creation.
- Invariant-derived skills without counterexample boundary updates.
- Full invariant + counterexample boundary method.

Do not run every arm if an arm cannot be specified and budget-matched. Any exclusions must be justified before outcomes.

## Matching and assignment

Freeze model/checkpoint, prompts, tool/runtime, observation representation, memory and context budgets, action/time/compute budgets, game order, reset policy, evaluator version and seeds. Use paired game/level starts only where official rules and environment permit. Do not assume arbitrary state forking. If exact replay is unavailable, causal estimates remain episode-level.

## Data and leakage

Specify permitted source experience and target evaluation material by track-specific manifest. Keep source traces, candidate construction, validation, and held-out evaluation distinct. No hidden/test outcomes or private leaderboard feedback for threshold tuning. Do not assign a confirmatory split until authorized under the existing project constraints. Log every attempted episode, including failures and timeouts.

## Outcomes and units

- Primary: official ARC-AGI-3 evaluator score.
- Secondary: actions to progress/completion; levels completed; per-game scores; skill generation/verification cost; tokens/wall time; prediction errors; abstention; negative transfer; fallback.
- Unit: game/episode or a justified paired level; individual actions are not independent samples.
- Report denominators, missingness, and per-game variation. Do not use a custom composite as a substitute for the official score.

## Decision and falsification

The protocol must state minimum meaningful effect, uncertainty method, regression guardrail, multiplicity handling, exclusions, sample size and analysis script before any confirmatory run. These values remain `UNSET`. Support each claim only from its own outcome; a result for A cannot stand in for B–E. If a requirement cannot be met, label the study exploratory/inconclusive, not confirmatory.
