"""Transfer-aware ranking: T = ITS × TU demotes high-frequency/low-transfer."""

from core import Invariant, InvariantEvidence, InvariantState
from invariants import rank_transfer_aware, transfer_scores_map
from transfer import TransferMemory, TransferRecord, TransferType


def _inv(iid, *, freq, c, g, r, sig=None):
    return Invariant(
        invariant_id=iid,
        pattern_signature=sig or ["find_symmetry", "apply_reflection"],
        frequency=freq,
        consistency=c,
        generality=g,
        transfer_contribution=0.0,
        evidence=InvariantEvidence(observations=freq, transfer_events=0),
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": r},
    )


def _add_successes(mem, iid, benefits, families):
    for benefit, family in zip(benefits, families):
        mem.record(
            TransferRecord(
                invariant_id=iid,
                source_family="reflect",
                target_family=family,
                success=True,
                benefit=benefit,
                reasoning_reduction=0.8,
                transfer_type=TransferType.MODERATE,
            )
        )


def test_high_its_outranks_zero_transfer_despite_lower_frequency():
    reflection = _inv("INV-ref", freq=20, c=0.9, g=0.8, r=0.7)
    verify = _inv(
        "INV-ver",
        freq=50,
        c=1.0,
        g=1.0,
        r=0.0,
        sig=["verify_output"],
    )
    mem = TransferMemory()
    # ITS ≈ 0.8 for reflection; verify has no transfer history → T=0
    _add_successes(mem, "INV-ref", [0.8, 0.8], ["count", "group"])

    ranked = rank_transfer_aware(
        [verify, reflection], mem, total_families=2
    )
    assert ranked[0].invariant.invariant_id == "INV-ref"
    assert ranked[0].scores.transfer > ranked[1].scores.transfer
    assert ranked[1].scores.score == 0.0


def test_transfer_scores_map_weighted_product():
    inv = _inv("INV-ref", freq=10, c=0.9, g=0.5, r=0.5)
    mem = TransferMemory()
    _add_successes(mem, "INV-ref", [1.0, 1.0], ["a", "b"])
    scores = transfer_scores_map([inv], mem, total_families=2)
    assert "INV-ref" in scores
    assert scores["INV-ref"] > 0.0
