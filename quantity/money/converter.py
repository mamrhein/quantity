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
from decimalfp import Decimal
from .. import UnitConversionError
from . import Currency, ExchangeRate


__metaclass__ = type


class MoneyConverter:
    """Abstract base class of Money converters."""

    def __call__(self, moneyAmnt, toCurrency, effectiveDate=None):
        """Convert a money amount in one currency to the equivalent amount for
        another currency.

        Args:
            moneyAmnt (:class:`Money`): money amount to be converted
            toCurrency (:class:`Currency`): currency for which the  equivalent
                amount is to be returned
            effectiveDate (date): date for which the exchange rate used must
                be effective (default: None)

        If `effectiveDate` is not given, the current date is used as
        reference.

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

    def getRate(self, unitCurrency, termCurrency, effectiveDate=None):
        """Return exchange rate from `unitCurrency` to `termCurrency` that is
        effective for `effectiveDate`.

        Args:
            unitCurrency (:class:`Currency`): currency to be converted from
            termCurrency (:class:`Currency`): currency to be converted to
            effectiveDate (date): date at which the rate must be effective
                (default: None)

        If `effectiveDate` is not given, the current date is used as
        reference.

        Returns:
            :class:`ExchangeRate`: exchange rate from `unitCurrency` to
                `termCurrency` that is effective for `effectiveDate`, `None`
                if there is no such rate
        """
        if unitCurrency is termCurrency:
            return Decimal(1)
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
        return NotImplemented

    def __enter__(self):
        """Register self as converter in class Currency."""
        Currency.registerConverter(self)
        return self

    def __exit__(self, *args):
        """Unregister self as converter in class Currency."""
        Currency.removeConverter(self)
        return None


class ConstantRateConverter(MoneyConverter):
    """Money converter that uses constant rates for all times.
    """

    def __init__(self, unitCurrency, convTable):
        self._baseCurrency = unitCurrency
        self._rateDict = {termCurrency:
                          ExchangeRate(unitCurrency, unitMultiple,
                                       termCurrency, termAmount)
                          for termCurrency, termAmount, unitMultiple
                          in convTable}

    def _getRate(self, termCurrency, effectiveDate):
        return self._rateDict[termCurrency]


class YearlyRateConverter(MoneyConverter):
    """Money converter that uses different rates per year."""

    def __init__(self, unitCurrency, convTable):
        self._baseCurrency = unitCurrency
        self._rateDict = {(year, termCurrency):
                          ExchangeRate(unitCurrency, unitMultiple,
                                       termCurrency, termAmount)
                          for year, termCurrency, termAmount, unitMultiple
                          in convTable}

    def _getRate(self, termCurrency, effectiveDate, getDfltDate=date.today):
        dt = effectiveDate or getDfltDate()
        year = dt.year
        return self._rateDict[(year, termCurrency)]


class MonthlyRateConverter(MoneyConverter):
    """Money converter that uses different rates per month."""

    def __init__(self, unitCurrency, convTable):
        self._baseCurrency = unitCurrency
        self._rateDict = {(year, month, termCurrency):
                          ExchangeRate(unitCurrency, unitMultiple,
                                       termCurrency, termAmount)
                          for (year, month, termCurrency, termAmount,
                               unitMultiple)
                          in convTable}

    def _getRate(self, termCurrency, effectiveDate, getDfltDate=date.today):
        dt = effectiveDate or getDfltDate()
        year, month = dt.year, dt.month
        return self._rateDict[(year, month, termCurrency)]


class DailyRateConverter(MoneyConverter):
    """Money converter that uses different rates per day."""

    def __init__(self, unitCurrency, convTable):
        self._baseCurrency = unitCurrency
        self._rateDict = {(dt, termCurrency):
                          ExchangeRate(unitCurrency, unitMultiple,
                                       termCurrency, termAmount)
                          for dt, termCurrency, termAmount, unitMultiple
                          in convTable}

    def _getRate(self, termCurrency, effectiveDate, getDfltDate=date.today):
        dt = effectiveDate or getDfltDate()
        return self._rateDict[(dt, termCurrency)]
