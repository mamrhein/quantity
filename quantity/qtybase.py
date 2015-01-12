# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        qtybase
## Purpose:     Provide base classes for defining quantities
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


"""Provide base classes for defining quantities."""

from __future__ import absolute_import, division, unicode_literals
import operator
from numbers import Integral, Real
from decimal import Decimal as StdLibDecimal
from decimalfp import Decimal
from .term import Term
from .converter import RefUnitConverter


__version__ = 0, 7, 0

__metaclass__ = type


# unicode handling and dict iterator Python 2 / Python 3
import sys
PY_VERSION = sys.version_info[0]
del sys
typearg = str       # first argument for type must be native str in both
str = type(u'')
bytes = type(b'')
str_types = (bytes, str)
if PY_VERSION < 3:
    itervalues = lambda d: d.itervalues()
else:
    itervalues = lambda d: d.values()


# because decimal.Decimal is not registered as number, we have to test it
# explicitly
NUM_TYPES = (Real, StdLibDecimal)


# decorator defining meta class, portable between Python 2 / Python 3
def withMetaCls(metaCls):
    def _createCls(cls):
        return metaCls(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return _createCls


class QuantityError(TypeError):

    """Base class for quantity exceptions."""


class IncompatibleUnitsError(QuantityError):

    """Exception raised when operands do not have compatible units."""

    def __init__(self, msg, operand1, operand2):
        if isinstance(operand1, QTermElem):
            operand1 = operand1.__class__.__name__
        if isinstance(operand2, QTermElem):
            operand2 = operand2.__class__.__name__
        QuantityError.__init__(self, msg % (operand1, operand2))


class UndefinedResultError(QuantityError):

    """Exception raised when operation results in an undefined quantity."""

    opSym = {operator.mul: '*',
             operator.truediv: '/',
             operator.floordiv: '//',
             operator.mod: '%',
             operator.pow: '**'
             }

    def __init__(self, op, operand1, operand2):
        if isinstance(operand1, QTermElem):
            operand1 = operand1.__class__.__name__
        if isinstance(operand2, QTermElem):
            operand2 = operand2.__class__.__name__
        QuantityError.__init__(self, "Undefined result: %s %s %s" %
                               (operand1, self.opSym[op], operand2))


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

    def __iter__(self):
        return iter(self._qtyList)


# Global registry of Quantities
_registry = QuantityRegistry()


def getUnitBySymbol(symbol):
    """Return the unit with symbol `symbol`.

    Args:
        symbol (str): symbol to look-up

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
            return qCls.Quantity._regIdx

    def __init__(self, name, bases, clsdict):
        type.__init__(self, name, bases, clsdict)
        try:
            self._clsDefinition = self.defineAs
            del self.defineAs
        except AttributeError:
            self._clsDefinition = None
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
                    unitClsDef = self._QClsDefinition(items)
                else:
                    unitClsDef = None
                unitCls = self.Unit = MetaQTerm(typearg(name + 'Unit'),
                                                (Unit,),
                                                {'Quantity': self,
                                                'defineAs': unitClsDef})
                # create and register reference unit
                symbol = clsdict.get('refUnitSymbol')
                name = clsdict.get('refUnitName')
                if symbol or self._refUnitDef:
                    unitCls._refUnit = unitCls(symbol, name)
                    # register reference unit converter
                    unitCls.registerConverter(RefUnitConverter())
                    # set Quantity.refUnitSymbol if not given
                    if not symbol:
                        self.refUnitSymbol = unitCls._refUnit.symbol
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
        return self._QClsDefinition([(self, 1)])

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
        """Return True is self is not derived from other quantity classes."""
        # base quantity -> class definition is None or empty term (_Unitless)
        return self._clsDefinition is None or len(self._clsDefinition) == 0

    def isDerivedQuantity(self):
        """Return True is self is derived from other quantity classes."""
        return not self.isBaseQuantity()

    @property
    def refUnit(self):
        try:
            return self.Unit.__dict__.get('_refUnit')
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

    class _QTerm(Term):
        """Definition of quantities."""

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
                return qty.Quantity._regIdx
            except AttributeError:
                return 0

        @staticmethod
        def convert(qty, into):
            """Return factor f so that f * into == qty.

            Raises TypeError if conversion is not possible."""
            return into(qty)

        @property
        def _numElem(self):
            try:
                firstElem = self[0][0]
            except IndexError:
                pass
            else:
                if self.isNumerical(firstElem):
                    return firstElem
            return None

        @property
        def amount(self):
            return self._numElem or Decimal(1)

        @property
        def unitTerm(self):
            if self._numElem is None:
                return self
            return self.__class__(self[1:])

    @property
    def definition(self):
        """The quantity's or units definition."""
        cls = self._QTerm
        if self.amount == 1:
            return cls([(self.unit, 1)])
        return cls([(self.amount, 1), (self.unit, 1)])

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
        """The elemets unit."""
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

    """Base class used to define types of quantity units."""

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
                raise ValueError("Symbol '%s' already registered." % symbol)
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
            unit._definition = defineAs
        else:
            raise TypeError("'defineAs' must be of type %s or %s; %s given"
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
            symbol (str): symbol to look-up

        Returns:
            :class:`Unit` sub-class: if a unit with given `symbol` exists
                within this :class:`Unit` sub-class
            None: otherwise
        """
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
        return iter(cls._converters)

    @property
    def definition(self):
        """Return the definition of the unit."""
        if self._definition is None:
            return self._QTerm(((self, 1),))
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
        return Decimal(1)

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
            except IncompatibleUnitsError:
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

    def __call__(self, qty):
        """Return number f so that type(qty)(f, self) == qty.

        Raises IncompatibleUnitsError if conversion not possible."""
        if qty.unit is self:            # same unit
            return qty.amount
        if self.Unit != qty.Unit:       # different Unit classes
            raise IncompatibleUnitsError("Can't convert '%s' to '%s'",
                                         qty.Quantity, self.Quantity)
        # try registered converters:
        for conv in self.registeredConverters():
            amnt = conv(qty, self)
            if amnt is not None:
                return amnt
        # if derived Unit class, try to convert base units:
        cls = self.Unit
        if cls.isDerivedQuantity():
            resDef = (qty.unit.normalizedDefinition /
                      self.normalizedDefinition)
            if len(resDef) <= 1:
                return qty.amount * resDef.amount
        # no success, give up
        raise IncompatibleUnitsError("Can't convert '%s' to '%s'",
                                     qty.unit.name, self.name)

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, NUM_TYPES):
            return self._QTerm(((other, 1), (self, 1)))
        elif isinstance(other, Unit):
            return self._QTerm(((self, 1), (other, 1)))
        elif isinstance(other, self._QTerm):
            return self._QTerm(((self, 1),)) * other
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, NUM_TYPES):
            return self._QTerm(((1 / other, 1), (self, 1)))
        elif isinstance(other, Unit):
            return self._QTerm(((self, 1), (other, -1)))
        elif isinstance(other, self._QTerm):
            return self._QTerm(((self, 1),)) / other
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, NUM_TYPES):
            return self._QTerm(((other, 1), (self, -1)))
        elif isinstance(other, self._QTerm):
            return other / self._QTerm(((self, 1),))
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        if not isinstance(exp, Integral):
            return NotImplemented
        return self._QTerm(((self, exp),))

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


class QuantityBase(QTermElem):

    """Abstract case class for `Quantity` and `_Unitless`."""

    # default format spec used in __format__
    dfltFormatSpec = ''

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
            except IndexError:
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
        return None

    @property
    def amount(self):
        """The quantity's amount, i.e. the numerical part of the quantity."""
        return NotImplementedError

    @property
    def unit(self):
        """Return the unit of the quantity."""
        return NotImplementedError

    def convert(self, toUnit):
        """Return quantity q where q == self and q.unit is toUnit.

        Args:
            toUnit (Unit): unit to be converted to

        Returns:
            Quantity: resulting quantity (of same type)

        Raises:
            IncompatibleUnitsError: self can't be converted to unit *toUnit*.
        """
        return self.Quantity(toUnit(self), toUnit)

    def __eq__(self, other):
        """self == other"""
        if isinstance(other, self.Quantity):
            try:
                return self.amount == self.unit(other)
            except IncompatibleUnitsError:
                pass
        return False

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        if isinstance(other, self.Quantity):
            return op(self.amount, self.unit(other))
        elif isinstance(other, QuantityBase):
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
            return self.Quantity(self.amount + self.unit(other), self.unit)
        elif isinstance(other, QuantityBase):
            raise IncompatibleUnitsError("Can't add a '%s' and a '%s'",
                                         self, other)
        return NotImplemented

    # other + self
    __radd__ = __add__

    def __sub__(self, other):
        """self - other"""
        if isinstance(other, self.Quantity):
            return self.Quantity(self.amount - self.unit(other), self.unit)
        elif isinstance(other, QuantityBase):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'",
                                         other, self)
        return NotImplemented

    def __rsub__(self, other):
        """other - self"""
        if isinstance(other, self.Quantity):
            return self.Quantity(other.amount - other.unit(self), other.unit)
        elif isinstance(other, QuantityBase):
            raise IncompatibleUnitsError("Can't subtract a '%s' from a '%s'",
                                         self, other)
        return NotImplemented

    def _getResQtyCls(self, other, op):
        """Return class resulting from op(self, other).

        op must be operator.mul, operator.truediv, operator.floordiv or
        operator.mod.
        Raises UndefinedResultError if resulting class is not defined."""
        resQtyDef = op(self.Quantity.clsDefinition,
                       other.Quantity.clsDefinition)
        if resQtyDef:
            try:
                return _registry.getQuantityCls(resQtyDef)
            except ValueError:
                raise UndefinedResultError(op, self, other)
        else:
            return _Unitless

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(self.amount * other, self.unit)
        elif isinstance(other, QuantityBase):
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
            return self.amount / self.unit(other)
        elif isinstance(other, QuantityBase):
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
        """round(self)

        Returns a copy of `self` with its amount rounded to the given
        `precision`.

        Note: this method is called by the standard `round` function only in
        Python 3.x!
        """
        return self.Quantity(Decimal(self.amount, precision), self.unit)

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


class _Unitless(QuantityBase):

    """Fake quantity without unit.

    Used to implement reversed operator rdiv."""

    __slots__ = ['_amount']

    # default format spec used in __format__
    dfltFormatSpec = '{a}'

    defineAs = MetaQTerm._QClsDefinition()

    def __new__(cls, amount):
        qty = super(QuantityBase, cls).__new__(cls)
        qty._amount = amount
        return qty

    @property
    def amount(self):
        return self._amount

    @property
    def unit(self):
        return None

    def __div__(self, other):
        """self / other"""
        if isinstance(other, QuantityBase):
            resQtyCls = self._getResQtyCls(other, operator.truediv)
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

# add references to the class itself
_Unitless.Quantity = _Unitless.Unit = _Unitless
# _Unitless must be registered before any quantity
# because it must get index 0 in order to be sorted to the first element
# in resulting terms and thus be handled like pure numerical elements !
_Unitless._regIdx = _registry.registerQuantityCls(_Unitless)
