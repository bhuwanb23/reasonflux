"""Local-only append-only JSONL journal for synthetic T2T contract fixtures.

This is a single-machine prototype, not a production event store or a secure
boundary for real or restricted data.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping

try:  # POSIX
    import fcntl
except ImportError:  # pragma: no cover - Windows
    fcntl = None  # type: ignore[assignment]
    import msvcrt

from .canonical import DIGEST_PROFILE, canonical_json_bytes, event_digest
from .errors import (
    EventOrderError,
    EventValidationError,
    JournalIntegrityError,
    SyntheticScopeError,
)
from .schema import SCHEMA_VERSION, validate_event

_CONTROLLED_FIELDS = {
    "event_id",
    "event_schema_version",
    "recorded_at",
    "stream_seq",
    "integrity",
}
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-8][0-9a-fA-F]{3}-"
    r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)


class EventJournal:
    """Append, read and verify a single-writer local JSONL journal.

    Events are validated before append. The JSONL file is append-only through
    this API; a separately updated `.head.json` checkpoint detects accidental
    truncation or disagreement between the log and its last acknowledged head.
    The checkpoint is metadata, not an event, and this local construction is
    tamper-evident rather than tamper-proof.

    The writer accepts only synthetic/local references and the exact
    `SYNTHETIC_FIXTURE` access class. It has no network, dataset, model,
    evaluator, or environment integration.
    """

    def __init__(self, path: str | Path, *, schema_path: str | Path | None = None):
        self.path = Path(path).expanduser().absolute()
        self.head_path = self.path.with_name(self.path.name + ".head.json")
        self.lock_path = self.path.with_name(self.path.name + ".lock")
        self.schema_path = Path(schema_path) if schema_path is not None else None
        self._thread_lock = threading.RLock()

        for candidate in (self.path, self.head_path, self.lock_path):
            if candidate.is_symlink():
                raise JournalIntegrityError(f"symlink journal paths are not allowed: {candidate}")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._locked():
            if not self.path.exists() and not self.head_path.exists():
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
                self._write_head(line_count=0, head_digest=None, file_size=0)
                self._fsync_directory()
            elif self.path.exists() != self.head_path.exists():
                raise JournalIntegrityError("journal and head checkpoint must both exist")
            else:
                self._read_verified_unlocked()

    @contextmanager
    def _locked(self) -> Iterator[None]:
        """Serialize local writers/readers with an advisory file lock.

        Uses ``flock`` on POSIX and ``msvcrt.locking`` on Windows so the
        journal and its hash-frozen fixtures behave identically on both
        platforms. This remains a single-machine lock, not a distributed one.
        """
        with self._thread_lock:
            fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
            try:
                if fcntl is not None:
                    fcntl.flock(fd, fcntl.LOCK_EX)
                else:  # pragma: no cover - Windows
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
                yield
            finally:
                if fcntl is not None:
                    fcntl.flock(fd, fcntl.LOCK_UN)
                else:  # pragma: no cover - Windows
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                os.close(fd)

    def append(self, event_template: Mapping[str, Any]) -> dict[str, Any]:
        """Append one event template and return the fully assigned event.

        The caller supplies `event_type`, `stream_id`, `activity_ref`, producer,
        access class, causal parents, payload and provenance. The journal assigns
        event ID, schema version, timestamp, per-stream sequence and integrity.
        Caller-supplied values for those controlled fields are rejected.
        """
        if not isinstance(event_template, Mapping):
            raise EventValidationError("event template must be a mapping")
        if _CONTROLLED_FIELDS.intersection(event_template):
            raise EventValidationError(
                "journal-controlled fields may not be supplied: "
                + ", ".join(sorted(_CONTROLLED_FIELDS.intersection(event_template)))
            )
        template = copy.deepcopy(dict(event_template))
        self._check_synthetic_scope(template)

        with self._locked():
            events = self._read_verified_unlocked()
            self._check_parents_exist(template, events)
            event = template
            event["event_id"] = str(uuid.uuid4())
            event["event_schema_version"] = SCHEMA_VERSION
            stream_id = event.get("stream_id")
            if not isinstance(stream_id, str):
                raise EventValidationError("stream_id is required")
            same_stream = [e for e in events if e["stream_id"] == stream_id]
            previous_in_stream = same_stream[-1] if same_stream else None
            event["stream_seq"] = (previous_in_stream["stream_seq"] + 1) if previous_in_stream else 0
            recorded_at = datetime.now(timezone.utc)
            if previous_in_stream:
                prior_time = self._parse_time(previous_in_stream["recorded_at"])
                if recorded_at <= prior_time:
                    recorded_at = prior_time + timedelta(microseconds=1)
            event["recorded_at"] = recorded_at.isoformat(timespec="microseconds").replace("+00:00", "Z")

            previous_digest = events[-1]["integrity"]["content_digest"] if events else None
            integrity: dict[str, str] = {"digest_profile": DIGEST_PROFILE}
            if previous_digest is not None:
                integrity["previous_digest"] = previous_digest
            event["integrity"] = integrity
            event["integrity"]["content_digest"] = event_digest(event)

            validate_event(event, path=self.schema_path)
            self._check_synthetic_scope(event)
            self._check_event_semantics(event, events)
            line = canonical_json_bytes(event) + b"\n"

            flags = os.O_CREAT | os.O_APPEND | os.O_WRONLY
            fd = os.open(self.path, flags, 0o600)
            try:
                written = os.write(fd, line)
                if written != len(line):
                    raise JournalIntegrityError("short append; journal is now held for verification")
                os.fsync(fd)
            finally:
                os.close(fd)

            new_size = self.path.stat().st_size
            self._write_head(
                line_count=len(events) + 1,
                head_digest=event["integrity"]["content_digest"],
                file_size=new_size,
            )
            self._fsync_directory()
            return copy.deepcopy(event)

    def read_all(self) -> list[dict[str, Any]]:
        """Return verified events in append order."""
        with self._locked():
            return copy.deepcopy(self._read_verified_unlocked())

    def verify(self) -> dict[str, Any]:
        """Verify schema, event hashes, chain, ordering and head checkpoint."""
        with self._locked():
            events = self._read_verified_unlocked()
            head = self._read_head()
            return {
                "valid": True,
                "event_count": len(events),
                "head_digest": head["head_digest"],
                "file_size": head["file_size"],
                "digest_profile": DIGEST_PROFILE,
                "scope": "SYNTHETIC_FIXTURE_ONLY",
            }

    def _read_verified_unlocked(self) -> list[dict[str, Any]]:
        try:
            raw = self.path.read_bytes()
        except OSError as exc:
            raise JournalIntegrityError(f"cannot read journal: {exc}") from exc
        if raw and not raw.endswith(b"\n"):
            raise JournalIntegrityError("journal has a partial final line")
        lines = raw.splitlines()
        events: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        last_seq: dict[str, int] = {}
        last_time: dict[str, datetime] = {}
        previous_digest: str | None = None
        by_id: dict[str, dict[str, Any]] = {}

        for line_number, line in enumerate(lines, start=1):
            try:
                event = json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise JournalIntegrityError(f"invalid JSON on line {line_number}: {exc}") from exc
            try:
                validate_event(event, path=self.schema_path)
            except EventValidationError as exc:
                raise JournalIntegrityError(f"schema failure on line {line_number}: {exc}") from exc
            self._check_synthetic_scope(event)

            event_id = event["event_id"]
            if event_id in seen_ids:
                raise JournalIntegrityError(f"duplicate event_id on line {line_number}")
            integrity = event["integrity"]
            if integrity["digest_profile"] != DIGEST_PROFILE:
                raise JournalIntegrityError(f"unsupported digest profile on line {line_number}")
            expected_previous = integrity.get("previous_digest")
            if expected_previous != previous_digest:
                raise JournalIntegrityError(f"broken hash chain on line {line_number}")
            expected_digest = event_digest(event)
            if integrity["content_digest"] != expected_digest:
                raise JournalIntegrityError(f"content digest mismatch on line {line_number}")

            stream_id = event["stream_id"]
            expected_seq = last_seq.get(stream_id, -1) + 1
            if event["stream_seq"] != expected_seq:
                raise JournalIntegrityError(f"stream sequence mismatch on line {line_number}")
            recorded_at = self._parse_time(event["recorded_at"])
            if stream_id in last_time and recorded_at <= last_time[stream_id]:
                raise JournalIntegrityError(f"non-increasing stream timestamp on line {line_number}")
            for parent in event["causal_parent_event_refs"]:
                if parent not in seen_ids:
                    raise JournalIntegrityError(f"missing/forward causal parent on line {line_number}")

            try:
                self._check_event_semantics(event, events)
            except (EventValidationError, EventOrderError) as exc:
                raise JournalIntegrityError(f"semantic event failure on line {line_number}: {exc}") from exc

            self._check_reference_scope(event, seen_ids)
            events.append(event)
            seen_ids.add(event_id)
            by_id[event_id] = event
            last_seq[stream_id] = event["stream_seq"]
            last_time[stream_id] = recorded_at
            previous_digest = integrity["content_digest"]

        head = self._read_head()
        if head["line_count"] != len(events):
            raise JournalIntegrityError("head checkpoint line_count does not match journal")
        if head["file_size"] != len(raw):
            raise JournalIntegrityError("head checkpoint file_size does not match journal")
        if head["head_digest"] != previous_digest:
            raise JournalIntegrityError("head checkpoint digest does not match journal")
        return events

    def _check_event_semantics(self, event: Mapping[str, Any], prior: list[dict[str, Any]]) -> None:
        """Validate local causal constraints across events already appended."""
        event_type = event["event_type"]
        payload = event["payload"]
        stream_id = event["stream_id"]
        by_id = {item["event_id"]: item for item in prior}

        def prior_event(ref: str, expected_type: str | None = None) -> dict[str, Any]:
            found = by_id.get(ref)
            if found is None:
                raise EventOrderError(f"reference is not a prior journal event: {ref}")
            if found["stream_id"] != stream_id:
                raise EventOrderError("causal event references must be in the same stream")
            if expected_type is not None and found["event_type"] != expected_type:
                raise EventOrderError(f"expected prior {expected_type}, got {found['event_type']}")
            return found

        same_stream = [item for item in prior if item["stream_id"] == stream_id]
        requests_by_intent = {
            item["payload"]["intent_id"]: item
            for item in same_stream
            if item["event_type"] == "ACTION_REQUESTED"
        }
        predictions = {
            item["payload"]["intent_id"]: item
            for item in same_stream
            if item["event_type"] == "PREDICTION_FROZEN"
        }
        dispatches = {
            item["event_id"]: item
            for item in same_stream
            if item["event_type"] == "ACTION_DISPATCHED"
        }

        if event_type == "ACTION_REQUESTED":
            if payload["intent_id"] in requests_by_intent:
                raise EventOrderError("intent_id is already used in this stream")
        elif event_type == "PREDICTION_FROZEN":
            intent_id = payload["intent_id"]
            if intent_id not in requests_by_intent:
                raise EventOrderError("prediction must follow its action request")
            if intent_id in predictions:
                raise EventOrderError("only one frozen prediction is allowed per intent")
            if any(item["payload"].get("intent_id") == intent_id for item in dispatches.values()):
                raise EventOrderError("prediction cannot be appended after dispatch")
            skill_ref = payload["skill_version_ref"]
            baseline_ref = payload["baseline_adapter_ref"]
            has_skill = isinstance(skill_ref, str)
            has_baseline = isinstance(baseline_ref, str)
            if has_skill == has_baseline:
                raise EventValidationError("prediction must identify exactly one of skill or baseline adapter")
        elif event_type == "ACTION_DISPATCHED":
            intent_id = payload["intent_id"]
            request_event = requests_by_intent.get(intent_id)
            if request_event is None:
                raise EventOrderError("dispatch must follow its action request")
            if intent_id in dispatches:
                raise EventOrderError("only one dispatch is allowed per intent")
            prediction_ref = payload["prediction_record_ref"]
            prediction_event = predictions.get(intent_id)
            required = request_event["payload"]["required_prediction"]
            if required:
                if not isinstance(prediction_ref, str) or prediction_event is None:
                    raise EventOrderError("required pre-action prediction is missing")
                if prediction_event["payload"]["prediction_record_ref"] != prediction_ref:
                    raise EventOrderError("dispatch prediction ref does not match frozen prediction")
            elif isinstance(prediction_ref, str):
                if prediction_event is None or prediction_event["payload"]["prediction_record_ref"] != prediction_ref:
                    raise EventOrderError("dispatch references a prediction not frozen for this intent")
        elif event_type == "ACTION_RESULT_RECORDED":
            dispatch = prior_event(payload["dispatch_event_ref"], "ACTION_DISPATCHED")
            if dispatch["payload"]["intent_id"] != payload["intent_id"]:
                raise EventOrderError("action result intent does not match dispatch")
        elif event_type == "TRANSITION_OBSERVED":
            prior_event(payload["action_result_event_ref"], "ACTION_RESULT_RECORDED")
            prior_event(payload["pre_observation_event_ref"], "OBSERVATION_RECORDED")
            prior_event(payload["post_observation_event_ref"], "OBSERVATION_RECORDED")
        elif event_type == "EFFECT_ASSESSED":
            prior_event(payload["transition_event_ref"], "TRANSITION_OBSERVED")
            matching = [
                item for item in same_stream
                if item["event_type"] == "PREDICTION_FROZEN"
                and item["payload"]["prediction_record_ref"] == payload["prediction_record_ref"]
            ]
            if not matching:
                raise EventOrderError("effect assessment requires a prior frozen prediction")

        if event_type == "EVENT_CORRECTION_APPENDED":
            prior_event(payload["supersedes_event_ref"])
        if event.get("supersedes_event_ref"):
            prior_event(event["supersedes_event_ref"])

    def _check_parents_exist(self, template: Mapping[str, Any], prior: list[dict[str, Any]]) -> None:
        seen = {event["event_id"] for event in prior}
        parents = template.get("causal_parent_event_refs", [])
        if not isinstance(parents, list):
            raise EventValidationError("causal_parent_event_refs must be an array")
        missing = [ref for ref in parents if ref not in seen]
        if missing:
            raise EventOrderError(f"causal parents must already exist in this journal: {missing}")

    def _check_synthetic_scope(self, event: Mapping[str, Any]) -> None:
        """Block non-synthetic access labels and unnamespaced external refs."""
        access_ref = event.get("access_class_ref")
        if access_ref not in {"SYNTHETIC_FIXTURE", "synthetic:access:SYNTHETIC_FIXTURE"}:
            raise SyntheticScopeError("local prototype accepts SYNTHETIC_FIXTURE access class only")
        role_ref = event.get("data_role_ref")
        if role_ref is not None and role_ref not in {
            "SYNTHETIC_FIXTURE", "LOCAL_TEST", "synthetic:role:SYNTHETIC_FIXTURE", "local:role:LOCAL_TEST"
        }:
            raise SyntheticScopeError("local prototype accepts synthetic/local data roles only")
        for key in ("stream_id", "activity_ref", "arm_ref", "data_role_ref"):
            value = event.get(key)
            if value is not None and value not in {"SYNTHETIC_FIXTURE", "LOCAL_TEST"} and not self._namespaced_ref(value):
                raise SyntheticScopeError(f"{key} must use a synthetic:/local: reference")
        for key in ("provenance_refs", "causal_parent_event_refs"):
            values = event.get(key, [])
            if isinstance(values, list):
                for value in values:
                    if not self._namespaced_ref(value) and not self._is_uuid(value):
                        raise SyntheticScopeError(f"{key} contains a non-synthetic reference")
        producer = event.get("producer", {})
        for key in ("producer_id", "producer_version_ref"):
            value = producer.get(key)
            if value is not None and not self._namespaced_ref(value):
                raise SyntheticScopeError(f"producer.{key} must use synthetic:/local: reference")
        self._check_reference_scope(event, set())

    def _check_reference_scope(self, value: Any, known_event_ids: set[str]) -> None:
        if isinstance(value, Mapping):
            for key, child in value.items():
                if key.endswith("_ref"):
                    self._check_ref_value(child, known_event_ids, key)
                elif key.endswith("_refs"):
                    if not isinstance(child, list):
                        raise SyntheticScopeError(f"{key} must be a reference list")
                    for ref in child:
                        self._check_ref_value(ref, known_event_ids, key)
                else:
                    self._check_reference_scope(child, known_event_ids)
        elif isinstance(value, list):
            for child in value:
                self._check_reference_scope(child, known_event_ids)

    def _check_ref_value(self, value: Any, known_event_ids: set[str], field: str) -> None:
        if isinstance(value, Mapping):
            # Explicit NOT_APPLICABLE reference tag is not an external ref.
            if value.get("availability") == "NOT_APPLICABLE":
                return
            self._check_reference_scope(value, known_event_ids)
            return
        if isinstance(value, list):
            for item in value:
                self._check_ref_value(item, known_event_ids, field)
            return
        if not isinstance(value, str):
            raise SyntheticScopeError(f"{field} must contain a string reference")
        if value in {"SYNTHETIC_FIXTURE", "LOCAL_TEST"}:
            return
        if self._namespaced_ref(value) or self._is_uuid(value) or value in known_event_ids:
            return
        raise SyntheticScopeError(f"{field} contains a non-synthetic reference: {value!r}")

    @staticmethod
    def _namespaced_ref(value: Any) -> bool:
        return isinstance(value, str) and value.startswith(("synthetic:", "local:"))

    @staticmethod
    def _is_uuid(value: Any) -> bool:
        return isinstance(value, str) and bool(_UUID_RE.fullmatch(value))

    @staticmethod
    def _parse_time(value: str) -> datetime:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except (TypeError, ValueError) as exc:
            raise JournalIntegrityError(f"invalid timestamp: {value!r}") from exc
        if parsed.tzinfo is None:
            raise JournalIntegrityError("timestamp must have an explicit timezone")
        return parsed.astimezone(timezone.utc)

    def _read_head(self) -> dict[str, Any]:
        try:
            head = json.loads(self.head_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise JournalIntegrityError(f"cannot read head checkpoint: {exc}") from exc
        if not isinstance(head, dict):
            raise JournalIntegrityError("head checkpoint must be an object")
        supplied = head.get("checkpoint_digest")
        body = {key: value for key, value in head.items() if key != "checkpoint_digest"}
        actual = "sha256:" + hashlib.sha256(canonical_json_bytes(body)).hexdigest()
        if supplied != actual:
            raise JournalIntegrityError("head checkpoint digest mismatch")
        if body.get("journal_version") != "t2t-local-jsonl-v1":
            raise JournalIntegrityError("unsupported journal checkpoint version")
        return body

    def _write_head(self, *, line_count: int, head_digest: str | None, file_size: int) -> None:
        body = {
            "journal_version": "t2t-local-jsonl-v1",
            "digest_profile": DIGEST_PROFILE,
            "line_count": line_count,
            "head_digest": head_digest,
            "file_size": file_size,
        }
        checkpoint = dict(body)
        checkpoint["checkpoint_digest"] = "sha256:" + hashlib.sha256(
            canonical_json_bytes(body)
        ).hexdigest()
        data = canonical_json_bytes(checkpoint) + b"\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.head_path.name + ".", dir=self.head_path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, self.head_path)
            os.chmod(self.head_path, 0o600)
        except Exception:
            try:
                os.unlink(temp_name)
            except OSError:
                pass
            raise

    def _fsync_directory(self) -> None:
        # Directory handles cannot be opened/fsynced portably on Windows.
        # File contents and the head checkpoint are already fsynced above.
        if os.name == "nt":  # pragma: no cover - Windows
            return
        fd = os.open(self.path.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
