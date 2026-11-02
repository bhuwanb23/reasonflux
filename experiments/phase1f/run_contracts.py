"""Run Phase 1F construct-separation, inference, and retirement contracts only."""
from __future__ import annotations
import csv, inspect, sys
from pathlib import Path
from intelligence_benchmark import (
    BATTERY_TESTS, FORBIDDEN_TARGET_FIELDS, INTELLIGENCE_TYPES, KEY_SECONDARY_PREDICTOR,
    LEARNING_EXPOSURES, PRIMARY_ENDPOINT, PRIMARY_PREDICTOR, PRIMARY_SOI, RANDOM_BASELINE, SIMPLE_BASELINES,
    behavioral_delta, ig_predictive_decision, intelligence_claim_decision,
    learning_curve_auc, score_task_output, validate_external_outcomes,
)


def run(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    def add(cid, ok, detail):
        rows.append({"contract_id":cid,"result":"PASS" if ok else "FAIL","detail":detail})
    add("IF-CT-01",len(BATTERY_TESTS)==6,"Six independently scored future-learning/adaptation tests declared")
    add("IF-CT-02",set(BATTERY_TESTS)=={"A_future_learning_rate","B_adaptation_speed","C_novel_environment_success","D_few_shot_acquisition","E_cross_domain_learning","F_generalization_retention"},"A-F test names match frozen specification")
    add("IF-CT-03",len(INTELLIGENCE_TYPES)==6,"I1-I6 intelligence taxonomy present")
    add("IF-CT-04",all(bool(v) for v in INTELLIGENCE_TYPES.values()),"Each taxonomy category has a behavioral definition")
    add("IF-CT-05",set(SIMPLE_BASELINES)=={"past_performance","experience_count","capability_score","memory_strength","transfer_metrics"},"All required B1-B5 comparator variables included")
    add("IF-CT-06",RANDOM_BASELINE=="random_chance_baseline","Random/chance comparator is explicit")
    add("IF-CT-07",PRIMARY_PREDICTOR=="IG_t","Primary candidate predictor is frozen as IG at time t")
    add("IF-CT-08",PRIMARY_ENDPOINT=="A_future_learning_rate_normalized_auc","One primary external endpoint is frozen")
    add("IF-CT-09",PRIMARY_SOI==.02,"Smallest effect of interest is explicit")
    add("IF-CT-10",LEARNING_EXPOSURES==(0,1,3,5),"Learning exposures are fixed before confirmatory outcomes")
    funcs=[("IF-CT-11",score_task_output,{"predicted","gold"}),
           ("IF-CT-12",learning_curve_auc,{"scores","exposures"}),
           ("IF-CT-13",behavioral_delta,{"pre_score","post_score"}),
           ("IF-CT-14",validate_external_outcomes,{"outcomes"})]
    for cid,fn,needed in funcs:
        params=set(inspect.signature(fn).parameters)
        add(cid,needed.issubset(params) and not (params & FORBIDDEN_TARGET_FIELDS),f"{fn.__name__} accepts external behavior/evaluator fields only")
    add("IF-CT-15",score_task_output("blue","blue")==1.0 and score_task_output("blue","red")==0.0,"External correctness compares output with evaluator gold")
    add("IF-CT-16",abs(learning_curve_auc([0,.5,.75,1])-0.65)<1e-12,"Learning-rate endpoint is normalized trapezoidal AULC")
    add("IF-CT-17",learning_curve_auc([.5,.5,.5,.5])==.5,"Flat external performance yields flat AULC")
    add("IF-CT-18",abs(behavioral_delta(.2,.7)-.5)<1e-12,"Behavioral change is computed from external pre/post scores")
    invalid_curve=False
    try: learning_curve_auc([0,1],[0,0])
    except ValueError: invalid_curve=True
    add("IF-CT-19",invalid_curve,"Invalid exposure sequence cannot be scored")
    invalid_length=False
    try: learning_curve_auc([0,1],[0,1,2])
    except ValueError: invalid_length=True
    add("IF-CT-20",invalid_length,"Mismatched curve shape cannot be scored")
    add("IF-CT-21",validate_external_outcomes({"test_id":"A","correct":1,"exposure":3}),"External outcome schema accepts task behavior only")
    add("IF-CT-22",all(not validate_external_outcomes({f:0}) for f in FORBIDDEN_TARGET_FIELDS),"All internal score fields are rejected from target payloads")
    add("IF-CT-23",len(FORBIDDEN_TARGET_FIELDS)>=10,"Target contamination deny-list is explicit and broad")
    add("IF-CT-24",ig_predictive_decision(.06,.04,.08,.02,slope_ci_low=.01,slope_ci_high=.10)=="ig_wins","Decision rule permits a positive incremental IG win")
    add("IF-CT-25",ig_predictive_decision(0,-.01,.01,.02,slope_ci_low=-.01,slope_ci_high=.01)=="equivalent_tie","Decision rule permits an equivalence tie")
    add("IF-CT-26",ig_predictive_decision(-.05,-.08,-.03,.02,slope_ci_low=-.10,slope_ci_high=-.01)=="ig_loses","Decision rule permits an IG loss/inverse direction")
    add("IF-CT-27",ig_predictive_decision(.01,-.02,.04,.02,slope_ci_low=-.01,slope_ci_high=.03)=="inconclusive","Decision rule preserves uncertainty")
    add("IF-CT-28",ig_predictive_decision(0,0,0,.02,available=False)=="unavailable","Integrity failure remains unavailable, not zero")
    add("IF-CT-29",ig_predictive_decision(.06,.04,.08,.02,slope_ci_low=-.10,slope_ci_high=-.01)=="ig_loses","A wrong-direction predictive association cannot be labeled an IG win")
    all_win={t:"ig_wins" for t in BATTERY_TESTS}
    all_tie={t:"equivalent_tie" for t in BATTERY_TESTS}
    all_loss={t:"ig_loses" for t in BATTERY_TESTS}
    primary_secondary={t:"equivalent_tie" for t in BATTERY_TESTS};primary_secondary["A_future_learning_rate"]="ig_wins";primary_secondary["E_cross_domain_learning"]="ig_wins"
    add("IF-CT-30",intelligence_claim_decision(all_win,all_win,adequate_power=True,integrity_pass=True)=="claim_survives","Claim survives only with replicated learning and second external win")
    add("IF-CT-31",intelligence_claim_decision(all_tie,all_tie,adequate_power=True,integrity_pass=True)=="retire_as_intelligence","Adequately powered replicated ties trigger retirement path")
    add("IF-CT-32",intelligence_claim_decision(all_loss,all_loss,adequate_power=True,integrity_pass=True)=="retire_as_intelligence","Replicated external losses trigger retirement path")
    add("IF-CT-33",intelligence_claim_decision(all_tie,all_tie,adequate_power=False,integrity_pass=True)=="inconclusive","Underpowered nulls cannot force retirement")
    add("IF-CT-34",intelligence_claim_decision(primary_secondary,all_tie,adequate_power=True,integrity_pass=True)=="claim_weakens","Single-cohort/partial wins weaken but do not survive")
    add("IF-CT-35",intelligence_claim_decision(all_win,all_win,adequate_power=True,integrity_pass=False)=="unavailable","Failed integrity gate prevents validation claim")
    add("IF-CT-36",intelligence_claim_decision({}, {},adequate_power=True,integrity_pass=True)=="unavailable","Missing A-F endpoint table is unavailable")
    add("IF-CT-37","IG" in FORBIDDEN_TARGET_FIELDS and "IGR" in FORBIDDEN_TARGET_FIELDS and "IE" in FORBIDDEN_TARGET_FIELDS,"IG/IGR/IE are explicitly excluded from external target scoring")
    add("IF-CT-38",{"capability_score","CGR","C_t"}.issubset(FORBIDDEN_TARGET_FIELDS),"Capability/CGR/C_t internal metrics cannot define the target")
    add("IF-CT-39","capability_score" in SIMPLE_BASELINES and not validate_external_outcomes({"capability_score":0}),"Capability score is available as a predictor but explicitly forbidden as an external target label")
    add("IF-CT-40",len(rows)+5==44,"Contract suite has a fixed declared count")
    invalid_status=dict(all_tie);invalid_status["A_future_learning_rate"]="invented_status"
    add("IF-CT-41",intelligence_claim_decision(invalid_status,all_tie,adequate_power=True,integrity_pass=True)=="unavailable","Invalid decision labels cannot be used to validate or retire the claim")
    all_inconclusive={t:"inconclusive" for t in BATTERY_TESTS}
    add("IF-CT-42",intelligence_claim_decision(all_inconclusive,all_inconclusive,adequate_power=True,integrity_pass=True)=="inconclusive","Inconclusive outcomes do not become a weakening or retirement verdict")
    add("IF-CT-43",KEY_SECONDARY_PREDICTOR=="IGR_t" and KEY_SECONDARY_PREDICTOR in FORBIDDEN_TARGET_FIELDS,"IGR is a separately declared predictor, never an external target field")
    unavailable_status=dict(all_tie);unavailable_status["B_adaptation_speed"]="unavailable"
    add("IF-CT-44",intelligence_claim_decision(unavailable_status,all_tie,adequate_power=True,integrity_pass=True)=="unavailable","Unavailable external outcome cannot be treated as a tie or retirement result")

    with (out/"phase1F_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"intelligence_battery_schema.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["test_id","construct","independent_behavioral_observation","internal_metric_inputs"])
        defs=[("A_future_learning_rate","I1 learning speed / I6 knowledge efficiency","External accuracy curve at 0,1,3,5 examples on future novel task families","none"),
              ("B_adaptation_speed","I2 adaptation","External recovery curve after fixed rule/distribution shift","none"),
              ("C_novel_environment_success","I5 generalization","Held-out environment success after fixed resource budget","none"),
              ("D_few_shot_acquisition","I1/I4/I6 acquisition and compositional learning","Held-out accuracy after fixed 1- and 5-shot examples","none"),
              ("E_cross_domain_learning","I3 transfer / I4 composition","Target-domain learning curve on disjoint domain tasks","none"),
              ("F_generalization_retention","I5 generalization / persistence","Delayed novel-variant performance and relearning savings","none")]
        w.writerows(defs)
    with (out/"ig_outcome_response_sanity.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["fixture","delta_mae","ci_low","ci_high","slope_ci_low","slope_ci_high","status","scope"])
        cases=[("constructed_win",.06,.04,.08,.01,.10,True),("equivalence_tie",0,-.01,.01,-.01,.01,True),
               ("constructed_loss",-.05,-.08,-.03,-.10,-.01,True),("uncertain",.01,-.02,.04,-.01,.03,True),
               ("integrity_failure",0,0,0,0,0,False)]
        for name,d,lo,hi,slo,shi,avail in cases:
            status=ig_predictive_decision(d,lo,hi,.02,slope_ci_low=slo,slope_ci_high=shi,available=avail)
            w.writerow([name,d,lo,hi,slo,shi,status,"constructed decision-rule fixture only; no task outcomes"])
    failures=[r for r in rows if r["result"]!="PASS"]
    print(f"{len(rows)-len(failures)}/{len(rows)} Phase 1F intelligence construct/contract checks PASS")
    print("No learning/adaptation battery or confirmatory outcomes were executed.")
    return 1 if failures else 0

if __name__=="__main__":
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    raise SystemExit(run(dest))
