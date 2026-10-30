"""Evaluation maturity levels L1–L5 (Phase 11E-4)."""

from __future__ import annotations

from evaluation.harness.models import LayerResult

LAYER_ORDER = (
    "invariant",
    "skill",
    "transfer",
    "capability",
    "intelligence",
)


def classify_evaluation_maturity(layers: list[LayerResult]) -> int:
    """Return highest consecutive passed level (1–5)."""
    by_name = {lr.layer: lr for lr in layers}
    level = 0
    for name in LAYER_ORDER:
        lr = by_name.get(name)
        if lr is None or not lr.passed:
            break
        level += 1
    return max(1, level) if level > 0 else 1


def maturity_label(level: int) -> str:
    labels = {
        1: "pattern_discovery",
        2: "skill_formation",
        3: "transfer_learning",
        4: "capability_growth",
        5: "intelligence_growth",
    }
    return labels.get(int(level), "pattern_discovery")
