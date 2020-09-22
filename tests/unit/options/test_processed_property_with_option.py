"""Test use of Options object with processed properties.

Attributes
----------
OPTION_1_KEYWORD : :obj:`str`
    Generic string identifier for testing.
OPTION_2_KEYWORD : :obj:`str`
    Generic string identifier for testing.
OPTION_3_KEYWORD : :obj:`str`
    Generic string identifier for testing.
OPTION_4_KEYWORD : :obj:`str`
    Generic string identifier for testing.
OPTION_5_KEYWORD : :obj:`str`
    Generic string identifier for testing.

"""
import re

import pytest

from pyproprop import Options
from pyproprop import processed_property

OPTION_1_KEYWORD = "option_1"
OPTION_2_KEYWORD = "option_2"
OPTION_3_KEYWORD = "option_3"
OPTION_4_KEYWORD = "option_4"
OPTION_5_KEYWORD = "option_5"

options_1_to_5 = (
    OPTION_1_KEYWORD,
    OPTION_2_KEYWORD,
    OPTION_3_KEYWORD,
    OPTION_4_KEYWORD,
    OPTION_5_KEYWORD,
)
options_3_to_5 = (
    OPTION_3_KEYWORD,
    OPTION_4_KEYWORD,
    OPTION_5_KEYWORD,
)

single_option = Options(OPTION_1_KEYWORD)
multiple_options = Options(options_1_to_5)
multiple_options_single_unsupported = Options(options_1_to_5,
                                              unsupported=OPTION_5_KEYWORD)
multiple_options_multiple_unsupported = Options(options_1_to_5,
                                                unsupported=options_3_to_5)


class ClassWithOptionProperties:
    """A class with processed properties to be used as fixture instances.

    Attributes
    ----------

    """

    one_option_prop = processed_property(
        "one_option_prop",
        description="option property with a single option",
        type=str,
        options=single_option,
    )
    mul_option_prop = processed_property(
        "mul_option_prop",
        description="option property with multiple options",
        type=str,
        options=multiple_options,
    )
    one_unsupported_option_prop = processed_property(
        "one_unsupported_option_prop",
        description=("option property with multiple options and a single "
                     "unsupported option"),
        type=str,
        options=multiple_options_single_unsupported,
    )
    mul_unsupported_option_prop = processed_property(
        "mul_unsupported_option_prop",
        description=("option property with multiple options and multiple "
                     "unsupported options"),
        type=str,
        options=multiple_options_multiple_unsupported,
    )

    def __init__(
            self,
            one_option=OPTION_1_KEYWORD,
            mul_option=OPTION_1_KEYWORD,
            one_unsupported_option=OPTION_1_KEYWORD,
            mul_unsupported_option=OPTION_1_KEYWORD,
    ):
        """Initialise the numerical bounds on the processed properties.

        Parameters
        ----------

        """
        self.one_option_prop = one_option
        self.mul_option_prop = mul_option
        self.one_unsupported_option_prop = one_unsupported_option
        self.mul_unsupported_option_prop = mul_unsupported_option


@pytest.fixture
def test_fixture():
    """Fixture with option properties."""
    return ClassWithOptionProperties()


def test_instantiation_class_with_option_properties():
    _ = ClassWithOptionProperties()


def test_single_option_all_unsupported_option():
    """"""
    expected_error_msg = re.escape(
        f"`one_all_unsupported_option_prop` does not have any supported "
        f"options from: `'option_1'`.")
    with pytest.raises(ValueError, match=expected_error_msg):

        class ClassWithSingleOptionAllUnsupportedOptionProperties:

            one_all_unsupported_option_prop = processed_property(
                "one_all_unsupported_option_prop",
                type=str,
                options=(OPTION_1_KEYWORD, ),
                unsupported_options=(OPTION_1_KEYWORD, ),
            )


def test_missing_option_kwarg_with_unsupported_option():
    """"""
    expected_error_msg = re.escape(
        f"`one_all_unsupported_option_prop` does not have any supported "
        f"options. Check unsupported options are valid options: `'option_1'`.")
    with pytest.raises(ValueError, match=expected_error_msg):

        class ClassWithSingleOptionAllUnsupportedOptionProperties:

            one_all_unsupported_option_prop = processed_property(
                "one_all_unsupported_option_prop",
                type=str,
                unsupported_options=(OPTION_1_KEYWORD, ),
            )


def test_correct_initialisation_class_with_option_properties(test_fixture):
    assert test_fixture.one_option_prop == OPTION_1_KEYWORD
    assert test_fixture.mul_option_prop == OPTION_1_KEYWORD
    assert test_fixture.one_unsupported_option_prop == OPTION_1_KEYWORD
    assert test_fixture.mul_unsupported_option_prop == OPTION_1_KEYWORD


def test_raises_value_error_with_invalid_option(test_fixture):
    with pytest.raises(ValueError):
        test_fixture.one_option_prop = OPTION_2_KEYWORD
    with pytest.raises(ValueError):
        test_fixture.one_unsupported_option_prop = OPTION_5_KEYWORD
