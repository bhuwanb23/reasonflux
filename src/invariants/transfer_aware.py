"""Transfer-aware ranking bridge — T = ITS × TU (Phase 11C-4).

Does not modify ranking.py; supplies a transfer_scores map instead.
"""

from __future__ import annotations

from typing import Sequence

from core.invariant import Invariant
from invariants.ranking import RankedInvariant, rank_invariants
from invariants.specification.policy import InvariantPolicy
from invariants.validation import ValidationConfig
from transfer.memory import TransferMemory
from transfer.metrics import TransferConfig, compute_transfer_score


def transfer_scores_map(
    candidates: Sequence[Invariant],
    memory: TransferMemory,
    config: TransferConfig | None = None,
    *,
    total_families: int = 1,
) -> dict[str, float]:
    """Map invariant_id → weighted T (ITS × TU) for ranking overrides."""
    config = config or TransferConfig()
    scores: dict[str, float] = {}
    for inv in candidates:
        result = compute_transfer_score(
            memory, inv.invariant_id, config, total_families=total_families
        )
        scores[inv.invariant_id] = result.weighted
    return scores


def rank_transfer_aware(
    candidates: Sequence[Invariant],
    memory: TransferMemory,
    *,
    config: TransferConfig | None = None,
    validation_config: ValidationConfig | None = None,
    policy: InvariantPolicy | None = None,
    total_families: int = 1,
) -> list[RankedInvariant]:
    """Rank candidates with T overridden by ITS × TU from transfer memory."""
    scores = transfer_scores_map(
        candidates, memory, config, total_families=total_families
    )
    return rank_invariants(
        list(candidates),
        validation_config,
        transfer_scores=scores,
        policy=policy,
    )
