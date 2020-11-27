"""Utilities for type checking user input and generating error messages.

Processed properties are a way of defining property attributes for a class that
require input sanitation, type checking, function application, error message
generation etc. from user-supplied values in a manner that minimises code
reuse.

"""
from numbers import Real
from typing import Any, Iterable, Tuple

import numpy as np

from .format_str_case import SUPPORTED_STR_FORMAT_OPTIONS, format_str_case
from .options import Options
from .utils import format_for_output, generate_name_description_error_message

__all__ = ["processed_property"]


class property(property):
    """Subclass in-built property type so attributes can be set."""
    pass


def processed_property(name, **kwargs):
    """Main function for creating a processed property within a class.

    Parameters
    ----------
    name : str
        Attribute name that will be used for the property.
    read_only : bool, False
        If a processed property is specified as read-only then after its value
        has been set once (i.e. after it has been instantiated), it is not able
        to be set again.
    type : type, None
        Tells the processed property the type of the value that the setter is
        expecting. If the value passed to the setter is not of this type then a
        TypeError will be raised.
    cast : bool, False
        Defines whether the value passed to the processed property's setter
        should be attempted to be cast to the expected type.
    optional : bool, False
        In additional to other specifications for the processed property, a
        value of `None` is also accepted.
    default : obj, None
        If a processed property is specified as `optional`, then if a value of
        `None` is supplied to the setter this is instead replaced with this
        specified default value.

    Returns
    -------
    property
        The metaprogrammed property object with setter including specified
        settings.

    """

    def parse_kwarg(kwarg_name, description, valids, default):
        kwarg = kwargs.get(kwarg_name, default)
        if isinstance(valids, type) and not isinstance(kwarg, valids):
            msg = (f"{repr(kwarg)} is not a valid {description}. Please "
                   f"use a value of type {repr(valids)}.")
            raise TypeError(msg)
        elif not isinstance(valids, type) and kwarg not in valids:
            formatted_valids = format_for_output(valids, with_or=True)
            msg = (f"{repr(kwarg)} is not a valid {description}. Please "
                   f"choose one of: {formatted_valids}.")
            raise ValueError(msg)
        return kwarg

    def error_check_option_kwarg(options, unsupported_options):
        """Error checking of the `options` and `unsupported_options`.

        Returns
        -------
        tuple of tuples
            Tuple of length two where the first element is a tuple of the
            options and the second is a tuple of the unsupported options.

        Raises
        ------
        ValueError
            If an unsupported option is specified that is also not specified as
            an option. If all of the options specified are also specified as
            unsupported options. If unsupported options are specified but no
            options are.

        """
        if isinstance(options, Options):
            return options.options, options.unsupported
        if (options is None and unsupported_options) or (
                set(unsupported_options).difference(set(options))):
            msg = (f"{name_str} does not have any supported options. Check "
                   f"unsupported options are valid options: "
                   f"{format_for_output(unsupported_options)}.")
            raise ValueError(msg)
        if not set(options).symmetric_difference(set(unsupported_options)):
            msg = (f"{name_str} does not have any supported options from: "
                   f"{format_for_output(options)}.")
            raise ValueError(msg)
        return tuple(options), tuple(unsupported_options)

    def generate_setter_dispatcher():
        setter_dispatcher = {}
        no_args_kwargs = ((), {})
        if read_only:
            args = (storage_name, name_str)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_read_only: (args, kwargs)})
            setattr(property, "is_read_only", read_only)
        if expected_type is not None:
            args = (
                iterable_allowed,
                expected_type,
                name_str,
                optional,
                cast_to_type,
                default,
            )
            setter_dispatcher.update({check_expected_type: (args, {})})
        if str_format:
            args = (str_format, )
            kwargs = {"process": True}
            setter_dispatcher.update({format_str_case: (args, kwargs)})
        if options is not None:
            args = (options, unsupported_options, name_str, name, description)
            setter_dispatcher.update({check_options: (args, {})})
        if min_value is not None:
            args = (name, description, exclusive, min_value)
            setter_dispatcher.update({check_min: (args, {})})
        if max_value is not None:
            args = (name, description, exclusive, max_value)
            setter_dispatcher.update({check_max: (args, {})})
        if less_than is not None:
            args = (less_than, name, description)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_less_than: (args, kwargs)})
        if greater_than is not None:
            args = (greater_than, name, description)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_greater_than: (args, kwargs)})
        if at_least is not None:
            args = (at_least, name, description)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_at_least: (args, kwargs)})
        if at_most is not None:
            args = (at_most, name, description)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_at_most: (args, kwargs)})
        if equal_to is not None:
            args = (equal_to, name, description)
            kwargs = {"instance": True}
            setter_dispatcher.update({check_equal_to: (args, kwargs)})
        if len_sequence is not None:
            args = (len_sequence, name_str)
            setter_dispatcher.update({check_len: (args, {})})
        if optimisable:
            args = (name_str, )
            setter_dispatcher.update({process_optimisable: (args, {})})
            setattr(property, "is_optimisable", optimisable)
        if post_method is not None:
            args = (optional, post_method)
            setter_dispatcher.update({apply_method: (args, {})})
        return setter_dispatcher

    storage_name = "_" + name
    description = kwargs.get("description")
    expected_type = kwargs.get("type")
    options = kwargs.get("options", None)
    unsupported_options = kwargs.get("unsupported_options", [])
    optional = kwargs.get("optional", False)
    default = kwargs.get("default", None)
    iterable_allowed = kwargs.get("iterable_allowed", False)
    cast_to_type = kwargs.get("cast", False)
    len_sequence = kwargs.get("len")
    max_value = kwargs.get("max")
    min_value = kwargs.get("min")
    exclusive = kwargs.get("exclusive", False)
    optimisable = kwargs.get("optimisable", False)
    post_method = kwargs.get("method")
    less_than = kwargs.get("less_than")
    greater_than = kwargs.get("greater_than")
    at_least = kwargs.get("at_least")
    at_most = kwargs.get("at_most")
    equal_to = kwargs.get("equal_to")
    str_format = parse_kwarg("str_format", "string case format",
                             SUPPORTED_STR_FORMAT_OPTIONS, None)
    read_only = kwargs.get("read_only")

    # Additional error checking of kwargs
    name_str = generate_name_description_error_message(name, description)
    if options or unsupported_options:
        options, unsupported_options = error_check_option_kwarg(
            options, unsupported_options)

    setter_dispatcher = generate_setter_dispatcher()

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
        for (method, (args, kwargs)) in setter_dispatcher.items():
            if kwargs.get("instance") is not None:
                kwargs["instance"] = self
            value = method(value, *args, **kwargs)
        setattr(self, storage_name, value)
        setattr(self, f"{storage_name}_dir", {
            "name": name,
            "description": description
        })

    return prop


def check_read_only(value, storage_name, name_str, *, instance):
    if hasattr(instance, storage_name):
        msg = (f"{name_str} is a read-only property and cannot be reset "
               f"after it has been initialised.")
        raise AttributeError(msg)
    return value


def check_expected_type(value, iterable_allowed, expected_type, name_str,
                        optional, cast_to_type, default):
    if iterable_allowed:
        if isinstance(value, Iterable):
            value = tuple([
                check_type(val, expected_type, name_str, optional,
                           cast_to_type, default) for val in value
            ])
        elif (value is None) and optional:
            if default is not None:
                return default
            return None
        else:
            value = check_type(value, expected_type, name_str, optional,
                               cast_to_type, default)
    else:
        value = check_type(value, expected_type, name_str, optional,
                           cast_to_type, default)
    return value


def check_type(value, expected_type, name_str, optional, cast_to_type,
               default):
    """Ensure the type of the property value to be set is as specified.

    Parameters
    ----------
    value : obj
        Property object value for setting.

    Returns
    -------
    Optional[obj]
        The value is returned if is already of the expected type. If the
        value is None and the property has been specified as optional,
        `None` is returned unless there is a default in which case the
        default is returned. Finally the supplied value is attempted to be
        cast to the specified type and if successful this is returned.

    Raises
    ------
    TypeError
        If the type of the value to be set do not match the specified
        required type.
    """
    if isinstance(value, expected_type):
        return value
    elif optional and (value is None):
        if default is not None:
            return default
        return None
    elif cast_to_type:
        return cast_type(value, expected_type, name_str)
    msg = (f"{name_str} must be a {repr(expected_type)}, instead got "
           f"a {repr(type(value))}.")
    raise TypeError(msg)


def cast_type(value, expected_type, name_str):
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
    if expected_type == np.ndarray:
        return np.array(value)
    cast_str = f"processed_value = {expected_type.__name__}({value})"
    try:
        exec(cast_str)
    except (ValueError, TypeError):
        msg = (f"{name_str} must be a {repr(expected_type)}, instead got "
               f"a {repr(type(value))} which cannot be cast.")
        raise ValueError(msg)
    return locals()["processed_value"]


def check_options(value, options, unsupported_options, name_str, name,
                  description):
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
    valid_options = [
        option for option in options if option not in unsupported_options
    ]
    formatted_valid_options = format_for_output(valid_options, with_or=True)
    if value in unsupported_options:
        formatted_unsupported_option = format_for_output(value, with_verb=True)
        formatted_description = generate_name_description_error_message(
            name, description, with_preposition=True)
        msg = (f"{formatted_unsupported_option} not currently supported as "
               f"{formatted_description}. Choose one of: "
               f"{formatted_valid_options}.")
        raise ValueError(msg)
    elif value not in options:
        formatted_value = format_for_output(value, with_verb=True)
        msg = (f"{formatted_value} not a valid option of {name_str}. "
               f"Choose one of: {formatted_valid_options}.")
        raise ValueError(msg)
    return value


def check_min(value, name, description, exclusive, min_value):
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

    Note
    ----
    Use function from py:mod:`utils` to format repr values with backticks.

    """
    name_str = generate_name_description_error_message(name,
                                                       description,
                                                       is_sentence_start=True)
    if exclusive:
        if value <= min_value:
            msg = (f"{name_str} must be greater than `{repr(min_value)}`. "
                   f"`{repr(value)}` is invalid.")
            raise ValueError(msg)
    else:
        if value < min_value:
            msg = (f"{name_str} must be greater than or equal to "
                   f"`{repr(min_value)}`. `{repr(value)}` is invalid.")
            raise ValueError(msg)
    return value


def check_max(value, name, description, exclusive, max_value):
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

    Note
    ----
    Use function from py:mod:`utils` to format repr values with backticks.

    """
    name_str = generate_name_description_error_message(name,
                                                       description,
                                                       is_sentence_start=True)
    if exclusive:
        if value >= max_value:
            msg = (f"{name_str} must be less than `{repr(max_value)}`. "
                   f"`{repr(value)}` is invalid.")
            raise ValueError(msg)
    else:
        if value > max_value:
            msg = (f"{name_str} must be less than or equal to "
                   f"`{repr(max_value)}`. `{repr(value)}` is invalid.")
            raise ValueError(msg)
    return value


def check_less_than(value, less_than, name, description, *, instance):
    def less_than_lambda(val_1, val_2):
        return val_1 < val_2

    check_comparison(value, instance, less_than, "less than", less_than_lambda,
                     name, description)
    return value


def check_greater_than(value, greater_than, name, description, *, instance):
    def greater_than_lambda(val_1, val_2):
        return val_1 > val_2

    check_comparison(
        value,
        instance,
        greater_than,
        "greater than",
        greater_than_lambda,
        name,
        description,
    )
    return value


def check_at_least(value, at_least, name, description, *, instance):
    def at_least_lambda(val_1, val_2):
        return val_1 >= val_2

    check_comparison(value, instance, at_least, "at least", at_least_lambda,
                     name, description)
    return value


def check_at_most(value, at_most, name, description, *, instance):
    def at_most_lambda(val_1, val_2):
        return val_1 <= val_2

    check_comparison(value, instance, at_most, "at most", at_most_lambda, name,
                     description)
    return value


def check_equal_to(value, equal_to, name, description, *, instance):
    def equal_to_lambda(val_1, val_2):
        return val_1 == val_2

    check_comparison(value, instance, equal_to, "equal to", equal_to_lambda,
                     name, description)
    return value


def check_comparison(value, instance, other, comparison_description,
                     comparison_func, name, description):
    try:
        other_value = getattr(instance, ("_" + other))
    except AttributeError:
        pass
    else:
        if not comparison_func(value, other_value):
            other_dir = getattr(instance, f"_{other}_dir")
            other_name = other_dir["name"]
            other_description = other_dir["description"]
            name_str = generate_name_description_error_message(
                name, description, is_sentence_start=True)
            other_name_str = generate_name_description_error_message(
                other_name, other_description)
            value_formatted = format_for_output(value)
            other_value_formatted = format_for_output(other_value)
            msg = (f"{name_str} with value {value_formatted} must be "
                   f"{comparison_description} {other_name_str} with "
                   f"value {other_value_formatted}.")
            raise ValueError(msg)


def check_len(value, len_sequence, name_str):
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
        msg = f"{name_str} must be a sequence of length {len_sequence}."
        raise ValueError(msg)
    return value


def apply_method(value, optional, post_method):
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


def process_optimisable(value, name_str):
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

    Raises
    ------
    ValueError
        If supplied `Iterable` is not of length 2.
    TypeError
        If either supplied bounds are not of type `numbers.Real` or
        the single supplied value is not of type `numbers.Real`.

    """
    if isinstance(value, Real):
        return value
    if isinstance(value, Iterable):
        check_len(value, 2, name_str)
        bounds = []
        msg = (f"Both {name_str} bounds must be of type {Real}, instead "
               f"got {value[0]} at index 0 (type {type(value[0])}) and "
               f"{value[1]} at index 1 (type {type(value[1])}).")
        for bound in value:
            if not isinstance(bound, Real):
                raise TypeError(msg)
            bounds.append(bound)
        bounds = check_bounds(bounds)
        return bounds
    msg = (f"{name_str} must be a {Real} or {Iterable} of length 2, "
           f"instead got {repr(type(value))}.")
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

    Raises
    ------
    ValueError
        If integer is outside 64-bit range or is lower bounds exceeds
        upper bound.

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
