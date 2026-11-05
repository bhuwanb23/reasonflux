"""Prototype-only JSON canonicalization and event digests.

This profile is intentionally local to the synthetic prototype. It does not
resolve the project-wide canonicalization profile left open by P2.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

DIGEST_PROFILE = "t2t-python-json-c14n-v1"


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically within this Python prototype profile."""
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"value is not canonicalizable JSON: {exc}") from exc
    return text.encode("utf-8")


def event_digest(event: Mapping[str, Any]) -> str:
    """Hash an event excluding its own content digest.

    The digest profile and `previous_digest` remain inside the hashed content,
    making the journal chain tamper-evident within the local prototype.
    """
    material = dict(event)
    integrity = dict(material.get("integrity", {}))
    integrity.pop("content_digest", None)
    material["integrity"] = integrity
    digest = hashlib.sha256(canonical_json_bytes(material)).hexdigest()
    return f"sha256:{digest}"
