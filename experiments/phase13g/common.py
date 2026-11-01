"""ARC-AGI-2 task loading and bounded symbolic program inventory for Phase 13G."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from core.trace import ReasoningStep, ReasoningTrace, TraceOutcome
from solver.grid import Grid, count_objects

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets/arc/arc-agi-2"
OUT = ROOT / "reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1"
PROGRAMS = (
    "identity", "reflect_horizontal", "reflect_vertical", "rotate_90",
    "rotate_180", "rotate_270", "transpose", "anti_transpose",
    "translate_constant", "recolor_bijection",
)
PROGRAM_FAMILY = {
    "identity": "identity_or_other",
    "reflect_horizontal": "reflection",
    "reflect_vertical": "reflection",
    "rotate_90": "rotation",
    "rotate_180": "rotation",
    "rotate_270": "rotation",
    "transpose": "rotation_or_reflection",
    "anti_transpose": "rotation_or_reflection",
    "translate_constant": "translation",
    "recolor_bijection": "recoloring",
}


def load_task_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks = []
    for row in rows:
        p = ROOT / "datasets/arc" / row["path"]
        task = json.loads(p.read_text())
        task["task_id"] = row["task_id"]
        task["split"] = row["split"]
        tasks.append(task)
    return tasks


def load_named_split(name: str) -> list[dict[str, Any]]:
    manifest = json.loads((DATA / "split_manifest.json").read_text())
    rows = [r for r in manifest["tasks"] if r["split"] == name]
    return load_task_rows(rows)


def load_split() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = json.loads((DATA / "split_manifest.json").read_text())
    groups = {name: [r for r in manifest["tasks"] if r["split"] == name]
              for name in ("discovery", "transfer", "holdout")}
    return tuple(load_task_rows(groups[k]) for k in ("discovery", "transfer", "holdout"))  # type: ignore[return-value]


def _tuple_grid(rows: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(int(c) for c in row) for row in rows)


def _mode_color(grid: tuple[tuple[int, ...], ...]) -> int:
    counts = Counter(c for row in grid for c in row)
    return min(counts, key=lambda c: (-counts[c], c))


def _rot90(g: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    h, w = len(g), len(g[0])
    return tuple(tuple(g[h - 1 - r][c] for r in range(h)) for c in range(w))


def _transform_static(name: str, g: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    if name == "identity":
        return g
    if name == "reflect_horizontal":
        return tuple(tuple(reversed(row)) for row in g)
    if name == "reflect_vertical":
        return tuple(reversed(g))
    if name == "rotate_90":
        return _rot90(g)
    if name == "rotate_180":
        return _rot90(_rot90(g))
    if name == "rotate_270":
        return _rot90(_rot90(_rot90(g)))
    if name == "transpose":
        return tuple(tuple(g[r][c] for r in range(len(g))) for c in range(len(g[0])))
    if name == "anti_transpose":
        h, w = len(g), len(g[0])
        return tuple(tuple(g[h - 1 - r][w - 1 - c] for r in range(h)) for c in range(w))
    raise KeyError(name)


def _shift(g: tuple[tuple[int, ...], ...], dy: int, dx: int, bg: int) -> tuple[tuple[int, ...], ...]:
    h, w = len(g), len(g[0])
    out = [[bg] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            rr, cc = r + dy, c + dx
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = g[r][c]
    return tuple(tuple(row) for row in out)


def _infer_shift(source: tuple[tuple[int, ...], ...], target: tuple[tuple[int, ...], ...]) -> tuple[int, int, int] | None:
    if len(source) != len(target) or len(source[0]) != len(target[0]):
        return None
    bg = _mode_color(source)
    src = [(r, c, source[r][c]) for r in range(len(source)) for c in range(len(source[0])) if source[r][c] != bg]
    tgt = [(r, c, target[r][c]) for r in range(len(target)) for c in range(len(target[0])) if target[r][c] != bg]
    if not src or not tgt:
        return None
    sr, sc = [x[0] for x in src], [x[1] for x in src]
    tr, tc = [x[0] for x in tgt], [x[1] for x in tgt]
    # Most ARC translations do not clip the moved object; test the bounding-box
    # displacement first, then use a rare-color anchor if clipping occurred.
    dy0, dx0 = min(tr) - min(sr), min(tc) - min(sc)
    if _shift(source, dy0, dx0, bg) == target:
        return dy0, dx0, bg
    src_by_color: dict[int, list[tuple[int, int]]] = {}
    tgt_by_color: dict[int, list[tuple[int, int]]] = {}
    for r, c, color in src: src_by_color.setdefault(color, []).append((r, c))
    for r, c, color in tgt: tgt_by_color.setdefault(color, []).append((r, c))
    common = [color for color in src_by_color if color in tgt_by_color]
    if not common:
        return None
    anchor = min(common, key=lambda color: len(src_by_color[color]) * len(tgt_by_color[color]))
    source_anchors = src_by_color[anchor]
    if len(source_anchors) > 16:
        source_anchors = [source_anchors[round(i*(len(source_anchors)-1)/15)] for i in range(16)]
    offsets = {(rt-rs, ct-cs) for rs, cs in source_anchors for rt, ct in tgt_by_color[anchor]}
    for dy, dx in sorted(offsets, key=lambda q: (abs(q[0])+abs(q[1]), q[0], q[1])):
        if _shift(source, dy, dx, bg) == target:
            return dy, dx, bg
    return None


def _infer_recolor(source: tuple[tuple[int, ...], ...], target: tuple[tuple[int, ...], ...]) -> dict[int, int] | None:
    if len(source) != len(target) or len(source[0]) != len(target[0]):
        return None
    mapping: dict[int, int] = {}
    reverse: dict[int, int] = {}
    for row_a, row_b in zip(source, target):
        for a, b in zip(row_a, row_b):
            if a in mapping and mapping[a] != b:
                return None
            if b in reverse and reverse[b] != a:
                return None
            mapping[a] = b
            reverse[b] = a
    return mapping


def infer_context(program: str, demos: list[dict[str, Any]]) -> dict[str, Any] | None:
    # Canonical sorting is safe: context inference is defined over the unordered
    # demonstration set, so pair-order perturbations cannot change its semantics.
    key = json.dumps(sorted(demos, key=lambda p: json.dumps(p, sort_keys=True)), sort_keys=True, separators=(",", ":"))
    return _infer_context_cached(program, key)


@lru_cache(maxsize=50000)
def _infer_context_cached(program: str, demos_json: str) -> dict[str, Any] | None:
    demos = json.loads(demos_json)
    if not demos:
        return None
    if program == "translate_constant":
        contexts = [_infer_shift(_tuple_grid(p["input"]), _tuple_grid(p["output"])) for p in demos]
        if any(x is None for x in contexts) or len(set(contexts)) != 1:
            return None
        dy, dx, bg = contexts[0]
        context: dict[str, Any] = {"dy": dy, "dx": dx, "bg": bg}
    elif program == "recolor_bijection":
        mappings = [_infer_recolor(_tuple_grid(p["input"]), _tuple_grid(p["output"])) for p in demos]
        if any(x is None for x in mappings) or any(x != mappings[0] for x in mappings[1:]):
            return None
        context = {"mapping": mappings[0]}
    else:
        context = {}
    for pair in demos:
        a, b = _tuple_grid(pair["input"]), _tuple_grid(pair["output"])
        try:
            pred = apply_program(program, a, context)
        except (KeyError, IndexError, ValueError):
            return None
        if pred != b:
            return None
    return context


def apply_program(program: str, g: tuple[tuple[int, ...], ...], context: dict[str, Any] | None = None) -> tuple[tuple[int, ...], ...] | None:
    ctx = context or {}
    if program in PROGRAMS[:8]:
        return _transform_static(program, g)
    if program == "translate_constant":
        if not {"dy", "dx", "bg"}.issubset(ctx):
            return None
        return _shift(g, int(ctx["dy"]), int(ctx["dx"]), int(ctx["bg"]))
    if program == "recolor_bijection":
        mapping = ctx.get("mapping")
        if not mapping or any(c not in mapping for row in g for c in row):
            return None
        return tuple(tuple(int(mapping[c]) for c in row) for row in g)
    raise KeyError(program)


def _all_test_exact(task: dict[str, Any], program: str, ctx: dict[str, Any]) -> tuple[bool, int]:
    n = len(task["test"])
    for pair in task["test"]:
        pred = apply_program(program, _tuple_grid(pair["input"]), ctx)
        if pred is None or pred != _tuple_grid(pair["output"]):
            return False, n
    return True, n


def solve_task(task: dict[str, Any], order: list[str] | tuple[str, ...], budget: int = 3) -> dict[str, Any]:
    tried = 0
    for program in list(dict.fromkeys(order))[:budget]:
        tried += 1
        ctx = infer_context(program, task["train"])
        if ctx is None:
            continue
        success, test_pairs = _all_test_exact(task, program, ctx)
        return {"program": program, "family": PROGRAM_FAMILY[program], "demo_fit": True,
                "task_exact": success, "candidate_trials": tried, "test_pairs": test_pairs,
                "failure_type": "" if success else "demo_fit_test_mismatch", "context": ctx}
    total = len(task["test"])
    return {"program": "", "family": "unsupported_v1", "demo_fit": False,
            "task_exact": False, "candidate_trials": tried, "test_pairs": total,
            "failure_type": "no_dsl_fit_within_budget", "context": {}}


def trace_for(task: dict[str, Any], result: dict[str, Any]) -> ReasoningTrace:
    tid = task["task_id"]
    program = str(result["program"])
    if program:
        ops = ["validate_grid_schema", "enumerate_candidate_programs", f"apply_{program}", "verify_demonstrations"]
        payload = ["rectangular_color_grid", "fixed_dsl_order", program, "all_demos_exact"]
        ok = bool(result["demo_fit"])
    else:
        ops = ["validate_grid_schema", "enumerate_candidate_programs", "candidate_budget_exhausted"]
        payload = ["rectangular_color_grid", "fixed_dsl_order", "no_exact_fit"]
        ok = False
    steps = [ReasoningStep(step_id=f"{tid}-s{i+1}", operation=op, outputs=[payload[i]], cost=1.0)
             for i, op in enumerate(ops)]
    family = str(result["family"])
    return ReasoningTrace(
        trace_id=f"arc2-{tid}", task_id=tid, timestamp=0.0, steps=steps,
        outcome=TraceOutcome(success=ok, result={"program": program, "demo_fit": ok}, cost=float(result["candidate_trials"])),
        metadata={"task_family": family, "dataset": "ARC-AGI-2", "split": task["split"],
                  "trace_source": "bounded_program_search", "test_outputs_used_for_trace": False},
    )


_FEATURE_CACHE: dict[str, tuple[float, ...]] = {}
_BUCKET_CACHE: dict[str, str] = {}


def task_features(task: dict[str, Any]) -> tuple[float, ...]:
    tid = str(task.get("task_id", ""))
    if tid and tid in _FEATURE_CACHE:
        return _FEATURE_CACHE[tid]
    dims, colors, objects, densities, changes = [], [], [], [], []
    for pair in task["train"]:
        g = _tuple_grid(pair["input"])
        out = _tuple_grid(pair["output"])
        dims.append((len(g) + len(g[0])) / 60.0)
        colors.append(len(set(c for row in g for c in row)) / 10.0)
        objects.append(min(20, count_objects(Grid(g))) / 20.0)
        densities.append(sum(c != 0 for row in g for c in row) / (len(g) * len(g[0])))
        if (len(g), len(g[0])) != (len(out), len(out[0])):
            changes.append(1.0)
        else:
            changes.append(sum(a != b for ra, rb in zip(g, out) for a, b in zip(ra, rb)) / max(1, len(g) * len(g[0])))
    n = max(1, len(dims))
    result = tuple(sum(x) / n for x in (dims, colors, objects, densities, changes))
    if tid:
        _FEATURE_CACHE[tid] = result
    return result


def structural_bucket(task: dict[str, Any]) -> str:
    tid = str(task.get("task_id", ""))
    if tid and tid in _BUCKET_CACHE:
        return _BUCKET_CACHE[tid]
    pair = task["train"][0]
    a, b = _tuple_grid(pair["input"]), _tuple_grid(pair["output"])
    shape = "same_shape" if (len(a), len(a[0])) == (len(b), len(b[0])) else "shape_changed"
    palette = "same_palette" if set(c for r in a for c in r) == set(c for r in b for c in r) else "palette_changed"
    obj_a, obj_b = count_objects(Grid(a)), count_objects(Grid(b))
    obj = "same_object_count" if obj_a == obj_b else "object_count_changed"
    result = f"{shape}|{palette}|{obj}"
    if tid:
        _BUCKET_CACHE[tid] = result
    return result


def symmetry_demo_property(task: dict[str, Any]) -> bool:
    """Whether any demonstration input/output is mirror-symmetric on either axis."""
    for pair in task["train"]:
        for rows in (pair["input"], pair["output"]):
            g = _tuple_grid(rows)
            if all(row == tuple(reversed(row)) for row in g):
                return True
            if g == tuple(reversed(g)):
                return True
    return False


def family_taxonomy(program: str) -> str:
    family = PROGRAM_FAMILY.get(program, "unsupported_v1")
    return family


def stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def mean(values: list[float]) -> float | None:
    return statistics.mean(values) if values else None


def normalized_distance(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return math.sqrt(sum((x-y) ** 2 for x, y in zip(a, b)))
