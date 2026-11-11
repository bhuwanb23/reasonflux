"""Experiment-local Phase-13D contracts; these tests never run the benchmark."""
from solver.grid import Grid
from core.skill import Skill
from experiments.phase13d.baselines import compressed_chunks
from experiments.phase13d.statistics import metric_bundle, performance
from experiments.phase13d.task_programs import execute_program, make_experiment_tasks
from experiments.phase13d.policies import init_policy_state, run_policy


def test_reference_interpreter_exact_hand_calculated_outputs():
    grid = Grid.from_rows([[0, 1], [2, 0]])
    assert execute_program(grid, ("apply_reflection",)).to_rows() == [[1, 0], [0, 2]]
    assert execute_program(grid, ("apply_rotation",)).to_rows() == [[2, 0], [0, 1]]
    assert execute_program(grid, ("count_objects",)) == 2
    assert execute_program(grid, ("group_by_color",)) == {1: 1, 2: 1}
    assert execute_program(grid, ("count_groups",)) == 2
    composite = execute_program(grid, ("apply_reflection", "count_objects"))
    assert composite == {"grid": [[1, 0], [0, 2]], "count_objects": 2}


def test_prefix_operation_preserves_requested_count_schema_but_can_harm_cost():
    grid = Grid.from_rows([[0, 1, 0], [0, 0, 2], [0, 0, 0]])
    task = make_experiment_tasks("EXP-TR-15", 900, 1)[0]
    expected = execute_program(task.input_grid, task.ops)
    actual = execute_program(task.input_grid, task.ops, prefix_ops=("apply_reflection",))
    assert actual == expected  # reflection preserves component count
    skill = Skill(skill_id="stub-reflection", trigger_conditions=["apply_reflection"],
                  metadata={"mvp_category": "reflection", "provisional": True})
    pool = [{"skill": skill, "op": "apply_reflection", "family": "reflection", "SCV10": 1.0}]
    row = run_policy(task, "EXP15_FORCED_REFLECTION", pool, [], [],
                     state=init_policy_state(pool, "EXP15_FORCED_REFLECTION", random_seed=1))
    assert row["correct_after"] is True
    assert row["assigned_application"] is True
    assert row["P_after"] < row["P_before"]
    assert row["transfer_steps"] > row["baseline_steps"]


def test_task_streams_are_deterministic_and_cell_ids_are_disjoint():
    ids = set()
    for exp in ("EXP-TR-01", "EXP-TR-04", "EXP-TR-07", "EXP-TR-10", "EXP-TR-15"):
        first = make_experiment_tasks(exp, 901, 10)
        second = make_experiment_tasks(exp, 901, 10)
        assert [t.task_id for t in first] == [t.task_id for t in second]
        assert not ids.intersection(t.task_id for t in first)
        ids.update(t.task_id for t in first)


def test_compression_uses_longest_exact_chunk_and_unmatched_items():
    library = [("apply_reflection",), ("apply_rotation", "count_objects")]
    assert compressed_chunks(("apply_rotation", "count_objects", "apply_reflection"), library) == [
        ("apply_rotation", "count_objects"), ("apply_reflection",)
    ]


def test_metric_formulas_keep_unavailable_search_counter_null():
    rows = [
        {"P_before": 0.8, "P_after": 0.9, "baseline_steps": 10, "transfer_steps": 5,
         "correct_before": True, "correct_after": True, "assigned_application": True,
         "reused": True, "taxonomy": "near", "retrieval_candidates_evaluated": 3},
        {"P_before": 0.8, "P_after": 0.6, "baseline_steps": 10, "transfer_steps": 20,
         "correct_before": True, "correct_after": False, "assigned_application": True,
         "reused": True, "taxonomy": "near", "retrieval_candidates_evaluated": 2},
    ]
    result = metric_bundle(rows)
    assert abs(result["TS"]["mean"] - (-0.05)) < 1e-9
    assert result["RCR_steps"] == -5
    assert result["NTR_accuracy"] == 0.5
    assert result["NTR_harm"] == 0.5
    assert result["retrieval_candidates_evaluated"] == 5
    assert result["solver_search_candidates"] is None
    assert performance(True, 5) == 0.9


def test_no_learning_policy_equals_frozen_reference_baseline():
    task = make_experiment_tasks("EXP-TR-04", 902, 1)[0]
    row = run_policy(task, "B1_NO_LEARNING", [], [], [],
                     state=init_policy_state([], "B1_NO_LEARNING", random_seed=1))
    assert row["correct_after"] is True
    assert row["P_after"] == row["P_before"]
    assert row["transfer_steps"] == row["baseline_steps"]
