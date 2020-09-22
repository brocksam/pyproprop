"""Test read-only processed properties."""
import re

import pytest

from pyproprop import processed_property


class ClassWithReadOnlyProperty:
    """Dummy class with read-only processed property for tests.

    Attributes
    ----------
    read_only_prop : :py:property:
        Read-only property that raises an AttributeError if tried to reset.

    Raises
    ------
    AttributeError
        If :py:attr:`read_only_prop` is tried to be set more than once.

    """

    read_only_prop = processed_property("read_only_prop", read_only=True)


@pytest.fixture
def test_fixture():
    """Fixture for easy instantiation of class with read-only property."""
    return ClassWithReadOnlyProperty()


def test_instantiation():
    """Read-only properties can be instantiated successfully."""
    _ = ClassWithReadOnlyProperty()


def test_setting_attribute_once(test_fixture):
    """Read-only property can be set once."""
    test_fixture.read_only_prop = 1


def test_raises_attribute_error_on_setting_twice(test_fixture):
    """Throws AttributeError if tried to set twice."""
    test_fixture.read_only_prop = 1
    expected_error_msg = re.escape(
        "`read_only_prop` is a read-only property and cannot be reset after "
        "it has been initialised.")
    with pytest.raises(AttributeError, match=expected_error_msg):
        test_fixture.read_only_prop = 2
