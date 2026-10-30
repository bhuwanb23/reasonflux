"""Benchmark runner (Phase 11E-4)."""

from __future__ import annotations

import uuid

from evaluation.harness.baselines import apply_ablation, apply_baseline
from evaluation.harness.config import HarnessConfig
from evaluation.harness.evidence import gate_run, map_claims
from evaluation.harness.layers import (
    build_snapshot,
    evaluate_capability_layer,
    evaluate_intelligence_layer,
    evaluate_invariant_layer,
    evaluate_skill_layer,
    evaluate_transfer_layer,
)
from evaluation.harness.maturity import classify_evaluation_maturity
from evaluation.harness.models import EvaluationRun, LayerResult
from evaluation.harness.scenarios import build_scenario
from evaluation.harness.stats import summarize


def _success_from_layers(layers: list[LayerResult], level: str) -> bool:
    by = {lr.layer: lr for lr in layers}
    order = ["invariant", "skill", "transfer", "capability", "intelligence"]
    # Require all layers up to requested level.
    target_idx = {
        "skill": 1,
        "transfer": 2,
        "capability": 3,
        "intelligence": 4,
        "arc": 4,
    }.get(str(level).lower(), 3)
    for name in order[: target_idx + 1]:
        lr = by.get(name)
        if lr is None or not lr.passed:
            return False
    return True


def run_benchmark(
    level: str = "capability",
    *,
    baseline: str | None = None,
    ablation: str | None = None,
    config: HarnessConfig | None = None,
    run_id: str | None = None,
) -> EvaluationRun:
    """Run a longitudinal synthetic benchmark and evaluate all layers."""
    cfg = config or HarnessConfig()
    steps = build_scenario(level if level != "intelligence" else "capability")
    if str(level).lower() == "arc":
        steps = build_scenario("arc")
    steps = apply_baseline(steps, baseline)
    steps = apply_ablation(steps, ablation)

    run = EvaluationRun(
        run_id=run_id or str(uuid.uuid4())[:8],
        level=str(level),
        baseline=baseline,
        ablation=ablation,
    )

    prev_score: float | None = None
    prev_ig: float | None = None
    prev_cgr: float | None = None
    experiences = cfg.experiences_per_step

    for i, step in enumerate(steps):
        exp = experiences * (i + 1)
        snap = build_snapshot(
            i,
            step.capabilities,
            step.skills,
            previous_score=prev_score,
            previous_ig=prev_ig,
            experiences=exp,
            config=cfg,
        )
        run.snapshots.append(snap)
        prev_cgr = snap.cgr
        prev_score = snap.capability_score
        prev_ig = snap.ig

    # Evaluate layers on final step (with history-aware capability/intel).
    final = steps[-1]
    prev_score_for_layers = (
        run.snapshots[-2].capability_score if len(run.snapshots) >= 2 else None
    )
    prev_ig_for_layers = run.snapshots[-2].ig if len(run.snapshots) >= 2 else None
    prev_cgr_for_layers = run.snapshots[-2].cgr if len(run.snapshots) >= 2 else None

    layers = [
        evaluate_invariant_layer(final.skills, cfg),
        evaluate_skill_layer(final.skills, cfg),
        evaluate_transfer_layer(final.skills, cfg),
        evaluate_capability_layer(
            final.capabilities,
            final.skills,
            previous_score=prev_score_for_layers,
            previous_cgr=prev_cgr_for_layers,
            config=cfg,
        ),
        evaluate_intelligence_layer(
            final.capabilities,
            final.skills,
            previous_ig=prev_ig_for_layers,
            previous_score=prev_score_for_layers,
            experiences=experiences * len(steps),
            config=cfg,
        ),
    ]
    run.layers = layers
    run.maturity = classify_evaluation_maturity(layers)
    run.claims = map_claims(run)

    # Stats over longitudinal series
    run.stats = {
        "cgr": summarize([s.cgr for s in run.snapshots], z=cfg.ci_z),
        "igr": summarize([s.igr for s in run.snapshots], z=cfg.ci_z),
        "capability_score": summarize(
            [s.capability_score for s in run.snapshots], z=cfg.ci_z
        ),
        "ig": summarize([s.ig for s in run.snapshots], z=cfg.ci_z),
    }

    ok_gate, kinds = gate_run(run)
    layer_ok = _success_from_layers(layers, level)
    # Flat baseline expected to fail growth success
    if baseline and str(baseline).upper() == "A":
        run.success = False
    else:
        run.success = layer_ok and ok_gate
    run.metadata["gate_ok"] = ok_gate
    run.metadata["gate_failures"] = kinds
    run.metadata["n_steps"] = len(steps)
    return run
