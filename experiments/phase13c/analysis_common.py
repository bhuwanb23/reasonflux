"""Shared read-only data access for post-hoc Phase 13C reporting."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "experiments" / "PHASE-13C-SCT-V1"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)
record = json.loads((OUT / "record.json").read_text(encoding="utf-8"))
raw = record["raw_results"]
candidates = record["candidate_level_results"]

def fmt(x: float, digits: int = 3) -> str:
    return f"{x:.{digits}f}"


def mean(values):
    values = list(values)
    return statistics.mean(values) if values else 0.0


def sample_sd(values):
    values = list(values)
    return statistics.stdev(values) if len(values) > 1 else 0.0


def paired_dz(values):
    values = list(values)
    sd = sample_sd(values)
    if sd == 0:
        return None
    return mean(values) / sd
