"""Utilities for creating attributes that support named dot-indexing.

Named iterables are a way of defining instance attributes for a class that
are able to support dot-indexing via user-specified names.

"""

from collections import namedtuple

import sympy as sym
from typing import (Any, Iterable, Union)


__all__ = ["named_iterable"]


def named_iterable(iterable, use_named=True, named_keys=None, sympify=False):
    """Formats user supplied arguments as a named tuple.

    Parameters
    ----------
    iterable : TYPE
        Description
    use_named : bool, optional
        Description
    named_keys : Optional[NamedTuple], optional
        Description
    sympify : bool, optional
        Whether the values should be automatically converted to Sympy objects
        before adding to the new iterable.

    Returns
    -------
    TYPE
        Description
    """
    iterable, named_keys = make_iterable(iterable, named_keys)
    if sympify:
        entries = [sym.sympify(entry) for entry in iterable]
    else:
        entries = list(iterable)
    if use_named:
        if named_keys is None:
            named_keys = [str(entry) for entry in entries]
        NamedTuple = namedtuple('NamedTuple', named_keys)
        formatted_entries = NamedTuple(*entries)
    else:
        formatted_entries = tuple(entries)

    return formatted_entries



def make_iterable(iterable, named_keys):
    """
    Parameters
    ----------
    iterable : Union[Any, Iterable[Any]]
        Description
    named_keys : TYPE
        Description
    
    Returns
    -------
    TYPE
        Description
    
    
    
    """
    if not iterable:
        return ()
    try:
        iter(iterable)
    except TypeError:
        return (iterable, ), named_keys
    try:
        return iterable.values(), iterable.keys()
    except:
        return iterable, named_keys
