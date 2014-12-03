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
types of quantities raised by some exponend.

Examples:

* Volume = Length ** 3

* Velocity = Length ** 1 * Duration ** -1

* Acceleration = Length ** 1 * Duration ** -2

* Force = Mass ** 1 * Acceleration ** 1

Each type of quantity may have one special unit which is used as a reference
for the definition of all other units, for example Meter, Kilogram and
Second. The other units are then defined by their relation to the reference
unit.

If a type of quantity is derived from types of quantities that all have a
reference unit, then the reference unit of that type is defined by a formula
that follows the formula defining the type of quantity.

Examples:

* Velocity -> Meter per Second = Meter ** 1 * Second ** -1

* Acceleration -> Meter per Second squared = Meter ** 1 * Second ** -2

* Force -> Newton = Kilogram ** 1 * Meter ** 1 * Second ** -2


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
    ...     refUnitName = 'Meter'
    ...     refUnitSymbol = 'm'
    ...
    >>> Length.refUnit
    Length.Unit('m')

Now, this unit can be given to create a quantity:

    >>> METER = Length.refUnit
    >>> print(Length(15, METER))
    15 m

If no unit is given, the reference unit is used:

    >>> print(Length(15)
    15 m

Other units can be derived from the reference unit (or another unit), giving
a definition by multiplying a scaling factor with that unit:

    >>> MILLIMETER = Length.Unit('mm', 'Millimeter', Decimal('0.001') * METER)
    >>> MILLIMETER
    Length.Unit('mm')
    >>> KILOMETER = Length.Unit('km', 'Kilometer', 1000 * METER)
    >>> KILOMETER
    Length.Unit('km')
    >>> CENTIMETER = Length.Unit('cm', 'Centimeter', 10 * MILLIMETER)
    >>> CENTIMETER
    Length.Unit('cm')

Using one unit as a reference and defining all other units by giving
a scaling factor is only possible if the units have the same scale. Otherwise,
units have to be instantiated via the coresponding :class:`Unit` sub-class
without giving a definition.

    >>> class Temperature(Quantity):
    ...     pass
    ...
    >>> CELSIUS = Temperature.Unit('°C', 'Degree Celsius')
    >>> KELVIN = Temperature.Unit('°K', 'Degree Kelvin')
    >>> FAHRENHEIT = Temperature.Unit('°F', 'Degree Fahrenheit')

**Derived** types of quantities are declared by giving a definition based on
more basic types of quantities:

    >>> class Volume(Quantity):
    ...     defineAs = Length ** 3
    ...     refUnitName = 'Cubic Meter'
    ...
    >>> class Duration(Quantity):
    ...     refUnitName = 'Second'
    ...     refUnitSymbol = 's'
    ...
    >>> class Velocity(Quantity):
    ...     defineAs = Length / Duration
    ...     refUnitName = 'Meter per Second'
    ...

If no symbol for the reference unit is given with the class declaration, a
symbol is generated from the definition, as long as all types of quantities
in that definition have a reference unit.

    >>> print(Volume.refUnit.symbol)
    m³
    >>> print(Velocity.refUnit.symbol)
    m/s

Converting between units
========================

A quantity can be converted to a quantity using a different unit by calling
the method :meth:`Quantity.convert`:

    >>> l5cm = Length(Decimal(5), CENTIMETER)
    >>> l5cm.convert(MILLIMETER)
    Length(Decimal('50'), Length.Unit('mm'))
    >>> l5cm.convert(KILOMETER)
    Length(Decimal('0.00005'), Length.Unit('km'))

To get just the amount of a quantity in another unit, that unit can be called
with the quantity as parameter:

    >>> MILLIMETER(l5cm)
    Decimal('50')
    >>> KILOMETER(l5cm)
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
    ...         return (Decimal(qty.amount) - Decimal(32)) / Decimal('1.8')
    ...     return None
    ...
    >>> def celsius2fahrenheit(qty, toUnit):
    ...     if qty.unit is CELSIUS and toUnit is FAHRENHEIT:
    ...         return Decimal(qty.amount) * Decimal('1.8') + Decimal(32)
    ...     return None
    ...
    >>> Temperature.Unit.registerConverter(celsius2fahrenheit)
    >>> Temperature.Unit.registerConverter(fahrenheit2celsius)
    >>> list(Temperature.Unit.registeredConverters())
    [<function celsius2fahrenheit at 0x7fab71bfef50>,
    <function fahrenheit2celsius at 0x7fab71bf7cf8>]

For the signature of the callables used as converters see :class:`Converter`.

    >>> t27c.convert(FAHRENHEIT)
    Temperature(Decimal('80.6'), Temperature.Unit('\xc2\xb0F'))
    >>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
    Temperature(Decimal('27'), Temperature.Unit('\xc2\xb0C'))

.. note::
    The numerical part of a quantity is not forced to a specific type of
    number. All computations are done via the number types used when defining
    units and instanciating quantities. Therefore the type of the numerical
    part of the result depends on these computations. Mixing different types
    of numbers may lead to unwanted results.

TODO: document TableConverter

Unit-safe computations
======================

Comparison
----------

TODO

Addition and subtraction
------------------------

Quantities can be added to or subtracted from other quantities ...

    >>> Length(27) + Length(9)
    Length(36)
    >>> Length(27) - Length(91)
    Length(-64)

... as long as they are instances of the same quantity type:

    >>> Length(27) + Duration(9)
    quantity.quantity.IncompatibleUnitsError: Can't add a 'Length' and a
    'Duration'

When quantities with different units are added or subtracted, the values are
converted to the unit of the first, if possible ...:

    >>> Length(27) + Length(12, CENTIMETER)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETER) + Length(17, METER)
    Length(Decimal('1712'), Length.Unit('cm'))
    >>> Temperature(20, CELSIUS) - Temperature(50, FAHRENHEIT)
    Temperature(Decimal('10'), Temperature.Unit(u'\xb0C'))

... but an exception is raised, if not:

    >>> Temperature(20, CELSIUS) - Temperature(281, KELVIN)
    IncompatibleUnitsError: Can't convert 'Degree Kelvin' to 'Degree Celsius'

Multiplication and division
---------------------------

Quantities can be multiplied or divided by scalars, preserving the unit ...:

    >>> 7.5 * Length(3, CENTIMETER)
    Length(22.5, Length.Unit(u'cm'))
    >>> Duration(66, MINUTE) / 11
    Duration(6.0, Duration.Unit(u'min'))

Quantities can be multiplied or divided by other quantities ...:

    >>> Length(15, METER) / Duration(3, SECOND)
    Velocity(5.0)

... as long as the resulting type of quantity is defined ...:

    >>> Duration(4, SECOND) * Length(7)
    UndefinedResultError: Undefined result: Duration * Length
    >>> Length(12, KILOMETER) / Duration(2, MINUTE) / Duration(50, SECOND)
    UndefinedResultError: Undefined result: Velocity / Duration
    >>> class Acceleration(Quantity):
    ...     defineAs = Length / Duration ** 2
    ...     refUnitName = 'Meter per Second squared'
    ...
    >>> Length(12, KILOMETER) / Duration(2, MINUTE) / Duration(50, SECOND)
    Acceleration(Decimal('2.0000000000000000000000000'))

... or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.400000000000000000000000000')

When cascading operations, all intermediate results have to be defined:

    >>> Length(6, KILOMETER) * Length(13,  METER) * Length(250, METER)
    UndefinedResultError: Undefined result: Length * Length
    >>> class Area(Quantity):
    ...         defineAs = Length ** 2
    ...         refUnitName = 'Square Meter'
    ...
    >>> Length(6, KILOMETER) * Length(13,  METER) * Length(250, METER)
    Volume(Decimal('19500000.000'))

"""

#TODO: more documentation

from __future__ import absolute_import, unicode_literals
from .quantity import Quantity, QuantityFromString, Unit
from .quantity import IncompatibleUnitsError, UndefinedResultError
from .quantity import Converter, TableConverter

__all__ = ['Quantity',
           'QuantityFromString',
           'Unit',
           'IncompatibleUnitsError',
           'UndefinedResultError',
           'Converter',
           'TableConverter']
