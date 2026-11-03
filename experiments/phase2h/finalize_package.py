"""Phase 2H QA and provenance finalizer."""
from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2H-CANDIDATE-POPULATION-READINESS-V1"
REPORTS=["candidate_source_audit.md","candidate_yield_audit.md","candidate_eligibility_rules.md","alternative_candidate_sources.md","benchmark_feasibility_decision.md","phase2H_readiness_review.md"]
ARTIFACTS=["README.md","candidate_source_audit.csv","candidate_yield_audit.csv","candidate_registry_template.csv","yield_summary.json","package_manifest.json"]
SOURCES=[
 "experiments/phase2h/build_audit.py","experiments/phase2h/finalize_package.py",
 "src/core/invariant.py","src/core/trace.py","src/invariants/detector.py",
 "src/invariants/pattern_mining.py","src/invariants/aggregation.py",
 "src/invariants/candidate_generation.py","src/invariants/specification/identity.py",
 "src/invariants/specification/policy.py","src/invariants/specification/qualification.py",
 "src/invariants/specification/rejection.py","src/invariants/promotion.py",
 "src/invariants/validator.py","src/invariants/ranking.py",
 "src/skills/candidate.py","src/skills/intake.py","src/skills/qualification.py",
 "src/skills/pipeline.py","src/pipelines/invariant_pipeline.py","src/pipelines/skill_pipeline.py",
 "src/traces/segmentation.py",
 "reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/task_stage_outcomes.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/phase2B_readiness_review.md",
 "reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/invariant_readiness_audit.md",
 "reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/trace_yield_report.md",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.md",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_and_validation_details.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/recurrence_summary.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/recurrence_benchmark.md",
 "reports/experiments/ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1/representation_hypothesis_status.md",
 "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/ranker_competition_spec.md",
 "reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1/phase1C_full_audit_report.md",
 "reports/experiments/ASFT-V1.1-PHASE-3A-R-READINESS-REMEDIATION-V1/phase3A-R_readiness_review.md",
]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    absent=[n for n in REPORTS+ARTIFACTS if not (PKG/n).is_file() or not (PKG/n).stat().st_size]
    if absent: raise SystemExit(f"missing deliverables: {absent}")
    rows=list(csv.DictReader((PKG/"candidate_yield_audit.csv").open(newline="")))
    summ=json.loads((PKG/"yield_summary.json").read_text())
    if len(rows)!=15 or summ["accepted_invariant_candidates_total_across_condition_rows"]!=0:
        raise SystemExit("yield audit does not confirm all 15 rows / zero accepted")
    if summ["unique_proposal_ids_in_relaxed_rows"]!=["INV-403ef00057eafb52","INV-6b9c0646e32acc5d"]:
        raise SystemExit("relaxed proposal IDs not reconciled")
    if sum(int(r["accepted_candidates"]) for r in rows)!=0:
        raise SystemExit("unexpected accepted candidate in yield rows")
    decision=(PKG/"phase2H_readiness_review.md").read_text().lower()
    for token in ("f2", "phase 3 remains blocked", "zero accepted", "not universal falsification"):
        if token not in decision: raise SystemExit(f"readiness review missing {token}")
    link_re=re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    bad=[]
    for md in PKG.glob("*.md"):
        for t in link_re.findall(md.read_text()):
            if t.startswith(("http://","https://","mailto:","#")): continue
            if not (md.parent/t.split("#",1)[0]).exists(): bad.append(f"{md.name}: {t}")
    if bad: raise SystemExit(f"broken links: {bad}")
    mp=PKG/"package_manifest.json"
    m=json.loads(mp.read_text())
    m["package_integrity"]="PASS"
    m["qa"]={"reports":"6/6 present","candidate_yield_rows":"15/15 reconciled",
      "accepted_invariant_candidates":0,"unique_relaxed_proposal_ids":2,
      "proposal_disposition":"all rejected; no candidate population",
      "candidate_registry":"template only; 0 rows","markdown_links":"PASS",
      "decision":"F2 current invariant path; Phase 3 blocked; F3 alternative not adopted"}
    mp.write_text(json.dumps(m,indent=2)+"\n")
    files=[PKG/n for n in REPORTS+ARTIFACTS]+[ROOT/x for x in SOURCES]
    missing=[p.relative_to(ROOT).as_posix() for p in files if not p.is_file()]
    if missing: raise SystemExit(f"missing hash inputs: {missing}")
    prov={"package_id":m["package_id"],"sha256":{p.relative_to(ROOT).as_posix():sha(p) for p in files},
      "counts":{"reports":6,"yield_rows":15,"accepted_candidates":0,"distinct_relaxed_proposal_ids":2},
      "scope":"Retrospective saved-artifact/source audit only; no candidate generation, outcome scoring, or Phase 3 execution.",
      "feasibility":"F2 for current audited invariant candidate path; F3 not adopted."}
    (PKG/"provenance.json").write_text(json.dumps(prov,indent=2)+"\n")
    print(json.dumps({"package":m["package_id"],"qa":m["qa"],"sha256_entries":len(files),"provenance":str(PKG/"provenance.json")},indent=2))
if __name__=="__main__":main()
