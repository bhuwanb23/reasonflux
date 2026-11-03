"""Build Phase 2H tables from saved, non-confirmatory Phase 2B/2D/2E audits.
No benchmark or candidate miner is run here.
"""
from __future__ import annotations
import csv, json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2H-CANDIDATE-POPULATION-READINESS-V1"
P2E=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1"


def readcsv(p):
    with p.open(newline="") as f: return list(csv.DictReader(f))

def main():
    gen=readcsv(P2E/"candidate_generation_audit.csv")
    detail=readcsv(P2E/"candidate_and_validation_details.csv")
    rec=readcsv(P2E/"recurrence_summary.csv")
    proposal_ids=defaultdict(set)
    for r in detail:
        if r["stage"]=="CANDIDATE_PROPOSAL":
            proposal_ids[(r["source"],r["threshold_id"])].add(r["item_id"])
    rec_map={r["source"]:r for r in rec}
    # Candidate mining uses the historical discovery split only (600 tasks).
    out=[]
    for r in gen:
        source,threshold=r["source"],r["threshold_id"]
        recrow=rec_map.get(source,{})
        ids=proposal_ids[(source,threshold)]
        threshold_col={"RELAXED_S2":"signatures_support_ge_2",
                       "CURRENT_S1":"signatures_support_ge_5",
                       "STRICT_S3":None}[threshold]
        supported=(recrow.get(threshold_col,"0") if threshold_col else "0")
        out.append({
          "source_condition":source,"threshold_id":threshold,
          "support_floor":r["support_floor"],"discovery_tasks_processed":recrow.get("discovery_tasks_processed",""),
          "successful_discovery_traces":r["successful_discovery_trace_inputs"],
          "trace_fragments":recrow.get("fragment_occurrences_after_per_trace_dedupe",""),
          "unique_signatures_before_filter":recrow.get("distinct_operation_ngram_signatures",""),
          "signatures_support_ge_floor":supported,
          "max_distinct_task_support":recrow.get("max_distinct_trace_support",""),
          "patterns_after_mining":r["patterns_after_frequency_and_cross_trace_gates"],
          "aggregated_structures":r["aggregated_structures"],
          "candidate_proposals_pre_rejection":r["candidate_proposals_before_generation_rejections"],
          "distinct_proposal_ids_within_condition":len(ids),
          "accepted_candidates":r["accepted_generation_candidates"],
          "rejected_candidates":r["generation_rejected_candidates"],
          "rejection_reasons":r["generation_rejection_reason_counts_json"],
          "phase3_rankable_eligible":0,
          "interpretation":"proposal/feature fixture only; no accepted invariant candidate",
        })
    p=PKG/"candidate_yield_audit.csv"
    with p.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    summary={
      "phase2e_conditions":len(out),
      "accepted_invariant_candidates_total_across_condition_rows":sum(int(r["accepted_candidates"]) for r in out),
      "conditions_with_any_pre_rejection_proposals":sum(int(r["candidate_proposals_pre_rejection"])>0 for r in out),
      "conditions_with_accepted_candidate":sum(int(r["accepted_candidates"])>0 for r in out),
      "unique_proposal_ids_in_relaxed_rows":sorted({cid for (s,t), ids in proposal_ids.items() if t=="RELAXED_S2" for cid in ids}),
      "warning":"Repeated condition rows reuse task IDs/recipes and are not independent populations; do not sum proposals across conditions as unique candidates.",
      "actual_rankable_candidate_population":0,
      "decision":"F2 for current audited invariant candidate path; alternative candidate layer would require a new construct/protocol decision",
    }
    (PKG/"yield_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
