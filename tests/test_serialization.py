"""Tests for JSON serialization helpers."""

from pathlib import Path

import pytest

from core import Invariant, Skill, Task
from utils.serialization import load_object, save_object


def test_save_load_task(tmp_path: Path):
    task = Task(
        task_id="t1",
        task_family="counting",
        input_state={"n": 3},
        expected_outcome=3,
    )
    path = tmp_path / "task.json"
    save_object(task, path)
    restored = load_object(path, Task.from_dict)
    assert restored == task


def test_save_load_invariant_and_skill(tmp_path: Path):
    inv = Invariant(
        invariant_id="INV-1",
        pattern_signature=["a", "b"],
        frequency=4,
        consistency=0.5,
        generality=1.0,
    )
    skill = Skill(skill_id="SK-1", source_invariant_id="INV-1", scv=2.0)

    inv_path = tmp_path / "inv.json"
    skill_path = tmp_path / "skill.json"
    save_object(inv, inv_path)
    save_object(skill, skill_path)

    assert load_object(inv_path, Invariant.from_dict).strength == pytest.approx(2.0)
    assert load_object(skill_path, Skill.from_dict).skill_id == "SK-1"


def test_save_object_requires_to_dict(tmp_path: Path):
    with pytest.raises(TypeError):
        save_object(object(), tmp_path / "bad.json")
