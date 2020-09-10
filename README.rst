*********
pyproprop
*********

Package for aiding writing classes with lots of similar simple properties without the boilerplate.

Status
======

.. list-table::
   :widths: 50 50 50 50

   * - **Latest Release**
     - .. image:: https://img.shields.io/pypi/v/pyproprop?color=brightgreen&label=version
            :alt: PyPI
            :target: https://pypi.org/project/pyproprop/
     - **Travis CI**
     - .. image:: https://travis-ci.com/brocksam/pyproprop.svg?branch=master
            :target: https://travis-ci.com/brocksam/pyproprop
   * - **Docs**
     - .. image:: https://readthedocs.org/projects/pyproprop/badge/?version=latest
            :target: https://pyproprop.readthedocs.io/en/latest/?badge=latest
            :alt: Documentation Status
     - **Appveyor**
     - .. image:: https://ci.appveyor.com/api/projects/status/github/brocksam/pyproprop?svg=true
            :target: https://ci.appveyor.com/project/brocksam/pyproprop
   * - **PyPI**
     - .. image:: https://img.shields.io/pypi/dm/pyproprop?color=brightgreen&label=downloads&logo=pypi
            :alt: PyPI - Downloads
            :target: https://pypi.org/project/pyproprop/
     - **Coverage**
     - .. image:: https://img.shields.io/codecov/c/github/brocksam/pyproprop?color=brightgreen&logo=codecov
            :alt: Codecov
   * - **Anaconda**
     - .. image:: https://img.shields.io/conda/dn/conda-forge/pyproprop?color=brightgreen&label=downloads&logo=conda-forge
            :alt: Conda
            :target: https://anaconda.org/conda-forge/pyproprop
     - **License**
     - .. image:: https://img.shields.io/badge/license-MIT-brightgreen.svg
           :target: https://github.com/brocksam/pyproprop/blob/master/LICENSE



What is pyproprop?
==================

Do you often find yourself writing classes with properties such as:

.. code-block:: python

    from some_other_module import DefaultObject, some_type
    
    class ExampleClass:
    
        def __init__(self, 
                     type_checked_value,
                     bounded_numeric_value,
                     specific_length_sequence_value,
                     obj_with_method_applied_value,
                     ):
            self.type_check_attr = type_checked_value
            self.bounded_numeric_attr = bounded_numeric_value
            self.specific_length_sequence_attr = specific_length_sequence_value
            self.obj_with_method_applied_attr = obj_with_method_applied_value
            self.instantiate_default_if_none_attr = None
    
        @property
        def type_checked_attr(self):
            return self._type_checked_attr
    
        @type_checked_attr.setter
        def type_checked_attr(self, val):
            if not isinstance(val, some_type):
                msg = "`type_checked_attr` must be of `some_type`"
                raise TypeError(msg)
            self._type_checked_attr = val
    
        @property
        def bounded_numeric_attr(self):
            return self._bounded_numeric_attr
    
        @bounded_numeric_attr.setter
        def bounded_numeric_attr(self, val):
            val = float(val)
            lower_bound = -1.0
            upper_bound = 2.5
            if val < lower_bound:
                msg = f"`bounded_numeric_attr` must be greater than {lower_bound}"
                raise ValueError(msg)
            if val >= upper_bound:
                msg = (f"`bounded_numeric_attr` must be less than or equal to "
                       f"{upper_bound}.")
                raise ValueError(msg)
            self._type_checked_attr = val
    
        @property
        def specific_length_sequence_attr(self):
            return self._specific_length_sequence_attr
    
        @specific_length_sequence_attr.setter
        def specific_length_sequence_attr(self, val):
            if len(val) != 2:
                msg = "`specific_length_sequence` must be an iterable of length 2."
                raise ValueError(msg)
            self._specific_length_sequence_attr = val
    
        @property
        def obj_with_method_applied_value(self):
            return self._obj_with_method_applied_value
    
        @obj_with_method_applied_value.setter
        def obj_with_method_applied_value(self, val):
            val = str(val)
            self._obj_with_method_applied_value = val.title()
    
        @property
        def instantiate_default_if_none_attr(self):
            return self._instantiate_default_if_none_attr
    
        @instantiate_default_if_none_attr.setter
        def instantiate_default_if_none_attr(self, val):
            if val is None:
                val = DefaultObject()
            self._instantiate_default_if_none_attr = val

With pyproprop all of this boilerplate can be removed and instead the exact same class can be rewritten as:

.. code-block:: python

    from pyproprop import processed_property
    from some_other_module import DefaultObject, some_type
    
    class ExampleClass:
    
        type_checked_attr = processed_property(
            "type_checked_attr",
            description="property with enforced type of `some_type`",
            type=some_type,
        )
        bounded_numeric_attr = processed_property(
            "bounded_numeric_attr",
            description="numerical attribute with upper and lower bounds"
            type=float,
            cast=True,
            min=-1.0,
            max=2.5,
        )
        specific_length_sequence_attr = processed_property(
            "specific_length_sequence_attr",
            description="sequence of length exactly 2",
            len=2,
        )
        obj_with_method_applied_attr = processed_property(
            "obj_with_method_applied_attr",
            description="sting formatted to use title case"
            type=str,
            cast=True,
            method="title",
        )
        instantiate_default_if_none_attr = processed_property(
            "instantiate_default_if_none_attr",
            default=DefaultObject,
        )
    
        def __init__(self, 
                     type_checked_value,
                     bounded_numeric_value,
                     specific_length_sequence_value,
                     obj_with_method_applied_value,
                     ):
            self.type_check_attr = type_checked_value
            self.bounded_numeric_attr = bounded_numeric_value
            self.specific_length_sequence_attr = specific_length_sequence_value
            self.obj_with_method_applied_attr = obj_with_method_applied_value
            self.instantiate_default_if_none_attr = None

Installation
============

The easiest way to install pyproprop is using the `Anaconda Python distribution <https://www.anaconda.com/what-is-anaconda/>`_ and its included *Conda* package management system. To install pyproprop and its required dependencies, enter the following command at a command prompt:

.. code-block:: bash

    conda install pyproprop

To install using pip, enter the following command at a command prompt:

.. code-block:: bash

    pip install pyproprop

For more information, refer to the `installation documentation <https://pyproprop.readthedocs.io/en/latest/user/installation.html>`_.

Contribute
==========

- Issue Tracker: https://github.com/brocksam/pyproprop/issues
- Source Code: https://github.com/brocksam/pyproprop

License
=======

This project is licensed under the terms of the MIT license.
