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
                 upper_comparison_kwarg):
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

    return ClassWithComparisonProcessedProperties(lower_bound, upper_bound)


@pytest.fixture
def compare_exclusive_float_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "less_than", "greater_than")
    return fixture


@pytest.fixture
def compare_inclusive_float_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "at_least", "at_most")
    return fixture


@pytest.fixture
def compare_equal_float_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, float,
                           "equal_to", "equal_to")
    return fixture


@pytest.fixture
def compare_exclusive_int_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "less_than", "greater_than")
    return fixture


@pytest.fixture
def compare_inclusive_int_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "at_least", "at_most")
    return fixture


@pytest.fixture
def compare_equal_int_fixture():
    fixture = make_fixture(FIXTURE_LOWER_BOUND, FIXTURE_UPPER_BOUND, int,
                           "equal_to", "equal_to")
    return fixture


@pytest.fixture
def compare_fixture(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize("compare_fixture",
                         ["compare_exclusive_float_fixture",
                          "compare_inclusive_float_fixture",
                          "compare_equal_float_fixture",
                          "compare_exclusive_int_fixture",
                          "compare_inclusive_float_fixture",
                          "compare_equal_int_fixture"],
                         indirect=True)
def test_valid_init_values_do_not_raise_error(compare_fixture):
    assert compare_fixture.some_prop_min == FIXTURE_LOWER_BOUND
    assert compare_fixture.some_prop_max == FIXTURE_UPPER_BOUND


def test_invalid_exclusive_float_comparison_raises_error(
        compare_exclusive_float_fixture):
    """"""
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
    """"""
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
