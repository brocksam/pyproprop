"""Tests for processed properties with default and optional properties."""


import hypothesis.strategies as st
from hypothesis import given

from pyproprop import processed_property


class ClassWithDefaultProperties:
    """Dummy class for testing processed properties with default/optional
    values."""

    prop_a = processed_property("prop_a", type=int, optional=True)
    prop_b = processed_property("prop_b", type=int, optional=True, default=1)


@given(st.integers())
def test_optional_instantiation_with_int(test_value):
    """Property instantiates with default value correctly."""
    test_fixture = ClassWithDefaultProperties()
    test_fixture.prop_a = test_value
    test_fixture.prop_b = test_value
    assert test_fixture.prop_a == test_value
    assert test_fixture.prop_b == test_value


@given(st.just(None))
def test_optional_instantiation_with_none(test_value):
    """Property instantiates with default value correctly."""
    test_fixture = ClassWithDefaultProperties()
    test_fixture.prop_a = test_value
    test_fixture.prop_b = test_value
    assert test_fixture.prop_a is None
    assert test_fixture.prop_b == 1
