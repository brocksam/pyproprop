import os
import sys

from hypothesis import given
from hypothesis.strategies import (booleans, floats, integers, iterables, text)
import pytest

from pyproprop import processed_property


@given(integer=integers(), float_=floats(), iterable=iterables(integers()))
def test_integer_type_checking(TestProcessedProperties, integer, float_,
		iterable):
	"""Tests error messaging is correct when `expected_type=int`."""
	test_instance = TestProcessedProperties(checked_type_int=integer)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_int=float_)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_int=iterable)


@given(integer=integers(), float_=floats(), iterable=iterables(integers()))
def test_float_type_checking(TestProcessedProperties, integer, float_,
		iterable):
	"""Tests error messaging is correct when `expected_type=float`."""
	test_instance = TestProcessedProperties(checked_type_float=float_)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_float=integer)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_float=iterable)


@given(integer=integers(), float_=floats(), text=text())
def test_string_type_checking(TestProcessedProperties, integer, float_, text):
	"""Tests error messaging is correct when `expected_type=str`."""
	test_instance = TestProcessedProperties(checked_type_str=text)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_str=integer)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_str=float_)


@given(integer=integers(), float_=floats(), iterable=iterables(integers()))
def test_iterable_type_checking(TestProcessedProperties, integer, float_,
		iterable):
	"""Tests error messaging is correct when `expected_type=Iterable`."""
	test_instance = TestProcessedProperties(checked_type_iterable=iterable)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_iterable=integer)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_iterable=float_)


@given(boolean=booleans(), float_=floats(), iterable=iterables(integers()))
def test_boolean_type_checking(TestProcessedProperties, boolean, float_,
		iterable):
	"""Tests error messaging is correct when `expected_type=bool`."""
	test_instance = TestProcessedProperties(checked_type_bool=boolean)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_bool=float_)
	with pytest.raises(TypeError):
		test_instance = TestProcessedProperties(checked_type_bool=iterable)
