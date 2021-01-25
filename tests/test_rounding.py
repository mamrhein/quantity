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


"""Test-driver for rounding and quantization."""

from fractions import Fraction

import pytest
from decimalfp import Decimal, ROUNDING

from quantity import Quantity
from quantity.predefined import (
    CARAT, CELSIUS, FAHRENHEIT, GRAM, HOUR, KELVIN, KILOGRAM, KILOWATT, METRE,
    MILE, MILLIWATT, OUNCE, POUND, )


@pytest.fixture(scope="module",
                params=[rounding_mode for rounding_mode in ROUNDING],
                ids=[rounding_mode.name for rounding_mode in ROUNDING])
def rounding_mode(request) -> ROUNDING:
    return request.param


@pytest.mark.parametrize("n_digits",
                         [-2, 0, 3],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty_unit",
                         [CARAT, GRAM, FAHRENHEIT, KILOWATT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty_amnt",
                         [17, Fraction(4, 3), Decimal("834.6719")],
                         ids=lambda p: str(p))
def test_round(qty_amnt, qty_unit, n_digits) -> None:
    qty = qty_amnt * qty_unit
    rounded = round(qty, n_digits)
    assert rounded.unit is qty_unit
    assert rounded.amount == round(qty.amount, n_digits)


@pytest.mark.parametrize("quant_unit",
                         [GRAM, CARAT, OUNCE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("quant_amnt",
                         [1, Fraction(1, 7), Decimal("0.25")],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty_unit",
                         [CARAT, GRAM, POUND, KILOGRAM],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty_amnt",
                         [17, Fraction(4, 3), Decimal("834.6719")],
                         ids=lambda p: str(p))
def test_quantize_linear_scaled(qty_amnt, qty_unit, quant_amnt, quant_unit,
                                rounding_mode) -> None:
    qty = qty_amnt * qty_unit
    quant = quant_amnt * quant_unit
    quantized = qty.quantize(quant, rounding_mode)
    assert isinstance(qty, Quantity)
    assert quantized.unit is qty_unit
    equiv = quant.equiv_amount(qty_unit)
    if isinstance(qty_amnt, int):
        res_amnt = Decimal(qty_amnt).quantize(equiv, rounding_mode)
    elif isinstance(qty_amnt, Decimal):
        res_amnt = qty_amnt.quantize(equiv, rounding_mode)
    else:  # handle Fraction
        mult = Decimal(qty_amnt / equiv, 3).adjusted(0, rounding_mode)
        if mult == 0 and rounding_mode in (ROUNDING.ROUND_05UP,
                                           ROUNDING.ROUND_CEILING):
            mult = 1
        res_amnt = mult * equiv
    assert quantized.amount == res_amnt


@pytest.mark.parametrize("quant_unit",
                         [GRAM, POUND, MILLIWATT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty_unit",
                         [METRE, MILE, HOUR, KELVIN],
                         ids=lambda p: str(p))
def test_quantize_wrong_quant_unit(qty_unit, quant_unit) -> None:
    qty = 5 * qty_unit
    quant = 1 * quant_unit
    with pytest.raises(TypeError):
        _ = qty.quantize(quant)


def test_quantize_qty_without_ref_unit() -> None:
    t = 73 * FAHRENHEIT
    q = 1 * CELSIUS
    with pytest.raises(TypeError):
        _ = t.quantize(q)
