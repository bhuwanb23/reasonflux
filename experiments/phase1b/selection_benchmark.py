"""Phase 1B selection-pressure contract harness (synthetic fixtures only).

This module validates selector plumbing and pressure on generated contract fixtures.
It is not the confirmatory SCT evaluation and its outcomes are not research evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random
from typing import Iterable

N_CANDIDATES = 20
CAPACITY = 8
STORAGE_BUDGET = 8.0
HORIZON = 10
MC_ESTIMATE = 0.06
SPLITS = ("calibration", "development", "confirmatory", "replication")
TYPES = ("A", "B", "C", "D", "E")
SIMPLE_CONTESTANTS = ("S2_FREQUENCY", "S3_REUSE", "S4_RANDOM")


@dataclass(frozen=True)
class CandidateCard:
    candidate_id: str
    split: str
    batch_seed: int
    arrival_order: int
    frequency: float
    p_reuse: float
    AG: float
    TS: float
    CC: float
    MC: float = MC_ESTIMATE
    storage_units: float = 1.0

    def selector_payload(self) -> dict[str, object]:
        """Only public pre-decision fields; never includes labels or outcomes."""
        return {
            "candidate_id": self.candidate_id,
            "split": self.split,
            "batch_seed": self.batch_seed,
            "arrival_order": self.arrival_order,
            "frequency": self.frequency,
            "p_reuse": self.p_reuse,
            "AG": self.AG,
            "TS": self.TS,
            "CC": self.CC,
            "MC": self.MC,
            "storage_units": self.storage_units,
        }


@dataclass(frozen=True)
class TruthRecord:
    candidate_id: str
    latent_type: str
    latent_expected_value: float
    latent_gross_future_utility: float
    opportunity_probability: float
    paired_utility_deltas: tuple[float, ...]
    creation_cost_teu: float
    maintenance_cost_teu: tuple[float, ...]


@dataclass(frozen=True)
class Batch:
    split: str
    seed: int
    cards: tuple[CandidateCard, ...]
    sealed_truth: tuple[TruthRecord, ...]
    type_counts_manifest: tuple[tuple[str, int], ...]


def scv10(card: CandidateCard) -> float:
    """Frozen Phase 13C score mapping, kept separate from ground truth."""
    clip = lambda x: min(1.0, max(0.0, float(x)))
    return HORIZON * clip(card.p_reuse) * clip(card.AG) * clip(card.TS) - max(0.0, card.CC) - HORIZON * card.MC


def _tie_key(card: CandidateCard, salt: str) -> str:
    return hashlib.sha256(f"{salt}|{card.candidate_id}".encode()).hexdigest()


def choose(cards: Iterable[CandidateCard], policy: str, *, rng_seed: str | None = None) -> tuple[str, ...]:
    cards = tuple(cards)
    by_id = {c.candidate_id: c for c in cards}
    if len(by_id) != len(cards):
        raise ValueError("candidate IDs must be unique")
    if policy == "S1_SCV":
        eligible = [c for c in cards if scv10(c) > 0.0]
        ordered = sorted(eligible, key=lambda c: (-scv10(c), _tie_key(c, "scv-v1")))
        return tuple(c.candidate_id for c in ordered[:CAPACITY])
    if policy == "S2_FREQUENCY":
        ordered = sorted(cards, key=lambda c: (-c.frequency, _tie_key(c, "frequency-v1")))
        return tuple(c.candidate_id for c in ordered[:CAPACITY])
    if policy == "S3_REUSE":
        ordered = sorted(cards, key=lambda c: (-c.p_reuse, _tie_key(c, "reuse-v1")))
        return tuple(c.candidate_id for c in ordered[:CAPACITY])
    if policy == "S4_RANDOM":
        if rng_seed is None:
            raise ValueError("random selector requires a recorded seed")
        rng = random.Random(rng_seed)
        return tuple(sorted(c.candidate_id for c in rng.sample(cards, CAPACITY)))
    if policy == "S5_ALWAYS_CAPACITY":
        ordered = sorted(cards, key=lambda c: (c.arrival_order, c.candidate_id))
        return tuple(c.candidate_id for c in ordered[:CAPACITY])
    if policy == "S6_NEVER":
        return tuple()
    raise ValueError(f"unknown production selector {policy!r}; oracle is analysis-only")


def oracle_select(cards: Iterable[CandidateCard], truths: Iterable[TruthRecord]) -> tuple[str, ...]:
    """Analysis-only oracle. Never called by production selector/pressure code."""
    cards = tuple(cards)
    truth_by_id = {t.candidate_id: t for t in truths}
    ranked = sorted(cards, key=lambda c: (-truth_by_id[c.candidate_id].latent_expected_value,
                                          _tie_key(c, "oracle-analysis-only-v1")))
    return tuple(c.candidate_id for c in ranked[:CAPACITY])


def future_net_value(truth: TruthRecord) -> float:
    """Fixture truth uses paired outcomes and costs, never selector scores."""
    if len(truth.paired_utility_deltas) != HORIZON or len(truth.maintenance_cost_teu) != HORIZON:
        raise ValueError("truth record must contain exactly the frozen ten-opportunity horizon")
    return (sum(truth.paired_utility_deltas) - truth.creation_cost_teu
            - sum(truth.maintenance_cost_teu))


def portfolio_net_value(selection: Iterable[str], truths: Iterable[TruthRecord]) -> float:
    """Mean fixture net value per available slot; empty never-create arm is zero."""
    selected = tuple(selection)
    if not selected:
        return 0.0
    truth_by_id = {t.candidate_id: t for t in truths}
    if len(selected) > CAPACITY or any(cid not in truth_by_id for cid in selected):
        raise ValueError("selection exceeds capacity or lacks a truth record")
    return sum(future_net_value(truth_by_id[cid]) for cid in selected) / CAPACITY


def pairwise_divergence(a: Iterable[str], b: Iterable[str], n: int = N_CANDIDATES) -> float:
    return len(set(a) ^ set(b)) / n


def pairwise_matrix(selections: dict[str, Iterable[str]]) -> dict[str, dict[str, float]]:
    return {a: {b: pairwise_divergence(sa, sb) for b, sb in selections.items()}
            for a, sa in selections.items()}


def contested_sdr(selections: dict[str, Iterable[str]]) -> float:
    names = ("S1_SCV", "S2_FREQUENCY", "S3_REUSE", "S4_RANDOM")
    vals = [pairwise_divergence(selections[a], selections[b])
            for i, a in enumerate(names) for b in names[i + 1:]]
    return sum(vals) / len(vals)


def pressure_gate(cards: tuple[CandidateCard, ...], selections: dict[str, tuple[str, ...]]) -> tuple[bool, dict[str, object]]:
    """Uses only pre-outcome cards and selector decisions; deliberately no TruthRecord arg."""
    n = len(cards)
    expected = {"S1_SCV": CAPACITY, "S2_FREQUENCY": CAPACITY, "S3_REUSE": CAPACITY,
                "S4_RANDOM": CAPACITY, "S5_ALWAYS_CAPACITY": CAPACITY, "S6_NEVER": 0}
    rates_ok = n == N_CANDIDATES and all(len(selections[k]) == v for k, v in expected.items())
    pair = {(a, b): pairwise_divergence(selections[a], selections[b])
            for a, b in (("S1_SCV", "S2_FREQUENCY"), ("S1_SCV", "S3_REUSE"),
                         ("S1_SCV", "S4_RANDOM"))}
    sdr = contested_sdr(selections)
    gate = rates_ok and all(x >= 0.10 for x in pair.values()) and sdr >= 0.20
    return gate, {"candidate_count": n, "selection_rates_ok": rates_ok,
                  "scv_pairwise": {f"{a}__{b}": v for (a, b), v in pair.items()},
                  "contested_sdr": sdr, "pressure_pass": gate}


def _candidate_features(kind: str, j: int) -> tuple[float, float, float, float, float]:
    """Frozen test-fixture score profiles; intentionally separate from truth recipes."""
    if kind == "A":
        return 0.60 + 0.02*j, 0.78 + 0.01*j, 0.85, 0.85, 0.10
    if kind == "B":
        return 0.45 + 0.02*j, 0.45 + 0.01*j, 0.40, 0.50, 0.10
    if kind == "C":
        return 0.96 - 0.01*j, 0.99 - 0.005*j, 0.15, 0.10, 0.10
    if kind == "D":
        return 0.88 + 0.01*j, 0.94 - 0.005*j, 0.85, 0.85, 0.10
    if kind == "E":
        return 0.08 + 0.01*j, 0.18 + 0.005*j, 0.95, 0.95, 0.10
    raise ValueError(kind)


def _truth_recipe(candidate_id: str, kind: str) -> TruthRecord:
    maint = (0.003,) * HORIZON
    if kind == "A":
        deltas = (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        create, gross, theta, p = 0.02, 5.00, 4.95, 0.50
    elif kind == "B":
        deltas = (0.0,) * HORIZON
        create, gross, theta, p = 0.02, 0.00, -0.05, 0.50
    elif kind == "C":
        deltas = (0.0,) * HORIZON
        create, gross, theta, p = 0.27, 0.00, -0.30, 0.50
    elif kind == "D":
        deltas = (1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0)
        create, gross, theta, p = 0.02, -6.00, -6.05, 0.50
    elif kind == "E":
        deltas = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        create, gross, theta, p = 0.02, 0.80, 0.75, 0.05
    else:
        raise ValueError(kind)
    return TruthRecord(candidate_id, kind, theta, gross, p, tuple(deltas), create, maint)


def make_batch(split: str, seed: int) -> Batch:
    """Create a deterministic fixture; opaque IDs/order are randomized independently of type."""
    if split not in SPLITS:
        raise ValueError(f"unknown split {split}")
    recipes = [(kind, j) for kind in TYPES for j in range(4)]
    order_rng = random.Random(f"ASFT-v1.1:panel-order:{split}:{seed}")
    order_rng.shuffle(recipes)
    cards, truths = [], []
    for position, (kind, j) in enumerate(recipes):
        # ID and arrival order disclose no class; assignment is fixed before truth is materialized.
        cid = f"{split.upper()}-{seed:04d}-CAND-{position+1:02d}"
        frequency, reuse, ag, ts, cc = _candidate_features(kind, j)
        cards.append(CandidateCard(cid, split, seed, position, frequency, reuse, ag, ts, cc))
        truths.append(_truth_recipe(cid, kind))
    return Batch(split, seed, tuple(cards), tuple(truths), tuple((t, 4) for t in TYPES))


def run_selectors(batch: Batch) -> dict[str, tuple[str, ...]]:
    cards = batch.cards
    selections = {
        "S1_SCV": choose(cards, "S1_SCV"),
        "S2_FREQUENCY": choose(cards, "S2_FREQUENCY"),
        "S3_REUSE": choose(cards, "S3_REUSE"),
        "S4_RANDOM": choose(cards, "S4_RANDOM", rng_seed=f"ASFT-v1.1:{batch.split}:{batch.seed}"),
        "S5_ALWAYS_CAPACITY": choose(cards, "S5_ALWAYS_CAPACITY"),
        "S6_NEVER": choose(cards, "S6_NEVER"),
    }
    return selections
