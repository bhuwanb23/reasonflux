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


def main() -> dict[str, object]:
    evidence = run_idt_evidence()
    checks = {
        "four_discovery_families": all(
            result["statistics"]["discovery"]["mean"] >= 1.0
            for result in evidence["discovery"].values()
        ),
        "precision_target": evidence["quality"]["statistics"]["IP"]["mean"] >= 0.70,
        "recall_target": evidence["quality"]["statistics"]["IR"]["mean"] >= 0.75,
        "positive_is_ts_correlation": evidence["transfer"]["statistics"]["PEARSON"]["mean"] > 0,
        "variation_survival": evidence["robustness"]["statistics"]["VST"]["mean"] >= 0.60,
        "baseline_comparison": evidence["baselines"]["statistics"]["ASFT"]["mean"]
        >= evidence["baselines"]["statistics"]["random_pattern"]["mean"],
    }
    result = {
        "phase": "13B",
        "success": all(checks.values()),
        "checks": checks,
        "evidence": "reports/experiments/idt_evidence/summary.json",
    }
    path = ROOT / "reports" / "experiments" / "idt_evidence" / "closure.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["success"] else 1)
