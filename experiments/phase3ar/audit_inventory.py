"""Read-only Phase 3A-R inventory builder.

Uses task manifests and test-blind Phase 2B audit rows only. Does not parse ARC
payloads, solver outputs, labels, candidate outcomes, or task test grids.
"""
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "reports/experiments/ASFT-V1.1-PHASE-3A-R-READINESS-REMEDIATION-V1"
DATA = ROOT / "datasets/arc"
P2B = ROOT / "reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/task_stage_outcomes.csv"


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    src = json.loads((DATA / "arc-agi-2/source_manifest.json").read_text())
    split = json.loads((DATA / "arc-agi-2/split_manifest.json").read_text())
    rows2b = {r["task_id"]: r for r in csv.DictReader(P2B.open(newline=""))}
    tasks = split["tasks"]
    ids = [t["task_id"] for t in tasks]
    if len(ids) != len(set(ids)) or len(ids) != src["count"] or set(ids) != set(rows2b):
        raise SystemExit("task manifest/audit ID reconciliation failed")
    registry_path = PKG / "task_registry_inventory.csv"
    fields = ["task_id", "source", "source_commit", "source_file", "source_sha256",
              "historical_split", "train_pairs", "test_pairs", "schema_audit_phase2B",
              "task_family", "difficulty_tier", "target_eligibility",
              "phase3AR_split_assignment", "prior_exposure", "notes"]
    with registry_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for t in sorted(tasks, key=lambda x: x["task_id"]):
            actual = DATA / t["path"]
            if not actual.is_file() or digest(actual) != t["sha256"]:
                raise SystemExit(f"source task hash mismatch: {t['task_id']}")
            audit = rows2b[t["task_id"]]
            if audit["schema_valid"] != "True":
                schema = "FAIL_PHASE2B"
            else:
                schema = "PASS_PHASE2B_TEST_BLIND"
            w.writerow({
                "task_id": t["task_id"], "source": src["repository"],
                "source_commit": src["commit"], "source_file": t["path"],
                "source_sha256": t["sha256"], "historical_split": t["split"],
                "train_pairs": t["train_pairs"], "test_pairs": t["test_pairs"],
                "schema_audit_phase2B": schema,
                "task_family": "UNANNOTATED", "difficulty_tier": "UNSET",
                "target_eligibility": "NOT_ESTABLISHED",
                "phase3AR_split_assignment": "UNASSIGNED",
                "prior_exposure": "YES_PHASE2B_PHASE2C; HOLDOUT ALSO PHASE13G",
                "notes": "Historical ARC task inventory only; not a Phase3A-R locked pool",
            })
    summary = {
        "source_repository": src["repository"], "source_commit": src["commit"],
        "source_manifest_count": src["count"], "registry_rows": len(tasks),
        "historical_split_counts": split["counts"],
        "phase2b_schema_valid_rows": sum(r["schema_valid"] == "True" for r in rows2b.values()),
        "target_eligible_rows": 0,
        "phase3ar_split_assignments": 0,
        "family_annotations": 0,
        "difficulty_annotations": 0,
        "task_files_hash_verified": len(tasks),
        "outcome_access": "not performed; manifest/hash and Phase2B test-blind status only",
        "candidate_registry_rows": 0,
        "candidate_basis": "Phase2E accepted ARC candidates=0 under audited R1 path; Phase1C actual registry absent",
        "task_registry_sha256": digest(registry_path),
    }
    (PKG / "inventory_audit.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
