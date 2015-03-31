#!usr/bin/env python
# -*- coding: utf-8 -*-
##****************************************************************************
## Name:        test_term
## Purpose:     Test driver for module term
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
from quantity.term import _mulSign, _powerChars, Term

# unicode handling Python 2 / Python 3
try:
    str = unicode
except NameError:
    pass

# parse string
import re
_pattern = r"""(?P<num>\d*)(?P<base>.*)"""
_parseString = re.compile(_pattern, re.VERBOSE).match
del re, _pattern


class XTerm(Term):

    @staticmethod
    def _splitElem(elem):
        num, base = _parseString(elem).groups()
        if num:
            return int(num), base
        else:
            return None, base

    @staticmethod
    def isBaseElem(elem):
        """True if elem is a base element; i.e. can not be decomposed."""
        num, base = XTerm._splitElem(elem)
        return num is None

    @staticmethod
    def normalizeElem(elem):
        """Return the decomposition of elem (list of items)."""
        num, base = XTerm._splitElem(elem)
        if num is None:
            return [(elem, 1)]
        else:
            return [(num, 1), (base, 1)]

    @staticmethod
    def normSortKey(elem):
        """Return sort key for elem; used for normalized form of term.

        The value returned should be either an int > 0 or a string."""
        if Term.isNumerical(elem):
            return ''
        num, base = XTerm._splitElem(elem)
        return str(base)

    @staticmethod
    def convert(elem, into):
        """Return factor f so that f * Term([(into, 1)]) == Term([(elem, 1)]).

        Raises TypeError if conversion is not possible."""
        numElem, baseElem = XTerm._splitElem(elem)
        numInto, baseInto = XTerm._splitElem(into)
        if baseElem == baseInto:
            return (numElem or 1) / (numInto or 1)
        raise NotImplementedError


class TermTest(unittest.TestCase):

    def testConstructor(self):
        x, y, z = 'x', 'y', 'z'
        t = Term([(x, 1)])
        self.assertEqual(t._items, ((x, 1),))
        t = Term([(y, 2), (x, 1)])
        self.assertEqual(t._items, ((x, 1), (y, 2)))
        t = Term([(x, 2), (x, 1)])
        self.assertEqual(t._items, ((x, 3),))
        t = Term([(y, 2), (x, 1), (y, 1), (z, -1), (y, 1),
                  (x, -1)])
        self.assertEqual(t._items, ((y, 4), (z, -1)))
        t = Term(((y, 1), (x, 1), (x, 1), (5, 1), (y, -1)))
        self.assertEqual(t._items, ((5, 1), (x, 2)))
        t = Term(((y, 0), (1, 1)))
        self.assertEqual(t._items, ())
        xt = XTerm([(x, 1)])
        self.assertEqual(xt._items, ((x, 1),))
        xt = XTerm((('100' + x, 1), ('10' + x, -1)))
        self.assertEqual(xt._items, ((10.0, 1),))
        xt = XTerm((('10' + x, 1), (x, 1)))
        self.assertEqual(xt._items, ((0.1, 1), ('10x', 2)))
        xt = XTerm((('10' + x, 1), ('10' + x, 1)))
        self.assertEqual(xt._items, (('10x', 2),))
        xt = XTerm(((x, 1), ('10' + x, 1)))
        self.assertEqual(xt._items, ((10.0, 1), (x, 2)))
        xt = XTerm(((x, 1), ('10' + x, 1), ('10' + x, 1)))
        self.assertEqual(xt._items, ((100.0, 1), (x, 3)))

    def testNormalization(self):
        x, y, z = 'x', 'y', 'z'
        t = Term([(y, 2), (x, 1)])
        self.assertTrue(t.isNormalized)
        xt = XTerm([(x, 1)])
        self.assertTrue(xt.isNormalized)
        dxt = XTerm([('10' + x, 1)])
        self.assertTrue(not dxt.isNormalized)
        self.assertEqual(dxt.normalized(), XTerm(((10, 1), (x, 1))))
        dxMzpky = XTerm([('10' + x, 1), ('1000000' + z, 1), ('1000' + y, -1)])
        self.assertTrue(not dxMzpky.isNormalized)
        self.assertEqual(dxMzpky.normalized(),
                         XTerm(((10000, 1), (x, 1), (y, -1), (z, 1))))

    def testHash(self):
        t = Term([('y', 2), ('x', 1)])
        self.assertEqual(hash(t), hash(t._items))

    def testComparision(self):
        x, y = 'x', 'y'
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, 2), (y, 1)])
        t3 = Term([(y, 1), (x, 2)])
        self.assertTrue(t1 != t2)
        self.assertTrue(t1 != t3)
        self.assertTrue(t2 == t3)
        xt = XTerm([(x, 1)])
        dxt = XTerm([('10' + x, 1)])
        self.assertTrue(xt != dxt)

    def testMultiplication(self):
        x, y, z = 'x', 'y', 'z'
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, -2), (z, 1), (y, 1)])
        self.assertEqual(t1 * t2, Term(((x, -1), (y, 3), (z, 1))))
        self.assertEqual(t1 * 5, Term(((5, 1), (x, 1), (y, 2))))
        self.assertEqual(t1 * 5, 5 * t1)
        self.assertRaises(TypeError, operator.mul, 'a', t1)
        self.assertRaises(TypeError, operator.mul, t1, 'a')
        xt = XTerm([(x, 1)])
        self.assertEqual(5 * xt, xt * 5)
        dxt = XTerm([('10' + x, 1)])
        self.assertEqual(10 * xt, dxt)

    def testDivision(self):
        x, y, z = 'x', 'y', 'z'
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, -2), (z, 1), (y, 1)])
        self.assertEqual(t1 / t2, Term(((x, 3), (y, 1), (z, -1))))
        self.assertEqual(t1 / t2, t1 * t2.reciprocal())
        self.assertEqual(t1 / 0.5, Term(((2, 1), (x, 1), (y, 2))))
        self.assertEqual(5 / t1, Term(((5, 1), (x, -1), (y, -2))))
        self.assertRaises(TypeError, operator.truediv, 'a', t1)
        self.assertRaises(TypeError, operator.truediv, t1, 'a')
        xt = XTerm([(x, 1)])
        self.assertEqual(xt / xt, XTerm())
        dxt = XTerm([('10' + x, 1)])
        self.assertEqual(xt, dxt / 10)

    def testPower(self):
        x, y, z = 'x', 'y', 'z'
        t = Term([(y, 2), (x, 1), (z, -3)])
        self.assertEqual(t ** 5, Term(((x, 5), (y, 10), (z, -15))))

    def testStr(self):
        t1 = Term([('y', 2), ('x', 1)])
        self.assertEqual(str(t1), 'x%sy%s' % (_mulSign, _powerChars[2]))

    def testRepr(self):
        t1 = Term([('y', 2), ('x', 1)])
        self.assertEqual(t1, eval(repr(t1)))


if __name__ == '__main__':
    unittest.main()
