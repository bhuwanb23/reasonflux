"""SF7 capability collapse and SF8 adversarial formation (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.metrics import capability_growth_rate, task_family_diversity


@dataclass(slots=True)
class CollapseRisk:
    collapsed: bool
    cgr: float
    periods: int
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "collapsed": self.collapsed,
            "cgr": self.cgr,
            "periods": self.periods,
            "reasons": list(self.reasons),
        }


@dataclass(slots=True)
class AdversarialRisk:
    blocked: bool
    tfd: float
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "blocked": self.blocked,
            "tfd": self.tfd,
            "reasons": list(self.reasons),
        }


def detect_capability_collapse(
    asu_series: Sequence[float],
    config: SkillRobustnessConfig | None = None,
) -> CollapseRisk:
    """Flag collapse when CGR stays below threshold for collapse_periods."""
    config = config or SkillRobustnessConfig()
    vals = [float(x) for x in asu_series]
    if len(vals) < 2:
        return CollapseRisk(False, 0.0, 0)
    negative = 0
    last_cgr = 0.0
    for i in range(1, len(vals)):
        cgr = vals[i] - vals[i - 1]
        last_cgr = cgr
        if cgr < float(config.cgr_collapse):
            negative += 1
        else:
            negative = 0
    collapsed = negative >= int(config.collapse_periods)
    reasons = ["cgr_negative"] if collapsed else []
    return CollapseRisk(
        collapsed=collapsed,
        cgr=last_cgr if vals else capability_growth_rate(vals),
        periods=negative,
        reasons=reasons,
    )


def detect_adversarial_formation(
    families: Sequence[str],
    tasks: int | None = None,
    config: SkillRobustnessConfig | None = None,
) -> AdversarialRisk:
    """Block promotion when task-family diversity is too low."""
    config = config or SkillRobustnessConfig()
    tfd = task_family_diversity(families, tasks)
    if tfd < float(config.tfd_min_promote):
        return AdversarialRisk(True, tfd, ["low_tfd"])
    return AdversarialRisk(False, tfd, [])
