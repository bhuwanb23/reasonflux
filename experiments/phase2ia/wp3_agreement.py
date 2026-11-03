"""Agreement statistics for the WP3 provisional annotation streams.

Implements nominal exact agreement, Cohen's kappa, and a full confusion
matrix. These numbers are descriptive diagnostics of two deterministic AI
policies, not human inter-annotator reliability.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence

from experiments.phase2ia.wp3_agents import Label

ONTOLOGY_DISPLAY_ORDER: tuple[str, ...] = (
    "OBJ_RELATION",
    "SPATIAL_CHANGE",
    "COLOR_ATTRIBUTE",
    "COUNT_REPLICATION",
    "PATTERN_COMPLETION",
    "REGION_TOPOLOGY",
    "FRAME_BOUNDS",
    "SYMBOLIC_SEQUENCE",
    "COMPOSITE_RULE",
    "UNKNOWN_AMBIGUOUS",
)


@dataclass(frozen=True, slots=True)
class AgreementResult:
    n: int
    observed_agreement: Fraction
    expected_agreement: Fraction
    cohen_kappa: Fraction
    kappa_defined: bool
    disagreements: tuple[str, ...]
    category_order: tuple[str, ...]
    matrix: tuple[tuple[int, ...], ...]
    marginals_a: Mapping[str, int]
    marginals_b: Mapping[str, int]
    unknown_a: int
    unknown_b: int
    missing_a: int
    missing_b: int

    @property
    def kappa_float(self) -> float:
        return float(self.cohen_kappa)

    @property
    def kappa_display(self) -> str:
        return f"{self.kappa_float:.4f}" if self.kappa_defined else "undefined (chance agreement is 1.0)"

    def matrix_rows(self) -> list[list[str | int]]:
        header = ["A \\ B", *self.category_order]
        rows: list[list[str | int]] = [header]
        for index, family in enumerate(self.category_order):
            rows.append([family, *self.matrix[index]])
        return rows


def _categories(a: Sequence[Label], b: Sequence[Label]) -> tuple[str, ...]:
    present = {label.primary_family for label in a} | {label.primary_family for label in b}
    ordered = [family for family in ONTOLOGY_DISPLAY_ORDER if family in present]
    extra = sorted(present - set(ordered))
    return tuple(ordered + extra)


def compute_agreement(a: Sequence[Label], b: Sequence[Label]) -> AgreementResult:
    if len(a) != len(b) or not a:
        raise ValueError("both streams must be nonempty and the same length")
    by_a = {label.task_id: label for label in a}
    by_b = {label.task_id: label for label in b}
    if set(by_a) != set(by_b):
        raise ValueError("the two streams must cover exactly the same task IDs")

    order = _categories(a, b)
    index = {family: position for position, family in enumerate(order)}
    matrix = [[0 for _ in order] for _ in order]
    disagreements: list[str] = []
    matches = 0
    for task_id in sorted(by_a):
        left, right = by_a[task_id], by_b[task_id]
        matrix[index[left.primary_family]][index[right.primary_family]] += 1
        if left.primary_family == right.primary_family:
            matches += 1
        else:
            disagreements.append(task_id)

    n = len(by_a)
    marginals_a = {family: sum(matrix[position]) for position, family in enumerate(order)}
    marginals_b = {family: sum(row[position] for row in matrix) for position, family in enumerate(order)}
    observed = Fraction(matches, n)
    expected = Fraction(sum(marginals_a[f] * marginals_b[f] for f in order), n * n)
    # Cohen's kappa is undefined when chance agreement is 1.0 (both streams use one category).
    kappa_defined = expected != 1
    kappa = (observed - expected) / (1 - expected) if kappa_defined else Fraction(0)

    return AgreementResult(
        n=n,
        observed_agreement=observed,
        expected_agreement=expected,
        cohen_kappa=kappa,
        kappa_defined=kappa_defined,
        disagreements=tuple(disagreements),
        category_order=order,
        matrix=tuple(tuple(row) for row in matrix),
        marginals_a=marginals_a,
        marginals_b=marginals_b,
        unknown_a=sum(1 for label in a if label.primary_family == "UNKNOWN_AMBIGUOUS"),
        unknown_b=sum(1 for label in b if label.primary_family == "UNKNOWN_AMBIGUOUS"),
        missing_a=sum(1 for label in a if not label.primary_family),
        missing_b=sum(1 for label in b if not label.primary_family),
    )


def kappa_interpretation(kappa: Fraction, *, defined: bool = True) -> str:
    if not defined:
        return "undefined (both streams used a single category)"
    value = float(kappa)
    if value >= 0.80:
        strength = "substantial"
    elif value >= 0.70:
        strength = "acceptable at the WP3 threshold"
    elif value >= 0.60:
        strength = "moderate"
    elif value >= 0.40:
        strength = "fair"
    else:
        strength = "poor"
    return strength


def render_confusion_markdown(result: AgreementResult) -> str:
    header = "| A \\ B | " + " | ".join(result.category_order) + " |"
    divider = "|" + "---|" * (len(result.category_order) + 1)
    lines = [header, divider]
    for position, family in enumerate(result.category_order):
        counts = " | ".join(str(value) for value in result.matrix[position])
        lines.append(f"| {family} | {counts} |")
    return "\n".join(lines)
