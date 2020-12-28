# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2020 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Test driver for module qtymeta."""

# Standard library imports

# Third-party imports
import pytest

# Local imports
from quantity.qtymeta import QuantityMeta, Term


class X(metaclass=QuantityMeta):
    """Special class, can not be combined!"""


class A(metaclass=QuantityMeta):
    """Base A"""


class B(metaclass=QuantityMeta):
    """Base B"""


class C(metaclass=QuantityMeta):
    """Derived A * B"""

    definition = A * B


class D(metaclass=QuantityMeta):
    """Derived A ** 2"""

    definition = A ** 2


class E(metaclass=QuantityMeta):
    """Derived C / D"""

    definition = C / D


class F(metaclass=QuantityMeta):
    """Derived (B ** 2 / A ** 2) / C"""

    definition = (B ** 2 / A ** 2) / C


class G(metaclass=QuantityMeta):
    """Derived B * (A ** 2 / E)"""

    definition = B * (A ** 2 / E)


@pytest.mark.parametrize("cls", [A, B], ids=["A", "B"])
def test_base(cls: QuantityMeta) -> None:
    assert isinstance(cls, QuantityMeta)
    assert cls.is_base_quantity()
    assert not cls.is_derived_quantity()
    assert cls.definition.items[0][0] is cls
    assert cls.definition.items[0][1] == 1
    assert str(cls.definition) == cls.__name__
    assert cls.normalized_definition == cls.definition


@pytest.mark.parametrize(("cls", "cdef"),
                         [(C, A * B),
                          (D, A ** 2),
                          (E, C / D),
                          (F, B ** 2 / (A ** 2 * C)),
                          (G, B * A ** 2 / E)],
                         ids=["C", "D", "E", "F", "G"])
def test_derived(cls: QuantityMeta, cdef: Term) -> None:
    assert isinstance(cls, QuantityMeta)
    assert not cls.is_base_quantity()
    assert cls.is_derived_quantity()
    assert cls.definition == cdef
    assert str(cls.definition) == str(cdef)


@pytest.mark.parametrize(("cls", "cdef"),
                         [(C, A * B),
                          (D, A ** 2),
                          (E, B / A),
                          (F, B / A ** 3),
                          (G, A ** 3)],
                         ids=["C", "D", "E", "F", "G"])
def test_normalized_def(cls: QuantityMeta, cdef: Term) -> None:
    assert cls.normalized_definition == cdef
    assert str(cls.normalized_definition) == str(cdef)


def test_str() -> None:
    assert str(A) == "A"
