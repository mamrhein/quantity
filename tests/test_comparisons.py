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

from fractions import Fraction
from typing import Any

import pytest
from decimalfp import Decimal

from quantity import (
    Quantity, QuantityError, Rational, Unit,
    )
from quantity.predefined import (
    CELSIUS, FAHRENHEIT, GRAM, KELVIN, KILOGRAM, KILOWATT, METRE, MILLIWATT,
    )


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
