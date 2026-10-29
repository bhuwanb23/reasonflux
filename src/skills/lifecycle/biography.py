"""Skill biography timeline (Phase 11D-3)."""

from __future__ import annotations

from typing import Any

from core.skill import Skill


_BIO_KEYS = (
    "birth",
    "growth_events",
    "peak_utility",
    "transfer_events",
    "failures",
    "retirement",
    "reactivations",
)


def _empty_bio() -> dict[str, Any]:
    return {
        "birth": None,
        "growth_events": [],
        "peak_utility": None,
        "transfer_events": [],
        "failures": [],
        "retirement": None,
        "reactivations": [],
    }


def build_biography(skill: Skill) -> dict[str, Any]:
    """Return biography dict (from metadata or synthesized defaults)."""
    meta = skill.metadata or {}
    raw = dict(meta.get("biography") or {})
    bio = _empty_bio()
    for key in _BIO_KEYS:
        if key in raw:
            bio[key] = raw[key]
    if bio["birth"] is None:
        bio["birth"] = {
            "skill_id": skill.skill_id,
            "source_invariant_id": skill.source_invariant_id,
            "state": skill.state.value if hasattr(skill.state, "value") else str(skill.state),
            "scv": float(skill.scv or 0.0),
        }
    peak = bio.get("peak_utility")
    current_u = float(skill.utility or 0.0)
    if peak is None or (
        isinstance(peak, dict) and current_u > float(peak.get("utility", float("-inf")))
    ):
        bio["peak_utility"] = {"utility": current_u, "reuse": int(skill.reuse_count or 0)}
    if not bio["transfer_events"] and skill.transfer_history:
        bio["transfer_events"] = list(skill.transfer_history)
    return bio


def append_biography_event(
    skill: Skill, kind: str, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Append a typed event into skill.metadata['biography']."""
    meta = dict(skill.metadata or {})
    bio = build_biography(skill)
    event = {"kind": kind, **(payload or {})}
    if kind in ("birth", "created", "promoted"):
        bio["birth"] = event
    elif kind in ("growth", "growing", "core", "decline"):
        events = list(bio.get("growth_events") or [])
        events.append(event)
        bio["growth_events"] = events
    elif kind in ("transfer",):
        events = list(bio.get("transfer_events") or [])
        events.append(event)
        bio["transfer_events"] = events
    elif kind in ("failure", "negative"):
        events = list(bio.get("failures") or [])
        events.append(event)
        bio["failures"] = events
    elif kind in ("retire", "retired", "archive", "archived", "dormant"):
        if kind in ("retire", "retired", "archive", "archived"):
            bio["retirement"] = event
        else:
            events = list(bio.get("growth_events") or [])
            events.append(event)
            bio["growth_events"] = events
    elif kind in ("reactivate", "reactivated"):
        events = list(bio.get("reactivations") or [])
        events.append(event)
        bio["reactivations"] = events
    else:
        events = list(bio.get("growth_events") or [])
        events.append(event)
        bio["growth_events"] = events

    u = float(skill.utility or 0.0)
    peak = bio.get("peak_utility")
    if peak is None or (
        isinstance(peak, dict) and u > float(peak.get("utility", float("-inf")))
    ):
        bio["peak_utility"] = {"utility": u, "reuse": int(skill.reuse_count or 0)}

    meta["biography"] = bio
    skill.metadata = meta
    return bio
