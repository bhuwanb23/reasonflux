"""Run Phase 1H baseline/ablation/fairness/decision contracts only."""
from __future__ import annotations
import csv,sys
from pathlib import Path
from competition_framework import (
    ABLATIONS, BASELINE_TAXONOMY, CLAIM_ABLATION_MAP, FAIRNESS_DIMENSIONS,
    MANDATORY_BASELINES, ablation_contribution_decision,
    baseline_comparison_decision, comparator_activation_status, fairness_status,
    gated_comparison_decision, governance_status,
)


def run(out: Path) -> int:
    out.mkdir(parents=True,exist_ok=True);rows=[]
    def add(cid,ok,detail):rows.append({"contract_id":cid,"result":"PASS" if ok else "FAIL","detail":detail})
    add("1H-CT-01",len(BASELINE_TAXONOMY)==7,"B1-B7 comparator taxonomy declared")
    add("1H-CT-02",set(BASELINE_TAXONOMY)=={"B1_NO_LEARNING","B2_MEMORY_RETRIEVAL","B3_RANDOM","B4_FREQUENCY","B5_COMPRESSION","B6_HEURISTIC_HYBRID","B7_ORACLE"},"All baseline families named")
    add("1H-CT-03",len(MANDATORY_BASELINES)==7,"Seven mandatory baseline slots declared")
    add("1H-CT-04",set(MANDATORY_BASELINES)=={"BL1_NO_LEARNING","BL2_MEMORY_RETRIEVAL","BL3_RANDOM","BL4_FREQUENCY","BL5_COMPRESSION","BL6_HYBRID_MEMORY_FREQUENCY","BL7_ORACLE_ANALYSIS_ONLY"},"Mandatory baselines include no-learning, memory, random, frequency, compression, hybrid, oracle")
    add("1H-CT-05","BL6_HYBRID_MEMORY_FREQUENCY" in MANDATORY_BASELINES,"Hybrid memory+frequency is an explicit comparator")
    add("1H-CT-06","BL7_ORACLE_ANALYSIS_ONLY" in MANDATORY_BASELINES,"Oracle is explicitly analysis-only")
    add("1H-CT-07",len(ABLATIONS)==9,"A1-A9 component ablations declared")
    add("1H-CT-08",set(ABLATIONS)=={"A1_NO_IDT","A2_NO_SCT","A3_NO_SCV","A4_NO_TRANSFER","A5_NO_CAPABILITY_LAYER","A6_NO_LIFECYCLE","A7_NO_COMPOSITION","A8_NO_MEMORY","A9_NO_ARC_EXTENSION"},"All required ablation families are explicit")
    add("1H-CT-09",set(CLAIM_ABLATION_MAP.values())=={(a,) for a in ABLATIONS},"Every major claim maps to a distinct required removal test")
    add("1H-CT-10",len(FAIRNESS_DIMENSIONS)==9,"Fairness checklist contains tasks, pool, budgets, storage, compute, horizon, exposure, evaluator, config parity")
    checks={k:True for k in FAIRNESS_DIMENSIONS}
    add("1H-CT-11",fairness_status(checks)=="pass","Fully matched comparison passes fairness gate")
    bad=dict(checks);bad["same_tasks"]=False
    add("1H-CT-12",fairness_status(bad)=="fail","Task mismatch fails fairness gate")
    bad=dict(checks);bad["same_candidate_pool"]=False
    add("1H-CT-13",fairness_status(bad)=="fail","Candidate-pool mismatch fails fairness gate")
    bad=dict(checks);bad["same_budget"]=False
    add("1H-CT-14",fairness_status(bad)=="fail","Budget mismatch fails fairness gate")
    unknown=dict(checks);unknown["same_horizon"]=None
    add("1H-CT-15",fairness_status(unknown)=="unavailable","Missing fairness evidence is unavailable, not pass")
    fail_unknown=dict(checks);fail_unknown["same_budget"]=False;fail_unknown["same_evaluator"]=None
    add("1H-CT-16",fairness_status(fail_unknown)=="fail","Known fairness violation dominates unknown audit fields")
    same={"ASFT":["a","b","c"],"freq":["a","b","c"],"random":["a","b","c"]};opp={k:3 for k in same}
    add("1H-CT-17",comparator_activation_status(same,opp)=="non_informative_identical_decisions","Identical comparator decisions are flagged non-informative")
    diff={"ASFT":["a","c","b"],"freq":["a","b","c"],"random":["c","b","a"]}
    add("1H-CT-18",comparator_activation_status(diff,opp)=="informative_decision_divergence","Divergent decisions create an informative selection comparison")
    add("1H-CT-19",comparator_activation_status(same,opp,common_candidate_pool=False)=="unmatched_candidate_pool","Unmatched candidate pools cannot support direct ranking attribution")
    add("1H-CT-20",comparator_activation_status(same,{"ASFT":3,"freq":2,"random":3})=="unmatched_opportunities","Different opportunity counts are explicitly flagged")
    add("1H-CT-21",comparator_activation_status(same,{k:0 for k in same})=="unavailable","No eligible opportunities are unavailable")
    add("1H-CT-22",comparator_activation_status({"ASFT":["a"],"freq":["a"]},{"ASFT":1})=="unavailable","Missing comparator records cannot be treated as a win")
    add("1H-CT-23",comparator_activation_status({"ASFT":["a"],"freq":["a","b"]},{"ASFT":2,"freq":2})=="unmatched_decision_horizon","Different decision horizons are flagged")
    add("1H-CT-24",baseline_comparison_decision(.06,.04,.08,.02)=="asft_wins","ASFT win path exists")
    add("1H-CT-25",baseline_comparison_decision(-.06,-.08,-.04,.02)=="baseline_wins","Alternative baseline win path exists")
    add("1H-CT-26",baseline_comparison_decision(0,-.01,.01,.02)=="equivalent_tie","Equivalent tie path exists")
    add("1H-CT-27",baseline_comparison_decision(.01,-.02,.04,.02)=="inconclusive","Uncertain comparison remains inconclusive")
    add("1H-CT-28",baseline_comparison_decision(0,0,0,.02,available=False)=="unavailable","Unavailable endpoint is not coded zero")
    add("1H-CT-29",ablation_contribution_decision(.06,.04,.08,.02)=="positive_contribution_under_tested_conditions","Ablation can show positive local component contribution")
    add("1H-CT-30",ablation_contribution_decision(0,-.01,.01,.02)=="no_measurable_contribution_under_tested_conditions","Ablation can remove a component without a measurable outcome change")
    add("1H-CT-31",ablation_contribution_decision(-.06,-.08,-.04,.02)=="negative_contribution_ablation_better_under_tested_conditions","Ablation can reveal a component harms the tested endpoint")
    add("1H-CT-32",ablation_contribution_decision(0,0,0,.02,manipulation_verified=False)=="unavailable","Unverified removal cannot establish a null contribution")
    add("1H-CT-33",ablation_contribution_decision(0,0,0,.02,available=False)=="unavailable","Missing ablation outcome remains unavailable")
    add("1H-CT-34",ablation_contribution_decision(.01,-.03,.03,.02)=="inconclusive","Abstaining/uncertain component effect is allowed")
    gov=dict(preregistered=True,config_locked_before_outcomes=True,endpoints_locked_before_outcomes=True,splits_locked_before_outcomes=True,no_posthoc_changes=True)
    add("1H-CT-35",governance_status(**gov)=="pass","Frozen governance checklist passes when all commitments verified")
    bad=dict(gov);bad["config_locked_before_outcomes"]=False
    add("1H-CT-36",governance_status(**bad)=="fail","Post-outcome config change fails governance")
    bad=dict(gov);bad["endpoints_locked_before_outcomes"]=False
    add("1H-CT-37",governance_status(**bad)=="fail","Endpoint drift fails governance")
    bad=dict(gov);bad["splits_locked_before_outcomes"]=False
    add("1H-CT-38",governance_status(**bad)=="fail","Split changes fail governance")
    bad=dict(gov);bad["no_posthoc_changes"]=None
    add("1H-CT-39",governance_status(**bad)=="unavailable","Unknown posthoc-change audit is unavailable")
    add("1H-CT-40",all(bool(v) for v in BASELINE_TAXONOMY.values()),"Every baseline family has an interpretation boundary")
    add("1H-CT-41",("A2_NO_SCT",) in CLAIM_ABLATION_MAP.values() and ("A3_NO_SCV",) in CLAIM_ABLATION_MAP.values(),"SCT formation and SCV selection require distinct ablations")
    add("1H-CT-42",len(rows)+9==50,"Contract suite has a fixed declared count")
    add("1H-CT-43",baseline_comparison_decision(.03,.021,.04,.02)=="asft_wins" and baseline_comparison_decision(-.03,-.04,-.021,.02)=="baseline_wins","Decision rule does not structurally favor ASFT")
    add("1H-CT-44",comparator_activation_status({"ASFT":["x"]},{"ASFT":4})=="unavailable","A single-arm result is not a comparator victory")
    add("1H-CT-45",all(a in ABLATIONS for vals in CLAIM_ABLATION_MAP.values() for a in vals),"Claim-to-ablation registry references only declared ablations")
    add("1H-CT-46",gated_comparison_decision(.06,.04,.08,"pass","informative_decision_divergence")=="asft_wins","Attribution permits a win only after fair, divergent comparison")
    add("1H-CT-47",gated_comparison_decision(.06,.04,.08,"pass","non_informative_identical_decisions")=="non_informative_comparison","Identical choices block a mechanism win label")
    add("1H-CT-48",gated_comparison_decision(.06,.04,.08,"fail","informative_decision_divergence")=="comparison_invalid","Unfair comparisons cannot be attributed even with favorable numbers")
    add("1H-CT-49",gated_comparison_decision(.06,.04,.08,"pass","unmatched_opportunities")=="comparison_invalid","Opportunity mismatch prevents direct attribution")
    add("1H-CT-50",comparator_activation_status({"A":[1,0],"B":[0,1]},{"A":3,"B":3})=="unmatched_decision_horizon","Decision-vector lengths must match eligible-opportunity counts")

    with (out/"phase1H_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"phase1H_registry_schema.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["registry_type","code","definition_or_claim","mandatory","interpretation_boundary"])
        for code,desc in BASELINE_TAXONOMY.items():w.writerow(["baseline_taxonomy",code,desc,code!="B7_ORACLE","Implementation subtype and endpoint frozen per experiment"])
        for code in MANDATORY_BASELINES:w.writerow(["mandatory_baseline",code,code,True,"Same opportunity/budget rules; oracle remains analysis-only"])
        for claim,ablations in CLAIM_ABLATION_MAP.items():
            for a in ablations:w.writerow(["claim_ablation",a,claim,True,"Local effect only; necessity is not universal"])
    with (out/"outcome_response_sanity.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["fixture","decision_or_status","scope"])
        vals=[("constructed_asft_win",baseline_comparison_decision(.06,.04,.08,.02)),
        ("constructed_tie",baseline_comparison_decision(0,-.01,.01,.02)),
        ("constructed_baseline_win",baseline_comparison_decision(-.06,-.08,-.04,.02)),
        ("constructed_inconclusive",baseline_comparison_decision(.01,-.02,.04,.02)),
        ("integrity_unavailable",baseline_comparison_decision(0,0,0,.02,available=False)),
        ("component_positive",ablation_contribution_decision(.06,.04,.08,.02)),
        ("component_no_measurable_effect",ablation_contribution_decision(0,-.01,.01,.02)),
        ("component_negative",ablation_contribution_decision(-.06,-.08,-.04,.02)),
        ("identical_decisions",comparator_activation_status(same,opp)),
        ("noninformative_cannot_become_win",gated_comparison_decision(.06,.04,.08,"pass","non_informative_identical_decisions")),
        ("unfair_comparison_invalid",gated_comparison_decision(.06,.04,.08,"fail","informative_decision_divergence"))]
        for name,status in vals:w.writerow([name,status,"constructed contract fixture only; no experiment outcomes"])
    failures=[r for r in rows if r["result"]!="PASS"]
    print(f"{len(rows)-len(failures)}/{len(rows)} Phase 1H competition-governance contracts PASS")
    print("No baseline, ablation, task, or confirmatory outcome was generated or analyzed.")
    return 1 if failures else 0

if __name__=="__main__":
    dst=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    raise SystemExit(run(dst))
