"""F3 transfer illusion WTS."""

import pytest

from invariants.robustness import compute_wts, difficulty_factor
from transfer import TransferType


def test_near_wts_much_less_than_structural():
    benefit = 0.8
    near = compute_wts(benefit, TransferType.NEAR)
    structural = compute_wts(benefit, TransferType.STRUCTURAL)
    assert near == pytest.approx(0.8 * difficulty_factor(TransferType.NEAR))
    assert structural == pytest.approx(0.8)
    assert near < structural * 0.5
