"""Path-confined source for pre-approved train-only task artifacts.

No ARC task file is opened by the module until a caller explicitly constructs
this source with a separate allowed task-ID-to-path map. Each file is read only
through the first top-level `train` array using WP3's streaming extractor.
"""
from __future__ import annotations
from pathlib import Path
from typing import Mapping, Any
import hashlib, json

from experiments.phase2ia.build_annotation_packets import TrainOnlyBoundaryError, extract_training_pairs

class TrainOnlyPathError(ValueError): pass

class _PrefixByteLimit:
    def __init__(self,stream:Any,max_bytes:int): self.stream=stream; self.max_bytes=max_bytes; self.read_bytes=0
    def read(self,n:int=-1)->bytes:
        if n<0: raise TrainOnlyBoundaryError("unbounded reads are forbidden")
        remaining=self.max_bytes-self.read_bytes
        if remaining<=0: raise TrainOnlyBoundaryError("train prefix exceeded byte limit")
        data=self.stream.read(min(n,remaining+1)); self.read_bytes+=len(data)
        if self.read_bytes>self.max_bytes: raise TrainOnlyBoundaryError("train prefix exceeded byte limit")
        return data

class TrainOnlyFileSource:
    def __init__(self, *, allowed_root:Path, task_files:Mapping[str,Path], max_train_prefix_bytes:int=2_097_152):
        if type(max_train_prefix_bytes) is not int or not 1<=max_train_prefix_bytes<=4_194_304:
            raise TrainOnlyPathError("train-prefix byte limit must be in [1, 4194304]")
        self.max_train_prefix_bytes=max_train_prefix_bytes
        self.allowed_root=allowed_root.resolve(strict=True)
        if not self.allowed_root.is_dir(): raise TrainOnlyPathError("allowed source root must be a directory")
        if not task_files: raise TrainOnlyPathError("explicit task-file allowlist is required")
        resolved={}; relative_paths={}
        for task_id,path in task_files.items():
            if not isinstance(task_id,str) or not task_id.strip(): raise TrainOnlyPathError("empty task ID in allowlist")
            p=Path(path).resolve(strict=True)
            if not p.is_file() or not p.is_relative_to(self.allowed_root):
                raise TrainOnlyPathError(f"source path is outside allowed root: {path}")
            if task_id in resolved: raise TrainOnlyPathError(f"duplicate task ID: {task_id}")
            resolved[task_id]=p
            relative_paths[task_id]=p.relative_to(self.allowed_root).as_posix()
        self._task_files=resolved
        payload=json.dumps({"root":self.allowed_root.as_posix(),"task_files":relative_paths},sort_keys=True,separators=(",",":"))
        self.allowlist_sha256=hashlib.sha256(payload.encode()).hexdigest()

    @property
    def task_ids(self)->tuple[str,...]: return tuple(sorted(self._task_files))

    def load(self,task_id:str)->dict[str,Any]:
        try: path=self._task_files[task_id]
        except KeyError as exc: raise TrainOnlyPathError(f"task ID is not on the explicit path allowlist: {task_id}") from exc
        # The extractor requires `train` first and stops at its closing bracket.
        with path.open("rb",buffering=0) as stream:
            pairs=extract_training_pairs(_PrefixByteLimit(stream,self.max_train_prefix_bytes))
        return {"train":pairs}

    __call__=load
