"""validate_and_rank with use_hard_gate."""

from core import Invariant, InvariantEvidence, InvariantState
from invariants import validate_and_rank
from invariants.robustness import RobustnessConfig
from transfer import TransferMemory, TransferRecord, TransferType


def _inv(iid, *, freq, c, g, t, r, families=None, obs=None, meta=None):
    return Invariant(
        invariant_id=iid,
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=freq,
        consistency=c,
        generality=g,
        transfer_contribution=t,
        evidence=InvariantEvidence(
            observations=obs or freq, transfer_events=int(t * 3)
        ),
        state=InvariantState.CANDIDATE,
        task_families=families or ["reflect", "count"],
        metadata=meta
        or {
            "reasoning_value": r,
            "variations": ["color", "shape", "position", "count"],
        },
    )


def test_hard_gate_blocks_sparse_promotion():
    sparse = _inv("INV-sp", freq=20, c=0.9, g=0.8, t=0.7, r=0.7, obs=2)
    result = validate_and_rank(
        [sparse],
        use_hard_gate=True,
        robustness_config=RobustnessConfig(),
    )
    assert result.promotable == []


def test_hard_gate_allows_strong_candidate_with_memory():
    inv = _inv("INV-r", freq=20, c=0.9, g=0.8, t=0.7, r=0.7)
    mem = TransferMemory()
    for fam in ("count", "group"):
        mem.record(
            TransferRecord(
                invariant_id="INV-r",
                source_family="reflect",
                target_family=fam,
                success=True,
                benefit=0.8,
                reasoning_reduction=0.8,
                transfer_type=TransferType.MODERATE,
            )
        )
    result = validate_and_rank(
        [inv],
        use_hard_gate=True,
        transfer_memory=mem,
        total_families=2,
    )
    assert len(result.promotable) == 1
