# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        converter
## Purpose:     Provides classes used to convert money amounts
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) 2015 Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Provides classes used to convert money amounts."""


from __future__ import absolute_import, unicode_literals
from datetime import date
from .. import UnitConversionError
from . import Currency, ExchangeRate


__metaclass__ = type


# string handling Python 2.x / Python 3.x
bytes = type(b'')
str = type(u'')


class MoneyConverter:

    """Converter for money amounts.

    Money converters can be used to hold different exchange rates.
    They can be registered with the class :class:`Currency` in order to
    support implicit conversion of money amounts from one currency into
    another.

    Args:
        baseCurrency (:class:`Currency`): currency used as reference currency
        getDfltEffectiveDate (callable): a callable without parameters that
            must return a date which is then used as default effective date in
            :meth:`MoneyConverter.getRate` (default: `datetime.date.today`)
    """

    _date2validity = {
        type(None): lambda d: None,
        int: lambda d: d.year,
        tuple: lambda d: (d.year, d.month),
        date: lambda d: d,
    }

    def __init__(self, baseCurrency, getDfltEffectiveDate=None):
        self._baseCurrency = baseCurrency
        self._rateDict = {}
        self._typeOfValidity = None
        if getDfltEffectiveDate is None:
            self._getDfltEffectiveDate = date.today
        else:
            self._getDfltEffectiveDate = getDfltEffectiveDate

    def __call__(self, moneyAmnt, toCurrency, effectiveDate=None):
        """Convert a money amount in one currency to the equivalent amount for
        another currency.

        Args:
            moneyAmnt (:class:`Money`): money amount to be converted
            toCurrency (:class:`Currency`): currency for which the  equivalent
                amount is to be returned
            effectiveDate (date): date for which the exchange rate used must
                be effective (default: None)

        If `effectiveDate` is not given, the return value of the callable
        given as `getDfltEffectiveDate` to :class:`MoneyConverter` is used as
        reference (default: today).

        Returns:
            number: amount equiv so that equiv ^ toCurrency == moneyAmnt

        Raises:
            UnitConversionError: exchange rate not available
        """
        rate = self.getRate(moneyAmnt.currency, toCurrency, effectiveDate)
        if rate is None:
            raise UnitConversionError("Can't convert '%s' to '%s'.",
                                      moneyAmnt.currency, toCurrency)
        return rate.rate * moneyAmnt.amount

    @property
    def baseCurrency(self):
        """The currency used as reference currency."""
        return self._baseCurrency

    def update(self, validity, rateSpecs):
        """Update the exchange rate dictionary used by the converter.

        Args:
            validity (see below): specifies the validity period of the given
                exchange rates
            rateSpecs (iterable): list of entries to update the converter

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

        Each entry in `rateSpecs` must be comprised of the following elements:

        - `termCurrency` (:class:`~Currency`): currency of equivalent amount,
          aka price currency
        - `termAmount` (number): equivalent amount of term currency
        - `unitMultiple` (Integral): amount of base currency

        `validity` and `termCurrency` are used together as the key for the
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
        if isinstance(validity, (str, bytes)):
            try:
                validity = int(validity)
            except ValueError:
                try:
                    parts = validity.split('-')
                except TypeError:
                    parts = validity.split(b'-')
                nParts = len(parts)
                if nParts == 3:
                    try:                        # verify date
                        validity = date(*parts)
                    except:
                        raise ValueError('Not a valid date: %s.' % validity)
                elif nParts == 2:
                    try:                        # verify year and month
                        dt = date(parts[0], parts[1], 1)
                    except:
                        raise ValueError('Not a valid year / month: %s.' %
                                         validity)
                    else:
                        validity = (dt.year, dt.month)
                else:
                    raise ValueError('Not a valid period: %s.' % validity)
            else:
                date(validity, 1, 1)            # verify valid year
        elif isinstance(validity, tuple):
            try:                                # verify year and month
                dt = date(validity[0], validity[1], 1)
            except:
                raise ValueError('Not a valid year / month: %s.' %
                                 validity)
        elif isinstance(validity, int):
            date(validity, 1, 1)                # verify valid year
        elif not (validity is None or isinstance(validity, date)):
            raise ValueError('Not a valid period: %s.' % validity)
        # check type of validity
        typeOfValidity = self._typeOfValidity
        if typeOfValidity is None:
            self._typeOfValidity = typeOfValidity = type(validity)
        elif typeOfValidity is not type(validity):
            raise ValueError('Different types of validity periods given.')
        # update internal dict
        baseCurrency = self._baseCurrency
        it = (((validity, termCurrency),
               ExchangeRate(baseCurrency, unitMultiple, termCurrency,
                            termAmount))
              for termCurrency, termAmount, unitMultiple in rateSpecs)
        self._rateDict.update(it)

    def getRate(self, unitCurrency, termCurrency, effectiveDate=None):
        """Return exchange rate from `unitCurrency` to `termCurrency` that is
        effective for `effectiveDate`.

        Args:
            unitCurrency (:class:`Currency`): currency to be converted from
            termCurrency (:class:`Currency`): currency to be converted to
            effectiveDate (date): date at which the rate must be effective
                (default: None)

        If `effectiveDate` is not given, the return value of the callable
        given as `getDfltEffectiveDate` to :class:`MoneyConverter` is used as
        reference (default: today).

        Returns:
            :class:`ExchangeRate`: exchange rate from `unitCurrency` to
                `termCurrency` that is effective for `effectiveDate`, `None`
                if there is no such rate
        """
        if unitCurrency is termCurrency:
            return ExchangeRate(unitCurrency, 1, termCurrency, 1)
        baseCurrency = self.baseCurrency
        if baseCurrency == unitCurrency:
            try:
                return self._getRate(termCurrency, effectiveDate)
            except KeyError:
                return None
        elif baseCurrency == termCurrency:
            try:
                rate = self._getRate(unitCurrency, effectiveDate)
            except KeyError:
                return None
            else:
                return rate.inverted()
        else:
            try:
                unitRate = self._getRate(unitCurrency, effectiveDate)
                termRate = self._getRate(termCurrency, effectiveDate)
            except KeyError:
                return None
            else:
                return ExchangeRate(unitCurrency, 1, termCurrency,
                                    termRate.rate / unitRate.rate)

    def _getRate(self, termCurrency, effectiveDate):
        if effectiveDate is None:
            effectiveDate = self._getDfltEffectiveDate()
        validity = self._date2validity[self._typeOfValidity](effectiveDate)
        return self._rateDict[(validity, termCurrency)]

    def __enter__(self):
        """Register self as converter in class Currency."""
        Currency.registerConverter(self)
        return self

    def __exit__(self, *args):
        """Unregister self as converter in class Currency."""
        Currency.removeConverter(self)
        return None
