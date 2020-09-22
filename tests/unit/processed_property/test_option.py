"""Tests for processed properties with enforced (and unsupported) options.

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

from pyproprop import processed_property

OPTION_1_KEYWORD = "option_1"
OPTION_2_KEYWORD = "option_2"
OPTION_3_KEYWORD = "option_3"
OPTION_4_KEYWORD = "option_4"
OPTION_5_KEYWORD = "option_5"


class ClassWithOptionProperties:
    """A class with processed properties to be used as fixture instances.

    Attributes
    ----------

    """

    one_option_prop = processed_property(
        "one_option_prop",
        description="option property with a single option",
        type=str,
        str_format="snake",
        options=(OPTION_1_KEYWORD, ),
    )
    mul_option_prop = processed_property(
        "mul_option_prop",
        description="option property with multiple options",
        type=str,
        str_format="snake",
        options=(
            OPTION_1_KEYWORD,
            OPTION_2_KEYWORD,
            OPTION_3_KEYWORD,
            OPTION_4_KEYWORD,
            OPTION_5_KEYWORD,
        ),
    )
    one_unsupported_option_prop = processed_property(
        "one_unsupported_option_prop",
        description=("option property with multiple options and a single "
                     "unsupported option"),
        type=str,
        str_format="snake",
        options=(
            OPTION_1_KEYWORD,
            OPTION_2_KEYWORD,
            OPTION_3_KEYWORD,
            OPTION_4_KEYWORD,
            OPTION_5_KEYWORD,
        ),
        unsupported_options=(OPTION_5_KEYWORD, ),
    )
    mul_unsupported_option_prop = processed_property(
        "mul_unsupported_option_prop",
        description=("option property with multiple options and multiple "
                     "unsupported options"),
        type=str,
        str_format="snake",
        options=(
            OPTION_1_KEYWORD,
            OPTION_2_KEYWORD,
            OPTION_3_KEYWORD,
            OPTION_4_KEYWORD,
            OPTION_5_KEYWORD,
        ),
        unsupported_options=(
            OPTION_3_KEYWORD,
            OPTION_4_KEYWORD,
            OPTION_5_KEYWORD,
        ),
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


@pytest.mark.parametrize(
    "input_str",
    [
        "option-1", "Option 1  ", "Option__1", "OpTiOn _-1 -__",
        "    OPTION_1---"
    ],
)
def test_setting_with_valid_options(test_fixture, input_str):
    test_fixture.one_option_prop = input_str
    assert test_fixture.one_option_prop == OPTION_1_KEYWORD


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


def test_no_option_with_unsupported_option():
    """"""
    expected_error_msg = re.escape(
        f"`one_all_unsupported_option_prop` does not have any supported "
        f"options. Check unsupported options are valid options: `'option_1'`.")
    with pytest.raises(ValueError, match=expected_error_msg):

        class ClassWithSingleOptionAllUnsupportedOptionProperties:

            one_all_unsupported_option_prop = processed_property(
                "one_all_unsupported_option_prop",
                type=str,
                options=(),
                unsupported_options=(OPTION_1_KEYWORD, ),
            )


def test_multiple_option_all_are_unsupported_option():
    """"""
    expected_error_msg = re.escape(
        f"`mul_all_unsupported_option_prop` does not have any supported "
        f"options from: `'option_1'`, `'option_2'`, `'option_3'`, "
        f"`'option_4'` and `'option_5'`.")
    with pytest.raises(ValueError, match=expected_error_msg):

        class ClassWithMultipleOptionAllUnsupportedOptionProperties:

            mul_all_unsupported_option_prop = processed_property(
                "mul_all_unsupported_option_prop",
                type=str,
                options=(
                    OPTION_1_KEYWORD,
                    OPTION_2_KEYWORD,
                    OPTION_3_KEYWORD,
                    OPTION_4_KEYWORD,
                    OPTION_5_KEYWORD,
                ),
                unsupported_options=(
                    OPTION_1_KEYWORD,
                    OPTION_2_KEYWORD,
                    OPTION_3_KEYWORD,
                    OPTION_4_KEYWORD,
                    OPTION_5_KEYWORD,
                ),
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


def test_option_creation_from_dict_keys():
    class ClassWithMultipleOptionAllUnsupportedOptionProperties:

        option_from_dict_keys_prop = processed_property(
            "option_from_dict_keys_prop",
            type=str,
            options={
                OPTION_1_KEYWORD: None,
                OPTION_2_KEYWORD: None,
                OPTION_3_KEYWORD: None,
                OPTION_4_KEYWORD: None,
                OPTION_5_KEYWORD: None,
            }.keys(),
            unsupported_options=(OPTION_5_KEYWORD, ),
        )

    def __init__(self):
        self.option_from_dict_keys_prop = OPTION_1_KEYWORD

    _ = ClassWithMultipleOptionAllUnsupportedOptionProperties()
