"""TransferGraph edges, neighbors, from_records."""

from transfer import TransferGraph, TransferRecord, TransferType


def test_add_edge_neighbors_and_invariants_between():
    g = TransferGraph()
    g.add_edge("reflect", "count", weight=1.0, invariant_id="INV-r")
    g.add_edge("reflect", "group", weight=1.0, invariant_id="INV-r")
    g.add_edge("reflect", "count", weight=1.0, invariant_id="INV-r2")

    assert g.neighbors("reflect") == ["count", "group"]
    assert g.invariants_between("reflect", "count") == ["INV-r", "INV-r2"]
    assert g.nodes() == ["count", "group", "reflect"]


def test_from_records_only_successful_edges():
    records = [
        TransferRecord(
            invariant_id="INV-r",
            source_family="reflect",
            target_family="count",
            success=True,
            benefit=0.8,
            transfer_type=TransferType.MODERATE,
        ),
        TransferRecord(
            invariant_id="INV-r",
            source_family="reflect",
            target_family="pure_count",
            success=False,
            benefit=0.0,
            transfer_type=TransferType.MODERATE,
        ),
        TransferRecord(
            invariant_id="INV-r",
            source_family="reflect",
            target_family="group",
            success=True,
            benefit=0.7,
            transfer_type=TransferType.COMPOSITIONAL,
        ),
    ]
    g = TransferGraph.from_records(records)
    assert "count" in g.neighbors("reflect")
    assert "group" in g.neighbors("reflect")
    assert "pure_count" not in g.neighbors("reflect")
    assert "pure_count" in g.nodes()
    payload = g.to_dict()
    assert "nodes" in payload and "edges" in payload
