"""Explicit CLI entry points; tests must not launch either experiment stage."""
from __future__ import annotations

import argparse
import json
from .calibration import run_calibration
from .reporting import run_confirmation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("calibrate", "confirm"))
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = run_calibration(write=not args.no_write) if args.stage == "calibrate" else run_confirmation(write=not args.no_write)
    stage_seeds = (
        result["calibration_seeds"] if args.stage == "calibrate" else result["seeds"]
    )
    print(
        json.dumps(
            {"stage": args.stage, "seeds": stage_seeds, "status": "complete"},
            indent=2,
        )
    )
