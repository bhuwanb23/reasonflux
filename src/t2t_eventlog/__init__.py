"""Local-only T2T event validation and append-only journal prototype."""

from .canonical import DIGEST_PROFILE, canonical_json_bytes, event_digest
from .errors import (
    EventJournalError,
    EventOrderError,
    EventValidationError,
    JournalIntegrityError,
    SyntheticScopeError,
)
from .journal import EventJournal
from .schema import SCHEMA_VERSION, check_schema, validate_event

__all__ = [
    "DIGEST_PROFILE",
    "SCHEMA_VERSION",
    "EventJournal",
    "EventJournalError",
    "EventOrderError",
    "EventValidationError",
    "JournalIntegrityError",
    "SyntheticScopeError",
    "canonical_json_bytes",
    "check_schema",
    "event_digest",
    "validate_event",
]
