"""Test formatting of a string value within a processed property.

Attributes
----------
LOWER_KEYWORD : :py:obj:`str`
    String identifier for lower case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
UPPER_KEYWORD : :py:obj:`str`
    String identifier for upper case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
TITLE_KEYWORD : :py:obj:`str`
    String identifier for title case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
SNAKE_KEYWORD : :py:obj:`str`
    String identifier for snake case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
PASCAL_KEYWORD : :py:obj:`str`
    String identifier for pascal case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
EXAMPLE_STR_1 : :py:obj:`str`
    Very basic test example.
EXAMPLE_STR_1_FORMATTED : :py:obj:`dict`
    Expected formatted output strings for :py:const:`EXAMPLE_STR_1`.
EXAMPLE_STR_2 : :py:obj:`str`
    Test example involving multiple spaces and an abbreviation.
EXAMPLE_STR_2_FORMATTED : :py:obj:`dict`
    Expected formatted output strings for :py:const:`EXAMPLE_STR_2`.
EXAMPLE_STR_3 : :py:obj:`str`
    Test example involving invalid identifier punctuation and underscores
    between words.
EXAMPLE_STR_3_FORMATTED : :py:obj:`dict`
    Expected formatted output strings for :py:const:`EXAMPLE_STR_3`.
EXAMPLE_STR_4 : :py:obj:`str`
    Test example involving punctuation, hyphenation between words and
    apostrophies.
EXAMPLE_STR_4_FORMATTED : :py:obj:`dict`
    Expected formatted output strings for :py:const:`EXAMPLE_STR_4`.

"""

import pytest

from pyproprop import processed_property


LOWER_KEYWORD = "lower"
UPPER_KEYWORD = "upper"
TITLE_KEYWORD = "title"
SNAKE_KEYWORD = "snake"
PASCAL_KEYWORD = "pascal"


EXAMPLE_STR_1 = "this is a string"
EXAMPLE_STR_1_FORMATTED = {LOWER_KEYWORD: "this is a string",
                           UPPER_KEYWORD: "THIS IS A STRING",
                           TITLE_KEYWORD: "This Is a String",
                           SNAKE_KEYWORD: "this_is_a_string",
                           PASCAL_KEYWORD: "ThisIsAString",
                           }
EXAMPLE_STR_2 = "string with an   ABRV"
EXAMPLE_STR_2_FORMATTED = {LOWER_KEYWORD: "string with an abrv",
                           UPPER_KEYWORD: "STRING WITH AN ABRV",
                           TITLE_KEYWORD: "String With an ABRV",
                           SNAKE_KEYWORD: "string_with_an_abrv",
                           PASCAL_KEYWORD: "StringWithAnABRV",
                           }
EXAMPLE_STR_3 = "string_with %_£+"
EXAMPLE_STR_3_FORMATTED = {LOWER_KEYWORD: "string_with %_£+",
                           UPPER_KEYWORD: "STRING_WITH %_£+",
                           TITLE_KEYWORD: "String_with %_£+",
                           SNAKE_KEYWORD: "string_with",
                           PASCAL_KEYWORD: "StringWith",
                           }
EXAMPLE_STR_4 = "it's an example-with punctuation!"
EXAMPLE_STR_4_FORMATTED = {LOWER_KEYWORD: "it's an example-with punctuation!",
                           UPPER_KEYWORD: "IT'S AN EXAMPLE-WITH PUNCTUATION!",
                           TITLE_KEYWORD: "It's an Example-With Punctuation!",
                           SNAKE_KEYWORD: "its_an_example_with_punctuation",
                           PASCAL_KEYWORD: "ItsAnExampleWithPunctuation",
                           }


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
        snake_prop : :py:property:`processed_property`
            String processed property that automatically formats to snake case.
        pascal_prop : :py:property:`processed_property`
            String processed property that automatically formats to pascal
            case.

        """
        lower_prop = processed_property("lower_prop", type=str, default="",
                                        str_format="lower")
        upper_prop = processed_property("upper_prop", type=str, default="",
                                        str_format="upper")
        title_prop = processed_property("title_prop", type=str, default="",
                                        str_format="title")
        snake_prop = processed_property("snake_prop", type=str, default="",
                                        str_format="snake")
        pascal_prop = processed_property("pascal_prop", type=str, default="",
                                         str_format="pascal")

        def __init__(self, lower_prop="", upper_prop="", title_prop="",
                     snake_prop="", pascal_prop=""):
            """Initialise the numerical bounds on the processed properties.

            Parameters
            ----------
            lower : :py:obj:`str`
                Value to initialise the :py:attr:`lower_prop` to.
            upper : :py:obj:`str`
                Value to initialise the :py:attr:`upper_prop` to.
            title : :py:obj:`str`
                Value to initialise the :py:attr:`title_prop` to.
            snake : :py:obj:`str`
                Value to initialise the :py:attr:`snake_prop` to.
            pascal : :py:obj:`str`
                Value to initialise the :py:attr:`pascal_prop` to.

            """
            self.lower_prop = lower_prop
            self.upper_prop = upper_prop
            self.title_prop = title_prop
            self.snake_prop = snake_prop
            self.pascal_prop = pascal_prop

    return ClassWithStringFormatProperties()


@pytest.mark.parametrize("input_str, expected",
                         [(EXAMPLE_STR_1, EXAMPLE_STR_1_FORMATTED),
                          (EXAMPLE_STR_2, EXAMPLE_STR_2_FORMATTED),
                          (EXAMPLE_STR_3, EXAMPLE_STR_3_FORMATTED),
                          (EXAMPLE_STR_4, EXAMPLE_STR_4_FORMATTED)])
def test_formatted_string_expected_result(test_fixture, input_str, expected):
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
    test_fixture.snake_prop = input_str
    assert test_fixture.snake_prop == expected[SNAKE_KEYWORD]
    test_fixture.pascal_prop = input_str
    assert test_fixture.pascal_prop == expected[PASCAL_KEYWORD]
