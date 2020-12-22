# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        quantity (package)
# Purpose:     Unit-safe computations with quantities.
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


# TODO: update doc
"""Unit-safe computations with quantities.

Usage
=====

.. _defining_a_qty_label:

Defining a quantity class
-------------------------

A **basic** type of quantity is declared just by sub-classing
:class:`Quantity`:

    >>> class Length(Quantity):
    ...     pass
    ...

In addition to the new quantity class the meta-class of :class:`Quantity`
creates a corresponding class for the units automatically. It can be
referenced via the quantity class:

    >>> Length.Unit
    <class 'quantity.quantity.LengthUnit'>

But, as long as there is no unit defined for that class, you can not create
any instance for the new quantity class:

    >>> l = Length(1)
    ValueError: A unit must be given.

If there is a reference unit, the simplest way to define it is giving a name
and a symbol for it as class variables. The meta-class of :class:`Quantity`
will then create a unit automatically:

    >>> class Length(Quantity):
    ...     refUnitName = 'Metre'
    ...     refUnitSymbol = 'm'
    ...
    >>> Length.refUnit
    Length.Unit('m')

Now, this unit can be given to create a quantity:

    >>> METRE = Length.refUnit
    >>> print(Length(15, METRE))
    15 m

If no unit is given, the reference unit is used:

    >>> print(Length(15))
    15 m

Other units can be derived from the reference unit (or another unit), giving
a definition by multiplying a scaling factor with that unit:

    >>> MILLIMETRE = Length.Unit('mm', 'Millimetre', Decimal('0.001') * METRE)
    >>> MILLIMETRE
    Length.Unit('mm')
    >>> KILOMETRE = Length.Unit('km', 'Kilometre', 1000 * METRE)
    >>> KILOMETRE
    Length.Unit('km')
    >>> CENTIMETRE = Length.Unit('cm', 'Centimetre', 10 * MILLIMETRE)
    >>> CENTIMETRE
    Length.Unit('cm')

Using one unit as a reference and defining all other units by giving
a scaling factor is only possible if the units have the same scale. Otherwise,
units have to be instantiated via the coresponding :class:`Unit` sub-class
without giving a definition:

    >>> class Temperature(Quantity):
    ...     pass
    ...
    >>> CELSIUS = Temperature.Unit('°C', 'Degree Celsius')
    >>> FAHRENHEIT = Temperature.Unit('°F', 'Degree Fahrenheit')
    >>> KELVIN = Temperature.Unit('K', 'Kelvin')

**Derived** types of quantities are declared by giving a definition based on
more basic types of quantities:

    >>> class Volume(Quantity):
    ...     defineAs = Length ** 3
    ...     refUnitName = 'Cubic Metre'
    ...
    >>> class Duration(Quantity):
    ...     refUnitName = 'Second'
    ...     refUnitSymbol = 's'
    ...
    >>> class Velocity(Quantity):
    ...     defineAs = Length / Duration
    ...     refUnitName = 'Metre per Second'
    ...

If no symbol for the reference unit is given with the class declaration, a
symbol is generated from the definition, as long as all types of quantities
in that definition have a reference unit.

    >>> print(Volume.refUnit.symbol)
    m³
    >>> print(Velocity.refUnit.symbol)
    m/s

Other units have to be defined explicitly. For derived quantities, the
function :func:`generateUnits` can be used to create all units from the
cross-product of all units of the quantity classes the class is derived from.

In order to define a **quantized** quantity, the smallest possible fraction
(in terms of the reference unit) can be given as class variable `quantum`. The
class method :meth:`Quantity.getQuantum` can then be used to retrieve the
smallest fraction for any unit:

    >>> class DataVolume(Quantity):
    ...     refUnitName = 'Byte'
    ...     refUnitSymbol = 'B'
    ...     quantum = Fraction(1, 8)
    ...
    >>> BYTE = DataVolume.refUnit
    >>> KILOBYTE = DataVolume.Unit('kB', 'Kilobyte', Decimal(1000) * BYTE)
    >>> DataVolume.getQuantum(KILOBYTE)
    Decimal('0.000125')

Instantiating quantities
------------------------

The simplest way to create an instance of a :class:`Quantity` subclass is to
call the class giving an amount and a unit. If the unit is omitted, the
quantity's reference unit is used (if one is defined):

    >>> Length(15, MILLIMETRE)
    Length(Decimal(15), Length.Unit('mm'))
    >>> Length(15)
    Length(Decimal(15))

Alternatively, the two-args infix operator '^' can be used to combine an
amount and a unit:

    >>> 17.5 ^ KILOMETRE
    Length(Decimal('17.5'), Length.Unit('km'))

Also, it's possible to create a :class:`Quantity` instance from a string
representation:

    >>> Length('17.5 km')
    Length(Decimal('17.5'), Length.Unit('km'))

If a unit is given in addition, the resulting quantity is converted
accordingly:

    >>> Length('17 m', KILOMETRE)
    Length(Decimal('0.017'), Length.Unit('km'))

Instead of calling a subclass, the class :class:`Quantity` can be used as a
factory function …:

    >>> Quantity(15, MILLIMETRE)
    Length(Decimal(15), Length.Unit('mm'))
    >>> Quantity('17.5 km')
    Length(Decimal('17.5'), Length.Unit('km'))

… as long as a unit is given:

    >>> Quantity(17.5)
    ValueError: A unit must be given.

If the :class:`Quantity` subclass defines a `quantum`, the amount of each
instance is automatically rounded to this quantum:

    >>> DataVolume('1/7', KILOBYTE)
    DataVolume(Decimal('0.142875'), DataVolume.Unit('kB'))

Converting between units
------------------------

A quantity can be converted to a quantity using a different unit by calling
the method :meth:`Quantity.convert`:

    >>> l5cm = Length(Decimal(5), CENTIMETRE)
    >>> l5cm.convert(MILLIMETRE)
    Length(Decimal('50'), Length.Unit('mm'))
    >>> l5cm.convert(KILOMETRE)
    Length(Decimal('0.00005'), Length.Unit('km'))

To get just the amount of a quantity in another unit, that unit can be called
with the quantity as parameter:

    >>> MILLIMETRE(l5cm)
    Decimal('50')
    >>> KILOMETRE(l5cm)
    Decimal('0.00005')

These kinds of conversion are automatically enabled for types of quantities
with reference units. For other types of quantities there is no default way
of converting between units.

    >>> t27c = Temperature(Decimal(27), CELSIUS)
    >>> t27c.convert(FAHRENHEIT)
    quantity.quantity.IncompatibleUnitsError: Can't convert 'Degree Celsius' \
to 'Degree Fahrenheit'

.. _converters_label:

Converters
^^^^^^^^^^

For types of quantities that do not have a reference unit, one or more
callables can be registered as converters:

    >>> def fahrenheit2celsius(qty, toUnit):
    ...     if qty.unit is FAHRENHEIT and toUnit is CELSIUS:
    ...         return (qty.amount - 32) / Decimal('1.8')
    ...     return None
    ...
    >>> def celsius2fahrenheit(qty, toUnit):
    ...     if qty.unit is CELSIUS and toUnit is FAHRENHEIT:
    ...         return qty.amount * Decimal('1.8') + 32
    ...     return None
    ...
    >>> Temperature.Unit.registerConverter(celsius2fahrenheit)
    >>> Temperature.Unit.registerConverter(fahrenheit2celsius)
    >>> list(Temperature.Unit.registeredConverters())
    [<function celsius2fahrenheit at 0x7fab71bfef50>, \
<function fahrenheit2celsius at 0x7fab71bf7cf8>]

For the signature of the callables used as converters see :class:`Converter`.

    >>> t27c.convert(FAHRENHEIT)
    Temperature(Decimal('80.6'), Temperature.Unit('\xb0F'))
    >>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
    Temperature(Decimal('27'), Temperature.Unit('\xb0C'))

Alternatively, an instance of :class:`TableConverter` can be created and
registered as converter.

The example given above can be implemented as follows:

    >>> tempConv = TableConverter({(CELSIUS, FAHRENHEIT):
                                   (Decimal('1.8'), 32)})
    >>> Temperature.Unit.registerConverter(tempConv)
    >>> t27c = Temperature(Decimal(27), CELSIUS)
    >>> t27c.convert(FAHRENHEIT)
    Temperature(Decimal('80.6'), Temperature.Unit('\xb0F'))

It is suffient to define the conversion in one direction, because a
reversed conversion is used automatically:

>>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
Temperature(Decimal(27), Temperature.Unit('\xb0C'))

Unit-safe computations
----------------------

Comparison
^^^^^^^^^^

Quantities can be compared to other quantities using all comparison operators
defined for numbers:

    >>> Length(27) > Length(9)
    True
    >>> Length(27) >= Length(91)
    False
    >>> Length(27) < Length(9)
    False
    >>> Length(27) <= Length(91)
    True
    >>> Length(27) == Length(27)
    True
    >>> Length(27) != Length(91)
    True

Different units are taken in to account automatically, as long as they are
compatible, i. e. a conversion is available:

    >>> Length(27, METRE) <= Length(91, CENTIMETRE)
    False
    >>> Temperature(20, CELSIUS) > Temperature(20, FAHRENHEIT)
    True
    >>> Temperature(20, CELSIUS) > Temperature(20, KELVIN)
    IncompatibleUnitsError: Can't convert 'Kelvin' to 'Degree Celsius'

Testing instances of different quantity types for equality always returns
false:

    >>> Length(20) == Mass(20)
    False
    >>> Length(20) != Mass(20)
    True

All other comparison operators raise an `IncompatibleUnitsError` in this case.

Addition and subtraction
^^^^^^^^^^^^^^^^^^^^^^^^

Quantities can be added to or subtracted from other quantities …:

    >>> Length(27) + Length(9)
    Length(Decimal(36))
    >>> Length(27) - Length(91)
    Length(Decimal(-64))

… as long as they are instances of the same quantity type:

    >>> Length(27) + Duration(9)
    IncompatibleUnitsError: Can't add a 'Length' and a 'Duration'

When quantities with different units are added or subtracted, the values are
converted to the unit of the first, if possible …:

    >>> Length(27) + Length(12, CENTIMETRE)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETRE) + Length(17, METRE)
    Length(Decimal('1712'), Length.Unit('cm'))
    >>> Temperature(20, CELSIUS) - Temperature(50, FAHRENHEIT)
    Temperature(Decimal('10'), Temperature.Unit('\xb0C'))

… but an exception is raised, if not:

    >>> Temperature(20, CELSIUS) - Temperature(281, KELVIN)
    IncompatibleUnitsError: Can't convert 'Kelvin' to 'Degree Celsius'

Multiplication and division
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Quantities can be multiplied or divided by scalars, preserving the unit:

    >>> 7.5 * Length(3, CENTIMETRE)
    Length(Decimal('22.5'), Length.Unit('cm'))
    >>> Duration(66, MINUTE) / 11
    Duration(Decimal(6), Duration.Unit('min'))

Quantities can be multiplied or divided by other quantities …:

    >>> Length(15, METRE) / Duration(3, SECOND)
    Velocity(Decimal(5))

… as long as the resulting type of quantity is defined …:

    >>> Duration(4, SECOND) * Length(7)
    UndefinedResultError: Undefined result: Duration * Length
    >>> Length(12, KILOMETRE) / Duration(2, MINUTE) / Duration(50, SECOND)
    UndefinedResultError: Undefined result: Velocity / Duration
    >>> class Acceleration(Quantity):
    ...     defineAs = Length / Duration ** 2
    ...     refUnitName = 'Metre per Second squared'
    ...
    >>> Length(12, KILOMETRE) / Duration(2, MINUTE) / Duration(50, SECOND)
    Acceleration(Decimal(2))

… or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.4')

When cascading operations, all intermediate results have to be defined:

    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    UndefinedResultError: Undefined result: Length * Length
    >>> class Area(Quantity):
    ...     defineAs = Length ** 2
    ...     refUnitName = 'Square Metre'
    ...
    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    Volume(Decimal(19500000, 3))

Exponentiation
^^^^^^^^^^^^^^

Quantities can be raised by an exponent, as long as the exponent is an
`Integral` number and the resulting quantity is defined:

    >>> (5 ^ METRE) ** 2
    Area(Decimal(25))
    >>> (5 ^ METRE) ** 2.5
    TypeError: unsupported operand type(s) for ** or pow(): 'Length' and
        'float'
    >>> (5 ^ METRE) ** -2
    UndefinedResultError: Undefined result: Length ** -2

Rounding
--------

The amount of a quantity can be rounded by using the standard `round`
function.

If an Integral is given as precision, a copy of the quanitity is returned,
with its amount rounded accordingly:

    >>> round(Length(Decimal('17.375'), MILLIMETRE), 1)
    Length(Decimal('17.4'), Length.Unit('mm'))

In addition, a unit or a quantity (of the same type) can be given to specify
the requested precision. The resulting quantity will then be the integer
multiple of that precision closest to the called quantity:

    >>> round(Length(Decimal('17.375'), METRE), CENTIMETRE)
    Length(Decimal('17.38'))
    >>> round(Length(Decimal('17.375'), METRE), Length(5, CENTIMETRE))
    Length(Decimal('17.4', 2))
    >>> round(Length(Decimal('17.372'), METRE), Length(5, CENTIMETRE))
    Length(Decimal('17.35'))

In any case the unit of the resulting quantity will be the same as the unit
of the called quantity.

.. note::
    This only applies to Python 3.x !!! In Python 2.x the standard `round`
    function tries to convert its first operand to a `float` and thus raises
    an exception when called with a quantity.

    You may circumvent this by modifying the built-in `round` function::

        try:
            int.__round__
        except AttributeError:
            import __builtin__
            py2_round = __builtin__.round

            def round(number, ndigits=0):
                try:
                    return number.__round__(ndigits)
                except AttributeError:
                    return py2_round(number, ndigits)

            __builtin__.round = round
            del __builtin__

    But be aware: this has side-effects if there are other classes defining a
    method named `__round__` !!!

    As an alternative the method :meth:`Quantity.quantize` can be used.

For more advanced cases of rounding the method :meth:`Quantity.quantize` can
round a quantity to any quantum according to any rounding mode:

    >>> l = Length('1.7296 km')
    >>> l.quantize(METRE)
    Length(Decimal('1.73', 3), Length.Unit('km'))
    >>> l.quantize(25 ^ METRE)
    Length(Decimal('1.725'), Length.Unit('km'))
    >>> l.quantize(25 ^ METRE, ROUND_UP)
    Length(Decimal('1.75', 3), Length.Unit('km'))

Apportioning
------------

The method :meth:`Quantity.allocate` can be used to apportion a quantity
according to a sequence of ratios:

    >>> m = Mass('10 kg')
    >>> ratios = [38, 5, 2, 15]
    >>> portions, remainder = m.allocate(ratios)
    >>> portions
    [Mass(Fraction(19, 3)),
     Mass(Fraction(5, 6)),
     Mass(Fraction(1, 3)),
     Mass(Decimal('2.5', 2))]
    >>> remainder
    Mass(Decimal(0, 2)))

If the quantity is quantized, there can be rounding errors causing a remainder
with an amount other than 0:

    >>> b = 10 ^ KILOBYTE
    >>> portions, remainder = b.allocate(ratios, disperseRoundingError=False)
    >>> portions
    [DataVolume(Decimal('6.333375'), DataVolume.Unit('kB')),
     DataVolume(Decimal('0.833375'), DataVolume.Unit('kB')),
     DataVolume(Decimal('0.333375'), DataVolume.Unit('kB')),
     DataVolume(Decimal('2.5', 6), DataVolume.Unit('kB'))]
    >>> remainder
    DataVolume(Decimal('-0.000125'), DataVolume.Unit('kB')))

By default the remainder will be dispersed:

    >>> portions, remainder = b.allocate(ratios)
    >>> portions
    [DataVolume(Decimal('6.333375'), DataVolume.Unit('kB')),
     DataVolume(Decimal('0.833375'), DataVolume.Unit('kB')),
     DataVolume(Decimal('0.33325', 6), DataVolume.Unit('kB')),
     DataVolume(Decimal('2.5', 6), DataVolume.Unit('kB'))],
    >>> remainder
    DataVolume(Decimal(0, 6), DataVolume.Unit('kB')))

As well as of numbers, quantities can be used as ratios (as long as they have
compatible units):

    >>> l = 10 ^ LITRE
    >>> ratios = [350 ^ GRAM, 500 ^ GRAM, 3 ^ KILOGRAM, 150 ^ GRAM]
    >>> l.allocate(ratios)
    ([Volume(Decimal('0.875', 4), Volume.Unit('l')),
      Volume(Decimal('1.25', 3), Volume.Unit('l')),
      Volume(Decimal('7.5', 2), Volume.Unit('l')),
      Volume(Decimal('0.375', 4), Volume.Unit('l'))],
     Volume(Decimal(0, 4), Volume.Unit('l')))

Formatting as string
--------------------

:class:`Quantity` supports the standard `str` and `unicode` (Python 2.x only)
functions. Both return a string representation of the quantity's amount
followed by a blank and the quantity's units symbol.

.. note::
    While the `str` function in Python 3.x and the `unicode` function in
    Python 2.x return the result as a unicode string, the `str` function in
    Python 2.x returns an utf8-encoded bytes string.

In addition, :class:`Quantity` supports the standard `format` function. The
format specifier should use two keys: 'a' for the amount and '' for the unit,
where 'a' can be followed by a valid format spec for numbers and '' by a
valid format spec for strings. If no format specifier is given, '{a} {u}' is
used:

    >>> v = Volume('19.36')
    >>> format(v)
    '19.36 m\xb3'
    >>> format(v, '{a:*>10.2f} {u:<3}')
    '*****19.36 m\xb3 '
"""


from .converter import Converter, TableConverter
from .exceptions import (IncompatibleUnitsError, QuantityError,
                         UndefinedResultError, UnitConversionError)
from .money import Currency, ExchangeRate, Money, registerCurrency
from .qtybase import Quantity, Unit, generateUnits
from .qtyreg import get_unit_by_symbol
from .utils import sum
from .version import version_tuple as __version__


# defined here in order to reduce pickle foot-print
def r(q_repr: str) -> Quantity:
    """Reconstruct quantity from string representation."""
    return Quantity(q_repr)


__all__ = [
    'Quantity',
    'Unit',
    'get_unit_by_symbol',
    'generateUnits',
    'sum',
    'QuantityError',
    'IncompatibleUnitsError',
    'UndefinedResultError',
    'Converter',
    'TableConverter',
    'UnitConversionError',
    'Currency',
    'Money',
    'ExchangeRate',
    'registerCurrency',
]
