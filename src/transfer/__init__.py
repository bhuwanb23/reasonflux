"""Transfer experiments — Task A → Task B effects (Phase 11C-4)."""

from transfer.gate import TransferGateResult, confirm_transfer, evaluate_transfer_gate
from transfer.graph import TransferEdge, TransferGraph
from transfer.memory import TransferMemory
from transfer.metrics import (
    TransferConfig,
    TransferScores,
    compute_its,
    compute_ntr,
    compute_transfer_score,
    compute_tu,
)
from transfer.records import TransferMemorySummary, TransferRecord
from transfer.task_mapper import TaskPair, map_related_tasks
from transfer.taxonomy import TransferType, classify_transfer, expected_transfer_band
from transfer.transfer_tracker import TransferTracker

__all__ = [
    "TaskPair",
    "TransferConfig",
    "TransferEdge",
    "TransferGateResult",
    "TransferGraph",
    "TransferMemory",
    "TransferMemorySummary",
    "TransferRecord",
    "TransferScores",
    "TransferTracker",
    "TransferType",
    "classify_transfer",
    "compute_its",
    "compute_ntr",
    "compute_transfer_score",
    "compute_tu",
    "confirm_transfer",
    "evaluate_transfer_gate",
    "expected_transfer_band",
    "map_related_tasks",
]
