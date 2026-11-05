# P4 Deliverables — Counterexample Boundary Algorithm

**Contract:** `T2T-P4-Boundary-v1.0.0-draft`  
**P4 status:** complete for documentation/design scope, 2026-11-04.  
**Authorization boundary:** no implementation, experiments, benchmarks, ARC runs, split assignment, candidate/skill execution, or restricted-outcome access.

## Normative design

- [`boundary_algorithm_v1.md`](boundary_algorithm_v1.md) — deterministic candidate-proposal pipeline, source-support accounting, counterexample triage, append-only scope refinement, data-use separation, and runtime abstain/fallback state machine.
- [`decision_fixtures.md`](decision_fixtures.md) — synthetic expected decisions and edge cases; contract fixtures, not execution or scientific evidence.
- [`../counterexample_boundary_algorithm.md`](../counterexample_boundary_algorithm.md) — legacy entrypoint reconciled to this versioned P4 contract.
- [`../formal_skill_object.md`](../formal_skill_object.md) — P2 CandidateVersion/SkillVersion, PredictionRecord, CounterexampleRecord and lifecycle rules.

## P4.1–P4.4 results

- **P4.1 Candidate generation:** pinned, versioned observation normalization and structural trace alignment; deterministic motif/template proposal; complete support, exclusion, ambiguity, and contradiction accounting. Proposal counts are not promotion thresholds.
- **P4.2 Counterexample taxonomy:** ordered triage separates outcome-only, observation/execution errors, confirmed dynamics mismatch, applicability/scope miss, missing-condition hypotheses, and unresolved cases. Uncertainty never becomes a negative label.
- **P4.3 Scope refinement:** immutable successor versions only; propose conjunctions or scope splits from a frozen observable predicate vocabulary; require evidence-policy checks for relaxation; allow quarantine, reduced coverage/abstention, or rejection. No target result validates a version it refined.
- **P4.4 Fallback:** explicit preflight, predicate, prediction-freeze, action, mismatch-stop, step/resource-limit, safe fallback, and append-only logging state machine. Unknown runtime-critical limits block invocation.

## Acceptance and open choices

P4 is complete for the bounded design/documentation scope. The algorithm is deterministic conditional on pinned representation, normalizer, relation-template, taxonomy, identity, and policy versions; if a required version or policy parameter is unset, it halts/holds instead of guessing. No evidence/promotion/support threshold, candidate population, target split, action/resource cap, or fallback skill is invented. The exact domain ontology, alignment/template library, diagnostic adjudication rubric, permitted manifests, guard-refinement thresholds, step budgets, and separately authorized validation plan remain open.

Final QA: P4 records and examples are internally cross-referenced with the P2 contract; the taxonomy uses only P2's existing counterexample enum, with P4 diagnostic detail carried in immutable assessment artifacts. Checked 56 Markdown files and 283 relative links with zero broken links; verified P4.1–P4.4 statuses and P2 enum interoperability. This is documentation/schema cross-checking only. Nothing here implements or runs the algorithm.
