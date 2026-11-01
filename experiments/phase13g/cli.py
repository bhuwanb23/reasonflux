"""Explicitly confirmed Phase 13G runner with pre-run source/data freeze."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import DATA, OUT, ROOT
from .reporting import write_evidence
from .runner import run_phase


def _hash(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def _source_manifest() -> tuple[list[dict[str,str]],str]:
    paths=[]
    for base in (ROOT/"experiments/phase13g", ROOT/"src"):
        paths.extend(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)
    paths.extend([ROOT/"experiments/phase13g/config.json",ROOT/"experiments/phase13g/preregistration.md",
                  ROOT/"datasets/arc/arc-agi-2/README.md",ROOT/"datasets/arc/arc-agi-2/LICENSE",
                  ROOT/"datasets/arc/arc-agi-2/source_manifest.json",ROOT/"datasets/arc/arc-agi-2/split_manifest.json",
                  ROOT/"tests/test_phase13g_contracts.py",
                  ROOT/"docs/03_implementation/validation/phase_13g_preflight.md"])
    records=[{"path":p.relative_to(ROOT).as_posix(),"sha256":_hash(p)} for p in sorted(set(paths))]
    root_hash=hashlib.sha256("\n".join(f"{r['path']}:{r['sha256']}" for r in records).encode()).hexdigest()
    return records,root_hash


def build_manifest() -> dict[str,Any]:
    sources,source_hash=_source_manifest()
    source_data=json.loads((DATA/"source_manifest.json").read_text())
    splits=json.loads((DATA/"split_manifest.json").read_text())
    return {"experiment_id":"PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1",
            "status":"frozen_pre_run","created_at_utc":datetime.now(timezone.utc).isoformat(),
            "python":sys.version,"platform":platform.platform(),
            "config_sha256":_hash(ROOT/"experiments/phase13g/config.json"),
            "preregistration_sha256":_hash(ROOT/"experiments/phase13g/preregistration.md"),
            "source_tree_sha256":source_hash,"source_files":sources,
            "dataset_commit":source_data["commit"],"dataset_source_manifest_sha256":_hash(DATA/"source_manifest.json"),
            "split_manifest_sha256":_hash(DATA/"split_manifest.json"),
            "task_count":source_data["count"],"split_counts":splits["counts"],
            "official_evaluation_json_extracted_or_scored":False,
            "transport_deviation":source_data["transport_note"],
            "prior_attempts":[{"path":"reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1-ATTEMPT-01-REPORT-WRITE-FAILED",
                               "status":"report_write_failure_after_holdout_predictions_generated_in_memory",
                               "outcome_tables_persisted":False,"outcomes_inspected_during_debugging":False,
                               "current_run_is_independent_replication":False}],
            "same_holdout_reused_after_software_serialization_fix":True,
            "holdout_scored":False}


def main() -> None:
    parser=argparse.ArgumentParser(description="Run frozen Phase 13G ARC-AGI-2 bounded validation")
    parser.add_argument("--confirm",action="store_true",help="confirm one new frozen run")
    args=parser.parse_args()
    if not args.confirm: parser.error("Phase 13G run requires explicit --confirm")
    if OUT.exists() and any(OUT.iterdir()):
        raise SystemExit(f"Refusing to overwrite Phase 13G artifacts in {OUT}; preserve and inspect them first.")
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=build_manifest()
    (OUT/"frozen_run_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    manifest["status"]="running"
    manifest["started_at_utc"]=datetime.now(timezone.utc).isoformat()
    (OUT/"run_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    try:
        results=run_phase()
        write_evidence(results,manifest)
        print(f"Phase 13G evidence package written: {OUT/'evidence_package.md'}",flush=True)
    except BaseException as exc:
        manifest["status"]="incomplete_error"
        manifest["error"]=f"{type(exc).__name__}: {exc}"
        manifest["failed_at_utc"]=datetime.now(timezone.utc).isoformat()
        (OUT/"run_manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
        raise


if __name__ == "__main__":
    main()
