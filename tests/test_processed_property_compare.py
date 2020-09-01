"""Test comparisons between different processed properties of a class.

Attributes
----------
FIXTURE_LOWER_BOUND : int
    Constant value for minimum value of processed properties in this test
    module.
FIXTURE_UPPER_BOUND : int
    Constant value for maximum value of processed properties in this test
    module.

"""

import pytest

from pyproprop import processed_property


FIXTURE_LOWER_BOUND = 2
FIXTURE_UPPER_BOUND = 10


def make_fixture(lower_bound, upper_bound, prop_type, lower_comparison_kwarg,
                 upper_comparison_kwarg, init_min, init_max):
    """Factory function to manufacture comparison fixtures.

    Parameters
    ----------
    lower_bound : :py:class:`Number <typing>`
        Numerical lower bound on processed property.
    upper_bound : :py:class:`Number <typing>`
        Numerical upper bound on processed property.
    prop_type : :py:class:`type`
        Type to be cast to corresponding to the :py:attr:`type` attribute of a
        :py:func:`processed_property`.
    lower_comparison_kwarg : str
        The :py:func:`processed_property` to which the :py:prop:`some_prop_min`
        :py:func:`processed_property` should be compared.
    upper_comparison_kwarg : str
        The :py:func:`processed_property` to which the :py:prop:`some_prop_max`
        :py:func:`processed_property` should be compared.

    Returns
    -------
    obj
        Class instance containing the required processed properties.

    """
    some_prop_min_keyword = "some_prop_min"
    some_prop_max_keyword = "some_prop_max"
    min_kwargs = {"type": prop_type, "cast": True, "min": lower_bound,
                  "max": upper_bound,
                  lower_comparison_kwarg: some_prop_max_keyword}
    max_kwargs = {"type": prop_type, "cast": True, "min": lower_bound,
                  "max": upper_bound,
                  upper_comparison_kwarg: some_prop_min_keyword}

    class ClassWithComparisonProcessedProperties:
        """A class with processed properties to be used as fixture instances.

        Attributes
        ----------
        some_prop_min : :py:property:`processed_property`
            Numerical processed property with minimum and maximum numerical
            bounds, and comparison to :py:property:`some_prop_max`.
        some_prop_max : :py:property:`processed_property`
            Numerical processed property with minimum and maximum numerical
            bounds, and comparison to :py:property:`some_prop_min`.

        """
        some_prop_min = processed_property(some_prop_min_keyword, **min_kwargs)
        some_prop_max = processed_property(some_prop_max_keyword, **max_kwargs)

        def __init__(self, some_prop_min, some_prop_max):
            """Initialise the numerical bounds on the processed properties.

            Parameters
            ----------
            some_prop_min : :py:class:`Number <typing>`
                Numerical value to initialise the :py:attr:`some_prop_min` to.
            some_prop_max : :py:class:`Number <typing>`
                Numerical value to initialise the :py:attr:`some_prop_max` to.

            """
            self.some_prop_min = some_prop_min
            self.some_prop_max = some_prop_max

    return ClassWithComparisonProcessedProperties(init_min, init_max)


@pytest.fixture
def compare_exclusive_float_fixture():
    """Create fixture with float greater than and less than properties."""
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "less_than", "greater_than", FIXTURE_LOWER_BOUND,
                           FIXTURE_UPPER_BOUND)
    return fixture


@pytest.fixture
def compare_inclusive_float_fixture():
    """Create fixture with float at most and at least properties."""
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "at_most", "at_least", FIXTURE_LOWER_BOUND,
                           FIXTURE_UPPER_BOUND)
    return fixture


@pytest.fixture
def compare_equal_float_fixture():
    """Create fixture with two float equal to properties."""
    average = (FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "equal_to", "equal_to", average, average)
    return fixture


@pytest.fixture
def compare_exclusive_int_fixture():
    """Create fixture with int greater than and less than properties."""
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "less_than", "greater_than", FIXTURE_LOWER_BOUND,
                           FIXTURE_UPPER_BOUND)
    return fixture


@pytest.fixture
def compare_inclusive_int_fixture():
    """Create fixture with int at most and at least properties."""
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "at_most", "at_least", FIXTURE_LOWER_BOUND,
                           FIXTURE_UPPER_BOUND)
    return fixture


@pytest.fixture
def compare_equal_int_fixture():
    """Create fixture with two int equal to properties."""
    average = (FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "equal_to", "equal_to", average, average)
    return fixture


@pytest.fixture
def compare_fixture(request):
    """Utility fixture to support providing multiple fixtures to same test."""
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("compare_fixture",
                         ["compare_exclusive_float_fixture",
                          "compare_inclusive_float_fixture",
                          "compare_exclusive_int_fixture",
                          "compare_inclusive_float_fixture"],
                         indirect=True)
def test_valid_init_values_do_not_raise_error(compare_fixture):
    """Check all fixtures initialise to values correctly."""
    assert compare_fixture.some_prop_min == FIXTURE_LOWER_BOUND
    assert compare_fixture.some_prop_max == FIXTURE_UPPER_BOUND


@pytest.mark.parametrize("compare_fixture",
                         ["compare_equal_float_fixture",
                          "compare_equal_int_fixture"],
                         indirect=True)
def test_valid_init_values_do_not_raise_error(compare_fixture):
    """Check all fixtures initialise to values correctly."""
    average = (FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2
    assert compare_fixture.some_prop_min == 6.0
    assert compare_fixture.some_prop_max == 6


def test_invalid_exclusive_float_comparison_raises_error(
        compare_exclusive_float_fixture):
    """ValueError raised setting greater and less than properties equal."""
    test_fixture = compare_exclusive_float_fixture
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{float(FIXTURE_UPPER_BOUND)}' must be less than "
                          f".*some_prop_max.* with value "
                          f"'{float(FIXTURE_UPPER_BOUND)}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_fixture.some_prop_max
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{float(FIXTURE_LOWER_BOUND)}' must be greater "
                          f"than .*some_prop_min.* with value "
                          f"'{float(FIXTURE_LOWER_BOUND)}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_fixture.some_prop_min


def test_invalid_exclusive_int_comparison_raises_error(
        compare_exclusive_int_fixture):
    """ValueError raised setting greater and less than properties equal."""
    test_fixture = compare_exclusive_int_fixture
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{int(FIXTURE_UPPER_BOUND)}' must be less than "
                          f".*some_prop_max.* with value "
                          f"'{int(FIXTURE_UPPER_BOUND)}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_fixture.some_prop_max
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{int(FIXTURE_LOWER_BOUND)}' must be greater "
                          f"than .*some_prop_min.* with value "
                          f"'{int(FIXTURE_LOWER_BOUND)}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_fixture.some_prop_min


def test_invalid_inclusive_float_comparison_raises_error(
        compare_inclusive_float_fixture):
    """ValueError raised setting at least < at most and visa versa."""
    test_fixture = compare_inclusive_float_fixture
    test_value = float((FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2)
    increment = 0.1
    test_min_value = test_value + increment
    test_max_value = test_value
    test_fixture.some_prop_max = test_max_value
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{test_min_value}' must be at most "
                          f".*some_prop_max.* with value "
                          f"'{test_max_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_min_value
    test_min_value = test_value
    test_max_value = test_value - increment
    test_fixture.some_prop_min = test_min_value
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{test_max_value}' must be at least "
                          f".*some_prop_min.* with value "
                          f"'{test_min_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_max_value


def test_invalid_inclusive_int_comparison_raises_error(
        compare_inclusive_int_fixture):
    """ValueError raised setting at least < at most and visa versa."""
    test_fixture = compare_inclusive_int_fixture
    test_value = int((FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2)
    increment = 1
    test_min_value = test_value + increment
    test_max_value = test_value
    test_fixture.some_prop_max = test_max_value
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{test_min_value}' must be at most "
                          f".*some_prop_max.* with value "
                          f"'{test_max_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_min_value
    test_min_value = test_value
    test_max_value = test_value - increment
    test_fixture.some_prop_min = test_min_value
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{test_max_value}' must be at least "
                          f".*some_prop_min.* with value "
                          f"'{test_min_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_max_value

def test_invalid_equal_float_comparison_raises_error(
        compare_equal_float_fixture):
    """ValueError raised setting properties not equal."""
    test_fixture = compare_equal_float_fixture
    test_value = float((FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2)
    increment = 0.1
    test_min_value = test_value + increment
    test_max_value = test_value
    test_fixture.some_prop_max = test_max_value
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{test_min_value}' must be equal to "
                          f".*some_prop_max.* with value "
                          f"'{test_max_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_min_value
    test_min_value = test_value
    test_max_value = test_value - increment
    test_fixture.some_prop_min = test_min_value
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{test_max_value}' must be equal to "
                          f".*some_prop_min.* with value "
                          f"'{test_min_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_max_value


def test_invalid_equal_int_comparison_raises_error(
        compare_equal_int_fixture):
    """ValueError raised setting properties not equal."""
    test_fixture = compare_equal_int_fixture
    test_value = int((FIXTURE_LOWER_BOUND + FIXTURE_UPPER_BOUND) / 2)
    increment = 1
    test_min_value = test_value + increment
    test_max_value = test_value
    test_fixture.some_prop_max = test_max_value
    expected_error_msg = (f".*some_prop_min.* with value "
                          f"'{test_min_value}' must be equal to "
                          f".*some_prop_max.* with value "
                          f"'{test_max_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_min = test_min_value
    test_min_value = test_value
    test_max_value = test_value - increment
    test_fixture.some_prop_min = test_min_value
    expected_error_msg = (f".*some_prop_max.* with value "
                          f"'{test_max_value}' must be equal to "
                          f".*some_prop_min.* with value "
                          f"'{test_min_value}'.")
    with pytest.raises(ValueError, match=expected_error_msg):
        test_fixture.some_prop_max = test_max_value
