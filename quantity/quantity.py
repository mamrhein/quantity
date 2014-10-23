# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        quantity
## Purpose:     Unit-safe computations with quantities
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software; you can redistribute it and/or
##              modify it under the terms of the GNU Lesser General Public
##              License as published by the Free Software Foundation; either
##              version 2 of the License, or (at your option) any later
##              version.
##              This program is distributed in the hope that it will be
##              useful, but WITHOUT ANY WARRANTY; without even the implied
##              warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##              PURPOSE.
##              See the GNU Lesser General Public License for more details.
##              You should have received a copy of the license text along with
##              this program; if not, get it from http://www.gnu.org/licenses,
##              or write to the Free Software Foundation, Inc.,
##              59 Temple Place, Suite 330, Boston MA 02111-1307, USA
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Unit-safe computations with quantities."""

#TODO: more documentation

from __future__ import absolute_import, division, unicode_literals
from numbers import Integral, Real
from decimal import Decimal
import operator
from .term import Term


__version__ = 0, 0, 1

__metaclass__ = type


# unicode handling and dict iterator Python 2 / Python 3
typearg = str       # first argument for type must be str in both
try:
    str = unicode   # make all strings unicode in Python 2
    itervalues = lambda d: d.itervalues()
except NameError:
    itervalues = lambda d: d.values()


# decorator defining meta class, portable between Python 2 / Python 3
def withMetaCls(metaCls):
    def _createCls(cls):
        return metaCls(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return _createCls


# because decimal.Decimal is not registered as number, we have to test it
# explicitly
NUM_TYPES = (Real, Decimal)


class QuantityError(TypeError):

    """Base class for quantity exceptions."""


class IncompatibleUnitsError(QuantityError):

    """Exception raised when operands do not have compatible units."""

    def __init__(self, msg, operand1, operand2):
        if isinstance(operand1, AbstractQuantity):
            operand1 = operand1.__class__.__name__
        if isinstance(operand2, AbstractQuantity):
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
        if isinstance(operand1, AbstractQuantity):
            operand1 = operand1.__class__.__name__
        if isinstance(operand2, AbstractQuantity):
            operand2 = operand2.__class__.__name__
        QuantityError.__init__(self, "Undefined result: %s %s %s" %
                              (operand1, self.opSym[op], operand2))


class QuantityRegistry():

    """Registers Quantity classes by definition."""

    def __init__(self):
        self._qtyReg = {}
        self._qtyIdx = 0

    def registerQuantityCls(self, qtyCls):
        """Register Quantity class."""
        qtyDef = qtyCls.normalizedClsDefinition
        try:
            regCls, idx = self._qtyReg[qtyDef]
            if regCls == qtyCls:
                return idx
            else:
                raise ValueError(
                    "Class with same definition already registered.")
        except KeyError:
            idx = self._qtyIdx = self._qtyIdx + 1
            self._qtyReg[qtyDef] = (qtyCls, idx)
            return idx

    def getQuantityCls(self, qtyDef):
        """Get Quantity class by definition."""
        return self._qtyReg[qtyDef][0]

    def getQuantityClsAndIdx(self, qtyDef):
        """Get Quantity class and its index by definition."""
        return self._qtyReg[qtyDef]


# Global registry of Quantities
_registry = QuantityRegistry()


class MetaQuantity(type):

    """Meta class that provides operators to construct derived quantities."""

    class QClsDefinition(Term):

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
            return qCls.Quantity.regIdx

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
            #register self
            self.regIdx = _registry.registerQuantityCls(self)
            # unit class given?
            try:
                unitCls = self.Unit
                if unitCls is None:
                    self.Unit = self
                else:
                    unitCls.Quantity = self
            except AttributeError:
                # create corresponding unit class
                qtyClsDef = self._clsDefinition
                if qtyClsDef:
                    items = ((qtyCls.Unit, exp) for qtyCls, exp in qtyClsDef)
                    unitClsDef = self.QClsDefinition(items)
                else:
                    unitClsDef = None
                unitCls = self.Unit = MetaQuantity(typearg(name + 'Unit'),
                                                   (Unit,),
                                                   {'Quantity': self,
                                                   'defineAs': unitClsDef})
                # create and register reference unit
                symbol = clsdict.get('refUnitSymbol', '')
                name = clsdict.get('refUnitName', '')
                if symbol or self._refUnitDef:
                    unitCls._refUnit = unitCls(symbol, name)
                    # register reference unit converter
                    unitCls.registerConverter(RefUnitConverter())
        # new Unit class:
        if 'Unit' in baseNames:
            # add reference to self
            self.Unit = self
            # initialize unit registry
            self._symDict = {}          # maps symbols to units
            self._termDict = {}         # maps normalized definitions to units
            # initialize converter registry
            self._converters = []

    def _asClsDefinition(self):
        return self.QClsDefinition([(self, 1)])

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
        return self.Unit.__dict__.get('_refUnit')

    @property
    def _refUnitDef(self):
        """Return definition of reference unit."""
        qtyDef = self.clsDefinition
        # check whether all base classes have a reference unit
        if any((qtyCls.refUnit is None for qtyCls, exp in qtyDef)):
            return None
        return self.QTerm(((qtyCls.refUnit, exp) for qtyCls, exp in qtyDef))

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, self.QClsDefinition):
            return self._asClsDefinition() * other
        else:
            return self._asClsDefinition() * other._asClsDefinition()

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, self.QClsDefinition):
            return self._asClsDefinition() / other
        else:
            return self._asClsDefinition() / other._asClsDefinition()

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, self.QClsDefinition):
            return other / self._asClsDefinition()
        else:
            return other._asClsDefinition() / self._asClsDefinition()

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        return self.clsDefinition ** exp

    def __str__(self):
        return self.__name__


@withMetaCls(MetaQuantity)
class AbstractQuantity:

    """Abstract base class for Quantity and Unit."""

    class QTerm(Term):
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
                return qty.Quantity.regIdx
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
        cls = self.QTerm
        if self.amount == 1:
            return cls([(self.unit, 1)])
        return cls([(self.amount, 1), (self.unit, 1)])

    @property
    def normalizedDefinition(self):
        if self.unit.isBaseUnit():
            return self.definition
        else:
            return self.definition.normalized()

    @property
    def amount(self):
        """The quantity's amount."""
        raise NotImplementedError

    @property
    def unit(self):
        """The quantity's unit."""
        raise NotImplementedError

    @property
    def refUnit(self):
        """Return reference unit of Quantity, if defined, otherwise None."""
        return self.Unit.refUnit

    def convert(self, toUnit):
        """Return quantity q where q == self and q.unit is toUnit.

        Raises IncompatibleUnitsError if self can't be converted to given
        unit."""
        return self.Quantity(toUnit(self), toUnit)

    def __copy__(self):
        """Return self (AbstractQuantity instances are immutable)."""
        return self

    def __deepcopy__(self, memo):
        return self.__copy__()

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        return NotImplemented

    def __eq__(self, other):
        """self == other"""
        return self._compare(other, operator.eq)

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


class Quantity(AbstractQuantity):

    __slots__ = ['_amount', '_unit']

    # default format spec used in __format__
    dfltFormatSpec = '{a} {u}'

    def __init__(self, amount, unit=None):
        if not isinstance(amount, NUM_TYPES):
            amount = Decimal(amount)
        self._amount = amount
        self._unit = unit = unit or self.refUnit
        if not unit:
            raise ValueError("A unit must be given.")
        if not isinstance(unit, self.Unit):
            raise TypeError("Given unit is not a %s." % self.Unit.__name__)

    @classmethod
    def fromQTerm(cls, qTerm):
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

    def __getstate__(self):
        return self._amount, self._unit.symbol

    def __setstate__(self, state):
        amount, symbol = state
        self._amount = amount
        self._unit = self.Unit(symbol)

    @property
    def amount(self):
        return self._amount

    @property
    def unit(self):
        return self._unit

    def _compare(self, other, op):
        """Compare self and other using operator op."""
        if isinstance(other, self.Quantity):
            return op(self.amount, self.unit(other))
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't compare a %s and a %s",
                                         self, other)
        return NotImplemented

    def __hash__(self):
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
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't add a %s and a %s",
                                         self, other)
        return NotImplemented

    # other + self
    __radd__ = __add__

    def __sub__(self, other):
        """self - other"""
        if isinstance(other, self.Quantity):
            return self.Quantity(self.amount - self.unit(other), self.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a %s from a %s",
                                         other, self)
        return NotImplemented

    def __rsub__(self, other):
        """other - self"""
        if isinstance(other, self.Quantity):
            return self.Quantity(other.amount - other.unit(self), other.unit)
        elif isinstance(other, Quantity):
            raise IncompatibleUnitsError("Can't subtract a %s from a %s",
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
                return _registry.getQuantityCls(resQtyDef.normalized())
            except KeyError:
                raise UndefinedResultError(op, self, other)
        else:
            return _Unitless

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
                return resQtyCls.fromQTerm(resQTerm)
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(self.amount / other, self.unit)
        if isinstance(other, self.Quantity):
            return self.amount / self.unit(other)
        elif isinstance(other, Quantity):
            resQtyCls = self._getResQtyCls(other, operator.truediv)
            resQTerm = (self.amount / other.amount) * (self.unit / other.unit)
            if resQtyCls is _Unitless:
                return resQTerm.normalized().amount
            else:
                return resQtyCls.fromQTerm(resQTerm)
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
        except KeyError:
            raise UndefinedResultError(operator.pow, self, exp)
        resQTerm = self.amount ** exp * self.unit ** exp
        return resQtyCls.fromQTerm(resQTerm)

    def __round__(self, precision=0):
        """round(self)

        In 3.x round changed from half-up to half-even!"""
        return self.Quantity(round(self.amount, precision), self.unit)

    def __repr__(self):
        if self.unit.isRefUnit():
            return "%s(%s)" % (self.__class__.__name__, repr(self.amount))
        else:
            return "%s(%s, %s)" % (self.__class__.__name__, repr(self.amount),
                                   repr(self.unit))

    def __str__(self):
        return "%s %s" % (self.amount, self.unit)

    def __lstr__(self):
        return self.__format__('{a:n} {u}')

    def __format__(self, fmtSpec=""):
        """Convert to string (according to format specifier).

        The specifier should be a standard format specifier,
        with the form described in PEP 3101.
        It should use two keys: 'a' for self.amount and 'u' for self.unit,
        where 'a' can be followed by a valid format spec for numbers and
        'u' by a valid format spec for strings.
        """
        if not fmtSpec:
            fmtSpec = self.dfltFormatSpec
        return fmtSpec.format(a=self.amount, u=self.unit)

#TODO: implement Quantity.allocate


class Unit(AbstractQuantity):

    __slots__ = ['_symbol', '_name', '_definition']

    def __new__(cls, symbol, name=None, defineAs=None):
        if not symbol:
            if defineAs is None:
                if cls.Quantity.isDerivedQuantity():
                    # try to generate symbol for reference unit of derived
                    # quantity:
                    refUnitDef = cls._refUnitDef
                    if refUnitDef:
                        symbol = str(refUnitDef)
            elif isinstance(defineAs, cls.QTerm):
                # try to generate symbol from definition:
                if defineAs.amount == 1:
                    symbol = str(defineAs)
        if not symbol:
            raise ValueError("Symbol must be given for unit.")
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
        elif isinstance(defineAs, cls.QTerm):
            unit._definition = defineAs
        else:
            raise TypeError("'defineAs' must be of type %s or %s; %s given"
                            % (cls.Quantity, cls.QTerm, type(defineAs)))
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
    def registerConverter(cls, conv):
        """Add converter conv to the list of converters registered in cls.

        Does nothing if converter is already registered."""
        if not conv in cls._converters:
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
        if self._definition is None:
            return self.QTerm(((self, 1),))
        return self._definition

    @property
    def symbol(self):
        """Unique string representation of self.

        Used for str, repr, format, hash and unit registry."""
        return self._symbol

    @property
    def name(self):
        return self._name or self._symbol

    @property
    def amount(self):
        return Decimal(1)

    @property
    def unit(self):
        return self

    def isRefUnit(self):
        return self is self.refUnit

    def isBaseUnit(self):
        return self._definition is None

    def isDerivedUnit(self):
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
            raise IncompatibleUnitsError("Can't convert %s to %s",
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
        raise IncompatibleUnitsError("Can't convert %s to %s",
                                     qty.unit.name, self.name)

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, NUM_TYPES):
            return self.QTerm(((other, 1), (self, 1)))
        elif isinstance(other, Unit):
            return self.QTerm(((self, 1), (other, 1)))
        return NotImplemented

    # other * self
    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        if isinstance(other, NUM_TYPES):
            return self.QTerm(((1 / other, 1), (self, 1)))
        elif isinstance(other, Unit):
            return self.QTerm(((self, 1), (other, -1)))
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, NUM_TYPES):
            return self.QTerm(((other, 1), (self, -1)))
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, exp):
        """self ** exp"""
        if not isinstance(exp, Integral):
            return NotImplemented
        return self.QTerm(((self, exp),))

    def __rxor__(self, other):
        """other ^ self

        Alternate constructor for quantity:
        other ^ self  ->  self.Quantity(other, self)

        Raises TypeError if other is not a Real number."""
        if isinstance(other, NUM_TYPES):
            return self.Quantity(other, self)
        return NotImplemented

    def __repr__(self):
        return "%s.Unit(%s)" % (self.Quantity.__name__, repr(self.symbol))

    def __str__(self):
        return "%s" % self.symbol

    def __format__(self, fmtSpec):
        """Convert to string (according to fmtSpec).

        fmtSpec must be a valid format spec for strings.
        """
        return format(self.symbol, fmtSpec)


#
# helper classes and functions
#


class _Unitless(Quantity):

    """Fake quantity without unit.

    Used to implement reversed operator rdiv."""

    defineAs = MetaQuantity.QClsDefinition()
    Unit = None

    def __init__(self, amount):
        self._amount = amount

    @property
    def unit(self):
        return None

    def __div__(self, other):
        """self / other"""
        if isinstance(other, Quantity):
            resQtyCls = self._getResQtyCls(other, operator.truediv)
            resQTerm = (self.amount / other.amount) / other.unit
            return resQtyCls.fromQTerm(resQTerm)
        return NotImplemented

    __truediv__ = __div__

    def __str__(self):
        return "%s" % (self.amount)

    def __lstr__(self):
        return self.__format__('{a:n}')

    def __format__(self, fmtSpec=""):
        if not fmtSpec:
            fmtSpec = '{a}'
        return fmtSpec.format(a=self.amount, u='')


class Converter:

    """Convert a quantity's amount to the equivalent amount for another
    unit.

    A quantity converter can be any callable with a signature like
    conv(qty, toUnit) -> number f so that type(qty)(f, toUnit) == qty.

    Must return None if conversion can not be done."""

    def __call__(self, qty, toUnit):
        return None


class RefUnitConverter:

    """Converter for Quantity classes that have a reference unit."""

    def __call__(self, qty, toUnit):
        """Return f so that type(qty)(f, toUnit) == qty."""
        if qty.unit is toUnit:          # same unit
            return qty.amount
        if qty.Unit == toUnit.Unit:     # same Unit class
            resDef = (qty.unit.normalizedDefinition
                      / toUnit.normalizedDefinition)
            return qty.amount * resDef.amount
        return None


class TableConverter:

    """Converter using a conversion table."""

    def __init__(self, convTable):
        if isinstance(convTable, dict):
            self._unitMap = convTable
        elif isinstance(convTable, list):
            self._unitMap = unitMap = {}
            for (fromUnitSymbol, toUnitSymbol, factor) in convTable:
                unitMap[(fromUnitSymbol, toUnitSymbol)] = factor
        else:
            raise TypeError("A dict or list must be given.")

    def __call__(self, qty, toUnit):
        """Return f so that type(qty)(f, toUnit) == qty."""
        if qty.unit is toUnit:          # same unit
            return qty.amount
        try:
            factor = self._unitMap[(qty.unit.symbol, toUnit.symbol)]
        except KeyError:
            # try reverse
            try:
                factor = 1 / self._unitMap[(toUnit.symbol, qty.unit.symbol)]
            except KeyError:
                return None
        return factor * qty.amount
