"""Fail-closed paired Phase 2I runner interface; ARC execution is not authorized.

The runner only accepts a demonstrations-only provider. It never reads ARC
files itself. Synthetic replay is permitted for QA; ARC mode additionally
requires a separate owner authorization manifest bound to the exact run hashes.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from enum import StrEnum
import csv, hashlib, json, multiprocessing, time
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from core.trace import ReasoningTrace
from representations.r3 import Action, ParseStatus, parse_grid
from traces.semantic_adapter import Representation, adapt_successful_candidate, validate_semantic_trace
from experiments.phase2ia.runtime_config import (
    CandidateIdentityLedger, build_trace_miner, load_frozen_runtime_config,
    phase2i_structural_violations,
)
from experiments.phase2ia.hcc_control import assert_no_hcc_task_in_arc_inputs

ROOT=Path(__file__).resolve().parents[2]
FORBIDDEN_KEYS=frozenset({"test","testoutput","testoutputs","predictedtest","predictedtestoutput",
 "hidden","hiddenoutput","hiddenoutcome","evaluationanswer","answergrid","targettest","oracletest"})
ARMS=frozenset({"R1","R3"})
STOP_REASONS=frozenset({"EXACT_FIT_FOUND","NO_FIT_WITHIN_LANGUAGE","CANDIDATE_BUDGET_EXHAUSTED",
 "INVALID_INPUT","RESOURCE_LIMIT","PARSE_FAILED","SELECTOR_AMBIGUOUS"})

class RunMode(StrEnum):
    SYNTHETIC_REPLAY="SYNTHETIC_REPLAY"
    ARC_PHASE2I="ARC_PHASE2I"

@dataclass(frozen=True,slots=True)
class ResourceLimits:
    max_tasks:int=600
    max_candidate_trials:int=10
    max_training_pairs_per_task:int=10
    max_grid_cells:int=900
    max_search_seconds:float=30.0
    max_address_space_mib:int=2048
    def __post_init__(self):
        if (self.max_tasks<1 or self.max_tasks>600 or self.max_candidate_trials<1 or self.max_candidate_trials>10
            or self.max_training_pairs_per_task<1 or self.max_training_pairs_per_task>10
            or self.max_grid_cells<1 or self.max_grid_cells>900
            or self.max_search_seconds<=0 or self.max_search_seconds>30
            or self.max_address_space_mib<1 or self.max_address_space_mib>2048):
            raise ValueError("invalid Phase 2I resource limits; caps cannot exceed 600 tasks, ten trials/demos, 900 cells, 30 seconds, or 2048 MiB address space")

@dataclass(frozen=True,slots=True)
class SearchObservation:
    parse_status:str
    search_status:str
    trial_count:int
    stop_reason:str
    candidate_id:str|None=None
    operation:str|Action|None=None
    trial_candidate_ids:tuple[str,...]=()

@dataclass(frozen=True,slots=True)
class TaskLedger:
    task_id:str
    train_demonstrations_sha256:str
    parse_status:str
    search_status:str
    trial_count:int
    stop_reason:str
    trial_candidate_ids:tuple[str,...]
    candidate_id:str|None
    trace_status:str

@dataclass(frozen=True,slots=True)
class StageLedger:
    tasks_submitted:int
    parsed_valid:int
    search_trials:int
    exact_demo_fits:int
    valid_semantic_traces:int
    raw_patterns:int
    aggregated_structures:int
    candidate_proposals:int
    generator_accepted:int
    generator_rejected:int
    structurally_eligible:int
    arm_unique_candidate_ids:int

@dataclass(frozen=True,slots=True)
class ArmArtifact:
    schema_version:str
    mode:str
    arm:str
    task_ids:tuple[str,...]
    task_list_sha256:str
    source_allowlist_sha256:str|None
    frozen_config_sha256:str
    family_map_sha256:str
    runner_code_sha256:str
    semantic_adapter_sha256:str
    search_adapter_sha256:str
    grammar_sha256:str
    implementation_sha256:str
    limits:ResourceLimits
    records:tuple[TaskLedger,...]
    stages:StageLedger
    candidate_ids:tuple[str,...]
    authorization_sha256:str|None
    protocol_sha256:str|None

@dataclass(frozen=True,slots=True)
class PairedArtifact:
    r1:ArmArtifact
    r3:ArmArtifact
    paired_task_order_equal:bool
    identical_limits:bool
    synthetic_only:bool

SearchFn=Callable[[str,str,tuple[Mapping[str,Any],...],int],SearchObservation]
TrainOnlyLoader=Callable[[str],Mapping[str,Any]]


def sha256_file(path:Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def load_allowed_task_ids(path:Path) -> tuple[str,...]:
    """Read an explicit newline-delimited ID file; reject duplicates/empty IDs."""
    ids=tuple(line.strip() for line in path.read_text().splitlines() if line.strip())
    if not ids or len(ids)!=len(set(ids)):
        raise ValueError("allowed task-ID file must contain unique nonempty IDs")
    if any(x.startswith("HCC-") for x in ids):
        raise ValueError("HCC IDs are not ARC candidate-production IDs")
    return ids


def _canonical_key(key:Any)->str:
    return "".join(ch.lower() for ch in str(key) if ch.isalnum())

def audit_forbidden_fields(value:Any,path:str="$" )->None:
    """Recursively reject hidden/test/outcome-bearing field names."""
    if isinstance(value,Mapping):
        for key,child in value.items():
            canon=_canonical_key(key)
            if canon in FORBIDDEN_KEYS or canon.startswith("testoutput") or canon.startswith("predictedtest"):
                raise ValueError(f"forbidden field at {path}.{key}")
            audit_forbidden_fields(child,f"{path}.{key}")
    elif isinstance(value,(list,tuple)):
        for i,child in enumerate(value): audit_forbidden_fields(child,f"{path}[{i}]")


def audit_run_artifact(value:Any,path:str="$" )->None:
    """Reject test/outcome fields and any raw train/input/output payload in run artifacts."""
    audit_forbidden_fields(value,path)
    def walk(node:Any,loc:str)->None:
        if isinstance(node,Mapping):
            for key,child in node.items():
                if _canonical_key(key) in {"train","trainpairs","input","output"}:
                    raise ValueError(f"raw demonstration field forbidden in run artifact at {loc}.{key}")
                walk(child,f"{loc}.{key}")
        elif isinstance(node,(list,tuple)):
            for i,child in enumerate(node): walk(child,f"{loc}[{i}]")
    walk(value,path)


def audit_output_directory(root:Path,allowed_relative_paths:Sequence[str])->dict[str,str]:
    """Enforce exact output-file allowlist, scan JSON/JSONL/CSV, and hash artifacts."""
    base=root.resolve(strict=True)
    allowed=set(allowed_relative_paths)
    if not allowed: raise ValueError("output artifact allowlist must not be empty")
    for rel in allowed:
        p=Path(rel)
        if p.is_absolute() or ".." in p.parts or not rel or "\\" in rel:
            raise ValueError(f"unsafe artifact path in allowlist: {rel}")
    actual={p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
    if actual!=allowed:
        raise ValueError(f"artifact path allowlist mismatch; unexpected={sorted(actual-allowed)}, missing={sorted(allowed-actual)}")
    hashes={}
    for rel in sorted(allowed):
        unresolved=base/rel
        if unresolved.is_symlink(): raise ValueError(f"symlink artifact path is forbidden: {rel}")
        path=unresolved.resolve(strict=True)
        if not path.is_relative_to(base): raise ValueError(f"artifact path escapes root: {rel}")
        raw=path.read_bytes()
        if b"FORBIDDEN_TEST_OUTPUT_SENTINEL" in raw: raise ValueError("forbidden test-output sentinel in serialized artifact")
        if path.suffix.lower()==".json":
            audit_run_artifact(json.loads(raw))
        elif path.suffix.lower()==".jsonl":
            for line_no,line in enumerate(raw.decode("utf-8").splitlines(),1):
                audit_run_artifact(json.loads(line),f"{rel}:{line_no}")
        elif path.suffix.lower()==".csv":
            rows=list(csv.DictReader(raw.decode("utf-8").splitlines()))
            audit_run_artifact(rows,rel)
        else:
            raise ValueError(f"unregistered run-artifact extension: {rel}")
        hashes[rel]=hashlib.sha256(raw).hexdigest()
    return hashes


def validate_train_only_payload(payload:Mapping[str,Any],limits:ResourceLimits)->tuple[Mapping[str,Any],...]:
    """Accept only a train-only envelope and exact input/output demo pairs."""
    if not isinstance(payload,Mapping): raise ValueError("train-only loader must return a mapping")
    audit_forbidden_fields(payload)
    if set(payload)!={"train"}: raise ValueError("train-only payload must contain exactly the 'train' field")
    pairs=payload["train"]
    if not isinstance(pairs,(list,tuple)) or not pairs or len(pairs)>limits.max_training_pairs_per_task:
        raise ValueError("train demonstrations missing or above resource cap")
    validated=[]
    for pair in pairs:
        if not isinstance(pair,Mapping) or set(pair)!={"input","output"}:
            raise ValueError("each train pair must contain exactly input and output")
        for name in ("input","output"):
            grid=pair[name]
            parsed=parse_grid(grid)
            if parsed.status is ParseStatus.INVALID_INPUT:
                raise ValueError(f"invalid train {name} grid: {parsed.error}")
            if parsed.height*parsed.width>limits.max_grid_cells:
                raise ValueError(f"train {name} grid exceeds registered cell limit")
        validated.append({"input":pair["input"],"output":pair["output"]})
    return tuple(validated)


def _require_arc_authorization(auth:Mapping[str,Any]|None,*,task_hash:str,source_hash:str,config_hash:str,family_hash:str,limits_hash:str,
                               runner_hash:str,adapter_hash:str,search_hash:str,arm:str,grammar_hash:str,
                               implementation_hash:str)->tuple[str,str]:
    if not isinstance(auth,Mapping): raise PermissionError("ARC run requires a separate run-specific authorization manifest")
    required={"status","protocol_sha256","task_list_sha256","source_allowlist_sha256","config_sha256","family_map_sha256","limits_sha256","runner_sha256","semantic_adapter_sha256","search_adapter_sha256","arm","grammar_sha256","implementation_sha256"}
    if set(auth)!=required or auth.get("status")!="AUTHORIZED":
        raise PermissionError("ARC authorization manifest is missing or not explicitly AUTHORIZED")
    for key,value in (("task_list_sha256",task_hash),("source_allowlist_sha256",source_hash),("config_sha256",config_hash),("family_map_sha256",family_hash),
                      ("limits_sha256",limits_hash),("runner_sha256",runner_hash),("semantic_adapter_sha256",adapter_hash),
                      ("search_adapter_sha256",search_hash),("arm",arm),("grammar_sha256",grammar_hash),
                      ("implementation_sha256",implementation_hash)):
        if auth.get(key)!=value: raise PermissionError(f"authorization hash/arm mismatch: {key}")
    for key in ("protocol_sha256","task_list_sha256","source_allowlist_sha256","config_sha256","family_map_sha256","limits_sha256","runner_sha256","semantic_adapter_sha256","search_adapter_sha256","grammar_sha256","implementation_sha256"): 
        if not isinstance(auth.get(key),str) or len(auth[key])!=64 or any(c not in "0123456789abcdef" for c in auth[key]):
            raise PermissionError(f"invalid authorization digest: {key}")
    return hashlib.sha256(json.dumps(dict(auth),sort_keys=True,separators=(",",":")).encode()).hexdigest(),str(auth["protocol_sha256"])


def _opaque_candidate_id(value:str)->str:
    if not isinstance(value,str) or not value or len(value)>512:
        raise RuntimeError("candidate ID must be a bounded nonempty string")
    return "CID-"+hashlib.sha256(value.encode("utf-8")).hexdigest()


def _search_worker(pipe,search,arm,task_id,demos,limits):
    try:
        import resource
        cap=limits.max_address_space_mib*1024*1024
        resource.setrlimit(resource.RLIMIT_AS,(cap,cap))
        result=search(arm,task_id,demos,limits.max_candidate_trials)
        pipe.send(("ok",result))
    except BaseException as exc:
        try: pipe.send(("error",type(exc).__name__,str(exc)))
        except BaseException: pass
    finally:
        pipe.close()


def _invoke_search(search:SearchFn,arm:str,task_id:str,demos:tuple[Mapping[str,Any],...],limits:ResourceLimits)->SearchObservation:
    """Run each task search in a memory-capped child with a hard wall timeout."""
    if "fork" not in multiprocessing.get_all_start_methods():
        raise RuntimeError("this runner requires OS process isolation with fork support")
    ctx=multiprocessing.get_context("fork")
    parent,child=ctx.Pipe(duplex=False)
    proc=ctx.Process(target=_search_worker,args=(child,search,arm,task_id,demos,limits),daemon=True)
    start=time.monotonic(); proc.start(); child.close()
    try:
        if not parent.poll(limits.max_search_seconds):
            if proc.is_alive(): proc.terminate()
            proc.join(timeout=2)
            raise RuntimeError("candidate search exceeded wall-clock limit")
        try: message=parent.recv()
        except EOFError as exc: raise RuntimeError("search worker exited without a result (resource or process failure)") from exc
        proc.join(timeout=2)
        if proc.is_alive(): proc.terminate(); proc.join()
        if time.monotonic()-start>limits.max_search_seconds:
            raise RuntimeError("candidate search exceeded wall-clock limit")
        if not message or message[0]!="ok":
            detail=message[2] if message and len(message)>2 else "unknown child failure"
            raise RuntimeError(f"candidate search worker failed: {detail}")
        return message[1]
    finally:
        parent.close()
        if proc.is_alive(): proc.terminate(); proc.join()


def run_registered_arm(*,arm:str,mode:RunMode|str,task_ids:Sequence[str],loader:TrainOnlyLoader,
  search:SearchFn,family_map:Mapping[str,str],limits:ResourceLimits,grammar_hash:str,
  implementation_hash:str,authorization:Mapping[str,Any]|None=None)->ArmArtifact:
    """Run an injected search callback on train-only payloads and emit audited ledgers."""
    arm=str(arm); mode=RunMode(mode)
    if arm not in ARMS: raise ValueError("arm must be registered R1 or R3")
    ids=tuple(task_ids)
    if not ids or len(ids)>limits.max_tasks or len(ids)!=len(set(ids)):
        raise ValueError("task IDs must be unique, nonempty, and within resource cap")
    loader_ids=getattr(loader,"task_ids",None)
    if loader_ids is not None and set(ids)!=set(loader_ids):
        raise ValueError("source file allowlist and run task-ID list must match exactly")
    if set(ids)!=set(family_map) or any(not str(family_map[x]).strip() for x in ids):
        raise ValueError("an explicit external family map is required for every allowed ID")
    if any(x.startswith("HCC-") for x in ids): raise ValueError("HCC tasks cannot enter the paired runner")
    if len(grammar_hash)!=64 or len(implementation_hash)!=64 or any(c not in "0123456789abcdef" for c in grammar_hash+implementation_hash):
        raise ValueError("grammar and implementation hashes must be lowercase SHA-256")
    cfg,config_hash=load_frozen_runtime_config()
    task_hash=hashlib.sha256(("\n".join(ids)+"\n").encode()).hexdigest()
    source_hash=getattr(loader,"allowlist_sha256",None)
    family_payload=json.dumps({task:str(family_map[task]) for task in ids},sort_keys=True,separators=(",",":"),ensure_ascii=True)
    family_hash=hashlib.sha256(family_payload.encode()).hexdigest()
    runner_hash=sha256_file(Path(__file__).resolve())
    adapter_hash=sha256_file(ROOT/"src/traces/semantic_adapter.py")
    search_adapter_hash=sha256_file(Path(__file__).with_name("search_adapters.py"))
    limits_json=json.dumps(asdict(limits),sort_keys=True,separators=(",",":"))
    limits_hash=hashlib.sha256(limits_json.encode()).hexdigest()
    auth_hash=None; protocol_hash=None
    if mode is RunMode.ARC_PHASE2I:
        auth_hash,protocol_hash=_require_arc_authorization(authorization,task_hash=task_hash,source_hash=source_hash,config_hash=config_hash,
          family_hash=family_hash,limits_hash=limits_hash,runner_hash=runner_hash,adapter_hash=adapter_hash,
          search_hash=search_adapter_hash,arm=arm,grammar_hash=grammar_hash,implementation_hash=implementation_hash)
        from experiments.phase2ia.train_only_source import TrainOnlyFileSource
        if not isinstance(loader,TrainOnlyFileSource) or not isinstance(source_hash,str):
            raise PermissionError("ARC mode requires the path-confined train-only source")
        from experiments.phase2ia.search_adapters import registered_searchers
        if search is not registered_searchers()[arm]:
            raise PermissionError("ARC mode only accepts the frozen registered R1/R3 search callback")
        assert_no_hcc_task_in_arc_inputs([x for x in ids if x.startswith("HCC-")],ids)
    elif authorization is not None:
        raise ValueError("synthetic replay must not be presented with ARC authorization")
    records=[]; traces:list[ReasoningTrace]=[]; trials=0; parsed=0; fits=0
    for task_id in ids:
        demos=validate_train_only_payload(loader(task_id),limits)
        demo_json=json.dumps(demos,sort_keys=True,separators=(",",":"),ensure_ascii=True)
        demo_hash=hashlib.sha256(demo_json.encode()).hexdigest()
        parsed+=1
        obs=_invoke_search(search,arm,task_id,demos,limits)
        if not isinstance(obs,SearchObservation): raise TypeError("search callback must return SearchObservation")
        if obs.parse_status not in {p.value for p in ParseStatus}:
            raise RuntimeError(f"unregistered parser status for {task_id}")
        allowed_search={"FOUND_EXACT_DEMO_FIT","NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET","INVALID_INPUT","RESOURCE_LIMIT"}
        if obs.search_status not in allowed_search or obs.stop_reason not in STOP_REASONS:
            raise RuntimeError(f"unregistered search status/stop reason for {task_id}")
        if obs.trial_count<0 or obs.trial_count>limits.max_candidate_trials:
            raise RuntimeError(f"candidate search exceeded registered cap for {task_id}")
        if len(obs.trial_candidate_ids)!=obs.trial_count or len(set(obs.trial_candidate_ids))!=len(obs.trial_candidate_ids):
            raise RuntimeError("candidate trial IDs must be complete and unique")
        opaque_trial_ids=tuple(_opaque_candidate_id(cid) for cid in obs.trial_candidate_ids)
        trials+=obs.trial_count
        if obs.parse_status==ParseStatus.INVALID_INPUT.value and obs.search_status!="INVALID_INPUT":
            raise RuntimeError("invalid parse cannot proceed to candidate search")
        opaque_candidate_id=None
        if obs.search_status=="FOUND_EXACT_DEMO_FIT":
            if obs.parse_status==ParseStatus.INVALID_INPUT.value or obs.trial_count<1:
                raise RuntimeError("exact-fit result requires a valid parse and at least one counted trial")
            if not obs.candidate_id or obs.operation is None: raise RuntimeError("exact-fit result lacks candidate lineage/operation")
            if not obs.trial_candidate_ids or obs.trial_candidate_ids[-1]!=obs.candidate_id:
                raise RuntimeError("first-fit candidate must be the final logged trial")
            opaque_candidate_id=_opaque_candidate_id(obs.candidate_id)
            fits+=1
            adapted=adapt_successful_candidate(representation=Representation(arm),operation=obs.operation,
              task_id=task_id,candidate_id=obs.candidate_id,grammar_hash=grammar_hash,
              implementation_hash=implementation_hash,trial_index=max(obs.trial_count,1),trace_id=f"{arm}-{task_id}-T1")
            validate_semantic_trace(adapted)
            projected=adapted.mining_projection(independent_task_family=str(family_map[task_id]))
            traces.append(projected); trace_status="VALID"
        else:
            if obs.candidate_id is not None or obs.operation is not None:
                raise RuntimeError("non-fit search result must not carry candidate or operation")
            trace_status="NO_PRIMARY_TRACE"
        records.append(TaskLedger(task_id,demo_hash,obs.parse_status,obs.search_status,obs.trial_count,
          obs.stop_reason,opaque_trial_ids,opaque_candidate_id,trace_status))
    miner=build_trace_miner(cfg); mining=miner.mine(traces)
    identity_ledger=CandidateIdentityLedger()
    for candidate in mining.candidates: identity_ledger.register(arm,candidate)
    structurally_eligible=sum(not phase2i_structural_violations(c,miner.policy) for c in mining.candidates)
    stages=StageLedger(len(ids),parsed,trials,fits,len(traces),len(mining.success_patterns),len(mining.structures),
      len(mining.candidates)+len(mining.rejected),len(mining.candidates),len(mining.rejected),
      structurally_eligible,identity_ledger.count(arm))
    authorization_sha=auth_hash
    artifact=ArmArtifact("ASFT-2I-RUN-ARTIFACT-V1",mode.value,arm,ids,task_hash,source_hash,config_hash,family_hash,
      runner_hash,adapter_hash,search_adapter_hash,grammar_hash,implementation_hash,limits,tuple(records),stages,
      tuple(sorted(identity_ledger.records(arm))),authorization_sha,protocol_hash)
    audit_run_artifact(asdict(artifact))
    return artifact


def run_paired_from_file(*,task_id_file:Path,loader:TrainOnlyLoader,search_by_arm:Mapping[str,SearchFn],
 family_map:Mapping[str,str],limits:ResourceLimits,hashes:Mapping[str,Mapping[str,str]],
 mode:RunMode|str=RunMode.SYNTHETIC_REPLAY,authorization_by_arm:Mapping[str,Mapping[str,Any]]|None=None)->PairedArtifact:
    """Read the explicit task allowlist then delegate without expanding its scope."""
    ids=load_allowed_task_ids(task_id_file)
    return run_paired(task_ids=ids,loader=loader,search_by_arm=search_by_arm,family_map=family_map,
      limits=limits,hashes=hashes,mode=mode,authorization_by_arm=authorization_by_arm)


def run_paired(*,task_ids:Sequence[str],loader:TrainOnlyLoader,search_by_arm:Mapping[str,SearchFn],
 family_map:Mapping[str,str],limits:ResourceLimits,hashes:Mapping[str,Mapping[str,str]],
 mode:RunMode|str=RunMode.SYNTHETIC_REPLAY,authorization_by_arm:Mapping[str,Mapping[str,Any]]|None=None)->PairedArtifact:
    """Run both arms over exactly the same ordered IDs and budget, then audit outputs."""
    if set(search_by_arm)!=ARMS or set(hashes)!=ARMS: raise ValueError("paired run requires exactly R1 and R3")
    artifacts={}
    for arm in ("R1","R3"):
        artifacts[arm]=run_registered_arm(arm=arm,mode=mode,task_ids=task_ids,loader=loader,
          search=search_by_arm[arm],family_map=family_map,limits=limits,
          grammar_hash=hashes[arm]["grammar_sha256"],implementation_hash=hashes[arm]["implementation_sha256"],
          authorization=(authorization_by_arm or {}).get(arm))
    paired=PairedArtifact(artifacts["R1"],artifacts["R3"],artifacts["R1"].task_ids==artifacts["R3"].task_ids,
      artifacts["R1"].limits==artifacts["R3"].limits,RunMode(mode) is RunMode.SYNTHETIC_REPLAY)
    if not paired.paired_task_order_equal or not paired.identical_limits: raise AssertionError("paired IDs/order/budgets diverged")
    audit_run_artifact(asdict(paired))
    return paired


def serialize_artifact(artifact:PairedArtifact)->str:
    """Stable JSON without task grids or candidate outputs."""
    payload=asdict(artifact); audit_run_artifact(payload)
    return json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=True)
