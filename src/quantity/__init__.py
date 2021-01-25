# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
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
r"""Unit-safe computations with quantities.

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

from __future__ import annotations

import operator
from decimal import Decimal as StdLibDecimal
from fractions import Fraction
from numbers import Integral, Rational
from typing import (
    Any, AnyStr, Callable, Dict, Generator, Iterator, List, MutableMapping,
    Optional, Tuple, Type, TypeVar, Union, cast, overload, )

from decimalfp import Decimal, ROUNDING, get_dflt_rounding_mode

from .converter import Converter, ConverterT, TableConverter
from .cwdmeta import ClassDefT, ClassWithDefinitionMeta, NonNumTermElem, Term
from .exceptions import (
    IncompatibleUnitsError, QuantityError, UndefinedResultError,
    UnitConversionError, )
from .rational import ONE
from .registry import DefinedItemRegistry
from .si_prefixes import SIPrefix
from .utils import sum
from .version import version_tuple as __version__  # noqa: F401

# Public interface
__all__ = [
    'Converter',
    'IncompatibleUnitsError',
    'Quantity',
    'QuantityError',
    'TableConverter',
    'UndefinedResultError',
    'UnitConversionError',
    'sum',
    ]

# Generic types
T = TypeVar("T")
CmpOpT = Callable[[T, T], bool]
BinOpT = Callable[[T, T], T]

# Parameterized types
UnitDefT = Term['Unit']
UnitRegistryT = DefinedItemRegistry['Unit']
QuantityClsDefT = Term['QuantityMeta']

# Cache for results of operations on unit definitions
BinOpResT = Union['Quantity', Rational]
_UNIT_OP_CACHE: MutableMapping[Tuple[BinOpT, Unit, Unit], BinOpResT] = {}

# Global registry of units
# [symbol -> unit] map, used to ensure that instances of Unit are singletons
_SYMBOL_UNIT_MAP: MutableMapping[str, Unit] = {}
# [term -> unit] map
_TERM_UNIT_MAP = UnitRegistryT(unique_items=False)


def _unit_from_symbol(symbol: str) -> Unit:
    return _SYMBOL_UNIT_MAP[symbol]


def _unit_from_term(term: UnitDefT) -> Unit:
    return _TERM_UNIT_MAP[term]


# defined here in order to reduce pickle foot-print
# def r(q_repr: str) -> Quantity:
#     """Reconstruct quantity from string representation."""
#     return Quantity(q_repr)


class Unit:
    """Unit of measure"""

    __slots__ = ['_symbol', '_name', '_equiv', '_definition', '_qty_cls']

    def __init__(self, symbol: str, name: Optional[str] = None,
                 define_as: Optional[Union[Quantity, UnitDefT]] = None):
        self._qty_cls: QuantityMeta
        self._equiv: Rational
        if isinstance(define_as, Quantity):
            definition = UnitDefT([(define_as.amount, 1),
                                   (define_as.unit, 1)])
            self._definition = definition
            self._equiv = definition.normalized().num_elem or ONE
        elif isinstance(define_as, Term):
            self._definition = define_as
            self._equiv = ONE
        assert symbol, "A symbol must be given for the unit."
        try:
            _SYMBOL_UNIT_MAP[symbol]
        except KeyError:
            _SYMBOL_UNIT_MAP[symbol] = self
        else:
            raise ValueError(
                f"Unit with symbol '{symbol}' already registered.")
        self._symbol = symbol
        self._name = name
        # UnitRegistryT has unique_items=False, so this will not raise an
        # exception!
        _TERM_UNIT_MAP.register_item(self)

    @property
    def symbol(self) -> str:
        """Return `self`s symbol.

        The symbol is a unique string representation of the unit.
        """
        return self._symbol

    @property
    def name(self) -> str:
        """Return `self`s name.

        If the unit was not given a name, its symbol is returned.
        """
        return self._name or self._symbol

    @property
    def definition(self) -> UnitDefT:
        """Return the definition of `self`."""
        try:
            return self._definition
        except AttributeError:
            return UnitDefT(((self, 1),))

    @property
    def normalized_definition(self) -> UnitDefT:
        """Return the normalized definition of `self`."""
        try:
            return self._definition.normalized()
        except AttributeError:
            return UnitDefT(((self, 1),))

    def is_base_unit(self) -> bool:
        """Return True if `self` is not derived from another unit."""
        try:
            self._definition
        except AttributeError:
            return True
        else:
            return False

    def is_derived_unit(self) -> bool:
        """Return True if `self` is derived from another unit."""
        return not self.is_base_unit()

    def is_ref_unit(self) -> bool:
        """Return True if `self` is a reference unit."""
        try:
            return self is self._qty_cls.ref_unit
        except AttributeError:
            return False

    @property
    def qty_cls(self) -> Optional[QuantityMeta]:
        """Return the `Quantity` subclass related to `self`."""
        try:
            return self._qty_cls
        except AttributeError:
            return None

    @property
    def quantum(self) -> Optional[Rational]:
        """Return the minimum amount of a quantity with unit `self`.

        Returns None if the quantity class related to `self` does not define a
        quantum.
        """
        cls = self.qty_cls
        if cls is None or cls.quantum is None:
            return None
        # cls.quantum not None => cls.ref_unit not None => self._equiv not None
        assert self._equiv is not None
        return cls.quantum / self._equiv

    def __hash__(self) -> int:
        """hash(self)"""
        return hash(self.symbol)

    def __copy__(self) -> Unit:
        """Return self (:class:`Unit` instances are immutable)."""
        return self

    def __deepcopy__(self, memo: Any) -> Unit:
        return self.__copy__()

    def __eq__(self, other: Any) -> bool:
        """self == other"""
        # Unit instances are singletons!
        return self is other

    def _compare(self, other: Any, op: CmpOpT) -> bool:
        """Compare self and other using operator op."""
        if isinstance(other, Unit):
            if self.qty_cls is other.qty_cls:
                factor = self._get_factor(other)
                if factor is None:
                    raise UnitConversionError("Can't convert '%s' to '%s'.",
                                              self, other)
                else:
                    return op(factor, ONE)
            msg = "Can't compare a '%s' unit and a '%s' unit."
            raise IncompatibleUnitsError(msg, self.qty_cls, other.qty_cls)
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        """self < other"""
        return self._compare(other, operator.lt)

    def __le__(self, other: Any) -> bool:
        """self <= other"""
        return self._compare(other, operator.le)

    def __gt__(self, other: Any) -> bool:
        """self > other"""
        return self._compare(other, operator.gt)

    def __ge__(self, other: Any) -> bool:
        """self >= other"""
        return self._compare(other, operator.ge)

    @overload
    def __mul__(self, other: Rational) -> Quantity:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: SIPrefix) -> Quantity:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: Unit) -> BinOpResT:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: Quantity) -> BinOpResT:  # noqa: D105
        ...

    def __mul__(self, other: Any, _op_cache = _UNIT_OP_CACHE) -> BinOpResT:
        """self * other"""
        if isinstance(other, Rational):
            return self._qty_cls(other, self)
        if isinstance(other, SIPrefix):
            return self._qty_cls(other.factor, self)
        if isinstance(other, Unit):
            try:  # try cache
                return _op_cache[(operator.mul, self, other)]
            except KeyError:
                pass
            # no cache hit
            res_def = UnitDefT(((self, 1), (other, 1)))
            try:
                res = _qty_from_term(res_def)
            except KeyError:
                raise UndefinedResultError(operator.mul,
                                           self.name, other.name) from None
            # cache it
            _op_cache[(operator.mul, self, other)] = res
            return res
        if isinstance(other, Quantity):
            return other.amount * (self * other.unit)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    @overload
    def __truediv__(self, other: Rational) -> Quantity:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Unit) -> BinOpResT:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Quantity) -> BinOpResT:  # noqa: D105
        ...

    def __truediv__(self, other: Any, _op_cache = _UNIT_OP_CACHE) -> BinOpResT:
        """self / other"""
        if isinstance(other, Rational):
            return self._qty_cls(ONE / other, self)
        if isinstance(other, Unit):
            try:  # try cache
                return _op_cache[(operator.truediv, self, other)]
            except KeyError:
                pass
            # no cache hit
            if self.qty_cls is other.qty_cls:
                try:
                    res = self._equiv / other._equiv
                except AttributeError:
                    raise UndefinedResultError(operator.truediv,
                                               self.name, other.name) \
                        from None
            else:
                res_def = UnitDefT(((self, 1), (other, -1)))
                try:
                    res = _qty_from_term(res_def)
                except KeyError:
                    raise UndefinedResultError(operator.truediv,
                                               self.name, other.name) \
                        from None
            # cache it
            _op_cache[(operator.truediv, self, other)] = res
            return res
        if isinstance(other, Quantity):
            return other.amount * (self / other.unit)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> Quantity:
        """other / self"""
        if isinstance(other, Rational):
            return other * self ** -1
        return NotImplemented

    def __pow__(self, exp: Any) -> Quantity:
        """self ** exp"""
        if isinstance(exp, int):
            if exp == 1:
                return self._qty_cls(1, self)
            res_def = UnitDefT(((self, exp),))
            try:
                return _qty_from_term(res_def)  # type: ignore
            except KeyError:
                raise UndefinedResultError(operator.pow, self.name, exp) \
                    from None
        return NotImplemented

    def __repr__(self) -> str:
        """repr(self)"""
        return f"Unit({self.symbol!r})"

    def __str__(self) -> str:
        """str(self)"""
        return f"{self.symbol}"

    # implement abstract methods of NonNumTermElem to allow instances of
    # Unit to be elements in terms:

    is_base_elem = is_base_unit

    def norm_sort_key(self) -> int:
        """Return sort key for `self` used for normalization of terms."""
        return self._qty_cls.norm_sort_key()

    def _get_factor(self, other: NonNumTermElem) -> Optional[Rational]:
        """Return scaling factor f so that f * `other` == 1 * `self`."""
        if isinstance(other, Unit):
            if self.qty_cls is other.qty_cls:
                try:
                    return self._equiv / other._equiv
                except AttributeError:
                    return None
        raise TypeError(f"Can't compare a unit to a '{type(other)}'.")


class QuantityMeta(ClassWithDefinitionMeta):
    """Meta class allowing to construct Quantity subclasses."""

    # Registry of Quantity classes (by normalized definition)
    _registry = DefinedItemRegistry['QuantityMeta']()

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _definition: Optional[ClassDefT]
    _ref_unit: Optional[Unit]
    _quantum: Rational

    def __new__(mcs, name: str, bases: Tuple[type, ...],  # noqa: N804
                clsdict: Dict[str, Any], **kwds: Any) -> QuantityMeta:
        """Create new Quantity (sub-)class."""
        cls: QuantityMeta
        ref_unit_def: Optional[UnitDefT] = None
        # optional definition
        define_as: Optional[QuantityClsDefT] = kwds.pop('define_as', None)
        # reference unit
        if define_as is not None:
            assert define_as, "Given definition is not valid."
            try:
                ref_unit_def = UnitDefT(_iter_ref_units(define_as))
            except TypeError:
                pass
        ref_unit_symbol = kwds.pop('ref_unit_symbol', None)
        if not ref_unit_symbol and ref_unit_def is not None:
            ref_unit_symbol = str(ref_unit_def)
        ref_unit_name = kwds.pop('ref_unit_name', None)
        # quantum
        quantum: Rational = kwds.pop('quantum', None)
        assert len(kwds) == 0, f"Unknown kwd(s): {kwds.keys()}"
        assert ref_unit_symbol if ref_unit_name else True, \
            "If `ref_unit_name` is given, `ref_unit_symbol` must also be " \
            "given."
        assert quantum is None or ref_unit_symbol, \
            "A quantum can only be defined together with a reference unit."
        # prevent __dict__ from being built for subclasses of Quantity
        try:
            clsdict['__slots__']
        except KeyError:
            clsdict['__slots__'] = ()
        cls = cast(QuantityMeta,
                   super().__new__(mcs, name, bases, clsdict,
                                   define_as=cast(ClassDefT, define_as)))
        if ref_unit_symbol:
            cls._make_ref_unit(ref_unit_symbol, ref_unit_name, ref_unit_def)
        else:
            cls._ref_unit = None
        cls._quantum = quantum
        return cls

    def __init__(cls, name: str, bases: Tuple[type, ...],  # noqa: N805
                 clsdict: Dict[str, Any], **kwds: Any):
        super().__init__(name, bases, clsdict)
        # register cls
        cls._reg_id = QuantityMeta._registry.register_item(cls)
        # map of units associated with Quantity class
        unit = cls._ref_unit
        if unit is None:
            cls._unit_map: Dict[str, Unit] = {}
        else:
            cls._unit_map = {unit.symbol: unit}
        # converter registry
        cls._converters: List[ConverterT] = []

    def _make_ref_unit(cls, symbol: str, name: str,  # noqa: N805
                       define_as: Optional[UnitDefT]) -> None:
        unit = Unit(symbol, name, define_as)
        unit._qty_cls = cls
        unit._equiv = ONE
        cls._ref_unit = unit

    @property
    def ref_unit(cls) -> Optional[Unit]:  # noqa: N805
        """Return the reference unit of `cls`, or None if no one is defined."""
        return cls._ref_unit

    @property
    def quantum(cls) -> Optional[Rational]:  # noqa: N805
        """Return the minumum amount for an instance of `cls`.

        The quantum is the minimum amount (in terms of the reference unit) an
        instance of `cls` can take (None no quantum is defined).
        """
        return cls._quantum

    def new_unit(cls, symbol: str, name: Optional[str],  # noqa: N805
                 define_as: Optional[Quantity] = None) -> Unit:
        """Create, register and return a new unit for `cls`."""
        if define_as is None:
            unit = Unit(symbol, name)
        else:
            assert isinstance(define_as, cls)
            unit = Unit(symbol, name, define_as)
        unit._qty_cls = cls
        cls._unit_map[unit.symbol] = unit
        return unit

    def units(cls) -> Tuple[Unit, ...]:  # noqa: N805
        """Return all registered units of `cls` as tuple."""
        return tuple(cls._unit_map.values())

    def register_converter(cls, conv: ConverterT) -> None:  # noqa: N805
        """Add converter `conv` to the list of converters registered in cls.

        Does nothing if converter is already registered.
        """
        if conv not in cls._converters:
            cls._converters.append(conv)

    def remove_converter(cls, conv: ConverterT) -> None:  # noqa: N805
        """Remove converter `conv` from the converters registered in cls.

        Raises ValueError if the converter is not present.
        """
        cls._converters.remove(conv)

    def registered_converters(cls) -> Iterator[ConverterT]:  # noqa: N805
        """Return an iterator over the converters registered in 'cls'.

        The converts are returned in reversed order of registration.
        """
        return reversed(cls._converters)

    def norm_sort_key(cls) -> int:  # noqa: N805
        """Return sort key for `cls` used for normalization of terms."""
        return cls._reg_id


class Quantity(metaclass=QuantityMeta):
    """Base class used to define types of quantities."""

    __slots__ = ['_amount', '_unit']

    # default format spec used in __format__
    dflt_format_spec = '{a} {u}'

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _amount: Union[Decimal, Fraction]
    _unit: Unit

    def __new__(cls, amount: Union[Rational, StdLibDecimal, AnyStr],
                unit: Optional[Unit] = None) -> Quantity:
        """Create new Quantity instance."""
        amnt: Rational
        if isinstance(amount, (Decimal, Fraction)):
            amnt = amount
        elif isinstance(amount, (Integral, StdLibDecimal)):
            amnt = Decimal(amount)  # convert to decimalfp.Decimal
        elif isinstance(amount, float):
            try:
                amnt = Decimal(amount)
            except ValueError:
                amnt = Fraction(amount)
        elif isinstance(amount, (str, bytes)):
            if isinstance(amount, bytes):
                try:
                    q_repr = amount.decode()
                except UnicodeError:
                    raise QuantityError("Can't decode given bytes using "
                                        "default encoding.")
            else:
                q_repr = amount
            parts = q_repr.lstrip().split(' ', 1)
            s_amount = parts[0]
            try:
                amnt = Decimal(s_amount)
            except (TypeError, ValueError):
                try:
                    amnt = Fraction(s_amount)
                except (TypeError, ValueError):
                    raise QuantityError(f"Can't convert '{s_amount}' to a "
                                        "rational number.")
            if len(parts) > 1:
                s_sym = parts[1].strip()
                try:
                    unit_from_sym = _unit_from_symbol(s_sym)
                except KeyError:
                    raise QuantityError(f"Unknown symbol '{s_sym}'.") \
                        from None
                else:
                    if unit is None:
                        unit = unit_from_sym
                    elif unit is unit_from_sym:
                        pass
                    else:
                        assert unit_from_sym.qty_cls is not None
                        qty = unit_from_sym.qty_cls(amnt, unit_from_sym)
                        return qty.convert(unit)
        else:
            raise TypeError("Given amount must be a number or a string "
                            "that can be converted to a number.")
        if unit is None:
            unit = cls.ref_unit
            if unit is None:
                raise QuantityError("A unit must be given.")
        elif not isinstance(unit, Unit):
            raise TypeError("Instance of 'Unit' expected as 'unit', got: "
                            f"{unit!r}.")
        if cls is Quantity:
            cls = cast(Type[Quantity], unit.qty_cls)
            if cls is None:
                raise TypeError(f"'{unit}' is nor a registered unit.")
        elif cls is not unit.qty_cls:
            raise QuantityError(f"Given unit '{unit}' is not a "
                                f"'{cls.__name__}' unit.")
        # make raw instance
        qty = super().__new__(cls)
        # check whether it should be quantized
        quantum = unit.quantum
        if quantum is not None:
            amnt = Decimal(amnt / quantum, 0) * quantum
        # finally set amount and unit
        qty._amount = amnt
        qty._unit = unit
        return qty

    @property
    def amount(self) -> Rational:
        """Return `self`s amount, i.e. the numerical part of the quantity."""
        return self._amount

    @property
    def unit(self) -> Unit:
        """Return `self`s unit."""
        return self._unit

    def equiv_amount(self, unit: Unit) -> Optional[Rational]:
        """Return amount e so that e * `unit` == `self`."""
        try:
            # noinspection PyProtectedMember
            factor = self.unit._get_factor(unit)
        except TypeError:
            if isinstance(unit, Unit):
                msg = "Can't convert a '%s' unit to a '%s' unit."
                raise IncompatibleUnitsError(msg, self.__class__,
                                             unit.qty_cls) from None
            else:
                raise
        else:
            if factor is None:
                # try registered converters:
                for conv in self.__class__.registered_converters():
                    try:
                        return conv(self, unit)
                    except UnitConversionError:
                        pass
                return None
            else:
                return factor * self.amount

    def convert(self, to_unit: Unit) -> Quantity:
        """Return quantity q where q == `self` and q.unit is `to_unit`.

        Args:
            to_unit (Unit): unit to be converted to

        Returns:
            type(self): resulting quantity

        Raises:
            IncompatibleUnitsError: `self` can't be converted to `to_unit`.
        """
        equiv_amount = self.equiv_amount(to_unit)
        if equiv_amount is None:
            raise UnitConversionError("Can't convert '%s' to '%s'.",
                                      self.unit, to_unit)
        return equiv_amount * to_unit

    def quantize(self, quant: Quantity,
                 rounding: Optional[ROUNDING] = None) -> Quantity:
        """Return integer multiple of `quant` closest to `self`.

        Args:
            quant (type(self)): quantum to get a multiple from
            rounding (ROUNDING): rounding mode (default: None)

        If no `rounding` mode is given, the current default mode from
        module `decimalfp` is used.

        Returns:
            type(self) instance that is the integer multiple of `quant` closest
                to `self` (according to `rounding` mode)

        Raises:
            IncompatibleUnitsError: `quant` can not be converted to self.unit
            TypeError: `quant` is not an instance of type(self)
            TypeError: type(self) has no reference unit
        """
        cls = self.__class__
        if quant.__class__ is not cls:
            raise TypeError(f"Expected a '{type(self)}' as 'quant', got a "
                            f"'{type(quant)}'.")
        if cls.ref_unit is None:
            raise TypeError(f"Can't quantize a quantity without reference "
                            f"unit: {cls.__name__}")
        num_quant = quant.equiv_amount(self.unit)
        if num_quant is None:
            raise UnitConversionError("Can't convert '%s' to '%s'.",
                                      quant.unit, self.unit)
        amnt = self.amount
        if amnt == 0:
            return self
        if isinstance(amnt, Decimal):
            res_amnt = amnt.quantize(num_quant, rounding=rounding)
        elif isinstance(amnt, Fraction):
            res_amnt = _quantize_fraction(amnt, num_quant, rounding)
        else:
            raise QuantityError
        return cls(res_amnt, self.unit)

    @overload
    def __mul__(self, other: Rational) -> Quantity:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: Quantity) -> BinOpResT:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: Unit) -> BinOpResT:  # noqa: D105
        ...

    def __mul__(self, other: Any) -> BinOpResT:
        """self * other"""
        if isinstance(other, Rational):
            return self.__class__(self.amount * other, self.unit)
        if isinstance(other, Quantity):
            return (self.amount * other.amount) * (self.unit * other.unit)
        if isinstance(other, Unit):
            return self.amount * (self.unit * other)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    @overload
    def __truediv__(self, other: Rational) -> Quantity:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Quantity) -> BinOpResT:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Unit) -> BinOpResT:  # noqa: D105
        ...

    def __truediv__(self, other: Any) -> BinOpResT:
        """self / other"""
        if isinstance(other, Rational):
            return self.__class__(self.amount / other, self.unit)
        if isinstance(other, Quantity):
            if self.__class__ is other.__class__:
                equiv_amount = other.equiv_amount(self.unit)
                if equiv_amount is None:
                    raise UnitConversionError("Can't convert '%s' to '%s'.",
                                              other.unit, self.unit)
                else:
                    return self.amount / equiv_amount
            else:
                return (self.amount / other.amount) * (self.unit / other.unit)
        if isinstance(other, Unit):
            if self.__class__ is other.qty_cls:
                equiv_amount = self.equiv_amount(other)
                if equiv_amount is None:
                    raise UnitConversionError("Can't convert '%s' to '%s'.",
                                              self.unit, other)
                else:
                    return equiv_amount
            else:
                return self.amount * (self.unit / other)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> Quantity:
        """other / self"""
        if isinstance(other, Rational):
            return (other / self.amount) * self.unit ** -1
        return NotImplemented

    def __pow__(self, exp: Any) -> BinOpResT:
        """self ** exp"""
        if not isinstance(exp, int):
            return NotImplemented
        return self.amount ** exp * self.unit ** exp

    def __round__(self, n_digits: int = 0) -> Quantity:
        """Return copy of `self` with its amount rounded to `n_digits`.

        Args:
            n_digits (`Integral`): number of fractional digits to be rounded
                to

        Returns:
            type(self): round(self.amount, n_digits) * self.unit
        """
        return self.__class__(round(self.amount, n_digits), self.unit)

    def __repr__(self) -> str:
        """repr(self)"""
        cls = self.__class__
        if self.unit is cls.ref_unit:
            return f"{cls.__name__}({self.amount!r})"
        else:
            return f"{cls.__name__}({self.amount!r}, {self.unit!r})"

    def __str__(self) -> str:
        """str(self)"""
        return f"{self.amount} {self.unit}"


# helper functions

def _iter_ref_units(cls_def: QuantityClsDefT) \
        -> Generator[Tuple[Unit, int], None, None]:
    for qty_cls, exp in cls_def:
        if isinstance(qty_cls, QuantityMeta):
            ref_unit = qty_cls.ref_unit
            if ref_unit is not None:
                yield ref_unit, exp
            else:
                raise TypeError


def _qty_from_term(term: UnitDefT) -> BinOpResT:
    num: Rational = ONE
    try:
        res_unit = _unit_from_term(term)
    except KeyError:
        num, res_def = term.normalized().split()
        if not res_def:  # empty term
            return num
        elif res_def != term:
            res_unit = _unit_from_term(res_def)
        else:
            raise
    qty_cls = res_unit.qty_cls
    assert qty_cls is not None
    return qty_cls(num, res_unit)


def _floordiv_rounded(x: int, y: int,
                      rounding: Optional[ROUNDING] = None) -> int:
    # Return x // y, rounded using given rounding mode (or default mode
    # if none is given)
    quot, rem = divmod(x, y)
    if rem == 0:  # no need for rounding
        return quot
    else:
        if rounding is None:
            rounding = get_dflt_rounding_mode()
        if rounding == ROUNDING.ROUND_HALF_UP:
            # Round 5 up (away from 0)
            # |remainder| > |divisor|/2 or
            # |remainder| = |divisor|/2 and quotient >= 0
            # => add 1
            ar, ay = abs(2 * rem), abs(y)
            if ar > ay or (ar == ay and quot >= 0):
                return quot + 1
            else:
                return quot
        elif rounding == ROUNDING.ROUND_HALF_EVEN:
            # Round 5 to even, rest to nearest
            # |remainder| > |divisor|/2 or
            # |remainder| = |divisor|/2 and quotient not even
            # => add 1
            ar, ay = abs(2 * rem), abs(y)
            if ar > ay or (ar == ay and quot % 2 != 0):
                return quot + 1
            else:
                return quot
        elif rounding == ROUNDING.ROUND_HALF_DOWN:
            # Round 5 down
            # |remainder| > |divisor|/2 or
            # |remainder| = |divisor|/2 and quotient < 0
            # => add 1
            ar, ay = abs(2 * rem), abs(y)
            if ar > ay or (ar == ay and quot < 0):
                return quot + 1
            else:
                return quot
        elif rounding == ROUNDING.ROUND_DOWN:
            # Round towards 0 (aka truncate)
            # quotient negativ
            # => add 1
            if quot < 0:
                return quot + 1
            else:
                return quot
        elif rounding == ROUNDING.ROUND_UP:
            # Round away from 0
            # quotient not negativ
            # => add 1
            if quot >= 0:
                return quot + 1
            else:
                return quot
        elif rounding == ROUNDING.ROUND_CEILING:
            # Round up (not away from 0 if negative)
            # => always add 1
            return quot + 1
        elif rounding == ROUNDING.ROUND_FLOOR:
            # Round down (not towards 0 if negative)
            # => never add 1
            return quot
        elif rounding == ROUNDING.ROUND_05UP:
            # Round down unless last digit is 0 or 5
            # quotient not negativ and
            # quotient divisible by 5 without remainder or
            # quotient negativ and
            # (quotient + 1) not divisible by 5 without remainder
            # => add 1
            if (quot >= 0 and quot % 5 == 0 or
                    quot < 0 and (quot + 1) % 5 != 0):
                return quot + 1
            else:
                return quot
    raise ValueError(f"Invalid rounding mode: {rounding!r}.")


def _quantize_fraction(self: Fraction, quant: Rational,
                       rounding: Optional[ROUNDING] = None) -> Fraction:
    """Return integer multiple of `quant` closest to `self`."""
    quot: Fraction = self / quant
    mult = _floordiv_rounded(quot.numerator, quot.denominator,
                             rounding=rounding)
    return mult * quant
