"""Utilities for type checking user input and generating error messages.

Processed properties are a way of defining property attributes for a class that
require input sanitation, type checking, function application, error message
generation etc. from user-supplied values in a manner that minimises code
reuse.

"""

from numbers import Real
from typing import Iterable

import numpy as np


__all__ = ["processed_property"]


def processed_property(name, **kwargs):
    """Main function for creating a processed property within a class.

    Parameters
    ----------
    name : str
        Attribute name that will be used for the property.
    **kwargs
        Arbitrary keyword arguments.

    Returns
    -------
    property
        The metaprogrammed property object with setter including specified
        settings.
    """
    storage_name = "_" + name
    description = kwargs.get("description")
    expected_type = kwargs.get("type")
    options = kwargs.get("options", None)
    unsupported_options = kwargs.get("unsupported_options", [])
    optional = kwargs.get("optional", False)
    default = kwargs.get("default", False)
    iterable_allowed = kwargs.get("iterable_allowed", False)
    cast_to_type = kwargs.get("cast", False)
    len_sequence = kwargs.get("len")
    max_value = kwargs.get("max")
    min_value = kwargs.get("min")
    exclusive = kwargs.get("exclusive", False)
    optimisable = kwargs.get("optimisable", False)
    post_method = kwargs.get("method")

    @property
    def prop(self):
        """Getter method for the property object.

        Returns
        -------
        obj
            The stored value of the property object held internally by the
            class in the 'private' variable of the name except with a leading
            underscore.
        """
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        """Setter method for the property object.

        Sequentially passes through a number of utility methods which enforce/
        apply the options specified when the processed property was created.

        Parameters
        ----------
        value : obj
            Property object value for setting.
        """
        if expected_type is not None:
            if iterable_allowed:
                if isinstance(value, Iterable):
                    value = tuple([check_type(val) for val in value])
                else:
                    value = (check_type(value), )
            else:
                value = check_type(value)
        if options is not None:
            check_options(value)
        if min_value is not None:
            check_min(value)
        if max_value is not None:
            check_max(value)
        if len_sequence is not None:
            check_len(value, len_sequence)
        if optimisable:
            value = process_optimisable(value)
        if post_method is not None:
            value = apply_method(value)
        setattr(self, storage_name, value)

    def check_type(value):
        """Ensure the type of the property value to be set is as specified.

        Parameters
        ----------
        value : obj
            Property object value for setting.

        Returns
        -------
        Optional[obj]
            The value is return if is already of the expected type. If the
            value is None and the property has been specified as optional, None
            is returned unless there is a default in which case the default is
            returned and cast to the expected type. Finally the supplied value
            is attempted to be cast to the specified type and if successful
            this is returned.

        Raises
        ------
        TypeError
            If the type of the value to be set do not match the specified
            required type.
        """
        if isinstance(value, expected_type):
            return value
        elif optional and value is None:
            if default:
                return expected_type(default)
            else:
                return None
        elif cast_to_type:
            return cast_type(value)
        else:
            msg = (f"`{name}` must be a {repr(expected_type)}, instead got a "
                   f"{repr(type(value))}.")
            raise TypeError(msg)

    def cast_type(value):
        """Enforce type casting of property value to be set to specific type.

        Parameters
        ----------
        value : obj
            Property object value for setting.

        Returns
        -------
        obj
            Supplied value cast to the specified type

        Raises
        ------
        ValueError
            If the casting fails.
        TypeError
            If the casting fails.
        """
        cast_str = f"processed_value = {expected_type.__name__}({value})"
        try:
            exec(cast_str)
        except (ValueError, TypeError) as e:
            msg = (f"`{name}` must be a {repr(expected_type)}, instead got a "
                   f"{repr(type(value))} which cannot be cast.")
            raise e(msg)
        return locals()['processed_value']

    def check_options(value):
        """Ensure user-supplied value is a valid option.

        Options for property can fall in to two camps: valid options and
        unsupported options. Unsupported options are valid options, however
        they are not currently implemented by the package. They are specified
        in this way to inform the user that they should become supported in the
        future as this is the intended roadmap of the package designer.

        Parameters
        ----------
        value : obj
            Property object value for setting.

        Raises
        ------
        ValueError
            If value trying to be set is not a valid option or is an
            unsupported option.
        """
        valid_options = [option for option in options
                         if option not in unsupported_options]
        formatted_valid_options = format_for_output(valid_options,
                                                    with_or=True)
        if value in unsupported_options:
            formatted_unsupported_option = format_for_output(value,
                                                             with_verb=True)
            formatted_description = format_for_output([description],
                                                      wrapping_char="",
                                                      with_preposition=True)
            msg = (
                f"{formatted_unsupported_option} not currently supported as "
                f"{formatted_description}. Choose one of: "
                f"{formatted_valid_options}."
            )
            raise ValueError(msg)
        elif value not in options:
            formatted_value = format_for_output(value, with_verb=True)
            msg = (
                f"{formatted_value} not a valid option of {description}. "
                f"Choose one of: {formatted_valid_options}.")
            raise ValueError(msg)

    def check_min(value):
        """Ensure the numerical value of property being set is greater than
        specified minimum.

        Parameters
        ----------
        value : float
            Property object value for setting.

        Raises
        ------
        ValueError
            If the value attempting to be set is less than the specified
            minimum.
        """
        if exclusive:
            if value <= min_value:
                msg = (f"{make_title_case(name)} must be greater than "
                       f"{min_value}. {value} is invalid.")
                raise ValueError(msg)
        else:
            if value < min_value:
                msg = (f"{make_title_case(name)} must be greater than "
                       f"or equal to {min_value}. {value} is invalid.")
                raise ValueError(msg)

    def check_max(value):
        """Ensure the numerical value of property being set is less than
        specified maximum.

        Parameters
        ----------
        value : float
            Property object value for setting.

        Raises
        ------
        ValueError
            If the value attempting to be set is less than the specified
            maximum.
        """
        if exclusive:
            if value >= max_value:
                msg = (f"{make_title_case(name)} must be less than "
                       f"{max_value}. {value} is invalid.")
                raise ValueError(msg)
        else:
            if value > max_value:
                msg = (f"{make_title_case(name)} must be less than or "
                       f"equal to {max_value}. {value} is invalid.")
                raise ValueError(msg)

    def make_title_case(description):
        if len(description) > 1:
            title_description = description[0].upper() + description[1:]
            return title_description
        return description.upper()

    def check_len(value, len_sequence):
        """Enforces the set sequence length to be equal to a specified value.

        Parameters
        ----------
        value : obj
            Property object value for setting.
        len_sequence : obj:`int`
            Length of desired sequence.

        Raises
        ------
        ValueError
            If sequence length and specified value are not equal.

        """
        if len(value) != len_sequence:
            msg = (f"`{name}` must be a sequence of length {len_sequence}.")
            raise ValueError(msg)

    def apply_method(value):
        """Applies a specified method at the end of the property setter.

        Parameters
        ----------
        value : obj
            Property object value for setting.

        Returns
        -------
        obj
            Property object value with post-method applied.
        """
        if optional and value is None:
            return None
        return post_method(value)

    def process_optimisable(value):
        """Processes properties flagged as `optimisable`.

        Parameters
        ----------
        value : obj
            Property object value for setting.

        Returns
        -------
        `numbers.Real`
            If a number is supplied by user.
        `tuple`
            If a set of valid bounds are supplied (see `check_bounds`).
        `ValueError`
            If supplied `Iterable` is not of length 2.
        `Type Error`
            If either supplied bounds are not of type `numbers.Real` or 
            the single supplied value is not of type `numbers.Real`

        """
        if isinstance(value, Real):
            return value
        if isinstance(value, Iterable):
            check_len(value, 2)
            bounds = []
            msg = (f"Both {name} bounds must be of type {Real}, instead got "
                f"{value[0]} at index 0 (type {type(value[0])}) and "
                f"{value[1]} at index 1 (type {type(value[1])}).")
            for bound in value:
                if not isinstance(bound, Real):
                    raise TypeError(msg)
                bounds.append(bound)
            bounds = check_bounds(bounds)
            return bounds
        msg = (f"{name} must be a {Real} or {Iterable} of length 2, instead "
            f"got {repr(type(value))}.")
        raise TypeError(msg)

    def check_bounds(bounds):
        """Validates bounds for `optimisable` processed property.

        Parameters
        ----------
        bounds : :obj:`Iterable`
            `Iterable` of bounds to be validated.

        Returns
        -------
        :obj:`numbers.Real`
            If the first bound equals the second bound.
        :obj:`tuple`
            If the second bound exceeds the first bound.
        `ValueError`
            If the first bound exceeds the second bound.

        """
        lower_bound = bounds[0]
        upper_bound = bounds[1]
        try:
            # Test if both bounds can be represented as signed 64-bit number.
            np.asarray(bounds, dtype=np.int64)
        except OverflowError:
            msg = ("Individual bounds must be able to be represented as a "
                   "signed 64-bit number, and hence must lie in the range "
                   "(-9223372036854775808, 9223372036854775807).")
            raise ValueError(msg)
        if np.isclose(lower_bound, upper_bound):
            return lower_bound
        if lower_bound > upper_bound:
            msg = (f"Lower bound ({lower_bound}) at index 0 must be less "
                f"than upper bound ({upper_bound}) at index 1.")
            raise ValueError(msg)
        return tuple(bounds)

    return prop


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
                                     with_verb=False, with_or=False,
                                     with_preposition=False):
    """Format multiple items for pretty console output.

    Args
    ----
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

    Returns
    -------
    str
        Formatted string of multiple items for console output.
    """
    items = (items, ) if isinstance(items, str) else items
    items = [f"{prefix_char}{format_case(item, case)}" for item in items]
    if len(items) == 1:
        formatted_items = f"{wrapping_char}{items[0]}{wrapping_char}"
        if with_preposition and wrapping_char == "":
            first_word, _ = formatted_items.split(maxsplit=1)
            starts_with_vowel = first_word[0] in {"a", "e", "h", "i", "o", "u"}
            is_acronym = first_word.upper() == first_word
            if starts_with_vowel or is_acronym:
                preposition = "an"
            else:
                preposition = "a"
            formatted_items = " ".join([preposition, formatted_items])
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
