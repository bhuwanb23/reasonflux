"""Phase 1C ranking-pressure contract harness (synthetic fixtures only).

This is a benchmark-interface/contract test, not an IDT experiment. Future
truth and latent fixture classes are held outside CandidateCard and are never
passed to rankers or the pressure gate.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random
from typing import Mapping, Sequence


@dataclass(frozen=True)
class CandidateCard:
    candidate_id: str
    frequency: float
    consistency: float
    generality: float
    transfer_calibration: float
    reasoning_value: float
    reuse_probability: float
    compression_gain: float


TYPE_COUNTS = {"A": 4, "B": 8, "C": 8, "D": 4, "E": 4, "F": 4, "G": 4, "H": 4}
# Public card-feature means and independent synthetic future utility means.
# These are interface-test recipes, not fitted estimates or study outcomes.
FEATURE_MEANS = {
    "A": (.60, .90, .65, .50, .75, .95, .25),
    "B": (.95, .85, .20, .05, .30, .80, .10),
    "C": (.15, .85, .80, .88, .78, .20, .25),
    "D": (.12, .70, .25, .10, .20, .25, .12),
    "E": (.35, .90, .90, .95, .82, .25, .35),
    "F": (.68, .80, .25, .15, .55, .90, .30),
    "G": (.45, .75, .50, .35, .55, .70, .95),
    "H": (.90, .75, .40, .65, .75, .10, .25),
}
FUTURE_VALUE_MEANS = {"A": .45, "B": -.10, "C": .90, "D": -.08,
                      "E": .95, "F": .08, "G": .25, "H": -.40}
FEATURE_NAMES = ("frequency", "consistency", "generality", "transfer_calibration",
                 "reasoning_value", "reuse_probability", "compression_gain")


def _clip(x: float) -> float:
    return max(0.0, min(1.0, x))


def make_panel(seed: int = 0, panel: int = 0) -> tuple[list[CandidateCard], dict[str, str], dict[str, float]]:
    """Return public cards, hidden type map, and separate synthetic truth."""
    label_rng = random.Random((seed + 1) * 1_000_003 + panel * 101)
    feature_rng = random.Random((seed + 1) * 2_000_033 + panel * 211)
    truth_rng = random.Random((seed + 1) * 2_000_071 + panel * 223)
    id_rng = random.Random((seed + 1) * 3_000_017 + panel * 307)
    arrival_rng = random.Random((seed + 1) * 4_000_037 + panel * 401)
    types = [t for t, n in TYPE_COUNTS.items() for _ in range(n)]
    label_rng.shuffle(types)
    ids = ["CAND-" + hashlib.sha256(f"{seed}:{panel}:{i}:{id_rng.random()}".encode()).hexdigest()[:12]
           for i in range(len(types))]
    candidates = []
    hidden_types: dict[str, str] = {}
    truth: dict[str, float] = {}
    for cid, t in zip(ids, types):
        means = FEATURE_MEANS[t]
        vals = [_clip(v + feature_rng.uniform(-.035, .035)) for v in means]
        candidates.append(CandidateCard(cid, *vals))
        hidden_types[cid] = t
        truth[cid] = FUTURE_VALUE_MEANS[t] + truth_rng.uniform(-.025, .025)
    arrival_rng.shuffle(candidates)
    return candidates, hidden_types, truth


def _stable_rank(cards: Sequence[CandidateCard], scores: Mapping[str, float]) -> list[str]:
    return [c.candidate_id for c in sorted(cards, key=lambda c: (-scores[c.candidate_id], c.candidate_id))]


def rank_all(cards: Sequence[CandidateCard], *, seed: int = 0) -> dict[str, list[str]]:
    """Five executable policies. Every policy receives the same card pool."""
    # Current v1.1 transfer-aware validation score: F*C*G*T*R, where T is
    # calibration-only transfer evidence. This is a synthetic feature proxy.
    idt = {c.candidate_id: (c.frequency * c.consistency * c.generality *
                            c.transfer_calibration * c.reasoning_value) for c in cards}
    freq = {c.candidate_id: c.frequency for c in cards}
    reuse = {c.candidate_id: c.reuse_probability for c in cards}
    compression = {c.candidate_id: c.compression_gain for c in cards}
    rng = random.Random(seed)
    random_scores = {cid: rng.random() for cid in sorted(c.candidate_id for c in cards)}
    return {
        "R1_IDT": _stable_rank(cards, idt),
        "R2_FREQUENCY": _stable_rank(cards, freq),
        "R3_REUSE": _stable_rank(cards, reuse),
        "R4_COMPRESSION": _stable_rank(cards, compression),
        "R5_RANDOM": _stable_rank(cards, random_scores),
    }


def oracle_rank(cards: Sequence[CandidateCard], truth: Mapping[str, float]) -> list[str]:
    """Analysis-only upper bound; must only be called post-ranking/outcome lock."""
    if set(truth) != {c.candidate_id for c in cards}:
        raise ValueError("oracle truth must cover exactly the candidate pool")
    return [c.candidate_id for c in sorted(cards, key=lambda c: (-truth[c.candidate_id], c.candidate_id))]


def topk_rdr(a: Sequence[str], b: Sequence[str], k: int) -> float:
    """Top-K ranking divergence rate = 1 - |TopK(a)∩TopK(b)|/K."""
    if k <= 0 or len(a) < k or len(b) < k:
        raise ValueError("rankings must contain at least positive K unique candidates")
    aa, bb = set(a[:k]), set(b[:k])
    return 1.0 - len(aa & bb) / k


def kendall_divergence(a: Sequence[str], b: Sequence[str]) -> float:
    """Fraction of candidate pairs ordered oppositely (normalized Kendall distance)."""
    if set(a) != set(b) or len(a) != len(set(a)):
        raise ValueError("rankings must be permutations of the same unique pool")
    pos = {x: i for i, x in enumerate(b)}
    vals = [pos[x] for x in a]
    discordant = sum(vals[i] > vals[j] for i in range(len(vals)) for j in range(i + 1, len(vals)))
    n = len(vals)
    return discordant / (n * (n - 1) / 2)


def evaluate_topk(rankings: Mapping[str, Sequence[str]], truth: Mapping[str, float], k: int) -> dict[str, float]:
    """Simple contract endpoint: mean synthetic future value per selected slot."""
    return {name: sum(truth[cid] for cid in order[:k]) / k for name, order in rankings.items()}


def pressure_metrics(rankings: Mapping[str, Sequence[str]], k: int) -> dict[str, float]:
    """Pre-outcome pressure diagnostics; no truth parameter by design."""
    names = ["R1_IDT", "R2_FREQUENCY", "R3_REUSE", "R4_COMPRESSION", "R5_RANDOM"]
    pair_top = [topk_rdr(rankings[a], rankings[b], k)
                for i, a in enumerate(names) for b in names[i + 1:]]
    idt_pair = {name: topk_rdr(rankings["R1_IDT"], rankings[name], k)
                for name in names[1:]}
    pair_full = [kendall_divergence(rankings[a], rankings[b])
                 for i, a in enumerate(names) for b in names[i + 1:]]
    return {
        "mean_pairwise_topk_rdr": sum(pair_top) / len(pair_top),
        "mean_pairwise_kendall_divergence": sum(pair_full) / len(pair_full),
        **{f"R1_vs_{name}_topk_rdr": value for name, value in idt_pair.items()},
    }


def pressure_gate(metrics: Mapping[str, float]) -> bool:
    """Frozen fixture gate; outcome-blind. Random has a less rigid minimum."""
    serious = ("R1_vs_R2_FREQUENCY_topk_rdr", "R1_vs_R3_REUSE_topk_rdr",
               "R1_vs_R4_COMPRESSION_topk_rdr")
    return (all(metrics[x] >= .25 for x in serious)
            and metrics["R1_vs_R5_RANDOM_topk_rdr"] >= .125
            and metrics["mean_pairwise_topk_rdr"] >= .30
            and metrics["mean_pairwise_kendall_divergence"] >= .15)


def run_pressure_fixtures(n: int = 100, k: int = 8) -> dict:
    panel_rows = []
    for seed in range(n):
        cards, _, _ = make_panel(seed=seed)
        ranks = rank_all(cards, seed=seed + 7919)
        m = pressure_metrics(ranks, k)
        panel_rows.append({"seed": seed, "pass": pressure_gate(m), **m})
    keys = [k for k in panel_rows[0] if k not in ("seed", "pass")]
    means = {key: sum(row[key] for row in panel_rows) / n for key in keys}
    mins = {key: min(row[key] for row in panel_rows) for key in keys}
    return {"fixture_only": True, "panels": n, "N": 40, "K": k,
            "pass_count": sum(bool(r["pass"]) for r in panel_rows),
            "all_pass": all(r["pass"] for r in panel_rows),
            "mean_metrics": means, "minimum_metrics": mins,
            "panel_results": panel_rows}
