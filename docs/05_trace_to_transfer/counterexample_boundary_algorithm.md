# Counterexample-Guided Boundary Algorithm — Design Draft

**Goal:** turn varied interaction evidence into conditional skills whose scope is supported, and whose known contradictions constrain use. This is a design sketch, not code or a run authorization.

## Inputs

- Append-only permitted interaction events: abstracted state, action, observed transition/effect, run/level context, budget and provenance.
- A candidate generator over recurring relational motifs.
- No hidden/test answers, human predictions of hidden states, or outcome data unavailable at decision time.

## Candidate loop

1. **Normalize observations:** derive an explicit state representation; preserve original observation references. Every normalization (object identity, position, color, action semantics) has a version and tests.
2. **Align traces:** match candidate relations/actions/effects across contexts. Keep variable values separate from invariant predicates. An alignment failure is logged, not forced.
3. **Propose candidate:** emit a provisional invariant/effect hypothesis with parameters, proposed preconditions, predicted effects and supporting source-event IDs.
4. **Search for contradictions:** examine permitted past events where the preconditions appeared to hold but the predicted effect did not occur. Classify as: genuine counterexample; state/observation uncertainty; action execution error; missing condition; or unresolved.
5. **Revise scope:** a candidate may add a precondition only if that condition is observable and supported by evidence. Otherwise reduce confidence/coverage or abstain. Do not specialize using one failure without checking whether it is a data/measurement error.
6. **Validate out of construction sample:** test the frozen candidate on contexts not used to construct that version. Record prediction, outcome, applicability decision and cost.
7. **Promote, hold, or reject:** apply a predeclared policy using source/validation evidence only. Preserve all versions and decisions.
8. **Runtime use:** check preconditions; abstain when uncertain; predict effect before action if applicable; observe result; stop/fallback on mismatch; append a counterexample event linked to the invoked version.

## Counterexample record minimum

`event_id, skill_version, state_ref, action, conditions_matched, prior_prediction, observed_effect, mismatch_type, consequence, recovery, data/provenance, timestamp/config`.

## Applicability and uncertainty

The first implementation should not invent a probability. Define deterministic `applicable / abstain / reject` rules from explicit predicates and evidence. A calibrated confidence model is a later research question. Track coverage alongside precision: a system that never invokes skills can have zero harmful transfer but no useful transfer.

## Open algorithmic questions for T2T-P4

- How are object/state correspondences inferred without leaking game identity or hand-coding public games?
- What minimum variation makes a relation meaningfully cross-context?
- When is a contradiction evidence for a missing precondition versus evidence against the invariant?
- Can boundary refinement be evaluated without using target outcomes to update the same skill version?
- What is the action budget for verification, and how does fallback affect the official score?

These questions must be resolved in documents before any run is proposed.
