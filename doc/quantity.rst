********
Quantity
********

.. automodule:: quantity

Classes
=======

.. autoclass:: Quantity
    :members: amount, unit, refUnit, definition, normalizedDefinition,
        convert, quantize, allocate, __hash__,
        __eq__, __lt__, __le__, __gt__, __ge__,
        __abs__, __neg__, __pos__,
        __add__, __radd__, __sub__, __rsub__,
        __mul__, __rmul__, __div__, __rdiv__,
        __truediv__, __rtruediv__, __pow__, __round__,
        __repr__, __str__, __format__

.. autoclass:: Unit
    :members: symbol, name, refUnit, definition, normalizedDefinition,
        registeredUnits,
        registerConverter, removeConverter, registeredConverters,
        isBaseUnit, isDerivedUnit, isRefUnit,
        __eq__, __lt__, __le__, __gt__, __ge__,
        __call__

.. autoclass:: Converter

.. autoclass:: TableConverter
    :members:

Functions
=========

.. autofunction:: getUnitBySymbol
.. autofunction:: generateUnits
.. autofunction:: sum

Exceptions
==========

.. autoclass:: QuantityError

.. autoclass:: IncompatibleUnitsError

.. autoclass:: UndefinedResultError


Submodules
==========

quantity.predefined
-------------------

.. automodule:: quantity.predefined
