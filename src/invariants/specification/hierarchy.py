"""Operation → pattern → invariant hierarchy (Phase 11C-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from core.invariant import Invariant, InvariantType
from invariants.specification.policy import SPECIFICATION
from invariants.specification.qualification import QUALIFICATION_RULE_SET
from invariants.specification.rejection import REJECTION_CRITERIA


class HierarchyLevel(str):
    """Level names in the invariant hierarchy."""

    OPERATION = "operations"
    PATTERN = "patterns"
    INVARIANT = "invariants"


def hierarchy_level_for(invariant: Invariant) -> str:
    """Map an invariant to its hierarchy level."""
    steps = [s for s in invariant.pattern_signature if str(s).strip()]
    if len(steps) <= 1:
        return HierarchyLevel.OPERATION
    if invariant.invariant_type is InvariantType.PROCEDURAL and len(steps) == 2:
        return HierarchyLevel.PATTERN
    return HierarchyLevel.INVARIANT


@dataclass(slots=True)
class HierarchyNode:
    """A node in the operation → pattern → invariant hierarchy."""

    level: str
    label: str
    members: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "label": self.label, "members": list(self.members)}


@dataclass(slots=True)
class InvariantHierarchy:
    """Groups invariants by hierarchy level."""

    nodes: list[HierarchyNode] = field(default_factory=list)

    @classmethod
    def build(cls, invariants: Iterable[Invariant]) -> InvariantHierarchy:
        grouped: dict[str, list[str]] = {
            HierarchyLevel.OPERATION: [],
            HierarchyLevel.PATTERN: [],
            HierarchyLevel.INVARIANT: [],
        }
        for inv in invariants:
            level = hierarchy_level_for(inv)
            grouped.setdefault(level, []).append(inv.invariant_id)
        nodes = [
            HierarchyNode(level=level, label=level, members=members)
            for level, members in grouped.items()
            if members
        ]
        return cls(nodes=nodes)

    def members_at(self, level: str) -> list[str]:
        for node in self.nodes:
            if node.level == level:
                return list(node.members)
        return []

    def to_dict(self) -> dict[str, Any]:
        return {"nodes": [n.to_dict() for n in self.nodes]}


def summarize_specification() -> dict[str, Any]:
    """Return the machine-readable Phase 11C-1 specification."""
    return {
        **SPECIFICATION,
        "qualification_rule_details": [
            {"name": r.name, "description": r.description}
            for r in QUALIFICATION_RULE_SET
        ],
        "rejection_criteria": [
            {"name": c.name, "description": c.description} for c in REJECTION_CRITERIA
        ],
    }
