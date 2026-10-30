"""Transfer memory — occurrence + transfer history per invariant (11C-4)."""

from __future__ import annotations

from dataclasses import dataclass, field

from transfer.records import TransferMemorySummary, TransferRecord


@dataclass
class TransferMemory:
    """Stores transfer attempts separately from discovery/validation evidence."""

    _records: list[TransferRecord] = field(default_factory=list)

    def record(self, item: TransferRecord) -> None:
        """Append a transfer attempt."""
        self._records.append(item)

    def records_for(self, invariant_id: str) -> list[TransferRecord]:
        return [r for r in self._records if r.invariant_id == invariant_id]

    def all_records(self) -> list[TransferRecord]:
        return list(self._records)

    def attempts(self, invariant_id: str) -> int:
        return len(self.records_for(invariant_id))

    def successes(self, invariant_id: str) -> int:
        return sum(1 for r in self.records_for(invariant_id) if r.success)

    def failures(self, invariant_id: str) -> int:
        return sum(1 for r in self.records_for(invariant_id) if not r.success)

    def coverage(self, invariant_id: str) -> int:
        families = {
            r.target_family for r in self.records_for(invariant_id) if r.target_family
        }
        return len(families)

    def summary(self, invariant_id: str) -> TransferMemorySummary:
        rows = self.records_for(invariant_id)
        families = sorted({r.target_family for r in rows if r.target_family})
        return TransferMemorySummary(
            invariant_id=invariant_id,
            attempts=len(rows),
            successes=sum(1 for r in rows if r.success),
            failures=sum(1 for r in rows if not r.success),
            total_benefit=sum(r.benefit for r in rows),
            total_reduction=sum(r.reasoning_reduction for r in rows),
            target_families=families,
        )

    def clear(self) -> None:
        self._records.clear()
