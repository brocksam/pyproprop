"""Tests for processed properties that allow iterables.

"""
import pytest

from pyproprop import processed_property


@pytest.fixture
def test_fixture():
    class ClassWithIterableAllowedProperties:
        """Dummy class for fixtures with property that casts to floats

        Attributes
        ----------
        cast_prop : processed_prop
            Processed property that enforces casting to a np.ndarray.

        """

        cast_prop = processed_property(
            "cast_prop",
            type=float,
            cast=True,
            iterable_allowed=True,
        )

    return ClassWithIterableAllowedProperties()


@pytest.mark.parametrize("test_input, expected", [(1, 1.0)])
def test_casting_without_iterable(test_fixture, test_input, expected):
    """Values are cast when not an iterable"""
    test_fixture.cast_prop = test_input
    assert test_input == test_fixture.cast_prop == expected
    assert type(test_fixture.cast_prop) == type(expected)


@pytest.mark.parametrize("test_input, expected", [([1, 2], (1.0, 2.0)),
                                                  ((1, 2), (1.0, 2.0))])
def test_casting_with_iterable(test_fixture, test_input, expected):
    """Values are cast when an iterable"""
    test_fixture.cast_prop = test_input
    assert test_fixture.cast_prop == expected
    assert type(test_fixture.cast_prop) is tuple
    for val in test_fixture.cast_prop:
        assert type(val) is float
