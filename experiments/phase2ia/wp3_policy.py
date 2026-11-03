"""Evidence scoring for the WP3 provisional annotators.

Converts task-level features into per-family evidence scores, then exposes the
two rubric-conditioned decisions: Agent A's mechanism-first choice and Agent B's
counter-hypothesis choice under the rubric's priority tiers.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from experiments.phase2ia.wp3_evidence import FAMILY_ORDER, FEATURE_SPECS, SPEC_BY_FEATURE
from experiments.phase2ia.wp3_features import TaskFeatures
from experiments.phase2ia.wp3_label import DECISION_THRESHOLD, all_pairs, build_label
from experiments.phase2ia.wp3_label import Label
from experiments.phase2ia.wp3_packet_loader import TrainTask

POLICY_A_THRESHOLD = 0.60
POLICY_A_SPECIFICITY = 0.45
POLICY_B_THRESHOLD = 0.75
POLICY_B_SPECIFICITY = 0.55

TIERS: tuple[tuple[str, ...], ...] = (
    ("OBJ_RELATION",),
    ("COUNT_REPLICATION", "PATTERN_COMPLETION"),
    ("REGION_TOPOLOGY",),
    ("SYMBOLIC_SEQUENCE",),
    ("COLOR_ATTRIBUTE",),
    ("SPATIAL_CHANGE",),
    ("FRAME_BOUNDS",),
)


@dataclass(frozen=True, slots=True)
class Score:
    family: str
    weight: float
    specificity: float
    features: tuple[str, ...]
    evidence: tuple[int, ...]


def family_scores(features: TaskFeatures, *, threshold: float) -> list[Score]:
    scores: dict[str, Score] = {}
    for spec in FEATURE_SPECS:
        rate = features.rate(spec.feature)
        if rate < threshold:
            continue
        contribution = rate * spec.weight
        previous = scores.get(spec.family)
        if previous is None:
            scores[spec.family] = Score(
                family=spec.family,
                weight=contribution,
                specificity=spec.weight * rate,
                features=(spec.feature,),
                evidence=features.evidence.get(spec.feature, ()),
            )
        else:
            scores[spec.family] = Score(
                family=spec.family,
                weight=previous.weight + contribution,
                specificity=max(previous.specificity, spec.weight * rate),
                features=previous.features + (spec.feature,),
                evidence=tuple(sorted(set(previous.evidence) | set(features.evidence.get(spec.feature, ())))),
            )
    return sorted(scores.values(), key=lambda s: (-s.weight, -s.specificity, FAMILY_ORDER.index(s.family)))


def confidence_of(best: Score, runner_up: Score | None) -> str:
    margin = best.weight - (runner_up.weight if runner_up else 0.0)
    if best.specificity >= 0.95 and margin >= 0.7:
        return "HIGH"
    if best.specificity >= 0.6 and margin >= 0.25:
        return "MEDIUM"
    return "LOW"


def mechanisms(score: Score) -> str:
    return "; ".join(f"{feature} ({SPEC_BY_FEATURE[feature].mechanism})" for feature in score.features)


def observed_change_text(score: Score) -> str:
    """Plain statement of what the demonstrations actually do, for the audit trail."""
    described = "; ".join(SPEC_BY_FEATURE[feature].mechanism for feature in score.features)
    pairs = ", ".join(map(str, score.evidence)) or "1"
    return f"On pair(s) {pairs}: {described}."


def competing_text(runner_up: Score | None) -> str:
    """The strongest rival reading, stated so a reviewer can test it."""
    if runner_up is None:
        return "No competing family reached the evidence threshold on these demonstrations."
    return (
        f"Rival reading {runner_up.family}: "
        + "; ".join(SPEC_BY_FEATURE[feature].mechanism for feature in runner_up.features)
        + f" (evidence weight {runner_up.weight:.2f})."
    )


def decision_basis_text(best: Score, runner_up: Score | None, *, tiered: bool) -> str:
    if runner_up is None:
        return f"{best.family} is the only family above the evidence threshold for this pass."
    margin = best.weight - runner_up.weight
    if tiered:
        relative = "outranks" if tier_of(best.family) < tier_of(runner_up.family) else "is outranked by"
        return (
            f"{best.family} sits in rubric tier {tier_of(best.family)} and {runner_up.family} in tier "
            f"{tier_of(runner_up.family)}, so {best.family} {relative} the rival reading on priority "
            f"(evidence weight {best.weight:.2f} versus {runner_up.weight:.2f})."
        )
    return (
        f"{best.family} carries the greater specific evidence weight ({best.weight:.2f} versus "
        f"{runner_up.weight:.2f}), a margin of {margin:+.2f}."
    )


def tier_of(family: str) -> int:
    for index, families in enumerate(TIERS):
        if family in families:
            return index
    return len(TIERS)


def _qualified(scores: Sequence[Score], min_specificity: float) -> list[Score]:
    return [s for s in scores if s.weight >= DECISION_THRESHOLD and s.specificity >= min_specificity]


def _unresolved(
    agent_id: str,
    task: TrainTask,
    features: TaskFeatures,
    note: str,
    *,
    competing: str = "",
    basis: str = "",
) -> Label:
    return build_label(
        agent_id,
        task,
        family="UNKNOWN_AMBIGUOUS",
        confidence="LOW",
        evidence=all_pairs(features),
        rationale=(
            f"Pairs 1-{features.pair_count} do not support one rubric family strongly enough for this pass, "
            f"so no primary family is asserted."
        ),
        notes=note,
        secondary=(),
        observed_change="No single transformation pattern held across enough training pairs to name a mechanism.",
        competing_interpretation=competing or "Several readings remain plausible; none clears the threshold.",
        decision_basis=basis or "Insufficient support for any single family under this pass's threshold.",
    )


def mechanism_first(task: TrainTask, features: TaskFeatures) -> Label:
    """Agent A: take the family with the greatest specific evidence weight."""
    scores = family_scores(features, threshold=POLICY_A_THRESHOLD)
    strong = _qualified(scores, POLICY_A_SPECIFICITY)
    if not strong:
        near = scores[0] if scores else None
        return _unresolved(
            "A",
            task,
            features,
            "no qualifying mechanism under the mechanism-first policy",
            competing=(
                f"Strongest partial signal was {near.family} ({near.weight:.2f}), below the required threshold."
                if near
                else ""
            ),
        )

    best = strong[0]
    runner_up = strong[1] if len(strong) > 1 else None
    contributions = tuple((s.family, round(s.weight, 4)) for s in strong[:4])

    if runner_up is not None and abs(best.weight - runner_up.weight) < 0.12 and best.specificity < 0.95:
        return build_label(
            "A",
            task,
            family="UNKNOWN_AMBIGUOUS",
            confidence="LOW",
            evidence=all_pairs(features),
            rationale=(
                f"Pairs 1-{features.pair_count} support {best.family} and {runner_up.family} almost equally "
                f"({best.weight:.2f} versus {runner_up.weight:.2f}); the demonstrations do not separate them."
            ),
            notes=f"near tie between {best.family} and {runner_up.family}",
            secondary=(best.family, runner_up.family),
            observed_change=observed_change_text(best),
            competing_interpretation=competing_text(runner_up),
            decision_basis=(
                f"Withheld: the margin of {best.weight - runner_up.weight:+.2f} is below the 0.12 separation "
                f"this pass requires before naming a primary family."
            ),
            contributions=contributions,
        )

    return build_label(
        "A",
        task,
        family=best.family,
        confidence=confidence_of(best, runner_up),
        evidence=best.evidence or all_pairs(features),
        rationale=(
            f"Pairs {', '.join(map(str, best.evidence)) or '1'} show that {mechanisms(best)}, "
            f"which is the most specific consistent mechanism."
        ),
        notes="; ".join(features.notes),
        secondary=[s.family for s in strong[1:3]],
        observed_change=observed_change_text(best),
        competing_interpretation=competing_text(runner_up),
        decision_basis=decision_basis_text(best, runner_up, tiered=False),
        contributions=contributions,
    )


def counter_hypothesis(task: TrainTask, features: TaskFeatures) -> Label:
    """Agent B: rank by rubric priority tier, then by evidence weight."""
    scores = family_scores(features, threshold=POLICY_B_THRESHOLD)
    strong = _qualified(scores, POLICY_B_SPECIFICITY)
    if not strong:
        near = scores[0] if scores else None
        return _unresolved(
            "B",
            task,
            features,
            "no qualifying mechanism after the counter-hypothesis check",
            competing=(
                f"Strongest partial signal after discounting surface actions was {near.family} "
                f"({near.weight:.2f}), below threshold."
                if near
                else ""
            ),
        )

    ranked = sorted(strong, key=lambda s: (tier_of(s.family), -s.weight))
    best = ranked[0]
    runner_up = ranked[1] if len(ranked) > 1 else None
    contributions = tuple((s.family, round(s.weight, 4)) for s in ranked[:4])

    if (
        runner_up is not None
        and tier_of(runner_up.family) == tier_of(best.family)
        and abs(best.weight - runner_up.weight) < 0.10
        and best.specificity < 0.9
    ):
        return build_label(
            "B",
            task,
            family="UNKNOWN_AMBIGUOUS",
            confidence="LOW",
            evidence=all_pairs(features),
            rationale=(
                f"{best.family} and {runner_up.family} sit in the same rubric tier and the demonstrations "
                f"support both equally, so this pass withholds a label."
            ),
            notes=f"tier tie between {best.family} and {runner_up.family}",
            secondary=(best.family, runner_up.family),
            observed_change=observed_change_text(best),
            competing_interpretation=competing_text(runner_up),
            decision_basis=(
                f"Withheld: both candidates are in tier {tier_of(best.family)} and differ by only "
                f"{best.weight - runner_up.weight:+.2f}, so the rubric offers no tie-break."
            ),
            contributions=contributions,
        )

    return build_label(
        "B",
        task,
        family=best.family,
        confidence=confidence_of(best, runner_up),
        evidence=best.evidence or all_pairs(features),
        rationale=(
            f"Pairs {', '.join(map(str, best.evidence)) or '1'} show that {mechanisms(best)}. "
            f"After checking whether a surface action is secondary to selection, region, count, or pattern "
            f"structure, {best.family} outranks the remaining readings "
            f"({', '.join(s.family for s in ranked[1:3]) or 'none'})."
        ),
        notes="; ".join(features.notes),
        secondary=[s.family for s in ranked[1:3]],
        observed_change=observed_change_text(best),
        competing_interpretation=competing_text(runner_up),
        decision_basis=decision_basis_text(best, runner_up, tiered=True),
        contributions=contributions,
    )


def annotate_agent_a(task: TrainTask, features: TaskFeatures) -> Label:
    """Public entry point for the Agent A stream."""
    return mechanism_first(task, features)


def annotate_agent_b(task: TrainTask, features: TaskFeatures) -> Label:
    """Public entry point for the Agent B stream."""
    return counter_hypothesis(task, features)
