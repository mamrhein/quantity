# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2021 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Test comparisions.."""

import operator
from fractions import Fraction
from typing import Any, Callable, TypeVar

import pytest
from decimalfp import Decimal

from quantity import (
    IncompatibleUnitsError, Quantity, QuantityError, Rational, Unit,
    UnitConversionError,
    )
from quantity.predefined import (
    CELSIUS, FAHRENHEIT, GRAM, KELVIN, KILOGRAM, KILOWATT, METRE, MILLIGRAM,
    MILLIWATT,
    )

T = TypeVar("T")
CmpOpT = Callable[[T, T], bool]


class QtyWithoutConv(Quantity):
    pass


QWC1 = QtyWithoutConv.new_unit('qwc1')
QWC2 = QtyWithoutConv.new_unit('qwc2')


@pytest.mark.parametrize(("rhs_amnt", "rhs_unit"),
                         [
                             (Decimal("17.3"), GRAM),
                             (Fraction(1, 3), KILOGRAM),
                             (50, MILLIWATT),
                             (Decimal("0.00005"), KILOWATT),
                             (30, CELSIUS),
                             (300, KELVIN),
                             (86, FAHRENHEIT)
                             ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize(("lhs_amnt", "lhs_unit"),
                         [
                             (Decimal("17.3"), GRAM),
                             (Fraction(1, 3), KILOGRAM),
                             (50, MILLIWATT),
                             (Decimal("0.00005"), KILOWATT),
                             (30, CELSIUS),
                             (300, KELVIN),
                             (86, FAHRENHEIT)
                             ],
                         ids=lambda p: str(p))
def test_qty_eq_qty(lhs_amnt: Rational, lhs_unit: Unit,
                    rhs_amnt: Rational, rhs_unit: Unit):
    lhs = lhs_amnt * lhs_unit
    rhs = rhs_amnt * rhs_unit
    try:
        equiv = rhs.convert(lhs_unit)
    except QuantityError:
        assert lhs != rhs
    else:
        assert (lhs == rhs) == (lhs_amnt == equiv.amount)


@pytest.mark.parametrize(("lhs", "rhs"),
                         [
                             ("283 mm", METRE),
                             ("20 kWh", 20),
                             ("3 °C", int),
                             ("27 GHz", "GHz"),
                             ],
                         ids=lambda p: str(p))
def test_qty_eq_non_qty(lhs: str, rhs: Any):
    lhs = Quantity(lhs)
    assert lhs != rhs


# noinspection PyMissingTypeHints
def test_eq_qty_without_conv():
    qty1 = 5 * QWC1
    qty2 = 5 * QWC2
    assert qty1 == qty1
    assert qty2 == qty2
    assert qty1 != qty2
    assert qty2 != qty1


@pytest.mark.parametrize(("rhs_amnt", "rhs_unit"),
                         [
                             (Decimal("13.04"), GRAM),
                             (Fraction(1, 3), KILOGRAM),
                             (50, MILLIGRAM),
                             (Decimal("0.00005"), KILOGRAM),
                             ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.lt, operator.le, operator.gt, operator.ge],
                         ids=lambda p: p.__name__)
@pytest.mark.parametrize(("lhs_amnt", "lhs_unit"),
                         [
                             (Decimal("13.04"), GRAM),
                             (Fraction(1, 3), KILOGRAM),
                             (50, MILLIGRAM),
                             (Decimal("0.00005"), KILOGRAM),
                             ],
                         ids=lambda p: str(p))
def test_qty_cmp_qty(lhs_amnt: Rational, lhs_unit: Unit, op: CmpOpT,
                     rhs_amnt: Rational, rhs_unit: Unit):
    lhs = lhs_amnt * lhs_unit
    rhs = rhs_amnt * rhs_unit
    equiv = rhs.convert(lhs_unit)
    assert op(lhs, rhs) == op(lhs_amnt, equiv.amount)


@pytest.mark.parametrize(("rhs_amnt", "rhs_unit"),
                         [
                             (Decimal("13.04"), GRAM),
                             (Fraction(1, 3), KILOWATT),
                             ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.lt, operator.le, operator.gt, operator.ge],
                         ids=lambda p: p.__name__)
@pytest.mark.parametrize(("lhs_amnt", "lhs_unit"),
                         [
                             (50, CELSIUS),
                             (Decimal("0.07"), METRE),
                             ],
                         ids=lambda p: str(p))
def test_qty_cmp_incompat_qty(lhs_amnt: Rational, lhs_unit: Unit, op: CmpOpT,
                              rhs_amnt: Rational, rhs_unit: Unit):
    lhs = lhs_amnt * lhs_unit
    rhs = rhs_amnt * rhs_unit
    with pytest.raises(IncompatibleUnitsError):
        op(lhs, rhs)


@pytest.mark.parametrize("op",
                         [operator.lt, operator.le, operator.gt, operator.ge],
                         ids=lambda p: p.__name__)
def test_cmp_qty_without_conv(op: CmpOpT):
    qty1 = 5 * QWC1
    qty2 = 5 * QWC2
    with pytest.raises(UnitConversionError):
        op(qty1, qty2)
    with pytest.raises(UnitConversionError):
        op(qty2, qty1)


@pytest.mark.parametrize("other",
                         [
                             197,
                             Fraction(1, 7),
                             "50"
                             ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.lt, operator.le, operator.gt, operator.ge],
                         ids=lambda p: p.__name__)
@pytest.mark.parametrize(("amnt", "unit"),
                         [
                             (530, METRE),
                             (Decimal("0.07"), KILOWATT),
                             ],
                         ids=lambda p: str(p))
def test_qty_cmp_non_qty(amnt: Rational, unit: Unit, op: CmpOpT,
                         other: Any):
    qty = amnt * unit
    with pytest.raises(TypeError):
        op(qty, other)
    with pytest.raises(TypeError):
        op(other, qty)
