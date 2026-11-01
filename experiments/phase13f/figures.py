"""Dependency-free SVG evidence figures."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .statistics import BASELINES, ABLATIONS


def _bar_svg(title: str, labels: list[str], values: list[float | None], path: Path, ylabel: str) -> None:
    width, height, left, bottom = 960, 500, 90, 390
    valid = [float(v) for v in values if v is not None]
    low = min([0.0, *valid]) if valid else 0.0
    high = max([0.1, *valid]) if valid else 1.0
    span = max(1e-9, high - low)
    xstep = 780 / max(1, len(labels))
    bars = []
    for i, (label, value) in enumerate(zip(labels, values)):
        x = left + i * xstep + xstep * 0.16
        bw = xstep * 0.68
        y0 = bottom - (0 - low) / span * 300
        if value is None:
            bars.append(f'<rect x="{x:.1f}" y="{bottom-12}" width="{bw:.1f}" height="12" fill="#cbd5e1"/><text x="{x+bw/2:.1f}" y="{bottom-23}" text-anchor="middle" font-size="11">NA</text>')
        else:
            yv = bottom - (float(value) - low) / span * 300
            y, h = min(y0, yv), max(2, abs(y0-yv))
            color = "#0f766e" if i == 0 else "#4f46e5"
            bars.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{color}"/><text x="{x+bw/2:.1f}" y="{y-6:.1f}" text-anchor="middle" font-size="11">{float(value):.3f}</text>')
        bars.append(f'<text transform="translate({x+bw/2:.1f},{bottom+18}) rotate(40)" text-anchor="start" font-size="11">{label}</text>')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="white"/><text x="{width/2}" y="34" text-anchor="middle" font-size="22" font-family="sans-serif">{title}</text><text transform="translate(22,240) rotate(-90)" text-anchor="middle" font-size="14">{ylabel}</text><line x1="{left}" y1="{bottom}" x2="900" y2="{bottom}" stroke="#334155"/>{''.join(bars)}<text x="{left}" y="{bottom+90}" font-size="11">Paired seed design; error intervals are in the linked CSV tables.</text></svg>', encoding="utf-8")


def _metric(analysis: dict[str, Any], arm: str, metric: str) -> float | None:
    row = next((r for r in analysis["arm_metrics"] if r["arm"] == arm and r["metric"] == metric), None)
    return row.get("mean") if row else None


def create_figures(analysis: dict[str, Any], out: Path) -> list[Path]:
    paths = []
    specs = [
        ("figure_1_asft_vs_baselines.svg", "ASFT vs mandatory baselines", ["ASFT", *BASELINES], "mean_task_utility_all_tasks", "Mean held-out task utility"),
        ("figure_2_ablation_comparison.svg", "ASFT vs component ablations", ["ASFT", *ABLATIONS], "mean_cgr", "Mean CGR"),
        ("figure_3_contribution_effects.svg", "Paired task-utility differences by contribution", [f"vs {x}" for x in [*BASELINES, *ABLATIONS]], "contrast_mean", "ASFT minus comparator task utility"),
        ("figure_4_sensitivity.svg", "Frozen sensitivity settings", ["SENS_SCV_Q25", "ASFT", "SENS_SCV_Q75", "SENS_IS_7_5", "SENS_IS_10", "SENS_COMP_LOOSE", "SENS_COMP_STRICT"], "mean_task_utility_all_tasks", "Mean held-out task utility"),
    ]
    for filename, title, labels, metric, ylabel in specs:
        values = []
        for label in labels:
            arm = label[3:] if label.startswith("vs ") else label
            if metric == "contrast_mean":
                contrast = next((r for r in analysis["paired_contrasts"] if r["contrast"] == f"ASFT - {arm}" and r["metric"] == "mean_task_utility_all_tasks"), None)
                values.append(contrast.get("mean") if contrast else None)
            else:
                values.append(_metric(analysis, arm, metric))
        path = out / filename
        _bar_svg(title, labels, values, path, ylabel)
        paths.append(path)
    return paths
