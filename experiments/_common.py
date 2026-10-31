"""Shared report writing for experiment runners (Phase 11).

Emits the JSON + Markdown pair under ``reports/metrics/`` and optional figures
under ``reports/figures/`` so every experiment produces paper-ready artifacts.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

__all__ = ["write_experiment", "write_figure"]


def write_experiment(
    name: str,
    payload: dict[str, Any],
    *,
    out_dir: str | Path = "reports/metrics",
    root: str | Path | None = None,
) -> dict[str, str]:
    """Write ``<name>.json`` and ``<name>.md``; return the paths."""
    directory = Path(root) / out_dir if root is not None else Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / f"{name}.json"
    md_path = directory / f"{name}.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(_to_markdown(name, payload), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path)}


def write_figure(
    name: str,
    series: dict[str, Sequence[float]],
    *,
    title: str,
    ylabel: str = "value",
    out_dir: str | Path = "reports/figures",
    root: str | Path | None = None,
) -> str:
    """Write a PNG line chart; return its path."""
    from utils.visualization import plot_metric

    directory = Path(root) / out_dir if root is not None else Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.png"
    plot_metric(series, title, path, xlabel="step", ylabel=ylabel)
    return str(path)


def _to_markdown(name: str, payload: dict[str, Any]) -> str:
    lines = [f"# {name}", ""]
    for key, value in payload.items():
        if isinstance(value, dict):
            lines.append(f"## {key}")
            lines.append("")
            for k, v in value.items():
                lines.append(f"- `{k}`: `{v}`")
            lines.append("")
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            lines.append(f"## {key}")
            lines.append("")
            headers = list(value[0].keys())
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join("---" for _ in headers) + " |")
            for row in value:
                lines.append(
                    "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |"
                )
            lines.append("")
        else:
            lines.append(f"- **{key}**: `{value}`")
    return "\n".join(lines) + "\n"
