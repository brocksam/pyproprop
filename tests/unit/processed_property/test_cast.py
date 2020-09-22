"""Tests for processed properties casting input to a specified type.

Notes
-----
:py:obj:`bool` objects can not be cast from other objects under very specific
circumstances including when the :py:meth:`__bool__` method does not return
a boolean, or when the class is a weak reference.

"""
import numpy as np
import pytest

from pyproprop import processed_property


@pytest.fixture
def test_fixture():
    class ClassWithCastableProperties:
        """Dummy class for fixtures with property that casts to np.ndarray

        Attributes
        ----------
        cast_prop : processed_prop
            Processed property that enforces casting to a np.ndarray.

        """

        cast_prop = processed_property(
            "cast_prop",
            type=np.ndarray,
            cast=True,
        )

    return ClassWithCastableProperties()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ([1, 2, 3], np.array([1, 2, 3])),
        ([[1, 2, 3], [4, 5, 6]], np.array([[1, 2, 3], [4, 5, 6]])),
    ],
)
def test_casting_to_numpy_array(test_fixture, test_input, expected):
    """Valid iterables can be successfully cast to np.ndarray"""
    test_fixture.cast_prop = test_input
    assert type(test_fixture.cast_prop) == type(expected)
    assert np.array_equal(test_fixture.cast_prop, expected)
