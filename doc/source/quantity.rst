********
Quantity
********

.. automodule:: quantity

Types
=====

.. autodata:: QuantityClsDefT

.. autodata:: UnitDefT

.. autodata:: AmountUnitTupleT

.. autodata:: BinOpResT

.. autodata:: ConverterT

.. autodata:: ConvMapT

.. autodata:: ConvSpecIterableT


Classes
=======

.. autoclass:: Unit
    :members:
    :special-members:
    :exclude-members: __new__, is_base_elem, norm_sort_key

.. autoclass:: QuantityMeta(name, define_as, ref_unit_symbol, ref_unit_name, quantum)
    :inherited-members: type
    :members:
    :special-members: __mul__, __rmul__, __truediv__, __rtuediv__
    :exclude-members: is_base_elem, norm_sort_key

.. autoclass:: Quantity
    :members:
    :special-members:
    :exclude-members: __new__

.. _converter_classes_label:

.. autoclass:: Converter
    :special-members: __call__

.. autoclass:: TableConverter
    :show-inheritance:

.. _functions_label:

Functions
=========

.. autofunction:: sum

.. _exceptions_label:

Exceptions
==========

.. autoexception:: QuantityError

.. autoexception:: IncompatibleUnitsError

.. autoexception:: UndefinedResultError

.. autoexception:: UnitConversionError
