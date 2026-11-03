"""Generate the WP3 provisional three-agent annotation artifacts.

Runs the two annotator passes and the adjudicator over the train-only discovery
packet, then writes the requested CSV/Markdown deliverables plus a hash-pinned
manifest into an isolated directory. The manifest records the hard
non-eligibility boundary so no downstream stage can mistake these labels for
human WP3 evidence.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from experiments.phase2ia.wp3_agreement import AgreementResult, compute_agreement  # noqa: E402
from experiments.phase2ia.wp3_agents import (  # noqa: E402
    LABEL_MODE,
    ONTOLOGY_VERSION,
    POLICY_VERSION,
    Label,
    adjudicate,
    annotate_agent_a,
    annotate_agent_b,
)
from experiments.phase2ia.wp3_features import TaskFeatures, extract_features  # noqa: E402
from experiments.phase2ia.wp3_packet_loader import (  # noqa: E402
    Packet,
    canonical_sha256,
    load_packet,
    verify_against_manifest,
)
from experiments.phase2ia.wp3_reports import (  # noqa: E402
    BANNER,
    HEADER_LINES,
    RUN_ID,
    agreement_markdown,
    completion_review,
    readme,
)

LABEL_FIELDS = (
    "task_id",
    "primary_family",
    "confidence",
    "evidence_pair_indices",
    "secondary_tags",
    "rationale",
    "ambiguity_notes",
    "label_mode",
    "agent_id",
    "ontology_version",
    "policy_version",
    "train_pairs_sha256",
    "record_sha256",
)
ADJUDICATION_FIELDS = (
    "task_id",
    "annotator_a_label",
    "annotator_b_label",
    "final_label",
    "adjudication_status",
    "decision_basis",
    "adjudicator_id",
    "label_mode",
    "train_pairs_sha256",
    "record_sha256",
)
FAMILY_MAP_FIELDS = (
    "task_id",
    "final_primary_family",
    "confidence",
    "annotation_version",
    "adjudication_status",
    "label_mode",
)


@dataclass(frozen=True, slots=True)
class ProvisionalBundle:
    packet: Packet
    features: dict[str, TaskFeatures]
    a: tuple[Label, ...]
    b: tuple[Label, ...]
    c: tuple[Label, ...]
    agreement: AgreementResult
    manifest_checks: dict[str, bool]


def run_provisional_workflow(
    packet_path: Path | str,
    *,
    manifest_path: Path | str | None = None,
    expected_count: int | None = 600,
) -> ProvisionalBundle:
    packet = load_packet(packet_path, expected_count=expected_count)
    checks = verify_against_manifest(packet, manifest_path) if manifest_path else {}
    features = {task.task_id: extract_features(task.task_id, task.grids) for task in packet.tasks}
    a = tuple(annotate_agent_a(task, features[task.task_id]) for task in packet.tasks)
    b = tuple(annotate_agent_b(task, features[task.task_id]) for task in packet.tasks)
    c = tuple(
        adjudicate(task, features[task.task_id], left, right)
        for task, left, right in zip(packet.tasks, a, b)
    )
    return ProvisionalBundle(
        packet=packet,
        features=features,
        a=a,
        b=b,
        c=c,
        agreement=compute_agreement(a, b),
        manifest_checks=checks,
    )


def _write_csv(path: Path, fields: Sequence[str], rows: Iterable[dict[str, str]]) -> None:
    """Write a strictly parseable CSV; AI provenance lives in a required column and the manifest."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _label_row(label: Label) -> dict[str, str]:
    return {
        "task_id": label.task_id,
        "primary_family": label.primary_family,
        "confidence": label.confidence,
        "evidence_pair_indices": ";".join(str(i) for i in label.evidence_pair_indices),
        "secondary_tags": ";".join(label.secondary_tags),
        "rationale": label.rationale,
        "ambiguity_notes": label.ambiguity_notes,
        "label_mode": label.mode,
        "agent_id": label.agent_id,
        "ontology_version": label.ontology_version,
        "policy_version": label.policy_version,
        "train_pairs_sha256": label.train_pairs_sha256,
        "record_sha256": label.record_hash(),
    }


def _adjudication_rows(bundle: ProvisionalBundle) -> list[dict[str, str]]:
    rows = []
    for task, left, right, final in zip(bundle.packet.tasks, bundle.a, bundle.b, bundle.c):
        agreed = left.primary_family == right.primary_family
        rows.append(
            {
                "task_id": task.task_id,
                "annotator_a_label": left.primary_family,
                "annotator_b_label": right.primary_family,
                "final_label": final.primary_family,
                "adjudication_status": "AGREEMENT_RETAINED" if agreed else "DISAGREEMENT_RESOLVED",
                "decision_basis": final.rationale,
                "adjudicator_id": final.agent_id,
                "label_mode": final.mode,
                "train_pairs_sha256": task.train_pairs_sha256,
                "record_sha256": final.record_hash(),
            }
        )
    return rows


def _family_map_rows(bundle: ProvisionalBundle) -> list[dict[str, str]]:
    return [
        {
            "task_id": label.task_id,
            "final_primary_family": label.primary_family,
            "confidence": label.confidence,
            "annotation_version": f"{ONTOLOGY_VERSION}/{POLICY_VERSION}",
            "adjudication_status": "PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN",
            "label_mode": label.mode,
        }
        for label in bundle.c
    ]


def _manifest(bundle: ProvisionalBundle, output: Path, family_map_hash: str, outputs: dict[str, str]) -> dict:
    result = bundle.agreement
    return {
        "artifact_header": list(HEADER_LINES),
        "run_id": RUN_ID,
        "status": "AI_PROVISIONAL_ONLY_NOT_WP3",
        "label_mode": LABEL_MODE,
        "ontology_version": ONTOLOGY_VERSION,
        "policy_version": POLICY_VERSION,
        "source_packet": bundle.packet.path,
        "source_packet_sha256": bundle.packet.sha256,
        "task_count": len(bundle.packet.tasks),
        "task_ids_sha256": canonical_sha256(sorted(task.task_id for task in bundle.packet.tasks)),
        "manifest_checks": bundle.manifest_checks,
        "agreement": {
            "n": result.n,
            "exact_matches": result.n - len(result.disagreements),
            "observed_agreement": float(result.observed_agreement),
            "expected_agreement": float(result.expected_agreement),
            "cohen_kappa_descriptive": result.kappa_float,
            "kappa_defined": result.kappa_defined,
            "unknown_a": result.unknown_a,
            "unknown_b": result.unknown_b,
            "missing_a": result.missing_a,
            "missing_b": result.missing_b,
        },
        "family_distribution": {
            family: sum(1 for label in bundle.c if label.primary_family == family)
            for family in result.category_order
        },
        "disagreement_task_ids": list(result.disagreements),
        "family_map_sha256": family_map_hash,
        "agreement_report_sha256": hashlib.sha256((output / "agreement_report.md").read_bytes()).hexdigest(),
        "adjudication_log_sha256": hashlib.sha256((output / "adjudication_log.csv").read_bytes()).hexdigest(),
        "outputs_sha256": outputs,
        "data_access": {
            "source_is_train_only_packet": True,
            "test_fields_or_outputs_accessed": False,
            "solver_programs_traces_candidate_yield_or_future_values_accessed": False,
            "packet_verified_against_frozen_manifest": bool(bundle.manifest_checks),
        },
        "use_restrictions": {
            "independent_human_annotation": False,
            "family_qualification": False,
            "candidate_eligibility": False,
            "phase2i_execution": False,
            "wp3_completion": False,
            "freeze_as_label_map": False,
        },
        "wp3_status": (
            "INCOMPLETE; two independent human coder streams and a separate human adjudicator remain required"
        ),
        "phase2i_run": "NOT AUTHORIZED; NOT RUN",
    }


def write_bundle(bundle: ProvisionalBundle, out_dir: Path | str) -> dict[str, object]:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    _write_csv(output / "annotator_A_labels.csv", LABEL_FIELDS, (_label_row(label) for label in bundle.a))
    _write_csv(output / "annotator_B_labels.csv", LABEL_FIELDS, (_label_row(label) for label in bundle.b))
    _write_csv(output / "adjudication_log.csv", ADJUDICATION_FIELDS, _adjudication_rows(bundle))
    _write_csv(output / "task_family_map.csv", FAMILY_MAP_FIELDS, _family_map_rows(bundle))

    result = bundle.agreement
    confusion_rows = []
    for position, family in enumerate(result.category_order):
        row = {"annotator_a_label": family}
        row.update({other: str(result.matrix[position][i]) for i, other in enumerate(result.category_order)})
        confusion_rows.append(row)
    _write_csv(output / "confusion_matrix.csv", ("annotator_a_label", *result.category_order), confusion_rows)

    (output / "agreement_report.md").write_text(agreement_markdown(bundle), encoding="utf-8", newline="\n")
    (output / "wp3_completion_review.md").write_text(completion_review(bundle), encoding="utf-8", newline="\n")
    (output / "README.md").write_text(readme(bundle), encoding="utf-8", newline="\n")

    family_map = output / "task_family_map.csv"
    family_map_hash = hashlib.sha256(family_map.read_bytes()).hexdigest()
    (output / "family_map_hash.txt").write_text(
        f"sha256={family_map_hash}\nfile=task_family_map.csv\n"
        f"run_id={RUN_ID}\nlabel_mode={LABEL_MODE}\nstatus=PROVISIONAL_NOT_WP3_ELIGIBLE\n",
        encoding="utf-8",
        newline="\n",
    )

    outputs = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(output.iterdir())
        if path.is_file() and path.name != "provisional_manifest.json"
    }
    manifest = _manifest(bundle, output, family_map_hash, outputs)
    (output / "provisional_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return manifest


def default_paths() -> tuple[Path, Path, Path]:
    root = Path(__file__).resolve().parents[2]
    package = root / "reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
    return (
        package / "annotation_packets/annotator_A_train_only.jsonl",
        package / "annotation_packets/packet_manifest.json",
        package / "wp3_provisional_v1",
    )


def main() -> None:
    packet_path, manifest_path, out_dir = default_paths()
    bundle = run_provisional_workflow(packet_path, manifest_path=manifest_path)
    manifest = write_bundle(bundle, out_dir)
    print(
        json.dumps(
            {
                "task_count": manifest["task_count"],
                "agreement": manifest["agreement"],
                "family_map_sha256": manifest["family_map_sha256"],
                "output_dir": str(out_dir),
            },
            indent=2,
        )
    )


__all__ = [
    "BANNER",
    "HEADER_LINES",
    "ProvisionalBundle",
    "default_paths",
    "run_provisional_workflow",
    "write_bundle",
]

if __name__ == "__main__":
    main()
