"""Label record and ontology constants for the WP3 provisional workflow.

The ``Label`` type is the single carrier of one agent's judgement. It refuses to
exist without a valid ontology family, a confidence level, evidence indices, and
a rationale, and it always stamps the training-pair hash plus the
``AI_PROVISIONAL`` mode.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from experiments.phase2ia.wp3_features import TaskFeatures
from experiments.phase2ia.wp3_packet_loader import (
    CONFIDENCE_LEVELS,
    PRIMARY_FAMILIES,
    TrainTask,
    canonical_sha256,
)

ONTOLOGY_VERSION = "WP3-ONTOLOGY-V1"
POLICY_VERSION = "WP3-AI-PROVISIONAL-V2"
LABEL_MODE = "AI_PROVISIONAL"
DECISION_THRESHOLD = 0.20

FAMILY_DESCRIPTIONS: Mapping[str, str] = {
    "OBJ_RELATION": "an entity is selected by a semantic property or relation, and that selection determines the output",
    "SPATIAL_CHANGE": "existing content is moved, rotated, reflected, or rearranged geometrically",
    "COLOR_ATTRIBUTE": "occupied positions are preserved while colours or attributes are reassigned",
    "COUNT_REPLICATION": "multiplicity, scaling, tiling, or a number derived from the input determines the output",
    "PATTERN_COMPLETION": "a repeated or symmetric visual pattern is completed, extrapolated, or regularised",
    "REGION_TOPOLOGY": "enclosure, connectivity, separation, or region structure governs the change",
    "FRAME_BOUNDS": "cropping, padding, border, or canvas extent is the central transformation",
    "SYMBOLIC_SEQUENCE": "a numeric, ordinal, or arithmetic progression determines the output",
    "COMPOSITE_RULE": "two or more mechanisms are jointly necessary and no single mechanism dominates",
    "UNKNOWN_AMBIGUOUS": "the demonstrations do not separate the competing explanations",
}


@dataclass(frozen=True, slots=True)
class Label:
    """One agent's judgement, with the audit fields a human reviewer needs.

    ``observed_change``, ``competing_interpretation``, and ``decision_basis``
    are the reviewer-facing audit trail. They are part of the record hash, so a
    human cannot silently rewrite the rationale of an AI draft.
    """

    task_id: str
    agent_id: str
    primary_family: str
    confidence: str
    evidence_pair_indices: tuple[int, ...]
    rationale: str
    ambiguity_notes: str
    secondary_tags: tuple[str, ...]
    train_pairs_sha256: str
    observed_change: str = ""
    competing_interpretation: str = ""
    decision_basis: str = ""
    contributions: tuple[tuple[str, float], ...] = ()
    ontology_version: str = ONTOLOGY_VERSION
    policy_version: str = POLICY_VERSION
    mode: str = LABEL_MODE

    def __post_init__(self) -> None:
        if self.primary_family not in PRIMARY_FAMILIES:
            raise ValueError(f"{self.task_id}: family outside the frozen ontology: {self.primary_family}")
        if self.confidence not in CONFIDENCE_LEVELS:
            raise ValueError(f"{self.task_id}: invalid confidence {self.confidence}")
        if not self.evidence_pair_indices:
            raise ValueError(f"{self.task_id}: at least one evidence pair index is required")
        if not self.rationale.strip():
            raise ValueError(f"{self.task_id}: a rationale is required")

    def audit_gaps(self) -> tuple[str, ...]:
        """Names of audit fields a reviewer would find empty."""
        gaps = []
        if not self.observed_change.strip():
            gaps.append("observed_change")
        if not self.competing_interpretation.strip():
            gaps.append("competing_interpretation")
        if not self.decision_basis.strip():
            gaps.append("decision_basis")
        if not self.rationale.strip():
            gaps.append("rationale")
        return tuple(gaps)

    def record_hash(self) -> str:
        return canonical_sha256(
            {
                "task_id": self.task_id,
                "agent_id": self.agent_id,
                "primary_family": self.primary_family,
                "confidence": self.confidence,
                "evidence_pair_indices": list(self.evidence_pair_indices),
                "rationale": self.rationale,
                "ambiguity_notes": self.ambiguity_notes,
                "secondary_tags": list(self.secondary_tags),
                "train_pairs_sha256": self.train_pairs_sha256,
                "observed_change": self.observed_change,
                "competing_interpretation": self.competing_interpretation,
                "decision_basis": self.decision_basis,
                "contributions": [list(item) for item in self.contributions],
                "ontology_version": self.ontology_version,
                "policy_version": self.policy_version,
                "mode": self.mode,
            }
        )


def all_pairs(features: TaskFeatures) -> tuple[int, ...]:
    return tuple(range(1, features.pair_count + 1))


def build_label(
    agent_id: str,
    task: TrainTask,
    *,
    family: str,
    confidence: str,
    evidence: tuple[int, ...],
    rationale: str,
    notes: str,
    secondary: Sequence[str],
    observed_change: str = "",
    competing_interpretation: str = "",
    decision_basis: str = "",
    contributions: Sequence[tuple[str, float]] = (),
) -> Label:
    return Label(
        task_id=task.task_id,
        agent_id=agent_id,
        primary_family=family,
        confidence=confidence,
        evidence_pair_indices=evidence,
        rationale=rationale,
        ambiguity_notes=notes,
        secondary_tags=tuple(sorted(set(secondary))),
        train_pairs_sha256=task.train_pairs_sha256,
        observed_change=observed_change,
        competing_interpretation=competing_interpretation,
        decision_basis=decision_basis,
        contributions=tuple(contributions),
    )
