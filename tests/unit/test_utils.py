"""Tests for utility functions."""

import re

import pytest

from pyproprop import processed_property


class ClassWithProcessedProperties:

    prop_a = processed_property("prop_a", type=str, options=("A", "B"))
    prop_b = processed_property("prop_b", type=str, options=("A", "B"),
                                unsupported_options=("B", ))
    prop_c = processed_property("prop_c", description="description", type=str,
                                options=("A", "B"),
                                unsupported_options=("B", ))
    prop_d = processed_property("prop_d", description="a", type=int, min=0,
                                max=1)
    prop_e = processed_property("prop_e", description="a description",
                                type=int, min=0, max=1)

    def __init__(self):
        self.prop_a = "A"
        self.prop_b = "A"
        self.prop_c = "A"
        self.prop_d = 1
        self.prop_e = 1


@pytest.fixture
def test_fixture():
    return ClassWithProcessedProperties()


def test_generate_name_description_error_message_options_prop(test_fixture):
    expected_error_msg = re.escape(
        "`'C'` is not a valid option of `prop_a`. Choose one of: `'A'` or "
        "`'B'`")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.prop_a = "C"

    expected_error_msg = re.escape(
        "`'B'` is not currently supported as a `prop_b`. Choose one of: "
        "`'A'`.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.prop_b = "B"

    expected_error_msg = re.escape(
        "`'B'` is not currently supported as a description (`prop_c`). Choose "
        "one of: `'A'`.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.prop_c = "B"


def test_generate_name_description_error_message_min_max_prop(test_fixture):
    expected_error_msg = re.escape(
        "A (`prop_d`) must be less than or equal to `1`. `2` is "
        "invalid.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.prop_d = 2

    expected_error_msg = re.escape(
        "A description (`prop_e`) must be less than or equal to `1`. `2` is "
        "invalid.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.prop_e = 2
