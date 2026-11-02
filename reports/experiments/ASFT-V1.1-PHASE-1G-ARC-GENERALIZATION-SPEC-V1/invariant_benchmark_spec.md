# Phase 1G.5 — Invariant Benchmark Specification

## Operational target

An invariant candidate is a versioned, explicit structure/rule proposed from experience that is claimed to recur across task IDs and predict behavior beyond its discovery demonstrations. The benchmark measures candidate formation and validation; it does not assume candidate existence equals a true abstraction.

## Required outputs

- Candidate counts: raw, unique, accepted, rejected, and unavailable; preserve provenance/task IDs.
- **Invariant precision:** independently validated candidates ÷ candidates with an evaluable validation denominator. If denominator is zero, precision is unavailable. Also report label agreement and validation coverage.
- **Invariant survival:** fraction of accepted candidates retained after disjoint validation/replication tasks or counterexample tests; report survived and pruned counts.
- **Recurrence and diversity:** cross-task support, unique structure classes, concentration, and examples per candidate, using frozen deduplication.
- **Predictive utility:** behavior on held-out demonstration pairs/tasks, kept separate from candidate precision and overall task accuracy.

## Validation

Require recurrence on disjoint task IDs, successful predictions for withheld demonstration pairs or preregistered counterexample probes, and blind annotation evidence where available. Annotator categories are not authoritative ARC truth; unknowns and disagreements remain. Thresholds, minimum support, and family definitions are selected in development and locked before confirmation.

## Zero and activation semantics

If a sufficient population of successful traces/candidates was available but none passed validation, report **zero validated invariants / stage not activated** for that run. If the successful-trace pool is below the frozen minimum (as in Phase 13G: 3 traces vs minimum support 5), report zero candidates as observed but classify the test of recurrence as **inconclusive due to insufficient support**, not a theory-level failure. An absent/invalid denominator is unavailable. No status is coded as “IDT disproven.”