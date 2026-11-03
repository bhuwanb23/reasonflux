"""Human review records and promotion rules for the WP3 family map.

This module makes the difference between an AI draft and human-accepted evidence
structurally enforceable. A record can only become human evidence when it
carries a complete reviewer sign-off whose subject hash matches the exact AI
draft the reviewer saw. Editing a CSV value, relabelling a column, or writing a
new status string is not sufficient: the sign-off hash is computed from the AI
draft, and any change to the draft breaks verification.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import re
from typing import Iterable, Mapping, Sequence

from experiments.phase2ia.wp3_agents import Label
from experiments.phase2ia.wp3_packet_loader import canonical_sha256

REVIEW_SCHEMA_VERSION = "WP3-HUMAN-REVIEW-V1"
SIGN_OFF_ALGORITHM = "sha256(draft_record_sha256|reviewer_id|role|decision|final_family|rationale)"

# ISO-8601 date-time; kept strict so an untimestamped claim cannot pass.
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
_MIN_RATIONALE_CHARS = 20


class ReviewState(StrEnum):
    UNREVIEWED = "UNREVIEWED"
    ACCEPTED_BY_HUMAN = "ACCEPTED_BY_HUMAN"
    EDITED_BY_HUMAN = "EDITED_BY_HUMAN"
    ADJUDICATED_BY_HUMAN = "ADJUDICATED_BY_HUMAN"


class ReviewError(ValueError):
    """Raised when a review record cannot legitimately count as human evidence."""


@dataclass(frozen=True, slots=True)
class HumanReview:
    """One human's decision about one AI draft.

    ``draft_record_sha256`` binds the review to the exact draft that was shown,
    so a later edit to the AI label invalidates the review instead of silently
    inheriting its authority.
    """

    task_id: str
    role: str
    reviewer_id: str
    decision: ReviewState
    final_family: str
    rationale: str
    reviewed_at_utc: str
    draft_record_sha256: str
    sign_off_sha256: str
    schema_version: str = REVIEW_SCHEMA_VERSION

    def subject_payload(self) -> str:
        return "|".join(
            (
                self.draft_record_sha256,
                self.reviewer_id,
                self.role,
                str(self.decision),
                self.final_family,
                self.rationale,
            )
        )

    def expected_sign_off(self) -> str:
        return canonical_sha256({"payload": self.subject_payload(), "algorithm": SIGN_OFF_ALGORITHM})

    def validate(self) -> None:
        if self.schema_version != REVIEW_SCHEMA_VERSION:
            raise ReviewError(f"{self.task_id}: unknown review schema {self.schema_version}")
        if self.decision not in {
            ReviewState.ACCEPTED_BY_HUMAN,
            ReviewState.EDITED_BY_HUMAN,
            ReviewState.ADJUDICATED_BY_HUMAN,
        }:
            raise ReviewError(f"{self.task_id}: decision {self.decision} is not a human review outcome")
        if not self.reviewer_id.strip():
            raise ReviewError(f"{self.task_id}: reviewer identity is required")
        if len(self.rationale.strip()) < _MIN_RATIONALE_CHARS:
            raise ReviewError(
                f"{self.task_id}: human rationale must be at least {_MIN_RATIONALE_CHARS} characters"
            )
        if not _TIMESTAMP.match(self.reviewed_at_utc):
            raise ReviewError(f"{self.task_id}: reviewed_at_utc must be an ISO-8601 timestamp")
        if not re.fullmatch(r"[0-9a-f]{64}", self.draft_record_sha256):
            raise ReviewError(f"{self.task_id}: draft_record_sha256 must be a sha256 hex digest")
        if self.sign_off_sha256 != self.expected_sign_off():
            raise ReviewError(f"{self.task_id}: sign-off hash does not match the review payload")


def sign_review(
    *,
    task_id: str,
    role: str,
    reviewer_id: str,
    decision: ReviewState,
    final_family: str,
    rationale: str,
    reviewed_at_utc: str,
    draft: Label,
) -> HumanReview:
    """Create a signed review record. Callers must supply real reviewer facts."""
    review = HumanReview(
        task_id=task_id,
        role=role,
        reviewer_id=reviewer_id,
        decision=decision,
        final_family=final_family,
        rationale=rationale,
        reviewed_at_utc=reviewed_at_utc,
        draft_record_sha256=draft.record_hash(),
        sign_off_sha256="",
    )
    return replace(review, sign_off_sha256=review.expected_sign_off())


def verify_reviews(drafts: Mapping[str, Label], reviews: Iterable[HumanReview]) -> dict[str, HumanReview]:
    """Validate reviews against the drafts they claim to judge.

    Fails closed on unknown tasks, duplicate reviewers for one task, drafts that
    changed after review, and any missing sign-off field.
    """
    verified: dict[str, HumanReview] = {}
    for review in reviews:
        draft = drafts.get(review.task_id)
        if draft is None:
            raise ReviewError(f"{review.task_id}: review targets a task with no AI draft")
        review.validate()
        if review.draft_record_sha256 != draft.record_hash():
            raise ReviewError(
                f"{review.task_id}: review was signed against a different draft; "
                "re-review the current label instead of reusing the signature"
            )
        key = f"{review.task_id}:{review.role}"
        if key in verified:
            raise ReviewError(f"{review.task_id}: duplicate review for role {review.role}")
        verified[key] = review
    return verified


def human_coverage(
    drafts: Mapping[str, Label],
    reviews: Iterable[HumanReview],
    *,
    required_roles: Sequence[str] = ("A", "B"),
) -> dict[str, object]:
    """Report which tasks have complete, verified human coverage.

    A task is human-covered only when every required role signed a review of the
    current draft. Nothing here can be satisfied by the AI drafts alone.
    """
    verified = verify_reviews(drafts, reviews)
    by_task: dict[str, set[str]] = {}
    for review in verified.values():
        by_task.setdefault(review.task_id, set()).add(review.role)
    covered = sorted(task for task, roles in by_task.items() if set(required_roles) <= roles)
    return {
        "total_tasks": len(drafts),
        "verified_reviews": len(verified),
        "tasks_with_any_review": len(by_task),
        "tasks_fully_covered": len(covered),
        "tasks_missing_review": sorted(set(drafts) - set(covered)),
        "human_gate_complete": bool(drafts) and len(covered) == len(drafts),
    }


def promotion_blockers(
    drafts: Mapping[str, Label],
    reviews: Sequence[HumanReview],
    *,
    required_roles: Sequence[str] = ("A", "B"),
    adjudicator_role: str = "C",
) -> tuple[str, ...]:
    """Reasons the AI family map still cannot be treated as human evidence."""
    blockers: list[str] = []
    try:
        coverage = human_coverage(drafts, reviews, required_roles=required_roles)
    except ReviewError as exc:
        return (f"review validation failed: {exc}",)

    if not coverage["human_gate_complete"]:
        blockers.append(
            f"{coverage['tasks_missing_review'].__len__()} of {coverage['total_tasks']} tasks lack complete "
            f"reviews from all required roles {tuple(required_roles)}"
        )
    reviewed = {review.task_id for review in reviews}
    if not any(review.role == adjudicator_role for review in reviews):
        blockers.append(f"no human adjudication records for role {adjudicator_role}")
    disagreements = [task for task, label in drafts.items() if label.agent_id == "C" and task in reviewed]
    if not disagreements and reviews:
        blockers.append("no disagreement adjudications exist to verify")
    return tuple(blockers)


def can_promote_to_human_evidence(
    drafts: Mapping[str, Label],
    reviews: Sequence[HumanReview],
    *,
    required_roles: Sequence[str] = ("A", "B"),
) -> bool:
    return not promotion_blockers(drafts, reviews, required_roles=required_roles)
