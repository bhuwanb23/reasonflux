"""Shared report writing for experiment runners (Phase 11).

Emits the JSON + Markdown pair under ``reports/metrics/`` and optional figures
under ``reports/figures/`` so every experiment produces paper-ready artifacts.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

from evaluation.metrics_registry import metric_definitions
from evaluation.stats import summarize_metrics

__all__ = [
    "ExperimentRecord",
    "default_seeds",
    "run_multi_seed",
    "write_experiment",
    "write_experiment_record",
    "write_figure",
]


@dataclass(slots=True)
class ExperimentRecord:
    """Auditable input/output record for one experiment execution."""

    experiment_id: str
    seed: int
    dataset_version: str
    configuration: dict[str, Any]
    thresholds: dict[str, Any]
    metrics: dict[str, Any]
    artifacts: dict[str, str]
    timestamp_utc: str
    status: str = "completed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_seeds(root: str | Path | None = None) -> tuple[int, ...]:
    """Load the minimum governed seed set from configs/experiments.yaml."""
    try:
        import yaml

        base = Path(root) if root is not None else Path(__file__).resolve().parents[1]
        config = yaml.safe_load(
            (base / "configs" / "experiments.yaml").read_text(encoding="utf-8")
        )
        seeds = config["seed_policy"]["minimum_seeds"]
        return tuple(int(seed) for seed in seeds)
    except (OSError, KeyError, TypeError, ValueError):
        return (0, 1, 2, 3, 4)


def confidence_level(root: str | Path | None = None) -> float:
    """Load the fixed confidence level from the experiment policy."""
    try:
        import yaml

        base = Path(root) if root is not None else Path(__file__).resolve().parents[1]
        config = yaml.safe_load(
            (base / "configs" / "experiments.yaml").read_text(encoding="utf-8")
        )
        return float(config["seed_policy"]["confidence_level"])
    except (OSError, KeyError, TypeError, ValueError):
        return 0.95


def run_multi_seed(
    runner: Callable[..., dict[str, Any]],
    *,
    seeds: Sequence[int],
    metric_paths: dict[str, str],
    experiment_id: str,
    dataset_version: str = "synthetic-v1",
    configuration: dict[str, Any] | None = None,
    thresholds: dict[str, Any] | None = None,
    confidence: float | None = None,
    write: bool = True,
    root: str | Path | None = None,
) -> dict[str, Any]:
    """Run an experiment for each seed and write raw and aggregate records."""
    raw: list[dict[str, Any]] = []
    metric_values: dict[str, list[float]] = {name: [] for name in metric_paths}
    for seed in seeds:
        result = runner(seed=int(seed), write=False)
        raw.append({"seed": int(seed), "result": result})
        for metric, path in metric_paths.items():
            value: Any = result
            for part in path.split("."):
                value = value[part]
            metric_values[metric].append(float(value))

    confidence = confidence if confidence is not None else confidence_level(root)
    aggregate = summarize_metrics(metric_values, confidence=confidence)
    payload = {
        "experiment_id": experiment_id,
        "dataset_version": dataset_version,
        "configuration": configuration or {},
        "thresholds": thresholds or {},
        "metrics": {name: values["mean"] for name, values in aggregate.items()},
        "metric_definitions": metric_definitions(list(metric_paths)),
        "confidence_level": confidence,
        "seeds": [int(seed) for seed in seeds],
        "raw_results": raw,
        "statistics": aggregate,
        "results": aggregate,
        "failure_cases": [],
        "observations": {},
    }
    if write:
        payload["artifacts"] = write_experiment_record(
            experiment_id,
            payload,
            root=root,
        )
    return payload


def write_experiment_record(
    experiment_id: str,
    payload: dict[str, Any],
    *,
    root: str | Path | None = None,
) -> dict[str, str]:
    """Write a Phase 13A record under reports/experiments/<id>/."""
    directory = Path(root) / "reports" / "experiments" / experiment_id if root else Path(
        "reports"
    ) / "experiments" / experiment_id
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        **payload,
        "seed": payload.get("seed"),
        "dataset_version": payload.get("dataset_version", "synthetic-v1"),
        "configuration": payload.get("configuration", {}),
        "thresholds": payload.get("thresholds", {}),
        "metrics": payload.get("metrics", {}),
        "metric_definitions": metric_definitions(
            list(payload.get("metrics", {}))
        ),
        "timestamp_utc": timestamp,
        "record_schema": "phase-13a-v1",
    }
    json_path = directory / "record.json"
    md_path = directory / "report.md"
    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(_to_markdown(experiment_id, record), encoding="utf-8")
    return {"json": str(json_path), "md": str(md_path)}


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
    record_artifacts = write_experiment_record(
        name,
        {
            "experiment_id": name,
            "seed": payload.get("seed"),
            "dataset_version": payload.get("dataset_version", "synthetic-v1"),
            "configuration": payload.get("configuration", {}),
            "dataset": payload.get("dataset", {}),
            "thresholds": payload.get("thresholds", {}),
            "metrics": payload.get("metrics", {}),
            "results": payload,
            "failure_cases": payload.get("failure_cases", []),
            "observations": payload.get("observations", {}),
        },
        root=root,
    )
    return {
        "json": str(json_path),
        "md": str(md_path),
        "record_json": record_artifacts["json"],
        "record_md": record_artifacts["md"],
    }


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
