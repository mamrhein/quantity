# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        money (package)
# Purpose:     Currency-safe computations with money amounts.
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2013 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$

"""Currency-safe computations with money amounts.

Usage
=====

Registering a currency
----------------------

A currency must explicitly be registered as a unit for further use. The
easiest way to do this is to call :meth:`Money.register_currency`:

    >>> from quantity.money import Money
    >>> EUR = Money.register_currency('EUR')
    >>> HKD = Money.register_currency('HKD')
    >>> TND = Money.register_currency('TND')
    >>> USD = Money.register_currency('USD')
    >>> EUR, HKD, TND, USD
    (Currency('EUR'), Currency('HKD'), Currency('TND'), Currency('USD'))

The method is backed by a database of currencies defined in ISO 4217. It
takes the 3-character ISO 4217 code as parameter.

:class:`Currency` derives from :class:`~quantity.Unit`. Each instance has a
symbol (which is usually the 3-character ISO 4217 code) and a name. In
addition, it holds the smallest fraction defined for amounts in this currency:

    >>> TND.symbol
    'TND'
    >>> TND.name
    'Tunisian Dinar'
    >>> TND.smallest_fraction
    Decimal('0.001')

Instantiating a money amount
----------------------------

As :class:`Money` derives from :class:`~quantity.Quantity`, an instance can
simply be created by giving an amount and a unit:

    >>> Money(30, EUR)
    Money(Decimal(30, 2), Currency('EUR'))

All amounts of money are rounded according to the smallest fraction defined
for the currency:

    >>> Money(3.128, EUR)
    Money(Decimal('3.13'), Currency('EUR'))
    >>> Money(41.1783, TND)
    Money(Decimal('41.178'), Currency('TND'))

As with other quantities, money amounts can also be derived from a string or
build using the operator `*`:

    >>> Money('3.18 USD')
    Money(Decimal('3.18'), Currency('USD'))
    >>> 3.18 * USD
    Money(Decimal('3.18'), Currency('USD'))

Computing with money amounts
----------------------------

:class:`Money` derives from :class:`~quantity.Quantity`, so all operations on
quantities can also be applied to instances of :class:`Money`. But because
there is no fixed relation between currencies, there is no implicit conversion
between money amounts of different currencies:

    >>> Money(30, EUR) + Money(3.18, EUR)
    Money(Decimal('33.18'), Currency('EUR'))
    >>> Money(30, EUR) + Money(3.18, USD)
    Traceback (most recent call last):
    UnitConversionError: Can't convert 'USD' to 'EUR'

Resulting values are always quantized to the smallest fraction defined with
the currency:

    >>> Money('3.20 USD') / 3
    Money(Decimal('1.07'), Currency('USD'))
    >>> Money('3.20 TND') / 3
    Money(Decimal('1.067'), Currency('TND'))

Converting between different currencies
---------------------------------------

Exchange rates
^^^^^^^^^^^^^^

A conversion factor between two currencies can be defined by using the
:class:`ExchangeRate`. It is given a unit currency (aka base currency), a unit
multiple, a term currency (aka price currency) and a term amount, i.e. the
amount in term currency equivalent to unit multiple in unit currency:

    >>> fxEUR2HKD = ExchangeRate(EUR, 1, HKD, Decimal('8.395804'))
    >>> fxEUR2HKD
    ExchangeRate(Currency('EUR'), Decimal(1), Currency('HKD'), \
Decimal('8.395804'))

`unit_multiple` and `term_amount` will always be adjusted so that the resulting
unit multiple is a power to 10 and the resulting term amounts magnitude is >=
-1. The latter will always be rounded to 6 decimal digits:

    >>> fxTND2EUR = ExchangeRate(TND, 5, EUR, Decimal('0.0082073'))
    >>> fxTND2EUR
    ExchangeRate(Currency('TND'), Decimal(100), Currency('EUR'), \
Decimal('0.164146'))

The resulting rate for an amount of 1 unit currency in term currency can be
obtained via the property :attr:`ExchangeRate.rate`:

    >>> fxTND2EUR.rate
    Decimal('0.00164146')

The property :attr:`ExchangeRate.quotation` gives a tuple of unit currency,
term currency and rate:

    >>> fxTND2EUR.quotation
    (Currency('TND'), Currency('EUR'), Decimal('0.00164146'))

The properties :attr:`ExchangeRate.inverseRate` and
:attr:`ExchangeRate.inverseQuotation` give the rate and the quotation in the
opposite direction (but do not round the rate!):

    >>> fxTND2EUR.inverse_rate
    Fraction(50000000, 82073)
    >>> fxTND2EUR.inverse_quotation
    (Currency('EUR'), Currency('TND'), Fraction(50000000, 82073))

The inverse ExchangeRate can be created by calling the method
:meth:`ExchangeRate.inverted`:

    >>> fxEUR2TND = fxTND2EUR.inverted()
    >>> fxEUR2TND
    ExchangeRate(Currency('EUR'), Decimal(1), Currency('TND'), \
Decimal('609.213749'))

An exchange rate can be derived from two other exchange rates, provided that
they have one currency in common ("triangulation"). If the unit currency of
one exchange rate is equal to the term currency of the other, the two exchange
rates can be multiplied with each other. If either the unit currencies or the
term currencies are equal, the two exchange rates can be divided:

    >>> fxEUR2HKD * fxTND2EUR
    ExchangeRate(Currency('TND'), Decimal(10), Currency('HKD'), \
Decimal('0.137814'))
    >>> fxEUR2HKD / fxEUR2TND
    ExchangeRate(Currency('TND'), Decimal(10), Currency('HKD'), \
Decimal('0.137814'))
    >>> fxEUR2TND / fxEUR2HKD
    ExchangeRate(Currency('HKD'), Decimal(1), Currency('TND'), \
Decimal('72.561693'))
    >>> fxHKD2EUR = fxEUR2HKD.inverted()
    >>> fxTND2EUR / fxHKD2EUR
    ExchangeRate(Currency('TND'), Decimal(10), Currency('HKD'), \
Decimal('0.137814'))

Converting money amounts using exchange rates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiplying an amount in some currency with an exchange rate with the same
currency as unit currency results in the equivalent amount in term currency:

    >>> mEUR = 5.27 * EUR
    >>> mEUR * fxEUR2HKD
    Money(Decimal('44.25'), Currency('HKD'))
    >>> mEUR * fxEUR2TND
    Money(Decimal('3210.556'), Currency('TND'))

Likewise, dividing an amount in some currency with an exchange rate with the
same currency as term currency results in the equivalent amount in unit
currency:

    >>> fxHKD2EUR = fxEUR2HKD.inverted()
    >>> mEUR / fxHKD2EUR
    Money(Decimal('44.25'), Currency('HKD'))

Using money converters
^^^^^^^^^^^^^^^^^^^^^^

Money converters can be used to hold different exchange rates, each of them
linked to a period of validity. The type of period must be the same for all
exchange rates held by a money converter.

A money converter is created by calling :class:`MoneyConverter`, giving the
base currency used by this converter:

    >>> conv = MoneyConverter(EUR)

The method :meth:`MoneyConverter.update` is then used to feed exchange rates
into the converter.

For example, a money converter with monthly rates can be created like this:

    >>> import datetime
    >>> today = datetime.date.today()
    >>> year, month, day = today.timetuple()[:3]
    >>> prev_month = month - 1
    >>> rates = [(USD, Decimal('1.1073'), 1),
    ...          (HKD, Decimal('8.7812'), 1)]
    >>> conv.update((year, prev_month), rates)
    >>> rates = [(USD, Decimal('1.0943'), 1),
    ...          (HKD, Decimal('8.4813'), 1)]
    >>> conv.update((year, month), rates)

Exchange rates can be retrieved by calling :meth:`MoneyConverter.get_rate`. If
no reference date is given, the current date is used (unless a callable
returning a different date is given when the converter is created, see below).
The method returns not only rates directly given to the converter, but also
inverted rates and rates calculated by triangulation:

    >>> conv.get_rate(EUR, USD)
    ExchangeRate(Currency('EUR'), Decimal(1), Currency('USD'), \
Decimal('1.0943', 6))
    >>> conv.get_rate(HKD, EUR, date(year, prev_month, 3))
    ExchangeRate(Currency('HKD'), Decimal(1), Currency('EUR'), \
Decimal('0.11388', 6))
    >>> conv.get_rate(USD, EUR)
    ExchangeRate(Currency('USD'), Decimal(1), Currency('EUR'), \
Decimal('0.913826'))
    >>> conv.get_rate(HKD, USD)
    ExchangeRate(Currency('HKD'), Decimal(1), Currency('USD'), \
Decimal('0.129025'))

A money converter can be registered with the class :class:`Money` in order
to support implicit conversion of money amounts from one currency into
another (using the default reference date, see below):

    >>> Money.register_converter(conv)
    >>> twoEUR = 2 * EUR
    >>> twoEUR.convert(USD)
    Money(Decimal('2.19'), Currency('USD'))

A money converter can also be registered and unregistered by using it as
context manager in a `with` statement.

In order to use a default reference date other than the current date, a
callable can be given to :class:`MoneyConverter`. It must be callable without
arguments and return a date. It is then used by
:meth:`~MoneyConverter.get_rate` to get the default reference date:

    >>> yesterday = lambda: datetime.date.today() - datetime.timedelta(1)
    >>> conv = MoneyConverter(EUR)      # uses today as default
    >>> conv.update(yesterday(), [(USD, Decimal('1.0943'), 1)])
    >>> conv.update(datetime.date.today(), [(USD, Decimal('1.0917'), 1)])
    >>> conv.get_rate(EUR, USD)
    ExchangeRate(Currency('EUR'), Decimal(1), Currency('USD'), \
Decimal('1.0917', 6))
    >>> conv = MoneyConverter(EUR, get_dflt_effective_date=yesterday)
    >>> conv.update(yesterday(), [(USD, Decimal('1.0943'), 1)])
    >>> conv.update(datetime.date.today(), [(USD, Decimal('1.0917'), 1)])
    >>> conv.get_rate(EUR, USD)
    ExchangeRate(Currency('EUR'), Decimal(1), Currency('USD'), \
Decimal('1.0943', 6))

As other quantity converters, a :class:`MoneyConverter` instance can be called
to convert a money amount into the equivalent amount in another currency. But
note that the amount is not adjusted to the smallest fraction of that
currency:

    >>> conv(twoEUR, USD)
    Decimal('2.1886', 8)
    >>> conv(twoEUR, USD, datetime.date.today())
    Decimal('2.1834', 8)

Combining Money with other quantities
-------------------------------------

As :class:`Money` derives from :class:`~quantity.Quantity`, it can be combined
with other quantities in order to define a new quantity. This is, for example,
useful for defining prices per quantum:

    >>> from quantity import Quantity
    >>> class Mass(Quantity,
    ...            ref_unit_name='Kilogram',
    ...            ref_unit_symbol='kg'):
    ...     pass
    >>> KILOGRAM = Mass.ref_unit
    >>> class PricePerMass(Quantity, define_as=Money / Mass):
    ...     pass

Because :class:`Money` has no reference unit, there is no reference unit
created for the derived quantity …:

    >>> PricePerMass.units()
    ()

… instead, units must be explicitly defined:

    >>> EURpKG = PricePerMass.derive_unit_from(EUR, KILOGRAM)
    >>> PricePerMass.units()
    (Unit('EUR/kg'),)

Instances of the derived quantity can be created and used just like those of
other quantities:

    >>> from decimalfp import Decimal
    >>> p = Decimal("17.45") * EURpKG
    >>> p * Decimal("1.05")
    PricePerMass(Decimal('18.3225'), Unit('EUR/kg'))
    >>> GRAM = Mass.new_unit('g', 'Gram', Decimal("0.001") * KILOGRAM)
    >>> m = 530 * GRAM
    >>> m * p
    Money(Decimal('9.25'), Currency('EUR'))

Note that instances of the derived class are not automatically quantized to
the quantum defined for the currency:

    >>> EURpKG.quantum is None
    True

Instances of such a "money per quantum" class can also be converted using
exchange rates, as long as the resulting unit is defined:

    >>> p * fxEUR2HKD
    Traceback (most recent call last):
    QuantityError: Resulting unit not defined: HKD/kg.
    >>> HKDpKG = PricePerMass.derive_unit_from(HKD, KILOGRAM)
    >>> p * fxEUR2HKD
    PricePerMass(Decimal('146.5067798', 8), Unit('HKD/kg'))
"""

from __future__ import annotations

from datetime import date
from fractions import Fraction
import math
from numbers import Integral, Rational, Real
from typing import (
    Any, Callable, Dict, Iterable, Optional, SupportsInt, Tuple, Type, Union,
    overload, )

from decimalfp import Decimal, ONE

from .currencies import get_currency_info
from .. import (
    ConverterT, Quantity, QuantityError, QuantityMeta, Unit,
    UnitConversionError, UnitDefT, _amnt_and_unit_from_term, )

# Public interface
__all__ = [
    'Currency',
    'ExchangeRate',
    'get_currency_info',
    'Money',
    'MoneyConverter',
    ]

# Parameterized types

#: Type of money converters
MoneyConverterT = Callable[['Money', 'Currency', Optional[date]], Rational]
#: Types convertable to int
ConvertableToIntT = Union[str, SupportsInt]
#: Mapping a type of validity period to a function that converts a date to that
#: type of period
TypeToConvDateToValidityMapT = \
    Dict[type, Callable[[date], Union[int, Tuple[int, int], date, None]]]
#: Types used to specify time periods for the validity of exchange rates
ValidityT = Union[date, int, str, ConvertableToIntT, Tuple[int, int],
                  Tuple[ConvertableToIntT, ConvertableToIntT], None]
#: Type of tuple to specify an exchange rate
RateSpecT = Tuple[Union['Currency', str], Union[Rational, float, str],
                  Rational]
#: Dict type mappping a validity period and a currency to an exchange rate
RateDictT = Dict[Tuple[ValidityT, Union['Currency', str]], 'ExchangeRate']


class Currency(Unit):
    # noinspection PyUnresolvedReferences
    """Represents a currency, i.e. a money unit.

    .. note::
        New instances of `Currency` can not be created directly by calling
        `Currency`. Instead, use `Money.register_currency` or `Money.new_unit`.

    """

    __slots__ = ['_smallest_fraction']

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _smallest_fraction: Decimal

    @property
    def iso_code(self) -> str:
        """ISO 4217 3-character code."""
        return self._symbol

    @property
    def smallest_fraction(self) -> Decimal:
        """The smallest fraction available for this currency."""
        return self._smallest_fraction

    @property
    def quantum(self) -> Decimal:
        """Return the minimum amount for this currency."""
        return self._smallest_fraction

    def __repr__(self) -> str:
        """repr(self)"""
        return "%s(%s)" % (self.__class__.__name__, repr(self._symbol))


class MoneyMeta(QuantityMeta):
    """Meta class for Money"""

    def new_unit(cls, symbol: str, name: Optional[str] = None,
                 minor_unit: Optional[int] = None,
                 smallest_fraction: Union[Real, str, None] = None) \
            -> Currency:
        """Create, register and return a new `Currency` instance.

        Args:
            symbol: symbol of the currency (should be a ISO 4217 3-character
                code, if possible)
            name: name of the currency
            minor_unit: amount of minor unit (as exponent to 10), optional,
                defaults to precision of smallest fraction, if that is given,
                otherwise to 2
            smallest_fraction: smallest fraction available for the currency,
                optional, defaults to Decimal(10) ** -minor_unit. Can also be
                given as a string, as long as it is convertable to a Decimal.

        Raises:
            TypeError: given `symbol` is not a string
            ValueError: no `symbol` was given
            TypeError: given `minor_unit` is not an Integral number
            ValueError: given `minor_unit` < 0
            ValueError: given `smallest_fraction` can not be converted to a
                Decimal
            ValueError: given `smallest_fraction` not > 0
            ValueError: 1 is not an integer multiple of given
                `smallest_fraction`
            ValueError: given `smallest_fraction` does not fit given
                `minor_unit`
        """
        if minor_unit is not None:
            if not isinstance(minor_unit, Integral):
                raise TypeError("'minor_unit' must be an Integral number.")
            if minor_unit < 0:
                raise ValueError("'minor_unit' must be >= 0.")
        if smallest_fraction is None:
            if minor_unit is None:
                smallest_fraction = Decimal('0.01')
            else:
                smallest_fraction = Decimal(10) ** -minor_unit
        else:
            smallest_fraction = Decimal(smallest_fraction)
            if minor_unit is None:
                if smallest_fraction <= 0:
                    raise ValueError("'smallest_fraction' must be > 0.")
                multiple = 1 / smallest_fraction
                if not (multiple.denominator == 1 and multiple.numerator > 1):
                    raise ValueError("1 must be an integer multiple of given "
                                     "'smallest_fraction'.")
            else:
                if minor_unit != smallest_fraction.precision:
                    raise ValueError(
                        "'smallest_fraction' does not fit 'minor_unit'.")
        assert isinstance(smallest_fraction, Decimal)
        curr = super().new_unit(symbol, name)
        assert isinstance(curr, Currency)
        curr._smallest_fraction = smallest_fraction
        return curr

    def register_currency(cls, iso_code: str) -> Currency:
        """Register the currency with code `iso_code` from ISO 4217 database.

        Args:
            iso_code: ISO 4217 3-character code for the currency to be
                registered

        Returns:
            registered currency

        Raises:
            ValueError: currency with code `iso_code` not in database
        """
        try:
            reg_curr = cls.get_unit_by_symbol(iso_code)
        except ValueError:
            iso_code, iso_num_code, name, minor_unit, countries = \
                get_currency_info(iso_code)
            curr = cls.new_unit(iso_code, name, minor_unit)
            return curr
        else:  # currency already registered
            assert isinstance(reg_curr, Currency)
            return reg_curr

    def register_converter(cls, conv: ConverterT) -> None:  # noqa: N805
        """Add converter 'conv' to the list of converters registered in 'cls'.

        Money converters should not be registered directly by using this
        method. Instead, this should be done by using them as context managers
        in a 'with' statement."""
        if isinstance(conv, MoneyConverter):
            cls._converters.append(conv)
        else:
            raise TypeError("Given `conv` is not a MoneyConverter.")

    def remove_converter(cls, conv: ConverterT) -> None:  # noqa: N805
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


class Money(Quantity, metaclass=MoneyMeta):
    # noinspection PyUnresolvedReferences
    """Represents a money amount, i.e. the combination of a numerical value
    and a money unit, aka. currency.

    Instances of `Money` can be created in two ways, by providing a numerical
    amount and a `Currency` or by providing a string representation of a money
    amount.

    **1. Form**

    Args:
        amount: money amount (gets rounded to a Decimal according
            to smallest fraction of currency)
        currency: money unit

    `amount` must convertable to a `decimalfp.Decimal`, it can also be given
    as a string.

    Raises:
        TypeError: `amount` can not be converted to a Decimal number
        ValueError: no currency given

    **2. Form**

    Args:
        mStr: unicode string representation of a money amount (incl.
            currency symbol)
        currency: the money's unit (optional)

    `mStr` must contain a numerical value and a currency symbol, separated
    atleast by one blank. Any surrounding white space is ignored. If
    `currency` is given in addition, the resulting money's currency is set to
    this currency and its amount is converted accordingly, if possible.

    Returns:
        `Money` instance

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

    _unit_cls: Type[Unit] = Currency

    # TODO: remove these class variables after mypy issue #1021 got fixed:
    _amount: Decimal
    _unit: Currency

    @property
    def currency(self) -> Currency:
        """The money's currency, i.e. its unit."""
        return self._unit


class ExchangeRate:
    """Basic representation of a conversion factor between two currencies.

    Args:
        unit_currency: currency to be converted from,
            aka base currency
        unit_multiple: amount of base currency (must be equal to
            an integer)
        term_currency: currency to be converted to, aka
            price currency
        term_amount: equivalent amount of term
            currency

    `unit_currency` and `term_currency` can also be given as 3-character ISO
    4217 codes of already registered currencies.

    `unit_multiple` must be > 1. It can also be given as a string, as long as
    it is convertable to an Integral.

    `term_amount` can also be given as a string, as long as it is convertable
    to a number.

    Example:

    1 USD = 0.9683 EUR   =>   ExchangeRate('USD', 1, 'EUR', '0.9683')

    `unit_multiple` and `term_amount` will always be adjusted so that
    the resulting unit multiple is a power to 10 and the resulting term
    amounts magnitude is >= -1. The latter will always be rounded to 6
    decimal digits.

    Raises:
        ValueError: non-registered / unknown symbol given for a currency
        TypeError: value of type other than `Currency` or string given for a
            currency
        ValueError: currencies given are identical
        ValueError: unit multiple is not equal to an integer or is not >= 1
        ValueError: term amount is not >= 0.000001
        ValueError: unit multiple or term amount can not be converted to a
            Decimal
    """

    def __init__(self, unit_currency: Union[Currency, str],
                 unit_multiple: Rational, term_currency: Union[Currency, str],
                 term_amount: Union[Rational, float, str]) -> None:
        if not isinstance(unit_currency, Currency):
            if isinstance(unit_currency, str):
                unit = Money.get_unit_by_symbol(unit_currency)
                assert isinstance(unit, Currency)
                unit_currency = unit
            else:
                raise TypeError("Can't use a '%s' as unit currency."
                                % type(unit_currency))
        if not isinstance(term_currency, Currency):
            if isinstance(term_currency, str):
                unit = Money.get_unit_by_symbol(term_currency)
                assert isinstance(unit, Currency)
                term_currency = unit
            else:
                raise TypeError("Can't use a '%s' as term currency."
                                % type(term_currency))
        if unit_currency is term_currency:
            raise ValueError("The currencies given must not be identical.")
        self._unit_currency = unit_currency
        self._term_currency = term_currency
        unit_multiple = Decimal(unit_multiple).adjusted()
        if unit_multiple.precision > 0:
            raise ValueError("Unit multiple must be an Integral.")
        if unit_multiple < 1:
            raise ValueError("Unit multiple must be >= 1.")
        if isinstance(term_amount, Decimal):
            magnitude_term_amount = term_amount.magnitude
        else:
            try:
                term_amount = Fraction(term_amount)
            except (ValueError, OverflowError):
                raise ValueError("Term amount must be convertable to a "
                                 "Rational.") from None
            except TypeError:
                raise TypeError(f"Rational number expected as term amount; "
                                f"{type(term_amount)} given.")
            if term_amount <= 0:
                raise ValueError("Term amount must be >= 0.000001.")
            magnitude_term_amount = int(math.floor(math.log10(term_amount)))
        if term_amount < Decimal("0.000001"):
            raise ValueError("Term amount must be >= 0.000001.")
        # adjust unit_multiple and term_amount so that
        # unit_multiple is a power to 10 and term_amount.magnitude >= -1
        mult = Decimal(10) ** (unit_multiple.magnitude
                               - min(0, magnitude_term_amount + 1))
        assert isinstance(mult, Decimal)
        self._unit_multiple = mult
        self._term_amount = Decimal(term_amount * mult / unit_multiple, 6)

    @property
    def unit_currency(self) -> Currency:
        """Currency to be converted from, aka base currency."""
        return self._unit_currency

    @property
    def term_currency(self) -> Currency:
        """Currency to be converted to, aka price currency."""
        return self._term_currency

    @property
    def rate(self) -> Rational:
        """Relative value of term_currency to unit_currency."""
        return self._term_amount / self._unit_multiple

    @property
    def inverse_rate(self) -> Rational:
        """Inverted rate, i.e. relative value of unit currency to term
        currency."""
        return self._unit_multiple / self._term_amount

    @property
    def quotation(self) -> Tuple[Currency, Currency, Rational]:
        """Tuple of unit currency, term currency and rate."""
        return self._unit_currency, self._term_currency, self.rate

    @property
    def inverse_quotation(self) -> Tuple[Currency, Currency, Rational]:
        """Tuple of term currency, unit currency and inverse rate."""
        return self._term_currency, self._unit_currency, self.inverse_rate

    def inverted(self) -> ExchangeRate:
        """Return inverted exchange rate."""
        return ExchangeRate(self._term_currency, ONE, self._unit_currency,
                            self.inverse_rate)

    def __hash__(self) -> int:
        """hash(self)"""
        return hash(self.quotation)

    def __eq__(self, other: Any) -> bool:
        """self == other

        Args:
            other: object to compare with

        Returns:
            True if other is an instance of ExchangeRate and
            self.quotation == other.quotation, False otherwise
        """
        if isinstance(other, ExchangeRate):
            return self.quotation == other.quotation
        return False

    @overload
    def __mul__(self, other: Money) -> Money:
        ...

    @overload
    def __mul__(self, other: ExchangeRate) -> ExchangeRate:
        ...

    @overload
    def __mul__(self, other: Quantity) -> Quantity:
        ...

    # noinspection DuplicatedCode
    def __mul__(self, other: Union[Money, ExchangeRate, Quantity]) \
            -> Union[Money, ExchangeRate, Quantity]:
        """self * other

        **1. Form**

        Args:
            other: money amount to multiply with

        Returns:
            `Money` equivalent of `other` in term currency

        Raises:
            ValueError: currency of `other` is not equal to unit currency

        **2. Form**

        Args:
            other: exchange rate to multiply with

        Returns:
            "triangulated" exchange rate

        Raises:
            ValueError: unit currency of one multiplicant does not equal the
                term currency of the other multiplicant

        **3. Form**

        Args:
            other: quantity to multiply with

        The type of `other` must be a sub-class of :class:`Quantity` derived
        from :class:`Money` divided by some other sub-class of
        :class:`Quantity`.

        Returns:
            equivalent of `other` in term currency

        Raises:
            ValueError: resulting unit is not defined
        """
        if isinstance(other, Money):
            if other.unit is self.unit_currency:
                return other.__class__(other.amount * self.rate,
                                       self.term_currency)
            raise ValueError("Can't multiply '%s' and '%s/%s'."
                             % (other.unit, self.term_currency,
                                self.unit_currency))
        if isinstance(other, ExchangeRate):
            if self.unit_currency is other.term_currency:
                return ExchangeRate(other.unit_currency, ONE,
                                    self.term_currency,
                                    self.rate * other.rate)
            elif self.term_currency is other.unit_currency:
                return ExchangeRate(self.unit_currency, ONE,
                                    other.term_currency,
                                    self.rate * other.rate)
            else:
                raise ValueError("Can't multiply '%s/%s' and '%s/%s'."
                                 % (self.term_currency, self.unit_currency,
                                    other.term_currency, other.unit_currency))
        if isinstance(other, Quantity):
            unit_term = other.unit.definition * \
                        UnitDefT(((self.term_currency, 1),
                                  (self.unit_currency, -1)))
            try:
                amnt, unit = _amnt_and_unit_from_term(unit_term)
            except KeyError:
                raise QuantityError(f"Resulting unit not defined: "
                                    f"{unit_term}.") from None
            amnt *= self.rate * other.amount
            return other.__class__(amnt, unit)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other: ExchangeRate) -> ExchangeRate:
        """self / other

        Args:
            other: exchange rate to divide with

        Returns:
            "triangulated" exchange rate

        Raises:
            ValueError: unit currencies of operands not equal and term
                currencies of operands not equal
        """
        if isinstance(other, ExchangeRate):
            if self.unit_currency is other.unit_currency:
                return ExchangeRate(other.term_currency, ONE,
                                    self.term_currency,
                                    self.rate / other.rate)
            elif self.term_currency is other.term_currency:
                return ExchangeRate(self.unit_currency, ONE,
                                    other.unit_currency,
                                    self.rate / other.rate)
            else:
                raise ValueError("Can't divide '%s/%s' by '%s/%s'."
                                 % (self.term_currency, self.unit_currency,
                                    other.term_currency, other.unit_currency))
        return NotImplemented

    @overload
    def __rtruediv__(self, other: Money) -> Money:
        ...

    @overload
    def __rtruediv__(self, other: Quantity) -> Quantity:
        ...

    # noinspection DuplicatedCode
    def __rtruediv__(self, other: Union[Money, Quantity]) \
            -> Union[Money, Quantity]:
        """other / self

        **1. Form**

        Args:
            other: money amount to divide

        Returns:
            equivalent of `other` in unit currency

        Raises:
            ValueError: currency of `other` is not equal to term currency

        **2. Form**

        Args:
            other: quantity to divide

        The type of `other` must be a sub-class of :class:`Quantity` derived
        from :class:`Money` divided by some other sub-class of
        :class:`Quantity`.

        Returns:
            equivalent of `other` in unit currency

        Raises:
            :class:`~quantity.QuantityError`: resulting unit is not defined
        """
        if isinstance(other, Money):
            if other.unit is self.term_currency:
                return other.__class__(other.amount * self.inverse_rate,
                                       self.unit_currency)
            raise ValueError("Can't divide '%s' by '%s/%s'"
                             % (other.unit, self.term_currency,
                                self.unit_currency))
        if isinstance(other, Quantity):
            unit_term = other.unit.definition * \
                        UnitDefT(((self.unit_currency, 1),
                                  (self.term_currency, -1)))
            try:
                amnt, unit = _amnt_and_unit_from_term(unit_term)
            except KeyError:
                raise QuantityError(f"Resulting unit not defined: "
                                    f"{unit_term}.") from None
            amnt *= self.inverse_rate * other.amount
            return other.__class__(amnt, unit)
        return NotImplemented

    def __repr__(self) -> str:
        """repr(self)"""
        return f"{self.__class__.__name__}({self.unit_currency!r}, " \
               f"{self._unit_multiple!r}, {self.term_currency!r}, " \
               f"{self._term_amount!r})"

    def __str__(self) -> str:
        """str(self)"""
        return f"{self.rate} {self.term_currency}/{self.unit_currency}"


class MoneyConverter:
    """Converter for money amounts.

    Money converters can be used to hold different exchange rates.
    They can be registered with the class :class:`Money` in order to
    support implicit conversion of money amounts from one currency into
    another.

    Args:
        base_currency: currency used as reference currency
        get_dflt_effective_date: a callable without parameters that must return
            a date which is then used as default effective date in
            :meth:`MoneyConverter.get_rate` (default: `datetime.date.today`)
    """

    _date2validity: TypeToConvDateToValidityMapT = {
        type(None): lambda d: None,
        int: lambda d: d.year,
        tuple: lambda d: (d.year, d.month),
        date: lambda d: d,
        }

    def __init__(self, base_currency: Currency,
                 get_dflt_effective_date: Optional[Callable[[], date]] =
                 None) -> None:
        self._base_currency = base_currency
        self._rate_dict: RateDictT = {}
        self._type_of_validity: Optional[Type[ValidityT]] = None
        if get_dflt_effective_date is None:
            self._get_dflt_effective_date = date.today
        else:
            self._get_dflt_effective_date = get_dflt_effective_date

    def __call__(self, money_amnt: Money, to_currency: Currency,
                 effective_date: Optional[date] = None) -> Rational:
        """Convert a money amount in one currency to the equivalent amount for
        another currency.

        Args:
            money_amnt: money amount to be converted
            to_currency: currency for which the  equivalent amount is to be
                returned
            effective_date: date for which the exchange rate to be used must be
                effective (default: None)

        If `effective_date` is not given, the return value of the callable
        given as `get_dflt_effective_date` to :class:`MoneyConverter` is
        used as reference (default: today).

        Returns:
            amount equiv so that equiv * to_currency == money_amnt

        Raises:
            UnitConversionError: exchange rate not available
        """
        rate = self.get_rate(money_amnt.currency, to_currency, effective_date)
        if rate is None:
            raise UnitConversionError("Can't convert '%s' to '%s'.",
                                      money_amnt.currency, to_currency)
        else:
            # TODO: remove 'type: ignore' when number.pyi got fixed
            return rate.rate * money_amnt.amount  # type: ignore

    @property
    def base_currency(self) -> Currency:
        """The currency used as reference currency."""
        return self._base_currency

    def update(self, validity: ValidityT, rate_specs: Iterable[RateSpecT]) \
            -> None:
        """Update the exchange rate dictionary used by the converter.

        Args:
            validity: specifies the validity period of the given
                exchange rates
            rate_specs: list of entries to update the converter

        `validity` can be given in different ways:

        If `None` is given, the validity of the given rates is not restricted,
        i. e. they are used for all times ("constant rates").

        If an `int` (or a string convertable to an `int`) is given, it is
        interpreted as a year and the given rates are treated as valid for
        that year ("yearly rates").

        If a tuple of two `int`s (or two strings convertable to an `int`) or
        a string in the form 'YYYY-MM' is given, it is interpreted as a
        combination of a year and a month, and the given rates are treated as
        valid for that month ("monthly rates").

        If a `date` or a string holding a date in ISO format ('YYYY-MM-DD') is
        given, the rates are treated as valid just for that date ("daily
        rates").

        The type of validity must be the same in recurring updates.

        Each entry in `rate_specs` must be comprised of the following elements:

        - `term_currency` (Union[Currency, str]): currency of equivalent
            amount, aka price currency
        - `term_amount` (Union[Rational, float, str]): equivalent amount of
            term currency
        - `unit_multiple` (Rational): amount of base currency

        `validity` and `term_currency` are used together as the key for the
        internal exchange rate dictionary.

        Raises:
            ValueError: invalid date given for `validity`
            ValueError: invalid year / month given for `validity`
            ValueError: invalid year given for `validity`
            ValueError: unknown value given for `validity`
            ValueError: different types of validity period given in subsequent
                calls
        """
        # check and transform validity
        if isinstance(validity, str):
            parts = validity.split('-')
            n_parts = len(parts)
            if n_parts == 3:
                dt_str = validity
                try:  # verify date
                    validity = date.fromisoformat(dt_str)
                except ValueError:
                    raise ValueError(f"Not a valid date: "
                                     f"{validity}.") from None
            elif n_parts == 2:
                dt_str = f"{validity}-01"
                try:  # verify year and month
                    dt = date.fromisoformat(dt_str)
                except ValueError:
                    raise ValueError(f"Not a valid year / month: "
                                     f"{validity}.") from None
                else:
                    validity = (dt.year, dt.month)
            elif n_parts == 1:
                dt_str = f"{validity}-01-01"
                try:  # verify year
                    dt = date.fromisoformat(dt_str)
                except ValueError:
                    raise ValueError(f"Not a valid year: "
                                     f"{validity}.") from None
                else:
                    validity = dt.year
            else:
                raise ValueError(f"Not a valid period: {validity}.")
        elif isinstance(validity, tuple):
            dt_str = f"{validity[0]:04d}-{validity[1]:02d}-01"
            try:  # verify year and month
                dt = date.fromisoformat(dt_str)
            except ValueError:
                raise ValueError(f"Not a valid year / month: "
                                 f"{validity}.") from None
            else:
                validity = (dt.year, dt.month)
        elif isinstance(validity, int):
            try:
                date(validity, 1, 1)  # verify year
            except ValueError:
                raise ValueError(f"Not a valid year: "
                                 f"{validity}.") from None
        elif not (validity is None or isinstance(validity, date)):
            raise ValueError(f"Not a valid period: {validity}.")
        # check type of validity
        type_of_validity = self._type_of_validity
        if type_of_validity is None:
            self._type_of_validity = type(validity)
        elif type_of_validity is not type(validity):
            raise ValueError('Different types of validity periods given.')
        # update internal dict
        base_currency = self._base_currency
        it = (((validity, term_currency),
               ExchangeRate(base_currency, unit_multiple, term_currency,
                            term_amount))
              for term_currency, term_amount, unit_multiple in rate_specs)
        self._rate_dict.update(it)

    def get_rate(self, unit_currency: Currency, term_currency: Currency,
                 effective_date: Optional[date] = None) \
            -> Optional[ExchangeRate]:
        """Return exchange rate from `unit_currency` to `term_currency` that is
        effective for `effective_date`.

        Args:
            unit_currency: currency to be converted from
            term_currency: currency to be converted to
            effective_date: date at which the rate must be effective
                (default: None)

        If `effective_date` is not given, the return value of the callable
        given as `get_dflt_effective_date` to :class:`MoneyConverter` is
        used as reference (default: today).

        Returns:
            exchange rate from `unit_currency` to `term_currency` that is
                effective for `effective_date`, `None` if there is no such rate
        """
        if unit_currency is term_currency:
            return ExchangeRate(unit_currency, ONE, term_currency, ONE)
        base_currency = self.base_currency
        if base_currency == unit_currency:
            try:
                return self._get_rate(term_currency, effective_date)
            except KeyError:
                return None
        elif base_currency == term_currency:
            try:
                rate = self._get_rate(unit_currency, effective_date)
            except KeyError:
                return None
            else:
                return rate.inverted()
        else:
            try:
                unit_rate = self._get_rate(unit_currency, effective_date)
                term_rate = self._get_rate(term_currency, effective_date)
            except KeyError:
                return None
            else:
                return ExchangeRate(unit_currency, ONE, term_currency,
                                    term_rate.rate / unit_rate.rate)

    def _get_rate(self, term_currency: Currency,
                  effective_date: Optional[date]) -> ExchangeRate:
        type_of_validity = self._type_of_validity
        if type_of_validity is None:
            raise KeyError
        if effective_date is None:
            effective_date = self._get_dflt_effective_date()
        validity = self._date2validity[type_of_validity](effective_date)
        return self._rate_dict[(validity, term_currency)]

    def __enter__(self) -> MoneyConverter:
        """Register self as converter in :class:`Money`."""
        Money.register_converter(self)
        return self

    def __exit__(self, *args: Tuple[Any, ...]) -> None:
        """Unregister self as converter in :class:`Money`."""
        Money.remove_converter(self)
        return None
