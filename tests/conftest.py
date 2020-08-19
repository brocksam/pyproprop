import os
from typing import Iterable
import sys

import pytest

from pyproprop import processed_property


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
		checked_type_int = processed_property("checked_type_int", type=int,
			optional=True)
		checked_type_float = processed_property("checked_type_float", type=float,
			optional=True)
		checked_type_str = processed_property("checked_type_str", type=str,
			optional=True)
		checked_type_iterable = processed_property("checked_type_iterable",
			type=Iterable, optional=True)
		checked_type_bool = processed_property("checked_type_bool", type=bool,
			optional=True)

		checked_list_len = processed_property("checked_list_len",
			len=_REQUIRED_LENGTH, optional=True)
		checked_max_value = processed_property("checked_max_value",
			max=_MAX_VALUE, optional=True)
		checked_min_value = processed_property("checked_min_value",
			min=_MIN_VALUE, optional=True)
		checked_max_value_excl = processed_property("checked_max_value_excl",
			max=_MAX_VALUE, exclusive=True, optional=True)
		checked_min_value_excl = processed_property("checked_min_value_excl",
			min=_MIN_VALUE, exclusive=True, optional=True)
		checked_bounds = processed_property("checked_bounds", min=_BOUNDS[0],
			max=_BOUNDS[1], optional=True)
		checked_iterable_allowed = processed_property("checked_iterable_allowed",
			iterable_allowed=True, optional=True)
		optional_prop = processed_property("optional_prop", type=int, optional=True)
		optional_prop_with_default = processed_property("optional_prop_with_default",
			type=int, default=_DEFAULT_INT, optional=True)
		cast_string = processed_property("cast_string",
			type=str, cast=True)
		optimisable_property = processed_property("optimisable_property",
			optimisable=True)

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
