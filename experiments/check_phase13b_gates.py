"""Phase 13B IDT evidence closure checker."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from experiments.idt_experiments import run_idt_evidence


def main(*, write: bool = False) -> dict[str, object]:
    evidence = run_idt_evidence(write=write)
    checks = {
        "evidence_package_success": bool(evidence["success"]),
        "four_discovery_families": all(
            result["statistics"]["discovery"]["mean"] >= 1.0
            for result in evidence["discovery"].values()
        ),
        "precision_target": evidence["quality"]["statistics"]["IP"]["mean"] >= 0.70,
        "recall_target": evidence["quality"]["statistics"]["IR"]["mean"] >= 0.75,
        "positive_is_ts_correlation": evidence["transfer"]["statistics"]["PEARSON"]["mean"] > 0,
        "positive_rank_is_ts_correlation": evidence["transfer"]["statistics"]["SPEARMAN"]["mean"] > 0,
        "positive_transfer_score": evidence["transfer"]["statistics"]["TS"]["mean"] > 0,
        "positive_transfer_utility": evidence["transfer"]["statistics"]["TU"]["mean"] > 0,
        "cross_family_transfer": evidence["transfer"]["statistics"]["cross_family_reuse"]["mean"] > 0,
        "cross_family_transfer_rate": evidence["transfer"]["statistics"][
            "cross_family_reuse_rate"
        ]["mean"] > 0,
        "correlation_sample_size": evidence["transfer"]["statistics"]["correlation_n"]["mean"]
        >= 4.0,
        "per_seed_transfer_sample_size": all(
            raw["metrics"]["correlation_n"] >= 4
            and raw["metrics"]["cross_family_reuse"] > 0
            and raw["metrics"]["PEARSON"] > 0
            and raw["metrics"]["SPEARMAN"] > 0
            for raw in evidence["transfer"]["raw_results"]
        ),
        "variation_survival": evidence["robustness"]["statistics"]["VST"]["mean"] >= 0.60,
        "noise_rank_stability": evidence["robustness"]["statistics"]["RANK_STABILITY"]["mean"]
        >= 0.60,
        "sparse_data_is_conservative": evidence["robustness"]["statistics"]["sparse_candidates"]["mean"]
        < evidence["robustness"]["statistics"]["clean_candidates"]["mean"],
        "sparse_data_reduces_strength": evidence["robustness"]["statistics"]["sparse_mean_IS"]["mean"]
        < evidence["robustness"]["statistics"]["clean_mean_IS"]["mean"],
        "sparse_data_avoids_strong_overpromotion": evidence["robustness"]["statistics"]["sparse_strong_fraction"]["mean"]
        <= evidence["robustness"]["statistics"]["clean_strong_fraction"]["mean"],
        "sparse_precision": evidence["robustness"]["statistics"]["sparse_precision"]["mean"]
        >= 0.70,
        "sparse_recall_floor": evidence["robustness"]["statistics"]["sparse_recall"]["mean"]
        >= 0.20,
        "seed_stability": bool(evidence["observations"]["seed_stable"]),
        "baseline_comparison": all(
            raw["metrics"]["ASFT"] > raw["metrics"]["frequency_only"]
            and raw["metrics"]["ASFT"] > raw["metrics"]["no_transfer"]
            and raw["metrics"]["ASFT"] > raw["metrics"]["random_pattern"]
            for raw in evidence["baselines"]["raw_results"]
        ),
    }
    result = {
        "phase": "13B",
        "success": all(checks.values()),
        "checks": checks,
        "evidence": "reports/experiments/idt_evidence/summary.json",
    }
    if write:
        path = ROOT / "reports" / "experiments" / "idt_evidence" / "closure.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    result = main(write=True)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["success"] else 1)
