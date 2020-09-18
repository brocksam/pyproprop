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


class ClassA:
    pass


class ClassB:
    pass


class ClassC:
    pass


def test_simple_instantiation():
    """:obj:`Options` can be instantiated and initialised correctly."""
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    options = Options(list(options_tuple))
    assert options.options == options_tuple
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()


def test_single_option_instantiation():
    """:obj:`Options` with single option can be instantiated and initialised
    correctly."""
    options = Options(OPTION_1_KEYWORD)
    assert options.options == (OPTION_1_KEYWORD, )
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()


def test_instantiation_for_unordered_options_without_default():
    """:obj:`Options` with multiple option can be instantiated and initialised
    correctly."""
    options_set = {OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD}
    options = Options(options_set)
    assert set(options.options) == options_set
    assert options.default is None
    assert options.unsupported == ()


def test_default_error_for_unordered_options_with_default():
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


def test_value_error_single_option_unsupported():
    expected_error_msg = re.escape(
        "All options (`'option_1'`) are unsupported.")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = Options(OPTION_1_KEYWORD, unsupported=OPTION_1_KEYWORD)


def test_value_error_multiple_options_all_unsupported():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    expected_error_msg = expected_error_msg = re.escape(
        "All options (`'option_1'`, `'option_2'` and `'option_3'`) are "
        "unsupported.")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = Options(options_tuple, unsupported=options_tuple)


def test_valid_handles():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    options = Options(options_tuple, handles=[ClassA, ClassB, ClassC])
    assert options.options == options_tuple
    assert options.default == OPTION_1_KEYWORD
    assert options.unsupported == ()
    assert options.handles == (ClassA, ClassB, ClassC)
    assert options.dispatcher == {
        OPTION_1_KEYWORD: ClassA,
        OPTION_2_KEYWORD: ClassB,
        OPTION_3_KEYWORD: ClassC,
    }


def test_type_error_handles_with_unordered_options():
    options_tuple = (OPTION_1_KEYWORD, OPTION_2_KEYWORD, OPTION_3_KEYWORD)
    expected_error_msg = ("Handles cannot be supplied when options have not "
                          "been supplied in a specified order.")
    with pytest.raises(TypeError, match=expected_error_msg):
        _ = Options(set(options_tuple), handles=[ClassA, ClassB, ClassC])
