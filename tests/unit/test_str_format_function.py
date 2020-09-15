"""Test formatting of a string value."""

from pyproprop import format_str_case
import pytest
from pytest_cases import (fixture_ref, parametrize_plus)


@parametrize_plus("input_str, expected",
                  [fixture_ref("example_string_1"),
                   fixture_ref("example_string_2"),
                   fixture_ref("example_string_3"),
                   fixture_ref("example_string_4"),
                   fixture_ref("example_string_5")])
def test_formatted_string_method_expected_result(input_str, expected,
        LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
        SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Assert strings examples formatted exactly as expected, with `process`
    flag set to `True`.

    Additional example strings should be added in future to this test to ensure
    that a number of wider use-cases are supported.

    """
    assert format_str_case(input_str, case=LOWER_KEYWORD, process=True) == expected[LOWER_KEYWORD]
    assert format_str_case(input_str, case=UPPER_KEYWORD, process=True) == expected[UPPER_KEYWORD]
    assert format_str_case(input_str, case=TITLE_KEYWORD, process=True) == expected[TITLE_KEYWORD]
    assert format_str_case(input_str, case=START_KEYWORD, process=True) == expected[START_KEYWORD]
    assert format_str_case(input_str, case=SNAKE_KEYWORD, process=True) == expected[SNAKE_KEYWORD]
    assert format_str_case(input_str, case=PASCAL_KEYWORD, process=True) == expected[PASCAL_KEYWORD]
    assert format_str_case(input_str, case=HYPHEN_KEYWORD, process=True) == expected[HYPHEN_KEYWORD]
