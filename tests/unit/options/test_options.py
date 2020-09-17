"""Test Options object.

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


OPTION_1_KEYWORD = "option_1"
OPTION_2_KEYWORD = "option_2"
OPTION_3_KEYWORD = "option_3"
OPTION_4_KEYWORD = "option_4"
OPTION_5_KEYWORD = "option_5"


def test_simple_instantiation():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    options = Options(list(options_tuple))
    assert options.options == options_tuple
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()


def test_single_option_instantiation():
    options = Options(OPTION_1_KEYWORD)
    assert options.options == (OPTION_1_KEYWORD, )
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()


def test_instantiation_for_unordered_options_with_default():
    options_set = {OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD}
    options = Options(options_set)
    assert set(options.options) == options_set
    assert options.default == None
    assert options.unsupported == ()


def test_default_error_for_unordered_options_without_default():
    options_set = {OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD}
    options = Options(options_set, default=OPTION_1_KEYWORD)
    assert set(options.options) == options_set
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()


def test_value_error_for_default_option_not_option():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    expected_error_msg = re.escape(
        "`'option_5'` is not a valid choice of default as it is not an "
        "option. Please choose one of: `'option_1'`, `'option_2'` or "
        "`'option_3'`")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = Options(options_tuple, default=OPTION_5_KEYWORD)


def test_value_error_for_single_unsupported_option_not_option():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    expected_error_msg = re.escape(
        "`'option_5'` is not a valid choice of unsupported option as it is "
        "not an option. Please choose from: `'option_1'`, `'option_2'` and "
        "`'option_3'`")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = Options(options_tuple, unsupported=OPTION_5_KEYWORD)


def test_value_error_for_multiple_unsupported_option_not_option():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    expected_error_msg = re.escape(
        "`'option_4'` and `'option_5'` are not a valid choices of unsupported "
        "options as they are not options. Please choose from: `'option_1'`, "
        "`'option_2'` and `'option_3'`")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = Options(options_tuple,
                    unsupported=(OPTION_4_KEYWORD, OPTION_5_KEYWORD))
