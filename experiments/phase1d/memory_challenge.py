"""Phase 1D memory-challenge design contracts; no research outcome simulation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class BudgetCaps:
    training_examples: int = 24
    storage_bytes: int = 4096
    candidate_units: int = 24
    training_compute_ops: int = 50_000
    inference_ops_per_task: int = 2_000
    retrieval_checks_per_task: int = 4
    future_tasks_per_family: int = 12


@dataclass(frozen=True)
class FamilySpec:
    family_id: str
    name: str
    exact_precedent: bool
    context_transform: bool
    composition_required: bool
    structural_relation_preserved: bool
    novel_family: bool
    adversarial_lure: bool
    design_role: str
    expected_mechanism: str


FAMILIES = (
    FamilySpec("A", "Exact Replay", True, False, False, False, False, False,
               "positive control: memory sufficiency", "M1 exact episodic memory"),
    FamilySpec("B", "Context Shift", False, True, False, True, False, False,
               "same principle, changed surface/context", "abstraction over exact retrieval"),
    FamilySpec("C", "Composition Shift", False, True, True, True, False, False,
               "unseen composition with a case-specific parameter", "hybrid memory + abstraction"),
    FamilySpec("D", "Structural Analogy", False, True, False, True, True, False,
               "relation preserved under new surface representation", "abstraction"),
    FamilySpec("E", "Far Transfer", False, True, False, True, True, False,
               "no exact or near precedent; learned rule still applies", "abstraction, if construct is valid"),
    FamilySpec("F", "Adversarial Memory", False, True, False, False, False, True,
               "high-similarity distractor maps to wrong rule", "verified abstraction/hybrid over unverified retrieval"),
)

MEMORY_TYPES = {
    "M1_EXACT_EPISODIC": "Store exact training task/solution pairs; replay only on permitted exact-key hit.",
    "M2_PARTIAL_EPISODIC": "Store task/trace fragments; cannot invent missing steps or parameters.",
    "M3_PATTERN_MEMORY": "Store recurring surface/sequence patterns with provenance; not a symbolic generalized rule.",
    "M4_SKILL_ABSTRACTION": "Store explicit generalized rule/skill objects and apply to eligible shifted tasks.",
    "M5_HYBRID": "Combine exact/partial episodic records with abstract rules under the same total budget caps.",
}

ARMS = (
    "B1A_M1_EXACT", "B1B_M2_PARTIAL", "B1C_M3_PATTERN",
    "B2_M4_ABSTRACTION", "B3_M5_HYBRID", "B4_RANDOM_RETRIEVAL",
    "B5_NO_LEARNING", "B6_ORACLE_ANALYSIS_ONLY",
)

# Each family appears in each split. IDs are generated from split/family/seed,
# and future labels are stored separately. A's exact training precedent is an
# explicitly preregistered exposure condition, not an accidental test answer.
SPLITS = ("development", "confirmatory", "replication")


def validate_budget_ledger(ledger: Mapping[str, Mapping[str, int]], caps: BudgetCaps | None = None) -> bool:
    caps = caps or BudgetCaps()
    limits = {
        "training_examples": caps.training_examples,
        "storage_bytes": caps.storage_bytes,
        "candidate_units": caps.candidate_units,
        "training_compute_ops": caps.training_compute_ops,
        "inference_ops_per_task": caps.inference_ops_per_task,
        "retrieval_checks_per_task": caps.retrieval_checks_per_task,
    }
    if set(ledger) != set(ARMS[:-1]):
        return False
    return all(all(0 <= int(values.get(metric, -1)) <= limit for metric, limit in limits.items())
               for values in ledger.values())


def has_intended_memory_win(family: FamilySpec) -> bool:
    return family.family_id == "A" and family.exact_precedent and not family.adversarial_lure


def has_intended_abstraction_challenge(family: FamilySpec) -> bool:
    return family.family_id in {"B", "D", "E", "F"} and not family.exact_precedent


def has_intended_hybrid_challenge(family: FamilySpec) -> bool:
    return family.family_id == "C" and family.composition_required and family.context_transform


def outcome_label_is_separate(policy_payload_fields: set[str]) -> bool:
    forbidden = {"gold_answer", "future_utility", "test_label", "hidden_rule", "future_success"}
    return not bool(policy_payload_fields & forbidden)
