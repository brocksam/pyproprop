"""Utilities for type checking user input and generating error messages.

Processed properties are a way of defining property attributes for a class that
require input sanitation, type checking, function application, error message
generation etc. from user-supplied values in a manner that minimises code
reuse.

"""

from numbers import Real
from typing import Any, Iterable, Tuple

import numpy as np

from .utils import (format_for_output, format_str_case,
                    generate_name_description_error_message,
                    SUPPORTED_STR_FORMAT_OPTIONS)


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

    def parse_kwarg(kwarg_name, description, valids, default):
        kwarg = kwargs.get(kwarg_name, default)
        if isinstance(valids, type) and not isinstance(kwarg, valids):
            msg = (f"{repr(kwarg)} is not a valid {description}. Please "
                   f"use a value of type {repr(valids)}.")
            raise TypeError(msg)
        elif not isinstance(valids, type) and kwarg not in valids:
            formatted_valids = format_for_output(valids, with_or=True)
            msg = (f"{repr(kwarg)} is not a valid {description}. Please "
                   "choose one of: {formatted_valids}.")
            raise ValueError(msg)
        return kwarg

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
    less_than = kwargs.get("less_than")
    greater_than = kwargs.get("greater_than")
    at_least = kwargs.get("at_least")
    at_most = kwargs.get("at_most")
    equal_to = kwargs.get("equal_to")
    str_format = parse_kwarg("str_format", "string case format",
                             SUPPORTED_STR_FORMAT_OPTIONS, None)

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
        if less_than is not None:
            check_less_than(self, value)
        if greater_than is not None:
            check_greater_than(self, value)
        if at_least is not None:
            check_at_least(self, value)
        if at_most is not None:
            check_at_most(self, value)
        if equal_to is not None:
            check_equal_to(self, value)
        if len_sequence is not None:
            check_len(value, len_sequence)
        if optimisable:
            value = process_optimisable(value)
        if str_format:
            value = format_str_case(value, str_format)
        if post_method is not None:
            value = apply_method(value)
        setattr(self, storage_name, value)
        setattr(self, f"{storage_name}_dir", {"name": name,
                                              "description": description})

    def check_type(value):
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
        elif optional and value is None:
            if default:
                return default
            else:
                return None
        elif cast_to_type:
            return cast_type(value)
        else:
            name_str = generate_name_description_error_message(name,
                                                               description)
            msg = (f"{name_str} must be a {repr(expected_type)}, instead got "
                   f"a {repr(type(value))}.")
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
            name_str = generate_name_description_error_message(name,
                                                               description)
            msg = (f"{name_str} must be a {repr(expected_type)}, instead got "
                   f"a {repr(type(value))} which cannot be cast.")
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
            formatted_description = generate_name_description_error_message(
                name,
                description,
                with_preposition=True)
            msg = (
                f"{formatted_unsupported_option} not currently supported as "
                f"{formatted_description}. Choose one of: "
                f"{formatted_valid_options}."
            )
            raise ValueError(msg)
        elif value not in options:
            formatted_value = format_for_output(value, with_verb=True)
            name_str = generate_name_description_error_message(name,
                                                               description)
            msg = (
                f"{formatted_value} not a valid option of {name_str}. "
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
        name_str = generate_name_description_error_message(
            name,
            description,
            is_sentence_start=True)
        if exclusive:
            if value <= min_value:
                msg = (f"{name_str} must be greater than {min_value}. {value} "
                       f"is invalid.")
                raise ValueError(msg)
        else:
            if value < min_value:
                msg = (f"{name_str} must be greater than or equal to "
                       f"{min_value}. {value} is invalid.")
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
        name_str = generate_name_description_error_message(
            name,
            description,
            is_sentence_start=True)
        if exclusive:
            if value >= max_value:
                msg = (f"{name_str} must be less than {max_value}. {value} is "
                       f"invalid.")
                raise ValueError(msg)
        else:
            if value > max_value:
                msg = (f"{name_str} must be less than or equal to "
                       f"{max_value}. {value} is invalid.")
                raise ValueError(msg)

    def check_less_than(self, value):
        def less_than_lambda(val_1, val_2):
            return val_1 < val_2
        check_comparison(self, value, less_than, "less than",
                         less_than_lambda)

    def check_greater_than(self, value):
        def greater_than_lambda(val_1, val_2):
            return val_1 > val_2
        check_comparison(self, value, greater_than, "greater than",
                         greater_than_lambda)

    def check_at_least(self, value):
        def at_least_lambda(val_1, val_2):
            return val_1 >= val_2
        check_comparison(self, value, at_least, "at least",
                         at_least_lambda)

    def check_at_most(self, value):
        def at_most_lambda(val_1, val_2):
            return val_1 <= val_2
        check_comparison(self, value, at_most, "at most",
                         at_most_lambda)

    def check_equal_to(self, value):
        def equal_to_lambda(val_1, val_2):
            return val_1 == val_2
        check_comparison(self, value, equal_to, "equal to",
                         equal_to_lambda)

    def check_comparison(self, value, other, comparison_description,
                         comparison_func):
        try:
            other_value = getattr(self, other)
        except AttributeError:
            pass
        else:
            if not comparison_func(value, other_value):
                other_dir = getattr(self, f"_{other}_dir")
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
            name_str = generate_name_description_error_message(name,
                                                               description)
            msg = (f"{name_str} must be a sequence of length {len_sequence}.")
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

        Raises
        ------
        ValueError
            If supplied `Iterable` is not of length 2.
        TypeError
            If either supplied bounds are not of type `numbers.Real` or
            the single supplied value is not of type `numbers.Real`.

        """
        name_str = generate_name_description_error_message(name, description)
        if isinstance(value, Real):
            return value
        if isinstance(value, Iterable):
            check_len(value, 2)
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

    return prop
