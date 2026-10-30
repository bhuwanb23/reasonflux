"""Skill robustness metrics: SER, NTR, RR, CGR, TFD (Phase 11D-5)."""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill


def skill_explosion_ratio(skills: int | Sequence, validated_invariants: int) -> float:
    """SER = skills / validated_invariants."""
    n_skills = len(skills) if not isinstance(skills, int) else int(skills)
    denom = max(1, int(validated_invariants))
    return float(n_skills) / float(denom)


def skill_ntr(skill: Skill) -> float:
    """NTR = negative transfers / transfer attempts from history + evidence.

    Negative evidence may overlap transfer_history (record_transfer writes both),
    so count the union rather than summing.
    """
    history = list(skill.transfer_history or [])
    meta = skill.metadata or {}
    evidence = meta.get("evidence") or {}
    negatives = list(evidence.get("negative") or [])
    history_fails = sum(1 for e in history if not e.get("success", True))
    # Evidence-only negatives not already represented in transfer history.
    extra = max(0, len(negatives) - history_fails)
    attempts = len(history) + extra
    if attempts <= 0:
        return 0.0
    fails = history_fails + extra
    return float(fails) / float(attempts)


def retrieval_recall(
    retrieved: Sequence[str] | Sequence[Skill],
    available: Sequence[str] | Sequence[Skill],
) -> float:
    """RR = |retrieved ∩ available| / |available| for useful skills."""

    def _ids(items: Sequence) -> set[str]:
        out: set[str] = set()
        for item in items:
            if isinstance(item, str):
                out.add(item)
            else:
                out.add(getattr(item, "skill_id", str(item)))
        return out

    avail = _ids(available)
    if not avail:
        return 1.0
    hit = _ids(retrieved) & avail
    return float(len(hit)) / float(len(avail))


def capability_growth_rate(asu_series: Sequence[float]) -> float:
    """CGR ≈ last ASU − previous ASU (portfolio utility growth)."""
    vals = [float(x) for x in asu_series]
    if len(vals) < 2:
        return 0.0
    return vals[-1] - vals[-2]


def task_family_diversity(families: Sequence[str], tasks: int | None = None) -> float:
    """TFD = unique families / total tasks."""
    unique = {str(f).strip() for f in families if str(f).strip()}
    total = int(tasks) if tasks is not None else max(1, len(list(families)))
    total = max(1, total)
    return float(len(unique)) / float(total)
