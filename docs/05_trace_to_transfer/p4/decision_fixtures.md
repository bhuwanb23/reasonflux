# P4 Decision Fixtures — Boundary Algorithm v1.0.0-draft

These are synthetic, hand-authored contract fixtures for [`boundary_algorithm_v1.md`](boundary_algorithm_v1.md). They are not ARC data, test executions, empirical outcomes, or evidence that any algorithm works. Each expected result describes the design contract only.

## F1 — Repeated structural motif, support counts preserved

**Input:** two permitted traces contain an unambiguous maximal common structural run; a pinned relation template matches typed pre-state/action/effect paths. The run has multiple raw occurrences, but some share one context ID.  
**Expected:** emit a non-executable `CandidateVersion` in `PROPOSED` if the identity/config/profile refs are pinned. The support ledger reports raw occurrences and distinct event/trace/run/context counts separately; duplicate events do not inflate independent-context counts. No numerical support threshold or promotion follows.

## F2 — Ambiguous alignment

**Input:** a repeated action-schema token occurs twice in one trace and has two equally valid correspondences to another trace; both produce different parameter maps.  
**Expected:** retain both alignments in the audit, label the correspondence `ALIGNMENT_AMBIGUOUS`, do not force one mapping, and do not use it as positive support for a candidate relation. Continue with other unambiguous proposals.

## F3 — Unknown/occluded feature

**Input:** a relevant state field is `UNKNOWN` in one aligned instance, while it is known in another.  
**Expected:** unknown is not wildcard, false, or a value to impute. The event remains in the ledger as unresolved/unknown; it cannot be counted as clean support or used to create a guard difference.

## F4 — Effect match

**Input:** a valid pre-outcome PredictionRecord, reliable action execution and observation, and a known observed effect equal under the pinned effect comparator.  
**Expected:** no counterexample. Append the EffectAssessment/observation refs; do not revise a guard or create a negative example.

## F5 — Tool/execution error

**Input:** the dispatched action differs from the frozen predicted action, a tool call fails, or the environment rejects the command before the predicted transition could occur.  
**Expected:** top-level P2 class `EXECUTION_ERROR`; stop the invocation and log the failure. Do not narrow applicability or reject the invariant from this event.

## F6 — Observation fault versus uncertainty

**Input A:** a verified stale normalizer or parser error corrupted the recorded state.  
**Expected A:** P2 class `OBSERVATION_ERROR`; preserve raw observation and derived record, quarantine only if integrity policy requires; do not refine the guard from corrupted data.

**Input B:** an object is occluded or two identity mappings remain plausible.  
**Expected B:** `AMBIGUOUS_UNRESOLVED` with P4 subtype `OBSERVATION_UNCERTAIN`; abstain, do not coerce uncertainty to negative evidence.

## F7 — Confirmed scope miss with a possible omitted condition

**Input:** an immutable skill version's required predicates evaluated TRUE; a valid prediction preceded the target action; action/observation are reliable; the local effect contradicts the prediction; a predicate `q` in the frozen observable vocabulary is KNOWN and FALSE in the miss and KNOWN/TRUE in at least one reliable prior support context. Prior source support and coverage for `q` are recorded but no quantitative support threshold is set.  
**Expected:** append `SCOPE_COUNTEREXAMPLE` and a `MISSING_CONDITION_HYPOTHESIS` sidecar (unless the P4 attribution rubric establishes another cause); stop and quarantine the affected version under the conservative policy. Emit a separate draft successor proposal with `G AND q` and full coverage/support ledger. Do not modify or reactivate the old version, and do not mark the successor validated/active. A single case can justify safety containment and a proposal, not promotion.

## F8 — Dynamics contradiction with deterministic relation

**Input:** all declared variables and observations are reliable; action execution is verified; all required conditions held; a frozen deterministic relation predicts an effect contradicted by the observed effect. No supported scope partition explains the mismatch.  
**Expected:** `DYNAMICS_COUNTEREXAMPLE`; challenge/reject the deterministic CandidateVersion according to the versioned lifecycle policy and quarantine any derived SkillVersion. Do not repair the relation by inventing a post-hoc guard. For a stochastic/noisy relation without a frozen decision criterion, hold/unresolve rather than selecting a threshold.

## F9 — No observable missing condition

**Input:** a reliable scope miss occurs, but no permitted, known predicate from the frozen vocabulary separates the miss from supported contexts.  
**Expected:** do not blacklist the level ID, event ID, screenshot hash, or target label. Keep the old version quarantined/disabled under policy; abstain, hold, or reject under the frozen decision policy. No inferred hidden condition is allowed.

## F10 — Relaxation after a later success

**Input:** a restrictive guard `G AND q` is followed by one success in a context where `q` is false.  
**Expected:** do not remove `q` automatically. Keep the successful event in its prospectively assigned evidence role. A relaxation proposal requires fresh permitted evidence and a frozen redundancy/generalization policy; if that policy is absent, hold the condition.

## F11 — Validation event reused for refinement

**Input:** a permitted held-out event assesses immutable version V1; after seeing its result, an authorized policy allows it to inform a successor V2.  
**Expected:** preserve the V1 assessment, append a new evidence-use event marking the event `REFINEMENT_FOR_SUCCESSOR`, and prohibit counting it as validation for V2 or descendants. If the event is hidden/test/confirmatory/restricted, no refinement is permitted at all.

## F12 — Unknown runtime predicate or limit

**Input:** an otherwise valid draft has an UNKNOWN required predicate, unresolved parameter binding, unknown action limit/unit, or is not separately authorized as `ACTIVE`.  
**Expected:** no invocation and no action. Return `ABSTAIN/REJECT` with a reason. Do not guess a default, infer authorization from schema validity, or execute the fallback unless separately authorized and budgeted.

## F13 — Runtime mismatch and fallback

**Input:** a valid PredictionRecord is frozen, one declared action is executed, and the observed effect mismatches or a postcondition fails. A separately authorized fallback is either absent or has a separately reserved budget.  
**Expected:** stop before the next skill action; append prediction/action/observation/mismatch/resource records; classify through P4.2; quarantine if required. If no eligible fallback exists, terminate with `ABSTAIN`/`NO_OP`/abort. If a safe policy or deopt is separately authorized, check its own applicability and remaining budget before calling it. Never retry invisibly or exceed caps.

## Fixture-wide invariants

- CandidateVersion remains a hypothesis; SkillVersion creation, validation, activation, and invocation require separate decisions/authorization.
- A semantic boundary change creates a successor digest/version; no record is overwritten.
- Unknown and ambiguous evidence remains unresolved and cannot narrow the guard.
- Candidate support counts are descriptive; P4 invents no support, confidence, refinement, promotion, or runtime threshold.
- Hidden/test/confirmatory outcomes never enter candidate or boundary updates.
- A target event used for refinement cannot validate the same successor or its descendants.
- Every current-turn outcome, action, failure, fallback, quarantine, and cost is retained in append-only records.
- No fixture has been executed; these are design expectations only.
