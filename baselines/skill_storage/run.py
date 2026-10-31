"""Baseline B — skill storage: store skills but skip IDT validation and SCV.

Every mined pattern becomes a skill unconditionally. This isolates the value of
the *economic* gate: the same candidates the full pipeline sees, minus the
decisions about which ones are worth keeping.
"""

from __future__ import annotations

from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from skills.library import SkillLibrary

from baselines._common import make_skill, measure_library

__all__ = ["run"]

NAME = "skill_storage"


def run(*, seed: int = 0, per_family: int = 4, difficulty: float = 0.2) -> dict:
    """Promote every mined candidate, ignoring validation and SCV."""
    trace_run = run_trace_pipeline(per_family=per_family, seed=seed, persist=False)
    inv_run = run_invariant_pipeline(trace_run.traces)

    library = SkillLibrary()
    for i, inv in enumerate(inv_run.candidates):
        library.add(
            make_skill(
                f"store-{i}",
                category=str((inv.metadata or {}).get("mvp_category", "general")),
                triggers=inv.pattern_signature,
                utility=0.3,
                transfer_score=0.0,
            )
        )
    result = measure_library(NAME, library)
    result.metadata["n_candidates"] = len(inv_run.candidates)
    return result.to_dict()
