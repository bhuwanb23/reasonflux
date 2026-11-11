"""End-to-end evaluation pipeline."""

from pipelines.evaluation_pipeline import run_evaluation_pipeline


def test_pipeline_growth_vs_baseline(tmp_path):
    growth = run_evaluation_pipeline(
        level="capability",
        out_dir=tmp_path / "growth",
        write=True,
        run_id="e2e_growth",
    )
    flat = run_evaluation_pipeline(
        level="capability",
        baseline="A",
        out_dir=tmp_path / "flat",
        write=True,
        run_id="e2e_flat",
    )
    assert growth["maturity"] >= 1
    assert growth["success"] is True
    assert flat["success"] is False
    assert growth["paths"].get("json")
    assert (tmp_path / "growth").exists()


def test_pipeline_intelligence_level(tmp_path):
    out = run_evaluation_pipeline(
        level="intelligence",
        out_dir=tmp_path,
        write=False,
        run_id="e2e_intel",
    )
    layers = {lr["layer"]: lr for lr in out["result"]["layers"]}
    assert "intelligence" in layers
    assert out["maturity"] >= 1
