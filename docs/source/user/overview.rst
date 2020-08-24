Overview
========

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