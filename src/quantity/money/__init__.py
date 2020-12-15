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
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


u"""Currency-safe computations with money amounts.

Usage
=====

Registering a currency
----------------------

A currency must explicitly be registered as a unit for further use. The
easiest way to do this is to call the function :func:`registerCurrency`:

    >>> EUR = registerCurrency('EUR')
    ... HKD = registerCurrency('HKD')
    ... TND = registerCurrency('TND')
    ... USD = registerCurrency('USD')
    >>> EUR, HKD, TND, USD
    (Currency(u'EUR'), Currency(u'HKD'), Currency(u'TND'), Currency(u'USD'))

The function is backed by a database of currencies defined in ISO 4217. It
takes the 3-character ISO 4217 code as parameter.

:class:`Currency` derives from :class:`~quantity.Unit`. Each instance has a
symbol (which is the 3-character ISO 4217 code) and a name. In addition, it
holds the smallest fraction defined for amounts in this currency:

    >>> TND.symbol
    u'TND'
    >>> TND.name
    u'Tunisian Dinar'
    >>> TND.smallestFraction
    Decimal('0.001')

Instantiating a money amount
----------------------------

As :class:`Money` derives from :class:`~quantity.Quantity`, an instance can
simply be created by giving an amount and a unit:

    >>> Money(30, EUR)
    Money(Decimal(30, 2), Currency(u'EUR'))

All amounts of money are rounded according to the smallest fraction defined
for the currency:

    >>> Money(3.128, EUR)
    Money(Decimal('3.13'), Currency(u'EUR'))
    >>> Money(41.1783, TND)
    Money(Decimal('41.178'), Currency(u'TND'))

As with other quantities, money amounts can also be derived from a string or
build using the operator `^`:

    >>> Money('3.18 USD')
    Money(Decimal('3.18'), Currency(u'USD'))
    >>> 3.18 ^ USD
    Money(Decimal('3.18'), Currency(u'USD'))

Computing with money amounts
----------------------------

:class:`Money` derives from :class:`~quantity.Quantity`, so all operations on
quantities can also be applied to instances of :class:`Money`. But because
there is no fixed relation between currencies, there is no implicit conversion
between money amounts of different currencies:

    >>> Money(30, EUR) + Money(3.18, EUR)
    Money(Decimal('33.18'), Currency(u'EUR'))
    >>> Money(30, EUR) + Money(3.18, USD)
    IncompatibleUnitsError: Can't convert 'US Dollar' to 'Euro'

Resulting values are always quantized to the smallest fraction defined with
the currency:

    >>> Money('3.20 USD') / 3
    Money(Decimal('1.07'), Currency(u'USD'))
    >>> Money('3.20 TND') / 3
    Money(Decimal('1.067'), Currency(u'TND'))

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
    ExchangeRate(Currency(u'EUR'), Decimal(1), Currency(u'HKD'), \
Decimal('8.395804'))

`unitMultiple` and `termAmount` will always be adjusted so that the resulting
unit multiple is a power to 10 and the resulting term amounts magnitude is >=
-1. The latter will always be rounded to 6 decimal digits:

    >>> fxTND2EUR = ExchangeRate(TND, 5, EUR, Decimal('0.0082073'))
    >>> fxTND2EUR
    ExchangeRate(Currency(u'TND'), Decimal(100), Currency(u'EUR'), \
Decimal('0.164146'))

The resulting rate for an amount of 1 unit currency in term currency can be
obtained via the property :attr:`ExchangeRate.rate`:

    >>> fxTND2EUR.rate
    Decimal('0.00164146')

The property :attr:`ExchangeRate.quotation` gives a tuple of unit currency,
term currency and rate:

    >>> fxTND2EUR.quotation
    (Currency(u'TND'), Currency(u'EUR'), Decimal('0.00164146'))

The properties :attr:`ExchangeRate.inverseRate` and
:attr:`ExchangeRate.inverseQuotation` give the rate and the quotation in the
opposite direction (but do not round the rate!):

    >>> fxTND2EUR.inverseRate
    Fraction(50000000, 82073)
    >>> fxTND2EUR.inverseQuotation
    (Currency(u'EUR'), Currency(u'TND'), Fraction(50000000, 82073))

The inverse ExchangeRate can be created by calling the method
:meth:`ExchangeRate.inverted`:

    >>> fxEUR2TND = fxTND2EUR.inverted()
    >>> fxEUR2TND
    ExchangeRate(Currency(u'EUR'), Decimal(1), Currency(u'TND'), \
Decimal('609.213749'))

An exchange rate can be derived from two other exchange rates, provided that
they have one currency in common ("triangulation"). If the unit currency of
one exchange rate is equal to the term currency of the other, the two exchange
rates can be multiplied with each other. If either the unit currencies or the
term currencies are equal, the two exchange rates can be divided:

    >>> fxEUR2HKD * fxTND2EUR
    ExchangeRate(Currency(u'TND'), Decimal(10), Currency(u'HKD'), \
Decimal('0.137814'))
    >>> fxEUR2HKD / fxEUR2TND
    ExchangeRate(Currency(u'TND'), Decimal(10), Currency(u'HKD'), \
Decimal('0.137814'))
    >>> fxEUR2TND / fxEUR2HKD
    ExchangeRate(Currency(u'HKD'), Decimal(1), Currency(u'TND'), \
Decimal('72.561693'))
    >>> fxHKD2EUR = fxEUR2HKD.inverted()
    >>> fxTND2EUR / fxHKD2EUR
    ExchangeRate(Currency(u'TND'), Decimal(10), Currency(u'HKD'), \
Decimal('0.137814'))

Converting money amounts using exchange rates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiplying an amount in some currency with an exchange rate with the same
currency as unit currency results in the equivalent amount in term currency:

    >>> mEUR = 5.27 ^ EUR
    >>> mEUR * fxEUR2HKD
    Money(Decimal('44.25'), Currency(u'HKD'))
    >>> mEUR * fxEUR2TND
    Money(Decimal('3210.556'), Currency(u'TND'))

Likewise, dividing an amount in some currency with an exchange rate with the
same currency as term currency results in the equivalent amount in unit
currency:

    >>> fxHKD2EUR = fxEUR2HKD.inverted()
    >>> mEUR / fxHKD2EUR
    Money(Decimal('44.25'), Currency(u'HKD'))

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

    >>> rates_2015_11 = [(USD, Decimal('1.1073'), 1),
    ...                  (HKD, Decimal('8.7812'), 1)]
    >>> conv.update((2015, 11), rates_2015_11)
    >>> rates_2015_12 = [(USD, Decimal('1.0943'), 1),
    ...                  (HKD, Decimal('8.4813'), 1)]
    >>> conv.update((2015, 12), rates_2015_12)

Exchange rates can be retrieved by calling :meth:`MoneyConverter.getRate`. If
no reference date is given, the current date is used (unless a callable
returning a different date is given when the converter is created, see below).
The method returns not only rates directly given to the converter, but also
inverted rates and rates calculated by triangulation:

    >>> # assuming today is a date in December 2015
    >>> conv.getRate(EUR, USD)
    ExchangeRate(Currency(u'EUR'), Decimal(1), Currency(u'USD'), \
Decimal('1.0943', 6))
    >>> conv.getRate(HKD, EUR, date(2015, 11, 3))
    ExchangeRate(Currency(u'HKD'), Decimal(1), Currency(u'EUR'), \
Decimal('0.11388', 6))
    >>> conv.getRate(USD, EUR)
    ExchangeRate(Currency(u'USD'), Decimal(1), Currency(u'EUR'), \
Decimal('0.913826'))
    >>> conv.getRate(HKD, USD)
    ExchangeRate(Currency(u'HKD'), Decimal(1), Currency(u'USD'), \
Decimal('0.129025'))

A money converter can be registered with the class :class:`Currency` in order
to support implicit conversion of money amounts from one currency into
another (using the default reference date, see below):

    >>> Currency.registerConverter(conv)
    >>> USD(2 ^ EUR)
    Decimal('2.1886', 8)
    >>> twoEUR = 2 ^ EUR
    >>> twoEUR.convert(USD)
    Money(Decimal('2.19'), Currency(u'USD'))

A money converter can also be registered and unregistered by using it as
context manager in a `with` statement.

In order to use a default reference date other than the current date, a
callable can be given to :class:`MoneyConverter`. It must be callable without
arguments and return a date. It is then used by
:meth:`~MoneyConverter.getRate` to get the default reference date:

    >>> yesterday = lambda: datetime.date.today() - datetime.timedelta(1)
    >>> conv = MoneyConverter(EUR)      # uses today as default
    >>> conv.update(yesterday(), [(USD, Decimal('1.0943'), 1)])
    >>> conv.update(datetime.date.today(), [(USD, Decimal('1.0917'), 1)])
    >>> conv.getRate(EUR, USD)
    ExchangeRate(Currency(u'EUR'), Decimal(1), Currency(u'USD'), \
Decimal('1.0917', 6))
    >>> conv = MoneyConverter(EUR, getDfltEffectiveDate=yesterday)
    >>> conv.update(yesterday(), [(USD, Decimal('1.0943'), 1)])
    >>> conv.update(datetime.date.today(), [(USD, Decimal('1.0917'), 1)])
    >>> conv.getRate(EUR, USD)
    ExchangeRate(Currency(u'EUR'), Decimal(1), Currency(u'USD'), \
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

    >>> class PricePerMass(Quantity):
    ...     defineAs = Money / Mass

Because :class:`Money` has no reference unit, there is no reference unit
created for the derived quantity …:

    >>> list(PricePerMass.Unit.registeredUnits())
    []

… instead, units must be explicitly defined:

    >>> EURpKG = PricePerMass.Unit(defineAs=EUR/KILOGRAM)
    >>> list(PricePerMass.Unit.registeredUnits())
    [PricePerMass.Unit(u'EUR/kg')]

As with other derived quantities, the function :func:`~quantity.generateUnits`
can be used to create all units from the cross-product of units of the base
quantities.

Instances of the derived quantity can be created and used just like those of
other quantities:

    >>> p = 17.45 ^ EURpKG
    >>> p * Decimal('1.05')
    PricePerMass(Decimal('18.354', 4), PricePerMass.Unit(u'EUR/kg'))
    >>> m = 530 ^ GRAM
    >>> m * p
    Money(Decimal('9.26'), Currency(u'EUR'))

Note that instances of the derived class are not automatically quantized to
the quantum defined for the currency:

    >>> PricePerMass.getQuantum(EURpKG) is None
    True

Instances of such a "money per quantum" class can also be converted using
exchange rates, as long as the resulting unit is defined:

    >>> p * fxEUR2HKD
    QuantityError: Resulting unit not defined: HKD/kg.
    >>> HKDpKG = PricePerMass.Unit(defineAs=HKD/KILOGRAM)
    >>> p * fxEUR2HKD
    PricePerMass(Decimal('146.75865392'), PricePerMass.Unit(u'HKD/kg'))
"""


from .converter import MoneyConverter
from .currencies import getCurrencyInfo, registerCurrency
from .moneybase import Currency, Money, ExchangeRate


__all__ = [
    'Currency',
    'Money',
    'ExchangeRate',
    'getCurrencyInfo',
    'registerCurrency',
    'MoneyConverter',
]
