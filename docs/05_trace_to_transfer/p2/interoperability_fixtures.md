# P2 Interoperability Fixtures — Contract v1.0.0-draft

These are **documentary, synthetic conformance examples** for independent implementations of [`schema_v1.json`](schema_v1.json) and [`formal_skill_object.md`](../formal_skill_object.md). They are not ARC traces, implementation tests, experiments, or scientific evidence. Expected results are contract semantics, not measured outcomes. IDs are fixture-only; fixture digests hash the literal labels described below and are not project artifact digests.

## F1 — A candidate is not executable

**Input:** a schema-valid `CANDIDATE_VERSION` with a relation hypothesis, parameters, preconditions, evidence snapshot, and provenance; no policy artifact or skill version exists.  
**Expected:** candidate parsing succeeds; dispatch as a skill fails; no invocation or promotion is inferred. Only a separate, evidence-linked `PROMOTION_DECISION` can accept the candidate for skill specification, and a separate `SKILL_VERSION` must then be authored.

## F2 — All required applicability predicates true

**Input:** every required predicate evaluates `TRUE`; representation and dependency versions match; no active contradiction exists.  
**Expected:** `APPLICABLE` is structurally consistent. This is only a local gate result; it is not proof of predictive accuracy, task success, validation, or authorization.

```json
{
  "record_type": "APPLICABILITY_RESULT",
  "schema_version": "1.0.0-draft",
  "skill_version_id": "urn:t2t:fixture:skill-v1",
  "context_ref": "urn:t2t:fixture:context-1",
  "decision": "APPLICABLE",
  "decision_reason_codes": ["ALL_REQUIRED_PREDICATES_TRUE"],
  "predicate_evaluations": [
    {
      "predicate_id": "urn:t2t:fixture:predicate-a",
      "result": "TRUE",
      "reason_code": "OBSERVED_MATCH",
      "source_event_refs": ["urn:t2t:fixture:event-1"]
    }
  ],
  "evaluator_ref": {
    "uri": "fixture://v1/evaluator",
    "digest": "sha256:dddd1a7672daaaeee32649e4fa11e354534a78607c87b228f3198470f574884a",
    "media_type": "application/test-fixture",
    "artifact_version": "fixture-v1"
  },
  "evaluated_at": "2026-11-03T00:00:00Z"
}
```

## F3 — Known false precondition

**Input:** a required applicability predicate evaluates `FALSE`, with a source-event reference and reason code.  
**Expected:** `REJECT` for this invocation context; no invocation. This does not automatically reject the candidate or retire the skill globally.

## F4 — Unknown precondition

**Input:** a required predicate evaluates `UNKNOWN` (e.g. the necessary feature is occluded or unavailable).  
**Expected:** `ABSTAIN`; it must not be coerced to `TRUE`, and must not be treated as a negative example for candidate formation.

```json
{
  "record_type": "APPLICABILITY_RESULT",
  "schema_version": "1.0.0-draft",
  "skill_version_id": "urn:t2t:fixture:skill-v1",
  "context_ref": "urn:t2t:fixture:context-2",
  "decision": "ABSTAIN",
  "decision_reason_codes": ["REQUIRED_FEATURE_UNKNOWN"],
  "predicate_evaluations": [
    {
      "predicate_id": "urn:t2t:fixture:predicate-a",
      "result": "UNKNOWN",
      "reason_code": "FEATURE_NOT_OBSERVED",
      "source_event_refs": []
    }
  ],
  "evaluator_ref": {
    "uri": "fixture://v1/evaluator",
    "digest": "sha256:dddd1a7672daaaeee32649e4fa11e354534a78607c87b228f3198470f574884a",
    "media_type": "application/test-fixture",
    "artifact_version": "fixture-v1"
  },
  "evaluated_at": "2026-11-03T00:00:01Z"
}
```

## F5 — Unresolved mismatch is not a scope counterexample

**Input:** a frozen prediction differs from an observed effect, but perception/action fidelity or hidden-state classification is unresolved. The `CounterexampleRecord.classification` is `AMBIGUOUS_UNRESOLVED`.  
**Expected:** append the record; retain its unresolved label; do not narrow applicability or claim the invariant is false. If the mismatch could make use unsafe, the current skill version may be quarantined pending review under a separately recorded policy decision. No automatic repair is implied.

## F6 — Classified scope counterexample and revision

**Input:** a prior prediction and matched preconditions are pinned; an independently allowed classification identifies a true skill-scope miss.  
**Expected:** append a `SCOPE_COUNTEREXAMPLE` linked to the old `skill_version_id`; record the old prediction and observed event separately; quarantine the old version if policy requires. Any revised guard creates a successor candidate/version and then a new skill version with new hashes and explicit predecessor/evidence refs. The original version and event remain byte-for-byte unchanged. A dynamics counterexample instead challenges the predicted relation/model; it is not automatically relabeled as a scope miss.

## F7 — Semantic edit with stale version digest

**Input:** change a relation, parameter schema, precondition, policy, effect prediction, termination, or fallback but reuse the prior `skill_version_id` / `content_digest`.  
**Expected:** reject at semantic integrity validation. JSON Schema can check digest shape but not calculate content identity; the canonical-digest checker must recompute it. Any semantic change requires a successor version.

## F8 — Outcome leakage into a pre-outcome evidence snapshot

**Input:** an evaluator-provided or restricted target outcome is added as `PERMITTED_SOURCE` evidence, or a promotion decision references that outcome.  
**Expected:** reject by provenance/access-policy validation. The v1 `EvidenceRef.access_class` only allows `PERMITTED_SOURCE`; evaluator outcomes belong to a separate, later evaluation record/store and cannot influence earlier candidate formation or promotion. A different final score alone is not a local counterexample.

## F9 — Parameterized replay can match the invariant treatment

**Input:** a strong replay comparator is given the same source traces, parameter slots, binding information, execution checks, retrieval opportunity, and budgets as the invariant treatment. It predicts and behaves identically on the allowed held-out contexts.  
**Expected:** report no demonstrated invariant-specific increment (Claim N unsupported or unidentifiable under that comparison), even if both methods beat raw replay or no-skill. Do not cripple the comparator or redefine its behavior as an invariant after seeing results.

## F10 — Lifecycle is append-only; `ACTIVE` is not a schema consequence

**Input:** a lifecycle transition changes a skill from `DRAFT` to `ELIGIBLE_FOR_VALIDATION`, `VALIDATED`, or `ACTIVE`.  
**Expected:** each transition has a new immutable `decision_id`, subject version, prior/next status, policy version, evidence snapshot, actor, timestamp, and predecessor decision. `ELIGIBLE_FOR_VALIDATION` is structural only. `VALIDATED` requires prospective criteria that are not set in P2. `ACTIVE` additionally requires separate runtime authorization. No lifecycle transition is run or authorized by these fixtures.

## F11 — Prediction is a separate, pre-outcome record

**Input:** a `PredictionRecord` binds one skill version, context, action, all-`TRUE` applicability predicates, explicit predicted target values, model/evidence refs, a timestamp, and append-order index before the target action/result. Later, an `EffectAssessment` references this immutable prediction and a separate observed-effect record.  
**Expected:** prediction parses and remains unchanged after outcome arrival; the assessment can compare it with the observed effect. A prediction with an `UNKNOWN`/`FALSE` required predicate is invalid; do not create a prediction when the applicability decision is `ABSTAIN` or `REJECT`.

```json
{
  "record_type": "PREDICTION_RECORD",
  "schema_version": "1.0.0-draft",
  "prediction_id": "urn:t2t:fixture:prediction-1",
  "skill_version_id": "urn:t2t:fixture:skill-v1",
  "context_ref": "urn:t2t:fixture:context-3",
  "action_ref": "urn:t2t:fixture:action-1",
  "predicate_evaluations": [
    {
      "predicate_id": "urn:t2t:fixture:predicate-a",
      "result": "TRUE",
      "reason_code": "OBSERVED_MATCH",
      "source_event_refs": ["urn:t2t:fixture:event-2"]
    }
  ],
  "predicted_effects": [
    {
      "target_ref": {
        "uri": "fixture://v1/effect-target",
        "digest": "sha256:eeee1a7672daaaeee32649e4fa11e354534a78607c87b228f3198470f574884a",
        "media_type": "application/test-fixture",
        "artifact_version": "fixture-v1"
      },
      "prediction_form": "DETERMINISTIC_RULE",
      "predicted_value": {
        "availability": "KNOWN",
        "value": {"color": "blue"},
        "source_refs": ["urn:t2t:fixture:context-3"]
      }
    }
  ],
  "prediction_model_ref": {
    "uri": "fixture://v1/prediction-model",
    "digest": "sha256:eeee1a7672daaaeee32649e4fa11e354534a78607c87b228f3198470f574884a",
    "media_type": "application/test-fixture",
    "artifact_version": "fixture-v1"
  },
  "evidence_snapshot_ref": {
    "evidence_snapshot_id": "urn:t2t:fixture:snapshot-1",
    "digest": "sha256:eeee1a7672daaaeee32649e4fa11e354534a78607c87b228f3198470f574884a"
  },
  "predicted_at": "2026-11-03T00:00:00Z",
  "log_sequence": 17
}
```

## Fixture-wide invariants

- Missing data is explicit `UNKNOWN` / `NOT_APPLICABLE`, never a silent default.
- Predictions are frozen before the target event; observed effects are appended after it.
- Support, contradiction, ambiguity, counterfactual activation utility, and evaluator outcome are distinct evidence classes.
- A status or evidence update does not mutate a semantic version.
- All cost dimensions remain separate; no composite promotion score is defined here.
- Fixture evaluation is documentation QA only and carries no scientific or execution authority.
