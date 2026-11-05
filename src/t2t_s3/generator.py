"""Declarative surface-recipe constructors; no suite or contexts are assigned."""

from __future__ import annotations

from dataclasses import dataclass

from .transforms import Coord, SurfaceTransform, _map_xy, transform_state
from .world import UnlockObject, UnlockState


@dataclass(frozen=True, slots=True)
class TransformationRecipe:
    """A transform specification only, not a generated/evaluated test context."""

    recipe_id: str
    rename_ids: tuple[tuple[str, str], ...] = ()
    recolor: tuple[tuple[str, str], ...] = ()
    reshape: tuple[tuple[str, str], ...] = ()
    coordinate_overrides_output_frame: tuple[tuple[str, Coord], ...] = ()
    translation: Coord = (0, 0)
    rotate_quarters: int = 0
    reflect_x: bool = False
    reverse_object_order: bool = False
    distractors_output_frame: tuple[UnlockObject, ...] = ()

    def as_surface_transform(self) -> SurfaceTransform:
        return SurfaceTransform(
            transform_id=self.recipe_id,
            object_id_map=self.rename_ids,
            color_map=self.recolor,
            shape_map=self.reshape,
            coordinate_overrides=self.coordinate_overrides_output_frame,
            translation=self.translation,
            rotate_quarters=self.rotate_quarters,
            reflect_x=self.reflect_x,
            reverse_object_order=self.reverse_object_order,
            distractors=self.distractors_output_frame,
        )


def identity_shift_recipe(state: UnlockState, cell_id: str = "H-ID") -> TransformationRecipe:
    """Construct a bijective fresh-ID recipe from the IDs in a supplied state."""
    return TransformationRecipe(
        recipe_id=cell_id,
        rename_ids=tuple((obj.object_id, f"{cell_id}::{obj.object_id}") for obj in state.objects),
    )


def appearance_shift_recipe(state: UnlockState, cell_id: str = "H-APP") -> TransformationRecipe:
    """One-to-one relabel observed appearance vocabularies independently of role."""
    colors = sorted({obj.color for obj in state.objects})
    shapes = sorted({obj.shape for obj in state.objects})
    return TransformationRecipe(
        recipe_id=cell_id,
        recolor=tuple((value, f"{cell_id}::color::{index}") for index, value in enumerate(colors)),
        reshape=tuple((value, f"{cell_id}::shape::{index}") for index, value in enumerate(shapes)),
    )


def layout_shift_recipe(cell_id: str = "H-LAYOUT") -> TransformationRecipe:
    """Frozen 90-degree rotation, fixed translation, and reverse record order."""
    return TransformationRecipe(
        recipe_id=cell_id,
        translation=(11, -7),
        rotate_quarters=1,
        reverse_object_order=True,
    )


def role_layout_recipe(
    state: UnlockState,
    cell_id: str = "H-ROLE",
    *,
    coordinate_frame: TransformationRecipe | None = None,
) -> TransformationRecipe:
    """Permute target coordinate slots within equal closed/adjacency groups.

    Eligible inputs need at least two closed-state/adjacency-matched targets with
    distinct positions. This changes which target ID occupies each spatial slot
    while preserving the target-level closed and adjacency predicates.
    """
    if not state.is_complete() or state.has_dangling_relations():
        raise ValueError("role-layout recipe requires a complete, well-formed state")
    frame = coordinate_frame.as_surface_transform() if coordinate_frame else SurfaceTransform("identity")
    agent_x, agent_y = _map_xy(state.agent_x, state.agent_y, frame)
    groups: dict[tuple[bool | None, bool], list[tuple[UnlockObject, Coord]]] = {}
    for obj in state.targets():
        coord = _map_xy(obj.x, obj.y, frame)
        adjacent = abs(agent_x - coord[0]) + abs(agent_y - coord[1]) == 1
        groups.setdefault((obj.closed, adjacent), []).append((obj, coord))
    overrides: list[tuple[str, Coord]] = []
    for group in groups.values():
        ordered = sorted(group, key=lambda item: item[0].object_id)
        if len(ordered) < 2:
            continue
        coordinates = [coord for _, coord in ordered]
        if len(coordinates) != len(set(coordinates)):
            continue
        for index, (obj, _) in enumerate(ordered):
            overrides.append((obj.object_id, coordinates[(index + 1) % len(coordinates)]))
    if not overrides:
        raise ValueError("role-layout cell requires two targets with equal closed/adjacency facts and distinct coordinates")
    return TransformationRecipe(
        recipe_id=cell_id,
        coordinate_overrides_output_frame=tuple(overrides),
        reverse_object_order=True,
    )


def composed_surface_recipe(state: UnlockState, cell_id: str = "H-COMPOSED") -> TransformationRecipe:
    """Compose fresh IDs, appearance, rigid layout, and role-slot permutation."""
    identity = identity_shift_recipe(state, "H-ID")
    appearance = appearance_shift_recipe(state, "H-APP")
    layout = layout_shift_recipe("H-LAYOUT")
    role = role_layout_recipe(state, "H-ROLE", coordinate_frame=layout)
    return TransformationRecipe(
        recipe_id=cell_id,
        rename_ids=identity.rename_ids,
        recolor=appearance.recolor,
        reshape=appearance.reshape,
        coordinate_overrides_output_frame=role.coordinate_overrides_output_frame,
        translation=layout.translation,
        rotate_quarters=layout.rotate_quarters,
        reflect_x=layout.reflect_x,
        reverse_object_order=True,
    )


def apply_recipe(state: UnlockState, recipe: TransformationRecipe) -> UnlockState:
    """Apply one recipe to an explicitly supplied synthetic development/source state.

    This utility does not create a suite, assign roles/splits, inspect outcomes,
    or select favorable transformations. Added distractor coordinates are in the
    output frame after the geometric transform.
    """
    return transform_state(state, recipe.as_surface_transform())
