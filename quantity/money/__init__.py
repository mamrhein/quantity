# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        money (package)
## Purpose:     Currency-safe computations with money amounts.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2013 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Currency-safe computations with money amounts.

Money derives from Quantity, so all operations on quantities can also be
apllied to instances of Money. All amounts of money are rounded according to
the smallest fraction defined for the currency.
"""


from __future__ import absolute_import, division, unicode_literals
from numbers import Integral
from decimalfp import Decimal
from .. import Quantity, Unit


# unicode handling Python 2 / Python 3
str = type(u'')
bytes = type(b'')
str_types = (bytes, str)


__metaclass__ = type


class Currency(Unit):

    """Represents a currency, i.e. a money unit.

        Args:
            isoCode (string): ISO 4217 3-character code
            name (string): name of the currency
            minorUnit (Integral): amount of minor unit (as exponent to 10),
                optional, defaults to precision of smallest fraction, if that
                is given, otherwise to 2
            smallestFraction (number): smallest fraction available for the
                currency, optional, defaults to Decimal(10) ** -minorUnit

        Returns:
            :class:`Currency` instance

        Raises:
            TypeError: given `isoCode` is not a string
            ValueError: no `isoCode` was given
            TypeError: given `minorUnit` is not an Integral number
            ValueError: given `minorUnit` < 0
            TypeError: given `smallestFraction` can not be converted to a
                Decimal
            ValueError: given `smallestFraction` not > 0 or not <= 1
            ValueError: given `smallestFraction` does not fit given
                `minorUnit`
    """

    __slots__ = ['_precision', '_smallestFraction']

    def __new__(cls, isoCode, name=None, minorUnit=None,
                smallestFraction=None):
        """Create `Currency` instance."""
        if not isinstance(isoCode, str_types):
            raise TypeError("IsoCode must be a string.")
        if not isoCode:
            raise ValueError("IsoCode must be given.")
        if minorUnit is not None:
            if not isinstance(minorUnit, Integral):
                raise TypeError("minorUnit must be an Integral number.")
            if minorUnit < 0:
                raise ValueError("minorUnit must be >= 0.")
        if smallestFraction is None:
            if minorUnit is None:
                precision = 2
            else:
                precision = minorUnit
        else:
            smallestFraction = Decimal(smallestFraction)
            if minorUnit is None:
                if smallestFraction < 0 or smallestFraction > 1:
                    raise ValueError("smallestFraction must be > 0 and <= 1.")
                precision = smallestFraction.precision
            else:
                precision = minorUnit
                if precision != smallestFraction.precision:
                    raise ValueError(
                        "smallestFraction does not fit minorUnit.")
        curr = Unit.__new__(cls, isoCode, name)
        curr._precision = precision
        curr._smallestFraction = smallestFraction
        return curr

    @property
    def isoCode(self):
        """ISO 4217 3-character code."""
        return self._symbol

    @property
    def name(self):
        """Name of this currency."""
        return self._name or self._isoCode

    @property
    def smallestFraction(self):
        """The smallest fraction available for this currency."""
        return self._smallestFraction or Decimal(10) ** -self._precision

    def round(self, amount):
        """Round amount according to smallest fraction of self."""
        smf = self._smallestFraction
        if smf:
            return Decimal(amount / smf, 0) * smf
        else:
            return Decimal(amount, self._precision)

    def __repr__(self):
        """repr(self)"""
        return "%s(%s)" % (self.__class__.__name__, repr(self.symbol))


class Money(Quantity):

    """Represents a money amount, i.e. the combination of a numerical value
    and a money unit, aka. currency.

    Instances of `Money` can be created in two ways, by providing a numerical
    amount and a `Currency` or by providing a string representation of a money
    amount.

    **1. Form**

    Args:
        amount (number): money amount (gets rounded to a Decimal according
            to smallest fraction of currency)
        currency(Currency): money unit

    `amount` must convertable to a `decimalfp.Decimal`.

    Raises:
        TypeError: `amount` can not be converted to a Decimal number
        ValueError: no currency given

    **2. Form**

    Args:
        mStr(string): unicode string representation of a money amount (incl.
            currency symbol)
        currency: the money's unit (optional)

    `mStr` must contain a numerical value and a currency symbol, separated
    atleast by one blank. Any surrounding white space is ignored. If
    `currency` is given in addition, the resulting money's currency is set to
    this currency and its amount is converted accordingly, if possible.

    Raises:
        TypeError: amount given in `mStr` can not be converted to a Decimal
            number
        ValueError: no currency given
        TypeError: a byte string is given that can not be decoded using the
            standard encoding
        ValueError: given string does not represent a `Money` amount
        IncompatibleUnitsError: the currency derived from the symbol given in
            `mStr` can not be converted to given `currency`
    """

    Unit = Currency

    @classmethod
    def getQuantum(cls, unit):
        """Return the smallest amount an instance of :class:`Money` can take
        for `unit`."""
        return unit.smallestFraction

    @property
    def currency(self):
        """The money's currency, i.e. its unit."""
        return self._unit


class ExchangeRate:

    """Basic representation of a conversion factor between two currencies.

    Args:
        unitCurrency (Currency): currency to be converted from, aka base
            currency
        unitMultiple (number): amount of base currency
        termCurrency (Currency): currency to be converted to, aka price
            currency
        termAmount (number): equivalent amount of price currency

    1 USD = 0.7683 EUR   =>   ExchangeRate('USD', 1, 'EUR', 0.7683)

    The given `termAmount` will always be rounded to 6 decimal digits.

    If the given `unitMultiple` is not a power of 10, it will be adjusted to
    the next power of 10 and the `termAmount` will be adjusted accordingly.
    """

    def __init__(self, unitCurrency, unitMultiple, termCurrency, termAmount):
        """Initialize new instance of ExchangeRate."""
        assert isinstance(unitCurrency, Currency)
        assert isinstance(termCurrency, Currency)
        assert unitCurrency != termCurrency
        self._unitCurrency = unitCurrency
        self._termCurrency = termCurrency
        if unitMultiple == 1 or unitMultiple % 10 == 0:
            self._unitMultiple = Decimal(unitMultiple)
            self._termAmount = Decimal(termAmount, 6)
        else:
            factor = Decimal(unitMultiple)
            self._unitMultiple = unitMultiple = (Decimal(10)
                                                 ** factor.magnitude)
            self._termAmount = Decimal(termAmount) * unitMultiple / factor

    @property
    def unitCurrency(self):
        """Currency to be converted from, aka base currency."""
        return self._unitCurrency

    @property
    def termCurrency(self):
        """Currency to be converted to, aka price currency."""
        return self._termCurrency

    @property
    def rate(self):
        """Relative value of termCurrency to unitCurrency."""
        return self._termAmount / self._unitMultiple

    @property
    def inverseRate(self):
        """Inverted rate, i.e. relative value of unitCurrency to
        termCurrency."""
        return self._unitMultiple / self._termAmount

    @property
    def quotation(self):
        """Tuple of unitCurrency, termCurrency and rate."""
        return (self._unitCurrency, self._termCurrency, self.rate)

    @property
    def inverseQuotation(self):
        """Tuple of termCurrency, unitCurrency and reverseRate."""
        return (self._termCurrency, self._unitCurrency, self.reverseRate)

    def inverted(self):
        """Return inverted exchange rate."""
        return ExchangeRate(self._termCurrency, 1, self._unitCurrency,
                            self.inverseRate)

    def __hash__(self):
        """hash(self)"""
        return hash(self.quotation)

    def __eq__(self, other):
        """self == other"""
        if isinstance(other, ExchangeRate):
            return self.quotation == other.quotation
        return False

    def __mul__(self, other):
        """self * other"""
        if isinstance(other, Money):
            if other.unit is self.unitCurrency:
                return other.__class__(other.amount * self.rate,
                                       self.termCurrency)
            raise ValueError("Can't multiply '%s' and '%s/%s'"
                             % (other.unit, self.termCurrency,
                                self.unitCurrency))
        return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, Money):
            if other.unit is self.termCurrency:
                return other.__class__(other.amount * self.reverseRate,
                                       self.unitCurrency)
            raise ValueError("Can't divide '%s' by '%s/%s'"
                             % (other.unit, self.termCurrency,
                                self.unitCurrency))
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __repr__(self):
        """repr(self)"""
        return "%s%s" % (self.__class__.__name__,
                         repr((self.unitCurrency, self._unitMultiple,
                               self.termCurrency, self._termAmount)))

    def __str__(self):
        """str(self)"""
        return "%s %s/%s" % (self.rate, self.termCurrency, self.unitCurrency)
