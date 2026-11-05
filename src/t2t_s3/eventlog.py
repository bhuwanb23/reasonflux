"""Explicit local JSONL audit records for S3 package integrations.

This module performs no experiment or outcome query. Calls append only when an
explicit caller supplies a destination path and event; no log is written on import.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .arms import Prediction
from .world import Effect, RelationalUnlockWorld, UnlockAction, UnlockState

SCHEMA_VERSION = "t2t-s3-event-v1"


def _effect_payload(effect: Effect) -> dict[str, bool]:
    return {"target_opened": effect.target_opened, "agent_advanced": effect.agent_advanced}


def observation_digest(state: UnlockState, action: UnlockAction) -> str:
    payload = {
        "state": RelationalUnlockWorld.exact_state_signature(state),
        "action": (action.key_id, action.target_id),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class AuditEvent:
    schema_version: str
    event_type: str
    package_version: str
    event_id: str
    context_id: str | None
    payload: Mapping[str, Any]

    def to_json_line(self) -> str:
        return json.dumps(
            {
                "schema_version": self.schema_version,
                "event_type": self.event_type,
                "package_version": self.package_version,
                "event_id": self.event_id,
                "context_id": self.context_id,
                "payload": dict(self.payload),
            },
            sort_keys=True,
            separators=(",", ":"),
        )


def prediction_event(
    *, event_id: str, package_version: str, arm_id: str, cell_id: str, state: UnlockState,
    action: UnlockAction, prediction: Prediction, resource_cost: Mapping[str, int] | None = None,
) -> AuditEvent:
    """Record predictions and abstentions without any observed target outcome."""
    payload: dict[str, Any] = {
        "arm_id": arm_id,
        "cell_id": cell_id,
        "observation_sha256": observation_digest(state, action),
        "action": {"key_id": action.key_id, "target_id": action.target_id},
        "status": prediction.status,
        "reason": prediction.reason,
        "prediction": None if prediction.effect is None else _effect_payload(prediction.effect),
        "source_trace_ids": list(prediction.source_trace_ids),
        "resource_cost": dict(resource_cost or {}),
    }
    return AuditEvent(SCHEMA_VERSION, "prediction", package_version, event_id, state.context_id, payload)


def score_event(
    *, event_id: str, package_version: str, arm_id: str, cell_id: str, state: UnlockState,
    action: UnlockAction, prediction: Prediction, observed_effect: Effect,
) -> AuditEvent:
    """Append-only scoring record; it cannot update or refit an arm."""
    exact = prediction.issued and prediction.effect == observed_effect
    payload = {
        "arm_id": arm_id,
        "cell_id": cell_id,
        "observation_sha256": observation_digest(state, action),
        "prediction_status": prediction.status,
        "predicted_effect": None if prediction.effect is None else _effect_payload(prediction.effect),
        "observed_effect": _effect_payload(observed_effect),
        "all_context_exact_score": int(exact),
        "scoring_rule": "correct=1; wrong, abstain, invalid, or missing=0",
    }
    return AuditEvent(SCHEMA_VERSION, "score", package_version, event_id, state.context_id, payload)


def fit_event(*, event_id: str, package_version: str, arm_id: str, source_trace_ids: tuple[str, ...], model_digest: str) -> AuditEvent:
    return AuditEvent(
        SCHEMA_VERSION,
        "fit",
        package_version,
        event_id,
        None,
        {"arm_id": arm_id, "source_trace_ids": list(source_trace_ids), "model_sha256": model_digest},
    )


def deviation_event(*, event_id: str, package_version: str, deviation_code: str, details: str) -> AuditEvent:
    return AuditEvent(
        SCHEMA_VERSION,
        "protocol_deviation",
        package_version,
        event_id,
        None,
        {"deviation_code": deviation_code, "details": details},
    )


def append_event(path: str | Path, event: AuditEvent) -> None:
    """Append one event to an explicitly selected local JSONL file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as stream:
        stream.write(event.to_json_line() + "\n")
