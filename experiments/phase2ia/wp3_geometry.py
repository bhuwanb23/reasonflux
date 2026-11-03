"""Grid geometry primitives shared by the WP3 provisional annotators.

Pure observational helpers over training grids only. No module here reads
test fields, solver programs, traces, candidate yield, or family labels.
"""
from __future__ import annotations

from typing import Iterable

Grid = tuple[tuple[int, ...], ...]
Cell = tuple[int, int]
Box = tuple[int, int, int, int]  # top, left, bottom-exclusive, right-exclusive


def shape(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0])


def cells_of(grid: Grid, *, background: int = 0) -> list[tuple[int, int, int]]:
    return [(r, c, v) for r, row in enumerate(grid) for c, v in enumerate(row) if v != background]


def mask_of(grid: Grid, *, background: int = 0) -> tuple[tuple[bool, ...], ...]:
    return tuple(tuple(v != background for v in row) for row in grid)


def palette(grid: Grid) -> set[int]:
    return {v for row in grid for v in row}


def bbox(grid: Grid, *, background: int = 0) -> Box | None:
    found = cells_of(grid, background=background)
    if not found:
        return None
    rows = [r for r, _, _ in found]
    cols = [c for _, c, _ in found]
    return min(rows), min(cols), max(rows) + 1, max(cols) + 1


def crop(grid: Grid, box: Box) -> Grid:
    top, left, bottom, right = box
    return tuple(tuple(row[left:right]) for row in grid[top:bottom])


def crop_to_content(grid: Grid) -> Grid | None:
    box = bbox(grid)
    return None if box is None else crop(grid, box)


def inside(cells: Iterable[Cell], box: Box) -> bool:
    top, left, bottom, right = box
    return all(top <= r < bottom and left <= c < right for r, c in cells)


def changed_cells(input_grid: Grid, output_grid: Grid) -> set[Cell]:
    if shape(input_grid) != shape(output_grid):
        return set()
    return {
        (r, c)
        for r, (row_a, row_b) in enumerate(zip(input_grid, output_grid))
        for c, (a, b) in enumerate(zip(row_a, row_b))
        if a != b
    }


def is_subgrid(input_grid: Grid, output_grid: Grid) -> bool:
    ih, iw = shape(input_grid)
    oh, ow = shape(output_grid)
    if oh > ih or ow > iw:
        return False
    for top in range(ih - oh + 1):
        for left in range(iw - ow + 1):
            if crop(input_grid, (top, left, top + oh, left + ow)) == output_grid:
                return True
    return False


def is_content_crop(input_grid: Grid, output_grid: Grid) -> bool:
    cropped = crop_to_content(input_grid)
    return cropped is not None and cropped == output_grid


def scale_factor(input_grid: Grid, output_grid: Grid) -> int | None:
    ih, iw = shape(input_grid)
    oh, ow = shape(output_grid)
    if ih == 0 or iw == 0 or oh % ih or ow % iw:
        return None
    factor = oh // ih
    if factor < 2 or ow // iw != factor:
        return None
    expanded = tuple(
        tuple(value for value in row for _ in range(factor)) for row in input_grid for _ in range(factor)
    )
    return factor if expanded == output_grid else None


def tile_factor(input_grid: Grid, output_grid: Grid) -> int | None:
    ih, iw = shape(input_grid)
    oh, ow = shape(output_grid)
    if ih == 0 or iw == 0 or oh % ih or ow % iw:
        return None
    reps = oh // ih
    if reps < 2 or ow // iw != reps:
        return None
    for r in range(oh):
        for c in range(ow):
            if output_grid[r][c] != input_grid[r % ih][c % iw]:
                return None
    return reps


def rotate(grid: Grid, quarter_turns: int) -> Grid:
    result = grid
    for _ in range(quarter_turns % 4):
        result = tuple(
            tuple(result[len(result) - 1 - r][c] for r in range(len(result)))
            for c in range(len(result[0]))
        )
    return result


def reflect_horizontal(grid: Grid) -> Grid:
    return tuple(reversed(grid))


def reflect_vertical(grid: Grid) -> Grid:
    return tuple(tuple(reversed(row)) for row in grid)


def is_rotation(input_grid: Grid, output_grid: Grid) -> bool:
    return any(rotate(input_grid, k) == output_grid for k in (1, 2, 3))


def is_reflection(input_grid: Grid, output_grid: Grid) -> bool:
    return output_grid in (reflect_horizontal(input_grid), reflect_vertical(input_grid))


def translation_delta(input_grid: Grid, output_grid: Grid) -> tuple[int, int] | None:
    source = sorted(cells_of(input_grid))
    target = sorted(cells_of(output_grid))
    if len(source) != len(target) or not source:
        return None
    dr = target[0][0] - source[0][0]
    dc = target[0][1] - source[0][1]
    if dr == 0 and dc == 0:
        return None
    shifted = sorted((r + dr, c + dc, v) for r, c, v in source)
    return (dr, dc) if shifted == target else None


def is_symmetric(grid: Grid) -> bool:
    return (
        reflect_horizontal(grid) == grid
        or reflect_vertical(grid) == grid
        or rotate(grid, 1) == grid
        or rotate(grid, 2) == grid
    )


def components(grid: Grid, *, background: int = 0) -> list[tuple[tuple[int, int, int], ...]]:
    """4-connected same-colour components, in deterministic scan order."""
    h, w = shape(grid)
    seen: set[Cell] = set()
    found: list[tuple[tuple[int, int, int], ...]] = []
    for r in range(h):
        for c in range(w):
            if (r, c) in seen or grid[r][c] == background:
                continue
            colour = grid[r][c]
            stack = [(r, c)]
            seen.add((r, c))
            cells: list[tuple[int, int, int]] = []
            while stack:
                cr, cc = stack.pop()
                cells.append((cr, cc, colour))
                for nr, nc in ((cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)):
                    if 0 <= nr < h and 0 <= nc < w and (nr, nc) not in seen and grid[nr][nc] == colour:
                        seen.add((nr, nc))
                        stack.append((nr, nc))
            found.append(tuple(sorted(cells)))
    return found


def component_boxes(grid: Grid) -> list[Box]:
    return [bbox_of_cells(cells) for cells in components(grid)]


def bbox_of_cells(cells: Iterable[tuple[int, int, int] | Cell]) -> Box:
    points = [(cell[0], cell[1]) for cell in cells]
    rows = [r for r, _ in points]
    cols = [c for _, c in points]
    return min(rows), min(cols), max(rows) + 1, max(cols) + 1


def component_crops(grid: Grid) -> list[Grid]:
    crops = []
    for cells in components(grid):
        top, left, bottom, right = bbox_of_cells(cells)
        colour = cells[0][2]
        canvas = [[0] * (right - left) for _ in range(bottom - top)]
        for r, c, _ in cells:
            canvas[r - top][c - left] = colour
        crops.append(tuple(tuple(row) for row in canvas))
    return crops


def enclosed_background(grid: Grid) -> set[Cell]:
    h, w = shape(grid)
    outside: set[Cell] = set()
    stack: list[Cell] = [(r, c) for r in range(h) for c in (0, w - 1)]
    stack += [(r, c) for c in range(w) for r in (0, h - 1)]
    while stack:
        r, c = stack.pop()
        if (r, c) in outside or not (0 <= r < h and 0 <= c < w) or grid[r][c] != 0:
            continue
        outside.add((r, c))
        stack.extend(((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)))
    return {(r, c) for r in range(h) for c in range(w) if grid[r][c] == 0 and (r, c) not in outside}


def full_separators(grid: Grid) -> tuple[list[int], list[int]]:
    h, w = shape(grid)
    rows = [r for r in range(h) if len(set(grid[r])) == 1 and grid[r][0] != 0]
    cols = [c for c in range(w) if len({grid[r][c] for r in range(h)}) == 1 and grid[0][c] != 0]
    return rows, cols


def _bands(separators: list[int], length: int) -> list[tuple[int, int]]:
    bands: list[tuple[int, int]] = []
    start = 0
    for index in separators:
        if index > start:
            bands.append((start, index))
        start = index + 1
    if start < length:
        bands.append((start, length))
    return bands


def separator_regions(grid: Grid) -> list[Grid]:
    rows, cols = full_separators(grid)
    if not rows and not cols:
        return []
    h, w = shape(grid)
    return [
        tuple(tuple(row[left:right]) for row in grid[top:bottom])
        for top, bottom in _bands(rows, h)
        for left, right in _bands(cols, w)
    ]
