"""Test formatting of options-related error messages in processed properties.

Attributes
----------
OPTIONS : :py:obj:`tuple`
    Collection of generic options for testing.
UNSUPPORTED_OPTIONS : :py:obj:`tuple`
    Collection of generic options from :py:const:`OPTIONS` arbitrarily deemed
    unsupported for testing purposes.
supported_options : :py:obj:`set`
    Difference between :py:const:`OPTIONS` and :py:const:`UNSUPPORTED_OPTIONS`.
"""

import re

from hypothesis import (assume, given)
import hypothesis.strategies as st
import pytest

from pyproprop import processed_property


OPTIONS = (None,
           "none",
           3,
           3.0,
           "3",
           "3.0",
           4,
           4.0,
           "4",
           "4.0",
           True,
           "True",
           )
UNSUPPORTED_OPTIONS = (True,
                       "True",
                       4,
                       4.0,
                       "4",
                       "4.0",
                       )
supported_options = set(OPTIONS).difference(set(UNSUPPORTED_OPTIONS))


@pytest.fixture
def test_fixture():
    """Fixture with options processed properties."""

    class ClassWithOptionsProperty:
        """A class with processed properties to be used as fixture instances.

        Attributes
        ----------
        options_prop : :py:property:`processed_property`
            Processed property that only takes an assortment of options. These
            options are random, contrived, of different types and are purely
            for testing purposes only.

        """
        options_prop = processed_property(
            "options_prop", options=OPTIONS,
            unsupported_options=UNSUPPORTED_OPTIONS)

        def __init__(self, option=None):
            """Initialise the numerical bounds on the processed properties.

            Parameters
            ----------
            option : obj
                Value to initialise the :py:attr:`options_prop` to.

            """
            self.options_prop = option

    return ClassWithOptionsProperty()


@pytest.mark.parametrize("option", supported_options)
def test_valid_options_set_correctly(test_fixture, option):
    test_fixture.options_prop = option
    assert test_fixture.options_prop == option


@pytest.mark.parametrize("option", UNSUPPORTED_OPTIONS)
def test_unsupported_options_raise_error(test_fixture, option):
    expected_error_msg = re.escape(
        f"`{repr(option)}` is not currently supported as an `options_prop`. "
        f"Choose one of: `None`, `'none'`, `3`, `3.0`, `'3'` or `'3.0'`.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.options_prop = option


@given(st.one_of(st.text()))
def test_invalid_options_raise_error(test_fixture, option):
    assume(option not in OPTIONS)
    expected_error_msg = re.escape(
        f"`{repr(option)}` is not a valid option of `options_prop`. Choose "
        f"one of: `None`, `'none'`, `3`, `3.0`, `'3'` or `'3.0'`.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.options_prop = option
