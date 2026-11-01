"""Command-line entry point for frozen Phase 13E confirmation and reporting."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import ROOT, load_config
from .reporting import OUT, write_evidence_package
from .runner import run_seed


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _source_manifest() -> tuple[list[dict[str, str]], str]:
    roots = [ROOT / "src", ROOT / "experiments" / "phase13c", ROOT / "experiments" / "phase13e"]
    files: list[Path] = []
    for root in roots:
        for path in root.rglob("*.py"):
            if "__pycache__" not in path.parts:
                files.append(path)
    files += [ROOT / "experiments" / "phase13e" / "config.json", ROOT / "experiments" / "phase13e" / "preregistration.md", ROOT / "docs" / "03_implementation" / "validation" / "phase_13e_preflight.md", ROOT / "pyproject.toml", ROOT / "requirements.txt"]
    records = []
    for path in sorted(set(files)):
        records.append({"path": path.relative_to(ROOT).as_posix(), "sha256": _sha256(path)})
    tree = hashlib.sha256("\n".join(f"{r['path']}:{r['sha256']}" for r in records).encode()).hexdigest()
    return records, tree


def build_manifest(config: dict[str, Any]) -> dict[str, Any]:
    source_files, source_hash = _source_manifest()
    config_path = ROOT / "experiments" / "phase13e" / "config.json"
    prereg_path = ROOT / "experiments" / "phase13e" / "preregistration.md"
    preflight_path = ROOT / "docs" / "03_implementation" / "validation" / "phase_13e_preflight.md"
    return {
        "experiment_id": config["experiment_id"],
        "status": "running",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "config_sha256": _sha256(config_path),
        "preregistration_sha256": _sha256(prereg_path),
        "preflight_sha256": _sha256(preflight_path),
        "source_tree_sha256": source_hash,
        "source_file_count": len(source_files),
        "source_files": source_files,
        "seeds": config["seeds"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run preregistered Phase 13E confirmation")
    parser.add_argument("--confirm", action="store_true", help="run all frozen seeds and write the evidence package")
    args = parser.parse_args()
    if not args.confirm:
        parser.error("confirmation requires explicit --confirm")
    cfg = load_config()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "run_manifest.json"
    frozen_manifest_path = OUT / "frozen_run_manifest.json"
    partial_path = OUT / "partial_results.json"
    if manifest_path.exists() or frozen_manifest_path.exists() or (OUT / "run_records.json").exists():
        raise SystemExit(f"Refusing to overwrite existing Phase 13E artifacts in {OUT}; preserve and inspect them first.")
    manifest = build_manifest(cfg)
    frozen_manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    run: dict[str, Any] = {"experiment_id": cfg["experiment_id"], "config": cfg, "seeds": []}
    try:
        for seed in cfg["seeds"]:
            print(f"Phase 13E confirmation seed {seed} starting", flush=True)
            result = run_seed(int(seed), cfg)
            run["seeds"].append(result)
            partial_path.write_text(json.dumps(run, indent=2, sort_keys=True), encoding="utf-8")
            print(f"Phase 13E confirmation seed {seed} complete", flush=True)
        manifest["status"] = "complete"
        manifest["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
        manifest["completed_seed_count"] = len(run["seeds"])
        write_evidence_package(run, manifest)
        partial_path.unlink(missing_ok=True)
        print(f"Evidence package written: {OUT / 'evidence_package.md'}", flush=True)
    except BaseException as exc:
        manifest["status"] = "incomplete_error"
        manifest["error"] = f"{type(exc).__name__}: {exc}"
        manifest["completed_seed_count"] = len(run["seeds"])
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
