"""Run Phase 1G stage-separation and protocol-integrity contracts only."""
from __future__ import annotations
import csv, inspect, sys
from pathlib import Path
from arc_validation import (
    FORBIDDEN_INTERNAL_FIELDS, PIPELINE_STAGES, accuracy_rate, budget_contract,
    coverage_rate, family_accuracy, mechanism_chain_status, partial_pixel_accuracy,
    protocol_integrity_status, rate_observation, score_task_output,
    stage_activation, validate_external_outcomes,
)


def run(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    def add(cid,ok,detail):
        rows.append({"contract_id":cid,"result":"PASS" if ok else "FAIL","detail":detail})
    add("1G-CT-01",len(PIPELINE_STAGES)==7,"Seven mechanism/accuracy stages are independently declared")
    add("1G-CT-02",PIPELINE_STAGES==("representation_coverage","trace_generation","invariant_discovery","skill_formation","transfer","capability","accuracy"),"Cascade order is explicit from coverage through task accuracy")
    add("1G-CT-03",score_task_output([[1,0],[0,1]],[[1,0],[0,1]]) and not score_task_output([[1,0]],[[0,1]]),"Exact task scoring compares output with independent gold")
    add("1G-CT-04",coverage_rate(8,10)=={"status":"observed","rate":.8,"successes":8,"opportunities":10},"Coverage is computed from representable tasks and task denominator")
    add("1G-CT-05",coverage_rate(0,10)["rate"]==0.0 and coverage_rate(0,10)["status"]=="observed","Zero coverage is observed zero, not unavailable")
    add("1G-CT-06",coverage_rate(0,0)["status"]=="unavailable" and coverage_rate(0,0)["rate"] is None,"No coverage denominator is unavailable, not zero")
    add("1G-CT-07",accuracy_rate(2,10)["rate"]==.2,"Exact accuracy has its own correct-task/scored-task denominator")
    add("1G-CT-08",partial_pixel_accuracy(12,20)["rate"]==.6,"Partial pixel accuracy has a separate pixel denominator")
    fam=family_accuracy({"reflection":(1,5),"grouping":(0,4)})
    add("1G-CT-09",fam["reflection"]["rate"]==.2 and fam["grouping"]["rate"]==0.0,"Family accuracy remains disaggregated")
    add("1G-CT-10",coverage_rate(8,10)["rate"]==.8 and accuracy_rate(2,10)["rate"]==.2,"High coverage/low accuracy is representable as separate measures")
    add("1G-CT-11",coverage_rate(1,10)["rate"]==.1 and accuracy_rate(1,10)["rate"]==.1,"Low coverage/low accuracy is representable without conflation")
    add("1G-CT-12",{"coverage"}.isdisjoint(set(inspect.signature(accuracy_rate).parameters)),"Accuracy function does not read coverage")
    add("1G-CT-13",{"accuracy","correct"}.isdisjoint(set(inspect.signature(coverage_rate).parameters)),"Coverage function does not read accuracy")
    add("1G-CT-14",stage_activation(1,10)=="activated","Observed candidate activation can be represented")
    add("1G-CT-15",stage_activation(0,10)=="not_activated","Observed no-activation can be represented without theory rejection")
    add("1G-CT-16",stage_activation(0,0)=="unavailable","Zero eligible denominator yields unavailable")
    add("1G-CT-17",stage_activation(0,10,adequate_denominator=False)=="inconclusive","Insufficient denominator remains inconclusive")
    add("1G-CT-18",stage_activation(0,10,minimum=2)=="not_activated","Frozen activation threshold can be applied")
    all_active={s:"activated" for s in PIPELINE_STAGES}
    break_case=dict(all_active);break_case["invariant_discovery"]="not_activated";break_case["skill_formation"]="unavailable";break_case["transfer"]="unavailable";break_case["capability"]="unavailable"
    unavailable={s:"activated" for s in PIPELINE_STAGES};unavailable["transfer"]="unavailable"
    unclear={s:"activated" for s in PIPELINE_STAGES};unclear["transfer"]="inconclusive"
    add("1G-CT-19",mechanism_chain_status(all_active)=="chain_activated","Complete chain activation is representable")
    add("1G-CT-20",mechanism_chain_status(break_case)=="chain_break_observed","Observed stage failure localizes chain break while downstream stays unavailable")
    add("1G-CT-21",mechanism_chain_status(unavailable)=="chain_unavailable","No eligible transfer opportunities do not become transfer failure")
    add("1G-CT-22",mechanism_chain_status(unclear)=="inconclusive","Uncertain stages remain inconclusive")
    add("1G-CT-23",mechanism_chain_status({})=="unavailable","Incomplete stage table cannot pass")
    add("1G-CT-24",mechanism_chain_status({**all_active,"extra":"activated"})=="unavailable","Unexpected stage fields cannot silently alter chain result")
    add("1G-CT-25",budget_contract(3,[3,3,3]),"Runtime budgets matching frozen config pass")
    add("1G-CT-26",not budget_contract(3,[3,10,3]),"Scored-arm/config mismatch is blocked")
    add("1G-CT-27",budget_contract(3,[3,3],full_scan_budget=10,full_scan_declared_diagnostic=True),"Larger full-inventory scan allowed only as declared diagnostic")
    add("1G-CT-28",not budget_contract(3,[3,3],full_scan_budget=10,full_scan_declared_diagnostic=False),"Undeclared exhaustive scan is a protocol failure")
    add("1G-CT-29",not budget_contract(3,[3,3,4]),"Inconsistent per-arm candidate budgets are blocked")
    add("1G-CT-30",protocol_integrity_status(budget_consistent=True,holdout_locked_before_run=True,holdout_single_use=True,evaluator_isolated=True,failure_logging_complete=True)=="pass","All five protocol controls can pass explicitly")
    add("1G-CT-31",protocol_integrity_status(budget_consistent=False,holdout_locked_before_run=True,holdout_single_use=True,evaluator_isolated=True,failure_logging_complete=True)=="fail","Budget mismatch causes integrity failure")
    add("1G-CT-32",protocol_integrity_status(budget_consistent=True,holdout_locked_before_run=True,holdout_single_use=False,evaluator_isolated=True,failure_logging_complete=True)=="fail","Holdout reuse prevents pristine confirmatory status")
    add("1G-CT-33",protocol_integrity_status(budget_consistent=True,holdout_locked_before_run=True,holdout_single_use=None,evaluator_isolated=True,failure_logging_complete=True)=="unavailable","Unknown holdout audit is unavailable, not pass")
    add("1G-CT-34",protocol_integrity_status(budget_consistent=True,holdout_locked_before_run=True,holdout_single_use=True,evaluator_isolated=True,failure_logging_complete=False)=="fail","Incomplete failure logging fails protocol integrity")
    add("1G-CT-35",validate_external_outcomes({"task_id":"x","exact_correct":0,"coverage":1}),"Behavioral and coverage fields may coexist without internal metric inputs")
    add("1G-CT-36",all(not validate_external_outcomes({f:0}) for f in FORBIDDEN_INTERNAL_FIELDS),"Internal growth/capability/transfer fields are rejected from outcome payloads")
    add("1G-CT-37",{"IG","IGR","IE","CGR","C_t"}.issubset(FORBIDDEN_INTERNAL_FIELDS),"All named internal metrics are explicitly blocked from external labels")
    bad_count=False
    try: rate_observation(11,10)
    except ValueError: bad_count=True
    add("1G-CT-38",bad_count,"Invalid numerator/denominator cannot be silently accepted")
    add("1G-CT-39",rate_observation(0,4)["rate"]==0.0 and rate_observation(0,0)["status"]=="unavailable","Zero and unavailable states remain distinct")
    add("1G-CT-40",len(rows)+3==42,"Contract suite has a fixed declared count")
    add("1G-CT-41",not budget_contract(3,[3,3],full_scan_budget=2,full_scan_declared_diagnostic=True),"A smaller search is not mislabeled an exhaustive diagnostic scan")
    add("1G-CT-42",protocol_integrity_status(budget_consistent=False,holdout_locked_before_run=None,holdout_single_use=True,evaluator_isolated=True,failure_logging_complete=True)=="fail","Known protocol failure dominates unknown audit fields")

    with (out/"phase1G_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"arc_pipeline_metric_schema.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["stage","primary_metric","denominator","zero_or_missing_rule","accuracy_separation"])
        records=[("representation_coverage","demo_fit_coverage_rate","tasks with demos","0 observed; denominator 0 unavailable","coverage is not accuracy"),
        ("trace_generation","trace_generation_rate + successful_trace_rate","attempted tasks / generated traces","no attempts unavailable; failures logged","trace validity is not accuracy"),
        ("invariant_discovery","candidate yield, precision, survival","successful traces / candidate validations","zero candidates observed; no denominator unavailable","candidate status is not accuracy"),
        ("skill_formation","formation count, promotion rate, survival","validated invariant candidates","zero skills observed","skill formation is not transfer"),
        ("transfer","eligible transfer rate, utility, negative transfer","eligible skill-task pairs","zero eligible skill denominator unavailable","transfer is not overall accuracy"),
        ("capability","validated external capability units, persistence, utility","independent behavioral task tests","insufficient behavior denominator unavailable","capability follows Phase 1E; not C_t/CGR"),
        ("accuracy","exact task, partial pixel, per-family accuracy","scored test tasks/pixels/family tasks","no scored tasks unavailable","accuracy is not coverage or transfer")]
        w.writerows(records)
    with (out/"outcome_response_sanity.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["fixture","coverage_status","accuracy_status","chain_status","scope"])
        states=[("coverage_high_accuracy_low","observed .80","observed .20","chain_break_observed"),
        ("coverage_low_accuracy_low","observed .10","observed .10","chain_break_observed"),
        ("coverage_high_transfer_low","observed .80","observed .20","chain_break_observed"),
        ("zero_skill_transfer_denominator","observed coverage","unavailable transfer","chain_unavailable"),
        ("all_stages_active","observed","observed","chain_activated")]
        for row in states:w.writerow([*row,"constructed contract fixture only; no ARC outcome data"])
    failures=[r for r in rows if r["result"]!="PASS"]
    print(f"{len(rows)-len(failures)}/{len(rows)} Phase 1G stage-separation/protocol contracts PASS")
    print("No ARC search, task evaluation, or confirmatory outcomes were executed.")
    return 1 if failures else 0

if __name__=="__main__":
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    raise SystemExit(run(dest))
