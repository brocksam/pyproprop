import os
import sys

from hypothesis import given
import hypothesis.strategies as st
import pytest

sys.path.append(os.path.abspath("../"))
from pyproprop import processed_property


@given(st.integers())
def test(TestProcessedProperties, integer):
	test_instance = TestProcessedProperties(checked_type_int=integer)