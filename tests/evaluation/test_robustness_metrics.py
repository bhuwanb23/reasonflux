"""IER, VST, TC, TFD formulas."""

import pytest

from invariants.robustness import (
    compute_ier,
    compute_tc,
    compute_tfd,
    compute_vst,
    variation_counts_from_metadata,
)


def test_compute_ier():
    assert compute_ier(10, 5) == pytest.approx(2.0)
    assert compute_ier(0, 0) == 0.0


def test_compute_vst_and_edges():
    assert compute_vst(3, 4) == pytest.approx(0.75)
    assert compute_vst(0, 0) == 1.0


def test_compute_tc_and_tfd():
    assert compute_tc(8, 10) == pytest.approx(0.8)
    assert compute_tfd(2, 10) == pytest.approx(0.2)


def test_variation_counts_from_metadata():
    meta = {
        "variations": ["color", "shape", "position", "count"],
        "failed_variations": ["color", "shape"],
    }
    s, t = variation_counts_from_metadata(meta)
    assert (s, t) == (2, 4)
