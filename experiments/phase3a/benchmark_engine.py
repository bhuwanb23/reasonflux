"""Phase 3A implementation-readiness engine.

This is a development/plumbing implementation of the Phase 1C contracts. It
accepts only public candidate cards and calibration-only transfer evidence;
future outcomes are handled by a separate post-lock vault API. It is not a
production data source or an IDT efficacy experiment.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
import hashlib
import math
import random
import re
from typing import Mapping, Sequence

from core.invariant import Invariant
from invariants.transfer_aware import rank_transfer_aware
from invariants.validation import ValidationConfig
from transfer.memory import TransferMemory
from transfer.metrics import TransferConfig, compute_transfer_score

POLICIES = ("R1_IDT", "R2_FREQUENCY", "R3_REUSE", "R4_COMPRESSION", "R5_RANDOM")
CARD_FIELDS = frozenset({
    "candidate_id", "frequency", "consistency", "generality",
    "transfer_calibration", "reasoning_value", "reuse_probability",
    "compression_gain",
})
ID_RE = re.compile(r"^[A-Z]{3,8}-[0-9a-f]{12,64}$")
FREQ_NORM = 10**12


@dataclass(frozen=True, slots=True)
class CandidateCard:
    """Allowlisted public candidate features; no labels, task IDs, or outcomes."""
    candidate_id: str
    frequency: float
    consistency: float
    generality: float
    transfer_calibration: float | None
    reasoning_value: float
    reuse_probability: float | None
    compression_gain: float | None

    def __post_init__(self) -> None:
        if not ID_RE.fullmatch(self.candidate_id):
            raise ValueError("candidate_id must be an opaque hash ID")
        for name in CARD_FIELDS - {"candidate_id"}:
            value = getattr(self, name)
            if value is None:
                continue
            if not math.isfinite(float(value)) or not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be finite and in [0,1], or unavailable")


@dataclass(frozen=True, slots=True)
class ReuseEvidence:
    successes: int
    eligible_attempts: int

    def probability(self) -> float:
        if self.eligible_attempts <= 0:
            raise ValueError("reuse probability unavailable: no eligible attempts")
        if self.successes < 0 or self.successes > self.eligible_attempts:
            raise ValueError("reuse successes must be between zero and eligible attempts")
        # Frozen unsmoothed empirical proportion; zero denominator is unavailable.
        return self.successes / self.eligible_attempts


def compression_gain(bits_before: float, bits_after: float) -> float:
    """Calibration-only bits-saved ratio; codec and corpus must be frozen upstream."""
    if not math.isfinite(bits_before) or not math.isfinite(bits_after) or bits_before <= 0:
        raise ValueError("bits_before must be positive and both bit counts finite")
    if bits_after < 0 or bits_after > bits_before:
        raise ValueError("bits_after must be in [0,bits_before]")
    return (bits_before - bits_after) / bits_before


def derive_seed(master_seed: int, panel_id: str, purpose: str) -> int:
    material = f"ASFT-3A-v1|{master_seed}|{panel_id}|{purpose}".encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big")


def randomized_arrival(cards: Sequence[CandidateCard], master_seed: int, panel_id: str) -> tuple[CandidateCard, ...]:
    result = sorted(cards, key=lambda c: c.candidate_id)
    random.Random(derive_seed(master_seed, panel_id, "arrival")).shuffle(result)
    return tuple(result)


def validate_pool(cards: Sequence[CandidateCard], *, master_seed: int, panel_id: str,
                  expected_n: int = 40, k: int = 8) -> None:
    if len(cards) != expected_n:
        raise ValueError(f"candidate pool has {len(cards)} rows; expected N={expected_n}")
    ids = [c.candidate_id for c in cards]
    if len(ids) != len(set(ids)):
        raise ValueError("candidate IDs must be unique")
    if not 1 <= k <= expected_n:
        raise ValueError("K must be in [1,N]")
    expected = [c.candidate_id for c in randomized_arrival(cards, master_seed, panel_id)]
    if ids != expected:
        raise ValueError("arrival order is not the frozen deterministic randomized permutation")


def _to_invariant(card: CandidateCard) -> Invariant:
    # Map normalized public F to the production ranker's normalized count with
    # negligible quantization; no family, label, or outcome fields are copied.
    return Invariant(
        invariant_id=card.candidate_id,
        pattern_signature=[],
        frequency=round(card.frequency * FREQ_NORM),
        consistency=card.consistency,
        generality=card.generality,
        metadata={"reasoning_value": card.reasoning_value},
    )


def _validate_rankings(rankings: Mapping[str, Sequence[str]], expected_ids: set[str]) -> None:
    for name in POLICIES:
        if name not in rankings:
            raise ValueError(f"missing policy {name}")
        order = list(rankings[name])
        if len(order) != len(expected_ids) or len(set(order)) != len(order) or set(order) != expected_ids:
            raise ValueError(f"{name} is not a complete permutation of the common pool")


def rank_all(cards: Sequence[CandidateCard], *, panel_id: str, master_seed: int,
             calibration_memory: TransferMemory, total_families: int,
             transfer_config: TransferConfig | None = None) -> dict[str, list[str]]:
    """Execute R1–R5 on one identical pool; no outcome or hidden-label argument."""
    if not cards or len({c.candidate_id for c in cards}) != len(cards):
        raise ValueError("cards must be nonempty with unique IDs")
    if total_families < 1:
        raise ValueError("total_families must be >= 1")
    transfer_config = transfer_config or TransferConfig()
    invariants = [_to_invariant(c) for c in cards]
    observed_t = {
        c.candidate_id: compute_transfer_score(
            calibration_memory, c.candidate_id, transfer_config,
            total_families=total_families,
        ).weighted for c in cards
    }
    for c in cards:
        if c.transfer_calibration is None:
            raise ValueError("R1 unavailable: transfer calibration missing")
        if not math.isclose(c.transfer_calibration, observed_t[c.candidate_id], rel_tol=1e-8, abs_tol=1e-10):
            raise ValueError(f"R1 calibration card/memory mismatch for {c.candidate_id}")
    # Execute the production transfer-aware bridge and its production ranking
    # implementation. The only transfer evidence supplied is the calibration-
    # only TransferMemory passed above.
    config = ValidationConfig(freq_norm=float(FREQ_NORM), transfer_norm=1.0)
    r1_rows = rank_transfer_aware(
        invariants, calibration_memory, config=transfer_config,
        validation_config=config, total_families=total_families,
    )
    r1 = [row.invariant.invariant_id for row in r1_rows]

    def feature_rank(name: str, getter) -> list[str]:
        vals = [(c.candidate_id, getter(c)) for c in cards]
        if any(v is None for _, v in vals):
            raise ValueError(f"{name} unavailable: feature missing for one or more candidates")
        return [cid for cid, _ in sorted(vals, key=lambda x: (-float(x[1]), x[0]))]

    # Stable per-panel random priorities are keyed by ID; arrival order is irrelevant.
    random_order = [c.candidate_id for c in sorted(
        cards,
        key=lambda c: (hashlib.sha256(
            f"{derive_seed(master_seed, panel_id, 'R5')}|{c.candidate_id}".encode()
        ).digest(), c.candidate_id),
    )]
    rankings = {
        "R1_IDT": r1,
        "R2_FREQUENCY": feature_rank("R2", lambda c: c.frequency),
        "R3_REUSE": feature_rank("R3", lambda c: c.reuse_probability),
        "R4_COMPRESSION": feature_rank("R4", lambda c: c.compression_gain),
        "R5_RANDOM": random_order,
    }
    _validate_rankings(rankings, {c.candidate_id for c in cards})
    return rankings


def _permutation(a: Sequence[str], b: Sequence[str]) -> None:
    if len(a) != len(b) or len(set(a)) != len(a) or len(set(b)) != len(b) or set(a) != set(b):
        raise ValueError("rankings must be permutations of the same unique pool")


def topk_rdr(a: Sequence[str], b: Sequence[str], k: int) -> float:
    _permutation(a, b)
    if k <= 0 or k > len(a):
        raise ValueError("K must be in [1,N]")
    return 1.0 - len(set(a[:k]) & set(b[:k])) / k


def topk_overlap(a: Sequence[str], b: Sequence[str], k: int) -> float:
    return 1.0 - topk_rdr(a, b, k)


def normalized_kendall_divergence(a: Sequence[str], b: Sequence[str]) -> float:
    _permutation(a, b)
    n = len(a)
    if n < 2:
        raise ValueError("Kendall divergence requires N>=2")
    pos = {x: i for i, x in enumerate(b)}
    ordered = [pos[x] for x in a]
    discordant = sum(ordered[i] > ordered[j] for i in range(n) for j in range(i + 1, n))
    return discordant / (n * (n - 1) / 2)


def normalized_pairwise_rank_divergence(a: Sequence[str], b: Sequence[str]) -> float:
    """Normalized Spearman footrule: mean absolute rank displacement, [0,1]."""
    _permutation(a, b)
    n = len(a)
    if n < 2:
        raise ValueError("rank divergence requires N>=2")
    pa, pb = ({x: i for i, x in enumerate(order)} for order in (a, b))
    max_footrule = (n * n) // 2
    return sum(abs(pa[x] - pb[x]) for x in pa) / max_footrule


def pressure_metrics(rankings: Mapping[str, Sequence[str]], k: int) -> dict[str, float]:
    _validate_rankings(rankings, set(rankings.get("R1_IDT", ())))
    pairs = [(a, b) for i, a in enumerate(POLICIES) for b in POLICIES[i + 1:]]
    rdr = {(a, b): topk_rdr(rankings[a], rankings[b], k) for a, b in pairs}
    kendall = {(a, b): normalized_kendall_divergence(rankings[a], rankings[b]) for a, b in pairs}
    rankdiv = {(a, b): normalized_pairwise_rank_divergence(rankings[a], rankings[b]) for a, b in pairs}
    result: dict[str, float] = {
        "mean_pairwise_topk_rdr": sum(rdr.values()) / len(rdr),
        "mean_pairwise_kendall_divergence": sum(kendall.values()) / len(kendall),
        "mean_pairwise_rank_divergence": sum(rankdiv.values()) / len(rankdiv),
    }
    for other in POLICIES[1:]:
        result[f"R1_vs_{other}_topk_rdr"] = rdr[("R1_IDT", other)]
        result[f"R1_vs_{other}_topk_overlap"] = 1.0 - rdr[("R1_IDT", other)]
        result[f"R1_vs_{other}_kendall_divergence"] = kendall[("R1_IDT", other)]
        result[f"R1_vs_{other}_rank_divergence"] = rankdiv[("R1_IDT", other)]
    return result


PRESSURE_THRESHOLDS = {
    "R1_vs_R2_FREQUENCY_topk_rdr": 0.25,
    "R1_vs_R3_REUSE_topk_rdr": 0.25,
    "R1_vs_R4_COMPRESSION_topk_rdr": 0.25,
    "R1_vs_R5_RANDOM_topk_rdr": 0.125,
    "mean_pairwise_topk_rdr": 0.30,
    "mean_pairwise_kendall_divergence": 0.15,
}


def pressure_gate(metrics: Mapping[str, float]) -> bool:
    return all(metrics.get(key, -math.inf) >= threshold
               for key, threshold in PRESSURE_THRESHOLDS.items())


@dataclass(frozen=True, slots=True)
class OutcomeRow:
    policy: str
    task_id: str
    utility: float | None
    no_candidate_utility: float | None
    portfolio_cost: float


@dataclass(frozen=True, slots=True)
class FNTUConfig:
    k: int
    h: int
    lambda_cost: float | None
    cost_model_sha256: str | None
    frozen: bool


def fntu_suite(rows_by_policy: Mapping[str, Sequence[OutcomeRow]],
               selected_ids: Mapping[str, Sequence[str]], candidate_ids: set[str],
               config: FNTUConfig) -> dict[str, float]:
    """Independent FNTU@K arithmetic; unavailable if model, pairing, or rows fail."""
    if (not config.frozen or config.lambda_cost is None or
            not config.cost_model_sha256 or
            not re.fullmatch(r"sha256:[0-9a-f]{64}", config.cost_model_sha256)):
        raise ValueError("FNTU unavailable: frozen hashed cost model/lambda absent")
    if (config.k <= 0 or config.h <= 0 or
            not math.isfinite(config.lambda_cost) or config.lambda_cost < 0):
        raise ValueError("invalid K, H, or lambda")
    if set(rows_by_policy) != set(POLICIES):
        raise ValueError("FNTU requires R1-R5 rows; Oracle is not a policy comparator")
    task_sets = {p: {r.task_id for r in rows_by_policy[p]} for p in POLICIES}
    if any(len(rows_by_policy[p]) != config.h or len(task_sets[p]) != config.h for p in POLICIES):
        raise ValueError("FNTU requires exactly H unique paired task rows per policy")
    common_tasks = next(iter(task_sets.values()))
    if any(s != common_tasks for s in task_sets.values()):
        raise ValueError("policies must use the exact same task horizon")
    for p in POLICIES:
        chosen = list(selected_ids[p])
        if len(chosen) != config.k or len(set(chosen)) != config.k or not set(chosen) <= candidate_ids:
            raise ValueError(f"{p} must select exactly K unique cards from the shared pool")
    if set(selected_ids) != set(POLICIES):
        raise ValueError("selection lists must cover R1-R5 exactly")
    if any(r.policy != p for p in POLICIES for r in rows_by_policy[p]):
        raise ValueError("outcome row policy key does not match its policy field")
    by_task = {p: {r.task_id: r for r in rows_by_policy[p]} for p in POLICIES}
    # No missingness is silently imputed. Phase 1C supplies a >5% gate but not
    # an explicit below-threshold estimator; this engine fails closed pending freeze.
    if any(r.utility is None or r.no_candidate_utility is None
           for p in POLICIES for r in rows_by_policy[p]):
        raise ValueError("FNTU unavailable: missing-outcome aggregation rule not frozen")
    if any(not math.isfinite(float(value)) for p in POLICIES for r in rows_by_policy[p]
           for value in (r.utility, r.no_candidate_utility)):
        raise ValueError("task utility and paired baseline must be finite")
    baseline_by_task = {
        tid: {by_task[p][tid].no_candidate_utility for p in POLICIES} for tid in common_tasks
    }
    if any(len(v) != 1 for v in baseline_by_task.values()):
        raise ValueError("paired no-candidate baseline differs across policies")
    out = {}
    for p in POLICIES:
        rows = rows_by_policy[p]
        costs = {r.portfolio_cost for r in rows}
        if len(costs) != 1 or not all(math.isfinite(r.portfolio_cost) and r.portfolio_cost >= 0 for r in rows):
            raise ValueError("portfolio cost must be finite and fixed across the paired horizon")
        gross_delta = sum(float(r.utility) - float(r.no_candidate_utility) for r in rows)
        cost = next(iter(costs))
        out[p] = (gross_delta - config.lambda_cost * cost) / (config.k * config.h)
    return out


def compare_fntu(scores: Mapping[str, float]) -> dict[str, float]:
    return {f"R1_minus_{p}": scores["R1_IDT"] - scores[p] for p in POLICIES[1:]}


def rankings_digest(rankings: Mapping[str, Sequence[str]]) -> str:
    text = "\n".join(f"{p}:" + ",".join(rankings[p]) for p in POLICIES)
    return hashlib.sha256(text.encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class PreOutcomeLock:
    rankings_sha256: str
    pool_sha256: str
    pressure_sha256: str


class OracleAccess:
    __slots__ = ("_outcomes", "_lock_hash")
    def __init__(self, outcomes: Mapping[str, float], lock_hash: str):
        self._outcomes = dict(outcomes)
        self._lock_hash = lock_hash


class OutcomeVault:
    """In-process protocol mock only; not a production security boundary."""
    __slots__ = ("_outcomes", "_sealed", "_commitment")
    def __init__(self, outcomes: Mapping[str, float], *, expected_commitment: str):
        self._outcomes = dict(outcomes)
        self._commitment = hashlib.sha256("\n".join(
            f"{k}:{self._outcomes[k]:.17g}" for k in sorted(self._outcomes)
        ).encode()).hexdigest()
        if self._commitment != expected_commitment:
            raise ValueError("outcome commitment mismatch")
        self._sealed = True

    @staticmethod
    def commitment(outcomes: Mapping[str, float]) -> str:
        return hashlib.sha256("\n".join(f"{k}:{outcomes[k]:.17g}" for k in sorted(outcomes)).encode()).hexdigest()

    def open_after_lock(self, lock: PreOutcomeLock, rankings: Mapping[str, Sequence[str]],
                        pressure: Mapping[str, float]) -> OracleAccess:
        if not self._sealed:
            raise ValueError("outcome vault is not sealed")
        if rankings_digest(rankings) != lock.rankings_sha256:
            raise ValueError("rankings differ from pre-outcome lock")
        if hashlib.sha256(repr(sorted(pressure.items())).encode()).hexdigest() != lock.pressure_sha256:
            raise ValueError("pressure log differs from pre-outcome lock")
        return OracleAccess(self._outcomes, lock.rankings_sha256)


def make_preoutcome_lock(rankings: Mapping[str, Sequence[str]], pool_ids: Sequence[str],
                         pressure: Mapping[str, float]) -> PreOutcomeLock:
    return PreOutcomeLock(
        rankings_sha256=rankings_digest(rankings),
        pool_sha256=hashlib.sha256("\n".join(sorted(pool_ids)).encode()).hexdigest(),
        pressure_sha256=hashlib.sha256(repr(sorted(pressure.items())).encode()).hexdigest(),
    )


def oracle_rank(access: OracleAccess, lock: PreOutcomeLock, pool_ids: Sequence[str]) -> list[str]:
    if access._lock_hash != lock.rankings_sha256:
        raise ValueError("Oracle access does not match this lock")
    if set(access._outcomes) != set(pool_ids):
        raise ValueError("oracle outcomes must cover exactly the locked candidate pool")
    return sorted(pool_ids, key=lambda cid: (-access._outcomes[cid], cid))


def card_schema() -> tuple[str, ...]:
    return tuple(f.name for f in fields(CandidateCard))
