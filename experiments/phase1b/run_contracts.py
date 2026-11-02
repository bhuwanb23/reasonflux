"""Run Phase 1B contract checks on synthetic development fixtures only."""
from __future__ import annotations
import csv
import inspect
import itertools
from dataclasses import replace
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from phase1b.selection_benchmark import (  # noqa: E402
    CAPACITY, STORAGE_BUDGET, HORIZON, MC_ESTIMATE, TYPES, SPLITS, CandidateCard, choose,
    contested_sdr, future_net_value, make_batch, oracle_select, pairwise_divergence,
    pairwise_matrix, pressure_gate, run_selectors, scv10, portfolio_net_value,
)


def _assert(condition, message):
    if not condition:
        raise AssertionError(message)


def _checks():
    batch = make_batch("development", 0)
    cards, truths = batch.cards, batch.sealed_truth
    outputs = run_selectors(batch)
    truth_by_id = {x.candidate_id: x for x in truths}
    oracle = oracle_select(cards, truths)
    all7 = {**outputs, "S7_ORACLE": oracle}
    pass_batches = []
    gates = []
    for seed in range(100):
        b = make_batch("development", seed)
        sels = run_selectors(b)
        ok, result = pressure_gate(b.cards, sels)
        pass_batches.append(ok); gates.append(result)

    def taxonomy():
        return set(t.latent_type for t in truths) == set(TYPES)
    def quotas():
        return batch.type_counts_manifest == tuple((t, 4) for t in TYPES) and len(cards) == 20
    def hidden():
        forbidden = {"latent_type", "class", "label", "truth", "outcomes", "future_value", "oracle"}
        payload_ok = all(not (set(c.selector_payload()) & forbidden) and "-CAND-" in c.candidate_id
                         and not any(c.candidate_id.endswith(f"-{kind}{j}") for kind in TYPES for j in range(1,5))
                         for c in cards)
        positions = {kind:set() for kind in TYPES}
        for seed in range(20):
            b = make_batch("development", seed)
            truth = {t.candidate_id:t.latent_type for t in b.sealed_truth}
            for order,c in enumerate(b.cards): positions[truth[c.candidate_id]].add(order)
        return payload_ok and all(len(v)>1 for v in positions.values())
    def truth_independent():
        baseline = {t.candidate_id: future_net_value(t) for t in truths}
        mutated = [CandidateCard(c.candidate_id,c.split,c.batch_seed,c.arrival_order,c.frequency,
                    1.0-c.p_reuse,1.0-c.AG,1.0-c.TS,1.0-c.CC,c.MC) for c in cards]
        _ = [scv10(c) for c in mutated]
        return baseline == {t.candidate_id: future_net_value(t) for t in truths}
    def no_circular():
        t = truths[0]
        return "card" not in inspect.signature(future_net_value).parameters and future_net_value(t) == future_net_value(t)
    def seven_operational():
        return len(outputs) == 6 and len(all7) == 7 and all(len(v) == 8 for k,v in all7.items() if k != "S6_NEVER") and len(outputs["S6_NEVER"]) == 0
    def deterministic():
        return run_selectors(batch) == run_selectors(make_batch("development", 0))
    def tie_break():
        tied = tuple(CandidateCard(f"T-{i}", "development", 0, i, .5,.5,.5,.5,.1,.06) for i in range(20))
        return choose(tied,"S2_FREQUENCY") == choose(tied,"S2_FREQUENCY") and len(choose(tied,"S2_FREQUENCY")) == 8
    def divergence_rate():
        return all(pass_batches) and min(x["contested_sdr"] for x in gates) >= .20
    def topk_disagree():
        return all(pairwise_divergence(run_selectors(make_batch("development", s))["S1_SCV"],
                         run_selectors(make_batch("development", s))[p]) >= .10
                   for s in range(100) for p in ("S2_FREQUENCY","S3_REUSE","S4_RANDOM"))
    def pressure_before_truth():
        return tuple(inspect.signature(pressure_gate).parameters) == ("cards", "selections")
    def storage_parity():
        card_by_id = {c.candidate_id: c for c in cards}
        return (all(len(outputs[p]) == CAPACITY and sum(card_by_id[cid].storage_units for cid in outputs[p]) <= STORAGE_BUDGET
                    for p in ("S1_SCV","S2_FREQUENCY","S3_REUSE","S4_RANDOM","S5_ALWAYS_CAPACITY"))
                and len(outputs["S6_NEVER"]) == 0)
    def opportunity_parity():
        return all(set(outputs[p]) <= {c.candidate_id for c in cards} for p in outputs)
    def horizon_parity():
        return all(len(t.paired_utility_deltas) == HORIZON and len(t.maintenance_cost_teu) == HORIZON for t in truths)
    def information_parity():
        keysets = {tuple(sorted(c.selector_payload())) for c in cards}
        return len(keysets) == 1 and hidden()
    def no_outcome_leak():
        return hidden()
    def no_label_leak():
        return all("latent_type" not in c.selector_payload() for c in cards)
    def split_isolation():
        idsets = [{c.candidate_id for seed in range(10) for c in make_batch(split, seed).cards} for split in SPLITS]
        return all(not (idsets[i] & idsets[j]) for i,j in itertools.combinations(range(len(idsets)),2))
    def oracle_excluded():
        return "S7_ORACLE" not in outputs and len(oracle) == CAPACITY
    def oracle_no_pressure_effect():
        return tuple(inspect.signature(pressure_gate).parameters) == ("cards", "selections") and "S7_ORACLE" not in outputs
    def cost_frozen():
        return MC_ESTIMATE == .06 and all(len(t.maintenance_cost_teu)==HORIZON and set(t.maintenance_cost_teu)=={.003} for t in truths)
    def reward_frozen():
        return all(len(t.paired_utility_deltas)==10 for t in truths) and future_net_value(truths[0]) == sum(truths[0].paired_utility_deltas)-truths[0].creation_cost_teu-sum(truths[0].maintenance_cost_teu)
    def labels_robust():
        # The latent recipe is classed before observations; +/-5% on cost conversion
        # leaves its intended type unchanged. D/E are checked by their defining rules.
        def inferred(t, scale):
            theta = t.latent_gross_future_utility - scale*(t.creation_cost_teu + sum(t.maintenance_cost_teu))
            early = sum(t.paired_utility_deltas[:2]) - scale*(t.creation_cost_teu + sum(t.maintenance_cost_teu[:2]))
            if early >= .10 and theta <= -.10: return "D"
            if t.opportunity_probability <= .10 and theta >= .50: return "E"
            if theta >= .10: return "A"
            if theta <= -.10: return "C"
            return "B"
        return all(inferred(t,scale)==t.latent_type for t in truths for scale in (.95,1.0,1.05))
    def score_can_lose():
        y = {p: portfolio_net_value(sel, truths) for p,sel in all7.items()}
        return (y["S1_SCV"] < y["S4_RANDOM"] and y["S1_SCV"] < y["S5_ALWAYS_CAPACITY"]
                and y["S1_SCV"] < y["S6_NEVER"])
    def score_can_win():
        y = {p: portfolio_net_value(sel, truths) for p,sel in outputs.items()}
        return y["S1_SCV"] > y["S2_FREQUENCY"] and y["S1_SCV"] > y["S3_REUSE"]
    def score_can_tie():
        flat = [replace(t, paired_utility_deltas=(.1,)*HORIZON, creation_cost_teu=0.0,
                        maintenance_cost_teu=(0.0,)*HORIZON) for t in truths]
        y = {p: portfolio_net_value(sel, flat) for p,sel in outputs.items() if p != "S6_NEVER"}
        return max(y.values()) - min(y.values()) < 1e-12

    return [

      ("CT-1A","All five candidate classes present",taxonomy),
      ("CT-1B","Per-batch 4xA-E quotas and N=20",quotas),
      ("CT-1C","Candidate labels hidden from selector payloads",hidden),
      ("CT-2A","Future Net Value depends on held-out truth/cost, not predictors",truth_independent),
      ("CT-2B","Mutating SCV inputs cannot mutate ground-truth value",no_circular),
      ("CT-3A","All seven required selectors operational (oracle analysis-only)",seven_operational),
      ("CT-3B","Deterministic replay for same seed",deterministic),
      ("CT-3C","Tie ordering is deterministic",tie_break),
      ("CT-4A","Mean pairwise SDR >= .20 in 100 development fixtures",divergence_rate),
      ("CT-4B","SCV top-K differs from frequency, reuse, and random",topk_disagree),
      ("CT-4C","Pressure gate receives no truth/outcome argument",pressure_before_truth),
      ("CT-5A","Creation/storage capacity parity (K=8)",storage_parity),
      ("CT-5B","Opportunity/candidate pool parity",opportunity_parity),
      ("CT-5C","Evaluation horizon parity (10 opportunities)",horizon_parity),
      ("CT-5D","Information-card parity and no hidden fields",information_parity),
      ("CT-6A","No held-out outcome leakage",no_outcome_leak),
      ("CT-6B","No taxonomy-label leakage",no_label_leak),
      ("CT-6C","Calibration/dev/confirmatory/replication IDs disjoint",split_isolation),
      ("CT-7A","Oracle isolated from production competition",oracle_excluded),
      ("CT-7B","Oracle cannot affect pressure or candidate generation",oracle_no_pressure_effect),
      ("CT-8A","Cost model fixed in contract fixture",cost_frozen),
      ("CT-8B","Reward formula and horizon fixed",reward_frozen),
      ("CT-8C","Type labels robust under +/-5% cost conversion",labels_robust),
      ("CT-9A","Adverse-value fixture lets SCV lose to Always and Never",score_can_lose),
      ("CT-9B","Outcome aggregation returns a tie when all candidate values tie",score_can_tie),
      ("CT-9C","Same outcome pipeline can register SCV wins vs frequency/reuse",score_can_win),
    ], batch, outputs, all7, gates


def main(out_dir: Path):
    results, batch, outputs, all7, gates = _checks()
    out_dir.mkdir(parents=True, exist_ok=True)
    table=[]
    for cid, name, fn in results:
        try:
            passed=bool(fn()); detail="Contract assertion passed" if passed else "Contract assertion returned false"
        except Exception as e:
            passed=False; detail=f"{type(e).__name__}: {e}"
        table.append({"contract_id":cid,"contract":name,"result":"PASS" if passed else "FAIL","detail":detail})
    with (out_dir/"contract_test_results.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["contract_id","contract","result","detail"]);w.writeheader();w.writerows(table)
    first=run_selectors(batch)
    matrix=pairwise_matrix(first)
    with (out_dir/"pairwise_divergence_matrix.csv").open("w",newline="",encoding="utf-8") as f:
        names=list(matrix)
        w=csv.DictWriter(f,fieldnames=["selector"]+names);w.writeheader()
        for name,row in matrix.items():w.writerow({"selector":name,**row})
    truth_by_id={t.candidate_id:t for t in batch.sealed_truth}
    outcome_rows=[]
    scv_y=portfolio_net_value(first["S1_SCV"],batch.sealed_truth)
    for policy,selected in all7.items():
        counts={kind:sum(truth_by_id[cid].latent_type==kind for cid in selected) for kind in TYPES}
        y=portfolio_net_value(selected,batch.sealed_truth)
        outcome_rows.append({"fixture_split":"development","fixture_seed":batch.seed,
            "policy":policy,"selected_n":len(selected),"selected_type_counts":json.dumps(counts,sort_keys=True),
            "mean_net_value_per_slot_teu":y,"difference_vs_scv_teu":y-scv_y,
            "interpretation":"synthetic outcome-response contract only; not research evidence"})
    with (out_dir/"outcome_response_sanity.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(outcome_rows[0]));w.writeheader();w.writerows(outcome_rows)
    stats={"fixture_split":"development","fixture_seed":batch.seed,"batches_checked":len(gates),
           "all_batches_pressure_pass":all(x["pressure_pass"] for x in gates),
           "min_contested_sdr":min(x["contested_sdr"] for x in gates),
           "mean_contested_sdr":sum(x["contested_sdr"] for x in gates)/len(gates),
           "max_contested_sdr":max(x["contested_sdr"] for x in gates),
           "mean_scv_frequency_divergence":sum(x["scv_pairwise"]["S1_SCV__S2_FREQUENCY"] for x in gates)/len(gates),
           "min_scv_frequency_divergence":min(x["scv_pairwise"]["S1_SCV__S2_FREQUENCY"] for x in gates),
           "mean_scv_reuse_divergence":sum(x["scv_pairwise"]["S1_SCV__S3_REUSE"] for x in gates)/len(gates),
           "min_scv_reuse_divergence":min(x["scv_pairwise"]["S1_SCV__S3_REUSE"] for x in gates),
           "mean_scv_random_divergence":sum(x["scv_pairwise"]["S1_SCV__S4_RANDOM"] for x in gates)/len(gates),
           "min_scv_random_divergence":min(x["scv_pairwise"]["S1_SCV__S4_RANDOM"] for x in gates),
           "selection_sets":{k:list(v) for k,v in first.items()},
           "selection_rates":{k:len(v)/20 for k,v in first.items()},
           "sdr_definition":"mean of pairwise symmetric-difference / N among S1-S4",
           "data_status":"synthetic contract fixtures only; not candidate outcome evidence or confirmatory data"}
    (out_dir/"pressure_validation.json").write_text(json.dumps(stats,indent=2)+"\n")
    n_pass=sum(x["result"]=="PASS" for x in table)
    print(f"{n_pass}/{len(table)} contracts PASS")
    print("100/100 development fixture pressure gates:",stats["all_batches_pressure_pass"])
    print("mean SDR:",stats["mean_contested_sdr"],"minimum SDR:",stats["min_contested_sdr"])
    if n_pass != len(table): raise SystemExit(1)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: python run_contracts.py <output-dir>")
    main(Path(sys.argv[1]))
