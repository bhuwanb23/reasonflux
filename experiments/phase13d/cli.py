"""Hash-freeze and execute the preregistered ten-seed confirmation run."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from .common import ROOT, OUT_DIR, CONFIG_PATH, load_config
from .reporting import write_package
from .runner import aggregate, run_seed

PROTOCOL = ROOT / "docs/03_implementation/validation/phase_13d_preregistration_v1.md"
PREFLIGHT = ROOT / "docs/03_implementation/validation/phase_13d_preflight.md"


def source_files() -> list[Path]:
    paths = [*Path(ROOT / "experiments/phase13d").glob("*.py"),
             ROOT / "experiments/phase13c/scoring.py", ROOT / "experiments/phase13c/common.py",
             ROOT / "experiments/phase13c/tasking.py", ROOT / "tests/test_phase13d_contracts.py",
             CONFIG_PATH, PROTOCOL, PREFLIGHT]
    paths.extend((ROOT / "src").rglob("*.py"))
    return sorted({p.resolve() for p in paths if p.is_file()})


def build_manifest() -> dict[str, Any]:
    entries = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in source_files()}
    root_hash = hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"manifest_version": 1, "algorithm": "sha256", "files": entries, "root_sha256": root_hash}


def verify_manifest() -> dict[str, Any]:
    path = OUT_DIR / "preregistration_hashes.json"
    if not path.exists():
        raise SystemExit("No hash freeze found. Run --freeze only after reviewing the preregistration.")
    frozen = json.loads(path.read_text(encoding="utf-8"))
    current = build_manifest()
    if frozen != current:
        raise SystemExit("Frozen source/config/protocol hash mismatch; do not run. Create a new version and untouched seed set.")
    return frozen


def run_contract_tests() -> None:
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/test_phase13d_contracts.py"],
                            cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit("Contract tests failed; no freeze or benchmark run performed.")


def freeze() -> None:
    run_contract_tests()
    config = load_config()
    if config.get("experiment", {}).get("status") != "frozen_pre_run":
        raise SystemExit("Config status is not frozen_pre_run; refusing hash freeze.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()
    (OUT_DIR / "preregistration_hashes.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Frozen {len(manifest['files'])} source/config/protocol files; SHA-256 {manifest['root_sha256']}")
    print(f"Manifest: {OUT_DIR / 'preregistration_hashes.json'}")


def run() -> None:
    frozen = verify_manifest()
    run_contract_tests()
    config = load_config()
    seeds = list(config["seeds"]["confirmation"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seed_results = []
    for seed in seeds:
        checkpoint = OUT_DIR / f"seed_{seed}.json"
        if checkpoint.exists():
            result = json.loads(checkpoint.read_text(encoding="utf-8"))
            if (int(result.get("run_seed", -1)) != int(seed)
                    or result.get("frozen_root_sha256") != frozen["root_sha256"]):
                raise SystemExit(f"Invalid or mismatched-hash checkpoint: {checkpoint}")
            seed_results.append(result)
            print(f"seed {seed}: loaded completed checkpoint")
            continue
        result = run_seed(int(seed), config)
        result["frozen_root_sha256"] = frozen["root_sha256"]
        checkpoint.write_text(json.dumps(result, sort_keys=True, default=str) + "\n", encoding="utf-8")
        seed_results.append(result)
        print(f"seed {seed}: complete ({len(result['task_rows'])} task/policy rows)")
    aggregate_results = aggregate(seed_results)
    write_package(seed_results, aggregate_results, frozen)
    print(f"Results package: {OUT_DIR / 'phase13d_results.md'}")
    print("All outcomes are empirical; inspect criteria.json rather than assuming success.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--freeze", action="store_true", help="run stub-only contracts and freeze source/config/protocol hashes")
    group.add_argument("--run", action="store_true", help="run the preregistered ten-seed confirmation after hash verification")
    args = parser.parse_args()
    if args.freeze:
        freeze()
    else:
        run()


if __name__ == "__main__":
    main()
