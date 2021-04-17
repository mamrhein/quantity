# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2021 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.txt provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Test driver for Quantity conversion functions.."""

from fractions import Fraction
from numbers import Rational

import pytest
from decimalfp import Decimal

from quantity import IncompatibleUnitsError, Quantity, Unit
from quantity.predefined import (
    CELSIUS, CUBIC_CENTIMETRE, CUBIC_METRE, DAY, FAHRENHEIT, GIGAHERTZ, GRAM,
    HERTZ, JOULE, KELVIN, KILOWATT, KILOWATT_HOUR, LITRE, METRE, MILE_PER_HOUR,
    MILLIGRAM, MILLIMETRE, MILLIWATT, NEWTON, SQUARE_METRE,
    )


@pytest.mark.parametrize(("amnt", "unit", "to_unit", "res_amnt"),
                         [
                             ("17.3", GRAM, MILLIGRAM, "17300"),
                             (3, CUBIC_METRE, LITRE, 3000),
                             (50, MILLIWATT, KILOWATT, "0.00005"),
                             (30, CELSIUS, KELVIN, "303.15"),
                             (400, KELVIN, FAHRENHEIT, "260.33"),
                             (10, FAHRENHEIT, CELSIUS, Fraction(-110, 9))
                             ],
                         ids=lambda p: str(p))
def test_convert(amnt: str, unit: Unit, to_unit: Unit, res_amnt: str) -> None:
    if isinstance(amnt, str):
        amount = Decimal(amnt)
    else:
        amount = amnt
    if isinstance(res_amnt, str):
        res_amount = Decimal(res_amnt)
    else:
        res_amount = res_amnt
    qty = Decimal(amount) * unit
    conv_qty = qty.convert(to_unit)
    assert conv_qty.unit is to_unit
    assert conv_qty.amount == res_amount
    conv_back = conv_qty.convert(unit)
    assert conv_back.unit is unit
    assert conv_back.amount == amount


@pytest.mark.parametrize(("amnt", "unit", "to_unit"),
                         [
                             (17, GRAM, MILLIMETRE),
                             (3, CUBIC_METRE, MILE_PER_HOUR),
                             (50, MILLIWATT, KILOWATT_HOUR),
                             (30, CELSIUS, GIGAHERTZ),
                             ],
                         ids=lambda p: str(p))
def test_conv_wrong_unit(amnt: str, unit: Unit, to_unit: Unit) -> None:
    qty = Decimal(amnt) * unit
    with pytest.raises(IncompatibleUnitsError):
        _ = qty.convert(to_unit)


@pytest.mark.parametrize(("qty_str", "unit", "res_amnt"),
                         [
                             ("28.4 mm", METRE, Decimal("0.0284")),
                             ("20.7 kWh", JOULE, 74520000),
                             ("3 °C", KELVIN, Decimal("276.15")),
                             ("27 °F", CELSIUS, Fraction(-25, 9)),
                             ],
                         ids=lambda p: str(p))
def test_qty_from_str_with_unit(qty_str: str, unit: Unit, res_amnt: Rational) \
        -> None:
    qty = Quantity(qty_str, unit)
    assert qty.unit is unit
    assert qty.amount == res_amnt


@pytest.mark.parametrize(("qty_str", "unit"),
                         [
                             ("283 mm", SQUARE_METRE),
                             ("20 kWh", CELSIUS),
                             ("3 °C", HERTZ),
                             ("27 GHz", DAY),
                             ],
                         ids=lambda p: str(p))
def test_qty_from_str_wrong_unit(qty_str: str, unit: Unit) -> None:
    with pytest.raises(IncompatibleUnitsError):
        _ = Quantity(qty_str, unit)


@pytest.mark.parametrize("unit",
                         [NEWTON, FAHRENHEIT, CUBIC_CENTIMETRE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_qty_to_str(value: Rational, unit: Unit) -> None:
    qty = value * unit
    assert str(qty) == " ".join((str(qty.amount), str(qty.unit)))


@pytest.mark.parametrize("unit",
                         [NEWTON, FAHRENHEIT, CUBIC_CENTIMETRE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_qty_repr(value: Rational, unit: Unit) -> None:
    qty = value * unit
    if unit.is_ref_unit():
        assert repr(qty) == "%s(%s)" % (qty.__class__.__name__,
                                        repr(qty.amount))
    else:
        assert repr(qty) == "%s(%s, %s)" % (qty.__class__.__name__,
                                            repr(qty.amount), repr(qty.unit))
