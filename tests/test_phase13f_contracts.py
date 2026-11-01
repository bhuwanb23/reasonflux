from __future__ import annotations

from types import SimpleNamespace

import pytest

from experiments.phase13f.arms import build_arms
from experiments.phase13f.cli import run
from experiments.phase13f.common import load_config, names
from experiments.phase13f.statistics import _effect, build_analysis


def _empty_discovery():
    return {"candidates": [], "trace_run": SimpleNamespace(traces=[])}


def test_frozen_seed_block_and_unique_arm_names():
    cfg = load_config()
    assert cfg["seeds"] == list(range(70, 80))
    assert len(names(cfg)) == len(set(names(cfg)))
    assert "B4_COMPRESSION_PROXY" in names(cfg)


def test_baseline_and_ablation_policies_are_distinct():
    cfg = load_config()
    arms = build_arms(0, _empty_discovery(), cfg)
    assert not arms["B1_NO_LEARNING"].enable_capabilities
    assert not arms["B2_MEMORY_SKILL_STORE"].enable_capabilities
    assert arms["A2_2_NO_LIFECYCLE"].lifecycle_enabled is False
    assert arms["A2_3_NO_COMPOSITION"].enable_composition is False
    assert arms["ASFT"].enable_composition is True
    assert arms["X3_NO_EXPERIENCE_MEMORY"].arm == "X3_NO_EXPERIENCE_MEMORY"


def test_cgm_measurement_ablations_are_marked_not_comparators():
    arms = build_arms(0, _empty_discovery(), load_config())
    assert arms["A3_1_NO_GROWTH_TRACKING"].mask_growth
    assert arms["A3_2_INDEPENDENT_CAPABILITIES"].mask_growth
    assert arms["A3_2_INDEPENDENT_CAPABILITIES"].independent_capabilities
    assert not arms["A3_NO_CAPABILITY_LAYER"].enable_capabilities
    assert arms["X4_NO_CAPABILITY_FORMATION"].enable_capabilities
    assert not arms["X4_NO_CAPABILITY_FORMATION"].allow_capability_formation


def test_no_library_ablation_discards_created_library():
    arms = build_arms(0, _empty_discovery(), load_config())
    assert not arms["X2_NO_SKILL_LIBRARY"].enabled_library
    assert len(arms["X2_NO_SKILL_LIBRARY"].library) == 0


def test_random_and_scv_sensitivity_arms_are_explicit():
    arms = build_arms(4, _empty_discovery(), load_config())
    assert "A2_1_RANDOM_SCV" in arms
    assert "SENS_SCV_Q25" in arms and "SENS_SCV_Q75" in arms
    assert "SENS_IS_7_5" in arms and "SENS_IS_10" in arms


def test_candidate_selection_budgets_are_correct(monkeypatch):
    from core.skill import Skill
    from core.states import SkillState
    import experiments.phase13f.arms as module

    items = []
    for index, strength in enumerate((4.0, 8.0, 11.0)):
        inv = SimpleNamespace(invariant_id=f"i{index}", strength=strength, metadata={"validation": {"frequency": index + 1}})
        items.append({"invariant": inv, "candidate": object(), "score": {"SCV10": index + 0.1, "p_reuse_raw": index + 1}})

    def fake_create(item, library, config):
        skill = Skill(skill_id=item["invariant"].invariant_id, source_invariant_id=item["invariant"].invariant_id,
                      trigger_conditions=["apply_reflection"], execution_policy="test", abstraction_gain=0.1,
                      transfer_score=0.0, creation_cost=0.1, utility=0.0, state=SkillState.PROMOTED, metadata={})
        library.add(skill)
        return skill

    monkeypatch.setattr(module, "_create_candidate_skill", fake_create)
    arms = build_arms(0, {"candidates": items, "trace_run": SimpleNamespace(traces=[])}, load_config())
    assert len(arms["ASFT"].library) == 3
    assert len(arms["A2_NO_SCV"].library) == 3
    assert len(arms["A2_1_RANDOM_SCV"].library) == 3
    assert len(arms["B3_RANDOM_SKILL_CREATION"].library) == 2
    assert len(arms["SENS_IS_7_5"].library) == 2
    assert len(arms["SENS_IS_10"].library) == 1


def test_pair_effect_size_handles_zero_sd_as_undefined():
    result = _effect([0.0, 0.0, 0.0])
    assert result["mean"] == 0.0
    assert result["cohen_dz"] is None
    assert result["hedges_g"] is None


def test_effect_size_reports_paired_standardized_difference():
    result = _effect([1.0, 2.0, 3.0, 4.0])
    assert result["cohen_dz"] is not None
    assert result["hedges_g"] is not None
    assert result["n"] == 4


def test_analysis_decisions_keep_all_mandatory_comparisons():
    run_record = {"seeds": []}
    for seed in range(10):
        seed_record = {"seed": seed, "round_rows": [], "task_rows": []}
        for arm in ["ASFT", "B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY"]:
            for rnd in range(1, 5):
                seed_record["round_rows"].append({"seed": seed, "arm": arm, "round": rnd, "IS": 1.0, "SU": 0.5, "TS": 0.2, "cgr": 0.1, "ig": 0.1, "portfolio_coverage": 0.5, "task_utility": 0.8, "skill_count_created": 1, "skill_count_persistent": 1})
            seed_record["task_rows"].append({"seed": seed, "arm": arm, "task_utility": 0.8, "observed_success": True})
        run_record["seeds"].append(seed_record)
    analysis = build_analysis(run_record)
    assert {r["criterion"] for r in analysis["decisions"] if r["criterion"].startswith("ASFT_beats_")} == {f"ASFT_beats_{arm}" for arm in ["B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY"]}


def test_phase13e_metric_adapter_receives_frozen_13f_config():
    from experiments.phase13e.metrics import summarize_round
    cfg = load_config()
    runtime = build_arms(70, _empty_discovery(), cfg)["B1_NO_LEARNING"]
    row = summarize_round(runtime, round_index=0, previous=None, experiences=32,
                          task_utility_mean=0.5, new_capabilities=0, config=cfg)
    assert row["measurement_status"] == "available"
    assert row["cgr"] == 0.0


def test_confirmation_is_explicit():
    with pytest.raises(SystemExit):
        run(confirm=False)
