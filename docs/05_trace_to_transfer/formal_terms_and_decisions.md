# Terms and Decisions — T2T

This is the working vocabulary for the idea-stage documents. P2 object semantics are specified in [`formal_skill_object.md`](formal_skill_object.md) and its [versioned P2 packet](p2/README.md); P3 replay arms/Claim N controls are defined in the [fair replay contract](p3/fair_replay_controls_v1.md); P4 candidate/triage/refinement semantics are defined in the [boundary algorithm contract](p4/boundary_algorithm_v1.md). Remaining ambiguities must be resolved before any protocol is frozen.

## Core objects

- **Interaction trace:** ordered permitted observations, actions, observed transitions/effects, costs, and provenance for a run.
- **Candidate invariant / CandidateVersion:** a non-executable, falsifiable relation over normalized state/action/effect evidence, pinned to a representation/language version and evidence snapshot. A frequent string or operation label alone is not an invariant.
- **SkillVersion:** an immutable executable conditional specification derived from a specific CandidateVersion; it adds typed parameter bindings, observable applicability predicates, prospective effect prediction, policy artifact, termination/fallback, and derivation evidence. Schema validity is not validation, novelty, or run authorization.
- **EvidenceSnapshot:** immutable, purpose-specific ordered references to permitted source events, each labeled by evidence class and role; new evidence yields a new snapshot rather than mutation of old evidence.
- **LifecycleEvent:** append-only, evidence- and policy-linked status transition for one candidate/skill version. Status is derived from events, not overwritten in semantic content.
- **Dynamics counterexample:** a sourced observation/transition that contradicts a predicted effect under a fixed state/action model; this challenges the dynamics hypothesis.
- **Scope counterexample:** a correctly classified event showing that a skill’s applicability guard admitted a context in which the skill’s predicted behavior was invalid. This can motivate guard review/refinement, but does not by itself prove the invariant is false; hidden state, perception, action execution or an incomplete condition may explain the mismatch. Preserve event provenance and classification; do not silently drop it.
- **Counterfactual activation evidence:** matched skill/no-skill outcomes or invoke/skip branches estimating whether activation helps. This is an activation-utility signal, not automatically a dynamics or scope counterexample. SkillApt and SelSkill are direct prior work in this category; see the P1 packet.
- **Applicability boundary:** the observable condition set under which a candidate’s predicted behavior is supported. It may be narrow or uncertain; every required predicate evaluates TRUE, FALSE, or UNKNOWN; UNKNOWN requires abstention.
- **Replay baseline:** uses source traces/scripts without the proposed cross-context invariant relation. Raw and strong parameterized/compressed variants must be specified separately and given the same source experience/resources.
- **Negative transfer:** a skill invocation that causes a preregistered harmful deviation relative to its matched control, such as avoidable extra actions, lost progress, invalid execution, or lower outcome.

## Evidence labels

- **Observed:** directly present in an allowed interaction log.
- **Inferred:** hypothesis/annotation derived from observed events, with method and provenance.
- **Predicted:** frozen expectation produced before the target action/event.
- **Counterexample:** append-only observed event assessed against a pinned prior prediction and conditions; classify as dynamics, skill-scope, execution/observation error, outcome-only, or unresolved. Never use an unresolved mismatch to narrow the guard.
- **Counterfactual activation:** matched WITH/WITHOUT or invoke/skip utility evidence; it is not itself a transition/scope counterexample.
- **Outcome:** evaluator-provided result, stored separately and unavailable to earlier candidate formation, promotion, or threshold selection.

## Decisions still open

1. State abstraction / object correspondence for ARC-AGI-3.
2. Whether a candidate must recur across levels, games, or both.
3. How to distinguish noise, unobserved preconditions, and true invariant falsification.
4. Minimum positive and negative evidence; no thresholds are set here.
5. Whether candidate skills are deterministic macros, conditional policies, or small predictive programs.
6. How to compare “same state” counterfactuals when the official environment cannot fork a game.
7. How to separate action-efficiency score from tokens, wall time, and skill-construction cost without an arbitrary composite.
8. Whether a defensible contribution remains after direct comparison to SkillApt-style outcome-conditioned activation, BASM-style boundary records, counterexample-qualified guard refinement (#6645), and ARC world-model repair. P1 recommends no-go on the current standalone novelty claim; the owner selected the comparative reframe direction on 2026-11-03, but the residual contribution remains unresolved and not novelty-cleared.

These decisions are design questions, not permission to inspect hidden outcomes or to start a run.
