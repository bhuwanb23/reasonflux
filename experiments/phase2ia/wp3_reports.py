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


def _queue_counts(bundle: BundleView) -> dict[str, int]:
    """Priority-class counts derived from the draft stream itself."""
    conflict = set(bundle.agreement.disagreements)
    by_id = {label.task_id: label for label in bundle.c}
    a_by_id = {label.task_id: label for label in bundle.a}
    b_by_id = {label.task_id: label for label in bundle.b}
    counts = {"A_CODERS_DISAGREE": 0, "B_UNRESOLVED_AMBIGUOUS": 0, "C_LOW_CONFIDENCE": 0, "D_ROUTINE_CONFIRM": 0}
    for task_id, final in by_id.items():
        left, right = a_by_id[task_id], b_by_id[task_id]
        if task_id in conflict:
            counts["A_CODERS_DISAGREE"] += 1
        elif final.primary_family == "UNKNOWN_AMBIGUOUS":
            counts["B_UNRESOLVED_AMBIGUOUS"] += 1
        elif "LOW" in (left.confidence, right.confidence):
            counts["C_LOW_CONFIDENCE"] += 1
        else:
            counts["D_ROUTINE_CONFIRM"] += 1
    return counts


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
    queue_counts = _queue_counts(bundle)
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
            "## Two separate completion scales",
            "",
            "**AI draft completion: 100%.** All 600 tasks have an Agent A draft, an Agent B draft, and an "
            "Agent C synthesis with a full audit trail. Nothing is missing for review.",
            "",
            "**Human gate completion: 0%.** No record carries a human sign-off. Every row is "
            "`review_status=UNREVIEWED` with an empty `reviewer_id`, `reviewed_at_utc`, and "
            "`sign_off_sha256`. A human review is only counted when a signed record verifies against the "
            "exact draft hash it claims to judge; editing a CSV value cannot create one.",
            "",
            "## Where reviewer effort should go",
            "",
            "| Priority class | Tasks | What it means |",
            "|---|---:|---|",
            *[
                f"| `{cls}` | {count} | {meaning} |"
                for cls, count, meaning in (
                    ("A_CODERS_DISAGREE", queue_counts.get("A_CODERS_DISAGREE", 0),
                     "the two AI passes reached different families; these decide whether the rubric is usable"),
                    ("B_UNRESOLVED_AMBIGUOUS", queue_counts.get("B_UNRESOLVED_AMBIGUOUS", 0),
                     "no family was asserted; may indicate a missing rubric decision rule"),
                    ("C_LOW_CONFIDENCE", queue_counts.get("C_LOW_CONFIDENCE", 0),
                     "families agree but evidence is weak"),
                    ("D_ROUTINE_CONFIRM", queue_counts.get("D_ROUTINE_CONFIRM", 0),
                     "agreement with at least medium confidence; spot-check only"),
                )
            ],
            "",
            "See `disagreement_priority_queue.csv` for the ranked task list and `reviewer_A_packet.jsonl`, "
            "`reviewer_B_packet.jsonl`, `reviewer_C_packet.jsonl` for blinded review packets.",
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
            "| Annotator A completed | AI DRAFT ONLY — no human coder has signed a review |",
            "| Annotator B completed | AI DRAFT ONLY — no human coder has signed a review |",
            "| Independent annotators | NOT MET — both passes are deterministic policies in one repository |",
            "| Adjudicator completed | AI DRAFT ONLY — no human adjudicator has signed a review |",
            "| Cohen's kappa >= 0.70 | DESCRIPTIVE ONLY — measures policy agreement, not reader reliability |",
            "| Disagreements adjudicated | AI DRAFT ONLY — 124 tasks queued for human adjudication |",
            "| Family map frozen and hash-pinned | NOT MET — hash-pinned but not human-adjudicated |",
            "| No prohibited data accessed | MET — train-only packet, verified hashes |",
            "",
            "**WP3 remains INCOMPLETE.** The map produced here is `AI_PROVISIONAL` and must not be "
            "used for family qualification, candidate eligibility, Phase 2I execution, or any "
            "capability claim. Promoting it requires signed human reviews that verify against these "
            "draft hashes; see `wp3_human_review.py` for the enforcement rule.",
            "",
            "## What this is useful for",
            "",
            "1. A complete, reproducible first pass over all 600 discovery tasks.",
            "2. A ranked disagreement queue so human effort lands on the 124 conflicting cases first.",
            "3. Blinded A, B, and adjudicator packets that let real coders review without seeing each "
            "other's labels.",
            "4. Evidence about which rubric families are mechanically detectable and which need "
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
            "| `reviewer_A_packet.jsonl` | Blinded packet for coder A: training pairs plus A's AI draft only |",
            "| `reviewer_B_packet.jsonl` | Blinded packet for coder B: training pairs plus B's AI draft only |",
            "| `reviewer_C_packet.jsonl` | Adjudicator packet: both coder drafts plus the AI synthesis |",
            "| `disagreement_priority_queue.csv` | Ranked review order: conflicts, unknowns, low confidence |",
            "| `review_packet_manifest.json` | Packet hashes, field allowlists, and blinding notes |",
            "",
            "## Human review workflow",
            "",
            "Every label CSV carries `review_status`, `reviewer_id`, `reviewed_at_utc`, and "
            "`sign_off_sha256`, all empty. To make a label count as human evidence:",
            "",
            "1. A coder opens their own blinded packet and reads the training pairs and their AI draft.",
            "2. They record a decision (`ACCEPTED_BY_HUMAN`, `EDITED_BY_HUMAN`, or "
            "`ADJUDICATED_BY_HUMAN`), a final family, and their own rationale.",
            "3. A signed `HumanReview` record is created via `sign_review`, which binds the reviewer "
            "identity to the exact `ai_draft_record_sha256` they reviewed.",
            "4. `verify_reviews` rejects the record if the draft changed afterwards, so a stale "
            "signature cannot be inherited by an edited label.",
            "5. Only when both required roles are verified for all 600 tasks does "
            "`can_promote_to_human_evidence` return true.",
            "",
            "Editing a CSV value, renaming a column, or writing a status string does not create a "
            "review; the signature check fails.",
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
