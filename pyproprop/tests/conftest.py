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

		# TODO: expand to cover all use cases:
		#  * Find suitable post method for use in test.
		#  * Test description
		checked_type_int = processed_property("check_type_int", type=int,
			optional=True)
		checked_type_float = processed_property("check_type_int", type=float,
			optional=True)
		checked_type_str = processed_property("check_type_str", type=str,
			optional=True)
		checked_type_iterable = processed_property("checked_type_iterable",
			type=Iterable, optional=True)
		checked_type_bool = processed_property("bool", type=bool,
			optional=True)

		checked_len = processed_property("checked_len", len=3, optional=True)
		checked_max_value = processed_property("checked_max_value",
			max_value=4, optional=True)
		checked_min_value = processed_property("checked_min_value",
			min_value=4, optional=True)
		checked_max_value_excl = processed_property("checked_max_value_excl",
			max_value=4, exclusive=True, optional=True)
		checked_min_value_excl = processed_property("checked_min_value_excl",
			min_value=4, exclusive=True, optional=True)
		checked_iterable_allowed = processed_property("checked_iterable_allowed",
			iterable_allowed=True, optional=True)
		optional = processed_property("optional", type=int, optional=True)
		optional_with_default = processed_property("optional_with_default",
			type=int, default=5, optional=True)
		string_cast_from_int = processed_property("string_cast_from_int",
			type=str, cast=True)


		def __init__(self, *,
			checked_type_int=None,
			checked_type_float=None,
			checked_type_str=None,
			checked_type_iterable=None,
			checked_type_bool=None,
			checked_len=None,
			checked_max_value=None,
			checked_min_value=None,
			checked_max_value_excl=None,
			checked_min_value_excl=None,
			checked_iterable_allowed=None,
			optional=None,
			optional_with_default=None,
			string_cast_from_int=None
		):

			self.checked_type_int = checked_type_int
			self.checked_type_float = checked_type_float
			self.checked_type_str = checked_type_str
			self.checked_type_iterable = checked_type_iterable
			self.checked_type_bool = checked_type_bool

			# TODO: all length checking for optionals.
			# self.checked_len = checked_len
			self.checked_max_value = checked_max_value
			self.checked_min_value = checked_min_value
			self.checked_max_value_excl = checked_max_value_excl
			self.checked_min_value_excl = checked_min_value_excl
			self.checked_iterable_allowed = checked_iterable_allowed
			self.optional = optional
			self.optional_with_default = optional_with_default
			self.string_cast_from_int = string_cast_from_int

	return TestProcessedProperties