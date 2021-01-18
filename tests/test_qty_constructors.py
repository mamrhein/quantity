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


"""Test constructors for Quantity instances.."""

# Standard library imports
from decimal import Decimal as StdLibDecimal

# Third-party imports
from typing import Any

import pytest
from quantity import QuantityError, QuantityMeta, Rational, Unit
from quantity.predefined import *


# noinspection PyPep8Naming
@pytest.mark.parametrize("Qty", [Mass, Force], ids=("Mass", "Force"))
@pytest.mark.parametrize("amnt",
                         [17, Fraction(2, 7), StdLibDecimal("29.82"),
                          Decimal("9283.10006"), 3.5, "0.004", b"2.99"],
                         ids=lambda p: str(p))
def test_qty_from_amnt_without_unit(Qty: QuantityMeta, amnt: Rational) \
        -> None:
    qty = Qty(amnt)
    if isinstance(amnt, str):
        amnt = Decimal(amnt)
    elif isinstance(amnt, bytes):
        amnt = Decimal(amnt.decode())
    assert qty.amount == amnt
    assert qty.unit is Qty.ref_unit


# noinspection PyPep8Naming
@pytest.mark.parametrize("Qty", [Mass, Power], ids=("Mass", "Power"))
@pytest.mark.parametrize("amnt",
                         [17, Fraction(2, 7), Decimal("9283.10006")],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("unit", [MILLIGRAM, GIGAWATT], ids=("mg", "GW"))
def test_qty_from_amnt_n_unit(Qty: QuantityMeta, amnt: Rational, unit: Unit)\
        -> None:
    if Qty is unit.qty_cls:
        qty = Qty(amnt, unit)
        assert qty.amount == amnt
        assert qty.unit is unit
    else:
        with pytest.raises(QuantityError):
            _ = Qty(amnt, unit)


@pytest.mark.parametrize("unit", [5, 'a'], ids=("5", "'a'"))
def test_wrong_unit_type(unit: Any) -> None:
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        _ = Length(1, unit)                     # type: ignore


@pytest.mark.parametrize("amnt",
                         [int, (2, 7), [24, "m"]],
                         ids=lambda p: str(p))
def test_wrong_amnt_type(amnt: Any) -> None:
    with pytest.raises(TypeError):
        _ = Length(amnt, METRE)


@pytest.mark.parametrize("amnt",
                         ["~3.1 m", "29,3 s"],
                         ids=lambda p: str(p))
def test_incompat_amnt(amnt: Any) -> None:
    with pytest.raises(QuantityError):
        _ = Length(amnt, METRE)


@pytest.mark.parametrize(("num_str", "amnt", "unit"),
                         [("17 m", 17, METRE),
                          ("2/7 kW", Fraction(2, 7), KILOWATT),
                          ("713.1 °C", Decimal("713.1"), CELSIUS)],
                         ids=lambda p: p if isinstance(p, str) else "")
def test_qty_from_str_with_unit(num_str: str, amnt: Rational, unit: Unit) \
        -> None:
    qty = Quantity(num_str)
    assert qty.amount == amnt
    assert qty.unit is unit
    assert qty.__class__ is unit.qty_cls


@pytest.mark.parametrize("num_str",
                         ["28.5 ", "17 m"],
                         ids=lambda p: p)
def test_missing_or_unknown_symbol(num_str: str) -> None:
    with pytest.raises(QuantityError):
        _ = Temperature(num_str)


@pytest.mark.parametrize(("amnt", "unit"),
                         [(319, METRE),
                          (Fraction(2, 100), MEGAWATT),
                          (Decimal("-15"), CELSIUS)],
                         ids=lambda p: str(p))
def test_qty_from_amnt_mul_unit(amnt: Rational, unit: Unit) \
        -> None:
    qty = amnt * unit
    assert qty.amount == amnt
    assert qty.unit is unit
    assert qty.__class__ is unit.qty_cls
