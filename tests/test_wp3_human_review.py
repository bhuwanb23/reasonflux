"""Tests for the WP3 human-review workflow and provenance enforcement.

The central claim under test is negative: no AI draft can become human evidence
by editing a CSV, renaming a column, or writing a status string. Only a signed
review bound to the exact draft hash counts.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from experiments.phase2ia.wp3_human_review import (  # noqa: E402
    HumanReview,
    ReviewError,
    ReviewState,
    can_promote_to_human_evidence,
    human_coverage,
    promotion_blockers,
    sign_review,
    verify_reviews,
)
from experiments.phase2ia.wp3_label import LABEL_MODE, Label  # noqa: E402
from experiments.phase2ia.wp3_provisional import (  # noqa: E402
    default_paths,
    run_provisional_workflow,
    write_bundle,
)
from experiments.phase2ia.wp3_review_packets import (  # noqa: E402
    ADJUDICATOR_FIELDS,
    CODER_FIELDS,
    QUEUE_FIELDS,
)

PACKAGE = ROOT / "reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
ARTIFACT_DIR = PACKAGE / "wp3_provisional_v1"
TIMESTAMP = "2026-11-03T13:00:00Z"


@pytest.fixture(scope="module")
def bundle():
    packet_path, manifest_path, _ = default_paths()
    return run_provisional_workflow(packet_path, manifest_path=manifest_path)


def _sign(draft: Label, *, role: str = "A", reviewer: str = "reviewer-alpha") -> HumanReview:
    return sign_review(
        task_id=draft.task_id,
        role=role,
        reviewer_id=reviewer,
        decision=ReviewState.ACCEPTED_BY_HUMAN,
        final_family=draft.primary_family,
        rationale="I read the training pairs and agree with the draft reading here.",
        reviewed_at_utc=TIMESTAMP,
        draft=draft,
    )


def test_every_draft_has_a_complete_audit_trail(bundle):
    for label in (*bundle.a, *bundle.b, *bundle.c):
        assert label.observed_change.strip(), label.task_id
        assert label.competing_interpretation.strip(), label.task_id
        assert label.decision_basis.strip(), label.task_id
        assert label.audit_gaps() == (), (label.task_id, label.audit_gaps())
        assert label.mode == LABEL_MODE


def test_audit_fields_are_part_of_the_record_hash(bundle):
    original = bundle.a[0]
    changed = replace(original, decision_basis=original.decision_basis + " (tampered)")
    assert changed.record_hash() != original.record_hash()


def test_signed_review_verifies_against_its_draft(bundle):
    draft = bundle.a[0]
    review = _sign(draft)
    verified = verify_reviews({draft.task_id: draft}, [review])
    assert list(verified) == [f"{draft.task_id}:A"]


def test_review_rejected_if_draft_changed_after_signing(bundle):
    draft = bundle.a[0]
    review = _sign(draft)
    edited = replace(draft, primary_family="SPATIAL_CHANGE")
    with pytest.raises(ReviewError, match="different draft"):
        verify_reviews({edited.task_id: edited}, [review])


def test_review_rejected_without_reviewer_timestamp_or_rationale(bundle):
    draft = bundle.a[0]

    no_reviewer = _sign(draft)
    object.__setattr__(no_reviewer, "reviewer_id", "")
    with pytest.raises(ReviewError):
        verify_reviews({draft.task_id: draft}, [no_reviewer])

    short_rationale = replace(
        _sign(draft), rationale="ok", sign_off_sha256=""
    )
    short_rationale = replace(short_rationale, sign_off_sha256=short_rationale.expected_sign_off())
    with pytest.raises(ReviewError, match="rationale"):
        verify_reviews({draft.task_id: draft}, [short_rationale])

    bad_time = replace(_sign(draft), reviewed_at_utc="yesterday")
    bad_time = replace(bad_time, sign_off_sha256=bad_time.expected_sign_off())
    with pytest.raises(ReviewError, match="ISO-8601"):
        verify_reviews({draft.task_id: draft}, [bad_time])


def test_review_rejected_when_signature_does_not_match_payload(bundle):
    draft = bundle.a[0]
    forged = replace(_sign(draft), sign_off_sha256="0" * 64)
    with pytest.raises(ReviewError, match="sign-off hash"):
        verify_reviews({draft.task_id: draft}, [forged])


def test_unreviewed_state_is_not_a_human_outcome(bundle):
    draft = bundle.a[0]
    review = replace(_sign(draft), decision=ReviewState.UNREVIEWED)
    review = replace(review, sign_off_sha256=review.expected_sign_off())
    with pytest.raises(ReviewError, match="not a human review outcome"):
        verify_reviews({draft.task_id: draft}, [review])


def test_duplicate_role_reviews_are_rejected(bundle):
    draft = bundle.a[0]
    review = _sign(draft)
    with pytest.raises(ReviewError, match="duplicate review"):
        verify_reviews({draft.task_id: draft}, [review, review])


def test_single_signed_review_cannot_promote_the_family_map(bundle):
    drafts = {label.task_id: label for label in bundle.c}
    one_task = bundle.c[0]
    reviews = [_sign(one_task, role="A")]
    coverage = human_coverage(drafts, reviews)
    assert coverage["human_gate_complete"] is False
    assert coverage["tasks_fully_covered"] == 0
    assert can_promote_to_human_evidence(drafts, reviews) is False
    blockers = promotion_blockers(drafts, reviews)
    assert any("lack complete reviews" in blocker for blocker in blockers)


def test_no_reviews_means_blockers_report_incomplete_gate(bundle):
    drafts = {label.task_id: label for label in bundle.c}
    blockers = promotion_blockers(drafts, [])
    assert blockers
    assert any("no human adjudication records" in blocker for blocker in blockers)


def test_csv_status_edit_alone_does_not_create_human_evidence(bundle, tmp_path: Path):
    """Editing the CSV to claim a human review must not satisfy the gate."""
    write_bundle(bundle, tmp_path)
    map_path = tmp_path / "task_family_map.csv"
    with map_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0])
    for row in rows:
        row["review_status"] = "ACCEPTED_BY_HUMAN"
        row["reviewer_id"] = "someone"
        row["reviewed_at_utc"] = TIMESTAMP
        row["sign_off_sha256"] = hashlib.sha256(b"i promise").hexdigest()
    with map_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    drafts = {label.task_id: label for label in bundle.c}
    assert "ACCEPTED_BY_HUMAN" in map_path.read_text()
    # No HumanReview records exist, so the gate is still closed.
    assert can_promote_to_human_evidence(drafts, []) is False
    assert human_coverage(drafts, [])["human_gate_complete"] is False


def test_committed_bundle_ships_zero_human_reviews_and_open_gate():
    manifest = json.loads((ARTIFACT_DIR / "provisional_manifest.json").read_text(encoding="utf-8"))
    schema = manifest["human_review_schema"]
    assert schema["reviews_present"] == 0
    assert schema["promotion_blockers"]
    assert manifest["review_packets"]["review_fields_prefilled"] is False
    assert manifest["use_restrictions"]["wp3_completion"] is False
    assert manifest["status"] == "AI_PROVISIONAL_ONLY_NOT_WP3"

    with (ARTIFACT_DIR / "task_family_map.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 600
    assert all(row["review_status"] == "UNREVIEWED" for row in rows)
    assert all(row["reviewer_id"] == "" for row in rows)
    assert all(row["sign_off_sha256"] == "" for row in rows)
    assert all(row["adjudication_status"] == "PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN" for row in rows)


def test_label_csvs_expose_audit_fields_and_blank_review_columns(tmp_path: Path):
    packet_path, manifest_path, _ = default_paths()
    fresh = run_provisional_workflow(packet_path, manifest_path=manifest_path)
    write_bundle(fresh, tmp_path)
    with (tmp_path / "annotator_A_labels.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 600
    for row in rows:
        assert row["observed_change"].strip()
        assert row["competing_interpretation"].strip()
        assert row["decision_basis"].strip()
        assert row["review_status"] == "UNREVIEWED"
        assert row["sign_off_sha256"] == ""


def test_review_packets_are_blinded_complete_and_unfilled(tmp_path: Path):
    packet_path, manifest_path, _ = default_paths()
    fresh = run_provisional_workflow(packet_path, manifest_path=manifest_path)
    manifest = write_bundle(fresh, tmp_path)

    for name in ("reviewer_A_packet.jsonl", "reviewer_B_packet.jsonl", "reviewer_C_packet.jsonl"):
        lines = (tmp_path / name).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 600, name
        for line in lines:
            row = json.loads(line)
            assert row["train_pairs"]
            assert all(set(pair) == {"input", "output"} for pair in row["train_pairs"])
            for field in ("review_decision", "review_final_family", "review_rationale", "reviewer_id",
                          "reviewed_at_utc", "sign_off_sha256"):
                assert row[field] == "", (name, field)
            assert "test" not in row

    coder_a = json.loads((tmp_path / "reviewer_A_packet.jsonl").read_text(encoding="utf-8").splitlines()[0])
    coder_b = json.loads((tmp_path / "reviewer_B_packet.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert set(coder_a) == set(CODER_FIELDS)
    assert "coder_b_family" not in coder_a
    assert "coder_a_family" not in coder_b
    adjudicator = json.loads((tmp_path / "reviewer_C_packet.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert set(adjudicator) == set(ADJUDICATOR_FIELDS)
    assert manifest["review_packets"]["queue_counts"]


def test_priority_queue_ranks_conflicts_first_and_covers_every_task(tmp_path: Path):
    packet_path, manifest_path, _ = default_paths()
    fresh = run_provisional_workflow(packet_path, manifest_path=manifest_path)
    write_bundle(fresh, tmp_path)

    with (tmp_path / "disagreement_priority_queue.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 600
    assert list(rows[0]) == list(QUEUE_FIELDS)
    assert [int(row["priority_rank"]) for row in rows] == list(range(1, 601))
    scores = [int(row["priority_score"]) for row in rows]
    assert scores == sorted(scores, reverse=True)
    assert rows[0]["priority_class"] == "A_CODERS_DISAGREE"
    assert rows[-1]["priority_class"] == "D_ROUTINE_CONFIRM"
    assert sum(1 for row in rows if row["priority_class"] == "A_CODERS_DISAGREE") == len(
        fresh.agreement.disagreements
    )
    assert {row["task_id"] for row in rows} == {label.task_id for label in fresh.c}


def test_refuses_review_for_unknown_task(bundle):
    draft = bundle.a[0]
    review = _sign(draft)
    ghost = replace(review, task_id="does-not-exist")
    with pytest.raises(ReviewError, match="no AI draft"):
        verify_reviews({draft.task_id: draft}, [ghost])
