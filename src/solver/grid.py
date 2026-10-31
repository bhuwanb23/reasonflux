"""Immutable grid primitives for the deterministic task solver (Phase 11).

Grids are tuples of tuples of ints so they hash and compare cheaply. Every
operation is pure: it returns a new ``Grid`` and never mutates its input.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

__all__ = [
    "Grid",
    "apply_operation",
    "count_objects",
    "group_by_color",
    "reflect_horizontal",
    "reflect_vertical",
    "rotate_90",
]

Cell = int


@dataclass(frozen=True, slots=True)
class Grid:
    """A rectangular grid of integer cells."""

    cells: tuple[tuple[Cell, ...], ...]

    def __post_init__(self) -> None:
        if not self.cells:
            raise ValueError("grid must have at least one row")
        widths = {len(row) for row in self.cells}
        if len(widths) != 1:
            raise ValueError("all rows must have equal width")
        if widths.pop() == 0:
            raise ValueError("rows must be non-empty")

    @classmethod
    def from_rows(cls, rows: Iterable[Iterable[int]]) -> Grid:
        return cls(tuple(tuple(int(c) for c in row) for row in rows))

    @property
    def height(self) -> int:
        return len(self.cells)

    @property
    def width(self) -> int:
        return len(self.cells[0])

    def to_rows(self) -> list[list[int]]:
        return [list(row) for row in self.cells]

    def colors(self) -> set[int]:
        return {c for row in self.cells for c in row}

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Grid) and self.cells == other.cells

    def __hash__(self) -> int:
        return hash(self.cells)


def reflect_horizontal(grid: Grid) -> Grid:
    """Mirror each row left-to-right (the usual "reflection" in ARC tasks)."""
    return Grid(tuple(tuple(reversed(row)) for row in grid.cells))


def reflect_vertical(grid: Grid) -> Grid:
    """Mirror the grid top-to-bottom."""
    return Grid(tuple(reversed(grid.cells)))


def rotate_90(grid: Grid) -> Grid:
    """Rotate 90 degrees clockwise."""
    h, w = grid.height, grid.width
    return Grid(
        tuple(tuple(grid.cells[h - 1 - r][c] for r in range(h)) for c in range(w))
    )


def count_objects(grid: Grid, *, background: int = 0) -> int:
    """Count 4-connected non-background components."""
    seen: set[tuple[int, int]] = set()
    total = 0
    for r in range(grid.height):
        for c in range(grid.width):
            if grid.cells[r][c] == background or (r, c) in seen:
                continue
            total += 1
            stack = [(r, c)]
            seen.add((r, c))
            while stack:
                cr, cc = stack.pop()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = cr + dr, cc + dc
                    if not (0 <= nr < grid.height and 0 <= nc < grid.width):
                        continue
                    if (nr, nc) in seen or grid.cells[nr][nc] == background:
                        continue
                    seen.add((nr, nc))
                    stack.append((nr, nc))
    return total


def group_by_color(grid: Grid) -> dict[int, int]:
    """Map each non-background color to its cell count."""
    counts: dict[int, int] = {}
    for row in grid.cells:
        for cell in row:
            if cell == 0:
                continue
            counts[cell] = counts.get(cell, 0) + 1
    return dict(sorted(counts.items()))


def apply_operation(name: str, grid: Grid) -> Grid | dict[int, int] | int:
    """Apply a named grid operation.

    Returns a ``Grid`` for geometric ops, an ``int`` for counting, or a
    color→count mapping for grouping. Raises ``KeyError`` for unknown ops.
    """
    ops = {
        "reflect_horizontal": reflect_horizontal,
        "reflect_vertical": reflect_vertical,
        "rotate_90": rotate_90,
        "count_objects": count_objects,
        "group_by_color": group_by_color,
    }
    if name not in ops:
        raise KeyError(f"unknown grid operation: {name!r}")
    return ops[name](grid)


def same_shape(a: Grid, b: Grid) -> bool:
    return a.height == b.height and a.width == b.width


def diff_cells(a: Grid, b: Grid) -> int:
    """Count differing cells; mismatched shapes count every cell as different."""
    if not same_shape(a, b):
        return max(a.height * a.width, b.height * b.width)
    return sum(
        1
        for ra, rb in zip(a.cells, b.cells)
        for ca, cb in zip(ra, rb)
        if ca != cb
    )


def as_int_grid(value: Sequence[Sequence[int]] | Grid) -> Grid:
    return value if isinstance(value, Grid) else Grid.from_rows(value)
