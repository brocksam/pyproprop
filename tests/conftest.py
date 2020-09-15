import os
import sys

import pytest
from pyproprop import processed_property
from typing import Iterable


@pytest.fixture(scope="session")
def LOWER_KEYWORD():
    """:py:obj:`str` : String identifier for lower case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "lower"


@pytest.fixture(scope="session")
def UPPER_KEYWORD():
    """:py:obj:`str` : String identifier for upper case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "upper"


@pytest.fixture(scope="session")
def TITLE_KEYWORD():
    """:py:obj:`str` : String identifier for title case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "title"


@pytest.fixture(scope="session")
def START_KEYWORD():
    """:py:obj:`str` : String identifier for start case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "start"


@pytest.fixture(scope="session")
def SNAKE_KEYWORD():
    """:py:obj:`str` : String identifier for snake case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "snake"


@pytest.fixture(scope="session")
def PASCAL_KEYWORD():
    """:py:obj:`str` : String identifier for pascal case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "pascal"


@pytest.fixture(scope="session")
def HYPHEN_KEYWORD():
    """:py:obj:`str` : String identifier for hyphen case formatting. This is
    the same keyword that is seen in :py:mod:`pyproprop/utils`."""
    return "hyphen"


@pytest.fixture(scope="session")
def TestProcessedProperties():
    """Fixture returning base object for testing."""

    class TestProcessedProperties:
        """Base class for testing pyproprop functionality."""

        _REQUIRED_LENGTH = 5
        _MAX_VALUE = 5
        _MIN_VALUE = 5
        _BOUNDS = (1, 10)
        _DEFAULT_INT = 5

        # TODO: expand to cover all use cases:
        #  * Find suitable post method for use in test.
        #  * Test description
        checked_type_int = processed_property(
            "checked_type_int",
            type=int,
            optional=True,
        )
        checked_type_float = processed_property(
            "checked_type_float",
            type=float,
            optional=True,
        )
        checked_type_str = processed_property(
            "checked_type_str",
            type=str,
            optional=True,
        )
        checked_type_iterable = processed_property(
            "checked_type_iterable",
            type=Iterable,
            optional=True,
        )
        checked_type_bool = processed_property(
            "checked_type_bool",
            type=bool,
            optional=True,
        )
        checked_list_len = processed_property(
            "checked_list_len",
            len=_REQUIRED_LENGTH,
            optional=True,
        )
        checked_max_value = processed_property(
            "checked_max_value",
            max=_MAX_VALUE,
            optional=True,
        )
        checked_min_value = processed_property(
            "checked_min_value",
            min=_MIN_VALUE,
            optional=True,
        )
        checked_max_value_excl = processed_property(
            "checked_max_value_excl",
            max=_MAX_VALUE,
            exclusive=True,
            optional=True,
        )
        checked_min_value_excl = processed_property(
            "checked_min_value_excl",
            min=_MIN_VALUE,
            exclusive=True,
            optional=True,
        )
        checked_bounds = processed_property(
            "checked_bounds",
            min=_BOUNDS[0],
            max=_BOUNDS[1],
            optional=True,
        )
        checked_iterable_allowed = processed_property(
            "checked_iterable_allowed",
            iterable_allowed=True,
            optional=True,
        )
        optional_prop = processed_property(
            "optional_prop",
            type=int,
            optional=True,
        )
        optional_prop_with_default = processed_property(
            "optional_prop_with_default",
            type=int,
            default=_DEFAULT_INT,
            optional=True,
        )
        cast_string = processed_property(
            "cast_string",
            type=str,
            cast=True,
        )
        optimisable_property = processed_property(
            "optimisable_property",
            optimisable=True,
        )
        int_from_options = processed_property(
            "int_from_options",
            description="integer from a set of options",
            type=int,
            cast=True,
            options=(1, 2),
        )

        def __init__(self, *,
                     checked_type_int=None,
                     checked_type_float=None,
                     checked_type_str=None,
                     checked_type_iterable=None,
                     checked_type_bool=None,
                     checked_list_len=None,
                     checked_max_value=None,
                     checked_min_value=None,
                     checked_max_value_excl=None,
                     checked_min_value_excl=None,
                     checked_bounds=None,
                     checked_iterable_allowed=None,
                     optional_prop=None,
                     optional_prop_with_default=None,
                     cast_string=None,
                     optimisable_property=None
                     ):

            self.checked_type_int = checked_type_int
            self.checked_type_float = checked_type_float
            self.checked_type_str = checked_type_str
            self.checked_type_iterable = checked_type_iterable
            self.checked_type_bool = checked_type_bool

            if checked_list_len is not None:
                self.checked_list_len = checked_list_len
            if checked_max_value is not None:
                self.checked_max_value = checked_max_value
            if checked_min_value is not None:
                self.checked_min_value = checked_min_value
            if checked_max_value_excl is not None:
                self.checked_max_value_excl = checked_max_value_excl
            if checked_min_value_excl is not None:
                self.checked_min_value_excl = checked_min_value_excl
            if checked_bounds is not None:
                self.checked_bounds = checked_bounds
            self.checked_iterable_allowed = checked_iterable_allowed
            self.optional_prop = optional_prop
            self.optional_prop_with_default = optional_prop_with_default
            self.cast_string = cast_string
            if optimisable_property is not None:
                self.optimisable_property = optimisable_property

    return TestProcessedProperties


@pytest.fixture(scope='session')
def example_string_1(LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
                     SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Strings for testing string formatting cases.

    Parameters
    ----------
    EXAMPLE_STR_1 : :py:obj:`str`
        Very basic test example.
    EXAMPLE_STR_1_FORMATTED : :py:obj:`dict`
        Expected formatted output strings for :py:const:`EXAMPLE_STR_1`.

    Returns
    -------
    :py:obj:`list`
        A list of :py:obj:`tuple`s, one for each `EXAMPLE_STR`, with each
        :py:obj:`tuple` structured as follows:
        `(EXAMPLE_STR_X, EXAMPLE_STR_X_FORMATTED)`.

    """

    EXAMPLE_STR_1 = "this is a string"
    EXAMPLE_STR_1_FORMATTED = {LOWER_KEYWORD: "this is a string",
                               UPPER_KEYWORD: "THIS IS A STRING",
                               TITLE_KEYWORD: "This Is a String",
                               START_KEYWORD: "This is a string",
                               SNAKE_KEYWORD: "this_is_a_string",
                               PASCAL_KEYWORD: "ThisIsAString",
                               HYPHEN_KEYWORD: "this-is-a-string",
                               }

    return (EXAMPLE_STR_1, EXAMPLE_STR_1_FORMATTED)


@pytest.fixture(scope='session')
def example_string_2(LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
                     SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Strings for testing string formatting cases.

    Parameters
    ----------
    LOWER_KEYWORD : :py:obj:`str`
        String identifier for lower case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    UPPER_KEYWORD : :py:obj:`str`
        String identifier for upper case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    TITLE_KEYWORD : :py:obj:`str`
        String identifier for title case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    START_KEYWORD : :py:obj:`str`
        String identifier for start case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    SNAKE_KEYWORD : :py:obj:`str`
        String identifier for snake case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    PASCAL_KEYWORD : :py:obj:`str`
        String identifier for pascal case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    HYPHEN_KEYWORD : :py:obj:`str`
        String identifier for hyphen case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    EXAMPLE_STR_2 : :py:obj:`str`
        Test example involving multiple spaces and an abbreviation.
    EXAMPLE_STR_2_FORMATTED : :py:obj:`dict`
        Expected formatted output strings for :py:const:`EXAMPLE_STR_2`.

    Returns
    -------
    :py:obj:`list`
        A list of :py:obj:`tuple`s, one for each `EXAMPLE_STR`, with each
        :py:obj:`tuple` structured as follows:
        `(EXAMPLE_STR_X, EXAMPLE_STR_X_FORMATTED)`.

    """

    EXAMPLE_STR_2 = "string with an   ABRV"
    EXAMPLE_STR_2_FORMATTED = {LOWER_KEYWORD: "string with an abrv",
                               UPPER_KEYWORD: "STRING WITH AN ABRV",
                               TITLE_KEYWORD: "String With an ABRV",
                               START_KEYWORD: "String with an ABRV",
                               SNAKE_KEYWORD: "string_with_an_abrv",
                               PASCAL_KEYWORD: "StringWithAnABRV",
                               HYPHEN_KEYWORD: "string-with-an-abrv",
                               }

    return (EXAMPLE_STR_2, EXAMPLE_STR_2_FORMATTED)


@pytest.fixture(scope='session')
def example_string_3(LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
                     SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Strings for testing string formatting cases.

    Parameters
    ----------
    LOWER_KEYWORD : :py:obj:`str`
        String identifier for lower case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    UPPER_KEYWORD : :py:obj:`str`
        String identifier for upper case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    TITLE_KEYWORD : :py:obj:`str`
        String identifier for title case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    START_KEYWORD : :py:obj:`str`
        String identifier for start case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    SNAKE_KEYWORD : :py:obj:`str`
        String identifier for snake case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    PASCAL_KEYWORD : :py:obj:`str`
        String identifier for pascal case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    HYPHEN_KEYWORD : :py:obj:`str`
        String identifier for hyphen case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    EXAMPLE_STR_3 : :py:obj:`str`
        Test example involving invalid identifier punctuation and underscores
        between words.
    EXAMPLE_STR_3_FORMATTED : :py:obj:`dict`
        Expected formatted output strings for :py:const:`EXAMPLE_STR_3`.

    Returns
    -------
    :py:obj:`list`
        A list of :py:obj:`tuple`s, one for each `EXAMPLE_STR`, with each
        :py:obj:`tuple` structured as follows:
        `(EXAMPLE_STR_X, EXAMPLE_STR_X_FORMATTED)`.

    """

    EXAMPLE_STR_3 = "string_with %_£+"
    EXAMPLE_STR_3_FORMATTED = {LOWER_KEYWORD: "string_with %_£+",
                               UPPER_KEYWORD: "STRING_WITH %_£+",
                               TITLE_KEYWORD: "String_with %_£+",
                               START_KEYWORD: "String_with %_£+",
                               SNAKE_KEYWORD: "string_with",
                               PASCAL_KEYWORD: "StringWith",
                               HYPHEN_KEYWORD: "string-with",
                               }

    return (EXAMPLE_STR_3, EXAMPLE_STR_3_FORMATTED)


@pytest.fixture(scope='session')
def example_string_4(LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
                     SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Strings for testing string formatting cases.

    Parameters
    ----------
    LOWER_KEYWORD : :py:obj:`str`
        String identifier for lower case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    UPPER_KEYWORD : :py:obj:`str`
        String identifier for upper case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    TITLE_KEYWORD : :py:obj:`str`
        String identifier for title case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    START_KEYWORD : :py:obj:`str`
        String identifier for start case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    SNAKE_KEYWORD : :py:obj:`str`
        String identifier for snake case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    PASCAL_KEYWORD : :py:obj:`str`
        String identifier for pascal case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    HYPHEN_KEYWORD : :py:obj:`str`
        String identifier for hyphen case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    EXAMPLE_STR_4 : :py:obj:`str`
        Test example involving punctuation, hyphenation between words and
        apostrophies.
    EXAMPLE_STR_4_FORMATTED : :py:obj:`dict`
        Expected formatted output strings for :py:const:`EXAMPLE_STR_4`.

    Returns
    -------
    :py:obj:`list`
        A list of :py:obj:`tuple`s, one for each `EXAMPLE_STR`, with each
        :py:obj:`tuple` structured as follows:
        `(EXAMPLE_STR_X, EXAMPLE_STR_X_FORMATTED)`.

    """

    EXAMPLE_STR_4 = "it's an example-with punctuation!"
    EXAMPLE_STR_4_FORMATTED = {LOWER_KEYWORD: "it's an example-with punctuation!",
                               UPPER_KEYWORD: "IT'S AN EXAMPLE-WITH PUNCTUATION!",
                               TITLE_KEYWORD: "It's an Example-With Punctuation!",
                               START_KEYWORD: "It's an example-with punctuation!",
                               SNAKE_KEYWORD: "its_an_example_with_punctuation",
                               PASCAL_KEYWORD: "ItsAnExampleWithPunctuation",
                               HYPHEN_KEYWORD: "its-an-example-with-punctuation",
                               }

    return (EXAMPLE_STR_4, EXAMPLE_STR_4_FORMATTED)


@pytest.fixture(scope='session')
def example_string_5(LOWER_KEYWORD, UPPER_KEYWORD, TITLE_KEYWORD, START_KEYWORD,
                     SNAKE_KEYWORD, PASCAL_KEYWORD, HYPHEN_KEYWORD):
    """Strings for testing string formatting cases.

    Parameters
    ----------
    LOWER_KEYWORD : :py:obj:`str`
        String identifier for lower case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    UPPER_KEYWORD : :py:obj:`str`
        String identifier for upper case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    TITLE_KEYWORD : :py:obj:`str`
        String identifier for title case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    START_KEYWORD : :py:obj:`str`
        String identifier for start case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    SNAKE_KEYWORD : :py:obj:`str`
        String identifier for snake case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    PASCAL_KEYWORD : :py:obj:`str`
        String identifier for pascal case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    HYPHEN_KEYWORD : :py:obj:`str`
        String identifier for hyphen case formatting. This is the same keyword
        that is seen in :py:mod:`pyproprop/utils`.
    EXAMPLE_STR_5 : :py:obj:`str`
        Test example involving different uses of underscores.
    EXAMPLE_STR_5_FORMATTED : :py:obj:`dict`
        Expected formatted output strings for :py:const:`EXAMPLE_STR_5`.

    Returns
    -------
    :py:obj:`list`
        A list of :py:obj:`tuple`s, one for each `EXAMPLE_STR`, with each
        :py:obj:`tuple` structured as follows:
        `(EXAMPLE_STR_X, EXAMPLE_STR_X_FORMATTED)`.

    """

    EXAMPLE_STR_5 = "string _with__lots___of_underscores_"
    EXAMPLE_STR_5_FORMATTED = {LOWER_KEYWORD: "string _with__lots___of_underscores_",
                               UPPER_KEYWORD: "STRING _WITH__LOTS___OF_UNDERSCORES_",
                               TITLE_KEYWORD: "String _With__lots___of_underscores_",
                               START_KEYWORD: "String _with__lots___of_underscores_",
                               SNAKE_KEYWORD: "string_with_lots_of_underscores",
                               PASCAL_KEYWORD: "StringWithLotsOfUnderscores",
                               HYPHEN_KEYWORD: "string-with-lots-of-underscores",
                               }

    return (EXAMPLE_STR_5, EXAMPLE_STR_5_FORMATTED)
