"""Synthetic-only tests for the T2T local event-log prototype.

Run only with: python -m pytest -q tests/test_t2t_eventlog.py
No repository experiments, ARC data, network, model, evaluator or live environment
are used in this module.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from t2t_eventlog import (
    DIGEST_PROFILE,
    EventJournal,
    EventOrderError,
    EventValidationError,
    JournalIntegrityError,
    SyntheticScopeError,
    canonical_json_bytes,
    check_schema,
    event_digest,
    validate_event,
)

SYNTH = "synthetic:fixture:v1"
NA = {"availability": "NOT_APPLICABLE", "reason_code": "NOT_RECORDED"}
KNOWN = {"availability": "KNOWN", "value": "fixture-value", "source_refs": []}
UNKNOWN = {"availability": "UNKNOWN", "reason_code": "OCCLUDED", "source_refs": []}
KNOWN_FALSE = {"availability": "KNOWN", "value": False, "source_refs": []}


def envelope(event_type: str, payload: dict, *, event_id: str = "synthetic:event:1") -> dict:
    return {
        "event_id": event_id,
        "event_schema_version": "T2T-EventSchema-v1.0.0-draft",
        "event_type": event_type,
        "recorded_at": "2026-01-01T00:00:00.000001Z",
        "stream_id": "synthetic:stream:schema",
        "stream_seq": 0,
        "activity_ref": "synthetic:activity:schema-test",
        "data_role_ref": "SYNTHETIC_FIXTURE",
        "producer": {
            "producer_id": "local:t2t-eventlog-test",
            "producer_class": "SOFTWARE",
            "producer_version_ref": "local:test-v1",
        },
        "access_class_ref": "SYNTHETIC_FIXTURE",
        "causal_parent_event_refs": [],
        "payload": payload,
        "provenance_refs": ["synthetic:manifest:fixture-v1"],
        "integrity": {
            "content_digest": "sha256:" + "0" * 64,
            "digest_profile": DIGEST_PROFILE,
        },
    }


def payloads() -> dict[str, dict]:
    return {
        "ACTIVITY_CONFIG_BOUND": {
            "protocol_ref": f"{SYNTH}:protocol", "config_ref": f"{SYNTH}:config",
            "arm_artifact_refs": [f"{SYNTH}:arm"], "representation_refs": [f"{SYNTH}:representation"],
            "manifest_refs": [f"{SYNTH}:manifest"], "evaluator_ref": NA,
            "budget_contract_ref": f"{SYNTH}:budget", "authorization_decision_ref": f"{SYNTH}:authorization",
        },
        "DATA_ROLE_BOUND": {
            "manifest_ref": f"{SYNTH}:manifest", "artifact_or_event_ref": f"{SYNTH}:artifact",
            "role_ref": f"{SYNTH}:role", "allowed_fields_ref": f"{SYNTH}:fields",
            "purpose_ref": f"{SYNTH}:purpose", "decision_ref": f"{SYNTH}:decision",
        },
        "INTEGRITY_HOLD": {
            "affected_refs": [f"{SYNTH}:artifact"], "reason_code": f"{SYNTH}:reason",
            "hold_scope": f"{SYNTH}:scope", "review_required": True,
        },
        "OBSERVATION_RECORDED": {
            "observation_id": f"{SYNTH}:observation:1", "raw_observation_ref": f"{SYNTH}:raw-observation",
            "source_event_ref": NA, "source_time": UNKNOWN, "representation_ref": f"{SYNTH}:representation",
            "normalizer_ref": NA, "normalization_status": "NOT_STARTED",
        },
        "OBSERVATION_NORMALIZED": {
            "observation_id": f"{SYNTH}:observation:1", "source_observation_event_ref": f"{SYNTH}:observation-event",
            "normalized_observation_ref": f"{SYNTH}:normalized-observation", "normalizer_ref": f"{SYNTH}:normalizer",
            "field_availability_summary": [{"field_ref": f"{SYNTH}:field", "availability": "UNKNOWN", "reason_code": "OCCLUDED"}],
            "derivation_ref": f"{SYNTH}:derivation",
        },
        "SOURCE_ACTION_RECORDED": {
            "source_action_id": f"{SYNTH}:source-action", "source_trace_ref": f"{SYNTH}:trace",
            "source_event_index": 0, "action_ref": f"{SYNTH}:action", "pre_observation_event_ref": NA,
            "post_transition_event_ref": NA, "source_time": UNKNOWN,
        },
        "APPLICABILITY_ASSESSED": {
            "skill_version_ref": f"{SYNTH}:skill", "observation_event_ref": f"{SYNTH}:observation-event",
            "applicability_result_ref": f"{SYNTH}:applicability", "result": "ABSTAIN",
            "predicate_evaluation_refs": [f"{SYNTH}:predicate-eval"], "reason_codes": [f"{SYNTH}:unknown"],
        },
        "ACTION_REQUESTED": {
            "intent_id": f"{SYNTH}:intent", "agent_or_arm_ref": f"{SYNTH}:arm",
            "observation_event_refs": [f"{SYNTH}:observation-event"], "proposed_action_ref": f"{SYNTH}:action",
            "required_prediction": True, "remaining_budget_ref": f"{SYNTH}:budget",
        },
        "PREDICTION_FROZEN": {
            "prediction_record_ref": f"{SYNTH}:prediction", "skill_version_ref": f"{SYNTH}:skill",
            "baseline_adapter_ref": NA, "intent_id": f"{SYNTH}:intent", "target_effect_ref": f"{SYNTH}:effect",
        },
        "ACTION_DISPATCHED": {
            "intent_id": f"{SYNTH}:intent", "action_ref": f"{SYNTH}:action", "dispatch_ref": f"{SYNTH}:dispatch",
            "prediction_record_ref": f"{SYNTH}:prediction", "budget_before_ref": f"{SYNTH}:budget-before",
        },
        "ACTION_RESULT_RECORDED": {
            "intent_id": f"{SYNTH}:intent", "dispatch_event_ref": f"{SYNTH}:dispatch-event",
            "result_status": "ACCEPTED", "environment_response": KNOWN, "budget_after_ref": f"{SYNTH}:budget-after",
        },
        "TRANSITION_OBSERVED": {
            "pre_observation_event_ref": f"{SYNTH}:observation-pre", "action_result_event_ref": f"{SYNTH}:action-result",
            "post_observation_event_ref": f"{SYNTH}:observation-post", "observed_effect": UNKNOWN,
            "representation_ref": f"{SYNTH}:representation", "source_time": UNKNOWN,
        },
        "EFFECT_ASSESSED": {
            "effect_assessment_ref": f"{SYNTH}:effect-assessment", "prediction_record_ref": f"{SYNTH}:prediction",
            "transition_event_ref": f"{SYNTH}:transition", "assessment_status": "UNKNOWN",
            "comparator_ref": f"{SYNTH}:comparator",
        },
        "CANDIDATE_VERSION_EMITTED": {
            "candidate_version_ref": f"{SYNTH}:candidate-version", "candidate_version_id": f"{SYNTH}:candidate-id",
            "content_digest": "sha256:" + "1" * 64, "evidence_snapshot_ref": f"{SYNTH}:evidence",
            "support_ledger_ref": f"{SYNTH}:support-ledger", "proposal_audit_ref": f"{SYNTH}:proposal-audit",
        },
        "SKILL_VERSION_EMITTED": {
            "skill_version_ref": f"{SYNTH}:skill-version", "skill_version_id": f"{SYNTH}:skill-id",
            "content_digest": "sha256:" + "2" * 64, "candidate_version_ref": f"{SYNTH}:candidate-version",
            "derivation_evidence_ref": f"{SYNTH}:evidence", "lifecycle_status_ref": f"{SYNTH}:lifecycle",
        },
        "LIFECYCLE_DECISION_APPENDED": {
            "lifecycle_event_ref": f"{SYNTH}:lifecycle-event", "subject_ref": f"{SYNTH}:candidate-version",
            "prior_status": "NOT_APPLICABLE", "next_status": "PROPOSED", "decision_ref": f"{SYNTH}:decision",
            "evidence_snapshot_ref": f"{SYNTH}:evidence", "predecessor_lifecycle_event_ref": NA,
        },
        "TRIAGE_ASSESSMENT_APPENDED": {
            "counterexample_record_ref": f"{SYNTH}:counterexample", "p4_triage_sidecar_ref": f"{SYNTH}:triage-sidecar",
            "prediction_record_ref": f"{SYNTH}:prediction", "transition_event_ref": f"{SYNTH}:transition",
            "assessment_state": "UNRESOLVED",
        },
        "EVIDENCE_USE_APPENDED": {
            "evidence_ref": f"{SYNTH}:evidence-ref", "prior_role_ref": f"{SYNTH}:validation-role",
            "new_role_ref": f"{SYNTH}:refinement-role", "subject_version_refs": [f"{SYNTH}:successor"],
            "decision_ref": f"{SYNTH}:decision", "validation_eligibility_effect": f"{SYNTH}:ineligible-for-descendants",
        },
        "FALLBACK_SELECTED": {
            "trigger_event_ref": f"{SYNTH}:failure", "fallback_policy_ref": f"{SYNTH}:fallback-policy",
            "fallback_decision": "ABSTAIN", "reserved_budget_ref": NA, "result_event_ref": NA,
        },
        "STOP_OR_FAILURE": {
            "stage": f"{SYNTH}:stage", "reason_code": f"{SYNTH}:timeout", "affected_refs": [f"{SYNTH}:intent"],
            "stop_scope": f"{SYNTH}:invocation", "recoverable": UNKNOWN, "review_required": True,
        },
        "COST_MEASURED": {
            "cost_record_id": f"{SYNTH}:cost", "resource_dimension": f"{SYNTH}:actions", "amount": KNOWN,
            "unit_ref": f"{SYNTH}:unit:count", "measurement_method_ref": f"{SYNTH}:counter",
            "stage": f"{SYNTH}:invocation", "scope_ref": f"{SYNTH}:episode", "arm_ref": f"{SYNTH}:arm",
            "budget_contract_ref": f"{SYNTH}:budget", "window_start_ref": NA, "window_end_ref": NA,
        },
        "EVENT_CORRECTION_APPENDED": {
            "supersedes_event_ref": f"{SYNTH}:prior-event", "correction_reason": f"{SYNTH}:reason",
            "corrected_fields_or_payload_ref": f"{SYNTH}:corrected-payload", "approver_ref": f"{SYNTH}:reviewer",
            "integrity_impact": f"{SYNTH}:no-outcome-change",
        },
    }


def event_template(event_type: str, payload: dict | None = None, **overrides) -> dict:
    template = {
        "event_type": event_type,
        "stream_id": "synthetic:stream:journal-test",
        "activity_ref": "synthetic:activity:journal-test",
        "data_role_ref": "SYNTHETIC_FIXTURE",
        "producer": {
            "producer_id": "local:t2t-eventlog-test",
            "producer_class": "SOFTWARE",
            "producer_version_ref": "local:test-v1",
        },
        "access_class_ref": "SYNTHETIC_FIXTURE",
        "causal_parent_event_refs": [],
        "payload": copy.deepcopy(payload if payload is not None else payloads()[event_type]),
        "provenance_refs": ["synthetic:manifest:journal-test"],
    }
    template.update(overrides)
    return template


def append_observation(journal: EventJournal, suffix: str = "1") -> dict:
    payload = payloads()["OBSERVATION_RECORDED"]
    payload["observation_id"] = f"synthetic:observation:{suffix}"
    payload["raw_observation_ref"] = f"synthetic:raw:{suffix}"
    return journal.append(event_template("OBSERVATION_RECORDED", payload))


def append_prediction_action_chain(journal: EventJournal) -> tuple[dict, dict, dict]:
    observation = append_observation(journal, "chain")
    request = journal.append(
        event_template(
            "ACTION_REQUESTED",
            {
                "intent_id": "synthetic:intent:chain",
                "agent_or_arm_ref": "synthetic:arm:I0",
                "observation_event_refs": [observation["event_id"]],
                "proposed_action_ref": "synthetic:action:chain",
                "required_prediction": True,
                "remaining_budget_ref": "synthetic:budget:before",
            },
            causal_parent_event_refs=[observation["event_id"]],
        )
    )
    prediction = journal.append(
        event_template(
            "PREDICTION_FROZEN",
            {
                "prediction_record_ref": "synthetic:prediction:chain",
                "skill_version_ref": "synthetic:skill:v1",
                "baseline_adapter_ref": NA,
                "intent_id": "synthetic:intent:chain",
                "target_effect_ref": "synthetic:effect:chain",
            },
            causal_parent_event_refs=[request["event_id"]],
        )
    )
    dispatch = journal.append(
        event_template(
            "ACTION_DISPATCHED",
            {
                "intent_id": "synthetic:intent:chain",
                "action_ref": "synthetic:action:chain",
                "dispatch_ref": "synthetic:dispatch:chain",
                "prediction_record_ref": "synthetic:prediction:chain",
                "budget_before_ref": "synthetic:budget:before",
            },
            causal_parent_event_refs=[prediction["event_id"]],
        )
    )
    return observation, prediction, dispatch


def rehash_test_log(journal: EventJournal, events: list[dict]) -> None:
    """Rewrite a fixture log and its local head after a deliberate corruption."""
    previous = None
    for event in events:
        if previous is None:
            event["integrity"].pop("previous_digest", None)
        else:
            event["integrity"]["previous_digest"] = previous
        event["integrity"]["content_digest"] = event_digest(event)
        previous = event["integrity"]["content_digest"]
    journal.path.write_bytes(b"".join(canonical_json_bytes(event) + b"\n" for event in events))
    journal._write_head(
        line_count=len(events), head_digest=previous, file_size=journal.path.stat().st_size
    )


def test_machine_schema_meta_validates_and_covers_every_declared_type():
    check_schema()
    fixtures = payloads()
    assert len(fixtures) == 22
    for index, (event_type, payload) in enumerate(fixtures.items(), start=1):
        validate_event(envelope(event_type, payload, event_id=f"synthetic:event:{index}"))


def test_unknown_type_and_unexpected_fields_are_rejected():
    unknown = envelope("EVALUATOR_OUTCOME_RECORDED", {"outcome_ref": "synthetic:outcome"})
    with pytest.raises(EventValidationError):
        validate_event(unknown)

    extra = envelope("CANDIDATE_VERSION_EMITTED", payloads()["CANDIDATE_VERSION_EMITTED"])
    extra["unversioned_extra"] = "not allowed"
    with pytest.raises(EventValidationError):
        validate_event(extra)

    wrong_version = envelope("OBSERVATION_RECORDED", payloads()["OBSERVATION_RECORDED"])
    wrong_version["event_schema_version"] = "T2T-EventSchema-v99"
    with pytest.raises(EventValidationError):
        validate_event(wrong_version)

    malformed_digest = envelope("OBSERVATION_RECORDED", payloads()["OBSERVATION_RECORDED"])
    malformed_digest["integrity"]["content_digest"] = "not-a-sha256-digest"
    with pytest.raises(EventValidationError):
        validate_event(malformed_digest)


def test_unknown_false_not_applicable_and_absent_remain_distinct():
    observation = payloads()["OBSERVATION_RECORDED"]
    for tagged in (KNOWN, KNOWN_FALSE, UNKNOWN, NA):
        candidate = envelope("OBSERVATION_RECORDED", {**observation, "source_time": tagged})
        validate_event(candidate)
    missing_required = dict(observation)
    del missing_required["source_time"]
    with pytest.raises(EventValidationError):
        validate_event(envelope("OBSERVATION_RECORDED", missing_required))


def test_candidate_event_cannot_add_executable_policy():
    candidate_payload = payloads()["CANDIDATE_VERSION_EMITTED"]
    candidate_payload["executable_policy_ref"] = "synthetic:policy:bad"
    with pytest.raises(EventValidationError):
        validate_event(envelope("CANDIDATE_VERSION_EMITTED", candidate_payload))


def test_digest_profile_is_stable_and_semantic_change_changes_digest():
    event = envelope("OBSERVATION_RECORDED", payloads()["OBSERVATION_RECORDED"])
    assert event_digest(event) == event_digest(copy.deepcopy(event))
    changed = copy.deepcopy(event)
    changed["payload"]["normalization_status"] = "FAILED"
    assert event_digest(changed) != event_digest(event)
    assert canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'


def test_append_read_reopen_and_verify_with_monotone_sequences(tmp_path: Path):
    path = tmp_path / "fixture.jsonl"
    journal = EventJournal(path)
    first = append_observation(journal, "first")
    second = journal.append(
        event_template(
            "OBSERVATION_RECORDED",
            {**payloads()["OBSERVATION_RECORDED"], "observation_id": "synthetic:observation:second"},
        )
    )
    assert first["stream_seq"] == 0
    assert second["stream_seq"] == 1
    assert first["event_id"] != second["event_id"]
    assert first["recorded_at"] < second["recorded_at"]
    assert second["integrity"]["previous_digest"] == first["integrity"]["content_digest"]
    assert journal.verify()["event_count"] == 2
    assert len(journal.read_all()) == 2
    reopened = EventJournal(path)
    assert reopened.verify()["valid"] is True


def test_rejects_caller_controlled_fields_and_non_synthetic_refs(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    template = event_template("OBSERVATION_RECORDED")
    template["event_id"] = "synthetic:caller-id"
    with pytest.raises(EventValidationError):
        journal.append(template)
    assert journal.read_all() == []

    external = event_template("OBSERVATION_RECORDED")
    external["payload"]["raw_observation_ref"] = "task-42/raw"
    with pytest.raises(SyntheticScopeError):
        journal.append(external)
    assert journal.read_all() == []

    wrong_access = event_template("OBSERVATION_RECORDED", access_class_ref="CONFIRMATORY")
    with pytest.raises(SyntheticScopeError):
        journal.append(wrong_access)


def test_required_prediction_must_precede_dispatch(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    observation = append_observation(journal, "order")
    request = journal.append(
        event_template(
            "ACTION_REQUESTED",
            {
                "intent_id": "synthetic:intent:order",
                "agent_or_arm_ref": "synthetic:arm:I0",
                "observation_event_refs": [observation["event_id"]],
                "proposed_action_ref": "synthetic:action:order",
                "required_prediction": True,
                "remaining_budget_ref": "synthetic:budget:order",
            },
            causal_parent_event_refs=[observation["event_id"]],
        )
    )
    with pytest.raises(EventOrderError, match="required pre-action prediction"):
        journal.append(
            event_template(
                "ACTION_DISPATCHED",
                {
                    "intent_id": "synthetic:intent:order",
                    "action_ref": "synthetic:action:order",
                    "dispatch_ref": "synthetic:dispatch:order",
                    "prediction_record_ref": NA,
                    "budget_before_ref": "synthetic:budget:order",
                },
                causal_parent_event_refs=[request["event_id"]],
            )
        )
    assert len(journal.read_all()) == 2


def test_late_prediction_after_dispatch_is_rejected(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    observation = append_observation(journal, "late")
    request = journal.append(
        event_template(
            "ACTION_REQUESTED",
            {
                "intent_id": "synthetic:intent:late",
                "agent_or_arm_ref": "synthetic:arm:B0",
                "observation_event_refs": [observation["event_id"]],
                "proposed_action_ref": "synthetic:action:late",
                "required_prediction": False,
                "remaining_budget_ref": "synthetic:budget:late",
            },
            causal_parent_event_refs=[observation["event_id"]],
        )
    )
    dispatch = journal.append(
        event_template(
            "ACTION_DISPATCHED",
            {
                "intent_id": "synthetic:intent:late", "action_ref": "synthetic:action:late",
                "dispatch_ref": "synthetic:dispatch:late", "prediction_record_ref": NA,
                "budget_before_ref": "synthetic:budget:late",
            },
            causal_parent_event_refs=[request["event_id"]],
        )
    )
    with pytest.raises(EventOrderError, match="after dispatch"):
        journal.append(
            event_template(
                "PREDICTION_FROZEN",
                {
                    "prediction_record_ref": "synthetic:prediction:too-late", "skill_version_ref": NA,
                    "baseline_adapter_ref": "synthetic:baseline:B0", "intent_id": "synthetic:intent:late",
                    "target_effect_ref": "synthetic:effect:late",
                },
                causal_parent_event_refs=[dispatch["event_id"]],
            )
        )
    assert len(journal.read_all()) == 3


def test_valid_prediction_dispatch_effect_chain_is_preserved(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    observation, prediction, dispatch = append_prediction_action_chain(journal)
    action_result = journal.append(
        event_template(
            "ACTION_RESULT_RECORDED",
            {
                "intent_id": "synthetic:intent:chain",
                "dispatch_event_ref": dispatch["event_id"],
                "result_status": "ACCEPTED",
                "environment_response": KNOWN,
                "budget_after_ref": "synthetic:budget:after",
            },
            causal_parent_event_refs=[dispatch["event_id"]],
        )
    )
    post_observation = journal.append(
        event_template(
            "OBSERVATION_RECORDED",
            {
                **payloads()["OBSERVATION_RECORDED"],
                "observation_id": "synthetic:observation:post",
                "raw_observation_ref": "synthetic:raw:post",
            },
            causal_parent_event_refs=[action_result["event_id"]],
        )
    )
    transition = journal.append(
        event_template(
            "TRANSITION_OBSERVED",
            {
                "pre_observation_event_ref": observation["event_id"],
                "action_result_event_ref": action_result["event_id"],
                "post_observation_event_ref": post_observation["event_id"],
                "observed_effect": KNOWN,
                "representation_ref": "synthetic:representation:v1",
                "source_time": UNKNOWN,
            },
            causal_parent_event_refs=[action_result["event_id"], post_observation["event_id"]],
        )
    )
    journal.append(
        event_template(
            "EFFECT_ASSESSED",
            {
                "effect_assessment_ref": "synthetic:assessment:1",
                "prediction_record_ref": prediction["payload"]["prediction_record_ref"],
                "transition_event_ref": transition["event_id"],
                "assessment_status": "MATCH",
                "comparator_ref": "synthetic:comparator:v1",
            },
            causal_parent_event_refs=[prediction["event_id"], transition["event_id"]],
        )
    )
    assert journal.verify()["event_count"] == 8


def test_correction_appends_without_mutating_prior_event(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    original = append_observation(journal, "corrected")
    original_bytes = journal.path.read_bytes()
    correction = journal.append(
        event_template(
            "EVENT_CORRECTION_APPENDED",
            {
                "supersedes_event_ref": original["event_id"],
                "correction_reason": "synthetic:reason:typo",
                "corrected_fields_or_payload_ref": "synthetic:corrected-payload:v1",
                "approver_ref": "synthetic:reviewer:fixture",
                "integrity_impact": "synthetic:impact:none",
            },
            causal_parent_event_refs=[original["event_id"]],
            supersedes_event_ref=original["event_id"],
        )
    )
    events = journal.read_all()
    assert len(events) == 2
    assert events[0]["event_id"] == original["event_id"]
    assert events[0]["payload"] == original["payload"]
    assert journal.path.read_bytes().startswith(original_bytes)
    assert correction["event_id"] != original["event_id"]


def test_tamper_and_partial_tail_fail_closed(tmp_path: Path):
    path = tmp_path / "fixture.jsonl"
    journal = EventJournal(path)
    append_observation(journal, "tamper")
    original = path.read_bytes()
    path.write_bytes(original.replace(b"NOT_STARTED", b"FAILED", 1))
    with pytest.raises(JournalIntegrityError):
        EventJournal(path)

    path2 = tmp_path / "partial.jsonl"
    journal2 = EventJournal(path2)
    append_observation(journal2, "partial")
    path2.write_bytes(path2.read_bytes().rstrip(b"\n")[:-4])
    with pytest.raises(JournalIntegrityError):
        EventJournal(path2)


def test_invalid_json_duplicate_id_and_sequence_regression_fail_closed(tmp_path: Path):
    invalid_path = tmp_path / "invalid-json.jsonl"
    invalid_journal = EventJournal(invalid_path)
    append_observation(invalid_journal, "invalid-json")
    invalid_path.write_bytes(b"{not-json}\n")
    with pytest.raises(JournalIntegrityError, match="invalid JSON"):
        EventJournal(invalid_path)

    duplicate_path = tmp_path / "duplicate-id.jsonl"
    duplicate_journal = EventJournal(duplicate_path)
    append_observation(duplicate_journal, "duplicate-one")
    append_observation(duplicate_journal, "duplicate-two")
    duplicate_events = duplicate_journal.read_all()
    duplicate_events[1]["event_id"] = duplicate_events[0]["event_id"]
    rehash_test_log(duplicate_journal, duplicate_events)
    with pytest.raises(JournalIntegrityError, match="duplicate event_id"):
        EventJournal(duplicate_path)

    sequence_path = tmp_path / "sequence-regression.jsonl"
    sequence_journal = EventJournal(sequence_path)
    append_observation(sequence_journal, "sequence-one")
    append_observation(sequence_journal, "sequence-two")
    sequence_events = sequence_journal.read_all()
    sequence_events[1]["stream_seq"] = 0
    rehash_test_log(sequence_journal, sequence_events)
    with pytest.raises(JournalIntegrityError, match="stream sequence"):
        EventJournal(sequence_path)


def test_head_checkpoint_detects_valid_prefix_truncation(tmp_path: Path):
    path = tmp_path / "fixture.jsonl"
    journal = EventJournal(path)
    append_observation(journal, "one")
    append_observation(journal, "two")
    complete = path.read_bytes().splitlines(keepends=True)
    path.write_bytes(complete[0])
    with pytest.raises(JournalIntegrityError, match="checkpoint"):
        EventJournal(path)


def test_unknown_cost_stays_unknown_not_zero(tmp_path: Path):
    journal = EventJournal(tmp_path / "cost.jsonl")
    cost = payloads()["COST_MEASURED"]
    cost["amount"] = UNKNOWN
    event = journal.append(event_template("COST_MEASURED", cost))
    assert event["payload"]["amount"] == UNKNOWN
    assert journal.read_all()[0]["payload"]["amount"]["availability"] == "UNKNOWN"


def test_missing_parent_and_restricted_outcome_event_are_rejected(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    template = event_template(
        "OBSERVATION_RECORDED",
        causal_parent_event_refs=["synthetic:event:not-present"],
    )
    with pytest.raises(EventOrderError):
        journal.append(template)

    restricted = event_template(
        "EVALUATOR_OUTCOME_RECORDED",
        {"outcome_ref": "synthetic:outcome:must-not-enter"},
    )
    with pytest.raises(EventValidationError):
        journal.append(restricted)
    assert journal.read_all() == []


def test_stream_sequences_are_safe_under_local_concurrent_appends(tmp_path: Path):
    from concurrent.futures import ThreadPoolExecutor

    path = tmp_path / "concurrent.jsonl"

    def append_one(index: int) -> str:
        return EventJournal(path).append(
            event_template(
                "OBSERVATION_RECORDED",
                {
                    **payloads()["OBSERVATION_RECORDED"],
                    "observation_id": f"synthetic:observation:thread-{index}",
                    "raw_observation_ref": f"synthetic:raw:thread-{index}",
                },
            )
        )["event_id"]

    with ThreadPoolExecutor(max_workers=4) as pool:
        ids = list(pool.map(append_one, range(12)))
    assert len(set(ids)) == 12
    events = EventJournal(path).read_all()
    assert [event["stream_seq"] for event in events] == list(range(12))


def test_equal_timestamps_are_rejected_even_if_local_hashes_are_recomputed(tmp_path: Path):
    path = tmp_path / "timestamps.jsonl"
    journal = EventJournal(path)
    append_observation(journal, "timestamp-1")
    journal.append(
        event_template(
            "OBSERVATION_RECORDED",
            {**payloads()["OBSERVATION_RECORDED"], "observation_id": "synthetic:observation:timestamp-2"},
        )
    )
    events = journal.read_all()
    events[1]["recorded_at"] = events[0]["recorded_at"]
    rehash_test_log(journal, events)
    with pytest.raises(JournalIntegrityError, match="non-increasing stream timestamp"):
        EventJournal(path)


def test_jsonl_contains_only_valid_json_records(tmp_path: Path):
    journal = EventJournal(tmp_path / "fixture.jsonl")
    append_observation(journal, "jsonl")
    records = [json.loads(line) for line in journal.path.read_text(encoding="utf-8").splitlines()]
    assert len(records) == 1
    assert records[0]["event_type"] == "OBSERVATION_RECORDED"
