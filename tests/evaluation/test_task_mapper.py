"""map_related_tasks — cross-family pairs and transfer typing."""

from core import Task
from transfer import TransferType, map_related_tasks


def _task(tid, family):
    return Task(task_id=tid, task_family=family, input_state={})


def test_cross_family_pairs_skip_same_family():
    tasks = [
        _task("t1", "reflect"),
        _task("t2", "reflect"),
        _task("t3", "count"),
    ]
    pairs = map_related_tasks(tasks)
    assert len(pairs) == 2  # t1-t3 and t2-t3
    assert all(p.source_family != p.target_family for p in pairs)
    assert all(p.transfer_type is TransferType.MODERATE for p in pairs)


def test_ops_refine_transfer_type():
    tasks = [_task("a", "reflect"), _task("b", "reflect_count")]
    pairs = map_related_tasks(
        tasks,
        source_ops=["reflect"],
        target_ops_by_family={"reflect_count": ["reflect", "count"]},
    )
    assert len(pairs) == 1
    assert pairs[0].transfer_type is TransferType.COMPOSITIONAL


def test_max_pairs_cap():
    tasks = [_task(f"t{i}", f"fam{i}") for i in range(4)]
    pairs = map_related_tasks(tasks, max_pairs=2)
    assert len(pairs) == 2
