#!usr/bin/env python
# -*- coding: utf-8 -*-
##****************************************************************************
## Name:        test_quantity
## Purpose:     Test driver for module quantity
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) Michael Amrhein
##****************************************************************************
## $Source$
## $Revision$


from __future__ import absolute_import, division, unicode_literals
import unittest
import operator
from pickle import dumps, loads
from fractions import Fraction
from decimal import Decimal as StdLibDecimal
from decimalfp import Decimal, set_rounding
from decimalfp import ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, ROUND_HALF_UP, \
    ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_05UP
from quantity import (Quantity, Unit, getUnitBySymbol, generateUnits, sum,
                      QuantityError, UndefinedResultError,
                      IncompatibleUnitsError, UnitConversionError,
                      TableConverter)
from quantity.qtybase import typearg, MetaQTerm, _registry
from quantity.term import _mulSign, _SUPERSCRIPT_CHARS

rounding_modes = [ROUND_DOWN, ROUND_UP, ROUND_HALF_DOWN, ROUND_HALF_UP,
                  ROUND_HALF_EVEN, ROUND_CEILING, ROUND_FLOOR, ROUND_05UP]

# Python 2 / Python 3:
try:
    int.__round__
except AttributeError:
    PY_VERSION = 2

    # support __round__ in 2.x
    import __builtin__
    py2_round = __builtin__.round

    def round(number, ndigits=0):
        try:
            return number.__round__(ndigits)
        except AttributeError:
            return py2_round(number, ndigits)

    # unicode handling
    bytes = str
    str = unicode
else:
    PY_VERSION = 3


QTerm = Quantity._QTerm


class X(Quantity):
    refUnitName = 'XUnit'
    refUnitSymbol = 'x'

x = X.refUnit
kx = X.Unit('kx', 'kilox', X('1000'))
Mx = X.Unit('Mx', 'megax', X('1000', kx))


class Xinv(Quantity):
    defineAs = X ** -1


class Y(Quantity):
    refUnitName = 'YUnit'
    refUnitSymbol = 'y'

y = Y.refUnit
sy = Y.Unit('sy', '60y', Y('60'))
ssy = Y.Unit('ssy', '60sy', Y('60', sy))


defXpY = X / Y
class XpY(Quantity):
    defineAs = defXpY

xpy = XpY.refUnit
x30py = XpY.Unit('30x/y', '', Decimal(30) * xpy)


defYpX = Y * X ** -1
class YpX(Quantity):
    defineAs = defYpX

ypx = YpX.refUnit


class Z(Quantity):
    refUnitName = 'ZUnit'
    refUnitSymbol = 'z'

z = Z.refUnit


defZ2 = Z ** 2
class Z2(Quantity):
    defineAs = defZ2


defXtZ2pY = XpY * Z2
class XtZ2pY(Quantity):
    defineAs = defXtZ2pY


class A(Quantity):
    defineAs = X * Y


defK = A * Y / Z ** 3
class K(Quantity):
    defineAs = defK
    refUnitName = 'KUnit',
    refUnitSymbol = 'k'


# Quantity without reference unit
class U(Unit):
    pass
class Q(Quantity):
    Unit = U

u1 = U('u1', 'Q unit 1')
u2 = U('u2')
u3 = U('u3')

# x u1 = (5 * x - 3) u2 = (25 * x + 1.5) u3
uConvTab1 = [(u1, u2, Decimal(5), -3),
             (u2, u1, Decimal('0.2'), Decimal('0.6')),
             (u1, u3, Decimal(25), Decimal('1.5')),
             (u3, u2, Decimal('0.2'), Decimal('-3.3'))]
uConv1 = TableConverter(uConvTab1)

# x u1 = (5 * x - 1) u2
uConvTab2 = [(u1, u2, Decimal(5), -1)]
uConv2 = TableConverter(uConvTab2)


defQpX = Q / X
class QpX(Quantity):
    defineAs = defQpX

for qu in U.registeredUnits():
    for xu in X.Unit.registeredUnits():
        upx = QpX.Unit("%s/%s" % (qu.symbol, xu.symbol), defineAs=qu / xu)

u1px = QpX.Unit('u1/x')
u2pkx = QpX.Unit('u2/kx')


# quantized quantity
class T(Quantity):
    refUnitSymbol = 't'
    refUnitName = 't1'
    quantum = '0.02'

t = T.refUnit
kt = T.Unit('kt', 't1k', Decimal(1000) * t)


class Test1_MetaQTerm(unittest.TestCase):

    def testConstructor(self):
        self.assertTrue(X._clsDefinition is None)
        self.assertEqual(X.clsDefinition, X._QClsDefinition([(X, 1)]))
        self.assertTrue(X.Unit._clsDefinition is None)
        self.assertEqual(X.Unit.clsDefinition,
                         X.Unit._QClsDefinition([(X.Unit, 1)]))
        self.assertEqual(Xinv.clsDefinition, Xinv._QClsDefinition([(X, -1)]))
        self.assertEqual(Xinv.Unit.clsDefinition,
                         Xinv.Unit._QClsDefinition([(X.Unit, -1)]))
        self.assertTrue(XpY._clsDefinition is defXpY)
        self.assertTrue(XpY.Unit.Quantity is XpY)
        self.assertTrue(isinstance(XpY.refUnit, XpY.Unit))
        self.assertEqual(XpY.Unit._clsDefinition, X.Unit / Y.Unit)
        self.assertTrue(XtZ2pY._clsDefinition is defXtZ2pY)
        self.assertEqual(XtZ2pY.normalizedClsDefinition, X * Z ** 2 / Y)
        self.assertTrue(XtZ2pY.Unit.Quantity is XtZ2pY)
        self.assertTrue(isinstance(XtZ2pY.refUnit, XtZ2pY.Unit))
        self.assertEqual(XtZ2pY.Unit._clsDefinition, XpY.Unit * Z2.Unit)
        self.assertEqual(XtZ2pY.refUnit.symbol, ''.join(('x', _mulSign,
                         'z', _SUPERSCRIPT_CHARS[0], '/y')))
        self.assertEqual(XtZ2pY.refUnitSymbol, XtZ2pY.refUnit.symbol)
        self.assertRaises(TypeError, X, 'a')
        self.assertRaises(TypeError, X, 5, y)
        self.assertTrue(Q.refUnit is None)
        self.assertFalse(hasattr(u1, '__dict__'))
        self.assertFalse(hasattr(Q(2, u1), '__dict__'))
        for attr in ['refUnitSymbol', 'refUnitName', 'quantum']:
            self.assertTrue(hasattr(T, attr))
            self.assertRaises(AttributeError, setattr, X, attr, 'a')
        self.assertEqual(T.quantum, Decimal('0.02'))
        self.assertEqual(X.quantum, None)

    def testQuantityReg(self):
        self.assertTrue(_registry.getQuantityCls(X.clsDefinition) is X)
        self.assertRaises(ValueError, MetaQTerm, typearg('X_Y'),
                          (Quantity,), {typearg('defineAs'): defXpY})

    def testUnitReg(self):
        self.assertTrue(X.Unit._symDict[X.refUnit.symbol] is X.refUnit)
        self.assertTrue(X.Unit._symDict['kx'] is kx)
        self.assertRaises(ValueError, X.Unit, 'xx')
        self.assertEqual(K._refUnitDef,
                         K._QTerm(((qtyCls.refUnit, exp)
                                   for qtyCls, exp in K.clsDefinition)))
        self.assertTrue(K.Unit._symDict['k'] is K.refUnit)
        self.assertTrue(Q.Unit('u1') is u1)
        self.assertTrue(sorted([u.symbol for u in U.registeredUnits()])
                        == ['u1', 'u2', 'u3'])

    def testOperandTypeErrors(self):
        self.assertRaises(TypeError, operator.mul, X, 5)
        self.assertRaises(TypeError, operator.mul, X, X(1))
        self.assertRaises(TypeError, operator.mul, 5, X)
        self.assertRaises(TypeError, operator.mul, X(1), X)
        if PY_VERSION < 3:
            self.assertRaises(TypeError, operator.div, X, 5)
            self.assertRaises(TypeError, operator.div, X, X(1))
            self.assertRaises(TypeError, operator.div, 5, X)
            self.assertRaises(TypeError, operator.div, X(1), X)
        self.assertRaises(TypeError, operator.truediv, X, 5)
        self.assertRaises(TypeError, operator.truediv, X, X(1))
        self.assertRaises(TypeError, operator.truediv, 5, X)
        self.assertRaises(TypeError, operator.truediv, X(1), X)
        self.assertRaises(TypeError, operator.pow, X, 5.)
        self.assertRaises(TypeError, operator.pow, X, X(1))
        self.assertRaises(TypeError, operator.pow, 5, X)
        self.assertRaises(TypeError, operator.pow, X(1), X)

    def testGetUnitBySymbol(self):
        for qty in [X, Xinv, Y, XpY, YpX, Z, Z2, XtZ2pY, K, Q, QpX]:
            for unit in qty.Unit.registeredUnits():
                self.assertTrue(getUnitBySymbol(unit.symbol) is unit)

    def testGenerateUnits(self):
        # 'K' has only a reference unit so far
        self.assertEqual(len(list(K.Unit.registeredUnits())), 1)
        # create units from cross-product A * Y * Z (has 3 elements)
        generateUnits(K)
        # 3 new symbols created
        self.assertEqual(len(list(K.Unit.registeredUnits())), 4)
        # but only 2 new units
        self.assertEqual(len(K.Unit._termDict), 3)
        # test exception
        self.assertRaises(ValueError, generateUnits, X)


class Test2_Unit(unittest.TestCase):

    def testConstructor(self):
        self.assertEqual(u1.symbol, 'u1')
        self.assertEqual(u1.name, 'Q unit 1')
        self.assertEqual(u2.symbol, u2.name)
        self.assertTrue(u1._definition is None)
        self.assertTrue(U('u3') is u3)
        self.assertRaises(TypeError, X.Unit, b'ax', '', X(10))
        self.assertRaises(TypeError, X.Unit, 5, 'xxx', X(10))
        self.assertRaises(ValueError, X.Unit, '', '', X(10))
        self.assertEqual(kx.name, 'kilox')
        self.assertEqual(kx.symbol, 'kx')
        self.assertEqual(kx.definition.amount, 1000)
        self.assertEqual(kx.definition.unitTerm, x.definition)
        self.assertEqual(Mx.definition.amount, 1000)
        self.assertEqual(list(Mx.definition.unitTerm), [(kx, 1)])
        sypkx = YpX.Unit(None, 'sypkx', sy / kx)
        self.assertEqual(sypkx.symbol, str(sy / kx))

    def testHash(self):
        self.assertEqual(hash(x), hash(('X', 'x')))

    def testCoercions(self):
        self.assertEqual(x(kx), 1000)
        self.assertEqual(kx(x), Decimal('0.001'))
        self.assertEqual(x(Mx), 1000000)
        self.assertEqual(kx(Mx), 1000)
        self.assertEqual(Mx(kx), Decimal('0.001'))
        self.assertEqual(Mx(x), Decimal('0.000001'))
        q5kx = X(5, kx)
        self.assertEqual(kx(q5kx), 5)
        self.assertEqual(x(q5kx), 5000)
        self.assertEqual(Mx(q5kx), Decimal('0.005'))
        q500x = X(500, x)
        self.assertEqual(x(q500x), 500)
        self.assertEqual(kx(q500x), Decimal('0.5'))
        self.assertEqual(Mx(q500x), Decimal('0.0005'))
        xtz2py = XtZ2pY.refUnit
        q = (X('3', Mx) / Y('1', ssy)) * Z('3') ** 2
        self.assertEqual(round(xtz2py(q)), 7500)
        self.assertRaises(IncompatibleUnitsError, Mx, y)
        self.assertRaises(UnitConversionError, u1, u2)

    def testComparision(self):
        self.assertEqual(x, x)
        self.assertEqual(kx, kx)
        self.assertTrue(x < kx)
        self.assertFalse(x < x)
        self.assertTrue(Mx > x)
        self.assertTrue(kx < Mx)
        self.assertNotEqual(x, 'abc')
        self.assertTrue(x != u1)
        self.assertTrue(u1 != u2)
        self.assertRaises(IncompatibleUnitsError, operator.lt, x, y)
        self.assertRaises(IncompatibleUnitsError, operator.le, x, y)
        self.assertRaises(IncompatibleUnitsError, operator.gt, x, y)
        self.assertRaises(IncompatibleUnitsError, operator.ge, x, y)
        q1x = X(1)
        self.assertFalse(q1x == x)
        self.assertFalse(x == q1x)
        self.assertTrue(q1x != x)
        self.assertTrue(x != q1x)
        if PY_VERSION == 2:
            self.assertEqual(x.__lt__(q1x), NotImplemented)
            self.assertEqual(x.__le__(q1x), NotImplemented)
            self.assertEqual(x.__gt__(q1x), NotImplemented)
            self.assertEqual(x.__ge__(q1x), NotImplemented)
            self.assertEqual(q1x.__lt__(x), NotImplemented)
            self.assertEqual(q1x.__le__(x), NotImplemented)
            self.assertEqual(q1x.__gt__(x), NotImplemented)
            self.assertEqual(q1x.__ge__(x), NotImplemented)
        else:
            self.assertRaises(TypeError, operator.lt, x, q1x)
            self.assertRaises(TypeError, operator.le, x, q1x)
            self.assertRaises(TypeError, operator.gt, x, q1x)
            self.assertRaises(TypeError, operator.ge, x, q1x)
            self.assertRaises(TypeError, operator.lt, q1x, x)
            self.assertRaises(TypeError, operator.le, q1x, x)
            self.assertRaises(TypeError, operator.gt, q1x, x)
            self.assertRaises(TypeError, operator.ge, q1x, x)

    def testAddition(self):
        self.assertRaises(TypeError, operator.add, x, 3)
        self.assertRaises(TypeError, operator.add, x, x)
        self.assertRaises(TypeError, operator.add, X(1), x)
        self.assertRaises(TypeError, operator.add, x, X(1))

    def testSubtraction(self):
        self.assertRaises(TypeError, operator.sub, x, 3)
        self.assertRaises(TypeError, operator.sub, x, x)
        self.assertRaises(TypeError, operator.sub, X(1), x)
        self.assertRaises(TypeError, operator.sub, x, X(1))

    def testMultiplication(self):
        self.assertEqual(3 * z, QTerm(((3, 1), (z, 1))))
        self.assertEqual(3 * z, z * 3)
        self.assertEqual(x * z, QTerm(((x, 1), (z, 1))))
        self.assertEqual(x * z, z * x)
        self.assertEqual(x * z * z, QTerm(((x, 1), (z, 2))))
        self.assertRaises(TypeError, operator.mul, x, 'a')
        self.assertRaises(TypeError, operator.mul, 'a', x)
        self.assertRaises(TypeError, operator.mul, x, X(3))
        self.assertRaises(TypeError, operator.mul, X(3), x)

    def testDivision(self):
        self.assertEqual(3 / z, QTerm(((3, 1), (z, -1))))
        self.assertEqual(z / 2, QTerm(((0.5, 1), (z, 1))))
        self.assertEqual(x / z, QTerm(((x, 1), (z, -1))))
        self.assertEqual(z / x, QTerm(((x, -1), (z, 1))))
        self.assertEqual(x30py / xpy, QTerm(((Decimal(30), 1),)))
        self.assertEqual(z / x / z, QTerm(((x, -1),)))
        self.assertEqual(z / (x / y), QTerm(((x, -1), (y, 1), (z, 1))))
        self.assertRaises(TypeError, operator.truediv, x, 'a')
        self.assertRaises(TypeError, operator.truediv, 'a', x)
        self.assertRaises(TypeError, operator.truediv, x, X(3))
        self.assertRaises(TypeError, operator.truediv, X(3), x)

    def testPower(self):
        self.assertEqual(z ** 2, QTerm(((z, 2),)))
        self.assertEqual(x ** -3, QTerm(((x, -3),)))
        self.assertRaises(TypeError, operator.pow, z, 2.5)


class Test3_Quantity(unittest.TestCase):

    def testConstructor(self):
        qx = X(3)
        self.assertTrue(qx.unit is x)
        self.assertEqual(qx.amount, 3)
        qx = X(StdLibDecimal('3.2'))
        self.assertTrue(qx.unit is x)
        self.assertEqual(qx.amount, Decimal('3.2'))
        qx = X('32')
        self.assertEqual(qx.amount, 32)
        qx = X('32.89')
        self.assertEqual(qx.amount, Decimal('32.89'))
        qx = X('1/7')
        self.assertEqual(qx.amount, Fraction(1, 7))
        self.assertRaises(QuantityError, X, 'x')
        self.assertRaises(QuantityError, Q, 5)
        self.assertRaises(QuantityError, Quantity, 5)
        for i in range(-34, 39, 11):
            f = Fraction(i, 7)
            d = Decimal(f, 20)
            for u in (t, kt):
                q = T(f, u)
                self.assertEqual(q.amount, d.quantize(T.quantum * u(t)))

    def testAlternateConstructor(self):
        q3x = 3 ^ x
        self.assertTrue(q3x.unit is x)
        self.assertEqual(q3x.amount, 3)
        self.assertRaises(TypeError, operator.xor, x, 3)

    def testQuantityFromString(self):
        d = Decimal('3.94')
        q = Quantity(' %s  %s   ' % (d, kx))
        self.assertEqual(q.amount, d)
        self.assertTrue(q.unit is kx)
        d = Decimal('5.9')
        q = Quantity(str(XpY(d)))
        self.assertEqual(q.amount, d)
        self.assertTrue(q.unit is xpy)
        d = Decimal('57.99999999999999999999999999999999999')
        q = Quantity(str(Z2(d)))
        self.assertEqual(q.amount, d)
        self.assertTrue(q.unit is Z2.refUnit)
        f = Fraction(1, 4)
        q = QpX('\t %s  %s' % (f, u2pkx))
        self.assertEqual(q.amount, f)
        self.assertTrue(q.unit is u2pkx)
        self.assertRaises(IncompatibleUnitsError, Q, '3 u1', y)
        self.assertRaises(QuantityError, Q, '5 x')
        self.assertRaises(QuantityError, Quantity, '5')
        self.assertRaises(QuantityError, Quantity, '5 ax')

    def testHash(self):
        q3x = X(3)
        self.assertEqual(hash(q3x), hash((3, x)))

    def testConversions(self):
        r = (1 ^ kx).convert(x)
        self.assertEqual((r.amount, r.unit), (1000, x))
        r = (1 ^ x).convert(kx)
        self.assertEqual((r.amount, r.unit), (Decimal('0.001'), kx))
        r = (1 ^ kx).convert(Mx)
        self.assertEqual((r.amount, r.unit), (Decimal('0.001'), Mx))
        q5kx = X(5, kx)
        r = q5kx.convert(x)
        self.assertEqual((r.amount, r.unit), (5000, x))
        q500x = X(500, x)
        r = q500x.convert(Mx)
        self.assertEqual((r.amount, r.unit), (Decimal('0.0005'), Mx))
        self.assertRaises(IncompatibleUnitsError, q500x.convert, y)
        self.assertRaises(UnitConversionError, (1 ^ u1).convert, u2)
        q7u2pkx = QpX(Decimal(7), u2pkx)
        self.assertRaises(UnitConversionError, q7u2pkx.convert, u1px)
        U.registerConverter(uConv1)
        # x u1 = (5 * x - 3) u2 = (25 * x + 1.5) u3
        qu1 = Q(Decimal('1.7'), u1)
        qu2 = qu1.convert(u2)
        self.assertEqual(qu2.amount, Decimal('5.5'))
        self.assertTrue(qu2.unit is u2)
        qu3 = qu1.convert(u3)
        self.assertTrue(qu1 == qu2 == qu3)
        q50u1 = Q(Decimal(50), u1)
        self.assertEqual(u2(q50u1), Decimal(247))
        self.assertEqual(u2(u1), Decimal(2))
        self.assertEqual(u1(u2), Decimal('0.8'))
        self.assertEqual(u3(q50u1), Decimal(1251.5))
        self.assertEqual(u3(u1), Decimal(26.5))
        self.assertEqual(u1(u3), Decimal('-0.02'))
        self.assertEqual(u3(u2), Decimal('21.5'))
        self.assertEqual(u2(u3), Decimal('-3.1'))
        self.assertEqual(u1px(q7u2pkx), Decimal('0.0035'))
        r = q7u2pkx.convert(u1px)
        self.assertEqual((r.amount, r.unit), (Decimal('0.0035'), u1px))
        # add additional converter
        U.registerConverter(uConv2)
        # x u1 = (5 * x - 1) u2
        qu1 = Q(Decimal(2), u1)
        qu2 = qu1.convert(u2)
        self.assertEqual(qu2.amount, Decimal(9))
        qu2 = qu1.convert(u2)
        self.assertEqual(qu1, qu2)
        # remove converter
        U.removeConverter(uConv2)
        # # x u1 = (5 * x - 3) u2
        qu2 = qu1.convert(u2)
        self.assertEqual(qu2.amount, Decimal(7))

    def testComparision(self):
        x3 = X(3)
        self.assertEqual(x3, X(3))
        kx5 = 5 ^ kx
        self.assertEqual(kx5, X(5, kx))
        self.assertEqual(kx5, X(5000))
        mx7 = 7 ^ Mx
        self.assertEqual(mx7, X(7, Mx))
        self.assertEqual(mx7, X(7000, kx))
        self.assertEqual(mx7, X(7000000))
        self.assertTrue(x3 < X('3.2'))
        self.assertFalse(x3 < X(3))
        self.assertTrue(x3 < X(1, kx))
        self.assertTrue(kx5 < X(2, Mx))
        self.assertNotEqual(x3, 'abc')

    def testMixedQuantityComparision(self):
        q3x = X(3)
        q3y = Y(3)
        self.assertTrue(q3x != q3y)
        self.assertRaises(IncompatibleUnitsError, operator.lt, q3x, q3y)
        self.assertRaises(IncompatibleUnitsError, operator.le, q3x, q3y)
        self.assertRaises(IncompatibleUnitsError, operator.gt, q3x, q3y)
        self.assertRaises(IncompatibleUnitsError, operator.ge, q3x, q3y)

    def testRounding1(self):
        a = Decimal('2.1')
        self.assertEqual(round(X(a)), X(round(a)))
        self.assertEqual(round(X(a, kx)), X(round(a), kx))
        a = Decimal('19.374')
        self.assertEqual(round(X(a), 2), X(round(a, 2)))
        self.assertEqual(round(X(a, kx), 2), X(round(a, 2), kx))
        a = Fraction(1, 7)
        r = round(X(a), 2)
        self.assertEqual(r.amount, Decimal(a, 2))
        self.assertTrue(isinstance(r.amount, Decimal))

    def testQuantization(self):
        qkx = X('17.8394 kx')
        self.assertEqual(qkx.quantize(x), X('17.839 kx'))
        self.assertEqual(qkx.quantize(0.5 ^ x), X('17.8395 kx'))
        self.assertEqual(qkx.quantize(5 ^ x), X('17.84 kx'))
        for i in range(-34, 39, 11):
            d = Decimal(i / 7, 3)
            for u in (x, kx):
                q = X(d, u)
                for rounding in rounding_modes:
                    self.assertEqual(q.quantize(x, rounding),
                                     d.quantize(u(x), rounding) ^ u)
        for i in range(-34, 39, 11):
            f = Fraction(i, 7)
            d = Decimal(f, 15)
            for u in (x, kx):
                q = X(f, u)
                for rounding in rounding_modes:
                    self.assertEqual(q.quantize(x, rounding),
                                     d.quantize(u(x), rounding) ^ u)
        for u in [t, kt]:
            q = T(10, u) / 3
            d = Decimal(Fraction(10, 3), 20)
            self.assertEqual(q.amount, d.quantize(T.quantum * u(t)))

    def testRounding2(self):
        qkx = X('17.8394 kx')
        self.assertEqual(round(qkx, x), X('17.839 kx'))
        self.assertEqual(round(qkx, 0.5 ^ x), X('17.8395 kx'))
        self.assertEqual(round(qkx, 5 ^ x), X('17.84 kx'))
        a = Fraction(1, 7)
        r = round(X(a, kx), X('0.01 x'))
        self.assertEqual(r.amount, Decimal(a, 5))

    def testAddition(self):
        self.assertEqual(X(10, Mx), X(9500, kx) + X(500000))
        self.assertRaises(IncompatibleUnitsError, operator.add, X(5), XpY(7))
        self.assertEqual(XpY(10), XpY(9.5) + XpY(0.5))

    def testSubtraction(self):
        self.assertEqual(X(9, Mx), X(9500, kx) - X(500000))
        self.assertRaises(IncompatibleUnitsError, operator.sub, X(5), XpY(7))
        self.assertEqual(XpY(9), XpY(9.5) - XpY(0.5))

    def testMultiplication(self):
        self.assertEqual(3 * Z(1), Z(1) * 3)
        self.assertEqual(3 * Z(1), Z(3))
        self.assertEqual(3 * Z(8), Z(24))
        self.assertRaises(UndefinedResultError, operator.mul, X(3), Z(8))
        self.assertEqual(Z2(20), Z(4) * Z(5))
        self.assertEqual(XtZ2pY(1200), (Z(4) * Z(5)) * XpY(2, x30py))
        self.assertEqual((1 ^ xpy) * (1 ^ ypx), 1)
        self.assertEqual(XpY(4) * YpX(3), 12)
        self.assertEqual(XpY(4, x30py) * YpX(3), 360)
        self.assertEqual(QpX(Decimal(10), u1px) * X(1, kx),
                         Q(Decimal(10000), u1))
        self.assertRaises(TypeError, operator.mul, Z2(3), 'a')
        self.assertRaises(TypeError, operator.mul, 'a', Z2(3))

    def testDivision(self):
        self.assertEqual(Z(6) / 2, Z(3))
        self.assertEqual(Z(24) / Z(8), 3)
        self.assertRaises(UndefinedResultError, operator.truediv, 3, Z(8))
        self.assertRaises(UndefinedResultError, operator.truediv, X(3), Z(8))
        self.assertEqual(15 / X(3), Xinv(5))
        self.assertEqual(Z2(20) / Z(4), Z(5))
        self.assertEqual(XpY(2, x30py) / XpY(5, xpy), 12)
        self.assertEqual(XtZ2pY(1200) / XpY(2, x30py), Z2(20))
        self.assertRaises(TypeError, operator.truediv, Z2(3), 'a')
        self.assertRaises(TypeError, operator.truediv, 'a', Z2(3))

    def testPower(self):
        self.assertEqual(3 * Z(1) ** 2, Z2(3))
        self.assertEqual(Z(3) ** 2, Z2(9))
        fz = Z.Unit('fz', 'fz', Z(Decimal('0.05')))
        self.assertEqual(Z(20, fz) ** 2, Z2(1))
        self.assertRaises(TypeError, operator.pow, Z2(3), 2.5)

    def testPickle(self):
        q = X(Decimal('3.94'), kx)
        r = loads(dumps(q))
        self.assertEqual(r, q)
        self.assertTrue(r.unit is q.unit)
        q = XtZ2pY(Fraction(1, 7))
        r = loads(dumps(q))
        self.assertEqual(r, q)
        self.assertTrue(r.unit is q.unit)

    def testStr(self):
        self.assertEqual(str(x), x.symbol)
        q = X(Decimal('3.94'), kx)
        self.assertEqual(str(q), "%s %s" % (str(q.amount), q.unit.symbol))
        q = XpY('5.9')
        self.assertEqual(str(q), "%s %s" % (str(q.amount), q.unit.symbol))
        q = Z2('57.99999999999999999999999999999999999')
        self.assertEqual(str(q), "%s %s" % (str(q.amount), q.unit.symbol))

    def testRepr(self):
        self.assertEqual(repr(x), "X.Unit(%s)" % repr(x.symbol))
        self.assertEqual(repr(kx), "X.Unit(%s)" % repr(kx.symbol))
        q = X(Decimal('3.94'), kx)
        self.assertEqual(repr(q),
                         "X(%s, %s)" % (repr(q.amount), repr(q.unit)))
        q = XpY('5.9')
        self.assertEqual(repr(q), "XpY(%s)" % repr(q.amount))

    def testFormat(self):
        q = Z2(Decimal('3.943'))
        self.assertEqual(format(q), '3.943 z\xb2')
        self.assertEqual(format(q, '{a:*>7.2f} {u:>3}'), '***3.94  z\xb2')
        self.assertEqual(format(q, 'abc'), 'abc')

    def testSum(self):
        ql = [X(27), X(100), X(2, kx), X(-7)]
        self.assertEqual(sum(ql), X(2120))
        self.assertEqual(sum(ql, X(0)), X(2120))
        self.assertEqual(sum(ql, X(-20)), X(2100))
        self.assertRaises(IncompatibleUnitsError, sum, ql, 5 ^ y)
        self.assertRaises(TypeError, sum, ql, 5)

    def testAllocate(self):
        set_rounding(ROUND_HALF_UP)
        T._quantum = Decimal('0.01')
        qty = Decimal(10) ^ T.refUnit
        # negative rounding error
        ratios = [3, 7, 5, 6, 81, 3, 7]
        self.assertEqual(qty.allocate(ratios, False),
                         ([T(Decimal('0.27')),
                           T(Decimal('0.63')),
                           T(Decimal('0.45')),
                           T(Decimal('0.54')),
                           T(Decimal('7.23')),
                           T(Decimal('0.27')),
                           T(Decimal('0.63'))],
                          T(Decimal('-0.02'))))
        self.assertEqual(qty.allocate(ratios),
                         ([T(Decimal('0.27')),
                           T(Decimal('0.62')),
                           T(Decimal('0.45')),
                           T(Decimal('0.54')),
                           T(Decimal('7.23')),
                           T(Decimal('0.27')),
                           T(Decimal('0.62'))],
                          T(0)))
        # positive rounding error
        ratios = [3, 7, 5, 6, 87, 3, 7]
        self.assertEqual(qty.allocate(ratios, False),
                         ([T(Decimal('0.25')),
                           T(Decimal('0.59')),
                           T(Decimal('0.42')),
                           T(Decimal('0.51')),
                           T(Decimal('7.37')),
                           T(Decimal('0.25')),
                           T(Decimal('0.59'))],
                          T(Decimal('0.02'))))
        self.assertEqual(qty.allocate(ratios),
                         ([T(Decimal('0.26')),
                           T(Decimal('0.59')),
                           T(Decimal('0.42')),
                           T(Decimal('0.51')),
                           T(Decimal('7.37')),
                           T(Decimal('0.26')),
                           T(Decimal('0.59'))],
                          T(0)))
        # quantities as ratios
        ratios = [3 ^ x, 7 ^ x, 5 ^ x, 6 ^ x, Decimal('0.081') ^ kx, 3 ^ x,
                  7 ^ x]
        self.assertEqual(qty.allocate(ratios, False),
                         ([T(Decimal('0.27')),
                           T(Decimal('0.63')),
                           T(Decimal('0.45')),
                           T(Decimal('0.54')),
                           T(Decimal('7.23')),
                           T(Decimal('0.27')),
                           T(Decimal('0.63'))],
                          T(Decimal('-0.02'))))
        self.assertEqual(qty.allocate(ratios),
                         ([T(Decimal('0.27')),
                           T(Decimal('0.62')),
                           T(Decimal('0.45')),
                           T(Decimal('0.54')),
                           T(Decimal('7.23')),
                           T(Decimal('0.27')),
                           T(Decimal('0.62'))],
                          T(0)))
        # inconsistent ratios
        self.assertRaises(TypeError, qty.allocate, [3 ^ x, 6 ^ x, 2, 1 ^ x])
        self.assertRaises(IncompatibleUnitsError, qty.allocate, [3 ^ x, 6 ^ y,
                                                                 2 ^ kx])


if __name__ == '__main__':
    unittest.main()
