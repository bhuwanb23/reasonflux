"""Rebuild Phase 13E analysis artifacts from saved records only; never runs seeds."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import ROOT
from .reporting import OUT, write_evidence_package


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rebuild_from_saved_records() -> Path:
    records_path = OUT / "run_records.json"
    frozen_path = OUT / "frozen_run_manifest.json"
    current_path = OUT / "run_manifest.json"
    posthoc_path = OUT / "posthoc_analysis_manifest.json"
    if not records_path.exists() or not frozen_path.exists() or not current_path.exists():
        raise FileNotFoundError("Complete saved records and both run manifests are required")
    records_hash_before = _sha(records_path)
    if posthoc_path.exists():
        prior = json.loads(posthoc_path.read_text(encoding="utf-8"))
        if prior.get("saved_records_sha256_before") != records_hash_before:
            raise FileExistsError("Refusing posthoc refresh because saved run records changed")
    run: dict[str, Any] = json.loads(records_path.read_text(encoding="utf-8"))
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    manifest = json.loads(current_path.read_text(encoding="utf-8"))
    if len(run.get("seeds", [])) != len(frozen.get("seeds", [])):
        raise ValueError("Saved seed count does not match frozen seed block")
    code_paths = [
        ROOT / "experiments/phase13e/posthoc.py",
        ROOT / "experiments/phase13e/statistics.py",
        ROOT / "experiments/phase13e/reporting.py",
        ROOT / "experiments/phase13e/figures.py",
    ]
    file_hashes = {p.relative_to(ROOT).as_posix(): _sha(p) for p in code_paths}
    source_hash = hashlib.sha256("\n".join(f"{k}:{v}" for k, v in sorted(file_hashes.items())).encode()).hexdigest()
    posthoc = {
        "status": "complete_saved_records_only",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "reason": "Corrected IE-slope aggregation and criterion-table rendering of observed paired contrasts; no runner, seed generation, task outcome, metric formula, or threshold changed.",
        "benchmark_rerun": False,
        "saved_records_sha256_before": records_hash_before,
        "frozen_run_source_tree_sha256": frozen.get("source_tree_sha256"),
        "posthoc_source_tree_sha256": source_hash,
        "posthoc_source_files": file_hashes,
        "python": sys.version,
    }
    manifest["posthoc_analysis"] = posthoc
    report = write_evidence_package(run, manifest)
    records_hash_after = _sha(records_path)
    if records_hash_after != records_hash_before:
        raise RuntimeError("run_records.json changed during posthoc analysis")
    posthoc["saved_records_sha256_after"] = records_hash_after
    posthoc_path.write_text(json.dumps(posthoc, indent=2, sort_keys=True), encoding="utf-8")
    # Keep the completed manifest synchronized with the explicit posthoc audit.
    current_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(rebuild_from_saved_records())
