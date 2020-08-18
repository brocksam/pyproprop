pyproprop
=========

Do you often find yourself writing classes with properties such as

.. example-code::

  .. code-block:: python

    @property
    def type_checked_attr(self):
        return self._type_checked_attr

    @type_checked_attr.setter
    def type_checked_attr(self, val):
        if not isinstance(val, some_type):
            msg = "`type_checked_attr` must be of `some_type`"
            raise TypeError(msg)
        self._type_checked_attr = val

  .. code-block:: python

    @property
    def bounded_numeric_attr(self):
        return self._bounded_numeric_attr

    @bounded_numeric_attr.setter
    def bounded_numeric_attr(self, val):
        val = float(val)
        if val < lower_bound := -1:
            msg = f"`bounded_numeric_attr` must be greater than {lower_bound}"
            raise ValueError(msg)
        self._type_checked_attr = val

LICENSE
-------

This project is licensed under the terms of the MIT license.