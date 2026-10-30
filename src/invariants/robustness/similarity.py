"""Signature similarity for merge hints (E3)."""

from __future__ import annotations

from typing import Sequence

from invariants.robustness.config import RobustnessConfig


def jaccard_similarity(a: Sequence[str], b: Sequence[str]) -> float:
    """Jaccard index on pattern signature steps."""
    sa = {str(x).lower().strip() for x in a if str(x).strip()}
    sb = {str(x).lower().strip() for x in b if str(x).strip()}
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def should_merge_signatures(
    a: Sequence[str],
    b: Sequence[str],
    config: RobustnessConfig | None = None,
) -> bool:
    """True when signatures are similar enough to merge (policy hint only)."""
    config = config or RobustnessConfig()
    return jaccard_similarity(a, b) >= config.similarity_merge
