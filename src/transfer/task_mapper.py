"""Map related tasks into cross-family transfer pairs (Phase 11C-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from core.task import Task
from transfer.taxonomy import TransferType, classify_transfer


@dataclass(slots=True)
class TaskPair:
    """A source/target task pair for a transfer experiment."""

    source_task_id: str
    target_task_id: str
    source_family: str
    target_family: str
    transfer_type: TransferType

    def to_dict(self) -> dict:
        return {
            "source_task_id": self.source_task_id,
            "target_task_id": self.target_task_id,
            "source_family": self.source_family,
            "target_family": self.target_family,
            "transfer_type": self.transfer_type.value,
        }


def map_related_tasks(
    tasks: Sequence[Task],
    *,
    max_pairs: int | None = None,
    source_ops: Sequence[str] | None = None,
    target_ops_by_family: dict[str, Sequence[str]] | None = None,
) -> list[TaskPair]:
    """Return cross-family task pairs labeled with a TransferType.

    Same-family pairs are skipped (near-transfer within a family is not the
    primary transfer experiment). Optional op sequences refine classification.
    """
    items = list(tasks)
    pairs: list[TaskPair] = []
    target_ops_by_family = target_ops_by_family or {}

    for i, source in enumerate(items):
        for target in items[i + 1 :]:
            if source.task_family == target.task_family:
                continue
            src_ops = list(source_ops) if source_ops is not None else None
            tgt_ops = list(target_ops_by_family.get(target.task_family) or [])
            if not tgt_ops:
                tgt_ops = None
            ttype = classify_transfer(
                source.task_family,
                target.task_family,
                source_ops=src_ops,
                target_ops=tgt_ops,
            )
            pairs.append(
                TaskPair(
                    source_task_id=source.task_id,
                    target_task_id=target.task_id,
                    source_family=source.task_family,
                    target_family=target.task_family,
                    transfer_type=ttype,
                )
            )
            if max_pairs is not None and len(pairs) >= max_pairs:
                return pairs
    return pairs
