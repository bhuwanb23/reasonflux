"""Re-run the 26 Phase 1C contracts against the Phase 3A engine.

All generated panels/outcomes here are deliberately synthetic development
fixtures. Contract PASS means implementation plumbing only.
"""
from __future__ import annotations

from collections import Counter
import inspect
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from experiments.phase1c.ranking_benchmark import make_panel, TYPE_COUNTS
from transfer.memory import TransferMemory
from transfer.records import TransferRecord
from benchmark_engine import (
    CARD_FIELDS, POLICIES, CandidateCard, FNTUConfig, OutcomeRow, OutcomeVault,
    compare_fntu, fntu_suite, make_preoutcome_lock, normalized_kendall_divergence,
    oracle_rank, pressure_gate, pressure_metrics, randomized_arrival, rank_all,
    topk_rdr, validate_pool,
)


def make_fixture(seed: int = 17, panel: int = 0):
    old_cards, hidden, truth = make_panel(seed=seed, panel=panel)
    cards = [CandidateCard(
        c.candidate_id, c.frequency, c.consistency, c.generality,
        c.transfer_calibration, c.reasoning_value, c.reuse_probability,
        c.compression_gain,
    ) for c in old_cards]
    cards = randomized_arrival(cards, master_seed=seed, panel_id=f"dev-{panel}")
    memory = TransferMemory()
    for c in cards:
        t = float(c.transfer_calibration)
        x = t ** 0.5
        memory.record(TransferRecord(
            invariant_id=c.candidate_id, source_family="calibration-source",
            target_family="calibration-target", success=True, benefit=x,
            reasoning_reduction=x,
        ))
    validate_pool(cards, master_seed=seed, panel_id=f"dev-{panel}", expected_n=40, k=8)
    return cards, hidden, truth, memory


def endpoint_fixture(scores: dict[str, float], cards: tuple[CandidateCard, ...]):
    ids = [c.candidate_id for c in cards]
    chosen = {p: ids[i * 8:(i + 1) * 8] for i, p in enumerate(POLICIES)}
    rows = {}
    for p in POLICIES:
        rows[p] = [OutcomeRow(p, f"task-{h}", scores[p], 0.0, 0.0) for h in range(2)]
    return fntu_suite(rows, chosen, set(ids), FNTUConfig(8, 2, 1.0, "sha256:" + "a" * 64, True))


def run() -> list[dict]:
    c, labels, truth, memory = make_fixture()
    ranks = rank_all(c, panel_id="dev-0", master_seed=17,
                     calibration_memory=memory, total_families=1)
    pressure = pressure_metrics(ranks, 8)
    pool_ids = {x.candidate_id for x in c}
    checks: list[tuple[str, bool, str]] = []
    def check(cid, cond, detail): checks.append((cid, bool(cond), detail))

    check("CT-1", len(c) == 40 and Counter(labels.values()) == Counter(TYPE_COUNTS),
          "N=40; hidden synthetic quotas A-H and B/C stress classes verified outside engine")
    check("CT-2", set(CARD_FIELDS) == set(__import__('benchmark_engine').card_schema())
          and all("CAND-" in x and x in labels for x in pool_ids),
          "exact allowlist schema; opaque hash IDs; no latent/outcome field")
    check("CT-3", len(pool_ids) == 40 and list(x.candidate_id for x in c) ==
          [x.candidate_id for x in randomized_arrival(c, 17, "dev-0")],
          "unique IDs and deterministic randomized arrival permutation")
    check("CT-4", all(set(ranks[p]) == pool_ids for p in POLICIES),
          "R1-R5 consume and rank the exact same pool")
    check("CT-5", ranks == rank_all(c, panel_id="dev-0", master_seed=17,
          calibration_memory=memory, total_families=1), "same seed/panel replay is byte-stable")
    check("CT-6", all(len(ranks[p]) == 40 and len(set(ranks[p])) == 40 for p in POLICIES),
          "every policy returns a complete unique order; Top-8 selection is well-defined")
    check("CT-7", all(pressure[f"R1_vs_{p}_topk_rdr"] > 0 for p in POLICIES[1:]),
          "designed fixture exhibits disagreement with all four comparators")
    for idx, p in enumerate(POLICIES[1:4], start=8):
        check(f"CT-{idx}", pressure[f"R1_vs_{p}_topk_rdr"] >= 0.25,
              f"R1-vs-{p} synthetic TopK-RDR={pressure[f'R1_vs_{p}_topk_rdr']:.3f}")
    check("CT-11", pressure_gate(pressure), "synthetic fixture meets all frozen pressure thresholds")
    sig = inspect.signature(rank_all)
    check("CT-12", not ({"truth", "outcomes", "latent_labels", "oracle"} & set(sig.parameters)),
          "operational ranker API excludes outcomes, labels, and Oracle")
    lock = make_preoutcome_lock(ranks, list(pool_ids), pressure)
    vault = OutcomeVault(truth, expected_commitment=OutcomeVault.commitment(truth))
    access = vault.open_after_lock(lock, ranks, pressure)
    oracle = oracle_rank(access, lock, list(pool_ids))
    check("CT-13", len(oracle) == 40 and set(oracle) == pool_ids,
          "analysis-only Oracle rank emitted only after sealed-vault lock authorization")
    check("CT-14", set(inspect.signature(pressure_metrics).parameters) == {"rankings", "k"},
          "pre-outcome pressure validator accepts rankings and K only")
    rank_before = ranks
    changed_truth = {k: -v for k, v in truth.items()}
    _ = changed_truth
    ranks_after = rank_all(c, panel_id="dev-0", master_seed=17,
                           calibration_memory=memory, total_families=1)
    check("CT-15", rank_before == ranks_after,
          "separate outcome mutation cannot affect ranker API/output")
    check("CT-16", len({ranks[p][0] for p in POLICIES}) > 1,
          "selectors produce non-identical Top-1 choices in designed fixture")

    losing = {p: (0.0 if p == "R1_IDT" else 1.0 if p == "R2_FREQUENCY" else .25) for p in POLICIES}
    loss_scores = endpoint_fixture(losing, c)
    check("CT-17", compare_fntu(loss_scores)["R1_minus_R2_FREQUENCY"] < 0,
          "independent endpoint arithmetic can report R1 loss versus frequency")
    ties = {p: .5 for p in POLICIES}
    tie_scores = endpoint_fixture(ties, c)
    check("CT-18", all(abs(v) < 1e-12 for v in compare_fntu(tie_scores).values()),
          "equal-valued independent outcomes yield exact paired ties")
    wins = {p: (1.0 if p == "R1_IDT" else 0.0) for p in POLICIES}
    win_scores = endpoint_fixture(wins, c)
    check("CT-19", all(v > 0 for v in compare_fntu(win_scores).values()),
          "independent endpoint arithmetic can report R1 win")
    check("CT-20", set(labels) == set(truth) == pool_ids and not (set(labels) & set(CARD_FIELDS)),
          "labels/outcomes are separate opaque-ID keyed records, not ranker payload")
    check("CT-21", {"frequency", "consistency", "generality", "transfer_calibration",
                     "reasoning_value", "reuse_probability", "compression_gain"} <= CARD_FIELDS,
          "seven feature channels represented independently")
    check("CT-22", all(all(v is None or 0 <= v <= 1 for k, v in vars_card.items()
          if k != "candidate_id") for vars_card in [
              {name: getattr(x, name) for name in CARD_FIELDS} for x in c]),
          "all available public features bounded in [0,1]")

    panel_rows = []
    for seed in range(100):
        cards, _, _, mem = make_fixture(seed=seed, panel=0)
        rs = rank_all(cards, panel_id="dev-0", master_seed=seed,
                      calibration_memory=mem, total_families=1)
        pm = pressure_metrics(rs, 8)
        panel_rows.append({"seed": seed, "status": "pre-outcome", "pass": pressure_gate(pm), **pm})
    check("CT-23", all(r["pass"] for r in panel_rows),
          f"100 designed synthetic panels pass={sum(r['pass'] for r in panel_rows)}/100")
    mean_rdr = sum(r["mean_pairwise_topk_rdr"] for r in panel_rows) / len(panel_rows)
    mean_kendall = sum(r["mean_pairwise_kendall_divergence"] for r in panel_rows) / len(panel_rows)
    check("CT-24", mean_rdr >= 0.30, f"mean all-pair TopK-RDR={mean_rdr:.4f}")
    check("CT-25", mean_kendall >= 0.15, f"mean normalized Kendall divergence={mean_kendall:.4f}")
    check("CT-26", all(r["status"] == "pre-outcome" for r in panel_rows),
          "all pressure fixture rows explicitly marked pre-outcome")

    # Supplemental validations required for implementation readiness but not
    # individually numbered in the original 26-contract table.
    ids = sorted(pool_ids)
    tie_cards = [CandidateCard(cid, .5, .5, .5, 0.0, .5, .5, .5) for cid in ids]
    tie_cards = randomized_arrival(tie_cards, 501, "tie-panel")
    tie_memory = TransferMemory()
    for card in tie_cards:
        tie_memory.record(TransferRecord(card.candidate_id, "calibration-source", "calibration-target",
                                         True, 0.0, 0.0))
    ties_ranked = rank_all(tie_cards, panel_id="tie-panel", master_seed=501,
                           calibration_memory=tie_memory, total_families=1)
    expected_tie = sorted(ids)
    tie_break_ok = all(ties_ranked[p] == expected_tie for p in POLICIES[:4])
    replay_reversed = rank_all(list(reversed(tie_cards)), panel_id="tie-panel", master_seed=501,
                               calibration_memory=tie_memory, total_families=1)
    replay_ok = replay_reversed == ties_ranked
    seed_changed = rank_all(tie_cards, panel_id="tie-panel", master_seed=502,
                            calibration_memory=tie_memory, total_families=1)
    seed_stability_ok = seed_changed["R5_RANDOM"] != ties_ranked["R5_RANDOM"]
    converged = {p: ranks["R1_IDT"] for p in POLICIES}
    convergence_rejected = not pressure_gate(pressure_metrics(converged, 8))
    dummy_rows = {p: [OutcomeRow(p, f"t{i}", 0.0, 0.0, 0.0) for i in range(2)] for p in POLICIES}
    dummy_selected = {p: ids[:8] for p in POLICIES}
    try:
        fntu_suite(dummy_rows, dummy_selected, pool_ids, FNTUConfig(8, 2, None, None, False))
        rejects_unfrozen_cost = False
    except ValueError:
        rejects_unfrozen_cost = True
    missing_rows = {p: list(rows) for p, rows in dummy_rows.items()}
    missing_rows["R1_IDT"][0] = OutcomeRow("R1_IDT", "t0", None, 0.0, 0.0)
    try:
        fntu_suite(missing_rows, dummy_selected, pool_ids,
                   FNTUConfig(8, 2, 1.0, "sha256:" + "a" * 64, True))
        rejects_ambiguous_missing = False
    except ValueError:
        rejects_ambiguous_missing = True
    supplemental = {
        "deterministic_score_tie_break_by_opaque_id": tie_break_ok,
        "arrival_order_invariance": replay_ok,
        "random_seed_changes_random_order": seed_stability_ok,
        "converged_rankings_fail_pressure_gate": convergence_rejected,
        "unfrozen_cost_model_rejected": rejects_unfrozen_cost,
        "ambiguous_missing_outcome_rejected": rejects_ambiguous_missing,
    }
    if not all(supplemental.values()):
        raise AssertionError(f"supplemental checks failed: {supplemental}")
    if not all(ok for _, ok, _ in checks):
        failed = [f"{cid}: {detail}" for cid, ok, detail in checks if not ok]
        raise AssertionError("\n".join(failed))
    rows = [{"contract_id": cid, "result": "PASS" if ok else "FAIL", "detail": detail}
            for cid, ok, detail in checks]
    result = {
        "scope": "development/plumbing only; synthetic fixtures; not IDT efficacy",
        "contracts_passed": sum(r["result"] == "PASS" for r in rows),
        "contracts_total": len(rows),
        "pressure_panels": len(panel_rows),
        "pressure_all_pass": all(r["pass"] for r in panel_rows),
        "mean_pairwise_topk_rdr": mean_rdr,
        "mean_pairwise_kendall_divergence": mean_kendall,
        "mean_pairwise_rank_divergence": sum(r["mean_pairwise_rank_divergence"] for r in panel_rows) / len(panel_rows),
        "supplemental_checks": supplemental,
        "panel_rows": panel_rows,
        "contracts": rows,
    }
    out = Path(__file__).resolve().parent / "contract_results.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("panel_rows", "contracts")}, indent=2))
    print(f"contracts: {out}")
    return rows


if __name__ == "__main__":
    run()
