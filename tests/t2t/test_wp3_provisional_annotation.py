"""Tests for the WP3 provisional three-agent annotation workflow."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from experiments.phase2ia.wp3_agreement import compute_agreement  # noqa: E402
from experiments.phase2ia.wp3_agents import (  # noqa: E402
    LABEL_MODE,
    Label,
    adjudicate,
    annotate_agent_a,
    annotate_agent_b,
)
from experiments.phase2ia.wp3_evidence import FEATURE_SPECS  # noqa: E402
from experiments.phase2ia.wp3_features import FEATURE_NAMES, extract_features  # noqa: E402
from experiments.phase2ia.wp3_packet_loader import (  # noqa: E402
    ANNOTATION_KEYS,
    PRIMARY_FAMILIES,
    PacketBoundaryError,
    load_packet,
    verify_against_manifest,
)
from experiments.phase2ia.wp3_provisional import (  # noqa: E402
    HEADER_LINES,
    run_provisional_workflow,
    write_bundle,
)

PACKAGE = ROOT / "reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
PACKET = PACKAGE / "annotation_packets/annotator_A_train_only.jsonl"
PACKET_MANIFEST = PACKAGE / "annotation_packets/packet_manifest.json"
ARTIFACT_DIR = PACKAGE / "wp3_provisional_v1"


@pytest.fixture(scope="module")
def bundle():
    return run_provisional_workflow(PACKET, manifest_path=PACKET_MANIFEST)


def _write_packet(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "packet.jsonl"
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    return path


def _blank(task_id: str, pairs: list[dict]) -> dict:
    return {
        "task_id": task_id,
        "train_pairs": pairs,
        "annotation": {key: ([] if key in {"secondary_tags", "evidence_pair_indices"} else "") for key in ANNOTATION_KEYS},
    }


def test_loader_accepts_train_only_packet_and_rejects_any_extra_field(tmp_path: Path):
    good = _write_packet(tmp_path, [_blank("t1", [{"input": [[1]], "output": [[2]]}])])
    packet = load_packet(good, expected_count=1)
    assert packet.tasks[0].task_id == "t1"

    leaky = _blank("t1", [{"input": [[1]], "output": [[2]]}])
    leaky["test_pairs"] = [{"input": [[3]], "output": [[4]]}]
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [leaky]), expected_count=1)


def test_loader_rejects_prefilled_labels_and_bad_ontology_values(tmp_path: Path):
    prefilled = _blank("t1", [{"input": [[1]], "output": [[2]]}])
    prefilled["annotation"]["primary_family"] = "COLOR_ATTRIBUTE"
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [prefilled]), expected_count=1)

    with pytest.raises(ValueError):
        Label(
            task_id="t1",
            agent_id="A",
            primary_family="NOT_A_FAMILY",
            confidence="HIGH",
            evidence_pair_indices=(1,),
            rationale="x",
            ambiguity_notes="",
            secondary_tags=(),
            train_pairs_sha256="0" * 64,
        )


def test_loader_rejects_wrong_task_count_and_duplicate_ids(tmp_path: Path):
    row = _blank("dup", [{"input": [[1]], "output": [[2]]}])
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [row]), expected_count=600)
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [row, row]), expected_count=2)


def test_loader_rejects_malformed_training_grids(tmp_path: Path):
    ragged = _blank("t1", [{"input": [[1, 2], [3]], "output": [[0]]}])
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [ragged]), expected_count=1)
    out_of_palette = _blank("t1", [{"input": [[10]], "output": [[0]]}])
    with pytest.raises(PacketBoundaryError):
        load_packet(_write_packet(tmp_path, [out_of_palette]), expected_count=1)


def test_real_packet_matches_frozen_manifest_and_is_complete(bundle):
    assert len(bundle.packet.tasks) == 600
    assert len({task.task_id for task in bundle.packet.tasks}) == 600
    assert bundle.manifest_checks == {
        "packet_hash_matches_manifest": True,
        "all_train_pair_hashes_match": True,
        "task_count_matches_manifest": True,
        "manifest_records_train_only_access": True,
    }
    packet = load_packet(PACKET)
    assert verify_against_manifest(packet, PACKET_MANIFEST) == bundle.manifest_checks


def test_every_task_gets_three_labels_with_evidence_and_provisional_marker(bundle):
    assert len(bundle.a) == len(bundle.b) == len(bundle.c) == 600
    for left, right, final, task in zip(bundle.a, bundle.b, bundle.c, bundle.packet.tasks):
        for label in (left, right, final):
            assert label.mode == LABEL_MODE
            assert label.primary_family in PRIMARY_FAMILIES
            assert label.evidence_pair_indices
            assert label.rationale.strip()
            assert label.train_pairs_sha256 == task.train_pairs_sha256
        assert final.agent_id == "C"
        assert left.agent_id == "A" and right.agent_id == "B"


def test_agents_and_adjudication_are_deterministic(bundle):
    task = bundle.packet.tasks[0]
    features = extract_features(task.task_id, task.grids)
    first_a = annotate_agent_a(task, features)
    first_b = annotate_agent_b(task, features)
    second_a = annotate_agent_a(task, features)
    second_b = annotate_agent_b(task, features)
    assert first_a.record_hash() == second_a.record_hash()
    assert first_b.record_hash() == second_b.record_hash()
    assert adjudicate(task, features, first_a, first_b).record_hash() == adjudicate(
        task, features, second_a, second_b
    ).record_hash()


def test_feature_specs_only_reference_defined_features():
    defined = set(FEATURE_NAMES)
    for spec in FEATURE_SPECS:
        assert spec.feature in defined, spec.feature
        assert 0.0 < spec.weight <= 1.0


def test_agreement_statistics_are_consistent(bundle):
    result = bundle.agreement
    assert result.n == 600
    assert result.missing_a == result.missing_b == 0
    assert sum(result.marginals_a.values()) == 600
    assert sum(result.marginals_b.values()) == 600
    assert sum(sum(row) for row in result.matrix) == 600
    assert result.marginals_a == {
        family: sum(1 for label in bundle.a if label.primary_family == family) for family in result.category_order
    }
    assert result.marginals_b == {
        family: sum(1 for label in bundle.b if label.primary_family == family) for family in result.category_order
    }
    assert len(result.disagreements) + round(float(result.observed_agreement) * 600) == 600


def _label(task_id: str, family: str) -> Label:
    return Label(
        task_id=task_id,
        agent_id="A",
        primary_family=family,
        confidence="HIGH",
        evidence_pair_indices=(1,),
        rationale="test fixture",
        ambiguity_notes="",
        secondary_tags=(),
        train_pairs_sha256="0" * 64,
    )


def test_kappa_is_one_for_identical_streams_and_negative_for_systematic_disagreement():
    identical = compute_agreement(
        [
            _label("t1", "COLOR_ATTRIBUTE"),
            _label("t2", "COLOR_ATTRIBUTE"),
            _label("t3", "REGION_TOPOLOGY"),
        ],
        [
            _label("t1", "COLOR_ATTRIBUTE"),
            _label("t2", "COLOR_ATTRIBUTE"),
            _label("t3", "REGION_TOPOLOGY"),
        ],
    )
    assert float(identical.cohen_kappa) == 1.0
    assert identical.kappa_defined is True

    crossing = compute_agreement(
        [_label("t1", "COLOR_ATTRIBUTE"), _label("t2", "REGION_TOPOLOGY")],
        [_label("t1", "REGION_TOPOLOGY"), _label("t2", "COLOR_ATTRIBUTE")],
    )
    assert float(crossing.cohen_kappa) == -1.0
    assert set(crossing.disagreements) == {"t1", "t2"}


def test_kappa_is_reported_undefined_when_chance_agreement_is_certain():
    degenerate = compute_agreement([_label("t1", "COLOR_ATTRIBUTE")], [_label("t1", "COLOR_ATTRIBUTE")])
    assert degenerate.kappa_defined is False
    assert degenerate.kappa_display.startswith("undefined")


def test_agreement_requires_matching_task_sets():
    with pytest.raises(ValueError):
        compute_agreement([_label("t1", "COLOR_ATTRIBUTE")], [_label("t2", "COLOR_ATTRIBUTE")])


def test_written_artifacts_are_parseable_hash_pinned_and_marked_provisional(bundle, tmp_path: Path):
    manifest = write_bundle(bundle, tmp_path)

    for name, expected in manifest["outputs_sha256"].items():
        path = tmp_path / name
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected

    for name, fields in (
        ("annotator_A_labels.csv", 600),
        ("annotator_B_labels.csv", 600),
        ("adjudication_log.csv", 600),
        ("task_family_map.csv", 600),
    ):
        with (tmp_path / name).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == fields, name

    with (tmp_path / "task_family_map.csv").open(encoding="utf-8", newline="") as handle:
        family_rows = list(csv.DictReader(handle))
    assert {row["task_id"] for row in family_rows} == {task.task_id for task in bundle.packet.tasks}
    assert all(row["label_mode"] == LABEL_MODE for row in family_rows)
    assert all(row["adjudication_status"] == "PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN" for row in family_rows)
    assert all(row["final_primary_family"] in PRIMARY_FAMILIES for row in family_rows)

    hash_file = (tmp_path / "family_map_hash.txt").read_text(encoding="utf-8")
    recorded = dict(line.split("=", 1) for line in hash_file.strip().splitlines())
    assert recorded["sha256"] == hashlib.sha256((tmp_path / "task_family_map.csv").read_bytes()).hexdigest()
    assert recorded["status"] == "PROVISIONAL_NOT_WP3_ELIGIBLE"

    for name in ("agreement_report.md", "wp3_completion_review.md", "README.md"):
        text = (tmp_path / name).read_text(encoding="utf-8")
        for line in HEADER_LINES:
            assert line in text, (name, line)


def test_manifest_records_hard_non_eligibility_and_train_only_boundary(bundle, tmp_path: Path):
    manifest = write_bundle(bundle, tmp_path)
    assert manifest["status"] == "AI_PROVISIONAL_ONLY_NOT_WP3"
    assert manifest["wp3_status"].startswith("INCOMPLETE")
    assert manifest["phase2i_run"].startswith("NOT AUTHORIZED")
    assert all(value is False for value in manifest["use_restrictions"].values())
    assert manifest["data_access"]["source_is_train_only_packet"] is True
    assert manifest["data_access"]["test_fields_or_outputs_accessed"] is False
    assert manifest["data_access"]["solver_programs_traces_candidate_yield_or_future_values_accessed"] is False
    assert manifest["data_access"]["packet_verified_against_frozen_manifest"] is True
    assert len(manifest["disagreement_task_ids"]) == len(bundle.agreement.disagreements)
    assert sum(manifest["family_distribution"].values()) == 600


def test_committed_artifacts_match_a_fresh_run(bundle):
    """The checked-in provisional bundle must be reproducible from the current code."""
    with (ARTIFACT_DIR / "provisional_manifest.json").open(encoding="utf-8") as handle:
        committed = json.load(handle)
    assert committed["run_id"] == "ASFT-WP3-AI-PROVISIONAL-V1"
    assert committed["task_count"] == 600
    assert committed["agreement"]["n"] == 600
    assert committed["family_map_sha256"] == hashlib.sha256((ARTIFACT_DIR / "task_family_map.csv").read_bytes()).hexdigest()
    assert committed["agreement"]["exact_matches"] == len(bundle.agreement.disagreements) * -1 + 600
    assert committed["disagreement_task_ids"] == list(bundle.agreement.disagreements)


def test_committed_data_artifacts_contain_no_test_or_solver_payloads():
    data_artifacts = (
        "annotator_A_labels.csv",
        "annotator_B_labels.csv",
        "adjudication_log.csv",
        "task_family_map.csv",
        "confusion_matrix.csv",
        "family_map_hash.txt",
        "agreement_report.md",
        "wp3_completion_review.md",
        "README.md",
    )
    forbidden = ("HIDDEN_TEST_SENTINEL", "candidate_yield", "test_pairs", "solver_program", "test_input")
    for name in data_artifacts:
        text = (ARTIFACT_DIR / name).read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text, f"{name} leaked {token}"


def test_manifest_mentions_prohibited_fields_only_in_its_audit_block():
    manifest = json.loads((ARTIFACT_DIR / "provisional_manifest.json").read_text(encoding="utf-8"))
    audit = manifest["data_access"]
    assert audit["test_fields_or_outputs_accessed"] is False
    assert audit["solver_programs_traces_candidate_yield_or_future_values_accessed"] is False
    # The only permitted keys whose names mention prohibited data are the false-valued audit flags.
    def walk(node, path="root"):
        if isinstance(node, dict):
            for key, value in node.items():
                yield path, key, value
                yield from walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                yield from walk(value, f"{path}[{index}]")

    for path, key, value in walk(manifest):
        if any(token in key for token in ("test", "candidate_yield", "solver", "trace")):
            assert path.startswith("root.data_access") or path.startswith("root.source_packet"), (path, key)
            assert value is False or isinstance(value, str)
