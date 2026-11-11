"""Transfer taxonomy classification and expected bands."""

from transfer import TransferType, classify_transfer, expected_transfer_band


def test_near_same_family():
    assert classify_transfer("reflect", "reflect") is TransferType.NEAR


def test_near_identical_ops():
    ops = ["find_symmetry", "apply_reflection"]
    assert (
        classify_transfer("a", "b", source_ops=ops, target_ops=ops) is TransferType.NEAR
    )


def test_moderate_shared_core_different_family():
    # Shared core, target has no extras, families differ → moderate
    # (identical op sets are near by taxonomy rule).
    assert (
        classify_transfer(
            "reflect",
            "reflect_group",
            source_ops=["reflect", "align"],
            target_ops=["reflect"],
        )
        is TransferType.MODERATE
    )
    # No op info, different families → moderate default
    assert classify_transfer("reflect", "reflect_group") is TransferType.MODERATE


def test_compositional_target_has_extra_ops():
    assert (
        classify_transfer(
            "reflect",
            "reflect_count",
            source_ops=["reflect"],
            target_ops=["reflect", "count"],
        )
        is TransferType.COMPOSITIONAL
    )


def test_structural_flag_or_many_extras():
    assert (
        classify_transfer("reflect", "complex", structural=True)
        is TransferType.STRUCTURAL
    )
    assert (
        classify_transfer(
            "reflect",
            "complex",
            source_ops=["reflect"],
            target_ops=["reflect", "rotate", "group"],
        )
        is TransferType.STRUCTURAL
    )


def test_default_cross_family_without_ops_is_moderate():
    assert classify_transfer("reflect", "count") is TransferType.MODERATE


def test_expected_bands():
    assert expected_transfer_band(TransferType.NEAR) == "very_high"
    assert expected_transfer_band(TransferType.MODERATE) == "medium"
    assert expected_transfer_band(TransferType.COMPOSITIONAL) == "medium_to_high"
    assert expected_transfer_band(TransferType.STRUCTURAL) == "high"
