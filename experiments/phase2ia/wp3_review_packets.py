"""Blinded reviewer packets and a disagreement-priority queue for WP3.

Each packet contains only training demonstrations plus the AI draft fields a
reviewer needs for their role. Packets never contain test data, solver output,
traces, candidate yield, or future outcomes, and a coder packet never reveals the
other coder's labels.

The queue ranks tasks by how much human attention they deserve, so reviewer time
goes to unresolved and low-confidence cases first.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from experiments.phase2ia.wp3_agreement import AgreementResult
from experiments.phase2ia.wp3_label import Label
from experiments.phase2ia.wp3_packet_loader import Packet, TrainTask

REVIEW_PACKET_PROTOCOL = "WP3-HUMAN-REVIEW-PACKETS-V1"

CODER_FIELDS: tuple[str, ...] = (
    "task_id",
    "train_pairs",
    "ai_draft_family",
    "ai_draft_confidence",
    "ai_draft_observed_change",
    "ai_draft_competing_interpretation",
    "ai_draft_decision_basis",
    "ai_draft_evidence_pairs",
    "ai_draft_record_sha256",
    "draft_mode",
    "review_decision",
    "review_final_family",
    "review_rationale",
    "reviewer_id",
    "reviewed_at_utc",
    "sign_off_sha256",
)
ADJUDICATOR_FIELDS: tuple[str, ...] = (
    "task_id",
    "train_pairs",
    "coder_a_family",
    "coder_b_family",
    "ai_draft_family",
    "ai_draft_confidence",
    "ai_draft_observed_change",
    "ai_draft_competing_interpretation",
    "ai_draft_decision_basis",
    "ai_draft_evidence_pairs",
    "ai_draft_record_sha256",
    "draft_mode",
    "review_decision",
    "review_final_family",
    "review_rationale",
    "reviewer_id",
    "reviewed_at_utc",
    "sign_off_sha256",
)
QUEUE_FIELDS: tuple[str, ...] = (
    "priority_rank",
    "task_id",
    "priority_class",
    "priority_score",
    "coder_a_family",
    "coder_b_family",
    "ai_draft_family",
    "coder_a_confidence",
    "coder_b_confidence",
    "agreement_status",
    "reason",
)

CONFIDENCE_SCORE = {"LOW": 3, "MEDIUM": 2, "HIGH": 1}


@dataclass(frozen=True, slots=True)
class QueueEntry:
    task_id: str
    priority_class: str
    priority_score: int
    reason: str
    agreement_status: str


def _train_pairs_payload(task: TrainTask) -> list[dict[str, object]]:
    return [{"input": pair["input"], "output": pair["output"]} for pair in task.raw_pairs]


def _draft_columns(label: Label) -> dict[str, object]:
    return {
        "ai_draft_family": label.primary_family,
        "ai_draft_confidence": label.confidence,
        "ai_draft_observed_change": label.observed_change,
        "ai_draft_competing_interpretation": label.competing_interpretation,
        "ai_draft_decision_basis": label.decision_basis,
        "ai_draft_evidence_pairs": ";".join(str(i) for i in label.evidence_pair_indices),
        "ai_draft_record_sha256": label.record_hash(),
        "draft_mode": label.mode,
    }


def _blank_review_columns() -> dict[str, str]:
    return {
        "review_decision": "",
        "review_final_family": "",
        "review_rationale": "",
        "reviewer_id": "",
        "reviewed_at_utc": "",
        "sign_off_sha256": "",
    }


def build_coder_packet(packet: Packet, drafts: Mapping[str, Label]) -> list[dict[str, object]]:
    """One reviewer's blinded view: training pairs plus only their own AI draft."""
    rows = []
    for task in packet.tasks:
        label = drafts.get(task.task_id)
        if label is None:
            raise ValueError(f"{task.task_id}: missing AI draft for coder packet")
        rows.append(
            {
                "task_id": task.task_id,
                "train_pairs": _train_pairs_payload(task),
                **_draft_columns(label),
                **_blank_review_columns(),
            }
        )
    return rows


def build_adjudicator_packet(
    packet: Packet, a: Mapping[str, Label], b: Mapping[str, Label], c: Mapping[str, Label]
) -> list[dict[str, object]]:
    """Adjudicator view: both coder drafts plus the AI synthesis, no test data."""
    rows = []
    for task in packet.tasks:
        left, right, final = a.get(task.task_id), b.get(task.task_id), c.get(task.task_id)
        if left is None or right is None or final is None:
            raise ValueError(f"{task.task_id}: missing draft for adjudicator packet")
        rows.append(
            {
                "task_id": task.task_id,
                "train_pairs": _train_pairs_payload(task),
                "coder_a_family": left.primary_family,
                "coder_b_family": right.primary_family,
                **_draft_columns(final),
                **_blank_review_columns(),
            }
        )
    return rows


def _priority(tasks: Sequence[TrainTask], a: Mapping[str, Label], b: Mapping[str, Label], c: Mapping[str, Label], agreement: AgreementResult) -> list[QueueEntry]:
    conflict = set(agreement.disagreements)
    entries: list[QueueEntry] = []
    for task in tasks:
        left, right, final = a[task.task_id], b[task.task_id], c[task.task_id]
        low = CONFIDENCE_SCORE.get(left.confidence, 0) + CONFIDENCE_SCORE.get(right.confidence, 0)
        if task.task_id in conflict:
            cls, reason = "A_CODERS_DISAGREE", (
                f"coder readings conflict ({left.primary_family} versus {right.primary_family}); "
                f"AI synthesis chose {final.primary_family}"
            )
            score = 100 + low
        elif final.primary_family == "UNKNOWN_AMBIGUOUS":
            cls, reason = "B_UNRESOLVED_AMBIGUOUS", "no primary family was asserted; the rubric may need a decision rule"
            score = 80 + low
        elif "LOW" in (left.confidence, right.confidence):
            cls, reason = "C_LOW_CONFIDENCE", "coders agree on the family but at least one reported low confidence"
            score = 60 + low
        else:
            cls, reason = "D_ROUTINE_CONFIRM", "labels agree with at least medium confidence; spot-check only"
            score = low
        entries.append(
            QueueEntry(
                task_id=task.task_id,
                priority_class=cls,
                priority_score=score,
                reason=reason,
                agreement_status="AGREE" if task.task_id not in conflict else "DISAGREE",
            )
        )
    entries.sort(key=lambda entry: (-entry.priority_score, entry.task_id))
    return entries


def queue_rows(
    packet: Packet,
    a: Mapping[str, Label],
    b: Mapping[str, Label],
    c: Mapping[str, Label],
    agreement: AgreementResult,
) -> list[dict[str, str | int]]:
    rows = []
    for rank, entry in enumerate(_priority(packet.tasks, a, b, c, agreement), start=1):
        left, right, final = a[entry.task_id], b[entry.task_id], c[entry.task_id]
        rows.append(
            {
                "priority_rank": rank,
                "task_id": entry.task_id,
                "priority_class": entry.priority_class,
                "priority_score": entry.priority_score,
                "coder_a_family": left.primary_family,
                "coder_b_family": right.primary_family,
                "ai_draft_family": final.primary_family,
                "coder_a_confidence": left.confidence,
                "coder_b_confidence": right.confidence,
                "agreement_status": entry.agreement_status,
                "reason": entry.reason,
            }
        )
    return rows


def _write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> str:
    lines = [json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=True) for row in rows]
    payload = "\n".join(lines) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_review_packets(
    packet: Packet,
    a: Mapping[str, Label],
    b: Mapping[str, Label],
    c: Mapping[str, Label],
    agreement: AgreementResult,
    out_dir: Path | str,
) -> dict[str, object]:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    hashes = {
        "reviewer_A_packet.jsonl": _write_jsonl(output / "reviewer_A_packet.jsonl", build_coder_packet(packet, a)),
        "reviewer_B_packet.jsonl": _write_jsonl(output / "reviewer_B_packet.jsonl", build_coder_packet(packet, b)),
        "reviewer_C_packet.jsonl": _write_jsonl(
            output / "reviewer_C_packet.jsonl", build_adjudicator_packet(packet, a, b, c)
        ),
    }

    rows = queue_rows(packet, a, b, c, agreement)
    queue_path = output / "disagreement_priority_queue.csv"
    with queue_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(QUEUE_FIELDS), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    hashes[queue_path.name] = hashlib.sha256(queue_path.read_bytes()).hexdigest()

    counts: dict[str, int] = {}
    for row in rows:
        key = str(row["priority_class"])
        counts[key] = counts.get(key, 0) + 1

    manifest = {
        "protocol": REVIEW_PACKET_PROTOCOL,
        "status": "AI_DRAFT_FOR_HUMAN_REVIEW_ONLY",
        "task_count": len(packet.tasks),
        "source_packet_sha256": packet.sha256,
        "coder_fields": list(CODER_FIELDS),
        "adjudicator_fields": list(ADJUDICATOR_FIELDS),
        "queue_fields": list(QUEUE_FIELDS),
        "queue_counts": counts,
        "review_fields_prefilled": False,
        "excluded_fields": [
            "test",
            "test.input",
            "test.output",
            "solver_programs",
            "traces",
            "candidate_yield",
            "future_value",
        ],
        "blinding_note": (
            "reviewer_A_packet.jsonl exposes only coder A's AI draft; reviewer_B_packet.jsonl exposes only "
            "coder B's. Neither reveals the other coder's labels or the AI adjudication."
        ),
        "packet_sha256": hashes,
    }
    (output / "review_packet_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest
