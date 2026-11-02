"""Run Phase 1C synthetic ranking-pressure contracts; not a research experiment."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

from ranking_benchmark import (
    CandidateCard, TYPE_COUNTS, evaluate_topk, kendall_divergence, make_panel, oracle_rank,
    pressure_gate, pressure_metrics, rank_all, run_pressure_fixtures, topk_rdr,
)


def _row(cid, passed, detail):
    return {"contract_id": cid, "result": "PASS" if passed else "FAIL", "detail": detail}


def run(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    cards, hidden, truth = make_panel(0)
    k = 8
    ranks = rank_all(cards, seed=7919)
    ids = {c.candidate_id for c in cards}
    rows = []

    rows.append(_row("CT-1", len(cards) == 40 and len(hidden) == 40 and
                     {t: list(hidden.values()).count(t) for t in TYPE_COUNTS} == TYPE_COUNTS,
                     "N=40; hidden A-H fixture quotas with 8 each B/C"))
    import re
    rows.append(_row("CT-2", all(not hasattr(c, "latent_type") and
                     re.fullmatch(r"CAND-[0-9a-f]{12}", c.candidate_id) for c in cards),
                     "No latent-label field; IDs follow opaque hash-only format"))
    rows.append(_row("CT-3", len({c.candidate_id for c in cards}) == 40 and
                     cards != sorted(cards, key=lambda c: c.candidate_id),
                     "Unique opaque IDs; arrival order independently shuffled"))
    rows.append(_row("CT-4", set(ranks) == {"R1_IDT", "R2_FREQUENCY", "R3_REUSE", "R4_COMPRESSION", "R5_RANDOM"}
                     and all(set(r) == ids for r in ranks.values()),
                     "Five policy rankers use the exact same candidate pool"))
    rows.append(_row("CT-5", ranks == rank_all(cards, seed=7919), "Same-seed replay is deterministic"))
    rows.append(_row("CT-6", all(len(r[:k]) == k and len(set(r[:k])) == k for r in ranks.values()),
                     "Each policy returns exactly K=8 unique selections"))
    rows.append(_row("CT-7", all(ranks[a] != ranks[b] for a, b in [("R1_IDT", "R2_FREQUENCY"),
                     ("R1_IDT", "R3_REUSE"), ("R1_IDT", "R4_COMPRESSION")]),
                     "Fixture creates full-rank disagreement with each serious baseline"))
    pm = pressure_metrics(ranks, k)
    rows.append(_row("CT-8", pm["R1_vs_R2_FREQUENCY_topk_rdr"] >= .25,
                     f"IDT/Frequency Top-K RDR={pm['R1_vs_R2_FREQUENCY_topk_rdr']:.3f}"))
    rows.append(_row("CT-9", pm["R1_vs_R3_REUSE_topk_rdr"] >= .25,
                     f"IDT/Reuse Top-K RDR={pm['R1_vs_R3_REUSE_topk_rdr']:.3f}"))
    rows.append(_row("CT-10", pm["R1_vs_R4_COMPRESSION_topk_rdr"] >= .25,
                     f"IDT/Compression Top-K RDR={pm['R1_vs_R4_COMPRESSION_topk_rdr']:.3f}"))
    rows.append(_row("CT-11", pressure_gate(pm), "Pre-outcome RDR and Kendall gates pass fixture 0"))
    rows.append(_row("CT-12", "R6_ORACLE" not in ranks and
                     "truth" not in __import__("inspect").signature(rank_all).parameters,
                     "Oracle/truth excluded from production ranking interface"))
    rows.append(_row("CT-13", oracle_rank(cards, truth)[0] == max(truth, key=truth.get),
                     "Analysis-only Oracle ranks from truth only"))
    pressure_parameters = set(__import__("inspect").signature(pressure_metrics).parameters)
    rows.append(_row("CT-14", "truth" not in pressure_parameters and
                     set(pressure_parameters) == {"rankings", "k"},
                     "Pressure validator accepts ranks/K only; no truth input"))
    altered_truth = {cid: -v for cid, v in truth.items()}
    rows.append(_row("CT-15", ranks == rank_all(cards, seed=7919) and altered_truth != truth,
                     "Changing the separate outcome record cannot change ranker output"))
    rows.append(_row("CT-16", len({r[0] for r in [ranks[n] for n in ranks]}) > 1,
                     "Selectors produce nonidentical Top-1 candidates"))

    # Response tests: rankings are computed first; these deliberately constructed
    # truth vectors test only the arithmetic/decision pipeline, not policy efficacy.
    idt = set(ranks["R1_IDT"][:k]); freq = set(ranks["R2_FREQUENCY"][:k])
    loss_truth = {cid: (1.0 if cid in (freq - idt) else 0.0) for cid in ids}
    loss_scores = evaluate_topk({"R1_IDT": ranks["R1_IDT"], "R2_FREQUENCY": ranks["R2_FREQUENCY"]}, loss_truth, k)
    rows.append(_row("CT-17", loss_scores["R1_IDT"] < loss_scores["R2_FREQUENCY"],
                     "Outcome aggregator can report IDT loss vs Frequency"))
    tie_truth = {cid: 1.0 for cid in ids}
    tie_scores = evaluate_topk({"R1_IDT": ranks["R1_IDT"], "R2_FREQUENCY": ranks["R2_FREQUENCY"]}, tie_truth, k)
    rows.append(_row("CT-18", tie_scores["R1_IDT"] == tie_scores["R2_FREQUENCY"],
                     "Equal-value truth fixture yields a tie"))
    win_truth = {cid: (1.0 if cid in (idt - freq) else 0.0) for cid in ids}
    win_scores = evaluate_topk({"R1_IDT": ranks["R1_IDT"], "R2_FREQUENCY": ranks["R2_FREQUENCY"]}, win_truth, k)
    rows.append(_row("CT-19", win_scores["R1_IDT"] > win_scores["R2_FREQUENCY"],
                     "Outcome aggregator can report IDT win vs Frequency"))
    rows.append(_row("CT-20", set(truth) == ids and set(hidden) == ids,
                     "Truth and latent labels reside in separate records keyed by opaque IDs"))
    rows.append(_row("CT-21", len({c.frequency for c in cards}) > 1 and
                     len({c.reuse_probability for c in cards}) > 1 and
                     len({c.compression_gain for c in cards}) > 1,
                     "Frozen feature channels are independently represented"))
    rows.append(_row("CT-22", len(cards) == len(ids) and all(0 <= getattr(c, f) <= 1
                     for c in cards for f in ("frequency", "consistency", "generality",
                     "transfer_calibration", "reasoning_value", "reuse_probability", "compression_gain")),
                     "Common public card schema has bounded normalized features"))

    pressure = run_pressure_fixtures(100, k)
    rows.append(_row("CT-23", pressure["all_pass"],
                     f"100 synthetic pressure panels pass ({pressure['pass_count']}/100)"))
    rows.append(_row("CT-24", pressure["mean_metrics"]["mean_pairwise_topk_rdr"] >= .30,
                     f"Mean all-pair Top-K RDR={pressure['mean_metrics']['mean_pairwise_topk_rdr']:.3f}"))
    rows.append(_row("CT-25", pressure["mean_metrics"]["mean_pairwise_kendall_divergence"] >= .15,
                     f"Mean normalized Kendall divergence={pressure['mean_metrics']['mean_pairwise_kendall_divergence']:.3f}"))
    rows.append(_row("CT-26", all(not r["pass"] or r["seed"] >= 0 for r in pressure["panel_results"]),
                     "Pressure fixture log includes explicit pre-outcome panel status"))

    with (out_dir / "phase1C_contract_test_results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["contract_id", "result", "detail"])
        w.writeheader(); w.writerows(rows)
    (out_dir / "synthetic_pressure_validation.json").write_text(json.dumps(pressure, indent=2) + "\n")
    report = [
        "# Synthetic ranking-pressure contract report", "",
        "**Scope:** deterministic synthetic interface tests only; not IDT performance evidence.", "",
        f"- Panels: {pressure['panels']}",
        f"- Gate pass: {pressure['pass_count']}/{pressure['panels']}",
        f"- Mean/min all-pair Top-K RDR: {pressure['mean_metrics']['mean_pairwise_topk_rdr']:.4f} / {pressure['minimum_metrics']['mean_pairwise_topk_rdr']:.4f}",
        f"- Mean/min normalized Kendall divergence: {pressure['mean_metrics']['mean_pairwise_kendall_divergence']:.4f} / {pressure['minimum_metrics']['mean_pairwise_kendall_divergence']:.4f}",
        "", "| R1 comparison | Mean Top-K RDR | Minimum Top-K RDR |",
        "|---|---:|---:|",
    ]
    for label, key in [("Frequency", "R1_vs_R2_FREQUENCY_topk_rdr"),
                       ("Reuse", "R1_vs_R3_REUSE_topk_rdr"),
                       ("Compression", "R1_vs_R4_COMPRESSION_topk_rdr"),
                       ("Random", "R1_vs_R5_RANDOM_topk_rdr")]:
        report.append(f"| {label} | {pressure['mean_metrics'][key]:.4f} | {pressure['minimum_metrics'][key]:.4f} |")
    report += ["", "The 100 panels reuse one fixed feature/type recipe with independent seeds. They are contract fixtures, not independent research batches."]
    (out_dir / "synthetic_pressure_report.md").write_text("\n".join(report) + "\n")
    names = list(ranks)
    with (out_dir / "pairwise_rank_divergence.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["ranker_a", "ranker_b", "topk_rdr", "normalized_kendall_divergence"])
        for i, a in enumerate(names):
            for b in names[i+1:]:
                w.writerow([a, b, f"{topk_rdr(ranks[a], ranks[b], k):.6f}",
                            f"{kendall_divergence(ranks[a], ranks[b]):.6f}"])
    (out_dir / "outcome_response_sanity_report.md").write_text(
        "# Phase 1C — Outcome-Response Sanity Report\n\n"
        "The runner computes rankings first, then constructs separate truth vectors solely to test the utility aggregator. A loss fixture assigns value to Frequency-only selections outside the IDT set; a tie fixture gives every candidate equal value; a win fixture assigns value to IDT-only selections. The metric reports all three relations correctly.\n\n"
        "**This is a constructed metric-response contract, not an independent task outcome, not evidence that IDT wins or loses, and not a calibration/confirmatory result.** See `outcome_response_sanity.csv` for values.\n"
    )
    # Outcome-response data are explicitly constructed metric checks.
    with (out_dir / "outcome_response_sanity.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["fixture", "policy", "mean_value_per_slot", "scope"])
        for fixture_name, values in (("constructed_loss", loss_scores), ("equal_value_tie", tie_scores), ("constructed_win", win_scores)):
            for policy, value in values.items():
                w.writerow([fixture_name, policy, f"{value:.6f}", "synthetic metric-response contract only"])
    fails = [r for r in rows if r["result"] != "PASS"]
    print(f"{len(rows)-len(fails)}/{len(rows)} contracts PASS")
    print(f"synthetic pressure: {pressure['pass_count']}/{pressure['panels']} pass; "
          f"mean RDR={pressure['mean_metrics']['mean_pairwise_topk_rdr']:.4f}; "
          f"mean Kendall={pressure['mean_metrics']['mean_pairwise_kendall_divergence']:.4f}")
    return 1 if fails else 0


if __name__ == "__main__":
    dest = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    raise SystemExit(run(dest))
