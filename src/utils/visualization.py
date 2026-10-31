"""Plotting helpers for reports/figures (Phase 11).

Uses a non-interactive backend so figures render in CI and headless runs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")  # must precede pyplot import

import matplotlib.pyplot as plt  # noqa: E402

__all__ = ["plot_metric", "plot_series"]


def plot_metric(
    series: Sequence[float] | dict[str, Sequence[float]],
    title: str,
    path: str | Path,
    *,
    xlabel: str = "step",
    ylabel: str = "value",
    labels: Sequence[str] | None = None,
) -> Path:
    """Write a line chart for one or more series and return the file path."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if isinstance(series, dict):
        items = list(series.items())
    else:
        names = list(labels) if labels else ["value"]
        values = list(series)
        # A single flat list with labels means multiple aligned series.
        if labels and len(values) == len(names) and all(
            isinstance(v, (list, tuple)) for v in values
        ):
            items = list(zip(names, [list(v) for v in values]))  # type: ignore[arg-type]
        else:
            items = [(names[0], values)]

    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        for label, values in items:
            ys = [float(v) for v in values]
            ax.plot(range(len(ys)), ys, marker="o", linewidth=1.5, label=str(label))
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if len(items) > 1:
            ax.legend(frameon=False)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(target, dpi=140)
    finally:
        plt.close(fig)
    return target


def plot_series(
    values: Sequence[float],
    path: str | Path,
    *,
    title: str = "",
    xlabel: str = "step",
    ylabel: str = "value",
) -> Path:
    """Single-series convenience wrapper around :func:`plot_metric`."""
    return plot_metric(values, title or "metric", path, xlabel=xlabel, ylabel=ylabel)
