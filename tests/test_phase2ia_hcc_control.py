from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import pytest
from experiments.phase2ia.hcc_control import HCC_VERSION, RULES, assert_no_hcc_task_in_arc_inputs, build_hcc_tasks, run_hcc_control


def test_hcc_generator_is_balanced_train_demo_only_synthetic_corpus():
    tasks=build_hcc_tasks()
    assert len(tasks)==120
    assert {rule:sum(t.rule_family==rule for t in tasks) for rule in RULES}=={r:20 for r in RULES}
    assert {cohort:sum(t.synthetic_family==cohort for t in tasks) for cohort in ("layout_a","layout_b","layout_c")}=={
        "layout_a":40,"layout_b":40,"layout_c":40}
    assert all(t.task_id.startswith("HCC-") for t in tasks)
    assert_no_hcc_task_in_arc_inputs([t.task_id for t in tasks],[])
    with pytest.raises(ValueError,match="cannot enter ARC inputs"):
        assert_no_hcc_task_in_arc_inputs([tasks[0].task_id],[tasks[0].task_id])
    assert all(len(t.demonstrations)==2 for t in tasks)
    assert all(all(len(d.input_grid)==7 and len(d.output_grid)==7 for d in t.demonstrations) for t in tasks)


def test_hcc_oracle_equivalence_and_frozen_candidate_miner_plumbing():
    result=run_hcc_control()
    assert result.control_version==HCC_VERSION=="ASFT-2I-HCC-SYNTH-V1"
    assert result.task_count==120
    assert result.training_pair_count==240
    assert result.r1_equivalent_demo_checks==240
    assert result.r3_equivalent_demo_checks==240
    assert result.r1_traces==result.r3_traces==120
    assert result.r1_candidates==result.r3_candidates==6
    assert result.r1_structurally_eligible==result.r3_structurally_eligible==6
    assert result.identical_candidate_signatures
    assert result.scope=="SYNTHETIC_PLUMBING_ONLY_NOT_ARC_EVIDENCE"
