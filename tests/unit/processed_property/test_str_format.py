"""Test formatting of a string value within a processed property."""

from pyproprop import format_str_case, processed_property
import pytest
from pytest_cases import fixture_ref, parametrize_plus


@pytest.fixture
def test_fixture():
    """Fixture with string formatting processed properties."""

    class ClassWithStringFormatProperties:
        """A class with processed properties to be used as fixture instances.

        Attributes
        ----------
        lower_prop : :py:property:`processed_property`
            String processed property that automatically formats to lower case.
        upper_prop : :py:property:`processed_property`
            String processed property that automatically formats to upper case.
        title_prop : :py:property:`processed_property`
            String processed property that automatically formats to title case.
        start_prop : :py:property:`processed_property`
            String processed property that automatically formats to start case.
        snake_prop : :py:property:`processed_property`
            String processed property that automatically formats to snake case.
        pascal_prop : :py:property:`processed_property`
            String processed property that automatically formats to pascal
            case.

        """

        lower_prop = processed_property(
            "lower_prop", type=str, default="", str_format="lower"
        )
        upper_prop = processed_property(
            "upper_prop", type=str, default="", str_format="upper"
        )
        title_prop = processed_property(
            "title_prop", type=str, default="", str_format="title"
        )
        start_prop = processed_property(
            "start_prop", type=str, default="", str_format="start"
        )
        snake_prop = processed_property(
            "snake_prop", type=str, default="", str_format="snake"
        )
        pascal_prop = processed_property(
            "pascal_prop", type=str, default="", str_format="pascal"
        )
        hyphen_prop = processed_property(
            "hyphen_prop", type=str, default="", str_format="hyphen"
        )

        def __init__(
            self,
            lower_prop="",
            upper_prop="",
            title_prop="",
            start_prop="",
            snake_prop="",
            pascal_prop="",
            hyphen_prop="",
        ):
            """Initialise the numerical bounds on the processed properties.

            Parameters
            ----------
            lower : :py:obj:`str`
                Value to initialise the :py:attr:`lower_prop` to.
            upper : :py:obj:`str`
                Value to initialise the :py:attr:`upper_prop` to.
            title : :py:obj:`str`
                Value to initialise the :py:attr:`title_prop` to.
            start : :py:obj:`str`
                Value to initialise the :py:attr:`start_prop` to.
            snake : :py:obj:`str`
                Value to initialise the :py:attr:`snake_prop` to.
            pascal : :py:obj:`str`
                Value to initialise the :py:attr:`pascal_prop` to.
            hyphen : :py:obj:`str`
                Value to initialise the :py:attr:`hyphen_prop` to.

            """
            self.lower_prop = lower_prop
            self.upper_prop = upper_prop
            self.title_prop = title_prop
            self.start_prop = start_prop
            self.snake_prop = snake_prop
            self.pascal_prop = pascal_prop
            self.hyphen_prop = hyphen_prop

    return ClassWithStringFormatProperties()


@parametrize_plus(
    "input_str, expected",
    [
        fixture_ref("example_string_1"),
        fixture_ref("example_string_2"),
        fixture_ref("example_string_3"),
        fixture_ref("example_string_4"),
        fixture_ref("example_string_5"),
    ],
)
def test_formatted_string_expected_result(
    test_fixture,
    input_str,
    expected,
    LOWER_KEYWORD,
    UPPER_KEYWORD,
    TITLE_KEYWORD,
    START_KEYWORD,
    SNAKE_KEYWORD,
    PASCAL_KEYWORD,
    HYPHEN_KEYWORD,
):
    """Assert strings examples formatted exactly as expected.

    Additional example strings should be added in future to this test to ensure
    that a number of wider use-cases are supported.

    """
    test_fixture.lower_prop = input_str
    assert test_fixture.lower_prop == expected[LOWER_KEYWORD]
    test_fixture.upper_prop = input_str
    assert test_fixture.upper_prop == expected[UPPER_KEYWORD]
    test_fixture.title_prop = input_str
    assert test_fixture.title_prop == expected[TITLE_KEYWORD]
    test_fixture.start_prop = input_str
    assert test_fixture.start_prop == expected[START_KEYWORD]
    test_fixture.snake_prop = input_str
    assert test_fixture.snake_prop == expected[SNAKE_KEYWORD]
    test_fixture.pascal_prop = input_str
    assert test_fixture.pascal_prop == expected[PASCAL_KEYWORD]
    test_fixture.hyphen_prop = input_str
    assert test_fixture.hyphen_prop == expected[HYPHEN_KEYWORD]
