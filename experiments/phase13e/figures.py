"""Dependency-free SVG figures for the Phase 13E evidence package."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Any

COLORS = {
    "ASFT": "#176b87",
    "B1_NO_LEARNING": "#6b7280",
    "B2_SKILL_STORAGE_ONLY": "#d18f00",
    "B3_RANDOM_SKILL_CREATION": "#c2413b",
    "B4_COMPRESSION_PROXY": "#7952a0",
    "A4_NO_COMPOSITION": "#2e8b57",
}
ARMS = list(COLORS)


def _mean_ci(rows: list[dict[str, Any]], key: str) -> tuple[float, float, float] | None:
    vals = [float(r[key]) for r in rows if r.get(key) is not None]
    if not vals:
        return None
    m = mean(vals)
    half = 2.262157 * stdev(vals) / len(vals) ** 0.5 if len(vals) > 1 else 0.0
    return m, m - half, m + half


def _svg_chart(title: str, ylabel: str, series: dict[str, list[tuple[int, float, float, float] | None]], path: Path, *, subtitle: str = "") -> None:
    width, height = 980, 560
    left, right, top, bottom = 90, 250, 82, 92
    plot_w, plot_h = width - left - right, height - top - bottom
    all_values = [v for rows in series.values() for item in rows if item for v in item[1:]]
    if not all_values:
        ymin, ymax = -0.05, 0.05
    else:
        ymin, ymax = min(all_values), max(all_values)
        if abs(ymax - ymin) < 1e-9:
            ymin -= 0.05
            ymax += 0.05
        pad = (ymax - ymin) * 0.10
        ymin, ymax = ymin - pad, ymax + pad
    def ymap(v: float) -> float:
        return top + (ymax - v) / (ymax - ymin) * plot_h
    def xmap(round_no: int) -> float:
        return left + (round_no - 1) / 3 * plot_w
    items = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{left}" y="34" font-family="Arial,sans-serif" font-size="24" font-weight="700" fill="#18313d">{title}</text>',
        f'<text x="{left}" y="58" font-family="Arial,sans-serif" font-size="13" fill="#52636a">{subtitle}</text>',
    ]
    for tick in range(5):
        val = ymin + (ymax - ymin) * tick / 4
        yy = ymap(val)
        items.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{left+plot_w}" y2="{yy:.1f}" stroke="#e2e8eb"/>')
        items.append(f'<text x="{left-12}" y="{yy+4:.1f}" text-anchor="end" font-family="Arial" font-size="12" fill="#60727a">{val:.3f}</text>')
    for r in range(1, 5):
        xx = xmap(r)
        items.append(f'<line x1="{xx:.1f}" y1="{top}" x2="{xx:.1f}" y2="{top+plot_h}" stroke="#f1f4f5"/>')
        items.append(f'<text x="{xx:.1f}" y="{top+plot_h+24}" text-anchor="middle" font-family="Arial" font-size="13" fill="#52636a">Round {r}</text>')
    items.extend([
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top+plot_h}" stroke="#65777f"/>',
        f'<line x1="{left}" y1="{top+plot_h}" x2="{left+plot_w}" y2="{top+plot_h}" stroke="#65777f"/>',
        f'<text transform="translate(24 {top+plot_h/2:.1f}) rotate(-90)" text-anchor="middle" font-family="Arial" font-size="14" fill="#354b53">{ylabel}</text>',
    ])
    for arm, vals in series.items():
        color = COLORS.get(arm, "#667085")
        pts = []
        for item in vals:
            if not item:
                continue
            r, m, lo, hi = item
            xx, yy = xmap(r), ymap(m)
            pts.append((xx, yy))
            ylo, yhi = ymap(lo), ymap(hi)
            items.append(f'<line x1="{xx:.1f}" y1="{ylo:.1f}" x2="{xx:.1f}" y2="{yhi:.1f}" stroke="{color}" stroke-width="1.5" opacity="0.72"/>')
            items.append(f'<line x1="{xx-4:.1f}" y1="{ylo:.1f}" x2="{xx+4:.1f}" y2="{ylo:.1f}" stroke="{color}"/>')
            items.append(f'<line x1="{xx-4:.1f}" y1="{yhi:.1f}" x2="{xx+4:.1f}" y2="{yhi:.1f}" stroke="{color}"/>')
        if len(pts) >= 2:
            point_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
            items.append(f'<polyline points="{point_str}" fill="none" stroke="{color}" stroke-width="3"/>')
        for xx, yy in pts:
            items.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="4.5" fill="{color}" stroke="#fff" stroke-width="1.5"/>')
    legend_y = top + 26
    for idx, (arm, _) in enumerate(series.items()):
        yy = legend_y + idx * 29
        items.append(f'<line x1="{left+plot_w+25}" y1="{yy}" x2="{left+plot_w+52}" y2="{yy}" stroke="{COLORS.get(arm, "#667085")}" stroke-width="3"/>')
        items.append(f'<text x="{left+plot_w+60}" y="{yy+4}" font-family="Arial" font-size="12" fill="#31464e">{arm.replace("_", " ")}</text>')
    items.append('</svg>')
    path.write_text("\n".join(items), encoding="utf-8")


def _series(rounds: list[dict[str, Any]], metric: str, arms: list[str] = ARMS) -> dict[str, list[tuple[int, float, float, float] | None]]:
    out: dict[str, list[tuple[int, float, float, float] | None]] = {}
    for arm in arms:
        out[arm] = []
        for r in range(1, 5):
            cells = [row for row in rounds if row["arm"] == arm and int(row["round"]) == r]
            stat = _mean_ci(cells, metric)
            out[arm].append((r, *stat) if stat else None)
    return out


def create_figures(rounds: list[dict[str, Any]], composition: list[dict[str, Any]], target: Path) -> list[Path]:
    target.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    specs = [
        ("figure_1_capability_trajectory.svg", "Capability trajectory across rounds", "C_t (mean capability score)", "Round mean and two-sided 95% seed-level CI; 10 seeds where available", "ct"),
        ("figure_2_cgr.svg", "Capability growth rate", "CGR per round", "CGR = change in C_t divided by the preregistered one-round interval", "cgr"),
        ("figure_3_coverage.svg", "Capability coverage growth", "Portfolio coverage", "Repository portfolio coverage; empty portfolios remain zero", "portfolio_coverage"),
        ("figure_4_capability_utility.svg", "Capability utility growth", "Mean CapU", "Mean CapU over non-archived validated capabilities", "capu"),
        ("figure_5_composition_growth.svg", "Composition-associated portfolio growth", "Promoted composition skills", "Composition task outcomes are separately reported in Table 3 and task-level data", "composition_skill_count"),
    ]
    for fname, title, ylabel, subtitle, metric in specs:
        p = target / fname
        _svg_chart(title, ylabel, _series(rounds, metric), p, subtitle=subtitle)
        paths.append(p)
    # Figure 6: two-panel paired SVG using same helper; overlay IG/IGR by title.
    upper = _series(rounds, "ig")
    lower = _series(rounds, "igr")
    p = target / "figure_6_ig_igr.svg"
    tmp1, tmp2 = target / "._ig_tmp.svg", target / "._igr_tmp.svg"
    _svg_chart("Intelligence growth (IG)", "IG", upper, tmp1, subtitle="Primary frozen weighted CGM aggregate")
    _svg_chart("Intelligence growth rate (IGR)", "IGR per round", lower, tmp2, subtitle="First difference of IG across adjacent rounds")
    # Reuse the chart contents as two stacked SVG groups in a single deliverable.
    a = tmp1.read_text(encoding="utf-8").replace('<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" viewBox="0 0 980 560">', '<g transform="translate(0,0)">').replace('</svg>', '</g>')
    b = tmp2.read_text(encoding="utf-8").replace('<svg xmlns="http://www.w3.org/2000/svg" width="980" height="560" viewBox="0 0 980 560">', '<g transform="translate(0,545)">').replace('</svg>', '</g>')
    p.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="980" height="1100" viewBox="0 0 980 1100">\n' + a + '\n' + b + '\n</svg>', encoding="utf-8")
    tmp1.unlink(missing_ok=True)
    tmp2.unlink(missing_ok=True)
    paths.append(p)
    return paths
