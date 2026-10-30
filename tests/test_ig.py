"""Intelligence Growth aggregator."""

from evaluation import GrowthConfig, compute_ig


def test_ig_default_weights():
    ig = compute_ig(cgr=0.2, tg=0.1, ug=0.05, ccg=0.1, compg=0.0)
    expected = 0.35 * 0.2 + 0.25 * 0.1 + 0.2 * 0.05 + 0.15 * 0.1 + 0.05 * 0.0
    assert abs(ig - expected) < 1e-9


def test_ig_custom_weights_and_zeros():
    assert compute_ig(0.0, 0.0, 0.0, 0.0, 0.0) == 0.0
    weights = {"cgr": 1.0, "tg": 0.0, "ug": 0.0, "ccg": 0.0, "compg": 0.0}
    assert abs(compute_ig(0.4, 1.0, 1.0, 1.0, 1.0, weights=weights) - 0.4) < 1e-9
    cfg = GrowthConfig(
        ig_w_cgr=0.5,
        ig_w_tg=0.5,
        ig_w_ug=0.0,
        ig_w_ccg=0.0,
        ig_w_compg=0.0,
    )
    assert abs(compute_ig(0.2, 0.4, growth_config=cfg) - 0.3) < 1e-9
