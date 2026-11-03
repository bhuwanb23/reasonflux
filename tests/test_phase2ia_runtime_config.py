from __future__ import annotations

import pytest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from core.invariant import Invariant, InvariantEvidence, InvariantType
from experiments.phase2ia.runtime_config import (
    CandidateIdentityLedger,
    IdentityCollisionError,
    build_invariant_policy,
    build_mining_config,
    build_trace_miner,
    load_frozen_runtime_config,
    phase2i_structural_violations,
)


def _invariant(families=("family-a","family-b"), signature=("apply_rotate_90","verify_demonstrations")):
    fam=list(families)
    return Invariant(
        invariant_id="fixture-id",pattern_signature=list(signature),frequency=5,
        consistency=1.0,generality=2/3,origin="trace_mining",task_families=fam,
        invariant_type=InvariantType.TRANSFER,
        evidence=InvariantEvidence(observations=5,task_families=fam),
        source_trace_ids=["trace-1","trace-2"],
    )


def test_frozen_config_builds_exact_miner_and_policy_values():
    config,digest=load_frozen_runtime_config()
    assert len(digest)==64
    mining=build_mining_config(config)
    policy=build_invariant_policy(config)
    assert (mining.min_frequency,mining.min_cross_trace,mining.max_fragment_length,mining.min_core_length)==(5,5,4,1)
    assert mining.successful_trace_bias is True
    assert (policy.min_frequency,policy.min_consistency,policy.min_task_families)==(5,1.0,2)
    assert policy.require_transfer_evidence is False and policy.min_transfer_events==0
    assert build_trace_miner(config).config.min_core_length==1


def test_transfer_typed_candidate_can_pass_phase2i_preoutcome_structure_only():
    candidate=_invariant()
    assert candidate.invariant_type is InvariantType.TRANSFER
    assert phase2i_structural_violations(candidate)==[]
    one_family=_invariant(("family-a",))
    violations=phase2i_structural_violations(one_family)
    assert any(v.rule=="generality" for v in violations)


def test_identity_omits_family_but_keeps_arm_denominators_separate():
    ledger=CandidateIdentityLedger()
    r1=_invariant(("family-a","family-b"))
    r3=_invariant(("family-a","family-b"))
    assert ledger.register("R1",r1)
    assert ledger.register("R3",r3)
    duplicate=_invariant(("family-c",))
    assert not ledger.register("R1",duplicate)
    assert ledger.count("R1")==ledger.count("R3")==1
    shared=ledger.shared_ids()
    assert len(shared)==1
    candidate_id=next(iter(shared))
    assert ledger.records("R1")[candidate_id].task_families=={"family-a","family-b","family-c"}
    assert ledger.records("R3")[candidate_id].task_families=={"family-a","family-b"}


def test_identity_ledger_fails_closed_on_payload_collision():
    ledger=CandidateIdentityLedger()
    ledger._check_payload("INV-short","{\"origin\":\"trace_mining\",\"pattern\":[\"a\"]}")
    with pytest.raises(IdentityCollisionError):
        ledger._check_payload("INV-short","{\"origin\":\"trace_mining\",\"pattern\":[\"b\"]}")


def test_transfer_evidence_cannot_be_enabled_in_phase2i_structural_gate():
    from invariants.specification.policy import InvariantPolicy
    policy=InvariantPolicy(require_transfer_evidence=True,min_transfer_events=1)
    with pytest.raises(ValueError,match="must not require future transfer"):
        phase2i_structural_violations(_invariant(),policy)
