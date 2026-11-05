"""Deterministic surface transformations; no test/holdout suite is materialized."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .world import ObjectKind, UnlockObject, UnlockState

Coord = tuple[int, int]


@dataclass(frozen=True, slots=True)
class SurfaceTransform:
    transform_id: str
    object_id_map: tuple[tuple[str, str], ...] = ()
    color_map: tuple[tuple[str, str], ...] = ()
    shape_map: tuple[tuple[str, str], ...] = ()
    coordinate_overrides: tuple[tuple[str, Coord], ...] = ()
    translation: Coord = (0, 0)
    rotate_quarters: int = 0
    reflect_x: bool = False
    reverse_object_order: bool = False
    distractors: tuple[UnlockObject, ...] = ()

    def __post_init__(self) -> None:
        if not self.transform_id:
            raise ValueError("transform_id must be non-empty")
        for name, pairs in (
            ("object_id_map", self.object_id_map),
            ("color_map", self.color_map),
            ("shape_map", self.shape_map),
        ):
            sources = [source for source, _ in pairs]
            targets = [target for _, target in pairs]
            if len(sources) != len(set(sources)):
                raise ValueError(f"{name} contains duplicate source values")
            if len(targets) != len(set(targets)):
                raise ValueError(f"{name} must be one-to-one")
        coordinate_ids = [object_id for object_id, _ in self.coordinate_overrides]
        coordinates = [coord for _, coord in self.coordinate_overrides]
        if len(coordinate_ids) != len(set(coordinate_ids)):
            raise ValueError("coordinate_overrides contain duplicate object IDs")
        if len(coordinates) != len(set(coordinates)):
            raise ValueError("coordinate_overrides must be a permutation")


def _map_xy(x: int, y: int, transform: SurfaceTransform) -> Coord:
    if transform.reflect_x:
        x = -x
    turns = transform.rotate_quarters % 4
    for _ in range(turns):
        x, y = -y, x
    return x + transform.translation[0], y + transform.translation[1]


def transform_state(state: UnlockState, transform: SurfaceTransform) -> UnlockState:
    """Apply identity/appearance/layout transforms and remap relation references."""
    id_map: Mapping[str, str] = dict(transform.object_id_map)
    color_map: Mapping[str, str] = dict(transform.color_map)
    shape_map: Mapping[str, str] = dict(transform.shape_map)
    coordinate_map: Mapping[str, Coord] = dict(transform.coordinate_overrides)
    transformed: list[UnlockObject] = []
    for obj in state.objects:
        new_id = id_map.get(obj.object_id, obj.object_id)
        new_relation = (
            id_map.get(obj.opens_target_id, obj.opens_target_id)
            if obj.opens_target_id is not None
            else None
        )
        x, y = _map_xy(obj.x, obj.y, transform)
        if obj.object_id in coordinate_map:
            x, y = coordinate_map[obj.object_id]
        transformed.append(
            UnlockObject(
                object_id=new_id,
                kind=obj.kind,
                x=x,
                y=y,
                color=color_map.get(obj.color, obj.color),
                shape=shape_map.get(obj.shape, obj.shape),
                opens_target_id=new_relation,
                closed=obj.closed,
            )
        )
    ax, ay = _map_xy(state.agent_x, state.agent_y, transform)
    if transform.reverse_object_order:
        transformed.reverse()
    for distractor in transform.distractors:
        if distractor.kind is not ObjectKind.DISTRACTOR:
            raise ValueError("added surface objects must have DISTRACTOR role")
        transformed.append(distractor)
    source_ids = {obj.object_id for obj in state.objects}
    if not set(coordinate_map).issubset(source_ids):
        raise ValueError("coordinate_overrides reference unknown source object IDs")
    ids = [obj.object_id for obj in transformed]
    if len(ids) != len(set(ids)):
        raise ValueError("surface transform produced duplicate object IDs")
    result = UnlockState(
        context_id=f"{state.context_id}:{transform.transform_id}",
        objects=tuple(transformed),
        agent_x=ax,
        agent_y=ay,
        path_clear=state.path_clear,
    )
    if result.has_dangling_relations():
        raise ValueError("surface transform produced a dangling relation reference")
    return result
