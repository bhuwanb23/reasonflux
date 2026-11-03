"""Markdown reports for the WP3 provisional annotation bundle.

Renders the agreement report, the WP3 completion review, and the bundle README.
Every document leads with the explicit non-eligibility banner so a reader cannot
mistake these artifacts for human annotation evidence.
"""
from __future__ import annotations

from typing import Protocol, Sequence

from experiments.phase2ia.wp3_agreement import (
    AgreementResult,
    kappa_interpretation,
    render_confusion_markdown,
)
from experiments.phase2ia.wp3_label import ONTOLOGY_VERSION, POLICY_VERSION
from experiments.phase2ia.wp3_label import Label

RUN_ID = "ASFT-WP3-AI-PROVISIONAL-V1"
BANNER = "AI_PROVISIONAL — NOT HUMAN ANNOTATION — NOT WP3-ELIGIBLE"
HEADER_LINES: tuple[str, ...] = (
    BANNER,
    "Not Independent Human Annotation",
    "Not Eligible For Family Qualification",
    "Not Eligible For Candidate Eligibility",
    "Not Eligible For Phase 2I Execution",
    "Not Eligible For WP3 Completion",
)


class BundleView(Protocol):
    """Structural view of a provisional bundle; avoids a circular import."""

    a: Sequence[Label]
    b: Sequence[Label]
    c: Sequence[Label]
    agreement: AgreementResult


def _banner_block() -> list[str]:
    return [f"# {BANNER}", "", *[f"**{line}**  " for line in HEADER_LINES[1:]], ""]


def agreement_markdown(bundle: BundleView) -> str:
    result = bundle.agreement
    lines = _banner_block()
    lines += [
        "## Scope",
        "",
        "Descriptive comparison of two deterministic, rubric-conditioned AI policies over "
        f"all {result.n} discovery tasks. These are prompt-sensitivity diagnostics for a "
        "rule-based classifier, not human inter-annotator reliability and not estimates "
        "of annotation quality on unseen tasks.",
        "",
        "## Agreement",
        "",
        f"- Tasks compared: **{result.n}**",
        f"- Exact primary-family matches: **{result.n - len(result.disagreements)}/{result.n}**",
        f"- Observed agreement: **{float(result.observed_agreement):.4f}**",
        f"- Chance agreement: **{float(result.expected_agreement):.4f}**",
        f"- Cohen's kappa (descriptive): **{result.kappa_display}**",
        f"- Kappa band: **{kappa_interpretation(result.cohen_kappa, defined=result.kappa_defined)}**",
        f"- Disagreements: **{len(result.disagreements)}**",
        f"- `UNKNOWN_AMBIGUOUS` in pass A: **{result.unknown_a}** ({result.unknown_a / result.n:.1%})",
        f"- `UNKNOWN_AMBIGUOUS` in pass B: **{result.unknown_b}** ({result.unknown_b / result.n:.1%})",
        f"- Missing labels: **A={result.missing_a}, B={result.missing_b}**",
        "",
        "### Confusion matrix",
        "",
        "Rows are pass A; columns are pass B.",
        "",
        render_confusion_markdown(result),
        "",
        "### Marginals",
        "",
        "| Family | Pass A | Pass B |",
        "|---|---:|---:|",
    ]
    for family in result.category_order:
        lines.append(f"| {family} | {result.marginals_a[family]} | {result.marginals_b[family]} |")
    lines += [
        "",
        "## Interpretation boundary",
        "",
        "A high kappa here means the two rule policies were written to agree, not that two "
        "independent readers would agree. The WP3 gate requires human coders and a separate "
        "human adjudicator; this report cannot satisfy it.",
        "",
    ]
    return "\n".join(lines)


def completion_review(bundle: BundleView) -> str:
    result = bundle.agreement
    counts: dict[str, int] = {}
    for label in bundle.c:
        counts[label.primary_family] = counts.get(label.primary_family, 0) + 1
    distribution = "\n".join(
        f"| {family} | {count} | {count / result.n:.1%} |"
        for family, count in sorted(counts.items(), key=lambda kv: -kv[1])
    )
    return "\n".join(
        [
            *_banner_block(),
            "## What was produced",
            "",
            f"- Run ID: `{RUN_ID}`",
            f"- Ontology: `{ONTOLOGY_VERSION}`; policy: `{POLICY_VERSION}`",
            f"- Tasks labelled: **{result.n}** (one record per discovery task, no gaps)",
            f"- Agent A stream: {len(bundle.a)} labels",
            f"- Agent B stream: {len(bundle.b)} labels",
            f"- Agent C adjudication records: {len(bundle.c)}",
            f"- Exact A/B agreement: {result.n - len(result.disagreements)}/{result.n} "
            f"({float(result.observed_agreement):.1%})",
            f"- Descriptive Cohen's kappa: {result.kappa_display}",
            "",
            "## Final label distribution (provisional)",
            "",
            "| Family | Tasks | Share |",
            "|---|---:|---:|",
            distribution,
            "",
            "## WP3 gate status",
            "",
            "| Gate condition | Status |",
            "|---|---|",
            "| Annotator A completed | PARTIAL — AI agent only |",
            "| Annotator B completed | PARTIAL — AI agent only |",
            "| Independent annotators | NOT MET — both passes are deterministic policies in one repository |",
            "| Adjudicator completed | PARTIAL — AI agent, not independent |",
            "| Cohen's kappa >= 0.70 | DESCRIPTIVE ONLY — see agreement report |",
            "| Disagreements adjudicated | PARTIAL — resolved by policy, not by an independent adjudicator |",
            "| Family map frozen and hash-pinned | NOT MET — provisional map is hash-pinned but not frozen for use |",
            "| No prohibited data accessed | MET — train-only packet, verified hashes |",
            "",
            "**WP3 remains INCOMPLETE.** The map produced here is `AI_PROVISIONAL` and must not be "
            "used for family qualification, candidate eligibility, Phase 2I execution, or any "
            "capability claim.",
            "",
            "## What this is useful for",
            "",
            "1. A complete, reproducible first pass over all 600 discovery tasks.",
            "2. A concrete disagreement list for human reviewers to adjudicate first.",
            "3. Evidence about which rubric families are mechanically detectable and which need "
            "human judgement, including a quantified `UNKNOWN_AMBIGUOUS` rate.",
            "",
            "## What this is not",
            "",
            "- Not human annotation, and not a substitute for the two independent coder streams.",
            "- Not reliability evidence; kappa measures agreement between two rules, not between readers.",
            "- Not a validated family map; label accuracy against ground truth is unmeasured.",
            "",
        ]
    )


def readme(bundle: BundleView) -> str:
    return "\n".join(
        [
            *_banner_block(),
            "## Purpose",
            "",
            "A complete, reproducible first-pass family annotation of all 600 discovery tasks, "
            "produced by three deterministic AI policies. It exists so that human reviewers can "
            "start from a finished pass instead of a blank packet.",
            "",
            "## Why this is not WP3 completion",
            "",
            "WP3 requires two independent human annotators and a separate human adjudicator, all "
            "blind to solver outputs, candidate yield, and test data. Three policies in this "
            "repository are not independent readers: they share the same feature code, the same "
            "ontology, and the same author. Agreement between them measures policy design, not "
            "human reliability.",
            "",
            "## Files",
            "",
            "| File | Contents |",
            "|---|---|",
            "| `annotator_A_labels.csv` | Agent A mechanism-first labels for all 600 tasks |",
            "| `annotator_B_labels.csv` | Agent B counter-hypothesis labels for all 600 tasks |",
            "| `adjudication_log.csv` | Agent C decision and basis for every task |",
            "| `agreement_report.md` | Descriptive agreement, kappa, confusion matrix, marginals |",
            "| `confusion_matrix.csv` | Machine-readable A x B count matrix |",
            "| `task_family_map.csv` | Provisional adjudicated task to family map |",
            "| `family_map_hash.txt` | SHA-256 pin for the family map |",
            "| `wp3_completion_review.md` | Gate-by-gate status showing WP3 remains incomplete |",
            "| `provisional_manifest.json` | Hashes, boundary checks, and use restrictions |",
            "",
            "## Reproduce",
            "",
            "```",
            "python experiments/phase2ia/wp3_provisional.py",
            "```",
            "",
            "## Permitted and prohibited use",
            "",
            "Permitted: rubric debugging, sampling disagreements for human review, estimating the "
            "`UNKNOWN_AMBIGUOUS` rate, and prioritising reviewer effort.",
            "",
            "Prohibited: treating any label as a human annotation, passing `task_family_map.csv` into "
            "family qualification or candidate eligibility, running Phase 2I on it, or reporting the "
            "kappa as inter-annotator reliability.",
            "",
        ]
    )
