"""Utility functions for the whole Pyproprop package.

The module contains utility functions that can be used throughout the whole
Pyproprop package. These utilities predominantly process data and format it for
well-formatted console output, usually to be used in error messages.

"""

from .format_str_case import (format_str_case, START_STR_CASE_FORMAT_KEYWORD)


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
    :py:obj:`str`
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
        preposition = "an" if description[0] in need_an else "a"
        formatted_description = " ".join([preposition, description])
    else:
        formatted_description = description
    if is_sentence_start:
        formatted_description = format_str_case(formatted_description,
                                                START_STR_CASE_FORMAT_KEYWORD,
                                                process=True)
    return f"{formatted_description} (`{name}`)"


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
