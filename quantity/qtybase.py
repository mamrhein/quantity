# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        qtybase
## Purpose:     Provide base classes for defining quantities
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Provide base classes for defining quantities."""

from __future__ import absolute_import, division, unicode_literals
import itertools
import operator
from numbers import Integral, Real
from fractions import Fraction
from decimal import Decimal as StdLibDecimal
from decimalfp import Decimal
import quantity
from .exceptions import (QuantityError, IncompatibleUnitsError,
                         UndefinedResultError, UnitConversionError)
from .term import Term
from .converter import RefUnitConverter

__metaclass__ = type


# unicode handling, dict iterator and izip Python 2 / Python 3
import sys
PY_VERSION = sys.version_info[0]
del sys
typearg = str       # first argument for type must be native str in both
str = type(u'')
bytes = type(b'')
str_types = (bytes, str)
if PY_VERSION < 3:
    itervalues = lambda d: d.itervalues()
    zip = itertools.izip
else:
    itervalues = lambda d: d.values()


# because decimal.Decimal is not registered as number, we have to test it
# explicitly
NUM_TYPES = (Real, StdLibDecimal)

# decimal 1 constant
DECIMAL_1 = Decimal(1)

# cache for results of operations on quantity class definitions
QTY_CLS_OP_CACHE = {}

#cache for results of operations on unit definitions
UNIT_OP_CACHE = {}


# decorator defining meta class, portable between Python 2 / Python 3
def withMetaCls(metaCls):
    def _createCls(cls):
        return metaCls(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return _createCls


class QuantityRegistry():

    """Registers Quantity classes by definition."""

    def __init__(self):
        self._qtyDefMap = {}
        self._qtyList = []

    def registerQuantityCls(self, qtyCls):
        """Register Quantity class.

        Registers a sub-class of :class:`Quantity` by its normalized
        definition.

        Args:
            qtyCls (MetaQTerm): sub-class of :class:`Quantity` to be
                registered

        Returns:
            int: index of registered class

        Raises:
            ValueError: class with same definition already registered
        """
        qtyDef = qtyCls.normalizedClsDefinition
        try:
            idx = self._qtyDefMap[qtyDef]
        except KeyError:
            qtyList = self._qtyList
            qtyList.append(qtyCls)
            idx = len(qtyList) - 1
            self._qtyDefMap[qtyDef] = idx
            return idx
        else:
            regCls = self._qtyList[idx]
            if regCls == qtyCls:
                return idx
            else:
                raise ValueError(
                    "Class with same definition already registered.")

    def getQuantityCls(self, qtyDef):
        """Get Quantity class by definition.

        Args:
            qtyDef (MetaQTerm._QClsDefinition): definition of class to
                be looked-up

        Returns:
            MetaQTerm: sub-class of :class:`Quantity` registered with
                definition `qtyDef`

        Raises:
            ValueError: no sub-class of :class:`Quantity` registered with
                definition `qtyDef`
        """
        normQtyDef = qtyDef.normalized()
        try:
            idx = self._qtyDefMap[normQtyDef]
        except KeyError:
            raise ValueError('No quantity class registered with given '
                             'definition.')
        return self._qtyList[idx]

    def getUnitBySymbol(self, symbol):
        """Return the unit with symbol `symbol`.

        Args:
            symbol (str): symbol to look-up

        Returns:
            :class:`Unit` sub-class if a unit with given `symbol` exists in
                one of the registered quantities' `Unit` class, otherwise
                `None`
        """
        for qty in self:
            unit = qty.getUnitBySymbol(symbol)
            if unit:
                return unit
        return None

    def __len__(self):
        return len(self._qtyList)

    def __iter__(self):
        return iter(self._qtyList)


# Global registry of Quantities
_registry = QuantityRegistry()


def getUnitBySymbol(symbol):
    """getUnitBySymbol(symbol) -> unit

    Args:
        symbol (string): symbol to look-up

    Returns:
        :class:`Unit` sub-class if a unit with given `symbol` exists in
            one of the registered quantities' `Unit` class, otherwise
            `None`
    """
    return _registry.getUnitBySymbol(symbol)


class MetaQTerm(type):

    """Meta class that provides operators to construct derived quantities."""

    class _QClsDefinition(Term):

        """Definition of quantity classes."""

        __slots__ = []

        @staticmethod
        def isBaseElem(qCls):
            """True if qCls is a base quantity class."""
            return qCls.isBaseQuantity()

        @staticmethod
        def normalizeElem(qCls):
            """Return the normalized definition of qCls."""
            return qCls.normalizedClsDefinition

        @staticmethod
        def normSortKey(qCls):
            """Return sort key for qCls."""
            return qCls.Quantity._regIdx + 1

    def __new__(cls, name, bases, clsdict):
        # hide refUnitSymbol, refUnitName and quantum
        for key in ['refUnitSymbol', 'refUnitName', 'quantum']:
            try:
                val = clsdict[key]
            except KeyError:
                pass
            else:
                del clsdict[key]
                clsdict['_' + key] = val
        # prevent __dict__ from being built for subclasses of Quantity or Unit
        try:
            clsdict['__slots__']
        except KeyError:
            clsdict['__slots__'] = ()
        return type.__new__(cls, name, bases, clsdict)

    def __init__(self, name, bases, clsdict):
        type.__init__(self, name, bases, clsdict)
        # hide defineAs
        try:
            self._clsDefinition = self.defineAs
            del self.defineAs
        except AttributeError:
            self._clsDefinition = None
        # extract names of base classes
        baseNames = [base.__name__ for base in self.__mro__[1:]]
        # new Quantity class:
        if 'Quantity' in baseNames:
            # add reference to self
            self.Quantity = self
            # register self
            self._regIdx = _registry.registerQuantityCls(self)
            # unit class given?
            try:
                unitCls = self.Unit
                if unitCls is not None:
                    unitCls.Quantity = self
            except AttributeError:
                # create corresponding unit class
                qtyClsDef = self._clsDefinition
                if qtyClsDef:
                    items = ((qtyCls.Unit, exp) for qtyCls, exp in qtyClsDef)
                    unitClsDef = self._QClsDefinition(items,
                                                      reduceItems=False)
                else:
                    unitClsDef = None
                unitCls = self.Unit = MetaQTerm(typearg(name + 'Unit'),
                                                (Unit,),
                                                {'Quantity': self,
                                                'defineAs': unitClsDef})
                # create and register reference unit
                try:
                    refUnitSymbol = self._refUnitSymbol
                except AttributeError:
                    refUnitSymbol = None
                try:
                    refUnitName = self._refUnitName
                except AttributeError:
                    refUnitName = None
                if refUnitSymbol or self._refUnitDef:
                    unitCls._refUnit = unitCls(refUnitSymbol, refUnitName)
                    # register reference unit converter
                    unitCls.registerConverter(RefUnitConverter())
            # check quantum
            try:
                quantum = self._quantum
            except AttributeError:
                pass
            else:
                if self.refUnit:
                    try:
                        self._quantum = Decimal(quantum)
                    except (ValueError, TypeError):
                        raise TypeError("'quantum' must be a Decimal or be "
                                        "convertable to a Decimal.")
                else:
                    raise TypeError("A quantum can only be defined in "
                                    "combination with a reference unit.")
        # new Unit class:
        elif 'Unit' in baseNames:
            # add reference to self
            self.Unit = self
            # initialize unit registry
            self._symDict = {}          # maps symbols to units
            self._termDict = {}         # maps normalized definitions to units
            # initialize converter registry
            self._converters = []

    def _asClsDefinition(self):
        return self._QClsDefinition([(self, 1)], reduceItems=False)

    @property
    def clsDefinition(self):
        if self._clsDefinition is None:
            return self._asClsDefinition()
        return self._clsDefinition

    @property
    def normalizedClsDefinition(self):
        if self.isBaseQuantity():
            return self.clsDefinition
        else:
            return self.clsDefinition.normalized()

    def isBaseQuantity(self):
        """Return True if self is not derived from other quantity classes."""
        # base quantity -> class definition is None or empty term (_Unitless)
        return self._clsDefinition is None or len(self._clsDefinition) == 0

    def isDerivedQuantity(self):
        """Return True if self is derived from other quantity classes."""
        return not self.isBaseQuantity()

    @property
    def refUnit(self):
        """The reference unit of the :class:`Quantity` or :class:`Unit`
        sub-class, if defined, otherwise None."""
        try:
            return self.Unit.__dict__.get('_refUnit')
        except AttributeError:
            return None

    @property
    def refUnitSymbol(self):
        try:
            return self.refUnit.symbol
        except AttributeError:
            return None

    @property
    def refUnitName(self):
        try:
            return self.refUnit.name
        except AttributeError:
            return None

    @property
    def _refUnitDef(self):
        """Return definition of reference unit."""
        qtyDef = self.clsDefinition
        # check whether all base classes have a reference unit
        if any((qtyCls.refUnit is None for qtyCls, exp in qtyDef)):
            return None
        return self._QTerm(((qtyCls.refUnit, exp) for qtyCls, exp in qtyDef))

    @property
    def quantum(self):
        """The smallest amount (in terms of the reference unit) an instance of
        this :class:`Quantity` can take (None if quantum not defined)."""
        try:
            return self._quantum
        except AttributeError:
            return None

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, MetaQTerm):
            return self._asClsDefinition() * other._asClsDefinition()
        if isinstance(other, self._QClsDefinition):
            return self._asClsDefinition() * other
        return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, MetaQTerm):
            return self._asClsDefinition() / other._asClsDefinition()
        if isinstance(other, self._QClsDefinition):
            return self._asClsDefinition() / other
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, MetaQTerm):
            return other._asClsDefinition() / self._asClsDefinition()
        if isinstance(other, self._QClsDefinition):
            return other / self._asClsDefinition()
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        if isinstance(exp, Integral):
            return self.clsDefinition ** exp
        return NotImplemented

    def __str__(self):
        return self.__name__


@withMetaCls(MetaQTerm)
class QTermElem:

    """Abstract base class for Quantity and Unit."""

    __slots__ = []

    class _QTerm(Term):
        """Definition of quantities."""

        __slots__ = []

        @staticmethod
        def isBaseElem(qty):
            """True if qty.unit is a base unit."""
            return qty.unit.isBaseUnit()

        @staticmethod
        def normalizeElem(qty):
            """Return qty as normalized QTerm."""
            return qty.normalizedDefinition

        @staticmethod
        def normSortKey(qty):
            """Return sort key for qty."""
            try:
                return qty.Quantity._regIdx + 1
            except AttributeError:
                return 0

        @staticmethod
        def convert(qty, into):
            """Return factor f so that f * into == qty.

            Raises TypeError if conversion is not possible."""
            return into(qty)

        @property
        def amount(self):
            return self.numElem or DECIMAL_1

        @property
        def unitTerm(self):
            if self.numElem is None:
                return self
            return self.__class__(self[1:])

    @property
    def definition(self):
        """The quantity's or units definition."""
        cls = self._QTerm
        if self.amount == 1:
            return cls(((self.unit, 1),), reduceItems=False)
        return cls(((self.amount, 1), (self.unit, 1)), reduceItems=False)

    @property
    def normalizedDefinition(self):
        """The quantity's or units normalized definition.

        The normalized definition defines the quantity or unit in terms of
        base units only."""
        if self.unit.isBaseUnit():
            return self.definition
        else:
            return self.definition.normalized()

    @property
    def amount(self):
        """The elements amount."""
        raise NotImplementedError

    @property
    def unit(self):
        """The elements unit."""
        raise NotImplementedError

    @property
    def refUnit(self):
        """The reference unit of the :class:`Quantity` or :class:`Unit`
        sub-class, if defined, otherwise None."""
        try:
            return self.Unit.refUnit
        except AttributeError:
            return None

    def __copy__(self):
        """Return self (:class:`Quantity` and :class:`Unit` instances are
        immutable)."""
        return self

    def __deepcopy__(self, memo):
        return self.__copy__()

    def __eq__(self, other):
        """self == other"""
        raise NotImplementedError

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        raise NotImplementedError

    def __lt__(self, other):
        """self < other"""
        return self._compare(other, operator.lt)

    def __le__(self, other):
        """self <= other"""
        return self._compare(other, operator.le)

    def __gt__(self, other):
        """self > other"""
        return self._compare(other, operator.gt)

    def __ge__(self, other):
        """self >= other"""
        return self._compare(other, operator.ge)


class Unit(QTermElem):

    """Base class used to define types of quantity units.

    Args:
        symbol (unicode string): unique string representation of the unit
            (default: None)
        name (string): name of the unit (default: None)
        defineAs (:class:`Quantity` sub-class or _QTerm): definition of the
            unit (default: None)

    If no symbol is given, but a definition, and the numerical part of that
    definition is None or 1, the symbol is derived from the definition.

    If no symbol and no definition is given, but the corresponding
    :class:`Quantity` sub-class is a derived quantity class and all its base
    classes have a reference unit, the symbol and the definition are derived
    from the class definition.

    If only a `symbol` is given and a unit with that symbol is already
    registered, that unit is returned.

    Returns:
        :class:`Unit` instance

    Raises:
        TypeError: given `symbol` is not a unicode string
        ValueError: no `symbol` was given and it could not be generated
        ValueError: a unit with the given or generated `symbol` is already
            registered
        ValueError: no `defineAs` given, but reference unit already registered
        TypeError: given `defineAs` does not fit the :class:`Unit` sub-class
    """

    __slots__ = ['_symbol', '_name', '_definition']

    def __new__(cls, symbol=None, name=None, defineAs=None):
        if symbol is None:
            if defineAs is None:
                if cls.Quantity.isDerivedQuantity():
                    # try to generate symbol for reference unit of derived
                    # quantity:
                    refUnitDef = cls._refUnitDef
                    if refUnitDef:
                        symbol = str(refUnitDef)
            elif isinstance(defineAs, cls._QTerm):
                # try to generate symbol from definition:
                if defineAs.amount == 1:
                    symbol = str(defineAs)
        else:
            if not isinstance(symbol, str):
                raise TypeError('Symbol must be a unicode string.')
        if not symbol:
            raise ValueError("A symbol must be given for the unit.")
        # return unit with symbol if already registered
        try:
            unit = cls._symDict[symbol]
        except KeyError:
            pass
        else:
            if name is not None or defineAs is not None:
                raise ValueError("Unit with symbol '%s' already registered."
                                 % symbol)
            return unit
        # create new unit
        unit = super(Unit, cls).__new__(cls)
        unit._symbol = symbol
        unit._name = name
        if defineAs is None:
            if cls.refUnit is not None:
                # there can be only one reference unit
                raise ValueError(
                    "Unregistered symbol '%s' given without definition."
                    % symbol)
            if cls.Quantity.isBaseQuantity():
                unit._definition = None
            else:
                unit._definition = cls._refUnitDef
        elif isinstance(defineAs, cls.Quantity):
            unit._definition = defineAs.definition
        elif isinstance(defineAs, cls._QTerm):
            # TODO: check whether the correct term for the unit class is given
            unit._definition = defineAs
        else:
            raise TypeError("'defineAs' must be of type '%s' or a "
                            "corresponding term; a '%s' given instead."
                            % (cls.Quantity, cls._QTerm, type(defineAs)))
        # register new unit
        cls._symDict[symbol] = unit
        normDef = unit.normalizedDefinition
        try:
            equivalents = cls._termDict[normDef]
        except KeyError:
            cls._termDict[normDef] = [unit]
        else:
            equivalents.append(unit)
        # return new unit
        return unit

    @classmethod
    def registeredUnits(cls):
        """Return an iterator over the units registered in cls."""
        return itervalues(cls._symDict)

    @classmethod
    def getUnitBySymbol(cls, symbol):
        """Return the unit with symbol `symbol`.

        Args:
            symbol (string): symbol to look-up

        Returns:
            :class:`Unit` sub-class: if a unit with given `symbol` exists
                within this :class:`Unit` sub-class
            None: otherwise
        """
        try:        # transform to unicode
            symbol = symbol.decode()
        except (AttributeError, UnicodeEncodeError):
            pass
        return cls._symDict.get(symbol)

    @classmethod
    def registerConverter(cls, conv):
        """Add converter conv to the list of converters registered in cls.

        Does nothing if converter is already registered."""
        if conv not in cls._converters:
            cls._converters.append(conv)

    @classmethod
    def removeConverter(cls, conv):
        """Remove converter conv from the list of converters registered in
        cls.

        Raises ValueError if the converter is not present."""
        cls._converters.remove(conv)

    @classmethod
    def registeredConverters(cls):
        """Return an iterator over the converters registered in cls."""
        return reversed(cls._converters)

    @property
    def definition(self):
        """Return the definition of the unit."""
        if self._definition is None:
            return self._QTerm(((self, 1),), reduceItems=False)
        return self._definition

    @property
    def symbol(self):
        """Return the units symbol, a unique string representation of the
        unit.

        Used for the functions str, repr, format, hash and the unit
        registry."""
        return self._symbol

    @property
    def name(self):
        """Return the units name.

        If the unit was not given a name, its symbol is returned."""
        return self._name or self._symbol

    @property
    def amount(self):
        return DECIMAL_1

    @property
    def unit(self):
        return self

    def isRefUnit(self):
        """Return True if the unit is a reference unit."""
        return self is self.refUnit

    def isBaseUnit(self):
        """Return True if the unit is a base unit, i. e. it's not derived
        from another unit."""
        return self._definition is None

    def isDerivedUnit(self):
        """Return True if the unit is derived from another unit."""
        return self._definition is not None

    def __eq__(self, other):
        """self == other"""
        if isinstance(other, self.Unit):
            try:
                return self.amount == self(other)
            except UnitConversionError:
                pass
        return False

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        if isinstance(other, self.Unit):
            return op(self.amount, self(other))
        elif isinstance(other, Unit):
            raise IncompatibleUnitsError("Can't compare a %s and a %s",
                                         self, other)
        return NotImplemented

    def __hash__(self):
        return hash((self.Quantity.__name__, self.symbol))

    def __call__(self, equiv):
        """Return scaling factor to make `self` equivalent to `equiv`.

        Args:
            equiv (:class:`Quantity` or :class:`Unit`): equivalent looked for

        Returns:
            number: scaling factor so that (depending on type of `equiv`)
                factor ^ self == equiv or
                factor ^ self == 1 ^ equiv

        Raises:
            IncompatibleUnitsError: self and equiv are of incompatible types
            UnitConversionError: conversion factor not available
            TypeError: no :class:`Quantity` or :class:`Unit` instance given
        """
        try:
            oUnit = equiv.unit
        except AttributeError:
            raise TypeError("A '%s' or a '%s' must be given, not a '%s'."
                            % (self.Quantity, self.Unit, type(equiv)))
        if oUnit is self:                   # same unit
            return equiv.amount
        if self.Unit != equiv.Unit:         # different Unit classes
            raise IncompatibleUnitsError("Can't convert '%s' to '%s'.",
                                         equiv.Quantity, self.Quantity)
        # try registered converters:
        for conv in self.registeredConverters():
            try:
                return conv(equiv, self)
            except UnitConversionError:
                pass
        # if derived Unit class, try to convert base units:
        cls = self.Unit
        if cls.isDerivedQuantity():
            resDef = (equiv.unit.normalizedDefinition /
                      self.normalizedDefinition)
            if len(resDef) <= 1:
                return equiv.amount * resDef.amount
        # no success, give up
        raise UnitConversionError("Can't convert '%s' to '%s'.",
                                  equiv.unit, self)

    def __mul__(self, other, op_cache=UNIT_OP_CACHE):
        """self * other"""
        if isinstance(other, Unit):
            try:    # try cache
                return op_cache[(operator.mul, self, other)]
            except KeyError:
                pass
            # no cache hit
            res = self._QTerm(((self, 1), (other, 1)))
            # cache it
            op_cache[(operator.mul, self, other)] = res
        elif isinstance(other, NUM_TYPES):
            res = self._QTerm(((other, 1), (self, 1)), reduceItems=False)
        elif isinstance(other, self._QTerm):
            res = self._QTerm(((self, 1),)) * other
        else:
            return NotImplemented
        return res

    # other * self
    __rmul__ = __mul__

    def __div__(self, other, op_cache=UNIT_OP_CACHE):
        """self / other"""
        if isinstance(other, Unit):
            try:    # try cache
                return op_cache[(operator.truediv, self, other)]
            except KeyError:
                pass
            # no cache hit
            res = self._QTerm(((self, 1), (other, -1)))
            # cache it
            op_cache[(operator.truediv, self, other)] = res
        elif isinstance(other, NUM_TYPES):
            res = self._QTerm(((1 / other, 1), (self, 1)), reduceItems=False)
        elif isinstance(other, self._QTerm):
            res = self._QTerm(((self, 1),)) / other
        else:
            return NotImplemented
        return res

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, NUM_TYPES):
            return self._QTerm(((other, 1), (self, -1)), reduceItems=False)
        elif isinstance(other, self._QTerm):
            return other / self._QTerm(((self, 1),), reduceItems=False)
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        if not isinstance(exp, Integral):
            return NotImplemented
        return self._QTerm(((self, exp),), reduceItems=False)

    def __rxor__(self, other):
        """other ^ self

        Alternate constructor for quantity:
        other ^ self  ->  self.Quantity(other, self)

        Raises TypeError if other is not a Real number."""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(other, self)
        return NotImplemented

    def __repr__(self):
        """repr(self)"""
        return "%s.Unit(%s)" % (self.Quantity.__name__, repr(self.symbol))

    if PY_VERSION < 3:

        def __unicode__(self):
            """unicode(self)"""
            return "%s" % self.symbol

        def __str__(self):
            """str(self)"""
            return self.__unicode__().encode('utf8')

    else:

        def __str__(self):
            """str(self)"""
            return "%s" % self.symbol

    def __format__(self, fmtSpec):
        """Convert to string (according to fmtSpec).

        fmtSpec must be a valid format spec for strings.
        """
        return format(self.symbol, fmtSpec)


class Quantity(QTermElem):

    """Base class used to define types of quantities.

    Instances of `Quantity` can be created in two ways, by providing a
    numerical amount and - optionally - a unit or by providing a string
    representation of a quantity.

    **1. Form**

    Args:
        amount (number): the numerical part of the quantity
        unit (:class:`Unit` sub-class): the quantity's unit (optional)

    `amount` must be of type `number.Real` or be convertable to a
    `decimalfp.Decimal`. `unit` must be an instance of the :class:`Unit`
    sub-class corresponding to the :class:`Quantity` sub-class. If no `unit`
    is given, the reference unit of the :class:`Quantity` sub-class is used
    (if defined, otherwise a ValueError is raised).

    Returns:
        instance of called :class:`Quantity` sub-class or instance of the
            sub-class corresponding to given `unit` if :class:`Quantity` is
            called

    Raises:
        TypeError: `amount` is not a Real or Decimal number and can not be
            converted to a Decimal number
        ValueError: no unit given and the :class:`Quantity` sub-class doesn't
            define a reference unit
        TypeError: `unit` is not an instance of the :class:`Unit` sub-class
            corresponding to the :class:`Quantity` sub-class

    **2. Form**

    Args:
        qStr (unicode string): string representation of a quantity
        unit (:class:`Unit` sub-class): the quantity's unit (optional)

    `qStr` must contain a numerical value and a unit symbol, separated atleast
    by one blank. Any surrounding white space is ignored. If `unit` is given
    in addition, the resulting quantity's unit is set to this unit and its
    amount is converted accordingly.

    Returns:
        instance of :class:`Quantity` sub-class corresponding to symbol in
            `qRepr`

    Raises:
        QuantityError: amount given in `qStr` is not a Real or Decimal number
            and can not be converted to a Decimal number
        QuantityError: no unit given and the :class:`Quantity` sub-class
            doesn't define a reference unit
        QuantityError: `unit` is not an instance of the :class:`Unit`
            sub-class corresponding to the :class:`Quantity` sub-class
        QuantityError: a byte string is given that can not be decoded using
            the standard encoding
        QuantityError: given string does not represent a `Quantity`
        IncompatibleUnitsError: the unit derived from the symbol given in
            `qStr` is not compatible with given `unit`
    """

    __slots__ = ['_amount', '_unit']

    # default format spec used in __format__
    dfltFormatSpec = '{a} {u}'

    def __new__(cls, amount, unit=None):
        """Create a `Quantity` instance."""
        if isinstance(amount, (Decimal, Fraction)):
            pass
        elif isinstance(amount, (Integral, StdLibDecimal)):
            amount = Decimal(amount)      # convert to decimalfp.Decimal
        elif isinstance(amount, float):
            try:
                amount = Decimal(amount)
            except ValueError:
                amount = Fraction(amount)
        elif isinstance(amount, str_types):
            if isinstance(amount, bytes):
                try:
                    qRepr = amount.decode()
                except UnicodeError:
                    raise QuantityError("Can't decode given bytes using "
                                        "default encoding.")
            else:
                qRepr = amount
            parts = qRepr.lstrip().split(' ', 1)
            sAmount = parts[0]
            try:
                amount = Decimal(sAmount)
            except:
                try:
                    amount = Fraction(sAmount)
                except:
                    raise QuantityError("Can't convert '%s' to a number."
                                        % sAmount)
            if len(parts) > 1:
                sSym = parts[1].strip()
                unitFromSym = getUnitBySymbol(sSym)
                if unitFromSym:
                    if unit is None:
                        unit = unitFromSym
                    else:
                        amount *= unit(unitFromSym)
                else:
                    raise QuantityError("Unknown symbol '%s'." % sSym)
        else:
            raise QuantityError("Given amount must be a number or a string "
                                "that can be converted to a number.")
        if unit is None:
            unit = cls.refUnit
            if unit is None:
                raise QuantityError("A unit must be given.")
        if cls is Quantity:
            cls = unit.Quantity
        if not isinstance(unit, cls.Unit):
            raise QuantityError("Given unit '%s' is not a '%s'."
                                % (unit, cls.Unit.__name__))
        # make raw instance
        qty = super(QTermElem, cls).__new__(cls)
        # check whether it should be quantized
        quantum = cls.getQuantum(unit)
        if quantum:
            amount = cls._quantize(amount / quantum, unit) * quantum
        # finally set amount and unit
        qty._amount = amount
        qty._unit = unit
        return qty

    @classmethod
    def _fromQTerm(cls, qTerm):
        """Create quantity from qTerm."""
        unitCls = cls.Unit
        normUnitTerm = qTerm.unitTerm.normalized()
        try:
            unit = unitCls._termDict[normUnitTerm][0]
        except KeyError:
            normTerm = qTerm.normalized()
            try:
                unit = unitCls._termDict[normTerm.unitTerm][0]
            except (KeyError, IndexError):
                raise QuantityError("Unit not registered in %s." % unitCls)
            else:
                amount = normTerm.amount
        else:
            amount = qTerm.amount
        return cls.Quantity(amount, unit)

    @classmethod
    def getUnitBySymbol(cls, symbol):
        """Return the unit with symbol `symbol`.

        Args:
            symbol (str): symbol to look-up

        Returns:
            :class:`Unit` sub-class: if a unit with given `symbol` exists
                within the :class:`Unit` sub-class associated with this
                :class:`Quantity` sub-class
            None: otherwise
        """
        return cls.Unit.getUnitBySymbol(symbol)

    @staticmethod
    def _quantize(amount, unit, quant=None, rounding=None):
        if quant is None:
            numQuant = DECIMAL_1
        else:
            numQuant = unit(quant)
        try:
            return amount.quantize(numQuant, rounding)
        except AttributeError:
            # turn Fraction into Decimal:
            decAmount = Decimal(amount, max(1 - numQuant.magnitude, 0))
            return decAmount.quantize(numQuant, rounding)

    @classmethod
    def getQuantum(cls, unit):
        """Return the smallest amount an instance of this :class:`Quantity`
        can take for `unit` (return None if no quantum defined)."""
        quantum = cls.quantum
        if quantum is None:
            return None
        return quantum * unit(cls.refUnit)

    @property
    def amount(self):
        """The quantity's amount, i.e. the numerical part of the quantity."""
        return self._amount

    @property
    def unit(self):
        """The quantity's unit."""
        return self._unit

    def equivAmount(self, unit):
        """Return amount e so that e ^ `unit` == self."""
        return unit(self)

    def convert(self, toUnit):
        """Return quantity q where q == self and q.unit is toUnit.

        Args:
            toUnit (Unit): unit to be converted to

        Returns:
            Quantity: resulting quantity (of same type)

        Raises:
            IncompatibleUnitsError: self can't be converted to unit *toUnit*.
        """
        return self.Quantity(self.equivAmount(toUnit), toUnit)

    def quantize(self, quant, rounding=None):
        """Return integer multiple of `quant` closest to `self`.

        Args:
            quant (:class:`Quantity` or :class:`Unit`): quantum to get a
                multiple from
            rounding (str): rounding mode (default: None)

        `quant` must either be of type self.Quantity or of type self.Unit.

        If no `rounding` mode is given, the default mode from the current
        context (from module `decimal`) is used.

        Returns:
            :class:`Quantity` sub-class instance that is the integer multiple
                of `quant` closest to `self` (according to `rounding` mode)

        Raises:
            IncompatibleUnitsError: `quant` can not be converted to self.unit
            TypeError: no :class:`Quantity` or :class:`Unit` instance given
        """
        unit = self.unit
        amount = self._quantize(self.amount, unit, quant, rounding)
        return self.Quantity(amount, unit)

    def allocate(self, ratios, disperseRoundingError=True):
        """Apportion `self` according to `ratios`.

        Args:
            ratios (iterable): sequence of values defining the relative amount
                of the requested portions
            disperseRoundingError (bool): determines whether a rounding error
                (if there is one due to quantization) shall be dispersed

        Returns:
            tuple: portions of `self` according to `ratios` (list),
                remainder (:class:`Quantity`) = self - sum(portions)

        Raises:
            TypeError: `ratios` contains elements that can not be added
            IncompatibleUnitsError: `ratios` contains quantities that can not
                be added
        """
        nPortions = len(ratios)
        total = quantity.sum(ratios)
        # force 'total' to a Decimal, if possible
        try:
            total = Decimal(total)
        except:
            pass
        # calculate fractions from ratios
        fractions = [ratio / total for ratio in ratios]
        # apportion self according to fractions
        portions = [self * fraction for fraction in fractions]
        # check whether there's a remainder
        remainder = self - quantity.sum(portions)
        remAmount = remainder.amount
        if remAmount != 0:
            # calculate quantum for the quantity's unit
            quantum = self.getQuantum(self.unit)
            assert quantum is not None, \
                "Remainder != 0 for quantity w/o quantum."
            if disperseRoundingError:
                if remAmount < 0:
                    quantum = -quantum
                # calculate rounding errors
                errors = sorted(map(lambda portion, fraction, idx:
                                    (portion.amount - self.amount * fraction,
                                     idx),
                                    portions, fractions, range(nPortions)),
                                reverse=(remAmount < 0))
                for error, idx in errors:
                    portions[idx]._amount += quantum
                    remAmount -= quantum
                    if remAmount == 0:
                        break
                remainder = self.Quantity(remAmount, self.unit)
        return portions, remainder

    def __eq__(self, other):
        """self == other"""
        if isinstance(other, self.Quantity):
            try:
                return self.amount == other.equivAmount(self.unit)
            except IncompatibleUnitsError:
                pass
        return False

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        if isinstance(other, self.Quantity):
            return op(self.amount, other.equivAmount(self.unit))
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't compare a %s and a %s",
                                         self, other)
        return NotImplemented

    def __hash__(self):
        """hash(self)"""
        return hash((self.amount, self.unit))

    def __abs__(self):
        """abs(self) -> self.Quantity(abs(self.amount), self.unit)"""
        return self.Quantity(abs(self.amount), self.unit)

    def __pos__(self):
        """+self"""
        return self

    def __neg__(self):
        """-self -> self.Quantity(-self.amount, self.unit)"""
        return self.Quantity(-self.amount, self.unit)

    def __add__(self, other):
        """self + other"""
        if isinstance(other, self.Quantity):
            return self.Quantity(self.amount + other.equivAmount(self.unit),
                                 self.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't add a '%s' and a '%s'",
                                         self, other)
        return NotImplemented

    # other + self
    __radd__ = __add__

    def __sub__(self, other):
        """self - other"""
        if isinstance(other, self.Quantity):
            return self.Quantity(self.amount - other.equivAmount(self.unit),
                                 self.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'",
                                         other, self)
        return NotImplemented

    def __rsub__(self, other):
        """other - self"""
        if isinstance(other, self.Quantity):
            return self.Quantity(other.amount - self.equivAmount(other.unit),
                                 other.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'",
                                         self, other)
        return NotImplemented

    def _getResQtyCls(self, other, op, op_cache=QTY_CLS_OP_CACHE):
        """Return class resulting from op(self, other).

        op must be operator.mul, operator.truediv, operator.floordiv or
        operator.mod.
        Raises UndefinedResultError if resulting class is not defined."""
        selfQtyCls, otherQtyCls = self.Quantity, other.Quantity
        try:    # try cache
            return op_cache[(op, selfQtyCls, otherQtyCls)]
        except KeyError:
            pass
        # no cache hit
        resQtyDef = op(selfQtyCls.clsDefinition, otherQtyCls.clsDefinition)
        if resQtyDef:
            try:
                resQtyCls = _registry.getQuantityCls(resQtyDef)
            except ValueError:
                raise UndefinedResultError(op, self, other)
        else:
            resQtyCls = _Unitless
        # cache it
        op_cache[(op, selfQtyCls, otherQtyCls)] = resQtyCls
        return resQtyCls

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(self.amount * other, self.unit)
        elif isinstance(other, Quantity):
            resQtyCls = self._getResQtyCls(other, operator.mul)
            resQTerm = (self.amount * other.amount) * (self.unit * other.unit)
            if resQtyCls is _Unitless:
                return resQTerm.normalized().amount
            else:
                return resQtyCls._fromQTerm(resQTerm)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(self.amount / other, self.unit)
        if isinstance(other, self.Quantity):
            return self.amount / other.equivAmount(self.unit)
        elif isinstance(other, Quantity):
            resQtyCls = self._getResQtyCls(other, operator.truediv)
            resQTerm = (self.amount / other.amount) * (self.unit / other.unit)
            if resQtyCls is _Unitless:
                return resQTerm.normalized().amount
            else:
                return resQtyCls._fromQTerm(resQTerm)
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, NUM_TYPES):
            return _Unitless(other) / self
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        if not isinstance(exp, Integral):
            return NotImplemented
        resQtyDef = self.Quantity ** exp
        try:
            resQtyCls = _registry.getQuantityCls(resQtyDef)
        except ValueError:
            raise UndefinedResultError(operator.pow, self, exp)
        resQTerm = self.amount ** exp * self.unit ** exp
        return resQtyCls._fromQTerm(resQTerm)

    def __round__(self, precision=0):
        """Returns a copy of `self` with its amount rounded to the given
        `precision`.

        **1. Form**

        Args:
            precision (`Integral`): number of fractional digits to be rounded
                to

        Returns:
            copy of `self` with its amount rounded to an integer multiple of
                10 ** `precision`

        **2. Form**

        Args:
            precision (:class:`Quantity`): quantum of which the result has to
                be an integer multiple

        Returns:
            copy of `self` rounded to an integer multiple of `precision`

        **3. Form**

        Args:
            precision (:class:`Unit`): unit of which the result has to be an
                integer multiple of

        Returns:
            copy of `self` rounded to integer multiple of 1 ^ `precision`

        Raises:
            IncompatibleUnitsError: `precision` is not an Integral and can not
                be converted to self.unit

        Note: this method is called by the standard `round` function only in
        Python 3.x!
        """
        if isinstance(precision, Integral):
            return self.Quantity(Decimal(self.amount, precision), self.unit)
        return self.quantize(precision)

    def __repr__(self):
        """repr(self)"""
        if self.unit.isRefUnit():
            return "%s(%s)" % (self.__class__.__name__, repr(self.amount))
        else:
            return "%s(%s, %s)" % (self.__class__.__name__, repr(self.amount),
                                   repr(self.unit))

    if PY_VERSION < 3:

        def __unicode__(self):
            """unicode(self)"""
            return "%s %s" % (self.amount, self.unit)

        def __str__(self):
            """str(self)"""
            return self.__unicode__().encode('utf8')

    else:

        def __str__(self):
            """str(self)"""
            return "%s %s" % (self.amount, self.unit)

    def __format__(self, fmtSpec=""):
        """Convert to string (according to format specifier).

        The specifier must be a standard format specifier in the form
        described in PEP 3101. It should use two keys: 'a' for self.amount and
        'u' for self.unit, where 'a' can be followed by a valid format spec
        for numbers and 'u' by a valid format spec for strings.
        """
        if not fmtSpec:
            fmtSpec = self.dfltFormatSpec
        return fmtSpec.format(a=self.amount, u=self.unit)

    # pickle support
    def __reduce__(self):
        return (quantity.r, (str(self),))


class _Unitless:

    """Fake quantity without unit.

    Used to implement reversed operator rdiv."""

    __slots__ = ['_amount']

    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def __div__(self, other):
        """self / other"""
        if isinstance(other, Quantity):
            op = operator.truediv
            resQtyDef = op(other.Quantity._QClsDefinition(),
                           other.Quantity.clsDefinition)
            if resQtyDef:
                try:
                    resQtyCls = _registry.getQuantityCls(resQtyDef)
                except ValueError:
                    raise UndefinedResultError(op, self, other)
                resQTerm = (self.amount / other.amount) / other.unit
                return resQtyCls._fromQTerm(resQTerm)
        return NotImplemented

    __truediv__ = __div__

    def __str__(self):
        return "%s" % (self.amount)

    def __format__(self, fmtSpec=""):
        if not fmtSpec:
            fmtSpec = '{a}'
        return fmtSpec.format(a=self.amount, u='')


def generateUnits(qCls):
    """Create and register units by combining the units of the base classes.

    Args:
        qCls (:class:`Quantity` sub-class): derived quantity class to create
            units for

    Returns:
        None

    Raises:
        ValueError: given quantity class is not a derived quantity

    The function creates and registers all units from the cross-product of all
    units of the quantity classes the class `qCls` is derived from, provided
    that the corresponding symbol is not already registered.
    """
    if qCls.isBaseQuantity():
        raise ValueError('Given quantity class must be a derived quantity.')
    unitCls = qCls.Unit
    QTerm = qCls._QTerm
    clsDefinition = qCls.clsDefinition
    iterUnitClss = ((cls.Unit, exp) for cls, exp in clsDefinition)
    iterUnits = (zip(unitCls.registeredUnits(), itertools.repeat(exp))
                 for unitCls, exp in iterUnitClss)
    comb = itertools.product(*iterUnits)
    for term in comb:
        unitDef = QTerm(term)
        symbol = str(unitDef)
        if unitCls.getUnitBySymbol(symbol):
            # unit already registered
            continue
        unitCls(symbol, defineAs=unitDef)
