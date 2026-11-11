from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

from experiments.phase2ia.build_annotation_packets import (
    TrainOnlyBoundaryError,
    build_packets,
    extract_training_pairs,
)


def test_train_parser_stops_before_test_field_bytes():
    raw=(b'{"train":[{"input":[[1]],"output":[[2]]}],'
         b'"test":[{"input":[[3]],"output":"HIDDEN_TEST_SENTINEL"}]}')
    stream=BytesIO(raw)
    pairs=extract_training_pairs(stream)
    assert pairs==[{"input":[[1]],"output":[[2]]}]
    assert raw[stream.tell():].startswith(b',"test"')
    assert b"HIDDEN_TEST_SENTINEL" not in json.dumps(pairs).encode()


def test_loader_fails_closed_if_test_field_precedes_train():
    raw=b'{"test":[{"output":"DO_NOT_READ"}],"train":[]}'
    stream=BytesIO(raw)
    try:
        extract_training_pairs(stream)
    except TrainOnlyBoundaryError as exc:
        assert "first top-level field" in str(exc)
    else:
        raise AssertionError("test-first file must be refused")
    assert b"DO_NOT_READ" not in raw[:stream.tell()]


def test_packet_builder_includes_discovery_train_pairs_only(tmp_path: Path):
    arc_root=tmp_path/"datasets"/"arc"
    split_dir=arc_root/"arc-agi-2"
    task_dir=split_dir/"training"
    task_dir.mkdir(parents=True)
    task_path=task_dir/"task-a.json"
    task_path.write_text(
        '{"train":[{"input":[[1,0]],"output":[[0,1]]}],'
        '"test":[{"input":[[2,0]],"output":"HIDDEN_TEST_SENTINEL"}]}',
        encoding="utf-8",
    )
    split_manifest=split_dir/"split_manifest.json"
    split_manifest.write_text(json.dumps({"tasks":[
        {"task_id":"task-a","split":"discovery","path":"arc-agi-2/training/task-a.json"},
        {"task_id":"task-b","split":"transfer","path":"arc-agi-2/training/task-b.json"},
    ]}),encoding="utf-8")
    out=tmp_path/"packets"
    manifest=build_packets(split_manifest,out,expected_count=1)
    assert manifest["task_count"]==1
    assert set(manifest["packet_sha256"])=={"annotator_A_train_only.jsonl","annotator_B_train_only.jsonl"}
    for packet_path in out.glob("annotator_*.jsonl"):
        text=packet_path.read_text(encoding="utf-8")
        row=json.loads(text)
        assert row["task_id"]=="task-a"
        assert row["train_pairs"]==[{"input":[[1,0]],"output":[[0,1]]}]
        assert "HIDDEN_TEST_SENTINEL" not in text
        assert set(row)=={"task_id","train_pairs","annotation"}
    report=(out/"packet_manifest.json").read_text(encoding="utf-8")
    assert "test_pairs" not in report and "HIDDEN_TEST_SENTINEL" not in report
