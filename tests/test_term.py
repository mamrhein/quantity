#!usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# Name:        test_term
# Purpose:     Test driver for module term
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) Michael Amrhein
# ****************************************************************************
# $Source$
# $Revision$


import operator
import unittest
from numbers import Real

from decimalfp import Decimal

from quantity.term import (NonNumTermElem, Term, _div_sign, _mulSign,
                           _powerChars)


# parse string
import re
_pattern = r"""(?P<num>\d*)(?P<base>.*)"""
_parseString = re.compile(_pattern, re.VERBOSE).match
del re, _pattern


class XElem(str, NonNumTermElem):

    def is_base_elem(self):
        """True if self is a base element; i.e. can not be decomposed."""
        num, base = self._split()
        return num == 1

    def _split(self):
        num, base = _parseString(self).groups()
        if num:
            return Decimal(num), XElem(base)
        else:
            return 1, XElem(base)

    def __div__(self, other: 'XElem'):
        snum, sbase = _parseString(self).groups()
        onum, obase = _parseString(other).groups()
        if sbase == obase:
            return snum / onum
        return self.__class__(f"{snum / onum}{sbase}/{obase}")

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"


class XTerm(Term):

    @staticmethod
    def normalize_elem(elem):
        """Return the decomposition of elem (list of items)."""
        num, base = elem._split()
        if num is None:
            return [(elem, 1)]
        else:
            return [(num, 1), (base, 1)]

    @staticmethod
    def norm_sort_key(elem):
        """Return sort key for elem; used for normalized form of term.

        The value returned should be either an int > 0 or a string."""
        if isinstance(elem, Real):
            return ''
        num, base = elem._split()
        return str(base)

    @staticmethod
    def convert(elem, into):
        """Return factor f so that f * Term([(into, 1)]) == Term([(elem, 1)]).

        Raises TypeError if conversion is not possible."""
        numElem, baseElem = elem._split()
        numInto, baseInto = into._split()
        if baseElem == baseInto:
            return (numElem or 1) / (numInto or 1)
        raise NotImplementedError


class TermTest(unittest.TestCase):

    def testConstructor(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t = Term([(x, 1)])
        self.assertEqual(t._items, ((x, 1),))
        t = Term([(y, 2), (x, 1)])
        self.assertEqual(t._items, ((y, 2), (x, 1)))
        # t = Term([(y, 2), (x, 1)], keep_item_order=False)
        # self.assertEqual(t._items, ((x, 1), (y, 2)))
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
        xt = XTerm(((XElem('100x'), 1), (XElem('10x'), -1)))
        self.assertEqual(xt._items, ((10, 1),))
        xt = XTerm(((XElem('10x'), 1), (x, 1)))
        self.assertEqual(xt._items, ((Decimal('0.1'), 1), ('10x', 2)))
        xt = XTerm(((XElem('10x'), 1), (XElem('10x'), 1)))
        self.assertEqual(xt._items, (('10x', 2),))
        xt = XTerm(((x, 1), (XElem('10x'), 1)))
        self.assertEqual(xt._items, ((10.0, 1), (x, 2)))
        xt = XTerm(((x, 1), (XElem('10x'), 1), (XElem('10x'), 1)))
        self.assertEqual(xt._items, ((100, 1), (x, 3)))

    def testNormalization(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t = Term([(x, 1), (y, 2)])
        self.assertTrue(t.is_normalized)
        xt = XTerm([(x, 1)])
        self.assertTrue(xt.is_normalized)
        dxt = XTerm([(XElem('10x'), 1)])
        self.assertTrue(not dxt.is_normalized)
        self.assertEqual(dxt.normalized(), XTerm(((10, 1), (x, 1))))
        dxMzpky = XTerm([(XElem('10x'), 1),
                         (XElem('1000000z'), 1),
                         (XElem('1000y'), -1)])
        self.assertTrue(not dxMzpky.is_normalized)
        self.assertEqual(dxMzpky.normalized(),
                         XTerm(((10000, 1), (x, 1), (y, -1), (z, 1))))

    def testHash(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t = Term([(y, 2), (x, 1), (z, 0), (y, -1)])
        self.assertEqual(hash(t), hash(t.normalized()))

    def testComparision(self):
        x, y = XElem('x'), XElem('y')
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, 2), (y, 1)])
        t3 = Term([(y, 1), (x, 2)])
        self.assertTrue(t1 != t2)
        self.assertTrue(t1 != t3)
        self.assertTrue(t2 == t3)
        xt = XTerm([(x, 1)])
        dxt = XTerm([(XElem('10x'), 1)])
        self.assertTrue(xt != dxt)
        self.assertEqual(XTerm(((10, 1), (x, 1))), dxt)

    def testMultiplication(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, -2), (z, 1), (y, 1)])
        self.assertEqual(t1 * t2, Term(((x, -1), (y, 3), (z, 1))))
        self.assertEqual(t1 * 5, Term(((5, 1), (x, 1), (y, 2))))
        self.assertEqual(t1 * 5, 5 * t1)
        self.assertRaises(TypeError, operator.mul, 'a', t1)
        self.assertRaises(TypeError, operator.mul, t1, 'a')
        xt = XTerm([(x, 1)])
        self.assertEqual(5 * xt, xt * 5)
        dxt = XTerm([(XElem('10x'), 1)])
        self.assertEqual(10 * xt, dxt)

    def testDivision(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
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
        dxt = XTerm([(XElem('10x'), 1)])
        self.assertEqual(xt, dxt / Decimal(10))

    def testPower(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t = Term([(y, 2), (x, 1), (z, -3)])
        self.assertEqual(t ** 5, Term(((x, 5), (y, 10), (z, -15))))

    def testStr(self):
        x, y, z = XElem('x'), XElem('y'), XElem('z')
        t1 = Term([(y, 1), (x, 2)])
        self.assertEqual(str(t1), 'y%sx%s' % (_mulSign, _powerChars[2]))
        t2 = Term([(y, 2), (x, -1), (z, 3)])
        self.assertEqual(str(t2), 'y%s%sz%s%sx' %
                         (_powerChars[2], _mulSign, _powerChars[3], _div_sign))

    def testRepr(self):
        x, y = XElem('x'), XElem('y')
        t1 = Term([(y, 2), (x, 1)])
        self.assertEqual(t1, eval(repr(t1)))


if __name__ == '__main__':
    unittest.main()
