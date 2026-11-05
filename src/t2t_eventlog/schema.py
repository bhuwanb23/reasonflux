"""JSON Schema validation for the P6 local event prototype."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

from .errors import EventValidationError

SCHEMA_VERSION = "T2T-EventSchema-v1.0.0-draft"
DEFAULT_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "05_trace_to_transfer"
    / "p6"
    / "event_schema_v1.json"
)


@lru_cache(maxsize=4)
def _load_validator(schema_path: str) -> Draft202012Validator:
    path = Path(schema_path)
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EventValidationError(f"cannot load event schema at {path}: {exc}") from exc
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise EventValidationError(f"event schema is invalid: {exc.message}") from exc
    if schema.get("$id") != "urn:t2t:event-schema:1.0.0-draft":
        raise EventValidationError("unexpected event schema $id")
    return Draft202012Validator(schema, format_checker=FormatChecker())


def schema_path(path: str | Path | None = None) -> Path:
    """Return the selected event schema path."""
    return Path(path) if path is not None else DEFAULT_SCHEMA_PATH


def validate_event(event: Any, *, path: str | Path | None = None) -> None:
    """Raise :class:`EventValidationError` unless `event` matches the schema."""
    validator = _load_validator(str(schema_path(path).resolve()))
    errors = sorted(
        validator.iter_errors(event),
        key=lambda error: (tuple(str(part) for part in error.absolute_path), error.message),
    )
    if errors:
        rendered = []
        for error in errors[:8]:
            location = ".".join(str(part) for part in error.absolute_path) or "$"
            rendered.append(f"{location}: {error.message}")
        remainder = len(errors) - len(rendered)
        suffix = f" (+{remainder} more)" if remainder else ""
        raise EventValidationError("; ".join(rendered) + suffix)


def check_schema(*, path: str | Path | None = None) -> None:
    """Load and meta-validate the selected Draft 2020-12 schema."""
    _load_validator(str(schema_path(path).resolve()))
