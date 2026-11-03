# Formal Skill Object Specification — Draft 0.1

**Purpose:** define a candidate contract that independent implementers could realize consistently. The schema is a design proposal, not a frozen implementation or authorization.

## 1. Required fields

```text
SkillObject {
  schema_version
  skill_id                 stable identity for conceptual lineage
  version_id               immutable version/hash of executable semantics
  status                   candidate | provisional | validated | active | quarantined | retired
  invariant_hypothesis     machine-readable relation over state/action/effect
  parameters               typed variables bound at invocation
  preconditions            observable predicates; each cites supporting evidence
  policy                   executable action/controller procedure
  effect_model             predicted next-state/effect distribution or rule
  termination              explicit stop predicate/budget
  fallback                 safe behavior on mismatch/uncertainty
  positive_evidence[]      source run/event references, context, outcome
  counterexamples[]        source event, prior prediction, observed result, conditions
  applicability_evidence  support/contradiction summary; method/version identified
  creation_cost             tokens/time/compute and any action cost, separately logged
  invocation_costs          actions/time/compute per use, separately logged
  provenance                source trace IDs, code/prompt/model/config versions
  decisions[]               candidate/updates/promotion/quarantine/retirement reasons
}
```

No field may be silently omitted when it is required for the current state. Use typed `unknown/not_applicable` values; do not encode uncertainty as a guessed default.

## 2. Semantic requirements

- **Invariant hypothesis:** states what structural relationship is expected to remain stable, not merely a textual summary or trace hash.
- **Parameters:** values that should be rebound in a new context rather than copied from the source trace.
- **Preconditions:** facts needed before execution. Each predicate must be observable through permitted agent inputs and tied to positive/contradictory evidence.
- **Effect model:** predicts an outcome before execution. The observation used to evaluate a prediction cannot be fed backward into that same prediction.
- **Termination/fallback:** bound actions/steps and define what the runtime does on mismatch or uncertainty.
- **Evidence:** immutable references to source events; store successes, failures, abstentions and rejected candidates.
- **Versioning:** changing invariant, parameter schema, precondition, policy, effect model, or fallback creates a new version. Never overwrite historical behavior.

## 3. Minimum applicability response

An invocation-time applicability check must produce:

```text
ApplicabilityResult {
  decision: applicable | abstain | reject
  matched_preconditions[]
  unmet_or_unknown_preconditions[]
  supporting_evidence_refs[]
  contradiction_refs[]
  confidence_method_version
  reason_code
}
```

A numeric confidence field is not required until its calibration method is defined. An uncalibrated score must not be presented as probability.

## 4. State transitions

`candidate → provisional → validated → active` are the proposed forward states. `active → quarantined` follows a material contradiction or harm signal; `quarantined → revised-version candidate` requires a new version; `active → retired` follows a predeclared policy. This is not a final threshold policy: minimum support, evidence breadth, and recovery rules remain open.

## 5. Interoperability tests

Two independent implementations should agree on: schema parsing; version identity; precondition outcomes on fixed fixtures; prediction/effect comparison; counterexample append-only behavior; termination/fallback; and lineage completeness. No scientific result follows from passing these contract tests.
