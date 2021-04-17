# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Test driver for module term"""

import re
from fractions import Fraction
from numbers import Rational
from typing import Any, Optional, Sequence, Tuple, Union

import pytest
from decimalfp import Decimal

from quantity.term import Term, _DIV_SIGN, _MUL_SIGN, _POWER_CHARS

_pattern = r"""(?P<num>\d*)(?P<base>.*)"""
_parse_string = re.compile(_pattern, re.VERBOSE).match
del re, _pattern


class TElem(str):

    def _split(self) -> Tuple[Decimal, 'TElem']:
        match = _parse_string(self)
        if match:
            num, base = match.groups()
            if num:
                return Decimal(num), TElem(base)
        return Decimal(1), self

    def is_base_elem(self) -> bool:
        """Return True if self is a base element."""
        num, base = self._split()
        return num == 1

    @property
    def definition(self) -> Term['TElem']:
        return TElemTerm([(self, 1)])

    @property
    def normalized_definition(self) -> Term['TElem']:
        num, base = self._split()
        if num == 1:
            return TElemTerm([(self, 1)])
        return TElemTerm([(num, 1), (base, 1)])

    def norm_sort_key(self) -> int:
        num, base = self._split()
        return ord(base[0])

    def _get_factor(self, other: Any) -> Rational:
        if isinstance(other, TElem):
            snum, sbase = self._split()
            onum, obase = other._split()
            if sbase == obase:
                return snum / onum
        raise TypeError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self}')"


x, y, z = TElem('x'), TElem('y'), TElem('z')

TElemTerm = Term[TElem]
TItemSeq = Sequence[Tuple[Union[TElem, Rational], int]]


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ('term_params', 'items'),
    (
        ([(x, 1)], ((x, 1),)),
        ([(x, 1)], ((x, 1),)),
        ([(y, 2), (x, 1)], ((y, 2), (x, 1))),
        ([(x, 2), (x, 1)], ((x, 3),)),
        ([(y, 2), (x, 1), (y, 1), (z, -1), (y, 1), (x, -1)],
         ((y, 4), (z, -1))),
        (((y, 1), (x, 1), (x, 1), (5, 1), (y, -1)), ((5, 1), (x, 2))),
        (((y, 0), (1, 1)), ()),
        ([(x, 1)], ((x, 1),)),
        (((TElem('100x'), 1), (TElem('10x'), -1)), ((10, 1),)),
        (((TElem('10x'), 1), (x, 1)), ((Decimal('0.1'), 1), ('10x', 2))),
        (((TElem('10x'), 1), (TElem('10x'), 1)), (('10x', 2),)),
        (((x, 1), (TElem('10x'), 1)), ((10.0, 1), (x, 2))),
        (((x, 1), (TElem('10x'), 1), (TElem('10x'), 1)), ((100, 1), (x, 3))),
        (((5, 1), (TElem('10x'), 1), (2, 2)), ((20, 1), (TElem('10x'), 1))),
        (((25, 1), (Decimal(5), -2)), ()),
        (((10, 3), (Decimal(5), -2)), ((40, 1),)),
        )
    )
def test_constructor(term_params: TItemSeq, items: TItemSeq) -> None:
    term = TElemTerm(term_params)
    assert term._items == items


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("term", "normalized"),
    (
        (TElemTerm([(x, 1), (y, 2)]), None),
        (TElemTerm([(x, 1)]), None),
        (TElemTerm([(TElem('10x'), 1)]),
         TElemTerm(((Decimal(10), 1), (x, 1)))),
        (TElemTerm([(Decimal(10), -1), (TElem('10x'), 1)]),
         TElemTerm([(x, 1)])),
        (TElemTerm([(TElem('10x'), 1), (TElem('1000000z'), 1),
                    (TElem('1000y'), -1)]),
         TElemTerm(((Decimal(10000), 1), (x, 1), (y, -1), (z, 1)))),
        ),
    )
def test_normalization(term: TElemTerm, normalized: Optional[TElemTerm]) \
        -> None:
    if normalized is None:
        assert term.is_normalized
    else:
        assert not term.is_normalized
        assert term.normalized() == normalized


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("term", "splitted"),
    (
        (TElemTerm(), ()),
        (TElemTerm([(x, 1), (y, 2)]), ()),
        (TElemTerm([(Decimal(5), 1)]), (Decimal(5), TElemTerm())),
        (TElemTerm([(Decimal(5), 1), (y, 2), (z, -1)]),
         (Decimal(5), TElemTerm([(y, 2), (z, -1)]))),
        )
    )
def test_split(term: TElemTerm, splitted: Tuple[Rational, TElemTerm]) -> None:
    if not splitted:
        splitted = (1, term)
    assert term.split() == splitted


# noinspection PyMissingTypeHints
def test_hash() -> None:
    t = TElemTerm([(y, 2), (x, 1), (z, 0), (y, -1)])
    assert hash(t) == hash(t.normalized())


# noinspection PyMissingTypeHints
def test_comparision() -> None:
    t1 = TElemTerm([(y, 2), (x, 1)])
    t2 = TElemTerm([(x, 2), (y, 1)])
    t3 = TElemTerm([(y, 1), (x, 2)])
    assert t1 != t2
    assert t1 != t3
    assert t2 == t3
    xt = TElemTerm([(x, 1)])
    dxt = TElemTerm([(TElem('10x'), 1)])
    assert xt != dxt
    assert TElemTerm(((Decimal(10), 1), (x, 1))) == dxt
    assert TElemTerm(((Decimal(10), -1), (TElem('10x'), 1))) == xt


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("t1", "t2", "res"),
    (
        (TElemTerm([(y, 2), (x, 1)]), TElemTerm([(x, -2), (z, 1), (y, 1)]),
         TElemTerm(((x, -1), (y, 3), (z, 1)))),
        (TElemTerm([(y, 2), (x, 1)]), Decimal(5),
         TElemTerm(((Decimal(5), 1), (x, 1), (y, 2)))),
        (TElemTerm([(x, 1)]), Decimal(3),
         TElemTerm(((Decimal(3), 1), (x, 1)))),
        (Decimal(10), TElemTerm([(x, 1)]), TElemTerm([(TElem('10x'), 1)])),
        )
    )
def test_multiplication(t1: Union[TElemTerm, Rational],
                        t2: Union[TElemTerm, Rational], res: TElemTerm) \
        -> None:
    assert res == t1 * t2
    assert res == t2 * t1


# noinspection PyMissingTypeHints
@pytest.mark.parametrize(
    ("t1", "t2", "res"),
    (
        (TElemTerm([(y, 2), (x, 1)]), TElemTerm([(x, -2), (z, 1), (y, 1)]),
         TElemTerm(((x, 3), (y, 1), (z, -1)))),
        (TElemTerm([(y, 2), (x, 1)]), Fraction(1, 2),
         TElemTerm(((Decimal(2), 1), (x, 1), (y, 2)))),
        (Decimal(5), TElemTerm([(x, 1)]),
         TElemTerm(((Decimal(5), 1), (x, -1)))),
        (TElemTerm([(x, 1)]), TElemTerm([(x, 1)]), TElemTerm()),
        (TElemTerm([(TElem('10x'), 1)]), Decimal(10), TElemTerm([(x, 1)])),
        )
    )
def test_division(t1: Union[TElemTerm, Rational],
                  t2: Union[TElemTerm, Rational], res: TElemTerm) -> None:
    assert res == t1 / t2
    if isinstance(t2, Term):
        assert res == t1 * t2.reciprocal()


# noinspection PyUnresolvedReferences
def test_mul_div_raises() -> None:
    t = TElemTerm([(x, 1)])
    with pytest.raises(TypeError):
        _ = t * 'a'                     # type: ignore
    with pytest.raises(TypeError):
        _ = 'a' * t                     # type: ignore
    with pytest.raises(TypeError):
        _ = t / 'a'                     # type: ignore
    with pytest.raises(TypeError):
        _ = 'a' / t                     # type: ignore


def test_power() -> None:
    t = TElemTerm([(y, 2), (x, 1), (z, -3)])
    assert t ** 5 == TElemTerm(((x, 5), (y, 10), (z, -15)))


def test_str() -> None:
    t1 = TElemTerm([(y, 1), (x, 2)])
    assert str(t1) == 'y%sx%s' % (_MUL_SIGN, _POWER_CHARS[2])
    t2 = TElemTerm([(y, 2), (x, -1), (z, 3)])
    assert str(t2) == 'y%s%sz%s%sx' % (_POWER_CHARS[2], _MUL_SIGN,
                                       _POWER_CHARS[3], _DIV_SIGN)


def test_repr() -> None:
    t1 = TElemTerm([(y, 2), (x, 1)])
    assert t1, eval(repr(t1))
