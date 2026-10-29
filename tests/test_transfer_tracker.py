"""TransferTracker wiring: record → summary → graph → scores."""

import pytest

from transfer import TransferConfig, TransferTracker, TransferType


def test_tracker_record_summary_graph_scores():
    tracker = TransferTracker()
    tracker.record(
        invariant_id="INV-r",
        source_family="reflect",
        target_family="count",
        success=True,
        benefit=0.8,
        reasoning_reduction=0.6,
        transfer_type=TransferType.MODERATE,
    )
    tracker.record(
        invariant_id="INV-r",
        source_family="reflect",
        target_family="group",
        success=True,
        benefit=0.7,
        reasoning_reduction=0.5,
        transfer_type=TransferType.COMPOSITIONAL,
    )

    summary = tracker.summary("INV-r")
    assert summary.attempts == 2
    assert summary.successes == 2
    assert summary.coverage == 2

    graph = tracker.graph()
    assert set(graph.neighbors("reflect")) == {"count", "group"}

    scores = tracker.scores(
        "INV-r", TransferConfig(), total_families=2
    )
    assert scores.attempts == 2
    assert scores.its == pytest.approx(0.75)
    assert scores.ntr == pytest.approx(0.0)
    assert scores.weighted == pytest.approx(scores.its * scores.tu)
