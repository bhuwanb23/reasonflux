"""Portfolio utility metrics — ASU, TSU, PU, UG, NTB (Phase 11D-2)."""

from __future__ import annotations

from dataclasses import dataclass

from core.states import SkillState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.utility import compute_su, refresh_skill_utility
from skills.utility_components import compute_nr


@dataclass(slots=True)
class PortfolioMetrics:
    """Aggregate skill-library economic health."""

    asu: float = 0.0
    tsu: float = 0.0
    pu: float = 0.0
    ug: float = 0.0
    ntb: float = 0.0
    skill_count: int = 0

    def to_dict(self) -> dict[str, float | int]:
        return {
            "asu": self.asu,
            "tsu": self.tsu,
            "pu": self.pu,
            "ug": self.ug,
            "ntb": self.ntb,
            "skill_count": self.skill_count,
        }


def compute_portfolio_metrics(
    library: SkillLibrary,
    *,
    previous: PortfolioMetrics | None = None,
    config: SkillConfig | None = None,
    refresh: bool = True,
) -> PortfolioMetrics:
    """Compute ASU / TSU / PU / UG / NTB over active-tier skills."""
    config = config or SkillConfig()
    active_tier = {
        SkillState.ACTIVE,
        SkillState.GROWING,
        SkillState.CORE,
    }
    skills = [s for s in library.list_skills() if s.state in active_tier]
    if not skills:
        skills = [
            s
            for s in library.list_skills()
            if s.state
            not in (SkillState.RETIRED, SkillState.ARCHIVED, SkillState.CANDIDATE)
        ]
    if refresh:
        for skill in skills:
            refresh_skill_utility(skill, config)

    utilities = [float(s.utility) for s in skills]
    n = len(utilities)
    if n == 0:
        return PortfolioMetrics()

    asu = sum(utilities) / n
    tsu = max(utilities)
    pu = sum(u for u in utilities if u > 0)
    ug = asu - (previous.asu if previous else asu)
    nrs = [compute_nr(s, config) for s in skills]
    ntb = sum(nrs) / n

    return PortfolioMetrics(
        asu=asu, tsu=tsu, pu=pu, ug=ug, ntb=ntb, skill_count=n
    )
