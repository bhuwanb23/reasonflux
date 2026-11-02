# Phase 1D.3 — Challenge Family Specification

Each family tests a distinct relationship between prior experience and future structure. Families A–F must appear in both confirmatory and replication splits. Scenario expectations are design hypotheses, not observed results; every arm is scored on the same held-out instances.

| Family | Construction | Primary question / expected pressure |
|---|---|---|
| A — Exact Replay | A task is repeated according to a preregistered train/test pair generator. The training demonstration may contain its solution; the held-out query is otherwise unmodified. | Positive control: M1 exact memory should be sufficient and may beat abstraction on net cost. This is an explicit exposure treatment, not an accidental leakage. |
| B — Context Shift | The underlying rule is unchanged while surface/context features are transformed; no exact test key or answer is stored. | Tests whether abstraction preserves the rule while episodic matching degrades. M2/M3 remain meaningful memory comparators. |
| C — Composition Shift | Two or more learned rules must be composed in a new order/combination; the task includes a case-specific parameter available only in a permitted partial training fragment. | Tests whether M4 can compose and whether M5 can combine the abstract rules with the episodic parameter. No complete composite answer exists in training. |
| D — Structural Analogy | A relation/graph structure is preserved while the surface symbols and layout change; test family instances are disjoint. | Tests rule-level structural transfer vs surface-pattern retrieval. |
| E — Far Transfer | No exact or near exemplar exists in memory; the held-out family is novel but uses a rule/relational primitive learned in development. | Tests generalization beyond nearest-neighbor memory. The rule must be independently specified, not inferred from test labels. |
| F — Adversarial Memory | A high-similarity training decoy suggests a wrong output, while the true held-out task follows a distinct structural rule. | Tests retrieval precision, abstention, and whether abstraction/hybrid verification can reject a lure. No hidden answer is placed in the lure. |

## Factorial challenge strength and transition curve

Within B–F, vary the amount of exact recurrence and context transformation on a fixed, predeclared grid: exact-repeat probability `p ∈ {0, .25, .50, .75, 1.00}` and transformation level `s ∈ {0,1,2,3}`. Task-family definitions and grid are frozen using development data. The confirmatory and replication splits include every family; transition curves are reported only within the predeclared grid. If no crossover occurs, report “no crossover in tested range”; do not extrapolate.

## Outcome independence

The generator fixes latent rules and task transformations before any system acts. Gold outputs are computed from the task program and stored outside policy state. Systems see only inputs and their permitted stores. The evaluator joins outputs to gold after each run is sealed. This makes family structure a predeclared treatment, not a category assigned from observed arm success.

## Scope warning

These are challenge-family specifications. No held-out task generator, solver, or confirmatory outcomes were executed in Phase 1D design work. The qualitative expected winners must be tested by a later development harness and then by untouched confirmation/replication data.