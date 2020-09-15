import pytest

from pyproprop import format_str_case

# TODO - make example strings fixtures.
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


@pytest.mark.parametrize("input_str, expected",
                         [(EXAMPLE_STR_1, EXAMPLE_STR_1_FORMATTED),
                          (EXAMPLE_STR_2, EXAMPLE_STR_2_FORMATTED),
                          (EXAMPLE_STR_3, EXAMPLE_STR_3_FORMATTED),
                          (EXAMPLE_STR_4, EXAMPLE_STR_4_FORMATTED),
                          (EXAMPLE_STR_5, EXAMPLE_STR_5_FORMATTED)])
def test_formatted_string_method_expected_result_with_processing(input_str, expected):
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
