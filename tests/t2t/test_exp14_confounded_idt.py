"""EXP-IDT-14's controlled frequent-no-op stress-test contracts."""

from experiments import exp14_confounded_idt
from experiments.exp14_confounded_idt import _discovery_traces, run_one


def test_confounded_benchmark_injects_noop_only_in_registered_families():
    base, confounded = _discovery_traces(10)
    assert len(base) == len(confounded) == 48

    injected = [
        trace
        for trace in confounded
        if trace.metadata.get("exp14_role") == "frequent_nontransfer_noop"
    ]
    assert len(injected) == 36
    assert {trace.metadata["task_family"] for trace in injected} == {
        "reflection",
        "rotation",
        "counting",
    }
    assert all("normalize_grid" in trace.operations for trace in injected)
    assert all(
        "normalize_grid" not in trace.operations
        for trace in confounded
        if trace.metadata.get("task_family") == "grouping"
    )


def test_transfer_ranking_rejects_frequency_confounded_noop():
    result = run_one(10)
    diagnostics = result["ranking_diagnostics"]
    candidate_by_key = {
        row["semantic_key"]: row for row in result["candidate_rows"]
    }

    assert candidate_by_key["normalize_grid"]["frequency"] > candidate_by_key[
        "reflection"
    ]["frequency"]
    assert candidate_by_key["normalize_grid"]["evaluation"]["TU"] == 0.0
    assert candidate_by_key["reflection"]["evaluation"]["TU"] > 0.0
    assert diagnostics["transfer_order"][0]["semantic_key"] == "reflection"
    assert diagnostics["frequency_order"][0]["semantic_key"] == "normalize_grid"
    assert result["stress_test_success"] is True


def test_exp14_aggregation_uses_five_configured_seeds_and_controls(monkeypatch):
    def fake_run_one(seed):
        primary = 0.2 + seed / 1000
        return {
            "seed": seed,
            "metrics": {
                "ASFT": primary,
                "frequency_only": 0.0,
                "no_transfer": 0.0,
                "random_pattern": 0.05,
                "ASFT_advantage": primary,
                "ASFT_minus_no_transfer": primary,
                "ASFT_minus_random": primary - 0.05,
            },
            "ranking_diagnostics": {
                "mean_held_out_TU_at_k": {
                    "1": {
                        "ASFT": primary,
                        "frequency_only": 0.0,
                        "no_transfer": 0.0,
                    },
                    "2": {
                        "ASFT": 0.1,
                        "frequency_only": 0.05,
                        "no_transfer": 0.05,
                    },
                }
            },
            "stress_test_success": True,
        }

    monkeypatch.setattr(exp14_confounded_idt, "run_one", fake_run_one)
    result = exp14_confounded_idt.run_exp14(write=False)

    assert result["seeds"] == [10, 11, 12, 13, 14]
    assert result["stress_test_success"] is True
    assert len(result["raw_results"]) == 5
    assert result["metrics"]["ASFT"] > result["metrics"]["frequency_only"]
    assert result["metrics"]["ASFT"] > result["metrics"]["no_transfer"]
    assert result["metrics"]["ASFT"] > result["metrics"]["random_pattern"]
    assert result["top_k_statistics"]["2"]["ASFT"]["mean"] == 0.1
