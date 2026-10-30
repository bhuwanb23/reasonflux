"""Generate evaluation reports under reports/ (Phase 11E-4)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evaluation.harness.maturity import maturity_label
from evaluation.harness.models import EvaluationRun


def _section(run: EvaluationRun, layer: str) -> dict[str, Any]:
    for lr in run.layers:
        if lr.layer == layer:
            return lr.to_dict()
    return {"layer": layer, "passed": False, "metrics": {}, "notes": ["missing"]}


def write_report(
    result: EvaluationRun | dict[str, Any],
    out_dir: str | Path = "reports/metrics",
    *,
    run_name: str | None = None,
) -> dict[str, Path]:
    """Write JSON + Markdown summary for a benchmark run.

    Returns paths for ``json`` and ``md`` artifacts.
    """
    run = result if isinstance(result, EvaluationRun) else None
    payload: dict[str, Any]
    if run is not None:
        payload = {
            "run": run.to_dict(),
            "reports": {
                "invariant": _section(run, "invariant"),
                "skill": _section(run, "skill"),
                "transfer": _section(run, "transfer"),
                "capability": _section(run, "capability"),
                "intelligence": _section(run, "intelligence"),
            },
            "maturity_label": maturity_label(run.maturity),
            "success": run.success,
        }
        name = run_name or f"eval_{run.run_id}"
    else:
        payload = dict(result)
        name = run_name or str(payload.get("run_id") or "eval_run")

    directory = Path(out_dir)
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / f"{name}.json"
    md_path = directory / f"{name}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        f"# ASFT Evaluation Report — {name}",
        "",
        f"- success: `{payload.get('success')}`",
        f"- maturity: `{payload.get('maturity_label')}`",
        "",
        "## Layers",
        "",
    ]
    reports = payload.get("reports") or {}
    for key in ("invariant", "skill", "transfer", "capability", "intelligence"):
        sec = reports.get(key) or {}
        lines.append(
            f"- **{key}**: passed=`{sec.get('passed')}` metrics=`{sec.get('metrics')}`"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {"json": json_path, "md": md_path}
