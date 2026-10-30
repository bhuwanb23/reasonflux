"""In-memory capability library (Phase 11E-1)."""

from __future__ import annotations

from capability.models import Capability
from capability.states import CapabilityLifecycle


class CapabilityLibrary:
    """Store capabilities for membership lookup and portfolio aggregation."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def add(self, capability: Capability) -> None:
        if capability.capability_id in self._capabilities:
            raise ValueError(
                f"capability already exists: {capability.capability_id!r}"
            )
        self._capabilities[capability.capability_id] = capability

    def get(self, capability_id: str) -> Capability | None:
        return self._capabilities.get(capability_id)

    def list_capabilities(
        self, state: CapabilityLifecycle | None = None
    ) -> list[Capability]:
        items = list(self._capabilities.values())
        if state is None:
            return items
        return [c for c in items if c.state is state]

    def archive(self, capability_id: str) -> bool:
        """Prefer archive over hard delete. Returns True if archived."""
        cap = self._capabilities.get(capability_id)
        if cap is None:
            return False
        if cap.state is not CapabilityLifecycle.ARCHIVED:
            # Walk toward archived when possible.
            if cap.state is CapabilityLifecycle.CORE:
                cap.transition_to(CapabilityLifecycle.DECLINING)
            if cap.state in (
                CapabilityLifecycle.EMERGING,
                CapabilityLifecycle.DEVELOPING,
                CapabilityLifecycle.ESTABLISHED,
                CapabilityLifecycle.DECLINING,
            ):
                if cap.state is not CapabilityLifecycle.DECLINING:
                    if cap.state is CapabilityLifecycle.ESTABLISHED:
                        cap.transition_to(CapabilityLifecycle.DECLINING)
                    elif cap.state is CapabilityLifecycle.DEVELOPING:
                        cap.transition_to(CapabilityLifecycle.DECLINING)
                    elif cap.state is CapabilityLifecycle.EMERGING:
                        cap.transition_to(CapabilityLifecycle.DECLINING)
                if cap.state is CapabilityLifecycle.DECLINING:
                    cap.transition_to(CapabilityLifecycle.ARCHIVED)
        return cap.state is CapabilityLifecycle.ARCHIVED

    def remove(self, capability_id: str) -> bool:
        """Hard remove (tests only); prefer archive()."""
        return self._capabilities.pop(capability_id, None) is not None

    def find_by_skill(self, skill_id: str) -> list[Capability]:
        sid = str(skill_id)
        return [c for c in self._capabilities.values() if sid in c.skill_ids]

    def find_overlapping(
        self, skill_ids: list[str], *, min_jaccard: float = 0.5
    ) -> list[tuple[Capability, float]]:
        wanted = {str(s) for s in skill_ids if str(s).strip()}
        if not wanted:
            return []
        hits: list[tuple[Capability, float]] = []
        for cap in self._capabilities.values():
            members = set(cap.skill_ids)
            if not members:
                continue
            inter = len(wanted & members)
            union = len(wanted | members)
            score = inter / union if union else 0.0
            if score >= min_jaccard:
                hits.append((cap, score))
        hits.sort(key=lambda item: (-item[1], item[0].capability_id))
        return hits

    def __len__(self) -> int:
        return len(self._capabilities)
