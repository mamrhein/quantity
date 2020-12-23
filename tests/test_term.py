#!usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Test driver for module term"""


# Standard library imports
import operator
import unittest
from numbers import Real
from typing import Tuple

# Third-party imports

from decimalfp import Decimal

# Local imports
from quantity.term import (NonNumTermElem, Term, _div_sign, _mulSign,
                           _powerChars)


# parse string
import re
_pattern = r"""(?P<num>\d*)(?P<base>.*)"""
_parseString = re.compile(_pattern, re.VERBOSE).match
del re, _pattern


class TElem(str, NonNumTermElem):

    def _split(self) -> Tuple[Real, 'TElem']:
        num, base = _parseString(self).groups()
        if num:
            return Decimal(num), TElem(base)
        else:
            return 1, TElem(base)

    def is_base_elem(self) -> bool:
        """True if self is a base element; i.e. can not be decomposed."""
        num, base = self._split()
        return num == 1

    @property
    def normalized_definition(self) -> Term:
        num, base = self._split()
        return Term([(num, 1), (base, 1)])

    def norm_sort_key(self) -> int:
        num, base = self._split()
        return ord(base[0])

    def _get_factor(self, other: 'TElem') -> Real:
        snum, sbase = self._split()
        onum, obase = other._split()
        if sbase == obase:
            return snum / onum
        raise TypeError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"


class TermTest(unittest.TestCase):

    def testConstructor(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t = Term([(x, 1)])
        self.assertEqual(t._items, ((x, 1),))
        t = Term([(y, 2), (x, 1)])
        self.assertEqual(t._items, ((y, 2), (x, 1)))
        t = Term([(x, 2), (x, 1)])
        self.assertEqual(t._items, ((x, 3),))
        t = Term([(y, 2), (x, 1), (y, 1), (z, -1), (y, 1),
                  (x, -1)])
        self.assertEqual(t._items, ((y, 4), (z, -1)))
        t = Term(((y, 1), (x, 1), (x, 1), (5, 1), (y, -1)))
        self.assertEqual(t._items, ((5, 1), (x, 2)))
        t = Term(((y, 0), (1, 1)))
        self.assertEqual(t._items, ())
        xt = Term([(x, 1)])
        self.assertEqual(xt._items, ((x, 1),))
        xt = Term(((TElem('100x'), 1), (TElem('10x'), -1)))
        self.assertEqual(xt._items, ((10, 1),))
        xt = Term(((TElem('10x'), 1), (x, 1)))
        self.assertEqual(xt._items, ((Decimal('0.1'), 1), ('10x', 2)))
        xt = Term(((TElem('10x'), 1), (TElem('10x'), 1)))
        self.assertEqual(xt._items, (('10x', 2),))
        xt = Term(((x, 1), (TElem('10x'), 1)))
        self.assertEqual(xt._items, ((10.0, 1), (x, 2)))
        xt = Term(((x, 1), (TElem('10x'), 1), (TElem('10x'), 1)))
        self.assertEqual(xt._items, ((100, 1), (x, 3)))
        xt = Term(((5, 1), (TElem('10x'), 1), (2, 2)))
        self.assertEqual(xt._items, ((20, 1), (TElem('10x'), 1)))
        xt = Term(((25, 1), (5, -2)))
        self.assertEqual(xt._items, ())
        xt = Term(((10, 3), (5, -2)))
        self.assertEqual(xt._items, ((40, 1),))

    def testNormalization(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t = Term([(x, 1), (y, 2)])
        self.assertTrue(t.is_normalized)
        xt = Term([(x, 1)])
        self.assertTrue(xt.is_normalized)
        dxt = Term([(TElem('10x'), 1)])
        self.assertTrue(not dxt.is_normalized)
        self.assertEqual(dxt.normalized(), Term(((10, 1), (x, 1))))
        dxMzpky = Term([(TElem('10x'), 1),
                         (TElem('1000000z'), 1),
                         (TElem('1000y'), -1)])
        self.assertTrue(not dxMzpky.is_normalized)
        self.assertEqual(dxMzpky.normalized(),
                         Term(((10000, 1), (x, 1), (y, -1), (z, 1))))

    def testHash(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t = Term([(y, 2), (x, 1), (z, 0), (y, -1)])
        self.assertEqual(hash(t), hash(t.normalized()))

    def testComparision(self):
        x, y = TElem('x'), TElem('y')
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, 2), (y, 1)])
        t3 = Term([(y, 1), (x, 2)])
        self.assertTrue(t1 != t2)
        self.assertTrue(t1 != t3)
        self.assertTrue(t2 == t3)
        xt = Term([(x, 1)])
        dxt = Term([(TElem('10x'), 1)])
        self.assertTrue(xt != dxt)
        self.assertEqual(Term(((10, 1), (x, 1))), dxt)

    def testMultiplication(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, -2), (z, 1), (y, 1)])
        self.assertEqual(t1 * t2, Term(((x, -1), (y, 3), (z, 1))))
        self.assertEqual(t1 * 5, Term(((5, 1), (x, 1), (y, 2))))
        self.assertEqual(t1 * 5, 5 * t1)
        self.assertRaises(TypeError, operator.mul, 'a', t1)
        self.assertRaises(TypeError, operator.mul, t1, 'a')
        xt = Term([(x, 1)])
        self.assertEqual(5 * xt, xt * 5)
        dxt = Term([(TElem('10x'), 1)])
        self.assertEqual(10 * xt, dxt)

    def testDivision(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t1 = Term([(y, 2), (x, 1)])
        t2 = Term([(x, -2), (z, 1), (y, 1)])
        self.assertEqual(t1 / t2, Term(((x, 3), (y, 1), (z, -1))))
        self.assertEqual(t1 / t2, t1 * t2.reciprocal())
        self.assertEqual(t1 / 0.5, Term(((2, 1), (x, 1), (y, 2))))
        self.assertEqual(5 / t1, Term(((5, 1), (x, -1), (y, -2))))
        self.assertRaises(TypeError, operator.truediv, 'a', t1)
        self.assertRaises(TypeError, operator.truediv, t1, 'a')
        xt = Term([(x, 1)])
        self.assertEqual(xt / xt, Term())
        dxt = Term([(TElem('10x'), 1)])
        self.assertEqual(xt, dxt / Decimal(10))

    def testPower(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t = Term([(y, 2), (x, 1), (z, -3)])
        self.assertEqual(t ** 5, Term(((x, 5), (y, 10), (z, -15))))

    def testStr(self):
        x, y, z = TElem('x'), TElem('y'), TElem('z')
        t1 = Term([(y, 1), (x, 2)])
        self.assertEqual(str(t1), 'y%sx%s' % (_mulSign, _powerChars[2]))
        t2 = Term([(y, 2), (x, -1), (z, 3)])
        self.assertEqual(str(t2), 'y%s%sz%s%sx' %
                         (_powerChars[2], _mulSign, _powerChars[3], _div_sign))

    def testRepr(self):
        x, y = TElem('x'), TElem('y')
        t1 = Term([(y, 2), (x, 1)])
        self.assertEqual(t1, eval(repr(t1)))


if __name__ == '__main__':
    unittest.main()
