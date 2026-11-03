"""Final QA/provenance builder for the Phase 3A report package."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "reports/experiments/ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1"
REQ = [
    "historical_idt_audit.md", "ranker_validation_report.md",
    "candidate_pool_validation.md", "ranking_pressure_validation.md",
    "endpoint_validation_report.md", "leakage_audit.md", "fairness_audit.md",
    "contract_revalidation_report.md", "phase3A_readiness_review.md",
]
SUPPLEMENTAL = ["mentor_review.md"]
SOURCE_REL = [
    "experiments/phase3a/benchmark_engine.py",
    "experiments/phase3a/run_contracts.py",
    "experiments/phase3a/finalize_package.py",
    "experiments/phase3a/contract_results.json",
    "src/invariants/transfer_aware.py", "src/invariants/ranking.py",
    "src/invariants/validation/scores.py", "src/transfer/metrics.py",
    "experiments/phase1c/ranking_benchmark.py",
    "experiments/phase1c/run_contracts.py",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/phase1C_readiness_report.md",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/ranker_competition_spec.md",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/future_value_definition.md",
    "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/ranking_metrics.md",
    "docs/03_implementation/validation/phase_13b_results.md",
    "docs/03_implementation/validation/phase_13b_exp14_protocol.md",
    "reports/experiments/PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase14b_idt_analysis.md",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    missing = [n for n in REQ + SUPPLEMENTAL if not (PKG / n).is_file() or (PKG / n).stat().st_size == 0]
    if missing:
        raise SystemExit(f"missing required deliverables: {missing}")
    result_path = ROOT / "experiments/phase3a/contract_results.json"
    result = json.loads(result_path.read_text())
    assert result["contracts_passed"] == result["contracts_total"] == 26
    assert result["pressure_panels"] == 100 and result["pressure_all_pass"]
    assert all(result["supplemental_checks"].values())
    readiness = (PKG / "phase3A_readiness_review.md").read_text()
    mentor = (PKG / "mentor_review.md").read_text()
    for token in ("BLOCKED", "not authorized", "six unlock gates", "Phase 3D"):
        if token.lower() not in mentor.lower():
            raise SystemExit(f"mentor disposition missing required content: {token}")
    for q in range(1, 8):
        if f"| {q} |" not in readiness:
            raise SystemExit(f"readiness question {q} missing")
    for token in ("BLOCKED", "outcome store", "Phase 3B", "Phase 3D", "not established"):
        if token.lower() not in readiness.lower():
            raise SystemExit(f"readiness review missing required decision content: {token}")
    # Check local Markdown links in package files (external URLs are not fetched).
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    bad_links = []
    for md in PKG.glob("*.md"):
        for target in link_re.findall(md.read_text()):
            if target.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
                continue
            local = (md.parent / target.split("#", 1)[0]).resolve()
            if not local.exists():
                bad_links.append(f"{md.name}: {target}")
    if bad_links:
        raise SystemExit("broken package links: " + ", ".join(bad_links))
    manifest_path = PKG / "package_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["package_integrity"] = "PASS"
    manifest["qa"] = {
        "required_reports": f"{len(REQ)}/{len(REQ)} present",
        "contracts": "26/26 PASS (synthetic/plumbing scope)",
        "pressure_fixtures": "100/100 PASS; not actual candidate pools",
        "supplemental_checks": result["supplemental_checks"],
        "readiness_questions": "7/7 answered",
        "mentor_review": "concurred; Phase 3B/3D not authorized",
        "unlock_gates": "0/6 closed",
        "markdown_local_links": "PASS",
        "readiness_decision": "BLOCKED for Phase 3B/3D",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    hash_files = [PKG / n for n in REQ + SUPPLEMENTAL + ["README.md", "package_manifest.json"]]
    hash_files += [ROOT / r for r in SOURCE_REL]
    absent_sources = [p.relative_to(ROOT).as_posix() for p in hash_files if not p.is_file()]
    if absent_sources:
        raise SystemExit(f"missing provenance inputs: {absent_sources}")
    provenance = {
        "package_id": manifest["package_id"],
        "sha256": {p.relative_to(ROOT).as_posix(): sha(p) for p in hash_files},
        "counts": {"required_reports": len(REQ), "contracts_passed": 26,
                   "contracts_total": 26, "pressure_panels": 100},
        "scientific_scope": "Synthetic development plumbing only; readiness BLOCKED; no efficacy claim.",
    }
    (PKG / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"package": manifest["package_id"], "qa": manifest["qa"],
                      "hashes": len(hash_files), "provenance": str(PKG / "provenance.json")}, indent=2))


if __name__ == "__main__":
    main()
