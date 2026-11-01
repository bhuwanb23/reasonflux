"""Non-outcome contract tests for frozen Phase 13E protocol and metrics."""
from __future__ import annotations

from pathlib import Path

from capability import CapabilityLibrary, compute_system_capability_state
from evaluation.growth_metrics import compute_ig
from skills.library import SkillLibrary

from experiments.phase13e.common import build_round_tasks, growth_config_from_json, load_config
from experiments.phase13e.arms import ArmRuntime
from experiments.phase13e.metrics import summarize_round
from experiments.phase13e.robustness import run_isolated_robustness
from experiments.phase13e.statistics import build_analysis, summarize


def test_preregistered_seed_and_arm_contract():
    cfg = load_config()
    assert cfg["seeds"] == list(range(60, 70))
    assert cfg["arms"]["baselines"] == [
        "B1_NO_LEARNING", "B2_SKILL_STORAGE_ONLY", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY"
    ]
    assert len(cfg["arms"]["ablations"]) == 5
    assert cfg["growth_config"]["ig_formula"] == "evaluation.growth_metrics.compute_ig"
    assert cfg["statistics"]["independent_seed_count"] == 10


def test_round_streams_are_deterministic_and_unique():
    cfg = load_config()
    first = build_round_tasks(60, 2, cfg)
    again = build_round_tasks(60, 2, cfg)
    assert [t.task_id for t in first] == [t.task_id for t in again]
    assert len({t.task_id for t in first}) == len(first)
    assert all(t.metadata["compose"] for t in first if t.task_family == "reflection")
    assert not any(t.metadata["compose"] for t in first if t.task_family != "reflection")
    round_one = build_round_tasks(60, 0, cfg)
    round_two = build_round_tasks(60, 1, cfg)
    assert not any(t.metadata["symmetric"] for t in round_one if t.task_family in {"counting", "grouping"})
    assert any(t.metadata["symmetric"] for t in round_two if t.task_family in {"counting", "grouping"})


def test_primary_ig_path_uses_frozen_growth_config_weights():
    gc = growth_config_from_json(load_config())
    observed = compute_ig(0.2, tg=0.1, ug=-0.1, ccg=0.3, compg=1.0, growth_config=gc)
    expected = 0.35 * 0.2 + 0.25 * 0.1 + 0.20 * -0.1 + 0.15 * 0.3 + 0.05 * 1.0
    assert abs(observed - expected) < 1e-12


def test_empty_portfolio_is_zero_not_missing_positive_growth():
    snap = compute_system_capability_state(
        CapabilityLibrary(), SkillLibrary(), previous_score=0.0
    )
    assert snap.capability_score == 0.0
    assert snap.cgr == 0.0


def test_t_interval_and_null_handling():
    full = summarize(range(1, 11))
    empty = summarize([None, None])
    assert full["n"] == 10
    assert full["ci95_low"] < full["mean"] < full["ci95_high"]
    assert empty["n"] == 0
    assert empty["mean"] is None


def test_no_cgm_ablation_masks_growth_measurements():
    cfg = load_config()
    runtime = ArmRuntime("A5_NO_CGM", SkillLibrary(), CapabilityLibrary(), mask_growth=True)
    row = summarize_round(
        runtime,
        round_index=0,
        previous=None,
        experiences=48,
        task_utility_mean=0.9,
        new_capabilities=0,
        config=cfg,
    )
    assert row["ct"] is None
    assert row["cgr"] is None
    assert row["ig"] is None
    assert row["capability_ids"] is None
    assert row["measurement_status"] == "unavailable_by_design_no_CGM"


def test_isolated_robustness_fixture_does_not_mutate_empty_portfolio():
    runtime = ArmRuntime("fixture", SkillLibrary(), CapabilityLibrary())
    before = len(runtime.library)
    result = run_isolated_robustness(runtime)
    assert result["growth_illusion"]["status"] == "evaluated"
    assert result["growth_illusion"]["baseline_empty"] is True
    assert result["growth_illusion"]["unchanged_within_tolerance"] is True
    assert len(runtime.library) == before


def test_analysis_accepts_structural_fixture_without_running_benchmark():
    arms = ["ASFT", "B1_NO_LEARNING", "B2_SKILL_STORAGE_ONLY", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY", "A1_NO_IDT", "A2_NO_SCT", "A3_NO_SKILL_LIBRARY", "A4_NO_COMPOSITION", "A5_NO_CGM"]
    seeds = []
    for seed in range(10):
        rounds = []
        tasks = []
        comps = []
        for arm in arms:
            for round_no in range(1, 5):
                masked = arm == "A5_NO_CGM"
                rounds.append({
                    "seed": seed, "arm": arm, "round": round_no,
                    "ct": None if masked else 0.1 + seed / 1000 + round_no / 1000,
                    "cgr": None if masked else 0.001,
                    "capu": None if masked else 0.1,
                    "portfolio_coverage": None if masked else 0.2,
                    "supported_family_coverage": None if masked else 0.25,
                    "mean_skill_utility_su": 0.1,
                    "mean_transfer_score_ts": 0.2,
                    "ig": None if masked else 0.01,
                    "igr": None if masked else 0.01,
                    "ie": None if masked else 0.0001,
                    "task_utility": 0.8 + seed / 1000 + round_no / 1000,
                    "n_capabilities": None if masked else (1 if arm == "ASFT" else 0),
                    "new_capabilities": None if masked else 0,
                    "fragmentation_ratio": None if masked else 0.1,
                    "saturation_ratio": None if masked else 0.0,
                    "composition_skill_count": None if masked else 0,
                    "ccg": None if masked else 0.01,
                    "ug": None if masked else 0.01,
                    "growth_state": "unavailable_by_design_no_CGM" if masked else "growing",
                    "capability_ids": None if masked else (["cap"] if arm == "ASFT" else []),
                    "representation_failures": None if masked else [],
                })
                tasks.append({"seed": seed, "arm": arm, "task_id": f"{seed}-{arm}-{round_no}", "task_utility": 0.8})
            if arm == "ASFT":
                comps.append({"seed": seed, "arm": arm, "status": "evaluated", "incremental_gain": 0.1, "success": True})
        seeds.append({"seed": seed, "round_rows": rounds, "task_rows": tasks, "composition_rows": comps, "formation_rows": [], "robustness": {"regression": {"status": "unavailable"}, "growth_illusion": {"status": "evaluated", "baseline_empty": False, "unchanged_within_tolerance": True}}})
    analysis = build_analysis({"experiment_id": "fixture", "seeds": seeds})
    assert len(analysis["seed_summaries"]) == 100
    assert analysis["prediction"]["status"] == "available"
    assert any(row["criterion"] == "positive_IE_trend" for row in analysis["decisions"])
    ie_slope = next(row for row in analysis["arm_metrics"] if row["arm"] == "ASFT" and row["metric"] == "ie_slope")
    assert ie_slope["n"] == 10


def test_phase13e_source_modules_remain_modular_and_bounded():
    root = Path(__file__).resolve().parents[1] / "experiments" / "phase13e"
    for path in root.glob("*.py"):
        assert len(path.read_text(encoding="utf-8").splitlines()) < 400, path.name
