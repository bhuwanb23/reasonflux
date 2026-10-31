"""Backward-compatible read-only post-hoc reporting launcher."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.phase13c.posthoc_figures import write_figures
from experiments.phase13c.posthoc_report import evidence_report

if __name__ == "__main__":
    write_figures()
    evidence_report()
    print("Wrote Phase 13C evidence package and seven figures")
