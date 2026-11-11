"""Harness statistics helpers."""

from evaluation.harness.stats import (
    confidence_interval,
    mean,
    median,
    summarize,
    variance,
)


def test_mean_median_variance_ci():
    vals = [1.0, 2.0, 3.0, 4.0]
    assert abs(mean(vals) - 2.5) < 1e-9
    assert abs(median(vals) - 2.5) < 1e-9
    assert abs(median([1.0, 2.0, 3.0]) - 2.0) < 1e-9
    assert variance(vals) > 0
    lo, hi = confidence_interval(vals)
    assert lo < mean(vals) < hi
    summary = summarize(vals)
    assert summary["n"] == 4.0
    assert summary["ci_low"] <= summary["mean"] <= summary["ci_high"]
