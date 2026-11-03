"""Final QA and provenance for Phase 3A-R remediation package."""
from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "reports/experiments/ASFT-V1.1-PHASE-3A-R-READINESS-REMEDIATION-V1"
REPORTS = [
    "candidate_pool_qualification.md", "task_pool_qualification.md",
    "feature_lineage_freeze.md", "actual_pool_pressure_report.md",
    "fntu_evaluator_validation.md", "sealed_outcome_store_audit.md",
    "power_precision_plan.md", "phase3A-R_readiness_review.md",
]
ARTIFACTS = [
    "candidate_registry_template.csv", "task_registry_inventory.csv",
    "split_assignment_template.csv", "feature_lineage_matrix.csv",
    "feature_source_hashes.csv", "actual_pool_pressure_matrix.csv",
    "inventory_audit.json", "README.md", "package_manifest.json",
]
SOURCES = [
    "experiments/phase3ar/audit_inventory.py",
    "experiments/phase3ar/finalize_package.py",
    "datasets/arc/arc-agi-2/source_manifest.json",
    "datasets/arc/arc-agi-2/split_manifest.json",
    "reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/task_stage_outcomes.csv",
    "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.csv",
    "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.md",
    "reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/candidate_trial_log.csv",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/ranker_competition_spec.md",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/ranking_dataset_protocol.md",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/future_value_definition.md",
    "reports/experiments/ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1/mentor_review.md",
    "reports/experiments/ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1/phase3A_readiness_review.md",
    "src/invariants/validation/frequency.py", "src/invariants/validation/consistency.py",
    "src/invariants/validation/generality.py", "src/invariants/validation/reasoning_value.py",
    "src/invariants/transfer_aware.py", "src/transfer/metrics.py", "src/invariants/ranking.py",
    "experiments/phase3a/benchmark_engine.py",
    "reports/experiments/PHASE-13D-TRANSFER-V1/posthoc_analysis.md",
]

def sha(p: Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> None:
    missing = [n for n in REPORTS + ARTIFACTS if not (PKG/n).is_file() or not (PKG/n).stat().st_size]
    if missing: raise SystemExit(f"missing deliverables: {missing}")
    inv = json.loads((PKG/"inventory_audit.json").read_text())
    assert inv["registry_rows"] == inv["task_files_hash_verified"] == 1000
    assert inv["candidate_registry_rows"] == inv["target_eligible_rows"] == 0
    assert inv["phase3ar_split_assignments"] == inv["family_annotations"] == inv["difficulty_annotations"] == 0
    with (PKG/"actual_pool_pressure_matrix.csv").open(newline="") as f:
        pressure = list(csv.DictReader(f))
    assert len(pressure) == 10 and all(r["status"] == "NOT_COMPUTABLE" for r in pressure)
    readiness = (PKG/"phase3A-R_readiness_review.md").read_text().lower()
    for gate in range(1,7):
        if f"{gate}. " not in readiness and f"gate {gate}" not in readiness:
            raise SystemExit(f"readiness review does not enumerate Gate {gate}")
    for phrase in ("blocked", "not authorized", "phase 3b", "phase 3d", "feature", "not computable"):
        if phrase not in readiness: raise SystemExit(f"readiness missing {phrase}")
    feature = (PKG/"feature_lineage_freeze.md").read_text().lower()
    if "conflict" not in feature or "coverage" not in feature or "generality" not in feature or "reasoning value" not in feature:
        raise SystemExit("R1 / Phase3A-R feature semantic conflict not documented")
    # Local Markdown links only.
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    bad=[]
    for md in PKG.glob("*.md"):
        for target in link_re.findall(md.read_text()):
            if target.startswith(("http://","https://","mailto:","#")): continue
            if not (md.parent/target.split("#",1)[0]).exists(): bad.append(f"{md.name}: {target}")
    if bad: raise SystemExit(f"broken links: {bad}")
    manifest_path=PKG/"package_manifest.json"
    manifest=json.loads(manifest_path.read_text())
    manifest["qa"]={
        "reports":"8/8 present",
        "task_manifest_reconciliation":"1000/1000 task hashes verified; inventory only",
        "candidate_registry":"0 eligible actual candidates; no fabricated rows",
        "pressure_matrix":"10/10 comparisons NOT_COMPUTABLE, correctly fail-closed",
        "feature_semantic_conflict":"documented; no silent R1 change",
        "split_assignment":"0; C1-C4 not assigned",
        "local_markdown_links":"PASS",
        "readiness":"BLOCKED; Phase 3B/3D not authorized",
    }
    manifest_path.write_text(json.dumps(manifest,indent=2)+"\n")
    files=[PKG/n for n in REPORTS+ARTIFACTS]
    files += [ROOT/p for p in SOURCES]
    absent=[p.relative_to(ROOT).as_posix() for p in files if not p.is_file()]
    if absent: raise SystemExit(f"missing provenance sources: {absent}")
    provenance={
        "package_id":manifest["package_id"],
        "sha256":{p.relative_to(ROOT).as_posix():sha(p) for p in files},
        "task_file_hashes_in_inventory":1000,
        "scope":"Read-only readiness remediation; no outcome scoring, calibration, or efficacy run.",
        "decision":"BLOCKED; six gates not closed.",
    }
    (PKG/"provenance.json").write_text(json.dumps(provenance,indent=2)+"\n")
    print(json.dumps({"package":manifest["package_id"],"qa":manifest["qa"],"sha256_entries":len(files),"provenance":str(PKG/"provenance.json")},indent=2))
if __name__=="__main__": main()
