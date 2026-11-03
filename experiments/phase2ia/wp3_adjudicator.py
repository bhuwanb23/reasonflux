"""Adjudication for the WP3 provisional workflow.

Agent C resolves only the tasks where Agent A and Agent B disagree, using the
rubric's priority rules and the same train-only evidence. Agreement is retained
verbatim; unresolved disagreements stay explicitly ``UNKNOWN_AMBIGUOUS``.

Every adjudicated record carries the same audit trail a human adjudicator would
be expected to write: what was observed, the competing reading, and why the
final label was chosen.
"""
from __future__ import annotations

from experiments.phase2ia.wp3_evidence import FAMILY_ORDER
from experiments.phase2ia.wp3_features import TaskFeatures
from experiments.phase2ia.wp3_label import DECISION_THRESHOLD, Label, all_pairs, build_label
from experiments.phase2ia.wp3_packet_loader import TrainTask
from experiments.phase2ia.wp3_policy import family_scores

NEAR_TIE_GAP = 0.15


def _priority(family: str) -> int:
    return FAMILY_ORDER.index(family) if family in FAMILY_ORDER else len(FAMILY_ORDER)


def _competing(a: Label, b: Label) -> str:
    return f"A read {a.primary_family} ({a.confidence}); B read {b.primary_family} ({b.confidence})."


def adjudicate(task: TrainTask, features: TaskFeatures, a: Label, b: Label) -> Label:
    """Resolve one task, preferring direct demonstration evidence over label priority."""
    if a.primary_family == b.primary_family:
        return build_label(
            "C",
            task,
            family=a.primary_family,
            confidence=a.confidence,
            evidence=tuple(sorted(set(a.evidence_pair_indices) | set(b.evidence_pair_indices))),
            rationale=f"Both passes independently reached {a.primary_family}. {a.rationale}",
            notes="",
            secondary=set(a.secondary_tags) | set(b.secondary_tags),
            observed_change=a.observed_change,
            competing_interpretation="None: both passes converged on the same family.",
            decision_basis="Agreement retained without modification; no adjudication was required.",
            contributions=a.contributions,
        )

    scores = {s.family: s for s in family_scores(features, threshold=DECISION_THRESHOLD)}
    score_a = scores.get(a.primary_family)
    score_b = scores.get(b.primary_family)

    if score_a is not None and score_b is not None:
        gap = score_a.weight - score_b.weight
        if abs(gap) < NEAR_TIE_GAP:
            return build_label(
                "C",
                task,
                family="UNKNOWN_AMBIGUOUS",
                confidence="LOW",
                evidence=all_pairs(features),
                rationale=(
                    f"A read this as {a.primary_family} and B as {b.primary_family}. Both are supported by the "
                    f"demonstrations ({score_a.weight:.2f} versus {score_b.weight:.2f}) and no priority rule "
                    f"separates them, so the case stays unresolved."
                ),
                notes=f"unresolved disagreement A={a.primary_family} B={b.primary_family}",
                secondary={a.primary_family, b.primary_family} - {"UNKNOWN_AMBIGUOUS"},
                observed_change=a.observed_change or b.observed_change,
                competing_interpretation=_competing(a, b),
                decision_basis=(
                    f"Unresolved: the evidence gap is only {gap:+.2f}, below the {NEAR_TIE_GAP} threshold for a "
                    f"defensible adjudication, so both labels are preserved as competing readings."
                ),
            )
        winner, loser = (a, b) if gap > 0 else (b, a)
        basis = f"direct evidence favours {winner.primary_family} by {abs(gap):.2f}"
    elif score_a is not None or score_b is not None:
        winner, loser = (a, b) if score_a is not None else (b, a)
        basis = f"only {winner.primary_family} has supporting feature evidence"
    else:
        concrete = [label for label in (a, b) if label.primary_family != "UNKNOWN_AMBIGUOUS"]
        if len(concrete) == 1:
            winner, loser = concrete[0], (b if concrete[0] is a else a)
            basis = "the other pass withheld a label"
        else:
            winner = sorted((a, b), key=lambda label: _priority(label.primary_family))[0]
            loser = None
            basis = "rubric family priority"
        return build_label(
            "C",
            task,
            family=winner.primary_family,
            confidence="LOW",
            evidence=winner.evidence_pair_indices,
            rationale=(
                f"A read this as {a.primary_family} and B as {b.primary_family}. {basis.capitalize()}, so "
                f"{winner.primary_family} is retained at low confidence."
            ),
            notes=f"adjudicated from A={a.primary_family} B={b.primary_family}",
            secondary=(loser.primary_family,) if loser else (),
            observed_change=winner.observed_change,
            competing_interpretation=_competing(a, b),
            decision_basis=f"{basis.capitalize()}; retained at low confidence pending human review.",
        )

    assert loser is not None
    return build_label(
        "C",
        task,
        family=winner.primary_family,
        confidence="MEDIUM" if winner.confidence == "HIGH" else "LOW",
        evidence=winner.evidence_pair_indices,
        rationale=(
            f"A read this as {a.primary_family} and B as {b.primary_family}. {basis.capitalize()}: the "
            f"demonstrations support {winner.primary_family}."
        ),
        notes=f"resolved disagreement A={a.primary_family} B={b.primary_family}",
        secondary=(loser.primary_family,),
        observed_change=winner.observed_change,
        competing_interpretation=_competing(a, b),
        decision_basis=f"Resolved because {basis}.",
        contributions=winner.contributions,
    )
