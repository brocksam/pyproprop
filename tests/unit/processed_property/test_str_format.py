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
START_KEYWORD : :py:obj:`str`
    String identifier for start case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
SNAKE_KEYWORD : :py:obj:`str`
    String identifier for snake case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
PASCAL_KEYWORD : :py:obj:`str`
    String identifier for pascal case formatting. This is the same keyword that
    is seen in :py:mod:`pyproprop/utils`.
HYPHEN_KEYWORD : :py:obj:`str`
    String identifier for hyphen case formatting. This is the same keyword that
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
EXAMPLE_STR_5 : :py:obj:`str`
    Test example involving different uses of underscores.
EXAMPLE_STR_5_FORMATTED : :py:obj:`dict`
    Expected formatted output strings for :py:const:`EXAMPLE_STR_5`.

"""

import pytest

from pyproprop import processed_property

# TODO - make example strings fixtures using pytes-cases (see issue #36)
LOWER_KEYWORD = "lower"
UPPER_KEYWORD = "upper"
TITLE_KEYWORD = "title"
START_KEYWORD = "start"
SNAKE_KEYWORD = "snake"
PASCAL_KEYWORD = "pascal"
HYPHEN_KEYWORD = "hyphen"

EXAMPLE_STR_1 = "this is a string"
EXAMPLE_STR_1_FORMATTED = {LOWER_KEYWORD: "this is a string",
                           UPPER_KEYWORD: "THIS IS A STRING",
                           TITLE_KEYWORD: "This Is a String",
                           START_KEYWORD: "This is a string",
                           SNAKE_KEYWORD: "this_is_a_string",
                           PASCAL_KEYWORD: "ThisIsAString",
                           HYPHEN_KEYWORD: "this-is-a-string",
                           }
EXAMPLE_STR_2 = "string with an   ABRV"
EXAMPLE_STR_2_FORMATTED = {LOWER_KEYWORD: "string with an abrv",
                           UPPER_KEYWORD: "STRING WITH AN ABRV",
                           TITLE_KEYWORD: "String With an ABRV",
                           START_KEYWORD: "String with an ABRV",
                           SNAKE_KEYWORD: "string_with_an_abrv",
                           PASCAL_KEYWORD: "StringWithAnABRV",
                           HYPHEN_KEYWORD: "string-with-an-abrv",
                           }
EXAMPLE_STR_3 = "string_with %_£+"
EXAMPLE_STR_3_FORMATTED = {LOWER_KEYWORD: "string_with %_£+",
                           UPPER_KEYWORD: "STRING_WITH %_£+",
                           TITLE_KEYWORD: "String_with %_£+",
                           START_KEYWORD: "String_with %_£+",
                           SNAKE_KEYWORD: "string_with",
                           PASCAL_KEYWORD: "StringWith",
                           HYPHEN_KEYWORD: "string-with",
                           }
EXAMPLE_STR_4 = "it's an example-with punctuation!"
EXAMPLE_STR_4_FORMATTED = {LOWER_KEYWORD: "it's an example-with punctuation!",
                           UPPER_KEYWORD: "IT'S AN EXAMPLE-WITH PUNCTUATION!",
                           TITLE_KEYWORD: "It's an Example-With Punctuation!",
                           START_KEYWORD: "It's an example-with punctuation!",
                           SNAKE_KEYWORD: "its_an_example_with_punctuation",
                           PASCAL_KEYWORD: "ItsAnExampleWithPunctuation",
                           HYPHEN_KEYWORD: "its-an-example-with-punctuation",
                           }

EXAMPLE_STR_5 = "string _with__lots___of_underscores_"
EXAMPLE_STR_5_FORMATTED = {LOWER_KEYWORD: "string _with__lots___of_underscores_",
                           UPPER_KEYWORD: "STRING _WITH__LOTS___OF_UNDERSCORES_",
                           TITLE_KEYWORD: "String _With__lots___of_underscores_",
                           START_KEYWORD: "String _with__lots___of_underscores_",
                           SNAKE_KEYWORD: "string_with_lots_of_underscores",
                           PASCAL_KEYWORD: "StringWithLotsOfUnderscores",
                           HYPHEN_KEYWORD: "string-with-lots-of-underscores",
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
        start_prop : :py:property:`processed_property`
            String processed property that automatically formats to start case.
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
        start_prop = processed_property("start_prop", type=str, default="",
                                        str_format="start")
        snake_prop = processed_property("snake_prop", type=str, default="",
                                        str_format="snake")
        pascal_prop = processed_property("pascal_prop", type=str, default="",
                                         str_format="pascal")
        hyphen_prop = processed_property("hyphen_prop", type=str, default="",
                                         str_format="hyphen")

        def __init__(self, lower_prop="", upper_prop="", title_prop="",
                     start_prop="", snake_prop="", pascal_prop="",
                     hyphen_prop=""):
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


@pytest.mark.parametrize("input_str, expected",
                         [(EXAMPLE_STR_1, EXAMPLE_STR_1_FORMATTED),
                          (EXAMPLE_STR_2, EXAMPLE_STR_2_FORMATTED),
                          (EXAMPLE_STR_3, EXAMPLE_STR_3_FORMATTED),
                          (EXAMPLE_STR_4, EXAMPLE_STR_4_FORMATTED),
                          (EXAMPLE_STR_5, EXAMPLE_STR_5_FORMATTED)])
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
    test_fixture.start_prop = input_str
    assert test_fixture.start_prop == expected[START_KEYWORD]
    test_fixture.snake_prop = input_str
    assert test_fixture.snake_prop == expected[SNAKE_KEYWORD]
    test_fixture.pascal_prop = input_str
    assert test_fixture.pascal_prop == expected[PASCAL_KEYWORD]
    test_fixture.hyphen_prop = input_str
    assert test_fixture.hyphen_prop == expected[HYPHEN_KEYWORD]
