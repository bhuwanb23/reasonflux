"""Frozen Phase 2I runtime policy and identity helpers (WP4).

These helpers construct the unchanged downstream miner/policy from the
owner-approved WP4 config. They do not load ARC data or run a candidate search.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib, json
from pathlib import Path
from typing import Any, Mapping

from core.invariant import Invariant
from invariants.detector import TraceMiner
from invariants.pattern_mining import MiningConfig
from invariants.specification.identity import InvariantIdentity
from invariants.specification.policy import InvariantPolicy
from invariants.specification.qualification import QualificationViolation, qualify_invariant

ROOT=Path(__file__).resolve().parents[2]
CONFIG_PATH=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1/wp4_runtime_config_v1.json"

class IdentityCollisionError(RuntimeError):
    """A short canonical ID maps to more than one full identity payload."""


def load_frozen_runtime_config(path: Path=CONFIG_PATH) -> tuple[dict[str,Any],str]:
    raw=path.read_bytes()
    config=json.loads(raw)
    if config.get("status")!="OWNER_APPROVED_FROZEN":
        raise ValueError("runtime config is not owner-approved and frozen")
    if config.get("config_id")!="ASFT-V1.1-PHASE-2I-A-WP4-RUNTIME-CONFIG-V1":
        raise ValueError("unexpected runtime config version")
    return config,hashlib.sha256(raw).hexdigest()


def build_mining_config(config: Mapping[str,Any] | None=None) -> MiningConfig:
    cfg=config or load_frozen_runtime_config()[0]
    return MiningConfig.from_dict(dict(cfg["trace_mining"]))


def build_invariant_policy(config: Mapping[str,Any] | None=None) -> InvariantPolicy:
    cfg=config or load_frozen_runtime_config()[0]
    return InvariantPolicy.from_dict(dict(cfg["candidate_policy"]))


def build_trace_miner(config: Mapping[str,Any] | None=None) -> TraceMiner:
    cfg=config or load_frozen_runtime_config()[0]
    return TraceMiner(config=build_mining_config(cfg),policy=build_invariant_policy(cfg))


def phase2i_structural_violations(
    invariant: Invariant, policy: InvariantPolicy | None=None
) -> list[QualificationViolation]:
    """Outcome-blind structural check; transfer evidence/MVP type are not gates.

    The frozen WP4 config disables transfer evidence and the approved call
    deliberately allows InvariantType.TRANSFER for this candidate-population
    diagnostic. This does not perform promotion or make a Skill/Capability.
    """
    policy=policy or build_invariant_policy()
    if policy.require_transfer_evidence:
        raise ValueError("Phase 2I candidate policy must not require future transfer evidence")
    return qualify_invariant(invariant,policy,allow_unsupported_type=True)


def identity_payload(invariant: Invariant) -> dict[str,Any]:
    return {
        "origin":(invariant.origin or "unknown").strip().lower(),
        "pattern":[str(step).strip().lower() for step in invariant.pattern_signature],
    }


def _canonical_payload(payload: Mapping[str,Any]) -> str:
    return json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True)


@dataclass(slots=True)
class CandidateIdentityRecord:
    invariant_id: str
    payload_json: str
    invariant: Invariant
    source_arms: set[str]=field(default_factory=set)
    source_trace_ids: set[str]=field(default_factory=set)
    task_families: set[str]=field(default_factory=set)


class CandidateIdentityLedger:
    """Arm-separated deduplication with cross-arm identity collision checks."""
    ARMS=frozenset({"R1","R3"})
    def __init__(self) -> None:
        self._payload_by_id: dict[str,str]={}
        self._by_arm: dict[str,dict[str,CandidateIdentityRecord]]={a:{} for a in self.ARMS}

    def _check_payload(self,candidate_id:str,payload_json:str) -> None:
        prior=self._payload_by_id.get(candidate_id)
        if prior is not None and prior!=payload_json:
            raise IdentityCollisionError(f"canonical ID collision for {candidate_id}")
        self._payload_by_id[candidate_id]=payload_json

    def register(self,arm:str,invariant:Invariant) -> bool:
        """Register lineage; return True only for a new within-arm unique ID.

        Same IDs across arms are allowed but remain separate arm records/counts.
        Families are aggregated only among duplicate observations inside an arm.
        """
        if arm not in self.ARMS: raise ValueError(f"unregistered representation arm: {arm}")
        identity=InvariantIdentity.from_invariant(invariant)
        payload_json=_canonical_payload(identity_payload(invariant))
        self._check_payload(identity.invariant_id,payload_json)
        arm_records=self._by_arm[arm]
        record=arm_records.get(identity.invariant_id)
        if record is None:
            record=CandidateIdentityRecord(identity.invariant_id,payload_json,invariant)
            arm_records[identity.invariant_id]=record
            is_new=True
        else:
            if record.payload_json!=payload_json: raise IdentityCollisionError(f"within-arm payload mismatch: {identity.invariant_id}")
            is_new=False
        record.source_arms.add(arm)
        record.source_trace_ids.update(str(t) for t in invariant.source_trace_ids)
        record.task_families.update(str(f) for f in invariant.task_families)
        record.task_families.update(str(f) for f in invariant.evidence.task_families)
        return is_new

    def count(self,arm:str) -> int:
        if arm not in self.ARMS: raise ValueError(f"unregistered representation arm: {arm}")
        return len(self._by_arm[arm])

    def shared_ids(self) -> set[str]:
        return set(self._by_arm["R1"]) & set(self._by_arm["R3"])

    def records(self,arm:str) -> Mapping[str,CandidateIdentityRecord]:
        if arm not in self.ARMS: raise ValueError(f"unregistered representation arm: {arm}")
        return dict(self._by_arm[arm])
