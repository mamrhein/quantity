# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright:   (c) 2012 ff. Michael Amrhein (michael@adrhinum.de)
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$

# mypy: no-warn-return-any

# TODO: update doc
r"""Unit-safe computations with quantities.

Usage
=====

.. _defining_a_qty_label:

Defining a quantity class
-------------------------

A **basic** type of quantity is declared just by sub-classing
:class:`Quantity`:

    >>> class Length(Quantity):                             # doctest: +SKIP
    ...     pass
    ...

But, as long as there is no unit defined for that class, you can not create
any instance for the new quantity class:

    >>> l = Length(1)                                       # doctest: +SKIP
    Traceback (most recent call last):
    ValueError: A unit must be given.

If there is a reference unit, the simplest way to define it is giving a name
and a symbol for it as keywords. The meta-class of :class:`Quantity` will
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

Other units have to be defined explicitly.

In order to define a **quantized** quantity, the smallest possible fraction
(in terms of the reference unit) can be given as `quantum`:

    >>> class DataVolume(Quantity,
    ...                  ref_unit_name='Byte',
    ...                  ref_unit_symbol='B',
    ...                  quantum=Decimal('0.125')):
    ...     pass
    ...
    >>> DataVolume.quantum
    Decimal('0.125')

The method `quantum` can then be used to retrieve the smallest amount for a
unit:

    >>> BYTE = DataVolume.ref_unit
    >>> BYTE.quantum
    Decimal('0.125')
    >>> KILOBYTE = DataVolume.new_unit('kB', 'Kilobyte', KILO * BYTE)
    >>> KILOBYTE.quantum
    Decimal('0.000125')

Instantiating quantities
------------------------

The simplest way to create an instance of a :class:`Quantity` subclass is to
call the class giving an amount and a unit. If the unit is omitted, the
quantity's reference unit is used (if one is defined):

    >>> Length(15, MILLIMETRE)
    Length(Decimal(15), Unit('mm'))
    >>> Length(15)
    Length(Decimal(15))

Alternatively, an amount and a unit can be multiplied:

    >>> 17.5 * KILOMETRE
    Length(Decimal('17.5'), Unit('km'))

Also, it's possible to create a :class:`Quantity` instance from a string
representation:

    >>> Length('17.5 km')
    Length(Decimal('17.5'), Unit('km'))

If a unit is given in addition, the resulting quantity is converted
accordingly:

    >>> Length('17 m', KILOMETRE)
    Length(Decimal('0.017'), Unit('km'))

Instead of calling a subclass, the class :class:`Quantity` can be used as a
factory function …:

    >>> Quantity(15, MILLIMETRE)
    Length(Decimal(15), Unit('mm'))
    >>> Quantity('17.5 km')
    Length(Decimal('17.5'), Unit('km'))

… as long as a unit is given:

    >>> Quantity(17.5)
    Traceback (most recent call last):
    QuantityError: A unit must be given.

If the :class:`Quantity` subclass defines a `quantum`, the amount of each
instance is automatically rounded to this quantum:

    >>> DataVolume('1/7', KILOBYTE)
    DataVolume(Decimal('0.142875'), Unit('kB'))

Converting between units
------------------------

A quantity can be converted to a quantity using a different unit by calling
the method :meth:`Quantity.convert`:

    >>> l5cm = Length(Decimal(5), CENTIMETRE)
    >>> l5cm.convert(MILLIMETRE)
    Length(Decimal(50), Unit('mm'))
    >>> l5cm.convert(KILOMETRE)
    Length(Decimal('0.00005'), Unit('km'))

These kinds of conversion are automatically enabled for types of quantities
with reference units. For other types of quantities there is no default way
of converting between units.

    >>> t27c = Temperature(Decimal(27), CELSIUS)
    >>> t27c.convert(FAHRENHEIT)
    Traceback (most recent call last):
    UnitConversionError: Can't convert '°C' to '°F'.

.. _converters_label:

Converters
^^^^^^^^^^

For types of quantities that do not have a reference unit, one or more
callables can be registered as converters:

    >>> def fahrenheit2celsius(qty, to_unit):
    ...     if qty.unit is FAHRENHEIT and to_unit is CELSIUS:
    ...         return (qty.amount - 32) / Decimal('1.8')
    ...     return None
    ...
    >>> def celsius2fahrenheit(qty, to_unit):
    ...     if qty.unit is CELSIUS and to_unit is FAHRENHEIT:
    ...         return qty.amount * Decimal('1.8') + 32
    ...     return None
    ...
    >>> Temperature.register_converter(fahrenheit2celsius)
    >>> Temperature.register_converter(celsius2fahrenheit)
    >>> assert list(Temperature.registered_converters()) == \
    ...     [celsius2fahrenheit, fahrenheit2celsius]
    ...

For the signature of the callables used as converters see :class:`Converter`.

    >>> t27c.convert(FAHRENHEIT)
    Temperature(Decimal('80.6'), Unit('°F'))
    >>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
    Temperature(Decimal(27), Unit('°C'))

Alternatively, an instance of :class:`TableConverter` can be created and
registered as converter.

The example given above can be implemented as follows:

    >>> tconv = TableConverter({(CELSIUS, FAHRENHEIT): (Decimal('1.8'), 32)})
    >>> Temperature.register_converter(tconv)
    >>> t27c = Temperature(Decimal(27), CELSIUS)
    >>> t27c.convert(FAHRENHEIT)
    Temperature(Decimal('80.6'), Unit('°F'))

It is suffient to define the conversion in one direction, because a
reversed conversion is used automatically:

    >>> t27c.convert(FAHRENHEIT).convert(CELSIUS)
    Temperature(Decimal(27), Unit('°C'))

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
    Traceback (most recent call last):
    UnitConversionError: Can't convert 'K' to '°C'.

Testing instances of different quantity types for equality always returns
false:

    >>> Length(20) == Duration(20)
    False
    >>> Length(20) != Duration(20)
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
    Traceback (most recent call last):
    IncompatibleUnitsError: Can't add a 'Length' and a 'Duration'

When quantities with different units are added or subtracted, the values are
converted to the unit of the first, if possible …:

    >>> Length(27) + Length(12, CENTIMETRE)
    Length(Decimal('27.12'))
    >>> Length(12, CENTIMETRE) + Length(17, METRE)
    Length(Decimal(1712), Unit('cm'))
    >>> Temperature(20, CELSIUS) - Temperature(50, FAHRENHEIT)
    Temperature(Decimal(10), Unit('°C'))

… but an exception is raised, if not:

    >>> Temperature(20, CELSIUS) - Temperature(281, KELVIN)
    Traceback (most recent call last):
    UnitConversionError: Can't convert 'K' to '°C'.

Multiplication and division
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Quantities can be multiplied or divided by scalars, preserving the unit:

    >>> 7.5 * Length(3, CENTIMETRE)
    Length(Decimal('22.5'), Unit('cm'))
    >>> SECOND = Duration.ref_unit
    >>> MINUTE = Duration.new_unit('min', 'Minute', Decimal(60) * SECOND)
    >>> Duration(66, MINUTE) / 11
    Duration(Decimal(6), Unit('min'))

Quantities can be multiplied or divided by other quantities …:

    >>> Length(15, METRE) / Duration(3, SECOND)
    Velocity(Decimal(5))

… as long as the resulting type of quantity is defined …:

    >>> Duration(4, SECOND) * Length(7)
    Traceback (most recent call last):
    UndefinedResultError: Undefined result: Duration * Length
    >>> Length(12, KILOMETRE) / Duration(2, MINUTE) / Duration(50, SECOND)
    Traceback (most recent call last):
    UndefinedResultError: Undefined result: Velocity / Duration
    >>> class Acceleration(Quantity,
    ...                    define_as=Length / Duration ** 2,
    ...                    ref_unit_name='Metre per Second squared'):
    ...     pass
    ...
    >>> Length(12, KILOMETRE) / Duration(2, MINUTE) / Duration(50, SECOND)
    Acceleration(Decimal(2))

… or the result is a scalar:

    >>> Duration(2, MINUTE) / Duration(50, SECOND)
    Decimal('2.4')

When cascading operations, all intermediate results have to be defined:

    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    Traceback (most recent call last):
    UndefinedResultError: Undefined result: Length * Length
    >>> class Area(Quantity,
    ...            define_as=Length ** 2,
    ...            ref_unit_name='Square Metre'):
    ...     pass
    ...
    >>> Length(6, KILOMETRE) * Length(13,  METRE) * Length(250, METRE)
    Volume(Decimal(19500000))

Exponentiation
^^^^^^^^^^^^^^

Quantities can be raised by an exponent, as long as the exponent is an
`Integral` number and the resulting quantity is defined:

    >>> (5 * METRE) ** 2
    Area(Decimal(25))
    >>> (5 * METRE) ** 2.5
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for ** or pow(): 'Length' and
        'float'
    >>> (5 * METRE) ** -2
    Traceback (most recent call last):
    UndefinedResultError: Undefined result: Length ** -2

Rounding
--------

The amount of a quantity can be rounded by using the standard `round`
function. It returns a copy of the quanitity, with its amount rounded
accordingly:

    >>> round(Length(Decimal('17.375'), MILLIMETRE), 1)
    Length(Decimal('17.4'), Unit('mm'))

In any case the unit of the resulting quantity will be the same as the unit
of the called quantity.

For more advanced cases of rounding the method :meth:`Quantity.quantize` can
round a quantity to any quantum according to any rounding mode:

    >>> l = Length('1.7296 km')
    >>> l.quantize(Length(1))
    Length(Decimal('1.73', 3), Unit('km'))
    >>> l.quantize(25 * METRE)
    Length(Decimal('1.725'), Unit('km'))
    >>> l.quantize(25 * METRE, ROUNDING.ROUND_UP)
    Length(Decimal('1.75', 3), Unit('km'))

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
    Mass(Decimal(0, 2))

If the quantity is quantized, there can be rounding errors causing a remainder
with an amount other than 0:

    >>> b = 10 * KILOBYTE
    >>> portions, remainder = b.allocate(ratios, disperse_rounding_error=False)
    >>> portions
    [DataVolume(Decimal('6.333375'), Unit('kB')),
     DataVolume(Decimal('0.833375'), Unit('kB')),
     DataVolume(Decimal('0.333375'), Unit('kB')),
     DataVolume(Decimal('2.5', 6), Unit('kB'))]
    >>> remainder
    DataVolume(Decimal('-0.000125'), Unit('kB'))

By default the remainder will be dispersed:

    >>> portions, remainder = b.allocate(ratios)
    >>> portions
    [DataVolume(Decimal('6.333375'), Unit('kB')),
     DataVolume(Decimal('0.833375'), Unit('kB')),
     DataVolume(Decimal('0.33325', 6), Unit('kB')),
     DataVolume(Decimal('2.5', 6), Unit('kB'))]
    >>> remainder
    DataVolume(Decimal(0), Unit('kB'))

As well as of numbers, quantities can be used as ratios (as long as they have
compatible units):

    >>> CUBIC_METRE = Volume.ref_unit
    >>> LITRE = Volume.new_unit('l', 'Litre', MILLI * CUBIC_METRE)
    >>> l = 10 * LITRE
    >>> ratios = [350 * GRAM, 500 * GRAM, 3 * KILOGRAM, 150 * GRAM]
    >>> l.allocate(ratios)
    ([Volume(Decimal('0.875', 4), Unit('l')),
      Volume(Decimal('1.25', 3), Unit('l')),
      Volume(Decimal('7.5', 2), Unit('l')),
      Volume(Decimal('0.375', 4), Unit('l'))],
     Volume(Decimal(0, 4), Unit('l')))

Formatting as string
--------------------

:class:`Quantity` supports the standard `str` function. It returns a string
representation of the quantity's amount followed by a blank and the
quantity's units symbol.

In addition, :class:`Quantity` supports the standard `format` function. The
format specifier should use two keys: 'a' for the amount and 'u' for the unit,
where 'a' can be followed by a valid format spec for numbers and 'u' by a
valid format spec for strings. If no format specifier is given, '{a} {u}' is
used:

    >>> v = Volume('19.36')
    >>> format(v)
    '19.36 m³'
    >>> format(v, '{a:*>10.2f} {u:<3}')
    '*****19.36 m³ '
"""

from __future__ import annotations

import operator
from decimal import Decimal as StdLibDecimal
from fractions import Fraction
from numbers import Integral, Rational, Real
from typing import (
    Any, Callable, Collection, Dict, Generator, Iterator, List,
    MutableMapping, Optional, Tuple, Type, TypeVar, Union, overload,
    )

from decimalfp import Decimal, ONE, ROUNDING, get_dflt_rounding_mode

from .converter import Converter, TableConverter
from .cwdmeta import ClassDefT, ClassWithDefinitionMeta
from .exceptions import (
    IncompatibleUnitsError, QuantityError, UndefinedResultError,
    UnitConversionError,
    )
from .registry import DefinedItemRegistry
from .si_prefixes import SIPrefix
from .term import NonNumTermElem, Term
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
CmpOpT = Callable[[Any, Any], bool]
BinOpT = Callable[[Any, Any], Any]

# Parameterized types
UnitDefT = Term['Unit']
UnitRegistryT = DefinedItemRegistry['Unit']
QuantityClsDefT = Term['QuantityMeta']
ConverterT = Callable[['Quantity', 'Unit'], Optional[Rational]]

# Cache for results of operations on unit definitions
BinOpResT = Union['Quantity', Rational]
UnitOpCacheT = MutableMapping[Tuple[BinOpT, 'Unit', 'Unit'], BinOpResT]
_UNIT_OP_CACHE: UnitOpCacheT = {}

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

    __slots__ = ['_qty_cls', '_symbol', '_name', '_equiv', '_definition']

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _qty_cls: QuantityMeta
    _symbol: str
    _name: Optional[str]
    _equiv: Rational
    _definition: UnitDefT

    def __new__(cls, qty_cls: QuantityMeta, symbol: str,
                name: Optional[str] = None,
                define_as: Optional[Union[Quantity, UnitDefT]] = None,
                ref_unit: bool = False) -> Unit:
        self = super().__new__(cls)
        self._qty_cls = qty_cls
        if isinstance(define_as, Quantity):
            definition = UnitDefT([(define_as.amount, 1),
                                   (define_as.unit, 1)])
            self._definition = definition
            self._equiv = definition.normalized().num_elem or ONE
        elif isinstance(define_as, Term):
            self._definition = define_as
            self._equiv = define_as.normalized().num_elem or ONE
        else:
            assert define_as is None, "Unknown type of Unit definition."
            self._definition = None
            self._equiv = ONE if ref_unit else None
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
        return self

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
        return self._definition or UnitDefT(((self, 1),))

    @property
    def normalized_definition(self) -> UnitDefT:
        """Return the normalized definition of `self`."""
        definition = self._definition
        if definition is None:
            return UnitDefT(((self, 1),))
        return definition.normalized()

    def is_base_unit(self) -> bool:
        """Return True if `self` is not derived from another unit."""
        return self._definition is None

    def is_derived_unit(self) -> bool:
        """Return True if `self` is derived from another unit."""
        return self._definition is not None

    def is_ref_unit(self) -> bool:
        """Return True if `self` is a reference unit."""
        return self is self._qty_cls.ref_unit

    @property
    def qty_cls(self) -> QuantityMeta:
        """Return the `Quantity` subclass related to `self`."""
        return self._qty_cls

    @property
    def quantum(self) -> Optional[Rational]:
        """Return the minimum amount of a quantity with unit `self`.

        Returns None if the quantity class related to `self` does not define a
        quantum.
        """
        cls = self.qty_cls
        if cls.quantum is None:
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
                                              other, self)
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
    def __mul__(self, other: int) -> Quantity:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: float) -> Quantity:  # noqa: D105
        ...

    @overload
    def __mul__(self, other: Real) -> Quantity:  # noqa: D105
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

    def __mul__(self, other: Any, _op_cache: UnitOpCacheT = _UNIT_OP_CACHE) \
            -> BinOpResT:
        """self * other"""
        if isinstance(other, Rational):
            return self._qty_cls(other, self)
        if isinstance(other, Real):
            return self._qty_cls(Decimal(other), self)
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
                                           self._qty_cls.__name__,
                                           other._qty_cls.__name__,) \
                    from None
            # cache it
            _op_cache[(operator.mul, self, other)] = res
            return res
        if isinstance(other, Quantity):
            return other.amount * (self * other.unit)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    @overload
    def __truediv__(self, other: int) -> Quantity:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: float) -> Quantity:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Real) -> Quantity:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Unit) -> BinOpResT:  # noqa: D105
        ...

    @overload
    def __truediv__(self, other: Quantity) -> BinOpResT:  # noqa: D105
        ...

    def __truediv__(self, other: Any,
                    _op_cache: UnitOpCacheT = _UNIT_OP_CACHE) -> BinOpResT:
        """self / other"""
        if isinstance(other, Rational):
            return self._qty_cls(ONE / other, self)
        if isinstance(other, Real):
            return self._qty_cls(ONE / Decimal(other), self)
        if isinstance(other, Unit):
            try:  # try cache
                return _op_cache[(operator.truediv, self, other)]
            except KeyError:
                pass
            # no cache hit
            if self.qty_cls is other.qty_cls:
                try:
                    res: BinOpResT = self._equiv / other._equiv
                except AttributeError:
                    raise UndefinedResultError(operator.truediv,
                                               self._qty_cls.__name__,
                                               other._qty_cls.__name__) \
                        from None
            else:
                res_def = UnitDefT(((self, 1), (other, -1)))
                try:
                    res = _qty_from_term(res_def)
                except KeyError:
                    raise UndefinedResultError(operator.truediv,
                                               self._qty_cls.__name__,
                                               other._qty_cls.__name__) \
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
        if isinstance(other, Real):
            return Decimal(other) * self ** -1
        return NotImplemented

    def __pow__(self, exp: Any) -> Quantity:
        """self ** exp"""
        if isinstance(exp, int):
            if exp == 1:
                return self._qty_cls(ONE, self)
            res_def = UnitDefT(((self, exp),))
            try:
                return _qty_from_term(res_def)  # type: ignore
            except KeyError:
                raise UndefinedResultError(operator.pow,
                                           self._qty_cls.__name__, exp) \
                    from None
        return NotImplemented

    def __repr__(self) -> str:
        """repr(self)"""
        return f"Unit({self.symbol!r})"

    def __str__(self) -> str:
        """str(self)"""
        return f"{self.symbol}"

    def __format__(self, fmt_spec: str = "") -> str:
        """Convert to string (according to `fmt_spec`).

        `fmt_spec` must be a valid format spec for strings.
        """
        return format(self.symbol, fmt_spec)

    # implement abstract methods of NonNumTermElem to allow instances of
    # Unit to be elements in terms:

    is_base_elem = is_base_unit

    def norm_sort_key(self) -> int:
        """Return sort key for `self` used for normalization of terms."""
        return self._qty_cls.norm_sort_key()

    def _get_factor(self, other: NonNumTermElem) -> Optional[Rational]:
        """Return scaling factor f so that f * `other` == 1 * `self`."""
        qty_cls = self._qty_cls
        if isinstance(other, Unit):
            if self.qty_cls is other.qty_cls:
                if qty_cls.ref_unit is None:
                    return None
                return self._equiv / other._equiv
        raise TypeError(f"Can't compare a unit to a '{type(other)}'.")


class QuantityMeta(ClassWithDefinitionMeta):
    """Meta class allowing to construct Quantity subclasses."""

    # Registry of Quantity classes (by normalized definition)
    _registry = DefinedItemRegistry['QuantityMeta']()

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _definition: Optional[ClassDefT]
    _unit_cls: Type[Unit]
    _ref_unit: Optional[Unit]
    _quantum: Rational

    def __new__(mcs, name: str, bases: Tuple[type, ...],  # noqa: N804
                clsdict: Dict[str, Any], **kwds: Any) -> QuantityMeta:
        """Create new Quantity (sub-)class."""
        ref_unit_def: Optional[UnitDefT] = None
        # optional definition
        define_as: Optional[QuantityClsDefT] = kwds.pop('define_as', None)
        # reference unit
        if define_as is not None:   # empty Term
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
        # default unit class
        try:
            clsdict['_unit_cls']
        except KeyError:
            clsdict['_unit_cls'] = Unit
        # prevent __dict__ from being built for subclasses of Quantity
        try:
            clsdict['__slots__']
        except KeyError:
            clsdict['__slots__'] = ()
        cls = super().__new__(mcs, name, bases, clsdict,
                              define_as=define_as)
        assert isinstance(cls, QuantityMeta)
        if ref_unit_symbol:
            cls._make_ref_unit(ref_unit_symbol, ref_unit_name, ref_unit_def)
        else:
            cls._ref_unit = None
        cls._quantum = quantum
        return cls

    # noinspection PyUnusedLocal
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
        unit_cls = cls._unit_cls
        cls._ref_unit = unit_cls(cls, symbol, name=name, define_as=define_as,
                                 ref_unit=True)

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

    def new_unit(cls, symbol: str, name: Optional[str] = None,  # noqa: N805
                 define_as: Optional[Union[Quantity, UnitDefT]] = None, *,
                 derive_from: Optional[Union[Unit, Tuple[Unit, ...]]] = None) \
            -> Unit:
        """Create, register and return a new unit for `cls`."""
        unit_cls = cls._unit_cls
        if derive_from is None:
            if define_as is None:
                unit = unit_cls(cls, symbol, name=name)
            elif isinstance(define_as, Quantity):
                if not isinstance(define_as, cls):
                    raise TypeError(f"Can't use an instance of "
                                    f"'{define_as.__class__.__name__}' to "
                                    f"define a '{cls.__name__}' unit.")
                # noinspection PyTypeChecker
                unit = unit_cls(cls, symbol, name=name, define_as=define_as)
            elif isinstance(define_as, Term):
                try:
                    qty = _qty_from_term(define_as)
                except KeyError:
                    raise ValueError("Given term doesn't define a unit.")
                else:
                    if qty.__class__ is not cls:
                        raise ValueError(f"Given term doesn't define a "
                                         f"'{cls.__name__}' unit.")
                unit = unit_cls(cls, symbol, name=name, define_as=define_as)
            else:
                raise TypeError(f"'define_as' must be an instance of "
                                f"'{cls.__name__}' or a term denoting such "
                                f"an instance.")
        else:
            if cls.is_base_cls():
                raise TypeError(
                    "'derive_from' can't be used with a base quantity.")
            if define_as is not None:
                raise ValueError(
                    "'define_as' and 'derive_from' can't be used together.")
            if isinstance(derive_from, Unit):
                derive_from = (derive_from,)
            assert cls._definition is not None
            unit_def_items: List[Tuple[Unit, int]] = []
            for (qty_cls, exp), unit in zip(cls._definition, derive_from):
                if qty_cls is not unit.qty_cls:
                    raise ValueError(
                        "Given base units don't match base quantities.")
                unit_def_items.append((unit, exp))
            # noinspection PyTypeChecker
            unit_def_term = Term(unit_def_items)
            unit = unit_cls(cls, symbol, name=name, define_as=unit_def_term)
        cls._unit_map[unit.symbol] = unit
        return unit

    def units(cls) -> Tuple[Unit, ...]:  # noqa: N805
        """Return all registered units of `cls` as tuple."""
        return tuple(cls._unit_map.values())

    def __len__(cls) -> int:
        """Return the number of registered units of `cls`."""
        return len(cls._unit_map)

    def __contains__(cls, symbol: str) -> bool:
        """Return True if a unit with symbol `symbol` is registered in `cls`.
        """
        return symbol in cls._unit_map

    def __iter__(cls) -> Iterator[str]:
        """Return an iterator over the symbols registered in `cls`."""
        return iter(cls._unit_map)

    def get_unit_by_symbol(cls, symbol: str) -> Unit:
        """Return the unit with symbol `symbol`.

        Args:
            symbol (str): symbol to look-up

        Returns:
            :class:`Unit`: unit with given `symbol`

        Raises:
            ValueError: a unit with given `symbol` is not registered with `cls`

        """
        try:
            return cls._unit_map[symbol]
        except KeyError:
            raise ValueError(f"'{cls.__name__}' does not have a unit with "
                             f"symbol '{symbol}'.") from None

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


Q = TypeVar("Q", bound="Quantity")


class Quantity(metaclass=QuantityMeta):
    """Base class used to define types of quantities."""

    __slots__ = ['_amount', '_unit']

    # default format spec used in __format__
    dflt_format_spec = '{a} {u}'

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _amount: Rational
    _unit: Unit

    def __new__(cls: QuantityMeta,
                amount: Union[Real, str],
                unit: Optional[Unit] = None) -> Quantity:
        """Create new `Quantity` instance."""
        qty: Quantity
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
        elif isinstance(amount, str):
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
            cls = unit.qty_cls
            if cls is None:
                raise TypeError(f"'{unit}' is not a registered unit.")
        elif cls is not unit.qty_cls:
            raise QuantityError(f"Given unit '{unit}' is not a "
                                f"'{cls.__name__}' unit.")
        # make raw instance
        # noinspection PyTypeChecker
        qty = super().__new__(cls)      # type: ignore
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
                    amnt = conv(self, unit)
                    if amnt is not None:
                        return amnt
                return None
            else:
                return factor * self.amount

    def convert(self: Q, to_unit: Unit) -> Q:
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

    def quantize(self: Q, quant: Q, rounding: Optional[ROUNDING] = None) -> Q:
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
                            f"unit: {cls.__name__}.")
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

    def allocate(self: Q, ratios: Collection[Union[Rational, Quantity]],
                 disperse_rounding_error: bool = True) \
            -> Tuple[List[Q], Q]:
        """Apportion `self` according to `ratios`.

        Args:
            ratios (Collection[Union[Rational, Quantity]]): sequence of values
                defining the relative amount of the requested portions
            disperse_rounding_error (bool): determines whether a rounding error
                (if there is one due to quantization) shall be dispersed

        Returns:
            List[Q]: portions of `self` according to `ratios`
            Q: remainder = `self` - sum(portions)

        Raises:
            TypeError: `ratios` contains elements that can not be added
            IncompatibleUnitsError: `ratios` contains quantities that can not
                be added
        """
        n_portions = len(ratios)
        total = sum(ratios)
        if isinstance(total, Rational):
            # force 'total' to a Decimal, if possible
            try:
                total = Decimal(total)
            except ValueError:
                pass
        # calculate fractions from ratios
        fractions = [ratio / total for ratio in ratios]
        # apportion self according to fractions
        portions: List[Q] = [self * fraction for fraction in fractions]
        # check whether there's a remainder
        remainder = self - sum(portions)
        rem_amount = remainder.amount
        if rem_amount != 0:
            # calculate quantum for the quantity's unit
            assert self.unit.quantum is not None, \
                "Remainder != 0 for quantity w/o quantum."
            quantum = self.unit.quantum
            if disperse_rounding_error:
                if rem_amount < 0:
                    quantum = -quantum
                # calculate rounding errors
                errors = sorted(map(lambda portion, fraction, idx:
                                    (portion.amount - self.amount * fraction,
                                     idx),
                                    portions, fractions, range(n_portions)),
                                reverse=(rem_amount < 0))
                for error, idx in errors:
                    portions[idx]._amount += quantum
                    rem_amount -= quantum
                    if rem_amount == 0:
                        break
                remainder = rem_amount * self.unit
        return portions, remainder

    def __eq__(self, other: Any) -> bool:
        """self == other"""
        if isinstance(other, self.__class__):
            if self.unit is other.unit:
                return self.amount == other.amount
            equiv = other.equiv_amount(self.unit)
            if equiv is not None:
                return self.amount == equiv
        return False

    def _compare(self, other: Any, op: CmpOpT) -> bool:
        """Compare self and other using operator op."""
        if isinstance(other, self.__class__):
            if self.unit is other.unit:
                return op(self.amount, other.amount)
            equiv = other.equiv_amount(self.unit)
            if equiv is None:
                raise UnitConversionError("Can't convert '%s' to '%s'.",
                                          other.unit, self.unit)
            return op(self.amount, equiv)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't compare a '%s' and a '%s'.",
                                         self.__class__, other.__class__)
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

    def __hash__(self) -> int:
        """hash(self)"""
        return hash((self.amount, self.unit))

    def __abs__(self: Q) -> Q:
        """abs(self) -> self.Quantity(abs(self.amount), self.unit)"""
        return self.__class__(abs(self._amount), self.unit)

    def __pos__(self: Q) -> Q:
        """+self"""
        return self

    def __neg__(self: Q) -> Q:
        """-self -> self.Quantity(-self.amount, self.unit)"""
        return self.__class__(-self.amount, self.unit)

    def __add__(self: Q, other: Q) -> Q:
        """self + other"""
        if isinstance(other, self.__class__):
            equiv = other.equiv_amount(self.unit)
            if equiv is None:
                raise UnitConversionError("Can't convert '%s' to '%s'.",
                                          other.unit, self.unit)
            return self.__class__(self.amount + equiv, self.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't add a '%s' and a '%s'.",
                                         self.__class__, other.__class__)
        return NotImplemented

    # other + self
    __radd__ = __add__

    def __sub__(self: Q, other: Q) -> Q:
        """self - other"""
        if isinstance(other, self.__class__):
            equiv = other.equiv_amount(self.unit)
            if equiv is None:
                raise UnitConversionError("Can't convert '%s' to '%s'.",
                                          other.unit, self.unit)
            return self.__class__(self.amount - equiv, self.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'.",
                                         other.__class__, self.__class__)
        return NotImplemented

    def __rsub__(self: Q, other: Q) -> Q:
        """other - self"""
        if isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'.",
                                         self.__class__, other.__class__)
        return NotImplemented

    @overload
    def __mul__(self: Q, other: int) -> Q:  # noqa: D105
        ...

    @overload
    def __mul__(self: Q, other: float) -> Q:  # noqa: D105
        ...

    @overload
    def __mul__(self: Q, other: Real) -> Q:  # noqa: D105
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
        if isinstance(other, Real):
            return self.__class__(self.amount * Decimal(other), self.unit)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    @overload
    def __truediv__(self: Q, other: int) -> Q:  # noqa: D105
        ...

    @overload
    def __truediv__(self: Q, other: float) -> Q:  # noqa: D105
        ...

    @overload
    def __truediv__(self: Q, other: Real) -> Q:  # noqa: D105
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
        if isinstance(other, Real):
            return self.__class__(self.amount / Decimal(other), self.unit)
        return NotImplemented

    def __rtruediv__(self, other: Any) -> Quantity:
        """other / self"""
        if isinstance(other, Rational):
            return (other / self.amount) * self.unit ** -1
        if isinstance(other, Real):
            return (other / Decimal(self.amount)) * self.unit ** -1
        return NotImplemented

    def __pow__(self, exp: int) -> Quantity:
        """self ** exp"""
        if not isinstance(exp, int):
            return NotImplemented
        return self.amount ** exp * self.unit ** exp

    def __round__(self: Q, n_digits: int = 0) -> Q:
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

    def __format__(self, fmt_spec: str = "") -> str:
        """Convert to string (according to format specifier).

        The specifier must be a standard format specifier in the form
        described in PEP 3101. It should use two keys: 'a' for self.amount and
        'u' for self.unit, where 'a' can be followed by a valid format spec
        for numbers and 'u' by a valid format spec for strings.
        """
        if not fmt_spec:
            fmt_spec = self.dflt_format_spec
        return fmt_spec.format(a=self.amount, u=self.unit)


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
