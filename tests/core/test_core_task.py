"""Tests for Task knowledge object."""

import pytest

from core import Task


def test_task_construction():
    task = Task(
        task_id="t1",
        task_family="reflection",
        input_state={"grid": [[1]]},
        expected_outcome={"grid": [[1]]},
        difficulty=1.5,
    )
    assert task.task_id == "t1"
    assert task.task_family == "reflection"
    assert task.difficulty == 1.5


def test_task_rejects_empty_id():
    with pytest.raises(ValueError, match="task_id"):
        Task(task_id="", task_family="reflection", input_state=None)


def test_task_rejects_negative_difficulty():
    with pytest.raises(ValueError, match="difficulty"):
        Task(task_id="t1", task_family="rotation", input_state=None, difficulty=-1)


def test_task_dict_round_trip():
    task = Task(
        task_id="t2",
        task_family="counting",
        input_state=[1, 2, 3],
        expected_outcome=3,
        difficulty=0.5,
        metadata={"source": "synthetic"},
    )
    restored = Task.from_dict(task.to_dict())
    assert restored == task
