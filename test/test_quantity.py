#!usr/bin/env python
# -*- coding: utf-8 -*-
##****************************************************************************
## Name:        test_quantity
## Purpose:     Test driver for module quantity
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) Michael Amrhein
##****************************************************************************
## $Source$
## $Revision$


from __future__ import absolute_import, division, unicode_literals
import unittest
import operator
from pickle import dumps, loads
from decimal import Decimal, InvalidOperation
from quantity import (Quantity, Unit, IncompatibleUnitsError,
                      UndefinedResultError, TableConverter)
from quantity.quantity import MetaQuantity, _registry
from quantity.term import _mulSign, _SUPERSCRIPT_CHARS

# Python 2 / Python 3: determine version and support __round__ in 2.x
try:
    int.__round__
except AttributeError:
    PY_VERSION = 2
    import __builtin__
    py2_round = __builtin__.round

    def round(number, ndigits=0):
        try:
            return number.__round__(ndigits)
        except AttributeError:
            return py2_round(number, ndigits)
else:
    PY_VERSION = 3


__version__ = 0, 0, 1


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


defYpX = Y / X
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

# u1 = 5 u2 = 25 u3
uConvTable = [('u1', 'u2', Decimal(5)),
              ('u2', 'u1', Decimal('0.2')),
              ('u1', 'u3', Decimal(25)),
              ('u2', 'u3', Decimal(5))]
uConv = TableConverter(uConvTable)


defQpX = Q / X
class QpX(Quantity):
    defineAs = defQpX

for qu in U.registeredUnits():
    for xu in X.Unit.registeredUnits():
        upx = QpX.Unit("%s/%s" % (qu.symbol, xu.symbol), defineAs=qu/xu)

u1px = QpX.Unit('u1/x')
u2pkx = QpX.Unit('u2/kx')


class Test1_MetaQuantity(unittest.TestCase):

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
        self.assertRaises((ValueError, InvalidOperation), X, 'a')
        self.assertRaises(TypeError, X, 5, y)
        self.assertTrue(Q.refUnit is None)

    def testQuantityReg(self):
        self.assertTrue(_registry.getQuantityCls(X.clsDefinition) is X)
        self.assertRaises(ValueError, MetaQuantity, str('X_Y'), (Quantity,),
                          {str('defineAs'): defXpY})

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


class Test2_Unit(unittest.TestCase):

    def testConstructor(self):
        self.assertEqual(u1.symbol, 'u1')
        self.assertEqual(u1.name, 'Q unit 1')
        self.assertEqual(u2.symbol, u2.name)
        self.assertTrue(u1._definition is None)
        self.assertTrue(U('u3') is u3)
        self.assertRaises(ValueError, X.Unit, '', '', X(10))
        self.assertEqual(kx.name, 'kilox')
        self.assertEqual(kx.symbol, 'kx')
        self.assertEqual(kx.definition.amount, 1000)
        self.assertEqual(kx.definition.unitTerm, x.definition)
        self.assertEqual(Mx.definition.amount, 1000)
        self.assertEqual(list(Mx.definition.unitTerm), [(kx, 1)])
        sypkx = YpX.Unit('', 'sypkx', sy / kx)
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
        self.assertRaises(IncompatibleUnitsError, u1, u2)

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
        q3x = X(3)
        self.assertTrue(q3x.unit is x)
        self.assertEqual(q3x.amount, 3)
        q3x = X('3.2')
        self.assertTrue(q3x.unit is x)
        self.assertEqual(q3x.amount, Decimal('3.2'))

    def testAlternateConstructor(self):
        q3x = 3 ^ x
        self.assertTrue(q3x.unit is x)
        self.assertEqual(q3x.amount, 3)
        self.assertRaises(TypeError, operator.xor, x, 3)

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
        self.assertRaises(IncompatibleUnitsError, (1 ^ u1).convert, u2)
        q7u2pkx = QpX(Decimal(7), u2pkx)
        self.assertRaises(IncompatibleUnitsError, q7u2pkx.convert, u1px)
        U.registerConverter(uConv)
        q50 = Q(Decimal(50), u1)
        self.assertEqual(u2(q50), Decimal(250))
        self.assertEqual(u2(u1), Decimal(5))
        self.assertEqual(u1(u2), Decimal('0.2'))
        self.assertEqual(u3(q50), Decimal(1250))
        self.assertEqual(u3(u1), Decimal(25))
        self.assertEqual(u1(u3), Decimal('0.04'))
        self.assertEqual(u3(u2), Decimal(5))
        self.assertEqual(u2(u3), Decimal('0.2'))
        self.assertEqual(u1px(q7u2pkx), Decimal('0.0014'))
        r = q7u2pkx.convert(u1px)
        self.assertEqual((r.amount, r.unit), (Decimal('0.0014'), u1px))

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

    def testRounding(self):
        a = Decimal('2.1')
        self.assertEqual(round(X(a)), X(round(a)))
        self.assertEqual(round(X(a, kx)), X(round(a), kx))
        a = Decimal('2.247')
        self.assertEqual(round(X(a), 2), X(round(a, 2)))
        self.assertEqual(round(X(a, kx), 2), X(round(a, 2), kx))

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

    def testStr(self):
        self.assertEqual(str(x), x.symbol)
        q = X(Decimal('3.94'), kx)
        self.assertEqual(str(q), "%s %s" % (str(q.amount), q.unit.symbol))
        q = XpY('5.9')
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

if __name__ == '__main__':
    unittest.main()