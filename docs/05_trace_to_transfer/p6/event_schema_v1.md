# T2T-P6 Event Schema Proposal

**Schema ID:** `T2T-EventSchema-v1.0.0-draft`  
**Subphase:** P6.2 — Event schema  
**Status:** complete for documentation/design scope; schema service, serializer and tests are not implemented.  
**Dependencies:** P2 record contract; P3/P5 arm, data-role, cost and outcome separation; P4 triage and evidence-use sidecars.

## 1. Scope and conformance

This document specifies the logical event envelope and required event-specific references for immutable observation, action, prediction, transition, candidate/skill version, lifecycle, triage, failure/fallback and cost records. It is a versioned **schema proposal**, not an executable event processor, JSON Schema validator, database migration, or authorization.

P2 remains normative for the structure and semantics of `CandidateVersion`, `SkillVersion`, `PredictionRecord`, `EffectAssessment`, `ApplicabilityResult`, `EvidenceSnapshot`, `LifecycleEvent`, and `CounterexampleRecord`. P6 events reference those immutable records; they do not copy, extend, or mutate P2 objects. P4 fine-grained triage remains in the P4 sidecar and maps to P2's existing coarse enum. Do not add P2 enum values or fields through this event schema.

The original P6 design left the exact JSON Schema dialect, ID format, canonical serialization, digest profile, store URI scheme, and physical retention policy open. A separate user-authorized Step 1 instantiated a machine-readable [Draft 2020-12 schema](event_schema_v1.json) for synthetic/local use and a prototype-only `t2t-python-json-c14n-v1` digest profile. These local choices do **not** resolve P2's production ID/canonicalization profile, establish cross-language compatibility, or authorize use with real/ARC/restricted data. Production migration and retention remain `UNSET` pending owner/security review.

## 2. Event envelope

Every event has an immutable envelope. Implementations may use an equivalent physical encoding only if a reviewed schema version preserves these semantics.

| Field | Required | Meaning and constraint |
|---|---:|---|
| `event_id` | yes | Stable, globally unique identity under the project-approved ID scheme; scheme remains unset. Never reused. |
| `event_schema_version` | yes | Exact event contract version, initially `T2T-EventSchema-v1.0.0-draft`. |
| `event_type` | yes | One event kind in §4; type selects the payload contract. Unknown type is rejected, not silently accepted. |
| `recorded_at` | yes | RFC-3339 timestamp with explicit timezone for journal record time. The clock source/precision policy remains open. Not a substitute for sequence ordering. |
| `stream_id` | yes | Stable identity of the append stream (e.g., formation run or runtime episode); format unset. |
| `stream_seq` | yes | Nonnegative, unique, monotonically increasing append index within `stream_id`; gaps may be retained and explained but sequence cannot be rewritten. |
| `activity_ref` | yes | Opaque reference to the proposal, validation, runtime, or analysis activity/config record; it does not imply authorization. |
| `arm_ref` | conditional | Frozen arm/config ref for arm-specific events; absent for arm-independent source events. |
| `producer` | yes | Producer identity/class and software/config version refs, using P2 provenance semantics; AI-generated annotations must not be called independent human labels. |
| `data_role_ref` | conditional | Reference to the prospective P5 manifest/role assignment for data-derived events. It is not a new P2 `EvidenceSnapshot.purpose` value. |
| `access_class_ref` | yes | Reference to the controlling access/permission classification. Restricted outcome payloads are never copied into the general event stream. |
| `causal_parent_event_refs` | yes | Ordered list of known causal parent event IDs; empty only for genesis/source events. Missing parents are not inferred. |
| `supersedes_event_ref` | conditional | Existing event being corrected or superseded. Corrections append a new event and preserve the original. |
| `payload` | yes | Type-specific fields in §§3–4; raw or large content should be referenced, not duplicated. |
| `provenance_refs` | yes | Manifest/artifact/schema/config/evidence refs needed to reproduce interpretation; empty only when the event type has no such input and the reason is explicit. |
| `integrity` | yes | `content_digest`, `digest_profile_ref`, and optional predecessor digest/ref. Digest construction waits for the approved canonicalization profile; no custom hash rule is introduced here. |

### Ordering rules

- `stream_seq` is authoritative for append order inside its stream; timestamps are retained for audit but are not used to reorder events.
- A causal link across streams is explicit through event IDs and activity refs. Do not infer a total order between unsynchronized streams.
- For prediction-dependent action, the P2 `PredictionRecord` and its corresponding `PREDICTION_FROZEN` event must precede dispatch in journal sequence **and** by the P2-required timestamp ordering. If timestamp/order cannot establish precedence, the action gate must block that action or mark the trace invalid; no retrospective repair.
- `ACTION_REQUESTED` may precede the prediction because it records an intent. `ACTION_DISPATCHED` must follow the prediction when that arm/action requires one.
- Source event time (when supplied) is stored separately from journal `recorded_at`; neither may be silently substituted for the other.

## 3. Type and value semantics

1. A missing optional field means “not supplied under this event contract,” not unknown. An unknown observed value uses P2's tagged `UNKNOWN` form with a reason and available source refs. `NOT_APPLICABLE` is distinct. Known false is an explicit known value or tri-state predicate result `FALSE`.
2. Do not serialize unknown as `null`, empty string, zero, `false`, empty list, guessed default, or omission when the field is required.
3. IDs and content digests refer to immutable objects. If a referenced object changes semantically, create a successor object with a new version/digest and append the relevant lifecycle event.
4. A structurally valid event is not proof of scientific validity, complete provenance, permission, system safety, or run authorization.
5. Candidate and skill objects are refs to P2 records. Candidate proposal events must not contain executable policy content; a `CandidateVersion` cannot reach an action interface.
6. Prediction, action, observation/transition, effect assessment, and evaluator outcome are distinct event types and records. Never overwrite an expected value with an observed value.
7. Failed, aborted, timed-out, abstained, mismatched, missing-cost, and integrity-blocked events are retained with reason codes. No outcome-driven filtering in the event writer.

## 4. Event type registry and payload contracts

All listed types inherit the envelope. The tables specify required payload fields; additional type-specific fields require a reviewed event-schema version rather than undocumented extension.

### 4.1 Control and manifest events

| `event_type` | Required payload fields | Invariants |
|---|---|---|
| `ACTIVITY_CONFIG_BOUND` | `protocol_ref`, `config_ref`, `arm_artifact_refs`, `representation_refs`, `manifest_refs`, `evaluator_ref` or explicit `NOT_APPLICABLE`, `budget_contract_ref`, `authorization_decision_ref`. | Freeze before relevant data/outcomes; no task/split assignment is performed by this schema. A blocked authorization cannot produce runtime action events. |
| `DATA_ROLE_BOUND` | `manifest_ref`, `artifact_or_event_ref`, `role_ref`, `allowed_fields_ref`, `purpose_ref`, `decision_ref`. | Record role prospectively. P2 `purpose` values are not extended; P4 `REFINEMENT_FOR_SUCCESSOR` remains in its append-only evidence-use ledger. |
| `INTEGRITY_HOLD` | `affected_refs`, `reason_code`, `hold_scope`, `review_required`, optional `supersedes_event_ref`. | Stop affected flow; preserve source records; no silent repair or replacement. |

### 4.2 Observation and state events

| `event_type` | Required payload fields | Invariants |
|---|---|---|
| `OBSERVATION_RECORDED` | `observation_id`, `raw_observation_ref`, `source_event_ref` or explicit origin ref, `source_time` or tagged unknown, `representation_ref`, `normalizer_ref` or explicit not-yet-normalized state. | Raw observation is immutable. Normalized/derived content is a separate referenced artifact/event. No answer label/future observation may be added to a decision-time payload. |
| `OBSERVATION_NORMALIZED` | `observation_id`, `source_observation_event_ref`, `normalized_observation_ref`, `normalizer_ref`, `field_availability_summary`, `derivation_ref`. | Every derived field links to source; unknown/occluded/conflicting values remain tagged and do not become false. |
| `SOURCE_ACTION_RECORDED` | `source_action_id`, `source_trace_ref`, `source_event_index`, `action_ref`, `pre_observation_event_ref` or tagged unavailable, `post_transition_event_ref` or tagged unavailable, `source_time` or tagged unknown. | Records an action that occurred in permitted source experience; it is not a runtime dispatch by the current agent. Keep source provenance and evidence role; missing source observations remain explicit. |

### 4.3 Applicability, prediction, and effect events

| `event_type` | Required payload fields | Invariants |
|---|---|---|
| `APPLICABILITY_ASSESSED` | `skill_version_ref`, `observation_event_ref`, `applicability_result_ref`, `result` (`APPLICABLE`, `REJECT`, `ABSTAIN`), `predicate_evaluation_refs`, `reason_codes`. | P2 tri-state semantics: any required known false may reject locally; any required unknown blocks positive applicability. This is not global skill rejection. |
| `ACTION_REQUESTED` | `intent_id`, `agent_or_arm_ref`, `observation_event_refs`, `proposed_action_ref` or explicit no-action, `required_prediction` boolean, `remaining_budget_ref`. | Records intent only; it does not mean action was dispatched or accepted. |
| `PREDICTION_FROZEN` | `prediction_record_ref`, `skill_version_ref` or explicit baseline adapter ref, `intent_id`, `target_effect_ref`. | References an immutable P2 `PredictionRecord`; its envelope sequence/timestamp must precede the later dispatch/action-result events. The later event order is the check; no reference to a future action event is embedded into the prediction. If required prediction is absent/invalid, block dependent dispatch. |
| `ACTION_DISPATCHED` | `intent_id`, `action_ref`, `dispatch_ref`, `prediction_record_ref` or reasoned `NOT_APPLICABLE`, `budget_before_ref`. | Represents an actual dispatch attempt, distinct from a request or environment acceptance. When P5 requires prediction, reference must resolve to a prior prediction. |
| `ACTION_RESULT_RECORDED` | `intent_id`, `dispatch_event_ref`, `result_status` (`ACCEPTED`, `REJECTED`, `FAILED`, `UNKNOWN`), `environment_response_ref` or tagged unknown, `budget_after_ref`. | No response is not success. Rejected/failed/unknown action is retained and cannot be treated as successful execution. |
| `TRANSITION_OBSERVED` | `pre_observation_event_ref`, `action_result_event_ref`, `post_observation_event_ref`, `observed_effect_ref` or tagged unknown, `representation_ref`, `source_time`. | Local observation of a transition only; does not itself establish prediction correctness or evaluator outcome. |
| `EFFECT_ASSESSED` | `effect_assessment_ref`, `prediction_record_ref`, `transition_event_ref`, `assessment_status` (`MATCH`, `MISMATCH`, `UNKNOWN`, `NOT_ASSESSED`), `comparator_ref`. | P2 `EffectAssessment` remains authoritative. Unknown attribution is not a counterexample. |

### 4.4 Candidate, skill, lifecycle, and triage events

| `event_type` | Required payload fields | Invariants |
|---|---|---|
| `CANDIDATE_VERSION_EMITTED` | `candidate_version_ref`, `candidate_version_id`, `content_digest`, `evidence_snapshot_ref`, `support_ledger_ref`, `proposal_audit_ref`. | Candidate is non-executable. No runtime policy/action payload. Formation uses only allowed source role; emitted event is not validation. |
| `SKILL_VERSION_EMITTED` | `skill_version_ref`, `skill_version_id`, `content_digest`, `candidate_version_ref`, `derivation_evidence_ref`, `lifecycle_status_ref`. | A skill specification is not necessarily implemented, validated, active, or authorized. |
| `LIFECYCLE_DECISION_APPENDED` | `lifecycle_event_ref`, `subject_ref`, `prior_status`, `next_status`, `decision_ref`, `evidence_snapshot_ref`, `predecessor_lifecycle_event_ref` or explicit genesis. | Append-only P2 transition policy; no status is updated in place. |
| `TRIAGE_ASSESSMENT_APPENDED` | `counterexample_record_ref` or explicit no-record reason, `p4_triage_sidecar_ref`, `prediction_record_ref`, `transition_event_ref`, `assessment_state`. | P2 coarse `CounterexampleRecord.classification` enum is unchanged. P4 subtype/adjudication remains in sidecar. |
| `EVIDENCE_USE_APPENDED` | `evidence_ref`, `prior_role_ref`, `new_role_ref`, `subject_version_refs`, `decision_ref`, `validation_eligibility_effect`. | Corrections/role changes are append-only; any refinement use invalidates that event as validation of the successor and descendants. Restricted/confirmatory outcomes cannot enter refinement. |

### 4.5 Fallback, stop, failure, and cost events

| `event_type` | Required payload fields | Invariants |
|---|---|---|
| `FALLBACK_SELECTED` | `trigger_event_ref`, `fallback_policy_ref` or explicit none, `fallback_decision`, `reserved_budget_ref`, `result_event_ref` or pending ref. | Fallback is separately declared/authorized and budgeted; no uncharged retry, deopt, or extra model call. |
| `STOP_OR_FAILURE` | `stage`, `reason_code`, `affected_refs`, `stop_scope`, `recoverable` tagged value, `review_required`. | Record abstention, timeout, crash, mismatch, cap breach and integrity fault. Stop means no further action unless an authorized fallback explicitly proceeds. |
| `COST_MEASURED` | `cost_record_id`, `resource_dimension`, `amount` tagged known/unknown, `unit_ref`, `measurement_method_ref`, `stage`, `scope_ref`, `arm_ref` or explicit N/A, `budget_contract_ref`, `window_start_ref`, `window_end_ref` or pending status. | Record cap and realized amount separately; unknown is not zero; keep vector components separate. |
| `EVENT_CORRECTION_APPENDED` | `supersedes_event_ref`, `correction_reason`, `corrected_fields_or_payload_ref`, `approver_ref`, `integrity_impact`. | Original stays readable and immutable. Correction is not allowed to erase an unfavorable result or evade an assignment/denominator. |

### 4.6 Restricted evaluator outcome (separate store only)

`EVALUATOR_OUTCOME_RECORDED` is not written to the general run journal. If ever permitted under official/live rules and separate authorization, its isolated outcome record must include protocol/run/arm refs, evaluator version, assigned unit ref, raw outcome artifact ref, timestamp, access-policy ref and export audit. The general journal may contain only an opaque authorized outcome-record reference after the evaluation gate; it must not carry answer-bearing payloads, hidden labels, or a reverse channel to the agent, candidate, baseline, threshold, or refinement services. This event type is included to state the boundary, not to authorize any access.

## 5. Cost and resource field contract

The ledger uses the P3/P5 resource vector, with no numeric values added by P6. Each measurement records:

- `resource_dimension` (e.g., source events/bytes, annotations, tokens/calls, CPU/GPU/compute, wall time, storage, retrieval, environment actions, retries/fallback, evaluator use);
- `amount` as a typed `KNOWN` value with unit or `UNKNOWN` with reason/provenance; never default to zero;
- `unit_ref` and `measurement_method_ref` (pinned, or `UNSET` and therefore blocking when the missing unit is needed for parity);
- `stage` (formation, review, validation, retrieval, invocation, fallback, evaluation), `scope_ref` (per event/task/episode/run/arm), and `arm_ref`;
- `budget_contract_ref`, `declared_cap_ref`, and `realized_amount_ref` kept separate;
- measurement interval/counter source, producer, missingness and provenance; and
- optional allocation/amortization method only when prospectively specified; no default allocation.

Report declared opportunities/caps and realized use for every arm. Parity is checked over predeclared dimensions and caps, not by summing different units into an invented score. Cap values, units, counter sources and acceptable residual mismatch remain P5 freeze-gate choices.

## 6. Immutability, versioning and integrity rules

1. Event payload and envelope are write-once. No update/delete operation is part of the contract.
2. Every event is typed by `event_schema_version`; every P2 object and artifact has its own schema/version refs. A changed event contract receives a new version and migration mapping; historical values retain their original interpretation.
3. Canonicalization/digest and ID algorithms are unresolved. Before implementation, choose a P2-compatible, independently reviewed profile and pin it in the envelope; never invent an incompatible hash or pretend a URI alone is integrity evidence.
4. Journal append ordering is sequence-controlled. Concurrent append conflict rejects or produces a new sequence; never renumber prior events.
5. Corrections append `EVENT_CORRECTION_APPENDED` with explicit superseded ref, reason and review. Analyses must retain the original, correction and impact. Both remain in denominators where relevant.
6. Event schema version and P2 schema version are separate. A P6 event revision must not mutate P2 objects; references are validated against the pinned P2 version.
7. Event integrity or access breach creates `INTEGRITY_HOLD`; affected data are quarantined for review. No “repair” by deleting or rewriting a record.
8. Raw observations/artifacts may be held outside the journal behind access control. Their immutable refs, digest profile and permission status must still be auditable. No credentials or secrets belong in events.

## 7. Role separation, retention and access rules

- Source/formation, development/refinement, validation, confirmatory/target and restricted roles are assigned prospectively through manifest refs, following P5. This event vocabulary does not create new access rights.
- Preserve P2 `EvidenceSnapshot.purpose` and P4 sidecar/evidence-use semantics; do not enlarge enums to simplify logging.
- A record used to refine a version cannot validate that version or descendants. Append `EVIDENCE_USE_APPENDED` and carry the eligibility effect forward.
- No hidden/test/confirmatory outcome is exposed to the agent, candidate generator, baseline author, threshold selection, or refinement system. Restricted outcomes are held in a distinct store and any permitted report export is separately authorized.
- Retention duration, encryption, redaction, deletion/legal hold policy, storage URI, and access roles require security/privacy review; P6 assigns no values or credentials.

## 8. Deliberately unresolved schema decisions

- project-approved globally unique ID format and event stream naming;
- exact canonical JSON/serialization and digest profile compatible with P2;
- JSON Schema dialect/tooling and strict extension/migration policy;
- timestamp source/precision and cross-process ordering design;
- artifact URI/reference resolver, object-store/database/event-journal choice, transaction/retention policy;
- exact environment action/observation/result enumerations and representation versions;
- resource unit/counter definitions, budget reference format, and arm parity acceptance rule;
- privacy/security access classes and physical restricted-store separation;
- exact report-export contract and named schema owner/reviewer.

Until these are reviewed and frozen, this remains a design contract, not a machine-validated production schema.
