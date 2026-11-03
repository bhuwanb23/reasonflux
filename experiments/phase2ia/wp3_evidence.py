"""Feature-to-family evidence specification for the WP3 provisional agents.

Each observable feature contributes weighted evidence to one ontology family.
Specific mechanisms carry full weight; broad by-product signals (for example a
background-region count changing whenever cells are filled) carry low weight so
that they cannot outvote a decisive mechanism.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Spec:
    feature: str
    family: str
    weight: float
    mechanism: str


FEATURE_SPECS: tuple[Spec, ...] = (
    # Frame / extent
    Spec("frame_content_crop", "FRAME_BOUNDS", 1.0, "output is the content crop of the input"),
    Spec("frame_subgrid_exact", "FRAME_BOUNDS", 0.95, "output is an exact sub-region of the input"),
    Spec("frame_band_crop", "FRAME_BOUNDS", 0.9, "output keeps one full-width or full-height band"),
    # Counting / repetition
    Spec("count_scale", "COUNT_REPLICATION", 1.0, "output is a fixed multiple expansion of the input"),
    Spec("count_tile", "COUNT_REPLICATION", 1.0, "output is a tiling of the input"),
    Spec("count_axis_repeat", "COUNT_REPLICATION", 0.95, "output repeats the input along one axis"),
    Spec("count_dim_match", "COUNT_REPLICATION", 0.85, "an output dimension equals the number of input entities"),
    Spec("count_cell_match", "COUNT_REPLICATION", 0.85, "the output cell count equals the number of input entities"),
    Spec("count_dim_eq_colors", "COUNT_REPLICATION", 0.8, "output dimensions equal the number of input colours"),
    Spec("count_dim_eq_objects", "COUNT_REPLICATION", 0.8, "output dimensions equal the number of input entities"),
    Spec("count_uniform_output", "COUNT_REPLICATION", 0.45, "output collapses to a single colour"),
    # Object selection
    Spec("obj_component_crop", "OBJ_RELATION", 1.0, "output reproduces exactly one embedded entity"),
    Spec("obj_largest_component_crop", "OBJ_RELATION", 1.0, "output reproduces the largest embedded entity"),
    Spec("obj_subset_to_one", "OBJ_RELATION", 0.85, "several entities reduce to one selected entity"),
    Spec("obj_single_component_change", "OBJ_RELATION", 0.5, "all changes fall inside a single entity"),
    # Colour / attribute
    Spec("color_mask_recode", "COLOR_ATTRIBUTE", 0.95, "occupied positions are preserved and only colours change"),
    Spec("color_one_object_recolor", "COLOR_ATTRIBUTE", 0.95, "one entity is recoloured in place"),
    Spec("color_global_swap", "COLOR_ATTRIBUTE", 1.0, "the output is the input with one colour globally renamed"),
    Spec("color_region_paint", "COLOR_ATTRIBUTE", 0.7, "one new colour is painted onto background cells"),
    Spec("color_palette_reduction", "COLOR_ATTRIBUTE", 0.6, "the occupied positions are preserved with fewer colours"),
    # Spatial arrangement
    Spec("spatial_rotation", "SPATIAL_CHANGE", 1.0, "output is a rotation of the input"),
    Spec("spatial_reflection", "SPATIAL_CHANGE", 1.0, "output is a reflection of the input"),
    Spec("spatial_translation", "SPATIAL_CHANGE", 0.95, "the content set is translated rigidly"),
    Spec("spatial_gravity", "SPATIAL_CHANGE", 0.85, "content is packed toward one edge without reordering"),
    # Pattern completion
    Spec("pattern_symmetry_completion", "PATTERN_COMPLETION", 1.0, "cells are added until the grid is symmetric"),
    Spec("pattern_self_mirror", "PATTERN_COMPLETION", 1.0, "output is the input plus its mirror image"),
    Spec("pattern_separator_tiling", "PATTERN_COMPLETION", 0.9, "every separator region is replaced by the same pattern"),
    Spec("pattern_periodic_output", "PATTERN_COMPLETION", 0.75, "output becomes periodic along an axis"),
    # Region / topology
    Spec("region_enclosed_fill", "REGION_TOPOLOGY", 1.0, "enclosed background is entirely filled"),
    Spec("region_bbox_fill", "REGION_TOPOLOGY", 0.9, "background inside the content bounding box is filled"),
    Spec("region_separator_regions", "REGION_TOPOLOGY", 0.55, "the grid is partitioned by full separators"),
    Spec("region_connectivity_change", "REGION_TOPOLOGY", 0.3, "the number of background regions changes"),
    Spec("region_majority_fill", "REGION_TOPOLOGY", 0.3, "the dominant colour is preserved while the histogram changes"),
    # Symbolic
    Spec("symbolic_progression", "SYMBOLIC_SEQUENCE", 0.9, "the output contains an arithmetic progression"),
    Spec("symbolic_single_pixel", "SYMBOLIC_SEQUENCE", 0.7, "the output is a single pixel drawn from the input palette"),
)

SPEC_BY_FEATURE: dict[str, Spec] = {spec.feature: spec for spec in FEATURE_SPECS}

# Families whose mechanisms are surface actions rather than target selection.
SURFACE_FAMILIES = frozenset({"SPATIAL_CHANGE", "COLOR_ATTRIBUTE", "FRAME_BOUNDS"})
# Families that outrank a surface action under the rubric's selection priority.
SELECTION_FAMILIES = frozenset({"OBJ_RELATION", "REGION_TOPOLOGY", "COUNT_REPLICATION", "PATTERN_COMPLETION"})

FAMILY_ORDER: tuple[str, ...] = (
    "OBJ_RELATION",
    "SPATIAL_CHANGE",
    "COLOR_ATTRIBUTE",
    "COUNT_REPLICATION",
    "PATTERN_COMPLETION",
    "REGION_TOPOLOGY",
    "FRAME_BOUNDS",
    "SYMBOLIC_SEQUENCE",
)
