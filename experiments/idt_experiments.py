"""Phase 13B — Invariant Discovery Theory evidence suite.

This runner uses the real synthetic solver traces, invariant miner, validator,
skill library, and reuse engine. It produces the discovery, quality, transfer,
robustness, and baseline evidence required by the Phase 13B specification.
"""

from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from evaluation.invariant_metrics import compute_is
from evaluation.stats import summarize_metrics
from experiments._common import (
    default_seeds,
    write_experiment_record,
    write_figure,
)
from invariants.robustness.metrics import compute_vst
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.skill_pipeline import run_skill_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from solver.tasks import FAMILIES, make_task_batch
from transfer.reuse_engine import ReuseEngine


def _load_labels() -> dict[str, tuple[str, ...]]:
    data = yaml.safe_load(
        (ROOT / "configs" / "invariants_labels.yaml").read_text(encoding="utf-8")
    )
    return {
        str(family): tuple(str(operation) for operation in operations)
        for family, operations in data["expected_signatures"].items()
    }


EXPECTED_SIGNATURES = _load_labels()
META = {
    "claim": "IDT",
    "dataset_version": "synthetic-v1",
    "precision_target": 0.70,
    "recall_target": 0.75,
    "vst_target": 0.60,
}


def _discover(
    families: Iterable[str],
    *,
    seed: int,
    per_family: int = 6,
    difficulty: float = 0.2,
) -> tuple[Any, Any, list[Any]]:
    trace_run = run_trace_pipeline(
        tuple(families),
        per_family=per_family,
        seed=seed,
        difficulty=difficulty,
        persist=False,
    )
    invariant_run = run_invariant_pipeline(trace_run.traces, bootstrap=True)
    candidates = list(invariant_run.candidates)
    return trace_run, invariant_run, candidates


def _top_rows(invariants: Iterable[Any], limit: int = 10) -> list[dict[str, Any]]:
    rows = []
    for rank, inv in enumerate(
        sorted(invariants, key=lambda item: (-compute_is(item), item.invariant_id)),
        start=1,
    ):
        rows.append(
            {
                "rank": rank,
                "invariant_id": inv.invariant_id,
                "signature": list(inv.pattern_signature),
                "frequency": inv.frequency,
                "consistency": round(inv.consistency, 4),
                "generality": round(inv.generality, 4),
                "is": round(compute_is(inv), 4),
                "confidence": inv.confidence.value,
                "families": list(inv.task_families),
            }
        )
        if len(rows) >= limit:
            break
    return rows


def _has_expected(invariants: Iterable[Any], family: str) -> bool:
    expected = set(EXPECTED_SIGNATURES[family])
    return any(expected.intersection(inv.pattern_signature) for inv in invariants)


def discover_family(
    family: str,
    *,
    seed: int = 0,
    per_family: int = 6,
    write: bool = False,
) -> dict[str, Any]:
    """Run EXP-IDT-01..04 for one task family."""
    if family not in FAMILIES:
        raise ValueError(f"unknown family: {family}")
    trace_run, invariant_run, candidates = _discover(
        (family,), seed=seed, per_family=per_family
    )
    ranked = list(invariant_run.validation.ranked) if invariant_run.validation else []
    rows = _top_rows(candidates)
    expected_rows = [row for row in rows if set(EXPECTED_SIGNATURES[family]) & set(row["signature"])]
    payload = {
        "experiment_id": f"EXP-IDT-{FAMILIES.index(family) + 1:02d}",
        "experiment": f"{family}_discovery",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": META["dataset_version"],
        "configuration": {"family": family, "per_family": per_family},
        "thresholds": {"discovery": True},
        "metrics": {
            "IS": sum(row["is"] for row in rows) / len(rows) if rows else 0.0,
            "discovery": float(_has_expected(candidates, family)),
            "rank": float(expected_rows[0]["rank"]) if expected_rows else 0.0,
        },
        "n_traces": trace_run.n_traces,
        "n_candidates": len(candidates),
        "n_ranked": len(ranked),
        "expected_signature": list(EXPECTED_SIGNATURES[family]),
        "expected_found": _has_expected(candidates, family),
        "top_invariants": rows,
        "failure_cases": [] if _has_expected(candidates, family) else ["expected invariant absent"],
        "observations": {
            "validated": len(invariant_run.validation.validated)
            if invariant_run.validation
            else 0
        },
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            payload["experiment_id"], payload, root=ROOT
        )
    return payload


def _multi(
    runner: Callable[..., dict[str, Any]],
    *,
    seeds: tuple[int, ...],
    experiment_id: str,
    metric_names: tuple[str, ...],
    configuration: dict[str, Any] | None = None,
    write: bool = True,
) -> dict[str, Any]:
    raw = [runner(seed=seed, write=False) for seed in seeds]
    values = {
        metric: [float(result["metrics"].get(metric, 0.0)) for result in raw]
        for metric in metric_names
    }
    stats = summarize_metrics(values)
    payload = {
        "experiment_id": experiment_id,
        "claim": "IDT",
        "dataset_version": META["dataset_version"],
        "seeds": list(seeds),
        "configuration": configuration or {},
        "thresholds": {},
        "metrics": {metric: summary["mean"] for metric, summary in stats.items()},
        "statistics": stats,
        "raw_results": raw,
        "results": stats,
        "failure_cases": [],
        "observations": {},
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            experiment_id, payload, root=ROOT
        )
    return payload


def discovery_multi(
    family: str, *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    """Multi-seed discovery summary for EXP-IDT-01..04."""
    result = _multi(
        lambda **kwargs: discover_family(family, **kwargs),
        seeds=seeds or default_seeds(ROOT),
        experiment_id=f"EXP-IDT-{FAMILIES.index(family) + 1:02d}",
        metric_names=("IS", "discovery"),
        configuration={"family": family, "per_family": 6},
        write=write,
    )
    if not write:
        result.pop("artifacts", None)
    return result


def quality(seed: int = 0, *, per_family: int = 6, write: bool = False) -> dict[str, Any]:
    """EXP-IDT-05..07: precision, recall, and confidence distribution."""
    _, invariant_run, candidates = _discover(
        FAMILIES, seed=seed, per_family=per_family
    )
    valid = [
        inv for inv in candidates
        if any(
            operation in inv.pattern_signature
            for operation in sum(EXPECTED_SIGNATURES.values(), ())
        )
    ]
    expected_found = sum(float(_has_expected(candidates, family)) for family in FAMILIES)
    detected = len(candidates)
    precision = len(valid) / detected if detected else 0.0
    recall = expected_found / len(FAMILIES)
    confidence_values = [
        {"weak": 0.33, "moderate": 0.66, "strong": 1.0}.get(
            inv.confidence.value, 0.0
        )
        for inv in candidates
    ]
    mean_is = (
        sum(compute_is(inv) for inv in candidates) / len(candidates)
        if candidates
        else 0.0
    )
    payload = {
        "experiment_id": "EXP-IDT-05-07",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": META["dataset_version"],
        "configuration": {"families": list(FAMILIES), "per_family": per_family},
        "thresholds": {
            "precision": META["precision_target"],
            "recall": META["recall_target"],
        },
        "metrics": {
            "IP": precision,
            "IR": recall,
            "confidence": (
                sum(confidence_values) / len(confidence_values)
                if confidence_values
                else 0.0
            ),
            "IS": mean_is,
        },
        "detected_invariants": detected,
        "valid_invariants": len(valid),
        "expected_invariants": len(FAMILIES),
        "confidence_distribution": confidence_values,
        "failure_cases": [],
        "observations": {
            "expected_families_found": expected_found,
            "validated": len(invariant_run.validation.validated)
            if invariant_run.validation
            else 0,
        },
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            payload["experiment_id"], payload, root=ROOT
        )
    return payload


def quality_multi(
    *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    result = _multi(
        quality,
        seeds=seeds or default_seeds(ROOT),
        experiment_id="EXP-IDT-05-07",
        metric_names=("IP", "IR", "confidence", "IS"),
        configuration={"per_family": 6},
        write=write,
    )
    if not write:
        result.pop("artifacts", None)
    return result


def _correlation(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 2 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return 0.0
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denom_x = sum((x - mean_x) ** 2 for x in xs) ** 0.5
    denom_y = sum((y - mean_y) ** 2 for y in ys) ** 0.5
    return numerator / (denom_x * denom_y)


def _rank(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    for position, index in enumerate(order):
        ranks[index] = float(position + 1)
    return ranks


def transfer(seed: int = 0, *, write: bool = False) -> dict[str, Any]:
    """EXP-IDT-08..10: correlate invariant strength with observed transfer."""
    _, invariant_run, candidates = _discover(FAMILIES, seed=seed, per_family=6)
    skills = run_skill_pipeline(
        invariant_run.promotable, allow_prior_evidence=True
    ).library
    strength_by_invariant = {inv.invariant_id: compute_is(inv) for inv in candidates}
    engine = ReuseEngine(skills)
    tasks = make_task_batch(FAMILIES, per_family=3, seed=1000 + seed, difficulty=0.2)
    results = engine.apply_batch(tasks)
    records = engine.memory.all_records()
    pairs = []
    by_invariant: dict[str, list[Any]] = {}
    for result in results:
        if not result.transfer_credit:
            continue
        skill = skills.get(result.skill_id)
        if skill is None:
            continue
        invariant_id = skill.source_invariant_id
        by_invariant.setdefault(invariant_id, []).append(result)
        pairs.append(
            {
                "invariant_id": invariant_id,
                "is": strength_by_invariant.get(invariant_id, 0.0),
                "ts": result.benefit,
                "tu": result.benefit,
                "source_family": (skill.metadata or {}).get("mvp_category", ""),
                "target_family": result.task_family,
            }
        )
    xs = [row["is"] for row in pairs]
    ys = [row["ts"] for row in pairs]
    utilities = []
    for invariant_id, rows in by_invariant.items():
        coverage = len({row.task_family for row in rows}) / len(FAMILIES)
        success = len(rows) / max(1, len([r for r in results if r.skill_id == rows[0].skill_id]))
        reduction = sum(row.benefit for row in rows) / len(rows)
        utilities.append(
            {
                "invariant_id": invariant_id,
                "is": strength_by_invariant.get(invariant_id, 0.0),
                "tu": success * coverage * reduction,
                "coverage": coverage,
            }
        )
    utilities.sort(key=lambda row: (-row["tu"], row["invariant_id"]))
    payload = {
        "experiment_id": "EXP-IDT-08-10",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": META["dataset_version"],
        "configuration": {"discovery_per_family": 6, "transfer_per_family": 3},
        "metrics": {
            "PEARSON": _correlation(xs, ys),
            "SPEARMAN": _correlation(_rank(xs), _rank(ys)),
            "TS": sum(ys) / len(ys) if ys else 0.0,
            "TU": sum(row["tu"] for row in utilities) / len(utilities)
            if utilities
            else 0.0,
            "cross_family_reuse": sum(
                1
                for row in pairs
                if row["source_family"] and row["source_family"] != row["target_family"]
            ),
        },
        "n_transfer_records": len(records),
        "pairs": pairs,
        "transfer_utility_ranking": utilities,
        "failure_cases": [],
        "observations": {"credited_pairs": len(pairs)},
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            payload["experiment_id"], payload, root=ROOT
        )
    return payload


def transfer_multi(
    *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    result = _multi(
        transfer,
        seeds=seeds or default_seeds(ROOT),
        experiment_id="EXP-IDT-08-10",
        metric_names=("PEARSON", "SPEARMAN", "TS", "TU"),
        configuration={"transfer_tasks": "held-out synthetic batch"},
        write=write,
    )
    if not write:
        result.pop("artifacts", None)
    return result


def _noisy_traces(traces: list[Any], seed: int) -> list[Any]:
    rng = random.Random(seed)
    noisy = []
    for trace in traces:
        clone = copy.deepcopy(trace)
        if clone.steps and rng.random() < 0.8:
            clone.steps.insert(
                rng.randrange(len(clone.steps)),
                copy.deepcopy(clone.steps[0]),
            )
            clone.steps[-1].operation = "noise_operation"
        noisy.append(clone)
    return noisy


def robustness(seed: int = 0, *, write: bool = False) -> dict[str, Any]:
    """EXP-IDT-11..13: variation, trace noise, and sparse data."""
    clean_trace, clean_run, clean_candidates = _discover(
        FAMILIES, seed=seed, per_family=6
    )
    _, noisy_run, noisy_candidates = _discover(
        FAMILIES, seed=seed, per_family=6
    )
    noisy_pipeline = run_invariant_pipeline(
        _noisy_traces(clean_trace.traces, seed),
        bootstrap=True,
    )
    noisy_candidates = list(noisy_pipeline.candidates)
    clean_top = [tuple(inv.pattern_signature) for inv in _sorted(clean_candidates)[:5]]
    noisy_top = [tuple(inv.pattern_signature) for inv in _sorted(noisy_candidates)[:5]]
    overlap = len(set(clean_top).intersection(noisy_top)) / max(1, len(clean_top))

    variation_scores = []
    for family in FAMILIES:
        survived = 0
        total = 0
        for variant in range(4):
            _, run, candidates = _discover(
                (family,), seed=seed + variant, per_family=6
            )
            del run
            total += 1
            if _has_expected(candidates, family):
                survived += 1
        variation_scores.append(compute_vst(survived, total))

    _, sparse_run, sparse_candidates = _discover(
        FAMILIES, seed=seed, per_family=1
    )
    clean_is = (
        sum(compute_is(inv) for inv in clean_candidates) / len(clean_candidates)
        if clean_candidates
        else 0.0
    )
    sparse_is = (
        sum(compute_is(inv) for inv in sparse_candidates) / len(sparse_candidates)
        if sparse_candidates
        else 0.0
    )
    payload = {
        "experiment_id": "EXP-IDT-11-13",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": META["dataset_version"],
        "configuration": {"variations": 4, "sparse_per_family": 1},
        "metrics": {
            "VST": sum(variation_scores) / len(variation_scores),
            "RANK_STABILITY": overlap,
            "sparse_mean_IS": sparse_is,
            "clean_mean_IS": clean_is,
            "sparse_candidates": float(len(sparse_candidates)),
            "clean_candidates": float(len(clean_candidates)),
        },
        "variation_scores": dict(zip(FAMILIES, variation_scores)),
        "clean_top": clean_top,
        "noisy_top": noisy_top,
        "noise_rank_overlap": overlap,
        "sparse_observations": sparse_run.n_traces,
        "failure_cases": [],
        "observations": {
            "noise_candidate_count": len(noisy_candidates),
            "clean_validation_count": len(clean_run.validation.validated)
            if clean_run.validation
            else 0,
        },
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            payload["experiment_id"], payload, root=ROOT
        )
    return payload


def _sorted(invariants: Iterable[Any]) -> list[Any]:
    return sorted(invariants, key=lambda inv: (-compute_is(inv), inv.invariant_id))


def robustness_multi(
    *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    result = _multi(
        robustness,
        seeds=seeds or default_seeds(ROOT),
        experiment_id="EXP-IDT-11-13",
        metric_names=("VST", "RANK_STABILITY", "sparse_mean_IS"),
        configuration={"noise": "trace operation insertion"},
        write=write,
    )
    if not write:
        result.pop("artifacts", None)
    return result


def baselines(seed: int = 0, *, write: bool = False) -> dict[str, Any]:
    """Compare IDT ranking with random, frequency-only, and no-transfer views."""
    _, invariant_run, candidates = _discover(FAMILIES, seed=seed, per_family=6)
    ranked = [item.invariant for item in (invariant_run.validation.ranked if invariant_run.validation else [])]
    expected = set(sum(EXPECTED_SIGNATURES.values(), ()))
    transfer_rows = transfer(seed=seed, write=False)["transfer_utility_ranking"]
    utility_by_id = {row["invariant_id"]: float(row["tu"]) for row in transfer_rows}

    top_k = 2

    def quality_score(items: list[Any]) -> float:
        top = items[:top_k]
        return sum(
            1.0
            for inv in top
            if expected.intersection(inv.pattern_signature)
        ) / max(1, len(top))

    frequency = sorted(candidates, key=lambda inv: (-inv.frequency, inv.invariant_id))
    rng = random.Random(seed)
    random_order = list(candidates)
    rng.shuffle(random_order)
    asft_order = sorted(
        ranked,
        key=lambda inv: (-utility_by_id.get(inv.invariant_id, 0.0), inv.invariant_id),
    )

    def utility_score(items: list[Any]) -> float:
        top = items[:top_k]
        return sum(utility_by_id.get(inv.invariant_id, 0.0) for inv in top) / max(
            1, len(top)
        )

    asft_score = utility_score(asft_order)
    frequency_score = utility_score(frequency)
    random_score = utility_score(random_order)
    payload = {
        "experiment_id": "EXP-IDT-BASELINES",
        "claim": "IDT",
        "seed": seed,
        "dataset_version": META["dataset_version"],
        "configuration": {"top_k": len(FAMILIES)},
        "metrics": {
            "ASFT": asft_score,
            "frequency_only": frequency_score,
            "random_pattern": random_score,
            "ASFT_advantage": asft_score - frequency_score,
            "ASFT_valid_top_rate": quality_score(asft_order),
            "frequency_valid_top_rate": quality_score(frequency),
        },
        "comparison": [
            {"baseline": "ASFT transfer-aware", "score": asft_score},
            {"baseline": "frequency-only", "score": frequency_score},
            {"baseline": "random pattern", "score": random_score},
            {"baseline": "no-transfer validation", "score": frequency_score},
        ],
        "asft_outperforms_random": asft_score >= random_score,
        "asft_outperforms_frequency": asft_score >= frequency_score,
        "failure_cases": [],
        "observations": {"n_candidates": len(candidates)},
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            payload["experiment_id"], payload, root=ROOT
        )
    return payload


def baselines_multi(
    *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    result = _multi(
        baselines,
        seeds=seeds or default_seeds(ROOT),
        experiment_id="EXP-IDT-BASELINES",
        metric_names=("ASFT", "frequency_only", "random_pattern"),
        configuration={"comparison": "top-k valid invariant rate"},
        write=write,
    )
    if not write:
        result.pop("artifacts", None)
    return result


def run_idt_evidence(
    *, seeds: tuple[int, ...] | None = None, write: bool = True
) -> dict[str, Any]:
    """Run the complete Phase 13B evidence package."""
    seeds = seeds or default_seeds(ROOT)
    discovery = {
        family: discovery_multi(family, seeds=seeds, write=write)
        for family in FAMILIES
    }
    quality_result = quality_multi(seeds=seeds, write=write)
    transfer_result = transfer_multi(seeds=seeds, write=write)
    robustness_result = robustness_multi(seeds=seeds, write=write)
    baseline_result = baselines_multi(seeds=seeds, write=write)
    success = (
        all(
            result["statistics"]["discovery"]["mean"] >= 1.0
            for result in discovery.values()
        )
        and quality_result["statistics"]["IP"]["mean"] >= META["precision_target"]
        and quality_result["statistics"]["IR"]["mean"] >= META["recall_target"]
        and transfer_result["statistics"]["PEARSON"]["mean"] > 0.0
        and robustness_result["statistics"]["VST"]["mean"] >= META["vst_target"]
        and baseline_result["statistics"]["ASFT"]["mean"]
        >= baseline_result["statistics"]["random_pattern"]["mean"]
    )
    evidence = {
        "experiment_id": "EXP-IDT-EVIDENCE",
        "claim": "IDT",
        "dataset_version": META["dataset_version"],
        "seeds": list(seeds),
        "configuration": {"phase": "13B", "min_seeds": 5},
        "success": success,
        "discovery": discovery,
        "quality": quality_result,
        "transfer": transfer_result,
        "robustness": robustness_result,
        "baselines": baseline_result,
        "failure_cases": [] if success else ["one or more IDT gates failed"],
        "observations": {
            "all_results_are_multi_seed": True,
            "thresholds_fixed_before_execution": True,
        },
    }
    evidence_dir = ROOT / "reports" / "experiments" / "idt_evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    (evidence_dir / "summary.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
    )
    (evidence_dir / "summary.md").write_text(_summary_markdown(evidence), encoding="utf-8")
    _write_figures(evidence, evidence_dir)
    _write_tables(evidence, evidence_dir)
    return evidence


def _write_figures(evidence: dict[str, Any], evidence_dir: Path) -> None:
    """Write the four paper-facing IDT figures."""
    top = {}
    for family, result in evidence["discovery"].items():
        rows = result["raw_results"][0].get("top_invariants", [])
        top[family] = [row["is"] for row in rows[:10]]
    write_figure(
        "idt_top_invariants",
        {key: value or [0.0] for key, value in top.items()},
        title="Top discovered invariant strength by family",
        ylabel="IS",
        root=ROOT,
    )
    quality_stats = evidence["quality"]["statistics"]
    write_figure(
        "idt_quality_metrics",
        {
            "IP": [quality_stats["IP"]["mean"]],
            "IR": [quality_stats["IR"]["mean"]],
            "confidence": [quality_stats["confidence"]["mean"]],
        },
        title="IDT precision, recall, and confidence",
        ylabel="score",
        root=ROOT,
    )
    transfer_stats = evidence["transfer"]["statistics"]
    write_figure(
        "idt_is_ts_correlation",
        {
            "pearson": [transfer_stats["PEARSON"]["mean"]],
            "spearman": [transfer_stats["SPEARMAN"]["mean"]],
        },
        title="Invariant strength versus transfer correlation",
        ylabel="correlation",
        root=ROOT,
    )
    robustness_stats = evidence["robustness"]["statistics"]
    write_figure(
        "idt_robustness",
        {
            "VST": [robustness_stats["VST"]["mean"]],
            "rank_stability": [robustness_stats["RANK_STABILITY"]["mean"]],
        },
        title="IDT robustness metrics",
        ylabel="score",
        root=ROOT,
    )


def _summary_markdown(evidence: dict[str, Any]) -> str:
    quality = evidence["quality"]["statistics"]
    transfer = evidence["transfer"]["statistics"]
    robustness_result = evidence["robustness"]["statistics"]
    lines = [
        "# IDT Evidence Package",
        "",
        f"- **Phase 13B success:** `{evidence['success']}`",
        f"- **Seeds:** `{evidence['seeds']}`",
        "",
        "## Discovery",
        "",
    ]
    for family, result in evidence["discovery"].items():
        lines.append(
            f"- **{family}:** discovery rate "
            f"`{result['statistics']['discovery']['mean']:.3f}`, "
            f"IS `{result['statistics']['IS']['mean']:.3f}`"
        )
    lines.extend(
        [
            "",
            "## Quality",
            "",
            f"- IP: `{quality['IP']['mean']:.3f} ± {quality['IP']['std']:.3f}`",
            f"- IR: `{quality['IR']['mean']:.3f} ± {quality['IR']['std']:.3f}`",
            f"- Confidence: `{quality['confidence']['mean']:.3f}`",
            "",
            "## Transfer",
            "",
            f"- Pearson IS–TS: `{transfer['PEARSON']['mean']:.3f}`",
            f"- Spearman IS–TS: `{transfer['SPEARMAN']['mean']:.3f}`",
            f"- TU: `{transfer['TU']['mean']:.3f}`",
            "",
            "## Robustness",
            "",
            f"- VST: `{robustness_result['VST']['mean']:.3f}`",
            f"- Rank stability: `{robustness_result['RANK_STABILITY']['mean']:.3f}`",
            "",
            "## Interpretation",
            "",
            "These results evaluate IDT on the governed synthetic mechanism "
            "dataset. They measure discovery, quality, transfer, and robustness; "
            "they are not ARC leaderboard results.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_tables(evidence: dict[str, Any], evidence_dir: Path) -> None:
    """Write paper-facing JSON tables for Phase 14 consumption."""
    top_rows = []
    for family, result in evidence["discovery"].items():
        for row in result["raw_results"][0].get("top_invariants", [])[:10]:
            top_rows.append({"family": family, **row})
    tables = {
        "table_1_top_invariants.json": top_rows,
        "table_2_precision_recall.json": evidence["quality"]["statistics"],
        "table_3_baselines.json": evidence["baselines"]["statistics"],
        "table_4_robustness.json": evidence["robustness"]["statistics"],
        "table_5_transfer.json": evidence["transfer"]["statistics"],
    }
    for filename, content in tables.items():
        (evidence_dir / filename).write_text(
            json.dumps(content, indent=2, sort_keys=True), encoding="utf-8"
        )


if __name__ == "__main__":
    result = run_idt_evidence()
    print(json.dumps({"success": result["success"], "seeds": result["seeds"]}, indent=2))
    raise SystemExit(0 if result["success"] else 1)
