"""Tests for lightweight Concept object."""

import pytest

from core import Concept


def test_concept_links_invariants():
    concept = Concept(
        concept_id="C-transform",
        label="Transformation",
        invariant_ids=["INV-reflect", "INV-rotate"],
    )
    assert "INV-reflect" in concept.invariant_ids
    assert concept.label == "Transformation"


def test_concept_rejects_empty_label():
    with pytest.raises(ValueError, match="label"):
        Concept(concept_id="C1", label="")


def test_concept_dict_round_trip():
    concept = Concept(
        concept_id="C1",
        label="Reflection",
        invariant_ids=["INV-1"],
        metadata={"mvp": True},
    )
    restored = Concept.from_dict(concept.to_dict())
    assert restored == concept
