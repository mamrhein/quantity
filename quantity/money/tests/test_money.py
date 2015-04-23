#!usr/bin/env python
# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        test_money
## Purpose:     Test driver for package quantity.money
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2015 Michael Amrhein
## License:     This program is part of a larger application. For license
##              details please read the file LICENSE.TXT provided together
##              with the application.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Test driver for package quantity.money"""


from __future__ import absolute_import, unicode_literals
import unittest
import operator
from fractions import Fraction
from decimalfp import Decimal
from quantity import IncompatibleUnitsError, UndefinedResultError
from quantity.money import Currency, Money, ExchangeRate
from quantity.money.currencies import getCurrencyInfo, registerCurrency


__metaclass__ = type


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
        self.assertRaises(TypeError, Money, 'x', EUR)
        self.assertRaises(ValueError, Money, 5)
        self.assertRaises(TypeError, Money, 'x EUR')
        self.assertRaises(ValueError, Money, '3 kg')
        self.assertRaises(IncompatibleUnitsError, Money, '3 EUR', HKD)
        self.assertEqual(Money.getQuantum(HKD), HKD.smallestFraction)
        m3eur = Money('3 EUR')
        self.assertTrue(m3eur.unit is EUR)
        self.assertTrue(m3eur.currency is EUR)
        self.assertEqual(m3eur.amount, Decimal(3))
        m333c = Money(Fraction(10, 3), EUR)
        self.assertEqual(m333c.amount, Decimal('3.33'))

    def testAlternateConstructor(self):
        EUR = registerCurrency('EUR')
        m30c = 0.30 ^ EUR
        self.assertTrue(m30c.unit is EUR)
        self.assertTrue(m30c.currency is EUR)
        self.assertEqual(m30c.amount, Decimal('0.3'))
        self.assertRaises(TypeError, operator.xor, EUR, 3)

    def testComputations(self):
        EUR = registerCurrency('EUR')
        HKD = registerCurrency('HKD')
        d = Decimal('0.3')
        m30c = d ^ EUR
        self.assertEqual(m30c + m30c, (d + d) ^ EUR)
        self.assertEqual(m30c - m30c, 0 ^ EUR)
        self.assertEqual(7 * m30c, (7 * d) ^ EUR)
        self.assertEqual(m30c / 7, (d / 7) ^ EUR)
        self.assertRaises(IncompatibleUnitsError, operator.add, m30c, 2 ^ HKD)
        self.assertRaises(IncompatibleUnitsError, operator.sub, m30c, 2 ^ HKD)
        self.assertRaises(UndefinedResultError, operator.mul, m30c, 2 ^ HKD)
        self.assertRaises(IncompatibleUnitsError, operator.truediv, m30c,
                          2 ^ HKD)
        self.assertRaises(UndefinedResultError, operator.pow, m30c, 2)


class Test3_ExchangeRate(unittest.TestCase):

    def testConstructor(self):
        EUR = registerCurrency('EUR')
        HKD = registerCurrency('HKD')
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
        EUR = registerCurrency('EUR')
        HKD = registerCurrency('HKD')
        USD = registerCurrency('USD')
        rateEUR2HKD = Decimal('8.395804')
        fxEUR2HKD = ExchangeRate(EUR, 1, HKD, rateEUR2HKD)
        rateEUR2USD = Decimal('1.0457')
        fxEUR2USD = ExchangeRate(EUR, 1, USD, rateEUR2USD)
        # inversion
        fxHKD2EUR = fxEUR2HKD.inverted()
        self.assertEqual(fxHKD2EUR.rate, Decimal(1 / rateEUR2HKD, 6))
        # ExchangeRate * Money
        self.assertEqual(fxEUR2HKD * (1 ^ EUR),
                         Money(rateEUR2HKD, HKD))
        self.assertEqual(fxEUR2HKD * (1000 ^ EUR),
                         Money(1000 * rateEUR2HKD, HKD))
        self.assertRaises(ValueError, operator.mul, fxEUR2HKD, 1 ^ HKD)
        # ExchangeRate * ExchangeRate
        fxUSD2HKD = fxHKD2EUR * fxEUR2USD
        self.assertEqual(fxUSD2HKD.rate,
                         Decimal(fxHKD2EUR.rate * fxEUR2USD.rate, 6))
        self.assertRaises(ValueError, operator.mul, fxEUR2HKD, fxEUR2USD)
        # unsupported multiplications
        self.assertRaises(TypeError, operator.mul, fxEUR2HKD, EUR)
        self.assertRaises(TypeError, operator.mul, fxEUR2HKD, 5)
        # Money / ExchangeRate
        self.assertEqual((100 ^ HKD) / fxEUR2HKD,
                         Money(Decimal(100 / rateEUR2HKD, 6), EUR))
        self.assertRaises(ValueError, operator.truediv, 1 ^ EUR, fxEUR2HKD)
        # ExchangeRate / ExchangeRate
        fxHKD2USD = fxEUR2HKD / fxEUR2USD
        self.assertEqual(fxHKD2USD.rate,
                         Decimal(fxEUR2HKD.rate / fxEUR2USD.rate, 6))
        self.assertRaises(ValueError, operator.truediv, fxHKD2EUR, fxEUR2USD)
        # unsupported divisions
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, 1 ^ HKD)
        self.assertRaises(TypeError, operator.truediv, EUR, fxEUR2HKD)
        self.assertRaises(TypeError, operator.truediv, 5, fxEUR2HKD)
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, EUR)
        self.assertRaises(TypeError, operator.truediv, fxEUR2HKD, 5)
