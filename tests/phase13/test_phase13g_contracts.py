from __future__ import annotations

import json
from pathlib import Path

from experiments.phase13g.common import (
    DATA, PROGRAMS, apply_program, infer_context, load_split, solve_task, symmetry_demo_property, trace_for,
)


def test_static_geometry_programs_fit_all_examples():
    demos = [
        {"input": [[1, 0], [2, 3]], "output": [[0, 1], [3, 2]]},
        {"input": [[4, 5, 6]], "output": [[6, 5, 4]]},
    ]
    assert infer_context("reflect_horizontal", demos) == {}


def test_constant_translation_infers_task_specific_parameters():
    demos = [{"input": [[1, 0, 0], [0, 0, 0]], "output": [[0, 1, 0], [0, 0, 0]]}]
    context = infer_context("translate_constant", demos)
    assert context == {"dy": 0, "dx": 1, "bg": 0}
    assert apply_program("translate_constant", ((1, 0, 0),), context) == ((0, 1, 0),)


def test_bijective_recolor_maps_consistently():
    demos = [
        {"input": [[1, 2], [2, 1]], "output": [[3, 4], [4, 3]]},
        {"input": [[2, 1]], "output": [[4, 3]]},
    ]
    assert infer_context("recolor_bijection", demos) == {"mapping": {1: 3, 2: 4}}


def test_solver_requires_exact_demo_fit_and_all_test_outputs():
    task = {
        "task_id": "tiny", "split": "unit",
        "train": [{"input": [[1, 2]], "output": [[2, 1]]}],
        "test": [{"input": [[3, 4]], "output": [[4, 3]]},
                {"input": [[5, 6]], "output": [[6, 5]]}],
    }
    result = solve_task(task, PROGRAMS, budget=10)
    assert result["program"] == "reflect_horizontal"
    assert result["demo_fit"] and result["task_exact"]
    assert result["test_pairs"] == 2
    assert trace_for(task, result).outcome.success


def test_unsupported_task_is_not_forced_into_family():
    task = {
        "task_id": "unsupported", "split": "unit",
        "train": [{"input": [[1, 0], [0, 0]], "output": [[1, 1], [1, 1]]}],
        "test": [{"input": [[0, 1], [0, 0]], "output": [[1, 0], [1, 1]]}],
    }
    result = solve_task(task, PROGRAMS, budget=10)
    assert result["family"] == "unsupported_v1"
    assert not result["demo_fit"]
    assert result["failure_type"] == "no_dsl_fit_within_budget"


def test_symmetry_is_recorded_as_property_only():
    task = {"train": [{"input": [[1, 0, 1], [0, 2, 0]], "output": [[1, 0, 1], [0, 2, 0]]}]}
    assert symmetry_demo_property(task)


def test_split_is_disjoint_and_complete():
    discovery, transfer, holdout = load_split()
    sets = [{t["task_id"] for t in group} for group in (discovery, transfer, holdout)]
    assert [len(g) for g in (discovery, transfer, holdout)] == [600, 200, 200]
    assert not sets[0] & sets[1] and not sets[0] & sets[2] and not sets[1] & sets[2]
    assert len(set.union(*sets)) == 1000
    manifest = json.loads((DATA / "split_manifest.json").read_text())
    assert all(r["split"] in {"discovery", "transfer", "holdout"} for r in manifest["tasks"])
