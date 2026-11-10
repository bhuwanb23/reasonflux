from __future__ import annotations

import multiprocessing

import pytest
import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

pytestmark = pytest.mark.skipif(
    "fork" not in multiprocessing.get_all_start_methods(),
    reason="Phase 2IA runner requires fork-based process isolation (POSIX)",
)

from representations.r3 import Action
from experiments.phase2ia.search_adapters import registered_searchers
from experiments.phase2ia.train_only_source import TrainOnlyFileSource
from experiments.phase2ia.runner import (
    ResourceLimits, RunMode, SearchObservation, audit_forbidden_fields, audit_output_directory, audit_run_artifact,
    run_paired, run_paired_from_file, run_registered_arm, serialize_artifact, validate_train_only_payload,
)

HASH_R1="1"*64
HASH_R3="2"*64
IMPL_R1="3"*64
IMPL_R3="4"*64


def _loader(task_id):
    return {"train":[{"input":[[0,0,0],[0,1,0],[0,0,0]],"output":[[0,0,0],[0,1,0],[0,0,0]]}]}


def _search(arm,task_id,demos,cap):
    assert cap==10 and len(demos)==1
    op="rotate_90" if arm=="R1" else Action.make("rotate",k=1)
    cid=f"C-{arm}-{task_id}"
    return SearchObservation("PARSED","FOUND_EXACT_DEMO_FIT",1,"EXACT_FIT_FOUND",cid,op,(cid,))


def test_paired_synthetic_replay_has_equal_ids_caps_and_separate_provenance():
    ids=tuple(f"SYNTH-{i}" for i in range(6))
    families={task:("family-a" if i<3 else "family-b") for i,task in enumerate(ids)}
    pair=run_paired(task_ids=ids,loader=_loader,search_by_arm={"R1":_search,"R3":_search},
      family_map=families,limits=ResourceLimits(max_tasks=10),hashes={
        "R1":{"grammar_sha256":HASH_R1,"implementation_sha256":IMPL_R1},
        "R3":{"grammar_sha256":HASH_R3,"implementation_sha256":IMPL_R3}},mode=RunMode.SYNTHETIC_REPLAY)
    assert pair.paired_task_order_equal and pair.identical_limits and pair.synthetic_only
    assert pair.r1.task_ids==pair.r3.task_ids==ids
    assert pair.r1.stages.tasks_submitted==pair.r3.stages.tasks_submitted==6
    assert pair.r1.stages.exact_demo_fits==pair.r3.stages.exact_demo_fits==6
    assert pair.r1.stages.valid_semantic_traces==pair.r3.stages.valid_semantic_traces==6
    assert pair.r1.records[0].candidate_id.startswith("CID-")
    assert pair.r3.records[0].candidate_id.startswith("CID-")
    for digest in (pair.r1.family_map_sha256,pair.r1.runner_code_sha256,pair.r1.semantic_adapter_sha256,
                   pair.r1.search_adapter_sha256,pair.r1.records[0].train_demonstrations_sha256):
        assert len(digest)==64
    assert all(value.startswith("CID-") and len(value)==68 for value in pair.r1.records[0].trial_candidate_ids)
    serialized=serialize_artifact(pair)
    assert "test_output" not in serialized and "FORBIDDEN" not in serialized
    assert "input" not in serialized and "output" not in serialized


def test_registered_search_adapters_run_only_within_synthetic_demo_budget():
    ids=("SYNTH-blackout-a","SYNTH-blackout-b")
    def loader(task_id):
        return {"train":[{"input":[[0,0,0],[0,1,0],[0,0,0]],"output":[[0,0,0],[0,0,0],[0,0,0]]}]}
    pair=run_paired(task_ids=ids,loader=loader,search_by_arm=registered_searchers(),
      family_map={ids[0]:"family-a",ids[1]:"family-b"},limits=ResourceLimits(max_tasks=2),hashes={
        "R1":{"grammar_sha256":HASH_R1,"implementation_sha256":IMPL_R1},
        "R3":{"grammar_sha256":HASH_R3,"implementation_sha256":IMPL_R3}})
    assert pair.r1.stages.search_trials==20
    assert pair.r3.stages.search_trials==2
    assert all(row.search_status=="NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET" for row in pair.r1.records)
    assert all(row.search_status=="FOUND_EXACT_DEMO_FIT" for row in pair.r3.records)
    assert all(len(row.trial_candidate_ids)==row.trial_count for row in pair.r1.records+pair.r3.records)


def test_explicit_task_id_file_is_respected_without_expanding_scope(tmp_path):
    path=tmp_path/"synthetic_ids.txt"
    path.write_text("SYNTH-A\nSYNTH-B\n")
    ids=("SYNTH-A","SYNTH-B")
    pair=run_paired_from_file(task_id_file=path,loader=_loader,search_by_arm={"R1":_search,"R3":_search},
      family_map={task:"family-a" for task in ids},limits=ResourceLimits(),hashes={
        "R1":{"grammar_sha256":HASH_R1,"implementation_sha256":IMPL_R1},
        "R3":{"grammar_sha256":HASH_R3,"implementation_sha256":IMPL_R3}})
    assert pair.r1.task_ids==pair.r3.task_ids==ids


def test_end_to_end_synthetic_file_source_search_trace_mining_and_artifact_audit(tmp_path):
    root=tmp_path/"tasks";root.mkdir()
    ids=("SYNTH-FILE-A","SYNTH-FILE-B")
    demo={"train":[{"input":[[0,0,0],[0,1,0],[0,0,0]],"output":[[0,0,0],[0,0,0],[0,0,0]]}],
          "test":"FORBIDDEN_TEST_OUTPUT_SENTINEL"}
    for task_id in ids:(root/f"{task_id}.json").write_text(json.dumps(demo))
    id_file=tmp_path/"ids.txt";id_file.write_text("\n".join(ids)+"\n")
    source=TrainOnlyFileSource(allowed_root=root,task_files={task_id:root/f"{task_id}.json" for task_id in ids})
    pair=run_paired_from_file(task_id_file=id_file,loader=source,search_by_arm=registered_searchers(),
      family_map={ids[0]:"family-a",ids[1]:"family-b"},limits=ResourceLimits(max_tasks=2),hashes={
        "R1":{"grammar_sha256":HASH_R1,"implementation_sha256":IMPL_R1},
        "R3":{"grammar_sha256":HASH_R3,"implementation_sha256":IMPL_R3}})
    assert pair.paired_task_order_equal and pair.identical_limits
    assert pair.r3.stages.exact_demo_fits==2 and pair.r1.stages.exact_demo_fits==0
    assert len(pair.r1.source_allowlist_sha256)==len(pair.r3.source_allowlist_sha256)==64
    assert pair.r1.source_allowlist_sha256==pair.r3.source_allowlist_sha256
    assert "FORBIDDEN_TEST_OUTPUT_SENTINEL" not in serialize_artifact(pair)
    artifact_dir=tmp_path/"artifacts";artifact_dir.mkdir()
    (artifact_dir/"paired.json").write_text(serialize_artifact(pair))
    hashes=audit_output_directory(artifact_dir,["paired.json"])
    assert len(hashes["paired.json"])==64


def test_train_only_loader_rejects_test_output_sentinel_before_search():
    bad={"train":_loader("x")["train"],"test_output":"FORBIDDEN_TEST_OUTPUT_SENTINEL"}
    with pytest.raises(ValueError,match="forbidden field"):
        validate_train_only_payload(bad,ResourceLimits())
    with pytest.raises(ValueError,match="forbidden field"):
        validate_train_only_payload({"train":_loader("x")["train"],"test":[]},ResourceLimits())


def test_arc_mode_fails_closed_without_separate_run_authorization():
    called=[]
    def loader(task_id):
        called.append(task_id)
        return _loader(task_id)
    with pytest.raises(PermissionError,match="separate run-specific authorization"):
        run_registered_arm(arm="R1",mode=RunMode.ARC_PHASE2I,task_ids=("ARC-DEV-1",),loader=loader,
          search=_search,family_map={"ARC-DEV-1":"independently-coded-family"},limits=ResourceLimits(),
          grammar_hash=HASH_R1,implementation_hash=IMPL_R1)
    assert called==[]


def test_hcc_namespace_and_search_trial_budget_are_hard_failures():
    family={"HCC-identity-00":"synthetic-family"}
    with pytest.raises(ValueError,match="HCC tasks cannot enter"):
        run_registered_arm(arm="R1",mode=RunMode.SYNTHETIC_REPLAY,task_ids=("HCC-identity-00",),
          loader=_loader,search=_search,family_map=family,limits=ResourceLimits(),grammar_hash=HASH_R1,implementation_hash=IMPL_R1)
    def over_budget(arm,task_id,demos,cap):
        return SearchObservation("PARSED","NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET",cap+1,"CANDIDATE_BUDGET_EXHAUSTED")
    with pytest.raises(RuntimeError,match="exceeded registered cap"):
        run_registered_arm(arm="R1",mode=RunMode.SYNTHETIC_REPLAY,task_ids=("SYNTH-1",),loader=_loader,
          search=over_budget,family_map={"SYNTH-1":"family-a"},limits=ResourceLimits(),grammar_hash=HASH_R1,implementation_hash=IMPL_R1)


def test_forbidden_field_audit_is_recursive_and_normalizes_names():
    with pytest.raises(ValueError,match="forbidden field"):
        audit_forbidden_fields({"records":[{"predicted_test_outputs":[1]}]})
    with pytest.raises(ValueError,match="raw demonstration field"):
        audit_run_artifact({"rows":[{"input":[[1]]}]})


def test_output_directory_requires_exact_paths_hashes_and_clean_fields(tmp_path):
    (tmp_path/"run.json").write_text('{"status":"SYNTHETIC_REPLAY","count":2}')
    hashes=audit_output_directory(tmp_path,["run.json"])
    assert len(hashes["run.json"])==64
    (tmp_path/"extra.json").write_text("{}")
    with pytest.raises(ValueError,match="allowlist mismatch"):
        audit_output_directory(tmp_path,["run.json"])
    (tmp_path/"extra.json").unlink()
    (tmp_path/"run.json").write_text('{"nested":{"test_output":"FORBIDDEN_TEST_OUTPUT_SENTINEL"}}')
    with pytest.raises(ValueError,match="sentinel|forbidden field"):
        audit_output_directory(tmp_path,["run.json"])


def test_wall_clock_and_grid_cell_limits_fail_closed():
    import time
    def slow(arm,task_id,demos,cap):
        time.sleep(0.05)
        return SearchObservation("PARSED","NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET",0,"NO_FIT_WITHIN_LANGUAGE",None,None,())
    with pytest.raises(RuntimeError,match="wall-clock limit"):
        run_registered_arm(arm="R1",mode=RunMode.SYNTHETIC_REPLAY,task_ids=("SYNTH-SLOW",),loader=_loader,
          search=slow,family_map={"SYNTH-SLOW":"family-a"},limits=ResourceLimits(max_search_seconds=0.01),
          grammar_hash=HASH_R1,implementation_hash=IMPL_R1)
    with pytest.raises(ValueError,match="cell limit"):
        validate_train_only_payload(_loader("x"),ResourceLimits(max_grid_cells=4))
