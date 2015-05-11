The package `quantity` provides classes for unit-safe computations with
quantities, including money.

Defining a quantity class
=========================

A **basic** type of quantity is declared just by sub-classing the class
`Quantity`:

    >>> class Length(Quantity):
    ...     pass

In addition to the new quantity class the meta-class of class `Quantity`
creates a corresponding class for the units automatically. It can be
referenced via the quantity class:

    >>> Length.Unit
    <class 'quantity.quantity.LengthUnit'>

If the quantity has a unit which is used as a reference for defining other
units, the simplest way to define it is giving a name and a symbol for it as
class variables. The meta-class of class `Quantity` will then create a unit
automatically:

    >>> class Length(Quantity):
    ...     refUnitName = 'Meter'
    ...     refUnitSymbol = 'm'
    >>> Length.refUnit
    Length.Unit('m')

Now, this unit can be given to create a quantity:

    >>> METER = Length.refUnit
    >>> print(Length(15, METER))
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
units have to be instantiated via the coresponding class `Unit` sub-class
without giving a definition.

    >>> class Temperature(Quantity):
    ...     pass
    >>> CELSIUS = Temperature.Unit('°C', 'Degree Celsius')
    >>> FAHRENHEIT = Temperature.Unit('°F', 'Degree Fahrenheit')

**Derived** types of quantities are declared by giving a definition based on
more basic types of quantities:

    >>> class Volume(Quantity):
    ...     defineAs = Length ** 3
    ...     refUnitName = 'Cubic Meter'
    >>> class Duration(Quantity):
    ...     refUnitName = 'Second'
    ...     refUnitSymbol = 's'
    >>> class Velocity(Quantity):
    ...     defineAs = Length / Duration
    ...     refUnitName = 'Meter per Second'

If no symbol for the reference unit is given with the class declaration, a
symbol is generated from the definition, as long as all types of quantities
in that definition have a reference unit.

    >>> print(Volume.refUnit.symbol)
    m³
    >>> print(Velocity.refUnit.symbol)
    m/s

Instantiating quantities
========================

The simplest way to create an instance of a class `Quantity` subclass is to
call the class giving an amount and a unit. If the unit is omitted, the
quantity's reference unit is used (if one is defined).

    >>> Length(15, MILLIMETER)
    Length(Decimal(15), Length.Unit(u'mm'))

Alternatively, the two-args infix operator '^' can be used to combine an
amount and a unit:

    >>> 17.5 ^ KILOMETER
    Length(Decimal('17.5'), Length.Unit(u'km'))

Also, it's possible to create a `Quantity` sub-class instance from a string
representation:

    >>> Length('17.5 km')
    Length(Decimal('17.5'), Length.Unit(u'km'))

Unit-safe computations
======================

A quantity can be converted to a quantity using a different unit by calling
the method `Quantity.convert`:

    >>> l5cm = Length(Decimal(5), CENTIMETER)
    >>> l5cm.convert(MILLIMETER)
    Length(Decimal('50'), Length.Unit('mm'))
    >>> l5cm.convert(KILOMETER)
    Length(Decimal('0.00005'), Length.Unit('km'))

Quantities can be compared to other quantities using all comparison operators
defined for numbers. Different units are taken into account automatically, as
long as they are compatible, i. e. a conversion is available:

    >>> Length(27) <= Length(91)
    True
    >>> Length(27, METER) <= Length(91, CENTIMETER)
    False

Quantities can be added to or subtracted from other quantities ...

    >>> Length(27) + Length(9)
    Length(Decimal(36))
    >>> Length(27) - Length(91)
    Length(Decimal(-64))
    >>> Length(27) + Length(12, CENTIMETER)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETER) + Length(17, METER)
    Length(Decimal('1712'), Length.Unit('cm'))

... as long as they are instances of the same quantity type:

    >>> Length(27) + Duration(9)
    quantity.quantity.IncompatibleUnitsError: Can't add a 'Length' and a
        'Duration'

Quantities can be multiplied or divided by scalars, preserving the unit:

    >>> 7.5 * Length(3, CENTIMETER)
    Length(Decimal('22.5'), Length.Unit(u'cm'))
    >>> Duration(66, MINUTE) / 11
    Duration(Decimal(6), Duration.Unit(u'min'))

Quantities can be multiplied or divided by other quantities ...:

    >>> Length(15, METER) / Duration(3, SECOND)
    Velocity(Decimal(5))

... as long as the resulting type of quantity is defined ...:

    >>> Duration(4, SECOND) * Length(7)
    UndefinedResultError: Undefined result: Duration * Length

... or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.4')

Money
=====

Money is a special type of quantity. Its unit type is known as currency.

Money differs from physical quantities mainly in two aspects:

* Money amounts are discrete. For each currency there is a smallest fraction
  that can not be split further.

* The relation between different currencies is not fixed, instead, it varies
  over time.

The sub-package `quantity.money` provides classes and functions to deal with
these specifics.

A currency must explicitly be registered as a unit for further use. The
easiest way to do this is to call the function :func:`registerCurrency`. The
function is backed by a database of currencies defined in ISO 4217. It takes
the 3-character ISO 4217 code as parameter.

:class:`Money` derives from :class:`Quantity`, so all operations on quantities
can also be applied to instances of :class:`Money`. But because there is no
fixed relation between currencies, there is no implicit conversion between
money amounts of different currencies. Resulting values are always quantized
to the smallest fraction defined with the currency.

A conversion factor between two currencies can be defined by using the
:class:`ExchangeRate`. It is given a unit currency (aka base currency), a unit
multiple, a term currency (aka price currency) and a term amount, i.e. the
amount in term currency equivalent to unit multiple in unit currency.

Multiplying an amount in some currency with an exchange rate with the same
currency as unit currency results in the equivalent amount in term currency.
Likewise, dividing an amount in some currency with an exchange rate with the
same currency as term currency results in the equivalent amount in unit
currency.

As :class:`Money` derives from :class:`Quantity`, it can be combined with
other quantities in order to define a new quantity. This is, for example,
useful for defining prices per quantum.

For more details see the documentation provided with the source distribution
or `here <http://pythonhosted.org/quantity>`_.
