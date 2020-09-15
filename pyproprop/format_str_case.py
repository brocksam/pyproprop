"""Functions implementing several string formatting use cases.

The module exports the `format_str_case` function to both the module
`processed_property.py` and directly to users.

Attributes
----------
LOWER_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for lower case formatting.
UPPER_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for upper case formatting.
TITLE_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for title case formatting.
START_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for start case formatting.
SNAKE_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for snake case formatting.
PASCAL_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for pascal case formatting.
HYPHEN_STR_CASE_FORMAT_KEYWORD : :py:obj:`str`
    String identifier for hyphen case formatting.
SUPPORTED_STR_FORMAT_OPTIONS : :py:obj:`set`
    Supported options for formatting methods, via identifiers.
FORMAT_STR_DISPATCHER : :py:obj:`dict`
    Dispatcher mapping string format identifier keywords to formatting
    functions.

"""

import re

import titlecase


__all__ = ["format_str_case"]


LOWER_STR_CASE_FORMAT_KEYWORD = "lower"
UPPER_STR_CASE_FORMAT_KEYWORD = "upper"
TITLE_STR_CASE_FORMAT_KEYWORD = "title"
START_STR_CASE_FORMAT_KEYWORD = "start"
SNAKE_STR_CASE_FORMAT_KEYWORD = "snake"
PASCAL_STR_CASE_FORMAT_KEYWORD = "pascal"
HYPHEN_STR_CASE_FORMAT_KEYWORD = "hyphen"
SUPPORTED_STR_FORMAT_OPTIONS = {None,
                                LOWER_STR_CASE_FORMAT_KEYWORD,
                                UPPER_STR_CASE_FORMAT_KEYWORD,
                                TITLE_STR_CASE_FORMAT_KEYWORD,
                                START_STR_CASE_FORMAT_KEYWORD,
                                SNAKE_STR_CASE_FORMAT_KEYWORD,
                                PASCAL_STR_CASE_FORMAT_KEYWORD,
                                HYPHEN_STR_CASE_FORMAT_KEYWORD,
                                }


def format_str_case(item, case, process=False):
    """Format the given string to a specified formatting case.

    Options for formatting cases are: lower, upper, title, snake and pascal.

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.
    case : :py:obj:`str` or :py:obj:`None`
        The keyword identifier for which formatting method is to be used. This
        is used to trigger the correct function call from the
        :py:const:`FORMAT_STR_DISPATCHER` dispatcher.
    process : :py:obj:`bool`
        If `True`, whitespace is converted to a single space, whitespace is
        inserted after [,.!?], and leading/trailing whitespace is stripped.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    if process:
        # Convert whitespace to single space
        item = re.sub(" +", " ", item)
        # Insert whitespace after [,.!?]
        item = re.sub(r"([,.!?])([^ 0-9])", r"\1 \2", item)
        # Strip trailing or leading whitespace
        item = item.strip()
        # Dispatch specialised case format method
    return FORMAT_STR_DISPATCHER[case](item)


def format_str_lower_case(item):
    """Format the given string to lower case.

    Examples
    --------
    >>> format_str_lower_case("this is a string")
    "this is a string"

    >>> format_str_lower_case("string with an   ABRV")
    "string with an abrv"

    >>> format_str_lower_case("string_with %_£+")
    "string_with %_£+"

    >>> format_str_lower_case("it's an example-with punctuation!")
    "it's an example-with punctuation!"

    >>> format_str_lower_case("string _with__lots___of_underscores_")
    "string _with__lots___of_underscores_"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    return item.lower()


def format_str_upper_case(item):
    """Format the given string to upper case.

    Examples
    --------
    >>> format_str_upper_case("this is a string")
    "THIS IS A STRING"

    >>> format_str_upper_case("string with an   ABRV")
    "STRING WITH AN ABRV"

    >>> format_str_upper_case("string_with %_£+")
    "STRING_WITH %_£+"

    >>> format_str_upper_case("it's an example-with punctuation!")
    "IT'S AN EXAMPLE-WITH PUNCTUATION!"

    >>> format_str_upper_case("string _with__lots___of_underscores_")
    "STRING _WITH__LOTS___OF_UNDERSCORES_"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    return item.upper()


def format_str_title_case(item):
    """Format the given string to title case.

    Examples
    --------
    >>> format_str_title_case("this is a string")
    "This Is a String"

    >>> format_str_title_case("string with an   ABRV")
    "String With an ABRV"

    >>> format_str_title_case("string_with %_£+")
    "String_with %_£+"

    >>> format_str_title_case("it's an example-with punctuation!")
    "It's an Example-With Punctuation!"

    >>> format_str_title_case("string _with__lots___of_underscores_")
    "String _With__lots___of_underscores_"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    return titlecase.titlecase(item)


def format_str_start_case(item):
    """Format the given string to start case.

    Examples
    --------
    >>> format_str_start_case("this is a string")
    "This is a string"

    >>> format_str_start_case("string with an   ABRV")
    "String with an ABRV"

    >>> format_str_start_case("string_with %_£+")
    "String_with %_£+"

    >>> format_str_start_case("it's an example-with punctuation!")
    "It's an example-with punctuation!"

    >>> format_str_start_case("string _with__lots___of_underscores_")
    "String _with__lots___of_underscores_"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    Note
    ----
    Use :py:package:`titlecase` on first word for more intelligent
    capitalisation.

    """
    len_item = len(item)
    if len_item == 0:
        return ""
    elif len_item == 1:
        return item.upper()
    else:
        return item[0].upper() + item[1:]


def format_str_snake_case(item):
    """Format the given string to snake case.

    Examples
    --------
    >>> format_str_snake_case("this is a string")
    "this_is_a_string"

    >>> format_str_snake_case("string with an   ABRV")
    "string_with_an_abrv"

    >>> format_str_snake_case("string_with %_£+")
    "string_with"

    >>> format_str_snake_case("it's an example-with punctuation!")
    "its_an_example_with_punctuation"

    >>> format_str_snake_case("string _with__lots___of_underscores_")
    "string_with_lots_of_underscores"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    # Strip punctuation
    item = re.sub(r"[,'!?\"'#$£%&\()*+./:;<=>?@\[\\\]^`{|}~]", r"", item)
    # Replace separators with underscores
    item = re.sub(r"[ \-_]", r"_", item)
    # Replace more than one consecutive underscore with single underscore
    item = re.sub(r"_+", r"_", item)
    # Strip underscore from end of string
    item = re.sub(r"_$", r"", item)
    # Return lower case
    return item.lower()


def format_str_pascal_case(item):
    """Format the given string to pascal case.

    Examples
    --------
    >>> format_str_pascal_case("this is a string")
    "ThisIsAString"

    >>> format_str_pascal_case("string with an   ABRV")
    "StringWithAnABRV"

    >>> format_str_pascal_case("string_with %_£+")
    "StringWith"

    >>> format_str_pascal_case("it's an example-with punctuation!")
    "ItsAnExampleWithPunctuation"

    >>> format_str_pascal_case("string _with__lots___of_underscores_")
    "StringWithLotsOfUnderscores"

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    # Strip punctuation
    item = re.sub(r"[,'!?\"'#$£%&\()*+./:;<=>?@\[\\\]^`{|}~]", r"", item)
    # Replace separators with underscores
    item = re.sub(r"[ \-_]", r" ", item)
    # Replace more than one consecutive underscore with single underscore
    item = re.sub(r" +", r" ", item)
    # Strip underscore from end of string
    item = re.sub(r" $", r"", item)
    # Format title case
    item = titlecase.titlecase(item)
    # Iterate over words and ensure all start uppercase
    item = "".join(f"{word[0].capitalize()}{word[1:]}"
                   for word in item.split())
    # Return with underscores removed
    return re.sub(r" ", r"", item)


def format_str_hyphen_case(item):
    """Format the given string to hyphen case.

    Examples
    --------
    >>> format_str_hyphen_case("this is a string")
    "this-is-a-string"

    >>> format_str_hyphen_case("string with an   ABRV")
    "string-with-an-abrv"

    >>> format_str_hyphen_case("string_with %_£+")
    "string-with"

    >>> format_str_hyphen_case("it's an example-with punctuation!")
    "its-an-example-with-punctuation"

    >>> format_str_hyphen_case("string _with__lots___of_underscores_")
    "string-with-lots-of-underscores"
x
    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    :py:obj:`str`
        The string item passed as a parameter in formatted form.

    """
    # Strip punctuation
    item = re.sub(r"[,'!?\"'#$£%&\()*+./:;<=>?@\[\\\]^`{|}~]", r"", item)
    # Replace separators with hyphens
    item = re.sub(r"[ \-_]", r"-", item)
    # Replace more than one consecutive hyphen with single hyphen
    item = re.sub(r"-+", r"-", item)
    # Strip hyphen from end of string
    item = re.sub(r"-$", r"", item)
    # Return lower case
    return item.lower()


FORMAT_STR_DISPATCHER = {None: lambda item: item,
                         LOWER_STR_CASE_FORMAT_KEYWORD: format_str_lower_case,
                         UPPER_STR_CASE_FORMAT_KEYWORD: format_str_upper_case,
                         TITLE_STR_CASE_FORMAT_KEYWORD: format_str_title_case,
                         START_STR_CASE_FORMAT_KEYWORD: format_str_start_case,
                         SNAKE_STR_CASE_FORMAT_KEYWORD: format_str_snake_case,
                         PASCAL_STR_CASE_FORMAT_KEYWORD: format_str_pascal_case,
                         HYPHEN_STR_CASE_FORMAT_KEYWORD: format_str_hyphen_case,
                         }
