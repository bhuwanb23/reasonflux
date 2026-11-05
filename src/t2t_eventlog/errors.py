"""Errors for the local-only T2T event journal prototype."""


class EventJournalError(Exception):
    """Base class for event-journal contract failures."""


class EventValidationError(EventJournalError):
    """Raised when an event fails JSON Schema or semantic validation."""


class JournalIntegrityError(EventJournalError):
    """Raised when the append-only log or its checkpoint cannot be verified."""


class EventOrderError(EventJournalError):
    """Raised when a causal or pre-action ordering rule is violated."""


class SyntheticScopeError(EventJournalError):
    """Raised when a reference is outside the local synthetic-only scope."""
