"""Transfer tracker — record attempts, summarize, score, graph (Phase 11C-4)."""

from __future__ import annotations

from transfer.graph import TransferGraph
from transfer.memory import TransferMemory
from transfer.metrics import TransferConfig, TransferScores, compute_transfer_score
from transfer.records import TransferRecord
from transfer.taxonomy import TransferType


class TransferTracker:
    """Record before/after transfer events and expose summaries/scores."""

    def __init__(self, memory: TransferMemory | None = None) -> None:
        self.memory = memory or TransferMemory()

    def record(
        self,
        *,
        invariant_id: str,
        source_family: str,
        target_family: str,
        success: bool,
        benefit: float = 0.0,
        reasoning_reduction: float = 0.0,
        transfer_type: TransferType | str = TransferType.NEAR,
        timestamp: float = 0.0,
    ) -> TransferRecord:
        """Append a transfer attempt to memory."""
        item = TransferRecord(
            invariant_id=invariant_id,
            source_family=source_family,
            target_family=target_family,
            success=success,
            benefit=benefit,
            reasoning_reduction=reasoning_reduction,
            transfer_type=transfer_type
            if isinstance(transfer_type, TransferType)
            else TransferType(transfer_type),
            timestamp=timestamp,
        )
        self.memory.record(item)
        return item

    def summary(self, invariant_id: str | None = None):
        """Return memory summary for one invariant, or all records if None."""
        if invariant_id is None:
            return self.memory.all_records()
        return self.memory.summary(invariant_id)

    def graph(self) -> TransferGraph:
        """Build a transfer graph from successful transfer records."""
        return TransferGraph.from_records(self.memory.all_records())

    def scores(
        self,
        invariant_id: str,
        config: TransferConfig | None = None,
        *,
        total_families: int = 1,
    ) -> TransferScores:
        """Compute ITS/TU/NTR scores for an invariant."""
        return compute_transfer_score(
            self.memory, invariant_id, config, total_families=total_families
        )
