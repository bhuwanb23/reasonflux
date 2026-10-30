"""Detect → Diagnose → Recover → Monitor for capabilities (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.taxonomy import CapabilityFailureKind, FailureDiagnosis
from capability.states import CapabilityLifecycle


@dataclass(slots=True)
class RecoveryAction:
    """Planned recovery for a capability failure."""

    action: str  # archive | restore | monitor | retire_harmful
    kind: CapabilityFailureKind
    capability_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "kind": self.kind.value,
            "capability_ids": list(self.capability_ids),
            "notes": list(self.notes),
        }


def plan_recovery(
    diagnosis: FailureDiagnosis,
    config: CapabilityRobustnessConfig | None = None,
) -> RecoveryAction:
    """Map CF diagnosis to a recovery action (no DreamCoder rebuild)."""
    del config
    kind = diagnosis.kind
    caps = list(diagnosis.capability_ids)
    if kind is CapabilityFailureKind.CF2:
        return RecoveryAction(
            "archive",
            kind,
            caps,
            ["merge_or_archive_tiny", *diagnosis.reasons],
        )
    if kind is CapabilityFailureKind.CF4:
        return RecoveryAction(
            "retire_harmful",
            kind,
            caps,
            ["archive_negative_transfer_caps", *diagnosis.reasons],
        )
    if kind is CapabilityFailureKind.CF6:
        return RecoveryAction(
            "restore",
            kind,
            caps,
            ["restore_declining_or_dormant", *diagnosis.reasons],
        )
    if kind is CapabilityFailureKind.CF10:
        return RecoveryAction(
            "restore",
            kind,
            caps,
            ["restore_core_members", *diagnosis.reasons],
        )
    if kind in (
        CapabilityFailureKind.CF3,
        CapabilityFailureKind.CF7,
        CapabilityFailureKind.CF8,
    ):
        return RecoveryAction(
            "archive",
            kind,
            caps,
            ["reject_inflated_claim", *diagnosis.reasons],
        )
    return RecoveryAction("monitor", kind, caps, list(diagnosis.reasons))


def _archive_cap(cap_lib: CapabilityLibrary, capability_id: str) -> bool:
    return cap_lib.archive(capability_id)


def _restore_cap(cap: Capability) -> bool:
    """Restore declining → developing; flag dormant/core via metadata."""
    meta = dict(cap.metadata or {})
    if meta.get("dormant") or meta.get("restore_candidate"):
        meta["dormant"] = False
        meta["restored"] = True
        cap.metadata = meta
    if cap.state is CapabilityLifecycle.DECLINING:
        cap.transition_to(CapabilityLifecycle.DEVELOPING)
        return True
    if cap.state is CapabilityLifecycle.ARCHIVED:
        # Cannot leave archived via normal transitions; mark for rebuild.
        meta["restore_requested"] = True
        cap.metadata = meta
        return False
    if cap.state is CapabilityLifecycle.CORE:
        meta["protected"] = True
        cap.metadata = meta
        return True
    return False


def apply_recovery(
    action: RecoveryAction,
    cap_lib: CapabilityLibrary,
    *,
    config: CapabilityRobustnessConfig | None = None,
) -> list[str]:
    """Apply recovery; return list of affected capability ids."""
    del config
    affected: list[str] = []
    targets = list(action.capability_ids)
    if action.action == "monitor":
        for cid in targets:
            cap = cap_lib.get(cid)
            if cap is None:
                continue
            meta = dict(cap.metadata or {})
            meta["monitored"] = True
            meta["monitor_reason"] = action.kind.value
            cap.metadata = meta
            affected.append(cid)
        return affected

    if action.action in ("archive", "retire_harmful"):
        # If no explicit targets, archive tiny/non-core members for CF2.
        if not targets and action.kind is CapabilityFailureKind.CF2:
            for cap in cap_lib.list_capabilities():
                if (
                    cap.state is not CapabilityLifecycle.ARCHIVED
                    and len(cap.skill_ids) <= 1
                    and cap.state is not CapabilityLifecycle.CORE
                ):
                    targets.append(cap.capability_id)
        for cid in targets:
            if _archive_cap(cap_lib, cid):
                affected.append(cid)
        return affected

    if action.action == "restore":
        if not targets:
            for cap in cap_lib.list_capabilities():
                if cap.state is CapabilityLifecycle.DECLINING or (
                    cap.metadata or {}
                ).get("dormant"):
                    targets.append(cap.capability_id)
        for cid in targets:
            cap = cap_lib.get(cid)
            if cap is None:
                continue
            if _restore_cap(cap):
                affected.append(cid)
        return affected

    return affected
