"""Paper-facing statistics for multi-seed experiment results."""

from __future__ import annotations

from statistics import NormalDist
from typing import Mapping, Sequence

from evaluation.harness.stats import summarize


def summarize_metric(values: Sequence[float], *, confidence: float = 0.95) -> dict[str, float]:
    """Return mean, standard deviation, variance, and normal CI.

    The harness uses a normal approximation consistently with its existing
    ``ci_z`` policy. The confidence argument is recorded for provenance;
    0.95 maps to the standard 1.96 z value.
    """
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    z = NormalDist().inv_cdf((1.0 + confidence) / 2.0)
    summary = summarize(values, z=z)
    variance = float(summary["variance"])
    return {
        "n": float(summary["n"]),
        "mean": float(summary["mean"]),
        "std": variance**0.5,
        "variance": variance,
        "ci_low": float(summary["ci_low"]),
        "ci_high": float(summary["ci_high"]),
        "confidence": float(confidence),
    }


def summarize_metrics(
    values_by_metric: Mapping[str, Sequence[float]], *, confidence: float = 0.95
) -> dict[str, dict[str, float]]:
    """Aggregate each metric independently across seeds."""
    return {
        str(name): summarize_metric(values, confidence=confidence)
        for name, values in values_by_metric.items()
    }
