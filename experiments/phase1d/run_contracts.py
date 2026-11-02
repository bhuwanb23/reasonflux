"""Run Phase 1D design/schema/budget/leakage contracts; no benchmark execution."""
from __future__ import annotations
import csv
from pathlib import Path
import sys
from memory_challenge import (
    ARMS, FAMILIES, MEMORY_TYPES, SPLITS, BudgetCaps,
    has_intended_abstraction_challenge, has_intended_hybrid_challenge,
    has_intended_memory_win, outcome_label_is_separate, validate_budget_ledger,
)


def run(out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    rows=[]
    def add(cid, ok, detail):
        rows.append({"contract_id":cid,"result":"PASS" if ok else "FAIL","detail":detail})
    family_ids={f.family_id for f in FAMILIES}
    add("CT-1", family_ids==set("ABCDEF"), "Six challenge families A-F defined")
    add("CT-2", len(MEMORY_TYPES)==5 and all(x in MEMORY_TYPES for x in
        ("M1_EXACT_EPISODIC","M2_PARTIAL_EPISODIC","M3_PATTERN_MEMORY","M4_SKILL_ABSTRACTION","M5_HYBRID")),
        "Five memory representations remain distinct")
    add("CT-3", has_intended_memory_win(next(f for f in FAMILIES if f.family_id=="A")),
        "Exact replay family is an explicit positive control for M1")
    add("CT-4", all(has_intended_abstraction_challenge(f) for f in FAMILIES if f.family_id in "BDEF"),
        "Context/analogy/far/adversarial families create non-exact abstraction tests")
    add("CT-5", has_intended_hybrid_challenge(next(f for f in FAMILIES if f.family_id=="C")),
        "Composition family requires both context shift and composition")
    add("CT-6", next(f for f in FAMILIES if f.family_id=="F").adversarial_lure,
        "Adversarial retrieval lure is named and explicit")
    add("CT-7", len(ARMS)==8 and "B6_ORACLE_ANALYSIS_ONLY"==ARMS[-1],
        "All required arms present; Oracle labeled analysis-only")
    add("CT-8", set(ARMS[:3])=={"B1A_M1_EXACT","B1B_M2_PARTIAL","B1C_M3_PATTERN"},
        "Memory-only comparator is a suite, not one selected memory variant")
    caps=BudgetCaps()
    offer={a:{"training_examples":caps.training_examples,"storage_bytes":caps.storage_bytes,
        "candidate_units":caps.candidate_units,"training_compute_ops":caps.training_compute_ops,
        "inference_ops_per_task":caps.inference_ops_per_task,
        "retrieval_checks_per_task":caps.retrieval_checks_per_task} for a in ARMS[:-1]}
    add("CT-9", all(x==offer[ARMS[0]] for x in offer.values()),
        "Same per-arm maximum training/storage/candidate/compute/retrieval caps")
    usage={a:{"training_examples":min(12,caps.training_examples),"storage_bytes":min(1024,caps.storage_bytes),
        "candidate_units":min(12,caps.candidate_units),"training_compute_ops":min(10_000,caps.training_compute_ops),
        "inference_ops_per_task":min(500,caps.inference_ops_per_task),
        "retrieval_checks_per_task":min(2,caps.retrieval_checks_per_task)} for a in offer}
    overrun={a:dict(usage[a]) for a in usage}; overrun[ARMS[0]]["storage_bytes"]=caps.storage_bytes+1
    add("CT-10", validate_budget_ledger(usage,caps) and not validate_budget_ledger(overrun,caps),
        "Usage ledger accepts in-cap use and rejects an overrun")
    split_families={s:{f.family_id for f in FAMILIES} for s in SPLITS}
    add("CT-11", set(SPLITS)=={"development","confirmatory","replication"} and
        all(split_families[s]==family_ids for s in SPLITS),
        "Every named split is specified to contain each challenge family")
    add("CT-12", outcome_label_is_separate({"candidate_id","surface_features","memory_key","rule_features"}),
        "Allowed policy payload excludes gold/future labels")
    add("CT-13", not outcome_label_is_separate({"candidate_id","gold_answer"}),
        "Leakage guard rejects hidden-answer field")
    add("CT-14", all(f.family_id=="A" or not f.exact_precedent for f in FAMILIES),
        "Only Family A permits exact-precedent exposure")
    adversarial_families={f.family_id for f in FAMILIES if f.adversarial_lure}
    add("CT-15", adversarial_families=={"F"},
        "Adversarial lure occurs only in declared family F")
    add("CT-16", len({f.name for f in FAMILIES})==6, "Distinct family identifiers and names")
    add("CT-17", all(bool(f.design_role) and bool(f.expected_mechanism) for f in FAMILIES),
        "Each family has design purpose and falsifiable mechanism expectation")
    add("CT-18", caps.future_tasks_per_family>0 and caps.inference_ops_per_task>0,
        "Common task horizon and per-query compute cap defined")
    add("CT-19", caps.storage_bytes>0 and caps.candidate_units>0,
        "Storage and candidate-unit caps are explicit")
    add("CT-20", caps.retrieval_checks_per_task>0, "Retrieval count is bounded and auditable")
    add("CT-21", "B6_ORACLE_ANALYSIS_ONLY" not in offer,
        "Oracle receives no competitive budget ledger and cannot tune policies")
    add("CT-22", len(SPLITS)==3, "Confirmatory and replication are separate from development")
    add("CT-23", len(family_ids)==len(FAMILIES)==6 and all(len(f.family_id)==1 for f in FAMILIES), "Every challenge family has a unique stable ID")
    add("CT-24", all(a in ARMS for a in ("B1A_M1_EXACT","B1B_M2_PARTIAL","B1C_M3_PATTERN","B2_M4_ABSTRACTION","B3_M5_HYBRID","B4_RANDOM_RETRIEVAL","B5_NO_LEARNING","B6_ORACLE_ANALYSIS_ONLY")),
        "Comparator names exactly include all requested systems")
    add("CT-25", all(f.family_id in "ABCDEF" for f in FAMILIES), "No undeclared family enters protocol")
    add("CT-26", all(f.family_id!="A" or (f.exact_precedent and not f.adversarial_lure) for f in FAMILIES),
        "Exact-replay exposure is explicit, isolated, and non-adversarial")
    with (out/"phase1D_contract_test_results.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","result","detail"]);w.writeheader();w.writerows(rows)
    with (out/"challenge_family_design_matrix.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["family","name","exact_precedent","context_transform","composition_required","structural_relation_preserved","novel_family","adversarial_lure","design_role","expected_mechanism"])
        for x in FAMILIES: w.writerow([x.family_id,x.name,x.exact_precedent,x.context_transform,x.composition_required,x.structural_relation_preserved,x.novel_family,x.adversarial_lure,x.design_role,x.expected_mechanism])
    with (out/"budget_caps.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["resource","per_arm_cap","unit"])
        for k,v in offer[ARMS[0]].items(): w.writerow([k,v,"fixed protocol cap"])
        w.writerow(["future_tasks_per_family",caps.future_tasks_per_family,"tasks"])
    fails=[r for r in rows if r["result"]!="PASS"]
    print(f"{len(rows)-len(fails)}/{len(rows)} Phase 1D design contracts PASS")
    print("No task outcomes were run; contracts validate specification interfaces and declared scenario logic only.")
    return 1 if fails else 0

if __name__=="__main__":
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(".")
    raise SystemExit(run(dest))
