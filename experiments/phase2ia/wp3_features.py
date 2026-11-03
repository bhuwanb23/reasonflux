"""Task-level structural features for the WP3 provisional annotators.

Each feature is an observational predicate over one training pair. A task
feature fires when it holds for at least the configured fraction of pairs.
Only training demonstrations are read.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from experiments.phase2ia.wp3_geometry import (
    Grid,
    bbox_of_cells,
    changed_cells,
    component_boxes,
    component_crops,
    components,
    crop,
    enclosed_background,
    full_separators,
    inside,
    is_content_crop,
    is_reflection,
    is_rotation,
    is_subgrid,
    is_symmetric,
    mask_of,
    palette,
    reflect_horizontal,
    reflect_vertical,
    rotate,
    scale_factor,
    separator_regions,
    shape,
    tile_factor,
)
from experiments.phase2ia.wp3_patterns import (
    arithmetic_progression,
    background_regions,
    bbox_interior_filled,
    color_added_uniform,
    color_histogram,
    gravity_compaction,
    is_color_swap,
    is_periodic,
    largest_component_crop,
    lines,
    majority_nonbackground_color,
    region_color_fill,
    solid,
)

FEATURE_NAMES: tuple[str, ...] = (
    "frame_content_crop",
    "frame_subgrid_exact",
    "frame_band_crop",
    "frame_grow_pad",
    "count_scale",
    "count_tile",
    "count_axis_repeat",
    "count_dim_match",
    "count_cell_match",
    "count_uniform_output",
    "obj_component_crop",
    "obj_largest_component_crop",
    "obj_single_component_change",
    "obj_subset_to_one",
    "color_mask_recode",
    "color_one_object_recolor",
    "color_palette_reduction",
    "color_global_swap",
    "color_region_paint",
    "spatial_rotation",
    "spatial_reflection",
    "spatial_translation",
    "pattern_symmetry_completion",
    "pattern_self_mirror",
    "pattern_separator_tiling",
    "region_enclosed_fill",
    "region_separator_regions",
    "region_connectivity_change",
    "region_majority_fill",
    "region_bbox_fill",
    "spatial_gravity",
    "pattern_periodic_output",
    "obj_largest_component_crop",
    "color_global_swap",
    "count_dim_eq_colors",
    "count_dim_eq_objects",
    "symbolic_single_pixel",
    "symbolic_progression",
)


def _same_shape_predicates(i: Grid, o: Grid) -> dict[str, bool]:
    mask_i, mask_o = mask_of(i), mask_of(o)
    changed = changed_cells(i, o)
    boxes = component_boxes(i)
    parts = components(i)
    preds: dict[str, bool] = {}

    preds["color_mask_recode"] = mask_i == mask_o and i != o
    preds["obj_single_component_change"] = bool(changed) and sum(1 for b in boxes if inside(changed, b)) == 1
    preds["color_one_object_recolor"] = (
        preds["obj_single_component_change"]
        and mask_i == mask_o
        and all(i[r][c] != 0 and o[r][c] != 0 for r, c in changed)
    )
    preds["obj_subset_to_one"] = (
        len(parts) > 1
        and sum(1 for row in o for v in row if v != 0) < sum(1 for row in i for v in row if v != 0)
        and preds["color_mask_recode"]
    )
    preds["color_palette_reduction"] = len(palette(o)) < len(palette(i)) and mask_i == mask_o
    preds["pattern_symmetry_completion"] = (
        is_symmetric(o)
        and not is_symmetric(i)
        and all(mask_i[r][c] or not mask_o[r][c] for r in range(len(i)) for c in range(len(i[0])))
    )
    enclosed = enclosed_background(i)
    preds["region_enclosed_fill"] = (
        bool(enclosed)
        and all(o[r][c] != 0 for r, c in enclosed)
        and all(o[r][c] == i[r][c] for r in range(len(i)) for c in range(len(i[0])) if (r, c) not in enclosed)
    )
    preds["count_uniform_output"] = solid(o) and not solid(i)
    # Topology: the number of background regions changes because barriers close or open.
    preds["region_connectivity_change"] = background_regions(o) != background_regions(i)
    preds["region_majority_fill"] = (
        not preds["color_mask_recode"]
        and majority_nonbackground_color(o) == majority_nonbackground_color(i)
        and color_histogram(o) != color_histogram(i)
    )
    preds["symbolic_progression"] = any(arithmetic_progression([v for v in line if v != 0]) for line in lines(o))
    preds["region_bbox_fill"] = bbox_interior_filled(i, o)
    preds["spatial_gravity"] = gravity_compaction(i, o)
    preds["pattern_periodic_output"] = is_periodic(o) and not is_periodic(i)
    preds["color_global_swap"] = is_color_swap(i, o)
    preds["color_region_paint"] = color_added_uniform(i, o) or (region_color_fill(i, o) and not bbox_interior_filled(i, o))
    colours = len(palette(i) - {0})
    preds["count_dim_eq_colors"] = colours > 1 and shape(o) == (colours, colours)
    preds["symbolic_single_pixel"] = shape(o) == (1, 1) and o[0][0] in palette(i)
    return preds


def _diff_shape_predicates(i: Grid, o: Grid) -> dict[str, bool]:
    (ih, iw), (oh, ow) = shape(i), shape(o)
    parts = components(i)
    preds: dict[str, bool] = {}

    preds["frame_content_crop"] = is_content_crop(i, o)
    preds["frame_subgrid_exact"] = is_subgrid(i, o)
    preds["frame_band_crop"] = (
        (oh <= ih and ow == iw and any(crop(i, (t, 0, t + oh, iw)) == o for t in range(ih - oh + 1)))
        or (ow <= iw and oh == ih and any(crop(i, (0, left, ih, left + ow)) == o for left in range(iw - ow + 1)))
    )
    preds["frame_grow_pad"] = False

    preds["count_scale"] = scale_factor(i, o) is not None
    preds["count_tile"] = tile_factor(i, o) is not None
    preds["count_axis_repeat"] = (
        (ow == iw and oh % ih == 0 and oh > ih and all(o[r][c] == i[r % ih][c] for r in range(oh) for c in range(iw)))
        or (oh == ih and ow % iw == 0 and ow > iw and all(o[r][c] == i[r][c % iw] for r in range(ih) for c in range(ow)))
    )
    preds["count_dim_match"] = len(parts) in (oh, ow) and len(parts) > 1
    preds["count_cell_match"] = len(parts) == sum(1 for row in o for v in row if v != 0)
    preds["count_uniform_output"] = solid(o)

    crops = component_crops(i)
    preds["obj_component_crop"] = any(part == o for part in crops)
    preds["obj_subset_to_one"] = preds["obj_component_crop"]
    largest = largest_component_crop(i)
    preds["obj_largest_component_crop"] = largest is not None and largest == o
    preds["count_dim_eq_objects"] = len(parts) > 1 and (oh, ow) == (len(parts), len(parts))

    preds["spatial_rotation"] = is_rotation(i, o)
    preds["spatial_reflection"] = is_reflection(i, o)

    preds["pattern_self_mirror"] = (
        oh == ih and ow == 2 * iw and crop(o, (0, 0, ih, iw)) == i
        and crop(o, (0, iw, ih, 2 * iw)) in (reflect_vertical(i), reflect_horizontal(i))
    ) or (
        oh == 2 * ih and ow == iw and crop(o, (0, 0, ih, iw)) == i
        and crop(o, (ih, 0, 2 * ih, iw)) in (reflect_horizontal(i), reflect_vertical(i))
    )
    regions = separator_regions(i)
    preds["pattern_separator_tiling"] = len(regions) > 1 and all(r == o for r in regions)
    rows, cols = full_separators(i)
    preds["region_separator_regions"] = bool(rows or cols)

    preds["symbolic_progression"] = any(arithmetic_progression([v for v in line if v != 0]) for line in lines(o))
    preds["pattern_periodic_output"] = is_periodic(o) and not is_periodic(i)
    preds["color_global_swap"] = is_color_swap(i, o)
    colours = len(palette(i) - {0})
    preds["count_dim_eq_colors"] = colours > 1 and (oh, ow) == (colours, colours)
    preds["symbolic_single_pixel"] = (oh, ow) == (1, 1) and o[0][0] in palette(i)
    return preds


def _pair_predicates(i: Grid, o: Grid) -> dict[str, bool]:
    if shape(i) == shape(o):
        return _same_shape_predicates(i, o)
    return _diff_shape_predicates(i, o)


@dataclass(frozen=True, slots=True)
class TaskFeatures:
    task_id: str
    pair_count: int
    rates: dict[str, float]
    evidence: dict[str, tuple[int, ...]]
    notes: tuple[str, ...] = field(default=())

    def rate(self, name: str) -> float:
        return self.rates.get(name, 0.0)

    def fires(self, name: str, threshold: float) -> bool:
        return self.rate(name) >= threshold

    @property
    def unresolved(self) -> bool:
        return not any(self.rates.values())


def extract_features(task_id: str, pairs: Sequence[tuple[Grid, Grid]]) -> TaskFeatures:
    hits: dict[str, list[int]] = {name: [] for name in FEATURE_NAMES}
    for index, (input_grid, output_grid) in enumerate(pairs, start=1):
        for name, value in _pair_predicates(input_grid, output_grid).items():
            if value:
                hits[name].append(index)
    total = max(1, len(pairs))
    rates = {name: len(indices) / total for name, indices in hits.items()}
    notes: list[str] = []
    if any(_pair_predicates(a, b).get("obj_component_crop", False) for a, b in pairs) and rates["frame_content_crop"]:
        notes.append("output is both a component crop and a content crop")
    if rates["color_mask_recode"] and rates["obj_single_component_change"]:
        notes.append("recolour is confined to a single entity")
    if rates["pattern_symmetry_completion"] and rates["region_enclosed_fill"]:
        notes.append("symmetry completion inside enclosed regions")
    return TaskFeatures(
        task_id=task_id,
        pair_count=len(pairs),
        rates=rates,
        evidence={name: tuple(indices) for name, indices in hits.items()},
        notes=tuple(notes),
    )


def coverage(features: TaskFeatures, threshold: float = 0.8) -> tuple[str, ...]:
    return tuple(name for name in FEATURE_NAMES if features.fires(name, threshold))


__all__ = [
    "FEATURE_NAMES",
    "TaskFeatures",
    "coverage",
    "extract_features",
    "bbox_of_cells",
    "changed_cells",
    "components",
    "rotate",
    "tile_factor",
]
