"""Utility functions for the whole Pyproprop package.

The module contains utility functions that can be used throughout the whole
Pyproprop package. These utilities predominantly process data and format it for
well-formatted console output, usually to be used in error messages.

"""


def format_case(item, case):
    """Allow :obj:`str` case formatting method application from keyword.

    Parameters
    ----------
    item : str
        Item to be case formatted.
    case : str
        Which case format method to use.

    Returns
    -------
    str
        :arg:`item` with case method applied.
    """
    if case == "title":
        return item.title()
    elif case == "upper":
        return item.upper()
    elif case == "lower":
        return item.lower()
    else:
        return item


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


def format_multiple_items_for_output(items, wrapping_char="'", *,
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
        Keyword for :func:`format_case`.
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
    items = [f"{prefix_char}{format_case(item, case)}" for item in items]
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
