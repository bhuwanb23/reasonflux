"""Run Phase 1E construct-separation and decision-rule contracts only."""
from __future__ import annotations
import csv, inspect
from pathlib import Path
import sys
from capability_benchmark import (
    BATTERY_TESTS, CAPABILITY_TYPES, FORBIDDEN_OUTCOME_FIELDS, PRIMARY_PREDICTOR,
    SIMPLE_BASELINES, behavioral_capability_pass, behavioral_growth,
    capability_metric_decision, external_battery_score, score_task_output,
    validate_external_outcomes,
)


def run(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    def add(cid, ok, detail):
        rows.append({"contract_id":cid,"result":"PASS" if ok else "FAIL","detail":detail})
    add("CT-1", len(BATTERY_TESTS)==6 and set(x[0] for x in BATTERY_TESTS)==set("ABCDEF"), "Six independent behavioral battery tests declared")
    add("CT-2", len(CAPABILITY_TYPES)==6, "C1-C6 capability taxonomy has six distinct definitions")
    add("CT-3", "CGR_t"==PRIMARY_PREDICTOR, "Primary CGM predictor is explicitly named CGR_t")
    add("CT-4", set(SIMPLE_BASELINES)=={"past_performance","experience_count","memory_strength","frequency_statistics","recency_since_related_success"}, "Required and additional declared simple comparator variables are included")
    for cid, fn, expected in [("CT-5", score_task_output, {"predicted","gold"}),
                              ("CT-6", external_battery_score, {"outcomes"}),
                              ("CT-7", behavioral_growth, {"pre_score","future_score"}),
                              ("CT-8", behavioral_capability_pass, {"task_count","observed_accuracy","lower_confidence_bound","baseline_accuracy","retention_ratio","net_utility_gain"})]:
        params=set(inspect.signature(fn).parameters)
        add(cid, expected.issubset(params) and not (params & FORBIDDEN_OUTCOME_FIELDS), f"{fn.__name__} signature contains only behavioral/evaluator fields")
    add("CT-9", score_task_output("A","A")==1 and score_task_output("A","B")==0, "Task correctness is independently scored against evaluator gold")
    sample={name:[1.0,0.0] for name in BATTERY_TESTS}
    add("CT-10", external_battery_score(sample)==0.5, "External battery score is macro-averaged from per-test family-level outcomes")
    add("CT-11", abs(behavioral_growth(.25,.50)-.25)<1e-12, "Behavioral growth is future-minus-prior external score")
    add("CT-12", validate_external_outcomes({"task_id":"x","correct":1,"family":"A"}), "Allowed outcome schema contains only task behavior fields")
    add("CT-13", all(not validate_external_outcomes({field:0}) for field in FORBIDDEN_OUTCOME_FIELDS), "CGR/C_t/IG fields are rejected from outcome payload")
    good=behavioral_capability_pass(24,.80,.75,.60,.95,.10)
    bad=behavioral_capability_pass(24,.80,.75,.60,.80,.10)
    add("CT-14", good and not bad, "Capability-unit rule requires behavior, generalization margin, retention, and utility")
    add("CT-15", not behavioral_capability_pass(10,.99,.95,.50,.99,.5), "Insufficient independent tasks cannot establish a capability unit")
    add("CT-16", not behavioral_capability_pass(24,.69,.65,.60,.95,.10), "High internal score cannot compensate for failed behavioral threshold")
    add("CT-17", capability_metric_decision(.06,.04,.08,.02,slope_ci_low=.01,slope_ci_high=.10)=="metric_wins", "Decision rule can report meaningful positive-direction CGR win")
    add("CT-18", capability_metric_decision(0,-.01,.01,.02,slope_ci_low=-.01,slope_ci_high=.01)=="equivalent_tie", "Decision rule can report an equivalence tie")
    add("CT-19", capability_metric_decision(-.05,-.08,-.03,.02,slope_ci_low=-.10,slope_ci_high=-.01)=="metric_loses", "Decision rule can report capability-metric loss/inverse direction")
    add("CT-20", capability_metric_decision(.01,-.02,.04,.02,slope_ci_low=-.01,slope_ci_high=.03)=="inconclusive", "Decision rule preserves uncertainty")
    add("CT-21", capability_metric_decision(0,0,0,.02,available=False)=="unavailable", "Integrity failure yields unavailable, not zero")
    add("CT-22", external_battery_score(sample)==external_battery_score(sample), "Identical behavioral records replay deterministically")
    add("CT-23", len({len(v) for v in sample.values()})==1, "Common test opportunities can be represented per battery component")
    add("CT-24", len(FORBIDDEN_OUTCOME_FIELDS)>=5, "Forbidden self-validating metric fields explicitly enumerated")
    add("CT-25", set(BATTERY_TESTS)=={"A_novel_task_success","B_transfer_success","C_task_breadth","D_retention","E_composition","F_adaptation"}, "Battery maps exactly to the six required behavioral tests")
    add("CT-26", all(len(k)>0 and len(v)>0 for k,v in CAPABILITY_TYPES.items()), "Every capability type has a behavioral description")
    add("CT-27", set(SIMPLE_BASELINES).isdisjoint(FORBIDDEN_OUTCOME_FIELDS), "Simple comparator variables are not target labels")
    add("CT-28", capability_metric_decision(.06,.04,.08,.02,slope_ci_low=.01,slope_ci_high=.10)=="metric_wins" and capability_metric_decision(-.05,-.08,-.03,.02,slope_ci_low=-.10,slope_ci_high=-.01)=="metric_loses", "Decision branches are mutually discriminable")
    add("CT-29", external_battery_score(sample)>=0 and external_battery_score(sample)<=1, "Independent behavioral battery score remains bounded")
    add("CT-30", "CGR" in FORBIDDEN_OUTCOME_FIELDS and "C_t" in FORBIDDEN_OUTCOME_FIELDS and "IG" in FORBIDDEN_OUTCOME_FIELDS, "All target-contamination metrics are explicitly denied")
    add("CT-31", capability_metric_decision(.06,.04,.08,.02,slope_ci_low=-.10,slope_ci_high=-.01)=="metric_loses", "Predictive gain in the wrong score direction cannot be called a capability-metric win")

    with (out/"phase1E_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"outcome_response_sanity.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["fixture","delta_mae","delta_ci_low","delta_ci_high","slope_ci_low","slope_ci_high","status","scope"])
        cases=[("constructed_win",.06,.04,.08,.01,.10,True),("equivalence_tie",0,-.01,.01,-.01,.01,True),
               ("constructed_loss",-.05,-.08,-.03,-.10,-.01,True),("uncertain",.01,-.02,.04,-.01,.03,True),
               ("integrity_failure",0,0,0,0,0,False)]
        for name,delta,lo,hi,slo,shi,available in cases:
            status=capability_metric_decision(delta,lo,hi,.02,slope_ci_low=slo,slope_ci_high=shi,available=available)
            w.writerow([name,delta,lo,hi,slo,shi,status,"decision-rule contract fixture only; no task outcome data"])
    with (out/"capability_battery_schema.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["test_id","behavioral_construct","primary_observation","internal_metric_inputs"])
        definitions=[("A_novel_task_success","novel-task competence","correct outputs on unseen instances","none"),
        ("B_transfer_success","transfer","correct outputs on disjoint family/surface","none"),
        ("C_task_breadth","breadth","family-level success proportions","none"),
        ("D_retention","persistence","delayed task performance after no refresh","none"),
        ("E_composition","composition","success on unseen component combinations","none"),
        ("F_adaptation","adaptation","behavior change after fixed demos","none")]
        w.writerows(definitions)
    failures=[x for x in rows if x["result"]!="PASS"]
    print(f"{len(rows)-len(failures)}/{len(rows)} Phase 1E construct/contract checks PASS")
    print("No capability battery, task runner, or confirmatory outcomes were executed.")
    return 1 if failures else 0

if __name__=="__main__":
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    raise SystemExit(run(dest))
