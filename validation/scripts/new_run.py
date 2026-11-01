#!/usr/bin/env python3
"""Create a non-overwriting ReasonFlux validation run bundle from templates."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
TRACKS = {"agi2", "agi3"}
HYPOTHESES = {"H1_IDT", "H2_SCT", "H3_CGM"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--track", required=True, choices=sorted(TRACKS))
    p.add_argument("--hypothesis", required=True, choices=sorted(HYPOTHESES))
    p.add_argument("--run-id", required=True, help="Unique ID, e.g. 20261029_agi2_H1_IDT_v01")
    p.add_argument("--owner", required=True)
    p.add_argument("--variant", default="REQUIRED_BEFORE_RUN")
    args = p.parse_args()

    if any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for ch in args.run_id):
        p.error("run-id may contain only letters, digits, underscore, and hyphen")
    out = ROOT / "results" / args.track / args.hypothesis / args.run_id
    if out.exists():
        p.error(f"Refusing to overwrite existing run bundle: {out}")
    out.mkdir(parents=True)
    shutil.copy2(ROOT / "ENVIRONMENT_TEMPLATE.yaml", out / "environment.yaml")
    shutil.copy2(ROOT / "DATA_MANIFEST_TEMPLATE.csv", out / "data_manifest.csv")
    (out / "config.yaml").write_text(
        f"run_id: {args.run_id}\ntrack: {args.track}\nhypothesis: {args.hypothesis}\n"
        f"variant_id: {args.variant}\nowner: {args.owner}\nstatus: NOT_RUN\n"
        "protocol_version: 0.1-draft\n# Fill all REQUIRED_BEFORE_RUN values before execution.\n",
        encoding="utf-8",
    )
    (out / "metrics.json").write_text(
        '{\n  "run_id": "' + args.run_id + '",\n  "status": "NOT_RUN",\n'
        '  "official_score": null,\n  "primary_metric": null,\n'
        '  "secondary_metrics": {},\n  "uncertainty_interval": null,\n'
        '  "task_count": null,\n  "failed_count": null,\n'
        '  "note": "Null values are not results; populate only from evaluator output."\n}\n',
        encoding="utf-8",
    )
    (out / "NOTES.md").write_text(
        f"# Run {args.run_id}\n\nStatus: NOT_RUN\n\n"
        f"Created UTC: {datetime.now(timezone.utc).isoformat()}\n\n"
        "Do not execute until protocol and manifest placeholders are filled and reviewed.\n",
        encoding="utf-8",
    )
    for name in ("traces.jsonl", "skill_events.jsonl", "stdout.log", "stderr.log"):
        (out / name).write_text("", encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
