"""F6 noisy trace weight."""

import pytest

from invariants.robustness import trace_weight, weight_from_steps


def test_low_tc_reduced_weight():
    assert trace_weight(0.8) == 1.0
    assert trace_weight(0.3) == pytest.approx(0.3)
    assert weight_from_steps(2, 10) == pytest.approx(0.2)
