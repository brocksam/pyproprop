"""Test optimisable processed properties."""

import pytest

from pyproprop import processed_property


class ClassWithOptimisableProperty:
    """Dummy class with optimisable processed property for tests.

    Attributes
    ----------
    optimisable_prop : :py:property:
        Optimisable property that accepts either a single value or an iterable
        of length two (with first entry less than or equal to second entry if
        type is numeric).

    """

    optimisable_prop = processed_property("optimisable_prop", optimisable=True)


@pytest.fixture
def test_fixture():
    """Fixture for easy instantiation of class with optimisable property."""
    return ClassWithOptimisableProperty()


def test_instantiation():
    """Optimisable properties can be instantiated successfully."""
    _ = ClassWithOptimisableProperty()


def test_optimisable_property_has_is_optimisable_attr():
    """Optimisable processed property has `is_optimisable` attr."""
    assert hasattr(ClassWithOptimisableProperty.optimisable_prop,
                   "is_optimisable")
    assert ClassWithOptimisableProperty.optimisable_prop.is_optimisable is True
