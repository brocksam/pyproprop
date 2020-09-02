"""Utility functions for the whole Pyproprop package.

The module contains utility functions that can be used throughout the whole
Pyproprop package. These utilities predominantly process data and format it for
well-formatted console output, usually to be used in error messages.

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
SUPPORTED_STR_FORMAT_OPTIONS : :py:obj:`set`
    Supported options for formatting methods, via identifiers.
FORMAT_STR_DISPATCHER : :py:obj:`dict`
    Dispatcher mapping string format identifier keywords to formatting
    functions.

"""

import re

import titlecase


LOWER_STR_CASE_FORMAT_KEYWORD = "lower"
UPPER_STR_CASE_FORMAT_KEYWORD = "upper"
TITLE_STR_CASE_FORMAT_KEYWORD = "title"
START_STR_CASE_FORMAT_KEYWORD = "start"
SNAKE_STR_CASE_FORMAT_KEYWORD = "snake"
PASCAL_STR_CASE_FORMAT_KEYWORD = "pascal"
SUPPORTED_STR_FORMAT_OPTIONS = {None,
                                LOWER_STR_CASE_FORMAT_KEYWORD,
                                UPPER_STR_CASE_FORMAT_KEYWORD,
                                TITLE_STR_CASE_FORMAT_KEYWORD,
                                START_STR_CASE_FORMAT_KEYWORD,
                                SNAKE_STR_CASE_FORMAT_KEYWORD,
                                PASCAL_STR_CASE_FORMAT_KEYWORD,
                                }


def generate_name_description_error_message(name,
                                            description,
                                            is_sentence_start=False,
                                            with_preposition=False):
    """Combine the name and description for correctly-formatted error.

    Parameters
    ----------
    is_sentence_start : bool, optional
        Should the formatted str be return in start case.
    with_preposition : bool, optional
        Should 'a' or 'an' be preappended to the error message.

    Returns
    -------
    str
        Formatted description.
    """
    need_an = {"a", "e", "h", "i", "o", "u"}
    if description is None:
        starts_with_vowel = name[0] in need_an
        if starts_with_vowel and with_preposition:
            return f"an `{name}`"
        elif with_preposition:
            return f"a `{name}`"
        return f"`{name}`"
    if with_preposition:
        first_word, _ = description.split(maxsplit=1)
        starts_with_vowel = first_word[0] in need_an
        is_acronym = first_word.upper() == first_word
        if starts_with_vowel or is_acronym:
            preposition = "an"
        else:
            preposition = "a"
        formatted_description = " ".join([preposition, description])
    else:
        formatted_description = description
    if is_sentence_start:
        formatted_description = format_str_case(formatted_description,
                                                START_STR_CASE_FORMAT_KEYWORD,
                                                process=True)
    return f"{formatted_description} (`{name}`)"


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

    Returns
    -------
    str
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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
        The string item passed as a parameter in formatted form.

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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
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

    Parameters
    ----------
    item : :py:obj:`str`
        The string object to be formatted.

    Returns
    -------
    str
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


def format_for_output(items, *args, **kwargs):
    """Utility method for formatting console output.

    Passes directly to :func:`format_multiple_items_for_output` just with a
    shorter function name.

    Parameters
    ----------
    items : iterable
        Items to be formatted for output.
    *args
        Variable length argument list.
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    str
        Formatted string for console output.
    """
    return format_multiple_items_for_output(items, *args, **kwargs)


def format_multiple_items_for_output(items, wrapping_char="`", *,
                                     prefix_char="", case=None,
                                     with_verb=False, with_or=False):
    """Format multiple items for pretty console output.

    Parameters
    ----------
    items : iterable of str
        Items to be formatted.
    wrapping_char : str (default `"'"`)
        Prefix and suffix character for format wrapping.
    prefix_char : str (default `""`)
        Additional prefix.
    case : str (default `None`)
        Keyword for :func:`format_str_case`.
    with_verb : bool, optional (default `False`)
        Append the correct conjugation of "is"/"are" to end of list.
    with_or : bool, optional
        Description

    Returns
    -------
    str
        Formatted string of multiple items for console output.
    """
    items = format_as_iterable(items)
    items = [f"{prefix_char}"
             f"{repr(format_str_case(item, case)) if isinstance(item, str) else repr(item)}"
             for item in items]
    if len(items) == 1:
        formatted_items = f"{wrapping_char}{items[0]}{wrapping_char}"
    else:
        pad = f"{wrapping_char}, {wrapping_char}"
        joiner = "or" if with_or else "and"
        formatted_items = (f"{wrapping_char}{pad.join(items[:-1])}"
                           f"{wrapping_char} {joiner} {wrapping_char}"
                           f"{items[-1]}{wrapping_char}")
    verb = "is" if len(items) == 1 else "are"
    if with_verb:
        formatted_items = f"{formatted_items} {verb}"

    return formatted_items


def format_as_iterable(items):
    """Checks whether an item can be iterated over like a list.

    Parameters
    ----------
    items : Any
        Object to be tested for whether it is a list-like iterable.

    Returns
    -------
    Union[Tuple[Any], Iterable[Any]]
        If the passed object is already a list-like iterable then this is
        returned straight away. Otherwise, the object is inserted in to a tuple
        of length 1.

    """
    if isinstance(items, str):
        return (items, )
    try:
        iter(items)
    except TypeError:
        return (items, )
    return items


FORMAT_STR_DISPATCHER = {None: lambda item: item,
                         LOWER_STR_CASE_FORMAT_KEYWORD: format_str_lower_case,
                         UPPER_STR_CASE_FORMAT_KEYWORD: format_str_upper_case,
                         TITLE_STR_CASE_FORMAT_KEYWORD: format_str_title_case,
                         START_STR_CASE_FORMAT_KEYWORD: format_str_start_case,
                         SNAKE_STR_CASE_FORMAT_KEYWORD: format_str_snake_case,
                         PASCAL_STR_CASE_FORMAT_KEYWORD: format_str_pascal_case,
                         }
