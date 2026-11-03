"""QA/provenance finalizer for the Phase 2I program specification."""
from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-INVARIANT-CANDIDATE-PRODUCTION-V1"
REPORTS=["candidate_production_protocol.md","candidate_eligibility_contract.md","representation_and_trace_plan.md","data_and_annotation_plan.md","candidate_source_and_yield_baseline.md","decision_rules.md","phase2I_readiness_review.md"]
ARTIFACTS=["README.md","condition_matrix.csv","candidate_registry_schema.csv","preflight_gate_matrix.csv","package_manifest.json"]
SOURCES=[
 "experiments/phase2i/finalize_package.py",
 "reports/experiments/ASFT-V1.1-PHASE-2H-CANDIDATE-POPULATION-READINESS-V1/phase2H_readiness_review.md",
 "reports/experiments/ASFT-V1.1-PHASE-2H-CANDIDATE-POPULATION-READINESS-V1/candidate_yield_audit.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2H-CANDIDATE-POPULATION-READINESS-V1/yield_summary.json",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/representation_registry.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/phase2F_framework_config.json",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/coverage_comparison_framework.md",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/phase2F_readiness_review.md",
 "reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/invariant_readiness_audit.md",
 "reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/trace_yield_report.md",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/recurrence_summary.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1/phase2G_integrated_manifest.json",
 "reports/experiments/ASFT-V1.1-PHASE-3A-R-READINESS-REMEDIATION-V1/phase3A-R_readiness_review.md",
 "src/invariants/detector.py","src/invariants/candidate_generation.py",
 "src/invariants/pattern_mining.py","src/invariants/specification/identity.py",
 "src/invariants/specification/policy.py","src/invariants/specification/rejection.py",
 "src/invariants/specification/qualification.py","src/traces/segmentation.py",
 "src/invariants/ranking.py","src/pipelines/invariant_pipeline.py",
]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    missing=[n for n in REPORTS+ARTIFACTS if not (PKG/n).is_file() or not (PKG/n).stat().st_size]
    if missing: raise SystemExit(f"missing files: {missing}")
    gates=list(csv.DictReader((PKG/"preflight_gate_matrix.csv").open(newline="")))
    assert len(gates)==8
    assert not (PKG/"candidate_registry_schema.csv").read_text().strip().splitlines()[1:]
    decision=(PKG/"phase2I_readiness_review.md").read_text().lower()
    for token in ("blocked", "not run", "phase 3b", "phase 3d", "invariant candidate"):
        if token not in decision: raise SystemExit(f"readiness missing: {token}")
    for token in ("r1", "r3", "support", "family", "trace"):
        if token not in (PKG/"candidate_production_protocol.md").read_text().lower():
            raise SystemExit(f"protocol missing: {token}")
    link_re=re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    bad=[]
    for md in PKG.glob("*.md"):
      for target in link_re.findall(md.read_text()):
        if target.startswith(("http://","https://","mailto:","#")): continue
        if not (md.parent/target.split("#",1)[0]).exists(): bad.append(f"{md.name}: {target}")
    if bad: raise SystemExit(f"broken links: {bad}")
    mp=PKG/"package_manifest.json"
    m=json.loads(mp.read_text())
    m["package_integrity"]="PASS"
    m["qa"]={"reports":"7/7 present","registered_conditions":"R1/R3 development comparison; HCC excluded from ARC yield",
       "candidate_registry":"schema only; zero data rows","preflight_gates":"8 documented; execution blocked",
       "new_candidate_run":"NOT RUN","local_markdown_links":"PASS",
       "decision":"Phase 2I program specified; execution blocked; Phase 3 remains blocked"}
    mp.write_text(json.dumps(m,indent=2)+"\n")
    files=[PKG/n for n in REPORTS+ARTIFACTS]+[ROOT/p for p in SOURCES]
    missing=[p.relative_to(ROOT).as_posix() for p in files if not p.is_file()]
    if missing: raise SystemExit(f"missing provenance inputs: {missing}")
    prov={"package_id":m["package_id"],"sha256":{p.relative_to(ROOT).as_posix():sha(p) for p in files},
      "counts":{"reports":7,"registered_arms":2,"candidate_rows":0,"preflight_gates":8},
      "scope":"Program specification only; no Phase2I search/candidate generation/outcome scoring run.",
      "decision":"Execution blocked; no Phase3B/Phase3D authorization."}
    (PKG/"provenance.json").write_text(json.dumps(prov,indent=2)+"\n")
    print(json.dumps({"package":m["package_id"],"qa":m["qa"],"sha256_entries":len(files),"provenance":str(PKG/"provenance.json")},indent=2))
if __name__=="__main__": main()
