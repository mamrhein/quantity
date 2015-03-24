# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        quantity (package)
## Purpose:     Unit-safe computations with quantities.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Unit-safe computations with quantities.

Introduction
============

What is a quantity?
-------------------

"The value of a quantity is generally expressed as the product of a number
and a unit. The unit is simply a particular example of the quantity concerned
which is used as a reference, and the number is the ratio of the value of the
quantity to the unit." (Bureau International des Poids et Mesures: The
International System of Units, 8th edition, 2006)

Basic types of quantities are defined "by convention", they do not depend on
other types of quantities, for example Length, Mass or Duration.

Derived types of quantities, on the opposite, are defined as products of other
types of quantities raised by some exponent.

Examples:

* Volume = Length ** 3

* Velocity = Length ** 1 * Duration ** -1

* Acceleration = Length ** 1 * Duration ** -2

* Force = Mass ** 1 * Acceleration ** 1

Each type of quantity may have one special unit which is used as a reference
for the definition of all other units, for example Metre, Kilogram and
Second. The other units are then defined by their relation to the reference
unit.

If a type of quantity is derived from types of quantities that all have a
reference unit, then the reference unit of that type is defined by a formula
that follows the formula defining the type of quantity.

Examples:

* Velocity -> Metre per Second = Metre ** 1 * Second ** -1

* Acceleration -> Metre per Second squared = Metre ** 1 * Second ** -2

* Force -> Newton = Kilogram ** 1 * Metre ** 1 * Second ** -2


"Systems of measure"
--------------------

There may be different systems which define quantities, their units and the
relations between these units in a different way.

This is not directly supported by this module. For each type of quantity there
can be only no or exactly one reference unit. But, if you have units from
different systems for the same type of quantity, you can define these units
and provide mechanisms to convert between them (see :ref:`converters_label`).

Defining a quantity class
=========================

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
without giving a definition.

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

Instantiating quantities
========================

The simplest way to create an instance of a :class:`Quantity` subclass is to
call the class giving an amount and a unit. If the unit is omitted, the
quantity's reference unit is used (if one is defined).

    >>> Length(15, MILLIMETRE)
    Length(Decimal(15), Length.Unit(u'mm'))
    >>> Length(15)
    Length(Decimal(15))

Alternatively, the two-args infix operator '^' can be used to combine an
amount and a unit:

    >>> 17.5 ^ KILOMETRE
    Length(Decimal('17.5'), Length.Unit(u'km'))

Also, it's possible to create a :class:`Quantity` instance from a string
representation:

    >>> Length('17.5 km')
    Length(Decimal('17.5'), Length.Unit(u'km'))

If a unit is given in addition, the resulting quantity is converted
accordingly:

    >>> Length('17 m', KILOMETRE)
    Length(Decimal('0.017'), Length.Unit(u'km'))

Instead of calling a subclass, the class :class:`Quantity` can be used as a
factory function ...

    >>> Quantity(15, MILLIMETRE)
    Length(Decimal(15), Length.Unit(u'mm'))
    >>> Quantity('17.5 km')
    Length(Decimal('17.5'), Length.Unit(u'km'))

... as long as a unit is given:

    >>> Quantity(17.5)
    ValueError: A unit must be given.

Converting between units
========================

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
    quantity.quantity.IncompatibleUnitsError: Can't convert 'Degree Celsius'
    to 'Degree Fahrenheit'

.. _converters_label:

Converters
----------

For types of quantities that do not have a reference unit, one or more
callables can be registered as converters.

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
    [<function celsius2fahrenheit at 0x7fab71bfef50>,
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
    Temperature(Decimal('80.6'), Temperature.Unit(u'\xb0F'))

It is suffient to define the conversion in one direction, because a
reversed conversion is used automatically:

>>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
Temperature(Decimal(27), Temperature.Unit(u'\xb0C'))

Unit-safe computations
======================

Comparison
----------

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
------------------------

Quantities can be added to or subtracted from other quantities ...

    >>> Length(27) + Length(9)
    Length(Decimal(36))
    >>> Length(27) - Length(91)
    Length(Decimal(-64))

... as long as they are instances of the same quantity type:

    >>> Length(27) + Duration(9)
    IncompatibleUnitsError: Can't add a 'Length' and a 'Duration'

When quantities with different units are added or subtracted, the values are
converted to the unit of the first, if possible ...:

    >>> Length(27) + Length(12, CENTIMETRE)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETRE) + Length(17, METRE)
    Length(Decimal('1712'), Length.Unit('cm'))
    >>> Temperature(20, CELSIUS) - Temperature(50, FAHRENHEIT)
    Temperature(Decimal('10'), Temperature.Unit(u'\xb0C'))

... but an exception is raised, if not:

    >>> Temperature(20, CELSIUS) - Temperature(281, KELVIN)
    IncompatibleUnitsError: Can't convert 'Kelvin' to 'Degree Celsius'

Multiplication and division
---------------------------

Quantities can be multiplied or divided by scalars, preserving the unit ...:

    >>> 7.5 * Length(3, CENTIMETRE)
    Length(Decimal('22.5'), Length.Unit(u'cm'))
    >>> Duration(66, MINUTE) / 11
    Duration(Decimal(6), Duration.Unit(u'min'))

Quantities can be multiplied or divided by other quantities ...:

    >>> Length(15, METRE) / Duration(3, SECOND)
    Velocity(Decimal(5))

... as long as the resulting type of quantity is defined ...:

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

... or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.4')

When cascading operations, all intermediate results have to be defined:

    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    UndefinedResultError: Undefined result: Length * Length
    >>> class Area(Quantity):
    ...         defineAs = Length ** 2
    ...         refUnitName = 'Square Metre'
    ...
    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    Volume(Decimal(19500000, 3))

Exponentiation
--------------

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
========

The amount of a quantity can be rounded by using the standard `round`
function.

If an Integral is given as precision, a copy of the quanitity is returned,
with its amount rounded accordingly.

    >>> round(Length(Decimal('17.375'), MILLIMETRE), 1)
    Length(Decimal('17.4'), Length.Unit('mm'))

In addition, a unit or a quantity (of the same type) can be given to specify
the requested precision. The resulting quantity will then be the integer
multiple of that precision closest to the called quantity.

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

    You may circumvent this by modifying the built-in `round` function:

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

    But be aware that this has side-effects if there are other classes
    defining a method named `__round__` !!!

    As an alternative the method :meth:`Quantity.quantize` can be used.

Formatting as string
====================

:class:`Quantity` supports the standard `str` and `unicode` (Python 2.x only)
functions. Both return a string representation of the quantity's amount
followed by a blank and the quantity's units symbol.

.. note::
    While the `str` function in Python 3.x and the `unicode` function in
    Python 2.x return the result as a unicode string, the `str` function in
    Python 2.x returns an utf8-encoded bytes string.

In addition, :class:`Quantity` supports the standard `format` function. The
format specifier should use two keys: 'a' for the amount and 'u' for the unit,
where 'a' can be followed by a valid format spec for numbers and 'u' by a
valid format spec for strings. If no format specifier is given, '{a} {u}' is
used.

    >>> v = Volume('19.36')
    >>> format(v)
    u'19.36 m\xb3'
    >>> format(v, '{a:*>10.2f} {u:<3}')
    u'*****19.36 m\xb3 '
"""

from __future__ import absolute_import, unicode_literals
from .qtybase import (Quantity, Unit, getUnitBySymbol, QuantityError,
                      IncompatibleUnitsError, UndefinedResultError)
from .converter import Converter, TableConverter

__version__ = 0, 7, 1


# defined here in order to reduce pickle foot-print
def r(qRepr):
    """Reconstruct quantity from string representation."""
    return Quantity(qRepr)


__all__ = ['Quantity',
           'Unit',
           'getUnitBySymbol',
           'QuantityError',
           'IncompatibleUnitsError',
           'UndefinedResultError',
           'Converter',
           'TableConverter']
