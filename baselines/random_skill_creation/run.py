"""Baseline C — random skill creation: promote at random, ignoring SCV.

The library is stocked with plausible skills, but selection is random. This
isolates the value of the SCV decision rule from the mere presence of skills.
"""

from __future__ import annotations

import random

from skills.library import SkillLibrary
from solver.tasks import FAMILY_OPS

from baselines._common import make_skill, measure_library

__all__ = ["run"]

NAME = "random_skill_creation"
APPLY_OPS = ("apply_reflection", "apply_rotation")


def run(
    *,
    seed: int = 0,
    n_skills: int = 6,
    utility_range: tuple[float, float] = (0.05, 0.4),
) -> dict:
    """Create ``n_skills`` random skills with arbitrary triggers."""
    rng = random.Random(seed)
    library = SkillLibrary()
    families = sorted(FAMILY_OPS)
    for i in range(n_skills):
        family = rng.choice(families)
        triggers = list(FAMILY_OPS[family])
        if rng.random() < 0.5:
            triggers.append(rng.choice(APPLY_OPS))
        library.add(
            make_skill(
                f"rand-{i}",
                category=family,
                triggers=triggers,
                utility=rng.uniform(*utility_range),
                transfer_score=0.0,
                reuse=rng.randint(0, 2),
            )
        )
    result = measure_library(NAME, library)
    result.metadata["random"] = True
    return result.to_dict()
