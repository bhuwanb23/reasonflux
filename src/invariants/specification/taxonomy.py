"""Invariant taxonomy classifier (Phase 11C-1)."""

from __future__ import annotations

from typing import Sequence

from core.invariant import InvariantType


def classify_invariant_type(
    pattern_signature: Sequence[str],
    task_family_count: int = 1,
    structural: bool = False,
) -> InvariantType:
    """Classify an invariant per the 11C-1 taxonomy.

    - single operation → operational
    - multi-step within one family → procedural
    - multi-step marked structural → structural
    - multi-step spanning >= 2 families → transfer
    """
    steps = [s for s in pattern_signature if str(s).strip()]
    if len(steps) <= 1:
        return InvariantType.OPERATIONAL
    if task_family_count >= 2:
        return InvariantType.TRANSFER
    if structural:
        return InvariantType.STRUCTURAL
    return InvariantType.PROCEDURAL
