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
from decimalfp import Decimal

# Local imports
from quantity.cwdmeta import ClassDefT, ClassWithDefinitionMeta


class X(metaclass=ClassWithDefinitionMeta):
    """Special class, can not be combined!"""


class A(metaclass=ClassWithDefinitionMeta):
    """Base A"""


class B(metaclass=ClassWithDefinitionMeta):
    """Base B"""


class C(metaclass=ClassWithDefinitionMeta, define_as=A * B):
    """Derived A * B"""


class D(metaclass=ClassWithDefinitionMeta, define_as=A ** 2):
    """Derived A ** 2"""


class E(metaclass=ClassWithDefinitionMeta, define_as=C / D):
    """Derived C / D"""


class F(metaclass=ClassWithDefinitionMeta, define_as=(B ** 2 / A ** 2) / C):
    """Derived (B ** 2 / A ** 2) / C"""


class G(metaclass=ClassWithDefinitionMeta, define_as=B * (A ** 2 / E)):
    """Derived B * (A ** 2 / E)"""


@pytest.mark.parametrize("cls", [A, B], ids=["A", "B"])
def test_base(cls: ClassWithDefinitionMeta) -> None:
    assert isinstance(cls, ClassWithDefinitionMeta)
    assert cls.is_base_cls()
    assert not cls.is_derived_cls()
    assert cls.definition.items[0][0] is cls
    assert cls.definition.items[0][1] == 1
    assert str(cls.definition) == cls.__name__
    assert cls.normalized_definition == cls.definition


@pytest.mark.parametrize(("cls", "cdef"),
                         [(C, C.definition),
                          (D, A ** 2),
                          (E, C / D),
                          (F, B ** 2 / (A ** 2 * C)),
                          (G, B * A ** 2 / E)],
                         ids=["C", "D", "E", "F", "G"])
def test_derived(cls: ClassWithDefinitionMeta, cdef: ClassDefT) -> None:
    assert isinstance(cls, ClassWithDefinitionMeta)
    assert not cls.is_base_cls()
    assert cls.is_derived_cls()
    assert cls.definition == cdef
    assert str(cls.definition) == str(cdef)


@pytest.mark.parametrize(("cls", "cdef"),
                         [(C, A * B),
                          (D, A ** 2),
                          (E, B / A),
                          (F, B / A ** 3),
                          (G, A ** 3)],
                         ids=["C", "D", "E", "F", "G"])
def test_normalized_def(cls: ClassWithDefinitionMeta, cdef: ClassDefT) \
        -> None:
    assert cls.normalized_definition == cdef
    assert str(cls.normalized_definition) == str(cdef)


def test_str() -> None:
    assert str(A) == "A"


@pytest.mark.parametrize("cdef",
                         ["abc",
                          ClassDefT([(Decimal(5), 1)]),
                          ClassDefT([(A, 1), (B, 1), (Decimal(7), 1)])])
def test_fail_cls_def(cdef: ClassDefT) -> None:
    with pytest.raises(AssertionError):
        ClassWithDefinitionMeta("Fail", (), {}, define_as=cdef)
