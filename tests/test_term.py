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
from numbers import Real
from typing import Any, Tuple

# Third-party imports
import pytest
from decimalfp import Decimal

# Local imports
from quantity.term import (Term, _div_sign, _mulSign,
                           _powerChars)


# parse string
import re
_pattern = r"""(?P<num>\d*)(?P<base>.*)"""
_parseString = re.compile(_pattern, re.VERBOSE).match
del re, _pattern


class TElem(str):

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

    def _get_factor(self, other: Any) -> Real:
        if isinstance(other, TElem):
            snum, sbase = self._split()
            onum, obase = other._split()
            if sbase == obase:
                return snum / onum
        raise TypeError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self}')"


x, y, z = TElem('x'), TElem('y'), TElem('z')


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ('term', 'items'),
    (
        (Term([(x, 1)]), ((x, 1),)),
        (Term([(x, 1)]), ((x, 1),)),
        (Term([(y, 2), (x, 1)]), ((y, 2), (x, 1))),
        (Term([(x, 2), (x, 1)]), ((x, 3),)),
        (Term([(y, 2), (x, 1), (y, 1), (z, -1), (y, 1), (x, -1)]), ((y, 4), (z, -1))),
        (Term(((y, 1), (x, 1), (x, 1), (5, 1), (y, -1))), ((5, 1), (x, 2))),
        (Term(((y, 0), (1, 1))), ()),
        (Term([(x, 1)]), ((x, 1),)),
        (Term(((TElem('100x'), 1), (TElem('10x'), -1))), ((10, 1),)),
        (Term(((TElem('10x'), 1), (x, 1))), ((Decimal('0.1'), 1), ('10x', 2))),
        (Term(((TElem('10x'), 1), (TElem('10x'), 1))), (('10x', 2),)),
        (Term(((x, 1), (TElem('10x'), 1))), ((10.0, 1), (x, 2))),
        (Term(((x, 1), (TElem('10x'), 1), (TElem('10x'), 1))), ((100, 1), (x, 3))),
        (Term(((5, 1), (TElem('10x'), 1), (2, 2))), ((20, 1), (TElem('10x'), 1))),
        (Term(((25, 1), (Decimal(5), -2))), ()),
        (Term(((10, 3), (Decimal(5), -2))), ((40, 1),)),
    )
)
def test_constructor(term, items):
    assert term._items == items


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("term", "normalized"),
    (
        (Term([(x, 1), (y, 2)]), None),
        (Term([(x, 1)]), None),
        (Term([(TElem('10x'), 1)]), Term(((10, 1), (x, 1)))),
        (Term([(Decimal(10), -1), (TElem('10x'), 1)]), Term([(x, 1)])),
        (Term([(TElem('10x'), 1), (TElem('1000000z'), 1),
               (TElem('1000y'), -1)]),
         Term(((10000, 1), (x, 1), (y, -1), (z, 1)))),
    ),
)
def test_normalization(term, normalized):
    if normalized is None:
        assert term.is_normalized
    else:
        assert not term.is_normalized
        assert term.normalized() == normalized


# noinspection PyMissingTypeHints
def test_hash():
    t = Term([(y, 2), (x, 1), (z, 0), (y, -1)])
    assert hash(t) == hash(t.normalized())


# noinspection PyMissingTypeHints
def test_comparision():
    t1 = Term([(y, 2), (x, 1)])
    t2 = Term([(x, 2), (y, 1)])
    t3 = Term([(y, 1), (x, 2)])
    assert t1 != t2
    assert t1 != t3
    assert t2 == t3
    xt = Term([(x, 1)])
    dxt = Term([(TElem('10x'), 1)])
    assert xt != dxt
    assert Term(((10, 1), (x, 1))) == dxt
    assert Term(((Decimal(10), -1), (TElem('10x'), 1))) == xt


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("t1", "t2", "res"),
    (
        (Term([(y, 2), (x, 1)]), Term([(x, -2), (z, 1), (y, 1)]),
         Term(((x, -1), (y, 3), (z, 1)))),
        (Term([(y, 2), (x, 1)]), 5, Term(((5, 1), (x, 1), (y, 2)))),
        (Term([(x, 1)]), 3, Term(((3, 1), (x, 1)))),
        (10, Term([(x, 1)]), Term([(TElem('10x'), 1)])),
    )
)
def test_multiplication(t1, t2, res):
    assert res == t1 * t2
    assert res == t2 * t1


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("t1", "t2", "res"),
    (
        (Term([(y, 2), (x, 1)]), Term([(x, -2), (z, 1), (y, 1)]),
         Term(((x, 3), (y, 1), (z, -1)))),
        (Term([(y, 2), (x, 1)]), 0.5, Term(((2, 1), (x, 1), (y, 2)))),
        (5, Term([(x, 1)]), Term(((5, 1), (x, -1)))),
        (Term([(x, 1)]), Term([(x, 1)]), Term()),
        (Term([(TElem('10x'), 1)]), Decimal(10), Term([(x, 1)])),
    )
)
def test_division(t1, t2, res):
    assert res == t1 / t2
    if isinstance(t2, Term):
        assert res == t1 * t2.reciprocal()


# noinspection PyMissingTypeHints
def test_mul_div_raises():
    t = Term([(x, 1)])
    with pytest.raises(TypeError):
        t * 'a'
    with pytest.raises(TypeError):
        'a' * t
    with pytest.raises(TypeError):
        t / 'a'
    with pytest.raises(TypeError):
        'a' / t


# noinspection PyMissingTypeHints
def test_power():
    t = Term([(y, 2), (x, 1), (z, -3)])
    assert t ** 5 == Term(((x, 5), (y, 10), (z, -15)))


# noinspection PyMissingTypeHints
def test_str():
    t1 = Term([(y, 1), (x, 2)])
    assert str(t1) == 'y%sx%s' % (_mulSign, _powerChars[2])
    t2 = Term([(y, 2), (x, -1), (z, 3)])
    assert str(t2) == 'y%s%sz%s%sx' % (_powerChars[2], _mulSign,
                                       _powerChars[3], _div_sign)


# noinspection PyMissingTypeHints
def test_repr():
    t1 = Term([(y, 2), (x, 1)])
    assert t1, eval(repr(t1))
