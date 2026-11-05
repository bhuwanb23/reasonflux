# Counterexample-Guided Boundary Algorithm — P4 Entry Point

**Status:** reconciled to [`T2T-P4-Boundary-v1.0.0-draft`](p4/boundary_algorithm_v1.md), complete for documentation/design scope only. It is not code, a candidate-generation result, validation, or run authorization.

## Contract summary

The normative design is [`p4/boundary_algorithm_v1.md`](p4/boundary_algorithm_v1.md); synthetic edge cases are in [`p4/decision_fixtures.md`](p4/decision_fixtures.md). P4 uses the [P2 formal object contract](formal_skill_object.md) and [P3 fair replay contract](p3/fair_replay_controls_v1.md).

1. **Propose:** validate a permitted, versioned source manifest; preserve raw observations; normalize with pinned schemas; enumerate maximal structural trace alignments and compatible frozen relation templates; account for all support, contradiction, ambiguity, duplicates and exclusions; emit only non-executable `CandidateVersion` proposals with immutable provenance.
2. **Triage:** require a prior frozen `PredictionRecord`; check permissions/integrity, observation reliability, action execution, outcome-only status, effect comparison and attribution in order. Separate dynamics contradictions, scope misses, execution/observation faults, missing-condition hypotheses and unresolved mismatches. Unknown is not false; unresolved never narrows a guard.
3. **Refine:** quarantine the affected immutable SkillVersion as required; form guard/split/relaxation proposals only from pinned observable predicates and permitted evidence. Every semantic edit creates a successor version. No support/promotion threshold is invented. An event reused to refine a successor cannot validate that successor or descendants; hidden/test/confirmatory outcomes remain unavailable.
4. **Run (design semantics only):** require separately authorized `ACTIVE` status, compatible pinned artifacts and known limits; evaluate tri-state predicates, bind parameters uniquely, freeze prediction before action, stop on the first mismatch or exhausted cap, use only an independently authorized and budgeted fallback, and append all logs.

P4 is deterministic conditional on pinned versions and policies. Missing or unresolved inputs lead to `BLOCKED`, `HOLD`, or `ABSTAIN`, not a guessed default. The full contract records open decisions and the no-implementation boundary.
