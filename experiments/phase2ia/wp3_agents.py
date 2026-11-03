"""Rubric-conditioned provisional annotators for WP3.

These are deterministic, auditable policies, not human coders. Agent A applies
mechanism-first scoring; Agent B applies the rubric's counter-hypothesis
priority and asks whether a surface action is secondary to selection, region,
count, or pattern structure. Agent C adjudicates only disagreements.

Every output is labelled ``AI_PROVISIONAL`` and carries the training-pair hash,
policy version, and evidence indices so it can never be mistaken for a human
annotation stream. This module re-exports the implementation split across
``wp3_label``, ``wp3_policy``, and ``wp3_adjudicator``.
"""
from __future__ import annotations

from experiments.phase2ia.wp3_adjudicator import adjudicate
from experiments.phase2ia.wp3_label import (
    DECISION_THRESHOLD,
    FAMILY_DESCRIPTIONS,
    LABEL_MODE,
    ONTOLOGY_VERSION,
    POLICY_VERSION,
    Label,
)
from experiments.phase2ia.wp3_policy import (
    POLICY_A_SPECIFICITY,
    POLICY_A_THRESHOLD,
    POLICY_B_SPECIFICITY,
    POLICY_B_THRESHOLD,
    TIERS,
    Score,
    annotate_agent_a,
    annotate_agent_b,
    family_scores,
    tier_of,
)

__all__ = [
    "DECISION_THRESHOLD",
    "FAMILY_DESCRIPTIONS",
    "LABEL_MODE",
    "ONTOLOGY_VERSION",
    "POLICY_A_SPECIFICITY",
    "POLICY_A_THRESHOLD",
    "POLICY_B_SPECIFICITY",
    "POLICY_B_THRESHOLD",
    "POLICY_VERSION",
    "Score",
    "TIERS",
    "Label",
    "adjudicate",
    "annotate_agent_a",
    "annotate_agent_b",
    "family_scores",
    "tier_of",
]
