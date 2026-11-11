"""F7 task family diversity."""

import pytest

from core import Task
from invariants.robustness import (
    compute_tfd_from_tasks,
    low_diversity_warning,
    meets_multi_family,
)
from core import Invariant, InvariantEvidence


def test_low_tfd_warning():
    tasks = [Task(task_id=f"t{i}", task_family="reflect", input_state={}) for i in range(5)]
    assert compute_tfd_from_tasks(tasks) == pytest.approx(0.2)
    assert low_diversity_warning(tasks)


def test_multi_family_hard_gate():
    inv = Invariant(
        invariant_id="x",
        pattern_signature=["a"],
        frequency=5,
        task_families=["only"],
        evidence=InvariantEvidence(observations=5),
    )
    assert not meets_multi_family(inv)
