import keyword
import string

from hypothesis import assume, given
import hypothesis.strategies as st
import pytest

from pyproprop import named_iterable


@pytest.mark.usefixtures("_named_iterable_fixture")
class TestNamedIterable:

    @pytest.fixture(autouse=True)
    def _named_iterable_fixture(self):
        """Simple fixture setting up an named iterables."""
        self.single_named_iter = named_iterable(1, named_keys=["x"])
        self.double_named_iter = named_iterable([1, 2], named_keys=["x", "y"])

    def test_dot_indexing(self):
        """Check that value- and dot-indexing are equivalent."""
        assert self.single_named_iter.x == self.single_named_iter[0]
        assert self.double_named_iter.x == self.double_named_iter[0]
        assert self.double_named_iter.y == self.double_named_iter[1]


@given(keys=st.iterables(st.text(alphabet=string.ascii_letters, min_size=1),
                         min_size=1,
                         unique=True),
       values=st.iterables(st.one_of(st.floats(),
                                     st.integers(),
                                     st.booleans()),
                           min_size=1))
def test_named_iterable_creation_as_mapping(keys, values):
    keys = list(keys)
    values = list(values)
    assume(not any(keyword.iskeyword(str(key)) for key in keys))
    _ = named_iterable(dict(zip(keys, values)))


@given(iterable=st.iterables(st.text(alphabet=string.ascii_letters,
                                     min_size=1),
                             min_size=1,
                             unique=True))
def test_named_iterable_creation_data_object(iterable):
    assume(not any(keyword.iskeyword(str(key)) for key in iterable))
    _ = named_iterable(iterable)


@given(iterable=st.iterables(st.one_of(st.just(kwarg)
                                       for kwarg in keyword.kwlist),
                             min_size=1,
                             unique=True))
def test_named_iterable_creation_keyword_raises_error(iterable):
    expected_error_msg = ("Type names and field names cannot be a "
                          "keyword: '.*'")
    with pytest.raises(ValueError, match=expected_error_msg):
        _ = named_iterable(iterable)


@given(keys=st.iterables(st.text(alphabet=(string.digits
                                           + string.punctuation
                                           + string.whitespace),
                                 min_size=1),
                         min_size=1),
       values=st.iterables(st.one_of(st.floats(),
                                     st.integers(),
                                     st.booleans()),
                           min_size=1))
def test_invalid_identifiers(keys, values):
    """Invalid identifiers raise ValueError."""
    with pytest.raises(ValueError):
        _ = named_iterable(dict(zip(keys, values)))
