#!usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_money
## Purpose:     Test driver for package quantity.money
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) 2015 Michael Amrhein
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Test driver for package quantity.money"""


from __future__ import absolute_import, unicode_literals
import unittest
import operator
from datetime import date
from fractions import Fraction
from decimalfp import Decimal
from quantity import (Quantity, QuantityError, UndefinedResultError,
                      IncompatibleUnitsError, UnitConversionError)
from quantity.money import (Currency, Money, ExchangeRate,
                            getCurrencyInfo, registerCurrency)
from quantity.predefined import Mass, GRAM, KILOGRAM, OUNCE
from quantity.money.converter import (ConstantRateConverter,
                                      DailyRateConverter,
                                      MonthlyRateConverter,
                                      YearlyRateConverter)


__metaclass__ = type


EUR = registerCurrency('EUR')
HKD = registerCurrency('HKD')
USD = registerCurrency('USD')
ZWL = registerCurrency('ZWL')


class PricePerMass(Quantity):
    defineAs = Money / Mass

EURpKG = PricePerMass.Unit(defineAs=EUR / KILOGRAM)
HKDpKG = PricePerMass.Unit(defineAs=HKD / KILOGRAM)


class Test1_Currency(unittest.TestCase):

    def testConstructor(self):
        self.assertRaises(TypeError, Currency, 5)
        self.assertRaises(ValueError, Currency, '')
        self.assertRaises(TypeError, Currency, 'XXT', 'XTest', 3.4)
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', -1)
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', None, 'a')
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', None,
                          Fraction(1, 3))
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', None, '-0.1')
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', None, 1)
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', None, '0.03')
        self.assertRaises(ValueError, Currency, 'XXT', 'XTest', 3, '0.1')
        XXT = Currency('XXT', 'XTest', 3)
        self.assertEqual(XXT.isoCode, 'XXT')
        self.assertEqual(XXT.isoCode, XXT.symbol)
        self.assertEqual(XXT.name, 'XTest')
        self.assertEqual(XXT.smallestFraction, Decimal('0.001'))
        self.assertTrue(Currency.getUnitBySymbol('XXT') is XXT)
        self.assertTrue(Currency('XXT') is XXT)

    def testCurrencyDatabase(self):
        self.assertEqual(getCurrencyInfo('EUR')[0], 'EUR')
        self.assertRaises(ValueError, getCurrencyInfo, 'abc')
        EUR = registerCurrency('EUR')
        self.assertTrue(EUR is Currency.getUnitBySymbol('EUR'))


class Test2_Money(unittest.TestCase):

    def testConstructor(self):
        EUR = registerCurrency('EUR')
        HKD = registerCurrency('HKD')
        self.assertRaises(QuantityError, Money, 'x', EUR)
        self.assertRaises(QuantityError, Money, 5)
        self.assertRaises(QuantityError, Money, 'x EUR')
        self.assertRaises(QuantityError, Money, '3 fgh')
        self.assertRaises(QuantityError, Money, '3 kg')
        self.assertRaises(UnitConversionError, Money, '3 EUR', HKD)
        self.assertEqual(Money.getQuantum(HKD), HKD.smallestFraction)
        m3eur = Money('3 EUR')
        self.assertTrue(m3eur.unit is EUR)
        self.assertTrue(m3eur.currency is EUR)
        self.assertEqual(m3eur.amount, Decimal(3))
        m333c = Money(Fraction(10, 3), EUR)
        self.assertEqual(m333c.amount, Decimal('3.33'))
        p = Quantity('3.17 EUR/kg')
        self.assertEqual(p.amount, Decimal('3.17'))
        self.assertTrue(p.unit is EURpKG)

    def testAlternateConstructor(self):
        m30c = 0.30 ^ EUR
        self.assertTrue(m30c.unit is EUR)
        self.assertTrue(m30c.currency is EUR)
        self.assertEqual(m30c.amount, Decimal('0.3'))
        self.assertRaises(TypeError, operator.xor, EUR, 3)

    def testComputations(self):
        d = Decimal('0.3')
        m30c = d ^ EUR
        self.assertEqual(m30c + m30c, (d + d) ^ EUR)
        self.assertEqual(m30c - m30c, 0 ^ EUR)
        self.assertEqual(7 * m30c, (7 * d) ^ EUR)
        self.assertEqual(m30c / 7, (d / 7) ^ EUR)
        self.assertRaises(UnitConversionError, operator.add, m30c, 2 ^ HKD)
        self.assertRaises(IncompatibleUnitsError,
                          operator.add, m30c, 2 ^ GRAM)
        self.assertRaises(UnitConversionError, operator.sub, m30c, 2 ^ HKD)
        self.assertRaises(IncompatibleUnitsError,
                          operator.sub, m30c, 2 ^ GRAM)
        self.assertRaises(UndefinedResultError, operator.mul, m30c, 2 ^ HKD)
        self.assertRaises(UnitConversionError, operator.truediv, m30c,
                          2 ^ HKD)
        self.assertRaises(UndefinedResultError, operator.pow, m30c, 2)

    def testMixedComputations(self):
        d = Decimal('12.647')
        p = d ^ EURpKG
        self.assertEqual(2 * p, (2 * d) ^ EURpKG)
        self.assertEqual(p * 5, (5 * d) ^ EURpKG)
        self.assertEqual(p / 5, (d / 5) ^ EURpKG)
        self.assertRaises(UndefinedResultError, operator.truediv, 5, p)
        m = 1.5 ^ KILOGRAM
        self.assertEqual(m * p, (1.5 * d) ^ EUR)
        self.assertEqual(m * p, p * m)
        m = 500 ^ GRAM
        self.assertEqual(m * p, (d / 2) ^ EUR)
        m = 24 ^ OUNCE
        self.assertEqual(m * p, Decimal(24 * KILOGRAM(OUNCE) * d, 2) ^ EUR)
        self.assertRaises(UndefinedResultError, operator.truediv, m, p)
        self.assertRaises(UndefinedResultError, operator.truediv, p, m)


class Test3_ExchangeRate(unittest.TestCase):

    def testConstructor(self):
        # unknown ISO 4217 code given for a currency:
        self.assertRaises(ValueError, ExchangeRate, 'abc', 1, EUR, 1)
        self.assertRaises(ValueError, ExchangeRate, EUR, 1, 'abc', 1)
        # wrong type of value given as currency
        self.assertRaises(TypeError, ExchangeRate, 3, 1, EUR, 1)
        self.assertRaises(TypeError, ExchangeRate, EUR, 1, 3, 1)
        # identical currencies
        self.assertRaises(ValueError, ExchangeRate, EUR, 1, EUR, 1)
        self.assertRaises(ValueError, ExchangeRate, EUR, 1, 'EUR', 1)
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 1, EUR, 1)
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 1, 'EUR', 1)
        # unit multiple not an Integral or not >= 1
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 'a', 'HKD', 1)
        self.assertRaises(ValueError, ExchangeRate, 'EUR', Decimal('0.1'),
                          'HKD', 1)
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 0.1, 'HKD', 1)
        # term amount < 0.000001
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 1, 'HKD',
                          Decimal('0.0000009'))
        # term amount not convertable to a Decimal
        self.assertRaises(ValueError, ExchangeRate, 'EUR', 1, 'HKD', '0.x')
        # test attributes
        rate = Decimal('8.395804')
        exch = ExchangeRate(EUR, 1, HKD, rate)
        self.assertTrue(exch.unitCurrency is EUR)
        self.assertTrue(exch.termCurrency is HKD)
        self.assertEqual(exch.rate, rate)
        self.assertEqual(exch.inverseRate, 1 / rate)
        self.assertEqual(exch.quotation, (EUR, HKD, rate))
        self.assertEqual(exch.inverseQuotation, (HKD, EUR, 1 / rate))
        # test adjustment
        rate = Decimal('0.00000927')
        exch = ExchangeRate(EUR, 1, HKD, rate)
        self.assertEqual(exch._unitMultiple, Decimal(100000))
        self.assertEqual(exch._termAmount, Decimal('0.927', 6))
        self.assertEqual(exch.rate, rate)
        exch2 = ExchangeRate('EUR', 50, 'HKD', 50 * rate)
        self.assertEqual(exch.rate, exch2.rate)

    def testComputations(self):
        rateEUR2HKD = Decimal('8.395804')
        fxEUR2HKD = ExchangeRate(EUR, 1, HKD, rateEUR2HKD)
        rateEUR2USD = Decimal('1.0457')
        fxEUR2USD = ExchangeRate(EUR, 1, USD, rateEUR2USD)
        # inversion
        fxHKD2EUR = fxEUR2HKD.inverted()
        self.assertEqual(fxHKD2EUR.rate, Decimal(1 / rateEUR2HKD, 6))
        fxUSD2EUR = fxEUR2USD.inverted()
        self.assertTrue(fxUSD2EUR.unitCurrency is USD)
        self.assertTrue(fxUSD2EUR.termCurrency is EUR)
        # ExchangeRate * Money
        self.assertEqual(fxEUR2HKD * (1 ^ EUR),
                         Money(rateEUR2HKD, HKD))
        self.assertEqual(fxEUR2HKD * (1000 ^ EUR),
                         Money(1000 * rateEUR2HKD, HKD))
        self.assertRaises(ValueError, operator.mul, fxEUR2HKD, 1 ^ HKD)
        # ExchangeRate * Money/Quantity
        d = Decimal('12.647')
        p = d ^ EURpKG
        self.assertEqual(fxEUR2HKD * p, PricePerMass(d * rateEUR2HKD, HKDpKG))
        self.assertEqual(p * fxEUR2HKD, PricePerMass(d * rateEUR2HKD, HKDpKG))
        self.assertRaises(QuantityError, operator.mul, fxHKD2EUR, p)
        self.assertRaises(QuantityError, operator.mul, p, fxHKD2EUR)
        self.assertRaises(QuantityError, operator.mul, fxEUR2USD, p)
        self.assertRaises(QuantityError, operator.mul, p, fxEUR2USD)
        # ExchangeRate * ExchangeRate
        fxHKD2USD = fxHKD2EUR * fxEUR2USD
        self.assertEqual(fxHKD2USD.rate,
                         Decimal(fxHKD2EUR.rate * fxEUR2USD.rate, 6))
        self.assertTrue(fxHKD2USD.unitCurrency is HKD)
        self.assertTrue(fxHKD2USD.termCurrency is USD)
        fxUSD2HKD = fxEUR2HKD * fxUSD2EUR
        self.assertEqual(fxUSD2HKD.rate,
                         Decimal(fxEUR2HKD.rate * fxUSD2EUR.rate, 6))
        self.assertTrue(fxUSD2HKD.unitCurrency is USD)
        self.assertTrue(fxUSD2HKD.termCurrency is HKD)
        self.assertRaises(ValueError, operator.mul, fxEUR2HKD, fxEUR2USD)
        # unsupported multiplications
        self.assertRaises(TypeError, operator.mul, fxEUR2HKD, EUR)
        self.assertRaises(TypeError, operator.mul, fxEUR2HKD, 5)
        self.assertRaises(TypeError, operator.mul, fxEUR2HKD, Mass(7))
        # Money / ExchangeRate
        self.assertEqual((100 ^ HKD) / fxEUR2HKD,
                         Money(Decimal(100 / rateEUR2HKD, 6), EUR))
        self.assertRaises(ValueError, operator.truediv, 1 ^ EUR, fxEUR2HKD)
        # Money/Quantity / ExchangeRate
        self.assertEqual(p / fxHKD2EUR,
                         PricePerMass(d / fxHKD2EUR.rate, HKDpKG))
        self.assertRaises(QuantityError, operator.truediv, p, fxEUR2HKD)
        # ExchangeRate / ExchangeRate
        fxUSD2HKD = fxEUR2HKD / fxEUR2USD
        self.assertEqual(fxUSD2HKD.rate,
                         Decimal(fxEUR2HKD.rate / fxEUR2USD.rate, 6))
        self.assertTrue(fxUSD2HKD.unitCurrency is USD)
        self.assertTrue(fxUSD2HKD.termCurrency is HKD)
        fxHKD2USD = fxHKD2EUR / fxUSD2EUR
        self.assertEqual(fxHKD2USD.rate,
                         Decimal(fxHKD2EUR.rate / fxUSD2EUR.rate, 6))
        self.assertTrue(fxHKD2USD.unitCurrency is HKD)
        self.assertTrue(fxHKD2USD.termCurrency is USD)
        self.assertEqual(fxHKD2EUR / fxUSD2EUR, fxEUR2USD / fxEUR2HKD)
        self.assertRaises(ValueError, operator.truediv, fxHKD2EUR, fxEUR2USD)
        # unsupported divisions
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, 1 ^ HKD)
        self.assertRaises(TypeError, operator.truediv, EUR, fxEUR2HKD)
        self.assertRaises(TypeError, operator.truediv, 5, fxEUR2HKD)
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, EUR)
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, 5)
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, Mass(7))
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, p)


class Test4_Converter(unittest.TestCase):

    def setUp(self):
        constantRates = [(USD, Decimal('1.2'), 1),
                         (HKD, Decimal('8.5'), 1)]
        self.constantRateConverter = ConstantRateConverter(EUR, constantRates)
        dailyRates = list(_genRates())
        self.dailyRateConverter = DailyRateConverter(EUR, dailyRates)
        monthlyRates = [(dt.year, dt.month, termCurrency, termAmount,
                         unitMultiple)
                        for dt, termCurrency, termAmount, unitMultiple
                        in dailyRates if dt.day == 1]
        self.monthlyRateConverter = MonthlyRateConverter(EUR, monthlyRates)
        yearlyRates = [(year, termCurrency, termAmount,
                        unitMultiple)
                       for year, month, termCurrency, termAmount, unitMultiple
                       in monthlyRates if month == 1]
        self.yearlyRateConverter = YearlyRateConverter(EUR, yearlyRates)

    def testRates(self):
        today = date.today()
        year, month, day = today.timetuple()[:3]
        # constant rates
        conv = self.constantRateConverter
        self.assertEqual(conv.baseCurrency, EUR)
        rateEUR2USD = conv.getRate(EUR, USD, today)
        self.assertEqual(rateEUR2USD.quotation, (EUR, USD, Decimal('1.2')))
        rateHKD2EUR = conv.getRate(HKD, EUR)
        self.assertEqual(rateHKD2EUR, conv.getRate(EUR, HKD).inverted())
        rateHKD2USD = conv.getRate(HKD, USD, date(2004, 12, 17))
        self.assertEqual(rateHKD2USD,
                         conv.getRate(EUR, USD) / conv.getRate(EUR, HKD))
        rateZWL2EUR = conv.getRate(ZWL, EUR)
        self.assertEqual(rateZWL2EUR, None)
        # daily rates
        conv = self.dailyRateConverter
        rateEUR2USD = conv.getRate(EUR, USD)
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (day, month, year)))
        rateEUR2USD = conv.getRate(EUR, USD, date(year, 1, 1))
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (1, 1, year)))
        rateEUR2HKD = conv.getRate(EUR, HKD, date(year - 1, 2, 2))
        self.assertEqual(rateEUR2HKD.rate,
                         2 * Decimal("%i.%02i%i" % (2, 2, year - 1)))
        if day <= 3:
            refDate = date(year, month, 4)
        else:
            refDate = date(year, month, day - 1)
        rateEUR2HKD = conv.getRate(EUR, HKD, refDate)
        self.assertEqual(rateEUR2HKD, None)
        # monthly rates
        conv = self.monthlyRateConverter
        rateEUR2USD = conv.getRate(EUR, USD)
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (1, month, year)))
        rateEUR2USD = conv.getRate(EUR, USD, date(year, 1, 17))
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (1, 1, year)))
        rateEUR2HKD = conv.getRate(EUR, HKD, date(year - 1, 2, 24))
        self.assertEqual(rateEUR2HKD.rate,
                         2 * Decimal("%i.%02i%i" % (1, 2, year - 1)))
        if month <= 3:
            refDate = date(year, 4, 14)
        else:
            refDate = date(year, month - 1, 14)
        rateEUR2HKD = conv.getRate(EUR, HKD, refDate)
        self.assertEqual(rateEUR2HKD, None)
        # yearly rates
        conv = self.yearlyRateConverter
        rateEUR2USD = conv.getRate(EUR, USD)
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (1, 1, year)))
        rateEUR2USD = conv.getRate(EUR, USD, date(year, 11, 17))
        self.assertEqual(rateEUR2USD.rate,
                         Decimal("%i.%02i%i" % (1, 1, year)))
        rateEUR2HKD = conv.getRate(EUR, HKD, date(year - 1, 2, 24))
        self.assertEqual(rateEUR2HKD.rate,
                         2 * Decimal("%i.%02i%i" % (1, 1, year - 1)))
        rateEUR2HKD = conv.getRate(EUR, HKD, date(year - 2, 1, 1))
        self.assertEqual(rateEUR2HKD, None)

    def testRegistration(self):
        # assert that there are no registered money converters yet
        self.assertFalse(list(Currency.registeredConverters()))
        Currency.registerConverter(self.constantRateConverter)
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.constantRateConverter])
        Currency.registerConverter(self.monthlyRateConverter)
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.monthlyRateConverter,
                          self.constantRateConverter])
        self.assertRaises(ValueError, Currency.removeConverter,
                          self.yearlyRateConverter)
        self.assertRaises(ValueError, Currency.removeConverter,
                          self.constantRateConverter)
        Currency.registerConverter(self.monthlyRateConverter)
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.monthlyRateConverter,
                          self.monthlyRateConverter,
                          self.constantRateConverter])
        Currency.removeConverter(self.monthlyRateConverter)
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.monthlyRateConverter,
                          self.constantRateConverter])
        Currency.removeConverter(self.monthlyRateConverter)
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.constantRateConverter])
        with self.constantRateConverter as conv1:
            self.assertEqual(list(Currency.registeredConverters()),
                             [conv1, self.constantRateConverter])
            with self.yearlyRateConverter as conv2:
                self.assertEqual(conv2, self.yearlyRateConverter)
                self.assertEqual(list(Currency.registeredConverters()),
                                 [conv2, conv1, self.constantRateConverter])
            self.assertEqual(list(Currency.registeredConverters()),
                             [conv1, self.constantRateConverter])
        self.assertEqual(list(Currency.registeredConverters()),
                         [self.constantRateConverter])
        Currency.removeConverter(self.constantRateConverter)
        self.assertFalse(list(Currency.registeredConverters()))

    def testConversion(self):
        today = date.today()
        year, month, day = today.timetuple()[:3]
        # assert that there are no registered money converters yet
        self.assertFalse(list(Currency.registeredConverters()))
        m4EUR = 4 ^ EUR
        self.assertRaises(UnitConversionError, m4EUR.convert, USD)
        with self.constantRateConverter:
            self.assertEqual(m4EUR.convert(USD), Decimal('4.8') ^ USD)
            with self.yearlyRateConverter:
                amnt = 4 * Decimal("%i.%02i%i" % (1, 1, year))
                self.assertEqual(m4EUR.convert(USD), amnt ^ USD)
                with self.monthlyRateConverter:
                    amnt = 4 * Decimal("%i.%02i%i" % (1, month, year))
                    self.assertEqual(m4EUR.convert(USD), amnt ^ USD)
                    with self.dailyRateConverter:
                        amnt = 4 * Decimal("%i.%02i%i" % (day, month, year))
                        self.assertEqual(m4EUR.convert(USD), amnt ^ USD)
                    amnt = 4 * Decimal("%i.%02i%i" % (1, month, year))
                    self.assertEqual(m4EUR.convert(USD), amnt ^ USD)
                amnt = 4 * Decimal("%i.%02i%i" % (1, 1, year))
                self.assertEqual(m4EUR.convert(USD), amnt ^ USD)
            self.assertEqual(m4EUR.convert(USD), Decimal('4.8') ^ USD)
        # assert that there are no registered money converters yet
        self.assertFalse(list(Currency.registeredConverters()))


# helper functions


def _genRates():
    today = date.today()
    thisYear = today.year
    prevYear = thisYear - 1
    thisMonth = today.month
    for day in (1, 2):
        for month in (1, 2, thisMonth):
            for year in (prevYear, thisYear):
                dt = date(year, month, day)
                rate = Decimal("%i.%02i%i" % (day, month, year))
                yield (dt, USD, rate, 1)
                yield (dt, HKD, 2 * rate, 1)
    year, month, day = today.timetuple()[:3]
    rate = Decimal("%i.%02i%i" % (day, month, year))
    yield (today, USD, rate, 1)
    yield (today, HKD, 2 * rate, 1)
