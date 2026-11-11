from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from experiments.phase2ia.finalize_package import PKG, REMOTE_WP3, digest  # noqa: E402


def test_remote_wp3_bundle_is_pinned_provisional_and_not_used_for_eligibility():
    remote = REMOTE_WP3
    assert remote["commit"] in remote["source_url"]
    assert remote["status"] == "AI_PROVISIONAL_ONLY_NOT_WP3"
    assert remote["task_count"] == 600
    assert remote["label_mode"] == "AI_PROVISIONAL"
    assert "not independent human" in remote["independence"].lower()
    assert remote["all_map_rows_status"] == "PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN"
    assert remote["family_map_sha256"] == remote["outputs_sha256"]["task_family_map.csv"]
    assert remote["source_packet_sha256"] == digest(
        PKG / "annotation_packets/annotator_A_train_only.jsonl"
    )
    assert remote["human_review"]["reviews_present"] == 0
    assert remote["human_review"]["human_gate_completion_percent"] == 0
    assert remote["human_review"]["all_A_B_C_rows_unreviewed"] is True
    assert remote["human_review"]["adjudication_reviews_present"] == 0

    agreement = remote["agreement"]
    assert agreement["n"] == 600
    assert agreement["exact_matches"] == 476
    assert agreement["cohen_kappa_descriptive"] == 0.7196367336172137
    assert agreement["final_unknown_ambiguous"] == 226
    assert agreement["final_non_unknown"] == 374

    for key in (
        "eligible_for_family_qualification",
        "eligible_for_candidate_eligibility",
        "eligible_for_phase2i_execution",
        "wp3_complete",
        "labels_used_by_runner_or_phase2i",
    ):
        assert remote[key] is False
    assert remote["phase2i_run"] == "NOT AUTHORIZED; NOT RUN"

    # The AI-provisional package exists locally, but only as a clearly marked
    # exploratory artifact. It must not be copied into the annotation packets or
    # treated as human evidence by the candidate runner.
    local_provisional = PKG / "wp3_provisional_v1"
    assert local_provisional.is_dir()
    local_manifest = json.loads(
        (local_provisional / "provisional_manifest.json").read_text(encoding="utf-8")
    )
    assert local_manifest["status"] == "AI_PROVISIONAL_ONLY_NOT_WP3"
    assert all(value is False for value in local_manifest["use_restrictions"].values())
    assert not (PKG / "annotation_packets" / "wp3_provisional_v1").exists()
    assert len(remote["outputs_sha256"]) == 14
    assert remote["review_packet_sha256"] == {
        name: remote["outputs_sha256"][name]
        for name in remote["review_packet_sha256"]
    }
    assert remote["human_review"]["promotion_blockers"]
