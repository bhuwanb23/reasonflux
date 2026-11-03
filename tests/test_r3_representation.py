from __future__ import annotations

from representations.r3 import (
    Action,
    ApplyStatus,
    Demonstration,
    ParseStatus,
    SearchStatus,
    SelectionStatus,
    Selector,
    apply_action,
    enumerate_candidates,
    parse_grid,
    run_search,
    select_object,
)


def test_parser_uses_same_color_four_connectivity_and_stable_ids():
    diagonal = parse_grid([[1, 0], [0, 1]])
    assert diagonal.status is ParseStatus.PARSED
    assert len(diagonal.objects) == 2
    assert diagonal.objects == parse_grid([[1, 0], [0, 1]]).objects

    joined = parse_grid([[1, 1], [0, 1]])
    assert len(joined.objects) == 1
    assert joined.objects[0].area == 3
    assert joined.objects[0].shape_signature == "2x2:1101"


def test_background_only_and_invalid_grid_are_distinct():
    assert parse_grid([[0, 0], [0, 0]]).status is ParseStatus.PARSED_NO_OBJECTS
    for raw in ([], [[1], [1, 2]], [[True]], [[10]], [[1.0]], ["12"]):
        assert parse_grid(raw).status is ParseStatus.INVALID_INPUT


def test_unique_selector_and_ambiguous_selector_rules():
    parsed = parse_grid([[1, 0, 1]])
    assert select_object(parsed, Selector("exact_color", 1)).status is SelectionStatus.SELECTOR_NOT_UNIQUE
    assert select_object(parsed, Selector("area_rank", 1)).status is SelectionStatus.SELECTOR_NOT_UNIQUE
    assert select_object(parsed, Selector("bbox_shape", "1x1:1")).status is SelectionStatus.SELECTOR_NOT_UNIQUE
    assert select_object(parsed, Selector("exact_color", 2)).status is SelectionStatus.SELECTOR_NO_MATCH
    assert select_object(parsed, Selector("exact_color", 0)).status is SelectionStatus.INVALID_SELECTOR


def test_move_clears_source_and_rejects_collision_or_out_of_bounds():
    parsed = parse_grid([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    result = apply_action(parsed, Selector("exact_color", 1), Action.make("move", dy=0, dx=1))
    assert result.status is ApplyStatus.APPLIED
    assert result.grid == ((0, 0, 0), (0, 0, 1), (0, 0, 0))
    assert apply_action(parsed, Selector("exact_color", 1), Action.make("move", dy=0, dx=2)).status is ApplyStatus.OUT_OF_BOUNDS

    blocked = parse_grid([[0, 0, 0], [0, 1, 2], [0, 0, 0]])
    collision = apply_action(blocked, Selector("exact_color", 1), Action.make("move", dy=0, dx=1))
    assert collision.status is ApplyStatus.COLLISION


def test_copy_preserves_source_and_rejects_overlap():
    parsed = parse_grid([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    copied = apply_action(parsed, Selector("exact_color", 1), Action.make("copy", dy=0, dx=1))
    assert copied.status is ApplyStatus.APPLIED
    assert copied.grid == ((0, 0, 0), (0, 1, 1), (0, 0, 0))
    assert apply_action(parsed, Selector("exact_color", 1), Action.make("copy", dy=0, dx=0)).status is ApplyStatus.COLLISION


def test_rectangular_rotation_swaps_bounding_box_dimensions():
    parsed = parse_grid([[1, 1, 0], [0, 0, 0]])
    rotated = apply_action(parsed, Selector("exact_color", 1), Action.make("rotate", k=1))
    assert rotated.status is ApplyStatus.APPLIED
    assert rotated.grid == ((1, 0, 0), (1, 0, 0))


def test_delete_recolor_zero_and_crop_bbox():
    parsed = parse_grid([[0, 0, 0, 0], [0, 2, 2, 0], [0, 2, 0, 0], [0, 0, 0, 0]])
    deleted = apply_action(parsed, Selector("exact_color", 2), Action.make("delete"))
    assert deleted.grid == tuple(tuple(0 for _ in range(4)) for _ in range(4))
    erased = apply_action(parsed, Selector("exact_color", 2), Action.make("recolor", color=0))
    assert erased.status is ApplyStatus.APPLIED
    assert erased.grid == deleted.grid
    cropped = apply_action(parsed, Selector("exact_color", 2), Action.make("crop_bbox"))
    assert cropped.grid == ((2, 2), (2, 0))


def test_rotation_and_reflections_use_frozen_local_coordinate_rules():
    parsed = parse_grid([[1, 1, 0], [1, 0, 0], [0, 0, 0]])
    rotated = apply_action(parsed, Selector("exact_color", 1), Action.make("rotate", k=1))
    assert rotated.status is ApplyStatus.APPLIED
    assert rotated.grid == ((1, 1, 0), (0, 1, 0), (0, 0, 0))
    horizontal = apply_action(parsed, Selector("exact_color", 1), Action.make("reflect_horizontal_axis"))
    assert horizontal.status is ApplyStatus.APPLIED
    assert horizontal.grid == ((1, 0, 0), (1, 1, 0), (0, 0, 0))
    vertical = apply_action(parsed, Selector("exact_color", 1), Action.make("reflect_vertical_axis"))
    assert vertical.status is ApplyStatus.APPLIED
    assert vertical.grid == ((1, 1, 0), (0, 1, 0), (0, 0, 0))


def test_enumerator_is_deterministic_and_cannot_exceed_ten():
    inputs = [[[0, 0, 0], [0, 1, 0], [0, 0, 0]]]
    a = enumerate_candidates(inputs, limit=10)
    b = enumerate_candidates(inputs, limit=10)
    assert len(a) == len(b) == 10
    assert [c.canonical_json for c in a] == [c.canonical_json for c in b]
    assert [c.candidate_id for c in a] == [c.candidate_id for c in b]
    assert len({c.candidate_id for c in a}) == 10
    for invalid in (0, 11, True):
        try:
            enumerate_candidates(inputs, limit=invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("enumeration limit outside 1..10 must fail")


def test_search_first_exact_fit_is_deterministic_and_shared_across_demos():
    grid = [[0] * 5 for _ in range(5)]
    grid[2][2] = 1
    first = enumerate_candidates([grid], limit=1)[0]
    out = apply_action(parse_grid(grid), first.selector, first.action)
    assert out.status is ApplyStatus.APPLIED
    demos = [Demonstration(grid, out.grid), Demonstration(grid, out.grid)]
    result = run_search(demos)
    assert result.status is SearchStatus.FOUND_EXACT_DEMO_FIT
    assert result.candidate == first
    assert len(result.trials) == 1
    assert run_search([]).status is SearchStatus.INVALID_INPUT
    assert run_search(demos, max_trials=11).status is SearchStatus.INVALID_INPUT


def test_one_candidate_parameterization_must_fit_every_demo():
    grid_a = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    grid_b = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    out_a = apply_action(parse_grid(grid_a), Selector("exact_color", 1), Action.make("move", dy=0, dx=1)).grid
    out_b = apply_action(parse_grid(grid_b), Selector("exact_color", 1), Action.make("move", dy=0, dx=2)).grid
    from representations.r3 import Candidate, _evaluate
    candidate = Candidate(Selector("exact_color", 1), Action.make("move", dy=0, dx=1))
    fits, reason = _evaluate(candidate, [Demonstration(grid_a, out_a), Demonstration(grid_b, out_b)])
    assert not fits
    assert reason == "DEMO_1:OUTPUT_MISMATCH"
