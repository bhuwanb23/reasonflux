"""Deterministic Phase 2F R3 object parser and bounded candidate enumerator.

Implements the owner-approved Phase 2I-A grammar addendum v1. This module is
an isolated representation adapter: it does not read test outputs, emit ASFT
invariants, or run the downstream miner/candidate pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction
import hashlib
import itertools
import json
from typing import Any, Iterable, Mapping, Sequence

R3_GRAMMAR_VERSION = "R3-GRAMMAR-ADDENDUM-V1"
Grid = tuple[tuple[int, ...], ...]
Cell = tuple[int, int]


class ParseStatus(StrEnum):
    PARSED = "PARSED"
    PARSED_NO_OBJECTS = "PARSED_NO_OBJECTS"
    INVALID_INPUT = "INVALID_INPUT"


class SelectionStatus(StrEnum):
    SELECTED = "SELECTED"
    SELECTOR_NO_MATCH = "SELECTOR_NO_MATCH"
    SELECTOR_NOT_UNIQUE = "SELECTOR_NOT_UNIQUE"
    INVALID_SELECTOR = "INVALID_SELECTOR"


class ApplyStatus(StrEnum):
    APPLIED = "APPLIED"
    INVALID_INPUT = "INVALID_INPUT"
    SELECTOR_NO_MATCH = "SELECTOR_NO_MATCH"
    SELECTOR_NOT_UNIQUE = "SELECTOR_NOT_UNIQUE"
    INVALID_ACTION = "INVALID_ACTION"
    OUT_OF_BOUNDS = "OUT_OF_BOUNDS"
    COLLISION = "COLLISION"


class SearchStatus(StrEnum):
    FOUND_EXACT_DEMO_FIT = "FOUND_EXACT_DEMO_FIT"
    NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET = "NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET"
    INVALID_INPUT = "INVALID_INPUT"
    RESOURCE_LIMIT = "RESOURCE_LIMIT"


@dataclass(frozen=True, slots=True)
class ObjectRecord:
    object_id: str
    color: int
    occupied_cells: tuple[Cell, ...]
    bbox: tuple[int, int, int, int]  # top, left, bottom-exclusive, right-exclusive
    height: int
    width: int
    area: int
    centroid_row: tuple[int, int]
    centroid_col: tuple[int, int]
    shape_signature: str
    border_contact: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "color": self.color,
            "occupied_cells": [list(p) for p in self.occupied_cells],
            "bbox": list(self.bbox),
            "height": self.height,
            "width": self.width,
            "area": self.area,
            "centroid_row": list(self.centroid_row),
            "centroid_col": list(self.centroid_col),
            "shape_signature": self.shape_signature,
            "border_contact": self.border_contact,
        }


@dataclass(frozen=True, slots=True)
class ParseResult:
    status: ParseStatus
    grid: Grid | None
    objects: tuple[ObjectRecord, ...]
    error: str | None = None

    @property
    def height(self) -> int:
        return len(self.grid) if self.grid is not None else 0

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0


@dataclass(frozen=True, slots=True)
class Selector:
    kind: str
    value: int | bool | str

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "value": self.value}


@dataclass(frozen=True, slots=True)
class Action:
    kind: str
    params: tuple[tuple[str, int | str], ...] = ()

    @classmethod
    def make(cls, kind: str, **params: int | str) -> Action:
        return cls(kind, tuple(sorted(params.items())))

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, **dict(self.params)}


@dataclass(frozen=True, slots=True)
class Candidate:
    selector: Selector
    action: Action

    def to_dict(self) -> dict[str, Any]:
        return {"action": self.action.to_dict(), "selector": self.selector.to_dict()}

    @property
    def canonical_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    @property
    def candidate_id(self) -> str:
        return "R3-" + hashlib.sha256(self.canonical_json.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class SelectionResult:
    status: SelectionStatus
    selected: ObjectRecord | None = None


@dataclass(frozen=True, slots=True)
class ApplyResult:
    status: ApplyStatus
    grid: Grid | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class Demonstration:
    input_grid: Any
    output_grid: Any


@dataclass(frozen=True, slots=True)
class CandidateTrial:
    trial_index: int
    candidate_id: str
    candidate_json: str
    status: str
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class SearchResult:
    status: SearchStatus
    candidate: Candidate | None
    trials: tuple[CandidateTrial, ...]
    stop_reason: str


def _fraction_pair(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


def _shape_signature(height: int, width: int, local_cells: set[Cell]) -> str:
    bits = "".join("1" if (r, c) in local_cells else "0" for r in range(height) for c in range(width))
    return f"{height}x{width}:{bits}"


def parse_grid(raw: Any) -> ParseResult:
    """Parse a rectangular integer-color grid into deterministic objects.

    Colors are the ARC palette 0..9; background is fixed to 0. Invalid input
    is explicit rather than being treated as an empty scene or a no-fit.
    """
    if not isinstance(raw, (list, tuple)) or not raw:
        return ParseResult(ParseStatus.INVALID_INPUT, None, (), "grid must be a nonempty sequence of rows")
    if any(not isinstance(row, (list, tuple)) for row in raw):
        return ParseResult(ParseStatus.INVALID_INPUT, None, (), "every row must be a sequence")
    width = len(raw[0])
    if width < 1 or any(len(row) != width for row in raw):
        return ParseResult(ParseStatus.INVALID_INPUT, None, (), "grid must be rectangular with nonzero width")
    if any(type(value) is not int or not 0 <= value <= 9 for row in raw for value in row):
        return ParseResult(ParseStatus.INVALID_INPUT, None, (), "cells must be integer colors in 0..9")
    grid: Grid = tuple(tuple(row) for row in raw)
    h, w = len(grid), width
    visited: set[Cell] = set()
    components: list[tuple[int, tuple[Cell, ...]]] = []
    for r in range(h):
        for c in range(w):
            color = grid[r][c]
            if color == 0 or (r, c) in visited:
                continue
            todo = [(r, c)]
            visited.add((r, c))
            cells: list[Cell] = []
            while todo:
                cr, cc = todo.pop()
                cells.append((cr, cc))
                for nr, nc in ((cr - 1, cc), (cr, cc - 1), (cr, cc + 1), (cr + 1, cc)):
                    if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in visited and grid[nr][nc] == color:
                        visited.add((nr, nc))
                        todo.append((nr, nc))
            components.append((color, tuple(sorted(cells))))

    provisional: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
    for color, cells in components:
        top = min(r for r, _ in cells)
        left = min(c for _, c in cells)
        bottom = max(r for r, _ in cells) + 1
        right = max(c for _, c in cells) + 1
        oh, ow = bottom - top, right - left
        local = {(r - top, c - left) for r, c in cells}
        signature = _shape_signature(oh, ow, local)
        key = (top, left, color, signature)
        rows = Fraction(sum(r for r, _ in cells), len(cells))
        cols = Fraction(sum(c for _, c in cells), len(cells))
        obj = {
            "color": color, "occupied_cells": cells, "bbox": (top, left, bottom, right),
            "height": oh, "width": ow, "area": len(cells),
            "centroid_row": _fraction_pair(rows), "centroid_col": _fraction_pair(cols),
            "shape_signature": signature,
            "border_contact": any(r in (0, h - 1) or c in (0, w - 1) for r, c in cells),
        }
        provisional.append((key, obj))
    provisional.sort(key=lambda item: item[0])
    objects = tuple(ObjectRecord(object_id=f"O{i:04d}", **obj) for i, (_, obj) in enumerate(provisional, start=1))
    status = ParseStatus.PARSED if objects else ParseStatus.PARSED_NO_OBJECTS
    return ParseResult(status, grid, objects)


def select_object(parsed: ParseResult, selector: Selector) -> SelectionResult:
    if parsed.grid is None or parsed.status is ParseStatus.INVALID_INPUT:
        return SelectionResult(SelectionStatus.INVALID_SELECTOR)
    objs = parsed.objects
    kind, value = selector.kind, selector.value
    matches: list[ObjectRecord]
    if kind == "exact_color" and type(value) is int and 1 <= value <= 9:
        matches = [o for o in objs if o.color == value]
    elif kind == "area_rank" and type(value) is int and value >= 1:
        areas = sorted({o.area for o in objs}, reverse=True)
        if value > len(areas):
            return SelectionResult(SelectionStatus.SELECTOR_NO_MATCH)
        chosen_area = areas[value - 1]
        matches = [o for o in objs if o.area == chosen_area]
    elif kind == "bbox_shape" and isinstance(value, str):
        matches = [o for o in objs if o.shape_signature == value]
    elif kind == "border_contact" and type(value) is bool:
        matches = [o for o in objs if o.border_contact is value]
    else:
        return SelectionResult(SelectionStatus.INVALID_SELECTOR)
    if not matches:
        return SelectionResult(SelectionStatus.SELECTOR_NO_MATCH)
    if len(matches) != 1:
        return SelectionResult(SelectionStatus.SELECTOR_NOT_UNIQUE)
    return SelectionResult(SelectionStatus.SELECTED, matches[0])


def _in_bounds(cells: Iterable[Cell], height: int, width: int) -> bool:
    return all(0 <= r < height and 0 <= c < width for r, c in cells)


def _place(grid: list[list[int]], cells: Iterable[Cell], color: int, *, allow_overlap: bool = False) -> ApplyStatus:
    cells = tuple(cells)
    h, w = len(grid), len(grid[0])
    if not _in_bounds(cells, h, w):
        return ApplyStatus.OUT_OF_BOUNDS
    if not allow_overlap and any(grid[r][c] != 0 for r, c in cells):
        return ApplyStatus.COLLISION
    for r, c in cells:
        grid[r][c] = color
    return ApplyStatus.APPLIED


def apply_action(parsed: ParseResult, selector: Selector, action: Action) -> ApplyResult:
    if parsed.grid is None or parsed.status is ParseStatus.INVALID_INPUT:
        return ApplyResult(ApplyStatus.INVALID_INPUT, reason="invalid input grid")
    selected = select_object(parsed, selector)
    if selected.status is SelectionStatus.SELECTOR_NO_MATCH:
        return ApplyResult(ApplyStatus.SELECTOR_NO_MATCH, reason=selected.status.value)
    if selected.status is SelectionStatus.SELECTOR_NOT_UNIQUE:
        return ApplyResult(ApplyStatus.SELECTOR_NOT_UNIQUE, reason=selected.status.value)
    if selected.status is not SelectionStatus.SELECTED or selected.selected is None:
        return ApplyResult(ApplyStatus.INVALID_ACTION, reason="invalid selector")
    obj = selected.selected
    rows = [list(row) for row in parsed.grid]
    cells = obj.occupied_cells
    params = dict(action.params)

    if action.kind == "delete" and not params:
        for r, c in cells:
            rows[r][c] = 0
    elif action.kind == "recolor" and set(params) == {"color"} and type(params["color"]) is int and 0 <= params["color"] <= 9:
        for r, c in cells:
            rows[r][c] = params["color"]
    elif action.kind in {"move", "copy"} and set(params) == {"dx", "dy"}:
        dx, dy = params["dx"], params["dy"]
        if type(dx) is not int or type(dy) is not int or not (-2 <= dx <= 2 and -2 <= dy <= 2):
            return ApplyResult(ApplyStatus.INVALID_ACTION, reason="offset outside [-2,2]")
        targets = tuple((r + dy, c + dx) for r, c in cells)
        if action.kind == "move":
            for r, c in cells:
                rows[r][c] = 0
        status = _place(rows, targets, obj.color)
        if status is not ApplyStatus.APPLIED:
            return ApplyResult(status, reason=status.value)
    elif action.kind in {"rotate", "reflect_horizontal_axis", "reflect_vertical_axis"}:
        if action.kind == "rotate":
            if set(params) != {"k"} or type(params.get("k")) is not int or params["k"] not in {1, 2, 3}:
                return ApplyResult(ApplyStatus.INVALID_ACTION, reason="rotation k must be 1, 2, or 3")
            k = params["k"]
        elif params:
            return ApplyResult(ApplyStatus.INVALID_ACTION, reason="reflection takes no parameters")
        top, left, _, _ = obj.bbox
        transformed: list[Cell] = []
        for r, c in cells:
            lr, lc = r - top, c - left
            if action.kind == "rotate":
                if k == 1: nr, nc = lc, obj.height - 1 - lr
                elif k == 2: nr, nc = obj.height - 1 - lr, obj.width - 1 - lc
                else: nr, nc = obj.width - 1 - lc, lr
            elif action.kind == "reflect_horizontal_axis":
                nr, nc = obj.height - 1 - lr, lc
            else:
                nr, nc = lr, obj.width - 1 - lc
            transformed.append((top + nr, left + nc))
        for r, c in cells:
            rows[r][c] = 0
        status = _place(rows, transformed, obj.color)
        if status is not ApplyStatus.APPLIED:
            return ApplyResult(status, reason=status.value)
    elif action.kind == "crop_bbox" and not params:
        top, left, bottom, right = obj.bbox
        cropped = tuple(tuple(row[left:right]) for row in parsed.grid[top:bottom])
        return ApplyResult(ApplyStatus.APPLIED, cropped)
    else:
        return ApplyResult(ApplyStatus.INVALID_ACTION, reason="action name or parameter schema invalid")
    return ApplyResult(ApplyStatus.APPLIED, tuple(tuple(row) for row in rows))


def _selector_domain(parsed_inputs: Sequence[ParseResult]) -> list[Selector]:
    max_objects = max((len(p.objects) for p in parsed_inputs), default=0)
    shapes = sorted({obj.shape_signature for p in parsed_inputs for obj in p.objects})
    selectors = [Selector("exact_color", c) for c in range(1, 10)]
    selectors += [Selector("area_rank", k) for k in range(1, max_objects + 1)]
    selectors += [Selector("bbox_shape", shape) for shape in shapes]
    selectors += [Selector("border_contact", value) for value in (False, True)]
    return sorted(selectors, key=lambda s: json.dumps(s.to_dict(), sort_keys=True, separators=(",", ":")))


def _action_domain() -> list[Action]:
    actions = [Action.make("move", dy=dy, dx=dx) for dy in range(-2, 3) for dx in range(-2, 3)]
    actions += [Action.make("copy", dy=dy, dx=dx) for dy in range(-2, 3) for dx in range(-2, 3)]
    actions += [Action.make("delete")]
    actions += [Action.make("recolor", color=c) for c in range(10)]
    actions += [Action.make("rotate", k=k) for k in (1, 2, 3)]
    actions += [Action.make("reflect_horizontal_axis"), Action.make("reflect_vertical_axis")]
    actions += [Action.make("crop_bbox")]
    return sorted(actions, key=lambda a: json.dumps(a.to_dict(), sort_keys=True, separators=(",", ":")))


def enumerate_candidates(training_inputs: Sequence[Any], *, limit: int = 10) -> tuple[Candidate, ...]:
    """Enumerate the first hypotheses in the frozen canonical-JSON order.

    Selector domains depend only on parsed training inputs, never outputs.
    ``limit`` is capped at the registered maximum of ten.
    """
    if type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("limit must be an integer in [1,10]")
    parsed = [parse_grid(grid) for grid in training_inputs]
    if not parsed or any(p.status is ParseStatus.INVALID_INPUT for p in parsed):
        return ()
    selectors = _selector_domain(parsed)
    actions = _action_domain()
    candidates: list[Candidate] = []
    for action in actions:
        for selector in selectors:
            candidates.append(Candidate(selector, action))
            if len(candidates) == limit:
                return tuple(candidates)
    return tuple(candidates)


def _evaluate(candidate: Candidate, demos: Sequence[Demonstration]) -> tuple[bool, str | None]:
    for index, demo in enumerate(demos):
        parsed = parse_grid(demo.input_grid)
        expected = parse_grid(demo.output_grid)
        if parsed.status is ParseStatus.INVALID_INPUT or expected.status is ParseStatus.INVALID_INPUT:
            return False, f"INVALID_INPUT_DEMO_{index}"
        applied = apply_action(parsed, candidate.selector, candidate.action)
        if applied.status is not ApplyStatus.APPLIED:
            return False, f"DEMO_{index}:{applied.status.value}"
        if applied.grid != expected.grid:
            return False, f"DEMO_{index}:OUTPUT_MISMATCH"
    return True, None


def run_search(demonstrations: Sequence[Demonstration], *, max_trials: int = 10) -> SearchResult:
    """Run deterministic first-fit R3 search on training demonstrations only."""
    if type(max_trials) is not int or not 1 <= max_trials <= 10:
        return SearchResult(SearchStatus.INVALID_INPUT, None, (), "TRIAL_LIMIT_MUST_BE_1_TO_10")
    if not demonstrations:
        return SearchResult(SearchStatus.INVALID_INPUT, None, (), "NO_TRAINING_DEMONSTRATIONS")
    parsed_inputs = [parse_grid(d.input_grid) for d in demonstrations]
    parsed_outputs = [parse_grid(d.output_grid) for d in demonstrations]
    if any(p.status is ParseStatus.INVALID_INPUT for p in parsed_inputs + parsed_outputs):
        return SearchResult(SearchStatus.INVALID_INPUT, None, (), "INVALID_DEMONSTRATION_GRID")
    candidates = enumerate_candidates([d.input_grid for d in demonstrations], limit=max_trials)
    trials: list[CandidateTrial] = []
    for index, candidate in enumerate(candidates, start=1):
        fits, reason = _evaluate(candidate, demonstrations)
        if fits:
            status = "EXACT_DEMO_FIT"
        elif reason and ":" in reason and reason.split(":", 1)[1] in {s.value for s in ApplyStatus}:
            status = reason.split(":", 1)[1]
        elif reason and "OUTPUT_MISMATCH" in reason:
            status = "OUTPUT_MISMATCH"
        elif reason and reason.startswith("INVALID_INPUT"):
            status = "INVALID_DEMONSTRATION"
        else:
            status = "REJECTED"
        trials.append(CandidateTrial(index, candidate.candidate_id, candidate.canonical_json, status, reason))
        if fits:
            return SearchResult(SearchStatus.FOUND_EXACT_DEMO_FIT, candidate, tuple(trials), "FIRST_EXACT_DEMO_FIT")
    return SearchResult(SearchStatus.NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET, None, tuple(trials), "TRIAL_CAP_OR_LANGUAGE_EXHAUSTED")
