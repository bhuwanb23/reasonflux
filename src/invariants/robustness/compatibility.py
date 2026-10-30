"""Invariant compatibility matrix (F4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from core.invariant import Invariant


# Known conflicting operation pairs (reflect vs rotate style).
_CONFLICT_PAIRS: frozenset[frozenset[str]] = frozenset(
    {
        frozenset({"reflect", "rotation"}),
        frozenset({"reflect", "rotate"}),
        frozenset({"apply_reflection", "apply_rotation"}),
    }
)


def _tokens(signature: Iterable[str]) -> set[str]:
    return {str(s).lower().strip() for s in signature if str(s).strip()}


def compatibility_score(a: Invariant, b: Invariant) -> float:
    """Score in [0, 1]; 1 = fully compatible, 0 = direct conflict."""
    ta, tb = _tokens(a.pattern_signature), _tokens(b.pattern_signature)
    if not ta or not tb:
        return 0.5
    reflect = {"reflect", "apply_reflection", "reflection"}
    rotate = {"rotate", "apply_rotation", "rotation"}
    if (ta & reflect and tb & rotate) or (ta & rotate and tb & reflect):
        return 0.2
    for pair in _CONFLICT_PAIRS:
        if pair <= ta and pair <= tb:
            return 0.0
    overlap = len(ta & tb) / max(len(ta | tb), 1)
    return max(0.0, min(1.0, 0.5 + 0.5 * overlap))


def are_compatible(
    a: Invariant, b: Invariant, *, min_score: float = 0.5
) -> bool:
    return compatibility_score(a, b) >= min_score


@dataclass
class CompatibilityMatrix:
    """Pairwise compatibility scores keyed by invariant id."""

    _scores: dict[tuple[str, str], float] = field(default_factory=dict)

    def set_pair(self, id_a: str, id_b: str, score: float) -> None:
        key = tuple(sorted((id_a, id_b)))
        self._scores[key] = max(0.0, min(1.0, score))

    def score(self, id_a: str, id_b: str) -> float:
        key = tuple(sorted((id_a, id_b)))
        return self._scores.get(key, 0.5)

    def register(self, a: Invariant, b: Invariant) -> float:
        s = compatibility_score(a, b)
        self.set_pair(a.invariant_id, b.invariant_id, s)
        return s
