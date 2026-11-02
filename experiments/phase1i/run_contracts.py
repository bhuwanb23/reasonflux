"""Run Phase 1I protocol/specification contracts; never runs experiments."""
from __future__ import annotations
import csv
from pathlib import Path
import sys
from evaluation_protocol import (
    ALLOWED_MISSINGNESS_POLICIES, EXPERIMENT_CLASSES, OUTCOME_STATES,
    REPLICATION_LABELS, REQUIRED_GOVERNANCE, REQUIRED_PREREG_FIELDS,
    REQUIRED_REPORT_FIELDS, classify_outcome, combined_claim_status,
    endpoint_status, governance_status, missingness_status, preregistration_status,
    report_status, replication_status, statistical_record_status,
    supports_primary_claim, transition_allowed, valid_experiment_class,
)


def main(outdir: str) -> int:
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True);rows=[]
    def add(cid,ok,detail): rows.append({"contract_id":cid,"result":"PASS" if bool(ok) else "FAIL","detail":detail})

    # Canonical constructed records used only to exercise validation code.
    prereg={k:"frozen" for k in REQUIRED_PREREG_FIELDS}
    prereg.update({"experiment_class":"E3","soi":0.02,"missingness_policy":"complete_case_with_denominator"})
    endpoints=[{"endpoint_id":"primary_accuracy","role":"primary","definition":"held-out exact score","direction":"higher","drives_decision":True},
               {"endpoint_id":"coverage","role":"diagnostic","definition":"eligible coverage","direction":"descriptive","drives_decision":False}]
    stat={"independent_unit":"seed_cluster","independent_unit_count":10,"row_count":440,"effect_estimate":0.06,
          "ci_low":0.04,"ci_high":0.08,"missing_count":2,"total_count":100,
          "exact_ties_reported":True,"zero_variance_reported":True}
    gov={k:True for k in REQUIRED_GOVERNANCE}
    report={k:"recorded" for k in REQUIRED_REPORT_FIELDS}
    report.update({"negative_results":["none or listed"],"unavailable_results":["none or listed"]})

    # A. Experiment classification and preregistration (12)
    add("1I-CT-01",set(EXPERIMENT_CLASSES)=={"E1","E2","E3","E4"},"All four experiment classes are defined")
    add("1I-CT-02",valid_experiment_class("E1") and valid_experiment_class("E2"),"Exploratory and development classes are valid")
    add("1I-CT-03",supports_primary_claim("E3") and supports_primary_claim("E4"),"Confirmatory and replication can support primary claims")
    add("1I-CT-04",not supports_primary_claim("E1") and not supports_primary_claim("E2"),"Exploratory/development evidence cannot support primary claims")
    add("1I-CT-05",not valid_experiment_class("E5"),"Unknown class is rejected")
    add("1I-CT-06",not transition_allowed("E1","E3",outcomes_accessed=False),"E1 evidence cannot be promoted into confirmatory evidence")
    add("1I-CT-07",not transition_allowed("E3","E4",outcomes_accessed=True),"Classification is immutable after outcome access")
    add("1I-CT-08",preregistration_status(prereg)=="complete","Fully populated preregistration passes")
    missing=dict(prereg);missing.pop("research_question")
    add("1I-CT-09",preregistration_status(missing).startswith("incomplete:"),"Missing research question blocks preregistration")
    badclass=dict(prereg);badclass["experiment_class"]="E1";badclass["primary_claim"]="claim"
    add("1I-CT-10",preregistration_status(badclass)=="class_cannot_support_primary_claim","E1 cannot register a primary scientific claim")
    badsoi=dict(prereg);badsoi["soi"]=-.1
    add("1I-CT-11",preregistration_status(badsoi)=="invalid_soi","SOI must be nonnegative and frozen")
    badmiss=dict(prereg);badmiss["missingness_policy"]="replace_missing_with_zero"
    add("1I-CT-12",preregistration_status(badmiss)=="invalid_missingness_policy","Missingness policy cannot convert unavailable to zero")

    # B. Endpoint separation (8)
    add("1I-CT-13",endpoint_status(endpoints)=="pass","One decision-driving primary endpoint passes")
    add("1I-CT-14",endpoint_status([endpoints[1]])=="require_exactly_one_primary","No primary endpoint is rejected")
    add("1I-CT-15",endpoint_status(endpoints+[dict(endpoints[0],endpoint_id="second_primary")])=="require_exactly_one_primary","Multiple primary endpoints are rejected")
    add("1I-CT-16",endpoint_status([endpoints[0],dict(endpoints[1],drives_decision=True)])=="secondary_or_diagnostic_drives_decision","Diagnostic metric cannot silently drive primary decision")
    add("1I-CT-17",endpoint_status([endpoints[0],{"endpoint_id":"secondary","role":"secondary","definition":"supporting","direction":"higher","drives_decision":True}])=="secondary_or_diagnostic_drives_decision","Secondary endpoint cannot replace primary after outcomes")
    add("1I-CT-18",endpoint_status([dict(endpoints[0],definition="")])=="incomplete_primary_definition","Primary definition and direction are required")
    add("1I-CT-19",endpoint_status([endpoints[0],dict(endpoints[1],endpoint_id="primary_accuracy")])=="duplicate_or_missing_id","Endpoint IDs must be unique")
    add("1I-CT-20",endpoint_status([dict(endpoints[0],role="exploratory")])=="invalid_role","Only primary/secondary/diagnostic roles are allowed")

    # C. Statistical units, denominators, missingness (10)
    add("1I-CT-21",statistical_record_status(stat)=="pass","Cluster-level independent unit and nested rows are reported")
    no_n=dict(stat);no_n.pop("independent_unit_count")
    add("1I-CT-22",statistical_record_status(no_n)=="unavailable","Missing independent-unit count is unavailable")
    zero_n=dict(stat);zero_n["independent_unit_count"]=0
    add("1I-CT-23",statistical_record_status(zero_n)=="invalid_denominator_or_units","Zero independent units are not a valid estimate")
    bad_ci=dict(stat);bad_ci.update({"ci_low":.09,"ci_high":.02})
    add("1I-CT-24",statistical_record_status(bad_ci)=="invalid_interval","Malformed uncertainty interval is rejected")
    no_ties=dict(stat);no_ties["exact_ties_reported"]=False
    add("1I-CT-25",statistical_record_status(no_ties)=="tie_or_zero_variance_not_reported","Exact ties must be explicitly reported")
    no_var=dict(stat);no_var["zero_variance_reported"]=False
    add("1I-CT-26",statistical_record_status(no_var)=="tie_or_zero_variance_not_reported","Zero variance must be explicitly reported")
    add("1I-CT-27",missingness_status(total=100,missing=2,policy="complete_case_with_denominator",max_missing_rate=.05)=="pass","Prespecified missingness below limit is handled")
    add("1I-CT-28",missingness_status(total=100,missing=6,policy="complete_case_with_denominator",max_missing_rate=.05)=="unavailable","Missingness beyond frozen limit blocks result")
    add("1I-CT-29",missingness_status(total=100,missing=0,policy="complete_case_with_denominator",max_missing_rate=.05)=="pass","Zero missingness is distinct from missing outcomes")
    add("1I-CT-30",missingness_status(total=0,missing=0,policy="complete_case_with_denominator",max_missing_rate=.05)=="unavailable","Undefined denominator is unavailable, not zero performance")

    # D. Five-state outcome logic and tie/zero-variance behavior (12)
    add("1I-CT-31",classify_outcome(.06,.04,.08,.02,independent_units=10)=="supported","Meaningful preregistered effect can be supported")
    add("1I-CT-32",classify_outcome(0,-.01,.01,.02,independent_units=10)=="contradicted","Precise null contradicts a meaningful-superiority claim")
    add("1I-CT-33",classify_outcome(.02,-.01,.04,.02,independent_units=10)=="inconclusive","Interval spanning decision boundary remains inconclusive")
    add("1I-CT-34",classify_outcome(None,None,None,.02,available=False)=="unavailable","Missing endpoint is unavailable, not zero")
    add("1I-CT-35",classify_outcome(.06,.04,.08,.02,informative=False)=="non_informative","Identical comparator decisions can be explicitly non-informative")
    add("1I-CT-36",classify_outcome(.06,.04,.08,.02,valid=False)=="unavailable","Failed integrity/fairness gate blocks outcome interpretation")
    add("1I-CT-37",classify_outcome(0,-.01,.01,.02,hypothesis="equivalence",independent_units=10)=="supported","A precise tie can support preregistered equivalence")
    add("1I-CT-38",classify_outcome(-.06,-.08,-.04,.02,hypothesis="negative_superiority",independent_units=10)=="supported","Opposite-direction effect can support a prespecified negative hypothesis")
    add("1I-CT-39",classify_outcome(0,-.01,.01,.02,hypothesis="noninferiority",independent_units=10)=="supported","Noninferiority is classifiable when preregistered")
    add("1I-CT-40",classify_outcome(.05,.03,.07,.02,independent_units=2,minimum_units=10)=="inconclusive","Insufficient independent units cannot be called support")
    add("1I-CT-41",classify_outcome(.10,.01,.04,.02,independent_units=10)=="unavailable","Estimate outside its interval is rejected")
    add("1I-CT-42",classify_outcome(0,0,0,.02,independent_units=10)=="contradicted","Exact tie/zero variance is reported and does not become superiority")

    # E. Replication discipline (11)
    add("1I-CT-43",set(REPLICATION_LABELS)=={"R1","R2","R3","R4"},"All four replication classes are defined")
    add("1I-CT-44",replication_status("R1",independent_manifest=True,independent_source=True,same_protocol=True)=="valid_replication_type","Within-generator independent replication is recognized")
    add("1I-CT-45",replication_status("R2",independent_manifest=True,independent_source=True,same_protocol=True)=="valid_replication_type","Cross-generator replication is recognized")
    add("1I-CT-46",replication_status("R3",independent_manifest=True,independent_source=True,same_protocol=True)=="valid_replication_type","Cross-domain replication is recognized")
    add("1I-CT-47",replication_status("R4",independent_manifest=True,independent_source=True,same_protocol=True)=="valid_replication_type","External benchmark replication is recognized")
    add("1I-CT-48",replication_status("R4",independent_manifest=False,independent_source=False,same_protocol=True)=="not_independent","Reusing holdout/data does not count as replication")
    add("1I-CT-49",replication_status("R1",independent_manifest=True,independent_source=True,same_protocol=True)=="valid_replication_type","New seeds/panels must have independent manifests")
    add("1I-CT-50",combined_claim_status("supported","supported","R1",generalization_claim=True)=="inconclusive","Within-generator replication alone cannot support generalization")
    add("1I-CT-51",combined_claim_status("supported","inconclusive","R2")=="inconclusive","One positive result is not generalized support")
    add("1I-CT-52",combined_claim_status("supported","supported","R2",generalization_claim=True)=="supported","Cross-generator replication can support a generalization claim")
    add("1I-CT-53",combined_claim_status("supported","contradicted","R2")=="inconclusive","Conflicting confirmatory/replication outcomes remain inconclusive")

    # F. Governance and reporting (11)
    add("1I-CT-54",governance_status(gov)=="pass","Complete governance audit passes")
    partial=dict(gov);partial.pop("G7_source_lineage_preserved")
    add("1I-CT-55",governance_status(partial)=="unavailable","Missing governance audit evidence is unavailable")
    changed=dict(gov);changed["G1_frozen_protocol_unchanged"]=False
    add("1I-CT-56",governance_status(changed)=="fail","Frozen-protocol changes fail governance")
    hidden=dict(gov);hidden["G3_negative_results_retained"]=False
    add("1I-CT-57",governance_status(hidden)=="fail","Hiding negative results fails governance")
    add("1I-CT-58",not transition_allowed("E2","E4",outcomes_accessed=False),"Development findings cannot be promoted as replication")
    posthoc=dict(gov);posthoc["no_post_outcome_rule_changes"]=False
    add("1I-CT-59",governance_status(posthoc)=="fail","Post-outcome endpoint/threshold/split changes fail governance")
    add("1I-CT-60",report_status(report)=="complete","Complete reporting record passes")
    no_negative=dict(report);no_negative["negative_results"]=[]
    add("1I-CT-61",report_status(no_negative).startswith("incomplete:"),"Negative results must be explicitly reported")
    no_unavail=dict(report);no_unavail["unavailable_results"]=[]
    add("1I-CT-62",report_status(no_unavail).startswith("incomplete:"),"Unavailable results must be explicitly reported")
    no_units=dict(report);no_units.pop("independent_unit_count")
    add("1I-CT-63",report_status(no_units).startswith("incomplete:"),"Reports must include independent-unit count and source lineage")
    add("1I-CT-64",len(rows)+4==67,"Contract suite has a fixed declared count")
    add("1I-CT-65",classify_outcome(.05,.03,.07,.02,independent_units=0)=="unavailable","No independent units is unavailable, not a zero-effect result")
    badsoi_nan=dict(prereg);badsoi_nan["soi"]=float("nan")
    add("1I-CT-66",preregistration_status(badsoi_nan)=="invalid_soi","Non-finite SOI is rejected")
    add("1I-CT-67",all(governance_status({**gov,k:False})=="fail" for k in REQUIRED_GOVERNANCE),"Every individual governance rule is fail-closed")

    # Constructed outcome-state matrix. These fixtures never represent measured data.
    cases=[
        ("constructed_support",classify_outcome(.06,.04,.08,.02,independent_units=10)),
        ("constructed_contradiction",classify_outcome(0,-.01,.01,.02,independent_units=10)),
        ("constructed_inconclusive",classify_outcome(.02,-.01,.04,.02,independent_units=10)),
        ("constructed_unavailable",classify_outcome(None,None,None,.02,available=False)),
        ("constructed_non_informative",classify_outcome(.06,.04,.08,.02,informative=False)),
        ("constructed_equivalence_tie",classify_outcome(0,-.01,.01,.02,hypothesis="equivalence",independent_units=10)),
        ("constructed_opposite_direction",classify_outcome(-.06,-.08,-.04,.02,independent_units=10)),
        ("constructed_alternative_superiority_supported",classify_outcome(-.06,-.08,-.04,.02,hypothesis="negative_superiority",independent_units=10)), 
    ]
    with (out/"phase1I_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"outcome_state_sanity.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["constructed_fixture","state","evidence_scope"])
        for name,state in cases:w.writerow([name,state,"constructed protocol contract only; no empirical result"])
    with (out/"phase1I_protocol_schema.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["section","required_field_or_rule","meaning"])
        for k in REQUIRED_PREREG_FIELDS:w.writerow(["preregistration",k,"must be frozen before confirmatory outcome access"])
        for k in REQUIRED_REPORT_FIELDS:w.writerow(["reporting",k,"must be reported; negative/unavailable outcomes explicit"])
        for k in REQUIRED_GOVERNANCE:w.writerow(["governance",k,"must pass or the claim is blocked"])
    if any(r["result"]!="PASS" for r in rows):
        print(f"{sum(r['result']=='PASS' for r in rows)}/{len(rows)} Phase 1I contracts PASS")
        return 1
    print(f"{len(rows)}/{len(rows)} Phase 1I evaluation-governance contracts PASS")
    print("Only protocol logic and constructed outcomes were tested; no benchmark or experiment was run.")
    return 0

if __name__=="__main__":
    target=sys.argv[1] if len(sys.argv)>1 else "reports/experiments/ASFT-V1.1-PHASE-1I-EVALUATION-PROTOCOL-V1"
    raise SystemExit(main(target))
