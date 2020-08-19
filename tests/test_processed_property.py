from typing import Iterable

from hypothesis import given, example
from hypothesis.strategies import (booleans, floats, integers, iterables,
                                   lists, one_of, text, tuples)
import numpy as np
import pytest


@given(input_=one_of(booleans(), floats(), integers(), iterables(integers()),
                     lists(integers()), text()))
def test_integer_type_checking(TestProcessedProperties, input_):
    """Tests error messaging is correct when `expected_type=int`."""
    if isinstance(input_, int):
        test_instance = TestProcessedProperties(checked_type_int=input_)
        assert test_instance.checked_type_int == input_
    else:
        with pytest.raises(TypeError):
            test_instance = TestProcessedProperties(checked_type_int=input_)


@given(integer_1=integers(), integer_2=integers(), float_=floats())
def test_type_checking_correct_when_property_updated(TestProcessedProperties,
                                                     integer_1, integer_2, float_):
    """Tests type checking and returning of type checked values when
    property is updated outside of an `__init__` method."""
    test_instance = TestProcessedProperties(checked_type_int=integer_1)
    assert test_instance.checked_type_int == integer_1
    test_instance = TestProcessedProperties(checked_type_int=integer_2)
    assert test_instance.checked_type_int == integer_2
    with pytest.raises(TypeError):
        test_instance = TestProcessedProperties(checked_type_int=float_)


@given(input_=one_of(booleans(), floats(), integers(), iterables(integers()),
                     lists(integers()), text()))
def test_string_type_checking(TestProcessedProperties, input_):
    """Tests error messaging is correct when `expected_type=str`."""
    if isinstance(input_, str):
        test_instance = TestProcessedProperties(checked_type_str=input_)
        assert test_instance.checked_type_str == input_
    else:
        with pytest.raises(TypeError):
            test_instance = TestProcessedProperties(checked_type_str=input_)


@given(input_=one_of(booleans(), floats(allow_nan=False), integers(), iterables(integers()),
                     lists(integers()), text()))
def test_float_type_checking(TestProcessedProperties, input_):
    """Tests error messaging is correct when `expected_type=float`. Fails
    if `checked_type_float` set to `NaN`."""
    if isinstance(input_, float):
        test_instance = TestProcessedProperties(checked_type_float=input_)
        assert test_instance.checked_type_float == input_
    else:
        with pytest.raises(TypeError):
            test_instance = TestProcessedProperties(checked_type_float=input_)


@given(input_=one_of(booleans(), floats(), integers(), iterables(integers()),
                     lists(integers()), text()))
def test_iterable_type_checking(TestProcessedProperties, input_):
    """Tests error messaging is correct when `expected_type=Iterable`."""
    if isinstance(input_, Iterable):
        test_instance = TestProcessedProperties(checked_type_iterable=input_)
        assert test_instance.checked_type_iterable == input_
    else:
        with pytest.raises(TypeError):
            test_instance = TestProcessedProperties(
                checked_type_iterable=input_)


@given(input_=one_of(booleans(), floats(), integers(), iterables(integers()),
                     lists(integers()), text()))
def test_boolean_type_checking(TestProcessedProperties, input_):
    """Tests error messaging is correct when `expected_type=bool`."""
    if isinstance(input_, bool):
        test_instance = TestProcessedProperties(checked_type_bool=input_)
        assert test_instance.checked_type_bool == input_
    else:
        with pytest.raises(TypeError):
            test_instance = TestProcessedProperties(checked_type_bool=input_)


@given(list_=lists(floats()))
def test_length_checking(TestProcessedProperties, list_):
    """Validates length checking error messaging and return statements
    function correctly."""
    required_length = TestProcessedProperties._REQUIRED_LENGTH
    if np.isclose(len(list_), required_length):
        test_instance = TestProcessedProperties(checked_list_len=list_)
        assert test_instance.checked_list_len == list_
    else:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(checked_list_len=list_)


@given(float_=floats())
def test_max_value_checking(TestProcessedProperties, float_):
    """Validates max value error messaging and return statements function
    correctly."""
    max_value = TestProcessedProperties._MAX_VALUE

    if float_ < max_value:
        test_instance = TestProcessedProperties(checked_max_value=float_)
        assert test_instance.checked_max_value == float_
    elif float_ > max_value:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(checked_max_value=float_)


@given(float_=floats())
def test_min_value_checking(TestProcessedProperties, float_):
    """Validates min value error messaging and return statements function
    correctly."""
    min_value = TestProcessedProperties._MIN_VALUE

    if float_ > min_value:
        test_instance = TestProcessedProperties(checked_min_value=float_)
        assert test_instance.checked_min_value == float_
    elif float_ < min_value:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(checked_min_value=float_)


@given(float_=floats())
def test_max_value_excl_checking(TestProcessedProperties, float_):
    """Validates exclusive max value error messaging and return statements
    function correctly."""
    max_value = TestProcessedProperties._MAX_VALUE

    if float_ < max_value:
        test_instance = TestProcessedProperties(checked_max_value_excl=float_)
        assert test_instance.checked_max_value_excl == float_
    elif float_ > max_value:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(
                checked_max_value_excl=float_)


@given(float_=floats())
def test_min_value_excl_checking(TestProcessedProperties, float_):
    """Validates exclusive min value error messaging and return statements
    function correctly."""
    min_value = TestProcessedProperties._MIN_VALUE

    if float_ > min_value:
        test_instance = TestProcessedProperties(checked_min_value_excl=float_)
        assert test_instance.checked_min_value_excl == float_
    elif float_ < min_value:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(
                checked_min_value_excl=float_)


@given(float_=floats(allow_nan=False))
def test_bound_checking(TestProcessedProperties, float_):
    """Validates bound checking error messaging and return statements
    function correctly. `float_` set to `nan` causes this test to fail. """
    lower_bound = TestProcessedProperties._BOUNDS[0]
    upper_bound = TestProcessedProperties._BOUNDS[1]

    if float_ >= lower_bound and float_ <= upper_bound:
        test_instance = TestProcessedProperties(checked_bounds=float_)
        assert test_instance.checked_bounds == float_
    else:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(checked_bounds=float_)


@given(integer=integers(), iterable=iterables(integers()))
def test_iterable_allowed_checking(TestProcessedProperties, integer, iterable):
    """Tests functionality associated with the `iterable_allowed` flag."""
    test_instance = TestProcessedProperties(checked_iterable_allowed=integer)
    assert test_instance.checked_iterable_allowed == integer
    test_instance = TestProcessedProperties(checked_iterable_allowed=iterable)
    assert test_instance.checked_iterable_allowed == iterable


@given(integer=integers())
def test_optional_return(TestProcessedProperties, integer):
    """Tests a property flagged as optional defaults to `None`."""
    test_instance = TestProcessedProperties(optional_prop=integer)
    assert test_instance.optional_prop == integer
    test_instance = TestProcessedProperties()
    assert test_instance.optional_prop is None


def test_optional_default_object_return(TestProcessedProperties):
    """Tests a property flagged as optional, with a default, defaults to
    correct value."""
    default = TestProcessedProperties._DEFAULT_INT
    test_instance = TestProcessedProperties()
    assert test_instance.optional_prop_with_default == default


@given(integer=integers(), float_=floats(allow_infinity=False,
                                         allow_nan=False))
def test_cast_to_string(TestProcessedProperties, integer, float_):
    """Tests cast input to string use case functions properly. Test fails
    when attempting to cast floats equal to `inf` or `nan`."""
    test_instance = TestProcessedProperties(cast_string=integer)
    assert test_instance.cast_string == str(integer)
    assert isinstance(test_instance.cast_string, str) is True
    test_instance = TestProcessedProperties(cast_string=float_)
    assert test_instance.cast_string == str(float_)
    assert isinstance(test_instance.cast_string, str) is True


@given(value=one_of(integers(), floats(allow_nan=False)),
       bounds=tuples(floats(allow_nan=False, min_value=-9.223372036854776e+18,
                            max_value=9.223372036854776e+18),
                     floats(allow_nan=False, min_value=-9.223372036854776e+18,
                            max_value=9.223372036854776e+18)))
@example(value=0, bounds=(-204797952.00000006, -204800000.00000006))
def test_optimisable_arg_passing(TestProcessedProperties, value, bounds):
    test_instance = TestProcessedProperties(optimisable_property=value)
    assert test_instance.optimisable_property == value
    if np.isclose(bounds[0], bounds[1]):
        test_instance = TestProcessedProperties(optimisable_property=bounds)
        assert test_instance.optimisable_property == bounds[0]
    elif bounds[0] < bounds[1]:
        test_instance = TestProcessedProperties(optimisable_property=bounds)
        assert test_instance.optimisable_property == bounds
    elif bounds[0] > bounds[1]:
        with pytest.raises(ValueError):
            test_instance = TestProcessedProperties(optimisable_property=bounds)


@given(float_bounds=tuples(floats(allow_nan=False,
                                  min_value=9.223372036854776e+18),
                           floats(allow_nan=False,
                                  max_value=-9.223372036854776e+18)),
       integer_bounds=tuples(integers(min_value=9223372036854775807),
                             integers(max_value=-9223372036854775808)))
def test_optimisable_error_messaging_for_non_64_bit_bounds(
        TestProcessedProperties, float_bounds, integer_bounds):
    """Test error handling when optimisable bounds cannot represented as
    signed 64-bit number."""
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=float_bounds)
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=integer_bounds)


@given(short_string=text(max_size=1),
       two_char_string=text(min_size=2, max_size=2),
       long_string=text(min_size=3),
       short_list=lists(integers(), min_size=0, max_size=1),
       long_list=lists(integers(), min_size=3),
       invalid_bounds=tuples(integers(), text()))
def test_optimisable_error_handling(TestProcessedProperties, short_string,
                                    two_char_string, long_string,
                                    short_list, long_list, invalid_bounds):
    """Tests error handling for properties flagged as `optimisable`."""
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=short_string)
    with pytest.raises(TypeError):
        test_instance = TestProcessedProperties(optimisable_property=two_char_string)
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=long_string)
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=short_list)
    with pytest.raises(ValueError):
        test_instance = TestProcessedProperties(optimisable_property=long_list)
    with pytest.raises(TypeError):
        test_instance = TestProcessedProperties(optimisable_property=invalid_bounds)
