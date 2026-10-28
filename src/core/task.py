"""Task — temporary problem instance (Phase 11B-1 Object 1)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class Task:
    """A problem instance presented to the system.

    Tasks are temporary learning stimuli; they are not stored as intelligence.
    """

    task_id: str
    task_family: str
    input_state: Any
    expected_outcome: Any = None
    difficulty: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task_id or not str(self.task_id).strip():
            raise ValueError("task_id must be a non-empty string")
        if not self.task_family or not str(self.task_family).strip():
            raise ValueError("task_family must be a non-empty string")
        if self.difficulty < 0:
            raise ValueError("difficulty must be >= 0")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return cls(
            task_id=data["task_id"],
            task_family=data["task_family"],
            input_state=data.get("input_state"),
            expected_outcome=data.get("expected_outcome"),
            difficulty=float(data.get("difficulty", 0.0)),
            metadata=dict(data.get("metadata") or {}),
        )
