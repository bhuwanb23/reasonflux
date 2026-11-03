"""Task-level pattern predicates for the WP3 provisional annotators.

These build on the primitives in ``wp3_geometry`` and describe recognisable
task-level regularities over training pairs only.
"""
from __future__ import annotations

from experiments.phase2ia.wp3_geometry import (
    Grid,
    bbox,
    cells_of,
    changed_cells,
    component_crops,
    components,
    palette,
    shape,
)


def replace_color(grid: Grid, source: int, target: int) -> Grid:
    return tuple(tuple(target if v == source else v for v in row) for row in grid)


def color_histogram(grid: Grid, *, background: int = 0) -> dict[int, int]:
    counts: dict[int, int] = {}
    for row in grid:
        for value in row:
            if value != background:
                counts[value] = counts.get(value, 0) + 1
    return counts


def majority_nonbackground_color(grid: Grid) -> int | None:
    counts = color_histogram(grid)
    if not counts:
        return None
    return max(counts.items(), key=lambda item: (item[1], -item[0]))[0]


def solid(grid: Grid) -> bool:
    return len(palette(grid)) == 1


def background_regions(grid: Grid) -> int:
    """Count 4-connected background regions, including the outer frame."""
    return len(components(grid, background=0))


def is_color_swap(input_grid: Grid, output_grid: Grid) -> bool:
    """True when the output equals the input with one colour globally renamed."""
    if shape(input_grid) != shape(output_grid):
        return False
    for source in sorted(palette(input_grid) - {0}):
        for target in range(10):
            if target != source and replace_color(input_grid, source, target) == output_grid:
                return True
    return False


def is_periodic(grid: Grid) -> bool:
    """True when the grid repeats with a smaller row or column period."""
    h, w = shape(grid)
    for period in range(1, w):
        if w % period or period >= w:
            continue
        if all(grid[r][c] == grid[r][c % period] for r in range(h) for c in range(w)):
            return True
    for period in range(1, h):
        if h % period or period >= h:
            continue
        if all(grid[r][c] == grid[r % period][c] for r in range(h) for c in range(w)):
            return True
    return False


def largest_component_crop(grid: Grid) -> Grid | None:
    crops = component_crops(grid)
    if not crops:
        return None
    return max(crops, key=lambda g: sum(1 for row in g for v in row if v))


def bbox_interior_filled(input_grid: Grid, output_grid: Grid) -> bool:
    """All background inside the content bounding box is filled and nothing outside changes."""
    if shape(input_grid) != shape(output_grid):
        return False
    box = bbox(input_grid)
    if box is None:
        return False
    top, left, bottom, right = box
    if bottom - top < 3 or right - left < 3:
        return False
    h, w = shape(input_grid)
    for r in range(h):
        for c in range(w):
            if top <= r < bottom and left <= c < right:
                continue
            if input_grid[r][c] != output_grid[r][c]:
                return False
    return all(output_grid[r][c] != 0 for r in range(top, bottom) for c in range(left, right) if input_grid[r][c] == 0)


def _single_new_colour_on_background(input_grid: Grid, output_grid: Grid) -> bool:
    if shape(input_grid) != shape(output_grid):
        return False
    changed = changed_cells(input_grid, output_grid)
    if not changed:
        return False
    if any(input_grid[r][c] != 0 for r, c in changed):
        return False
    return len({output_grid[r][c] for r, c in changed}) == 1


def region_color_fill(input_grid: Grid, output_grid: Grid) -> bool:
    """Background cells in one region become a single new colour; drawn cells are untouched."""
    return _single_new_colour_on_background(input_grid, output_grid)


def color_added_uniform(input_grid: Grid, output_grid: Grid) -> bool:
    """One new colour is painted onto background cells; existing colours are preserved."""
    return _single_new_colour_on_background(input_grid, output_grid)


def gravity_compaction(input_grid: Grid, output_grid: Grid) -> bool:
    """Content keeps its order but is packed toward one edge, with the same colour multiset."""
    if shape(input_grid) != shape(output_grid) or input_grid == output_grid:
        return False
    if sorted(v for _, _, v in cells_of(input_grid)) != sorted(v for _, _, v in cells_of(output_grid)):
        return False
    h, w = shape(input_grid)
    for c in range(w):
        source = [input_grid[r][c] for r in range(h) if input_grid[r][c] != 0]
        target = [output_grid[r][c] for r in range(h) if output_grid[r][c] != 0]
        if source != target:
            break
    else:
        return True
    for r in range(h):
        source = [v for v in input_grid[r] if v != 0]
        target = [v for v in output_grid[r] if v != 0]
        if source != target:
            break
    else:
        return True
    return False


def arithmetic_progression(values: list[int]) -> bool:
    if len(values) < 3:
        return False
    step = values[1] - values[0]
    return step != 0 and all(b - a == step for a, b in zip(values, values[1:]))


def lines(grid: Grid) -> list[list[int]]:
    rows = [list(row) for row in grid]
    cols = [[grid[r][c] for r in range(len(grid))] for c in range(len(grid[0]))]
    return rows + cols
