"""Build two blind Phase 2I-A family-coding packets from training demos only.

The loader requires `train` to be the first top-level task-file field and stops
reading immediately after that JSON array. It never decodes a task's `test`
field. Generated rows contain only task_id, training pairs, and blank labels.
"""
from __future__ import annotations
import hashlib, json, random
from pathlib import Path
from typing import BinaryIO, Any

ROOT=Path(__file__).resolve().parents[2]
DEFAULT_SPLIT_MANIFEST=ROOT/"datasets/arc/arc-agi-2/split_manifest.json"
DEFAULT_OUT=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1/annotation_packets"

class TrainOnlyBoundaryError(ValueError):
    pass

class _ByteReader:
    def __init__(self, stream: BinaryIO): self.stream=stream
    def char(self) -> str:
        b=self.stream.read(1)
        if not b: raise TrainOnlyBoundaryError("unexpected EOF before end of train field")
        try: return b.decode("ascii")
        except UnicodeDecodeError as exc: raise TrainOnlyBoundaryError("non-ASCII task JSON is refused by train-only loader") from exc
    def peek(self) -> str:
        pos=self.stream.tell(); c=self.char(); self.stream.seek(pos); return c
    def ws(self) -> str:
        c=self.char()
        while c.isspace(): c=self.char()
        return c
    def json_string(self, first: str='"') -> str:
        if first!='"': raise TrainOnlyBoundaryError("expected JSON string key")
        chars=[first]; escaped=False
        while True:
            c=self.char(); chars.append(c)
            if escaped: escaped=False
            elif c=='\\': escaped=True
            elif c=='"': break
        try: return json.loads("".join(chars))
        except json.JSONDecodeError as exc: raise TrainOnlyBoundaryError("invalid top-level JSON key") from exc
    def array_value(self) -> str:
        first=self.ws()
        if first!='[': raise TrainOnlyBoundaryError("top-level train value must be an array")
        chars=[first]; stack=['[']; in_string=False; escaped=False
        matching={']':'[','}':'{'}
        while stack:
            c=self.char(); chars.append(c)
            if in_string:
                if escaped: escaped=False
                elif c=='\\': escaped=True
                elif c=='"': in_string=False
                continue
            if c=='"': in_string=True
            elif c in '[{': stack.append(c)
            elif c in ']}':
                if not stack or stack[-1]!=matching[c]: raise TrainOnlyBoundaryError("malformed JSON inside train array")
                stack.pop()
        return "".join(chars)


def extract_training_pairs(stream: BinaryIO) -> list[dict[str, Any]]:
    """Decode only a first-position top-level `train` array; never read test value."""
    rd=_ByteReader(stream)
    if rd.ws()!='{': raise TrainOnlyBoundaryError("task file must be a top-level JSON object")
    key=rd.json_string(rd.ws())
    if key!="train":
        raise TrainOnlyBoundaryError("train must be the first top-level field; refusing to inspect other fields")
    if rd.ws()!=':': raise TrainOnlyBoundaryError("missing colon after train key")
    train_text=rd.array_value()
    try: pairs=json.loads(train_text)
    except json.JSONDecodeError as exc: raise TrainOnlyBoundaryError("invalid train array") from exc
    if not isinstance(pairs,list): raise TrainOnlyBoundaryError("train field must be an array")
    clean=[]
    for i,pair in enumerate(pairs):
        if not isinstance(pair,dict) or set(pair)!={"input","output"}:
            raise TrainOnlyBoundaryError(f"train pair {i} must contain exactly input and output")
        for key in ("input","output"):
            grid=pair[key]
            if (not isinstance(grid,list) or not grid or
                any(not isinstance(row,list) or not row for row in grid) or
                len({len(row) for row in grid})!=1 or
                any(type(v) is not int for row in grid for v in row)):
                raise TrainOnlyBoundaryError(f"train pair {i} has invalid {key} grid")
        clean.append({"input":pair["input"],"output":pair["output"]})
    return clean


def _discoveries(manifest_path: Path, expected_count: int | None=600) -> list[dict[str,str]]:
    manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
    rows=[]
    for item in manifest.get("tasks",[]):
        if item.get("split")=="discovery":
            task_id=item.get("task_id")
            rel=item.get("path")
            if not isinstance(task_id,str) or not isinstance(rel,str):
                raise ValueError("discovery manifest row missing task_id/path")
            rows.append({"task_id":task_id,"path":rel})
    if expected_count is not None and len(rows)!=expected_count:
        raise ValueError(f"expected {expected_count} discovery IDs, found {len(rows)}")
    if len({r['task_id'] for r in rows})!=len(rows): raise ValueError("duplicate discovery task IDs")
    return sorted(rows,key=lambda x:x['task_id'])


def build_packets(manifest_path: Path, out_dir: Path, *, expected_count: int | None=600) -> dict[str,Any]:
    """Create randomized coder packets, hashing training-only content only."""
    rows=_discoveries(manifest_path,expected_count)
    source_root=manifest_path.parent.parent
    task_records=[]
    for row in rows:
        file_path=(source_root/row['path']).resolve()
        if not file_path.is_relative_to(source_root.resolve()): raise ValueError("manifest path escapes dataset root")
        with file_path.open("rb",buffering=0) as f:
            pairs=extract_training_pairs(f)
        raw=json.dumps(pairs,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
        task_records.append({"task_id":row['task_id'],"train_pairs":pairs,"train_pairs_sha256":hashlib.sha256(raw).hexdigest()})
    out_dir.mkdir(parents=True,exist_ok=True)
    packet_hashes={}
    for coder,seed in (("A",20261102),("B",20261103)):
        ordered=list(task_records); random.Random(seed).shuffle(ordered)
        output=out_dir/f"annotator_{coder}_train_only.jsonl"
        with output.open("w",encoding="utf-8",newline="\n") as f:
            for row in ordered:
                packet={"task_id":row['task_id'],"train_pairs":row['train_pairs'],
                  "annotation":{"primary_family":"","secondary_tags":[],"confidence":"",
                    "evidence_pair_indices":[],"rationale":"","ambiguity_notes":""}}
                f.write(json.dumps(packet,separators=(",",":"),ensure_ascii=True)+"\n")
        packet_hashes[output.name]=hashlib.sha256(output.read_bytes()).hexdigest()
    try: manifest_ref=manifest_path.resolve().relative_to(ROOT).as_posix()
    except ValueError: manifest_ref=f"synthetic-fixture:{manifest_path.name}"
    manifest={"protocol":"PHASE-2I-A-WP3-TRAIN-ONLY-FAMILY-ANNOTATION-V1",
      "split_manifest":manifest_ref,"included_split":"discovery only",
      "task_count":len(task_records),"annotators":["A","B"],"independent_labels":"blank; not inferred or generated",
      "input_fields":["task_id","train_pairs.input","train_pairs.output"],
      "excluded_fields":["test","test.input","test.output","test_predictions","solver_programs","traces","candidate_yield","future_value","program_derived_family"],
      "train_pair_hashes_sha256":{r['task_id']:r['train_pairs_sha256'] for r in task_records},
      "packet_sha256":packet_hashes,"test_data_access":"NOT DECODED; train-only loader stops at closing bracket of first top-level train array"}
    mpath=out_dir/"packet_manifest.json"
    mpath.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    _audit_packets(out_dir,packet_hashes)
    return manifest


def _audit_packets(out_dir: Path, packet_hashes: dict[str,str]) -> None:
    forbidden={"test","test_output","test_outputs","test_prediction","hidden_evaluation","future_value","solver_program","trace","candidate_yield"}
    for name,expected in packet_hashes.items():
        path=out_dir/name
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected: raise ValueError(f"packet hash mismatch: {name}")
        for line_no,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
            obj=json.loads(line)
            if set(obj)!={"task_id","train_pairs","annotation"}: raise ValueError(f"packet schema violation: {name}:{line_no}")
            if any(key.lower() in forbidden for pair in obj['train_pairs'] for key in pair): raise ValueError("forbidden field in training packet")
            if not all(set(pair)=={"input","output"} for pair in obj['train_pairs']): raise ValueError("non-train pair field in packet")

if __name__=="__main__":
    result=build_packets(DEFAULT_SPLIT_MANIFEST,DEFAULT_OUT)
    print(json.dumps({"task_count":result["task_count"],"packets":result["packet_sha256"],"test_data_access":result["test_data_access"]},indent=2))
