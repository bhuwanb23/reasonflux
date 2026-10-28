"""Stable invariant identity fingerprint (Phase 11C-1)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from core.invariant import Invariant
from core.states import InvariantState
from invariants.specification._util import family_set
from invariants.specification.policy import InvariantPolicy
from invariants.specification.qualification import qualify_invariant


@dataclass(slots=True)
class InvariantIdentity:
    """Stable identity for an invariant (origin + pattern + families)."""

    origin: str
    pattern_signature: tuple[str, ...]
    task_families: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.origin or not str(self.origin).strip():
            raise ValueError("origin must be a non-empty string")
        if not self.pattern_signature:
            raise ValueError("pattern_signature must not be empty")

    @property
    def fingerprint(self) -> str:
        payload = {
            "origin": self.origin.strip().lower(),
            "pattern": [str(s).strip().lower() for s in self.pattern_signature],
        }
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]

    @property
    def invariant_id(self) -> str:
        return f"INV-{self.fingerprint}"

    @classmethod
    def from_invariant(cls, invariant: Invariant) -> InvariantIdentity:
        return cls(
            origin=invariant.origin or "unknown",
            pattern_signature=tuple(invariant.pattern_signature),
            task_families=tuple(sorted(family_set(invariant))),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "origin": self.origin,
            "pattern_signature": list(self.pattern_signature),
            "task_families": list(self.task_families),
            "fingerprint": self.fingerprint,
            "invariant_id": self.invariant_id,
        }


def can_become_skill_candidate(
    invariant: Invariant,
    policy: InvariantPolicy | None = None,
) -> bool:
    """True when an invariant has transfer-verified evidence for SCT handoff."""
    return (
        invariant.state == InvariantState.TRANSFER_VERIFIED
        and invariant.evidence.transfer_events
        >= (policy or InvariantPolicy()).min_transfer_events
        and not qualify_invariant(invariant, policy)
    )
