"""Report writer emits JSON + Markdown."""

from evaluation.harness.runner import run_benchmark
from evaluation.reports import write_report


def test_write_report_tmp(tmp_path):
    run = run_benchmark("skill", run_id="rep1")
    paths = write_report(run, out_dir=tmp_path, run_name="rep1")
    assert paths["json"].exists()
    assert paths["md"].exists()
    text = paths["json"].read_text(encoding="utf-8")
    assert "capability" in text or "skill" in text
    assert "reports" in text
