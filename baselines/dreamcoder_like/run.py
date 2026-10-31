"""Baseline D — DreamCoder-like: compress by reuse frequency only.

Primitives are admitted when they recur often, with no transfer test and no
economic evaluation. This is the closest classical analogue to ASFT; the point of
the comparison is that frequency-based compression looks strong on reuse while
producing little measured transfer.
"""

from __future__ import annotations

from collections import Counter

from pipelines.trace_pipeline import run_trace_pipeline
from skills.library import SkillLibrary
from solver.tasks import FAMILY_OPS

from baselines._common import make_skill, measure_library

__all__ = ["run"]

NAME = "dreamcoder_like"


def run(
    *,
    seed: int = 0,
    per_family: int = 4,
    top_k: int = 6,
    min_frequency: int = 3,
) -> dict:
    """Admit the most frequent op sequences as primitives."""
    trace_run = run_trace_pipeline(per_family=per_family, seed=seed, persist=False)
    counts: Counter[tuple[str, ...]] = Counter()
    for trace in trace_run.traces:
        ops = tuple(str(s.operation) for s in trace.steps)
        # Compression counts contiguous n-grams up to length 4, like DreamCoder.
        for n in range(2, min(4, len(ops)) + 1):
            for i in range(len(ops) - n + 1):
                counts[ops[i : i + n]] += 1

    library = SkillLibrary()
    admitted = 0
    for signature, freq in counts.most_common():
        if freq < min_frequency or admitted >= top_k:
            break
        library.add(
            make_skill(
                f"dc-{admitted}",
                category=_category(signature),
                triggers=list(signature),
                utility=min(1.0, freq / 10.0),
                transfer_score=0.0,
                reuse=freq,
            )
        )
        admitted += 1

    result = measure_library(NAME, library)
    result.metadata.update(
        {
            "admitted": admitted,
            "candidates": len(counts),
            "min_frequency": min_frequency,
        }
    )
    return result.to_dict()


def _category(signature: tuple[str, ...]) -> str:
    """Classify by the *discriminating* op, not any shared token.

    Every family begins with ``detect_object``, so a naive "any op in family"
    check labels every primitive as reflection. Match the reduction op instead.
    """
    joined = set(signature)
    if "apply_reflection" in joined:
        return "reflection"
    if "apply_rotation" in joined:
        return "rotation"
    if "count_objects" in joined:
        return "counting"
    if "group_by_color" in joined:
        return "grouping"
    return "general"
