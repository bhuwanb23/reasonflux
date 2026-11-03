"""Strict train-only loader for the WP3 family-annotation packets.

The loader accepts an exact allowlist of keys instead of scanning for
suspicious names. Anything that is not a task ID plus training input/output
demonstrations is rejected, so test fields, solver programs, traces,
candidate yield, or pre-filled family labels cannot enter the workflow.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

Grid = tuple[tuple[int, ...], ...]

PRIMARY_FAMILIES: tuple[str, ...] = (
    "OBJ_RELATION",
    "SPATIAL_CHANGE",
    "COLOR_ATTRIBUTE",
    "COUNT_REPLICATION",
    "PATTERN_COMPLETION",
    "REGION_TOPOLOGY",
    "FRAME_BOUNDS",
    "SYMBOLIC_SEQUENCE",
    "COMPOSITE_RULE",
    "UNKNOWN_AMBIGUOUS",
)
CONFIDENCE_LEVELS: tuple[str, ...] = ("HIGH", "MEDIUM", "LOW")
ROW_KEYS = frozenset({"task_id", "train_pairs", "annotation"})
ANNOTATION_KEYS = frozenset(
    {
        "primary_family",
        "secondary_tags",
        "confidence",
        "evidence_pair_indices",
        "rationale",
        "ambiguity_notes",
    }
)
PAIR_KEYS = frozenset({"input", "output"})


class PacketBoundaryError(ValueError):
    """Raised when a packet violates the train-only annotation boundary."""


@dataclass(frozen=True, slots=True)
class TrainTask:
    task_id: str
    grids: tuple[tuple[Grid, Grid], ...]
    raw_pairs: tuple[Mapping[str, Any], ...]
    train_pairs_sha256: str


@dataclass(frozen=True, slots=True)
class Packet:
    path: str
    sha256: str
    tasks: tuple[TrainTask, ...]

    def by_id(self) -> dict[str, TrainTask]:
        return {task.task_id: task for task in self.tasks}


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _grid(raw: Any, where: str) -> Grid:
    if not isinstance(raw, list) or not raw:
        raise PacketBoundaryError(f"{where}: grid must be a nonempty list of rows")
    width = None
    rows: list[tuple[int, ...]] = []
    for row_index, row in enumerate(raw):
        if not isinstance(row, list) or not row:
            raise PacketBoundaryError(f"{where}: row {row_index} must be a nonempty list")
        if width is None:
            width = len(row)
        elif len(row) != width:
            raise PacketBoundaryError(f"{where}: grid must be rectangular")
        for value in row:
            if type(value) is not int or not 0 <= value <= 9:
                raise PacketBoundaryError(f"{where}: cells must be integer colours in 0..9")
        rows.append(tuple(row))
    return tuple(rows)


def _task(row: Any, line_no: int) -> TrainTask:
    label = f"line {line_no}"
    if not isinstance(row, dict):
        raise PacketBoundaryError(f"{label}: packet row must be a JSON object")
    if set(row) != ROW_KEYS:
        raise PacketBoundaryError(f"{label}: row keys must be exactly {sorted(ROW_KEYS)}")
    task_id = row["task_id"]
    if not isinstance(task_id, str) or not task_id.strip():
        raise PacketBoundaryError(f"{label}: task_id must be a nonempty string")
    annotation = row["annotation"]
    if not isinstance(annotation, dict) or set(annotation) != ANNOTATION_KEYS:
        raise PacketBoundaryError(f"{label}: annotation block must be the frozen blank template")
    if annotation["primary_family"] or annotation["confidence"] or annotation["rationale"]:
        raise PacketBoundaryError(f"{label}: packet must not ship pre-filled labels")
    if annotation["secondary_tags"] or annotation["evidence_pair_indices"]:
        raise PacketBoundaryError(f"{label}: packet must not ship pre-filled tags or evidence")
    pairs = row["train_pairs"]
    if not isinstance(pairs, list) or not pairs:
        raise PacketBoundaryError(f"{label}: train_pairs must be a nonempty list")
    grids: list[tuple[Grid, Grid]] = []
    raw_pairs: list[Mapping[str, Any]] = []
    for pair_index, pair in enumerate(pairs):
        where = f"{label}: pair {pair_index}"
        if not isinstance(pair, dict) or set(pair) != PAIR_KEYS:
            raise PacketBoundaryError(f"{where}: pair keys must be exactly input and output")
        grids.append((_grid(pair["input"], f"{where} input"), _grid(pair["output"], f"{where} output")))
        raw_pairs.append({"input": pair["input"], "output": pair["output"]})
    return TrainTask(
        task_id=task_id,
        grids=tuple(grids),
        raw_pairs=tuple(raw_pairs),
        train_pairs_sha256=canonical_sha256(raw_pairs),
    )


def load_packet(path: Path | str, *, expected_count: int | None = 600) -> Packet:
    packet_path = Path(path)
    if not packet_path.is_file():
        raise PacketBoundaryError(f"packet not found: {packet_path}")
    payload = packet_path.read_bytes()
    tasks: list[TrainTask] = []
    for line_no, line in enumerate(payload.decode("utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise PacketBoundaryError(f"line {line_no}: invalid JSON") from exc
        tasks.append(_task(row, line_no))
    ids = [task.task_id for task in tasks]
    if len(set(ids)) != len(ids):
        raise PacketBoundaryError("packet contains duplicate task IDs")
    if expected_count is not None and len(tasks) != expected_count:
        raise PacketBoundaryError(f"expected {expected_count} tasks, found {len(tasks)}")
    if not tasks:
        raise PacketBoundaryError("packet is empty")
    return Packet(path=packet_path.as_posix(), sha256=hashlib.sha256(payload).hexdigest(), tasks=tuple(tasks))


def verify_against_manifest(packet: Packet, manifest_path: Path | str) -> dict[str, bool]:
    """Cross-check packet bytes and every training pair against the frozen manifest."""
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    name = Path(packet.path).name
    expected_file = manifest.get("packet_sha256", {}).get(name)
    if expected_file != packet.sha256:
        raise PacketBoundaryError(f"{name}: packet hash does not match the frozen manifest")
    expected_pairs = manifest.get("train_pair_hashes_sha256", {})
    for task in packet.tasks:
        if expected_pairs.get(task.task_id) != task.train_pairs_sha256:
            raise PacketBoundaryError(f"{task.task_id}: training pairs do not match the frozen manifest")
    if manifest.get("task_count") != len(packet.tasks):
        raise PacketBoundaryError("manifest task_count does not match the packet")
    if str(manifest.get("test_data_access", "")).upper().find("NOT DECODED") < 0:
        raise PacketBoundaryError("manifest does not record a train-only access boundary")
    return {
        "packet_hash_matches_manifest": True,
        "all_train_pair_hashes_match": True,
        "task_count_matches_manifest": True,
        "manifest_records_train_only_access": True,
    }


def assert_no_prohibited_fields(raw_row: Mapping[str, Any]) -> None:
    """Guard for callers that re-serialise a row before writing an artifact."""
    allowed_top = {"task_id", "train_pairs", "annotation", "grids"}
    unexpected = {key for key in raw_row if key not in allowed_top}
    if unexpected:
        raise PacketBoundaryError(f"unexpected fields would be written: {sorted(unexpected)}")
    for pair in raw_row.get("train_pairs", ()):
        if set(pair) != PAIR_KEYS:
            raise PacketBoundaryError("training pair must expose only input and output")
