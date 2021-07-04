The package _quantity_ provides classes for unit-safe computations with
quantities, including money.

### Defining a quantity class

A **basic** type of quantity is declared just by sub-classing _Quantity_:

    >>> class Length(Quantity):
    ...     pass
    ...

But, as long as there is no unit defined for that class, you can not create
any instance for the new quantity class:

    >>> l = Length(1)
    Traceback (most recent call last):
    ValueError: A unit must be given.

If there is a reference unit, the simplest way to define it is giving a name
and a symbol for it as keywords. The meta-class of _Quantity_ will
then create a unit automatically:

    >>> class Mass(Quantity,
    ...            ref_unit_name='Kilogram',
    ...            ref_unit_symbol='kg'):
    ...     pass
    ...
    >>> Mass.ref_unit
    Unit('kg')
    >>> class Length(Quantity,
    ...              ref_unit_name='Metre',
    ...              ref_unit_symbol='m'):
    ...     pass
    ...
    >>> Length.ref_unit
    Unit('m')

Now, this unit can be given to create a quantity:

    >>> METRE = Length.ref_unit
    >>> print(Length(15, METRE))
    15 m

If no unit is given, the reference unit is used:

    >>> print(Length(15))
    15 m

Other units can be derived from the reference unit (or another unit), giving
a definition by multiplying a scaling factor with that unit:

    >>> a_thousandth = Decimal("0.001")
    >>> KILOGRAM = Mass.ref_unit
    >>> GRAM = Mass.new_unit('g', 'Gram', a_thousandth * KILOGRAM)
    >>> MILLIMETRE = Length.new_unit('mm', 'Millimetre', a_thousandth * METRE)
    >>> MILLIMETRE
    Unit('mm')
    >>> KILOMETRE = Length.new_unit('km', 'Kilometre', 1000 * METRE)
    >>> KILOMETRE
    Unit('km')
    >>> CENTIMETRE = Length.new_unit('cm', 'Centimetre', 10 * MILLIMETRE)
    >>> CENTIMETRE
    Unit('cm')

Instead of a number a SI prefix can be used as scaling factor. SI prefixes are
provided in a sub-module:

    >>> from quantity.si_prefixes import *
    >>> NANO.abbr, NANO.name, NANO.factor
    ('n', 'Nano', Decimal('0.000000001'))

    >>> NANOMETRE = Length.new_unit('nm', 'Nanometre', NANO * METRE)
    >>> NANOMETRE
    Unit('nm')

Using one unit as a reference and defining all other units by giving a
scaling factor is only possible if the units have the same scale. Otherwise,
units can just be instantiated without giving a definition:

    >>> class Temperature(Quantity):
    ...     pass
    ...
    >>> CELSIUS = Temperature.new_unit('°C', 'Degree Celsius')
    >>> FAHRENHEIT = Temperature.new_unit('°F', 'Degree Fahrenheit')
    >>> KELVIN = Temperature.new_unit('K', 'Kelvin')

**Derived** types of quantities are declared by giving a definition based on
more basic types of quantities:

    >>> class Volume(Quantity,
    ...              define_as=Length ** 3,
    ...              ref_unit_name='Cubic Metre'):
    ...     pass
    ...
    >>> class Duration(Quantity,
    ...                ref_unit_name='Second',
    ...                ref_unit_symbol='s'):
    ...     pass
    ...
    >>> class Velocity(Quantity,
    ...                define_as=Length / Duration,
    ...                ref_unit_name='Metre per Second'):
    ...     pass
    ...

If no symbol for the reference unit is given with the class declaration, a
symbol is generated from the definition, as long as all types of quantities
in that definition have a reference unit.

    >>> Volume.ref_unit.symbol
    'm³'
    >>> Velocity.ref_unit.symbol
    'm/s'

Other units have to be defined explicitly. This can be done either as shown
above or by deriving them from units of the base quantities:

    >>> CUBIC_CENTIMETRE = Volume.derive_unit_from(CENTIMETRE,
    ...                                            name='Cubic Centimetre')
    >>> CUBIC_CENTIMETRE
    Unit('cm³')
    >>> HOUR = Duration.new_unit('h', 'Hour', 3600 * Duration.ref_unit)
    >>> KILOMETRE_PER_HOUR = Velocity.derive_unit_from(KILOMETRE, HOUR)
    >>> KILOMETRE_PER_HOUR
    Unit('km/h')

### Instantiating quantities

The simplest way to create an instance of a class _Quantity_ subclass is to
call the class giving an amount and a unit. If the unit is omitted, the
quantity's reference unit is used (if one is defined):

    >>> Length(15, MILLIMETRE)
    Length(Decimal(15), Unit('mm'))

Alternatively, an amount and a unit can be multiplied:

    >>> 17.5 * KILOMETRE
    Length(Decimal('17.5'), Unit('km'))

Also, it's possible to create a _Quantity_ sub-class instance from a string
representation:

    >>> Length('17.5 km')
    Length(Decimal('17.5'), Unit('km'))

### Unit-safe computations

A quantity can be converted to a quantity using a different unit by calling
the method _Quantity.convert_:

    >>> l5cm = Length(Decimal(5), CENTIMETRE)
    >>> l5cm.convert(MILLIMETRE)
    Length(Decimal(50), Unit('mm'))
    >>> l5cm.convert(KILOMETRE)
    Length(Decimal('0.00005'), Unit('km'))

Quantities can be compared to other quantities using all comparison operators
defined for numbers. Different units are taken into account automatically, as
long as they are compatible, i.e. a conversion is available:

    >>> Length(27) <= Length(91)
    True
    >>> Length(27, METRE) <= Length(91, CENTIMETRE)
    False

Quantities can be added to or subtracted from other quantities …:

    >>> Length(27) + Length(9)
    Length(Decimal(36))
    >>> Length(27) - Length(91)
    Length(Decimal(-64))
    >>> Length(27) + Length(12, CENTIMETER)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETER) + Length(17, METER)
    Length(Decimal('1712'), Length.Unit('cm'))

… as long as they are instances of the same quantity type:

    >>> Length(27) + Duration(9)
    Traceback (most recent call last):
    IncompatibleUnitsError: Can't add a 'Length' and a 'Duration'

Quantities can be multiplied or divided by scalars, preserving the unit:

    >>> 7.5 * Length(3, CENTIMETRE)
    Length(Decimal('22.5'), Unit('cm'))
    >>> Duration(66, MINUTE) / 11
    Duration(Decimal(6), Unit('min'))

Quantities can be multiplied or divided by other quantities …:

    >>> Length(15, METRE) / Duration(3, SECOND)
    Velocity(Decimal(5))

… as long as the resulting type of quantity is defined …:

    >>> Duration(4, SECOND) * Length(7)
    Traceback (most recent call last):
    UndefinedResultError: Undefined result: Duration * Length

… or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.4')

### Money

_Money_ is a special type of quantity. Its unit type is known as currency.

Money differs from physical quantities mainly in two aspects:

* Money amounts are discrete. For each currency there is a smallest fraction
  that can not be split further.

* The relation between different currencies is not fixed, instead, it varies
  over time.

The sub-package _quantity.money_ provides classes and functions to deal
with these specifics.

A currency must explicitly be registered as a unit for further use. The
easiest way to do this is to call _Money.register_currency_. The method
is backed by a database of currencies defined in ISO 4217. It takes the 
3-character ISO 4217 code as parameter.

_Money_ derives from _Quantity_, so all operations on quantities can also be
applied to instances of _Money_. But because there is no fixed relation
between currencies, there is no implicit conversion between money amounts of
different currencies. Resulting values are always quantized to the smallest
fraction defined with the currency.

A conversion factor between two currencies can be defined by using the
class _ExchangeRate_. It is given a unit currency (aka base currency), a unit
multiple, a term currency (aka price currency) and a term amount, i.e. the
amount in term currency equivalent to unit multiple in unit currency.

Multiplying an amount in some currency with an exchange rate with the same
currency as unit currency results in the equivalent amount in term currency.
Likewise, dividing an amount in some currency with an exchange rate with the
same currency as term currency results in the equivalent amount in unit
currency.

As _Money_ derives from _Quantity_, it can be combined with other quantities
in order to define a new quantity. This is, for example, useful for defining
prices per quantum.

For more details see the documentation provided with the source distribution
or [here](https://quantity.readthedocs.io/).
