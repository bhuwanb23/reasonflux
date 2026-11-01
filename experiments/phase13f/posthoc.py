"""Refresh Phase 13F evidence from saved run records only; never runs seeds."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import OUT, ROOT
from .reporting import write_package


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def refresh_saved_evidence() -> Path:
    records_path = OUT / "run_records.json"
    frozen_path = OUT / "frozen_run_manifest.json"
    current_path = OUT / "run_manifest.json"
    posthoc_path = OUT / "posthoc_analysis_manifest.json"
    if not records_path.exists() or not frozen_path.exists() or not current_path.exists():
        raise FileNotFoundError("Complete Phase 13F run records and frozen manifests are required")
    before = _sha(records_path)
    prior = json.loads(posthoc_path.read_text(encoding="utf-8")) if posthoc_path.exists() else None
    if prior and prior.get("saved_records_sha256_before") != before:
        raise RuntimeError("Saved records differ from the previously analyzed record set")
    run: dict[str, Any] = json.loads(records_path.read_text(encoding="utf-8"))
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    manifest = json.loads(current_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "complete":
        raise ValueError("Only completed saved records may be refreshed")
    code_paths = [ROOT / "experiments/phase13f/posthoc.py", ROOT / "experiments/phase13f/reporting.py",
                  ROOT / "experiments/phase13f/figures.py", ROOT / "experiments/phase13f/statistics.py"]
    hashes = {p.relative_to(ROOT).as_posix(): _sha(p) for p in code_paths}
    code_sha = hashlib.sha256("\n".join(f"{k}:{v}" for k, v in sorted(hashes.items())).encode()).hexdigest()
    audit = {"status": "complete_saved_records_only", "completed_at_utc": datetime.now(timezone.utc).isoformat(),
             "reason": "Expanded the result interpretation and raw-difference contribution figure; corrected only report presentation. No metric formula, threshold, decision gate, runner, or task outcome changed.",
             "benchmark_rerun": False, "saved_records_sha256_before": before,
             "frozen_run_source_tree_sha256": frozen.get("source_tree_sha256"),
             "posthoc_source_tree_sha256": code_sha, "posthoc_source_files": hashes,
             "python": sys.version}
    manifest["posthoc_analysis"] = audit
    report = write_package(run, manifest)
    after = _sha(records_path)
    if before != after:
        raise RuntimeError("run_records.json changed during saved-record analysis")
    audit["saved_records_sha256_after"] = after
    posthoc_path.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    current_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(refresh_saved_evidence())
