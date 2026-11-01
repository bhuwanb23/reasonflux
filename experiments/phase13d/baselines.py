"""Matched raw-memory and repeated-trace compression proxy controls."""
from __future__ import annotations
from collections import Counter
from typing import Any
from .common import ALLOWED_OPS
from solver.grid import Grid


def memory_matches(examples: list[dict[str, Any]], op: str, family: str) -> bool:
    return any(e["op"] == op and e["family"] == family for e in examples)


def literal_memory_matches(examples: list[dict[str, Any]], grid: Grid, op: str) -> bool:
    return any(e["op"] == op and e["grid"] == grid for e in examples)


def compression_library(examples: list[dict[str, Any]], slot_budget: int | None = None) -> list[tuple[str, ...]]:
    """Mine canonical operation chunks length 1–4 with count >= 2."""
    sequences = []
    for ex in examples:
        op = ex["op"]
        if op in ALLOWED_OPS:
            sequences.append((op,))
    counts: Counter[tuple[str, ...]] = Counter(sequences)
    eligible = sorted((seq for seq, count in counts.items() if count >= 2),
                      key=lambda seq: (-counts[seq], seq))
    if slot_budget is not None:
        eligible = eligible[:max(0, int(slot_budget))]
    return eligible


def compressed_chunks(ops: tuple[str, ...], library: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
    """Greedy longest exact chunk segmentation; ties use lexical order."""
    found: list[tuple[str, ...]] = []
    i = 0
    while i < len(ops):
        matches = [chunk for chunk in library if ops[i:i + len(chunk)] == chunk]
        if matches:
            chosen = min(matches, key=lambda chunk: (-len(chunk), chunk))
            found.append(chosen)
            i += len(chosen)
        else:
            found.append((ops[i],))
            i += 1
    return found
