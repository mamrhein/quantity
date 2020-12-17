# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        moneybase
# Purpose:     Base classes for computations with money amounts.
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2013 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Base classes for computations with money amounts"""


from fractions import Fraction
import math
from numbers import Integral

from decimalfp import Decimal

from ..qtybase import Quantity, Unit, QuantityError


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

    `smallestFraction` can also be given as a string, as long as it is
    convertable to a Decimal.

    Returns:
        :class:`Currency` instance

    Raises:
        TypeError: given `isoCode` is not a string
        ValueError: no `isoCode` was given
        TypeError: given `minorUnit` is not an Integral number
        ValueError: given `minorUnit` < 0
        ValueError: given `smallestFraction` can not be converted to a
            Decimal
        ValueError: given `smallestFraction` not > 0
        ValueError: 1 is not an integer multiple of given
            `smallestFraction`
        ValueError: given `smallestFraction` does not fit given
            `minorUnit`
    """

    __slots__ = ['_smallestFraction']

    def __new__(cls, isoCode, name=None, minorUnit=None,
                smallestFraction=None):
        """Create `Currency` instance."""
        if not isinstance(isoCode, str):
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
                smallestFraction = Decimal('0.01')
            else:
                smallestFraction = Decimal(10) ** -minorUnit
        else:
            smallestFraction = Decimal(smallestFraction)
            if minorUnit is None:
                if smallestFraction < 0:
                    raise ValueError("smallestFraction must be > 0.")
                multiple = 1 / smallestFraction
                if not (multiple.denominator == 1 and multiple.numerator > 1):
                    raise ValueError("1 must be an integer multiple of given "
                                     "smallestFraction.")
            else:
                if minorUnit != smallestFraction.precision:
                    raise ValueError(
                        "smallestFraction does not fit minorUnit.")
        curr = Unit.__new__(cls, isoCode, name)
        curr._smallestFraction = smallestFraction
        return curr

    @classmethod
    def registerConverter(cls, conv):
        """Add converter 'conv' to the list of converters registered in 'cls'.

        Money converters should not be registered directly by using this
        method. Instead, this should be done by using them as context managers
        in a 'with' statement."""
        cls._converters.append(conv)

    @classmethod
    def removeConverter(cls, conv):
        """Remove the last instance of converter 'conv' from the list of
        converters registered in 'cls'.

        Raises ValueError if 'conv' is not the most recently registered
        converter in 'cls'.

        That means that money converters must be unregistered in reversed
        order of registration. To enforce this, money converters should be
        registered and unregistered by using them as context managers in a
        'with' statement."""
        if cls._converters[-1] is conv:
            cls._converters.pop()
        elif conv in cls._converters:
            raise ValueError("Attempt to unregister converter which is not "
                             "the most recently registered one.")
        else:
            raise ValueError("Attempt to unregister an unregistered "
                             "converter.")

    @property
    def isoCode(self):
        """ISO 4217 3-character code."""
        return self._symbol

    @property
    def smallestFraction(self):
        """The smallest fraction available for this currency."""
        return self._smallestFraction

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

    `amount` must convertable to a `decimalfp.Decimal`, it can also be given
    as a string.

    Returns:
        :class:`Money` instance

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

    Returns:
        :class:`Money` instance

    Raises:
        TypeError: amount given in `mStr` can not be converted to a Decimal
            number
        ValueError: no currency given
        TypeError: a byte string is given that can not be decoded using the
            standard encoding
        ValueError: given string does not represent a `Money` amount
        :exp:`~quantity.IncompatibleUnitsError`: the currency derived from
            the symbol given in `mStr` can not be converted to given
            `currency`
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
        unitMultiple (Integral): amount of base currency
        termCurrency (Currency): currency to be converted to, aka price
            currency
        termAmount (number): equivalent amount of term currency

    `unitCurrency` and `termCurrency` can also be given as 3-character ISO
    4217 codes of already registered currencies.

    `unitMultiple` must be > 1. It can also be given as a string, as long as
    it is convertable to an Integral.

    `termAmount` can also be given as a string, as long as it is convertable
    to a number.

    Example:

    1 USD = 0.9683 EUR   =>   ExchangeRate('USD', 1, 'EUR', '0.9683')

    Returns:
        :class:`ExchangeRate` instance

    `unitMultiple` and `termAmount` will always be adjusted so that
    the resulting unit multiple is a power to 10 and the resulting term
    amounts magnitude is >= -1. The latter will always be rounded to 6
    decimal digits.

    Raises:
        ValueError: unknown ISO 4217 code given for a currency
        TypeError: value of type other than `Currency` or string given for a
            currency
        ValueError: currencies given are identical
        ValueError: unit multiple is not an Integral or is not >= 1
        ValueError: term amount is not >= 0.000001
        ValueError: unit multiple or term amount can not be converted to a
            Decimal
    """

    def __init__(self, unitCurrency, unitMultiple, termCurrency, termAmount):
        if not isinstance(unitCurrency, Currency):
            if isinstance(unitCurrency, str):
                unitCurrSym = unitCurrency
                unitCurrency = Currency.get_unit_by_symbol(unitCurrSym)
                if unitCurrency is None:
                    raise ValueError("Unknown ISO 4217 code: '%s'."
                                     % unitCurrSym)
            else:
                raise TypeError("Can't use a '%s' as unit currency."
                                % type(unitCurrency))
        if not isinstance(termCurrency, Currency):
            if isinstance(termCurrency, str):
                termCurrSym = termCurrency
                termCurrency = Currency.get_unit_by_symbol(termCurrSym)
                if termCurrency is None:
                    raise ValueError("Unknown ISO 4217 code: '%s'."
                                     % termCurrSym)
            else:
                raise TypeError("Can't use a '%s' as term currency."
                                % type(termCurrency))
        if unitCurrency is termCurrency:
            raise ValueError("The currencies given must not be identical.")
        self._unitCurrency = unitCurrency
        self._termCurrency = termCurrency
        unitMultiple = Decimal(unitMultiple).adjusted()
        if unitMultiple.precision > 0:
            raise ValueError("Unit multiple must be an Integral.")
        if unitMultiple < 1:
            raise ValueError("Unit multiple must be >= 1.")
        if isinstance(termAmount, Decimal):
            mgntTermAmount = termAmount.magnitude
        else:
            termAmount = Fraction(termAmount)
            mgntTermAmount = int(math.floor(math.log10(abs(termAmount))))
        if mgntTermAmount < -6:
            raise ValueError("Term amount must be >= 0.000001.")
        # adjust unitMultiple and termAmount so that
        # unitMultiple is a power to 10 and termAmount.magnitude >= -1
        mult = Decimal(10) ** (unitMultiple.magnitude
                               - min(0, mgntTermAmount + 1))
        self._unitMultiple = mult
        self._termAmount = Decimal(termAmount * mult / unitMultiple, 6)

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
        """Tuple of termCurrency, unitCurrency and inverseRate."""
        return (self._termCurrency, self._unitCurrency, self.inverseRate)

    def inverted(self):
        """Return inverted exchange rate."""
        return ExchangeRate(self._termCurrency, 1, self._unitCurrency,
                            self.inverseRate)

    @property
    def _definition(self):
        """Return self as QTerm."""
        return Quantity._QTerm(((self.rate, 1), (self.termCurrency, 1),
                                (self.unitCurrency, -1)))

    def __hash__(self):
        """hash(self)"""
        return hash(self.quotation)

    def __eq__(self, other):
        """self == other

        Args:
            other (object): object to compare with

        Returns:
            True if other is an instance of ExchangeRate and
            self.quotation == other.quotation, False otherwise
        """
        if isinstance(other, ExchangeRate):
            return self.quotation == other.quotation
        return False

    def __mul__(self, other):
        """self * other

        **1. Form**

        Args:
            other (:class:`Money`): money amount to multiply with

        Returns:
            :class:`Money` instance: equivalent of `other` in term currency

        Raises:
            ValueError: currency of `other` is not equal to unit currency

        **2. Form**

        Args:
            other (:class:`ExchangeRate`): exchange rate to multiply with

        Returns:
            :class:`ExchangeRate` instance: "triangulated" exchange rate

        Raises:
            ValueError: unit currency of one multiplicant does not equal the
                term currency of the other multiplicant

        **3. Form**

        Args:
            other (:class:`Quantity` sub-class): quantity to multiply with

        The type of `other` must be a sub-class of :class:`Quantity` derived
        from :class:`Money` divided by some other sub-class of
        :class:`Quantity`.

        Returns:
            :class:`Quantity` sub-class instance: equivalent of `other` in
                term currency

        Raises:
            ValueError: resulting unit is not defined
        """
        if isinstance(other, Money):
            if other.unit is self.unitCurrency:
                return other.__class__(other.amount * self.rate,
                                       self.termCurrency)
            raise ValueError("Can't multiply '%s' and '%s/%s'."
                             % (other.unit, self.termCurrency,
                                self.unitCurrency))
        if isinstance(other, ExchangeRate):
            if self.unitCurrency is other.termCurrency:
                return ExchangeRate(other.unitCurrency, 1, self.termCurrency,
                                    self.rate * other.rate)
            elif self.termCurrency is other.unitCurrency:
                return ExchangeRate(self.unitCurrency, 1, other.termCurrency,
                                    self.rate * other.rate)
            else:
                raise ValueError("Can't multiply '%s/%s' and '%s/%s'."
                                 % (self.termCurrency, self.unitCurrency,
                                    other.termCurrency, other.unitCurrency))
        if isinstance(other, Quantity):
            resTerm = other.normalizedDefinition * self._definition
            try:
                return other.Quantity._fromQTerm(resTerm)
            except TypeError:
                raise QuantityError("Resulting unit not defined: %s."
                                    % resTerm.unitTerm)
        return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other

        Args:
            other (:class:`ExchangeRate`): exchange rate to divide with

        Returns:
            :class:`ExchangeRate` instance: "triangulated" exchange rate

        Raises:
            ValueError: unit currencies of operands not equal and term
                currencies of operands not equal
        """
        if isinstance(other, ExchangeRate):
            if self.unitCurrency is other.unitCurrency:
                return ExchangeRate(other.termCurrency, 1, self.termCurrency,
                                    self.rate / other.rate)
            elif self.termCurrency is other.termCurrency:
                return ExchangeRate(self.unitCurrency, 1, other.unitCurrency,
                                    self.rate / other.rate)
            else:
                raise ValueError("Can't divide '%s/%s' by '%s/%s'."
                                 % (self.termCurrency, self.unitCurrency,
                                    other.termCurrency, other.unitCurrency))
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self

        **1. Form**

        Args:
            other (:class:`Money`): money amount to divide

        Returns:
            :class:`Money` instance: equivalent of `other` in unit currency

        Raises:
            ValueError: currency of `other` is not equal to term currency

        **2. Form**

        Args:
            other (:class:`Quantity` sub-class): quantity to divide

        The type of `other` must be a sub-class of :class:`Quantity` derived
        from :class:`Money` divided by some other sub-class of
        :class:`Quantity`.

        Returns:
            :class:`Quantity` sub-class instance: equivalent of `other` in
                unit currency

        Raises:
            :class:`~quantity.QuantityError`: resulting unit is not defined
        """
        if isinstance(other, Money):
            if other.unit is self.termCurrency:
                return other.__class__(other.amount * self.inverseRate,
                                       self.unitCurrency)
            raise ValueError("Can't divide '%s' by '%s/%s'"
                             % (other.unit, self.termCurrency,
                                self.unitCurrency))
        if isinstance(other, Quantity):
            resTerm = other.normalizedDefinition / self._definition
            try:
                return other.Quantity._fromQTerm(resTerm)
            except TypeError:
                raise QuantityError("Resulting unit not defined: %s."
                                    % resTerm.unitTerm)
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