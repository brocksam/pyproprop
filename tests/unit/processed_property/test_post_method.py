"""Test processed properties with post-methods applied."""


import hypothesis.strategies as st
import numpy as np
from hypothesis import given

from pyproprop import processed_property


def square(x):
    """Dummy function for squaring two numbers."""
    xx = x * x
    return xx


class ClassWithPostMethodProperty:
    """Dummy class for testing processed properties with post methods."""

    method_prop = processed_property("method_prop", type=int, method=square)
    np_method_prop = processed_property("np_method_prop", type=float,
                                        cast=True, method=np.cos)


@given(st.integers())
def test_post_method(test_value):
    """Applied python function correctly."""
    test_fixture = ClassWithPostMethodProperty()
    test_fixture.method_prop = test_value
    assert test_fixture.method_prop == square(test_value)


@given(st.floats(allow_infinity=False, allow_nan=False))
def test_post_method_numpy(test_value):
    """Applies numpy function correctly."""
    test_fixture = ClassWithPostMethodProperty()
    test_fixture.np_method_prop = test_value
    expected_result = np.cos(np.array([test_value]))
    assert (test_fixture.np_method_prop == expected_result).all()
