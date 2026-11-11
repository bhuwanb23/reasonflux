"""System-level Transfer Score (TS)."""

import pytest

from evaluation import compute_ts


def test_compute_ts_difference():
    assert compute_ts(0.4, 0.7) == pytest.approx(0.3)
    assert compute_ts(0.5, 0.5) == pytest.approx(0.0)
    assert compute_ts(0.8, 0.5) == pytest.approx(-0.3)


def test_compute_ts_coerces_numeric():
    assert compute_ts(1, 2) == pytest.approx(1.0)
