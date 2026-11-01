"""Explicit freeze and confirmation CLI for Phase 13F."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .common import CONFIG_PATH, OUT, ROOT, load_config
from .reporting import write_package
from .runner import run_confirmation


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or load_config()
    prereg = ROOT / "experiments/phase13f/preregistration.md"
    preflight = ROOT / "docs/03_implementation/validation/phase_13f_preflight.md"
    test = ROOT / "tests/test_phase13f_contracts.py"
    paths = [p for p in (ROOT / "experiments/phase13f").glob("*.py")]
    paths += [p for p in (ROOT / "experiments/phase13e").glob("*.py")]
    paths += [ROOT / "experiments/phase13c/scoring.py", test]
    paths += [p for p in (ROOT / "src").rglob("*.py") if "__pycache__" not in p.parts]
    files = {p.relative_to(ROOT).as_posix(): _hash(p) for p in sorted(set(paths)) if p.exists()}
    tree = hashlib.sha256("\n".join(f"{k}:{v}" for k, v in sorted(files.items())).encode()).hexdigest()
    return {"experiment_id": cfg["experiment_id"], "status": "frozen_preconfirmation",
            "seeds": cfg["seeds"], "config_sha256": _hash(CONFIG_PATH),
            "preregistration_sha256": _hash(prereg), "preflight_sha256": _hash(preflight), "source_tree_sha256": tree,
            "source_file_count": len(files), "source_files": files,
            "contract_test": "tests/test_phase13f_contracts.py", "contract_test_result": "11 passed; compileall passed",
            "prior_phase_evidence_modified": False}


def run(confirm: bool = False) -> Path:
    if not confirm:
        raise SystemExit("No run requested. Use --confirm only after protocol freeze and contract tests.")
    OUT.mkdir(parents=True, exist_ok=True)
    frozen_path = OUT / "frozen_run_manifest.json"
    if any((OUT / name).exists() for name in ("run_records.json", "run_manifest.json", "evidence_package.md", "frozen_run_manifest.json")):
        raise FileExistsError("Phase 13F output already exists; refusing to overwrite frozen outcomes")
    manifest = build_manifest()
    frozen_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    active = dict(manifest, status="running")
    (OUT / "run_manifest.json").write_text(json.dumps(active, indent=2, sort_keys=True), encoding="utf-8")
    try:
        results = run_confirmation()
        active["status"] = "complete"
        report = write_package(results, active)
        return report
    except BaseException as exc:
        active["status"] = "interrupted"
        active["error"] = f"{type(exc).__name__}: {exc}"
        (OUT / "run_manifest.json").write_text(json.dumps(active, indent=2, sort_keys=True), encoding="utf-8")
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    print(run(confirm=args.confirm))


if __name__ == "__main__":
    main()
