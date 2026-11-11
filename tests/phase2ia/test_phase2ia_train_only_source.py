from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

from experiments.phase2ia.build_annotation_packets import TrainOnlyBoundaryError
from experiments.phase2ia.train_only_source import TrainOnlyFileSource, TrainOnlyPathError


def test_source_reads_only_train_array_and_omits_trailing_test_sentinel(tmp_path):
    root=tmp_path/"allowed";root.mkdir()
    task=root/"demo.json"
    task.write_text('{"train":[{"input":[[0,1]],"output":[[1,0]]}],"test":"FORBIDDEN_TEST_OUTPUT_SENTINEL"}')
    source=TrainOnlyFileSource(allowed_root=root,task_files={"SYNTH-1":task})
    assert source.task_ids==("SYNTH-1",)
    assert source("SYNTH-1")=={"train":[{"input":[[0,1]],"output":[[1,0]]}]}
    with pytest.raises(TrainOnlyPathError,match="not on the explicit path allowlist"):
        source("SYNTH-2")


def test_source_refuses_nontrain_first_and_paths_outside_allowlist(tmp_path):
    root=tmp_path/"allowed";root.mkdir()
    file=root/"not_train_first.json"
    file.write_text('{"test":"FORBIDDEN_TEST_OUTPUT_SENTINEL","train":[]}')
    source=TrainOnlyFileSource(allowed_root=root,task_files={"SYNTH-1":file})
    with pytest.raises(TrainOnlyBoundaryError,match="train must be the first"):
        source("SYNTH-1")
    outside=tmp_path/"outside.json";outside.write_text('{"train":[]}')
    with pytest.raises(TrainOnlyPathError,match="outside allowed root"):
        TrainOnlyFileSource(allowed_root=root,task_files={"SYNTH-2":outside})
