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


"""Test mathematical operators."""

import operator
from fractions import Fraction
from numbers import Rational, Real
from typing import Any, Callable

import pytest
from decimalfp import Decimal, ONE

from quantity import (
    IncompatibleUnitsError, Quantity, QuantityMeta, UndefinedResultError,
    Unit, UnitConversionError,
    )
from quantity.predefined import (
    CENTIMETRE, CUBIC_CENTIMETRE, Duration, FAHRENHEIT, GRAM, HECTARE, HOUR,
    JOULE, KILOMETRE, KILOMETRE_PER_HOUR, LITRE, Length, METRE,
    METRE_PER_SECOND_SQUARED, MICROSECOND, MILLIGRAM, MILLIMETRE, MILLIWATT,
    MINUTE, NEWTON, SECOND, SQUARE_METRE, TERAWATT,
    )

BinOpT = Callable[[Any, Any], Any]


@pytest.mark.parametrize("unit",
                         [METRE, TERAWATT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [-302, -1, 0, 4],
                         ids=lambda p: str(p))
def test_abs(value: Any, unit: Unit) -> None:
    qty = value * unit
    abs_qty = abs(qty)
    assert qty.__class__ is abs_qty.__class__
    assert qty.unit is abs_qty.unit
    assert abs(qty.amount) == abs_qty.amount


@pytest.mark.parametrize("unit",
                         [SQUARE_METRE, MILLIWATT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [-302, -1, 0, 4],
                         ids=lambda p: str(p))
def test_pos(value: Any, unit: Unit) -> None:
    qty = value * unit
    assert +qty is qty


@pytest.mark.parametrize("unit",
                         [HECTARE, LITRE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [-302, -1, 0, 4],
                         ids=lambda p: str(p))
def test_neg(value: Any, unit: Unit) -> None:
    qty = value * unit
    neg_qty = -qty
    assert qty.__class__ is neg_qty.__class__
    assert qty.unit is neg_qty.unit
    assert -qty.amount == neg_qty.amount


@pytest.mark.parametrize("unit2",
                         Length.units(),
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value2",
                         [Decimal("0.04"),
                          Fraction(1, 7),
                          ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.add, operator.sub],
                         ids=lambda p: str(str(p.__name__)))
@pytest.mark.parametrize("unit1",
                         Length.units(),
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value1",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_add_sub_compat_qty(value1: Rational, unit1: Unit, op: BinOpT,
                            value2: Rational, unit2: Unit) -> None:
    qty1 = value1 * unit1
    qty2 = value2 * unit2
    res = op(qty1, qty2)
    assert res.__class__ is qty1.__class__
    assert res.unit is unit1
    assert res.amount == op(qty1.amount, qty2.equiv_amount(unit1))


@pytest.mark.parametrize("qty2",
                         [3 * KILOMETRE_PER_HOUR, 17 * JOULE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.add, operator.sub],
                         ids=lambda p: str(str(p.__name__)))
@pytest.mark.parametrize("qty1",
                         [3 * MILLIMETRE, 17 * NEWTON],
                         ids=lambda p: str(p))
def test_add_sub_incompat_qty(qty1: Quantity, op: BinOpT, qty2: Quantity) -> \
        None:
    with pytest.raises(IncompatibleUnitsError):
        op(qty1, qty2)
    with pytest.raises(IncompatibleUnitsError):
        op(qty2, qty1)


@pytest.mark.parametrize("other",
                         [293, Decimal(5), "90"],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("op",
                         [operator.add, operator.sub],
                         ids=lambda p: str(p.__name__))
@pytest.mark.parametrize("qty",
                         [3 * METRE, 17 * NEWTON],
                         ids=lambda p: str(p))
def test_add_sub_incompat_type(qty: Quantity, op: BinOpT, other: Any) -> None:
    with pytest.raises(TypeError):
        op(qty, other)
    with pytest.raises(TypeError):
        op(other, qty)


@pytest.mark.parametrize("other",
                         [293, Decimal(5), Fraction(1, 3)],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [7 * METRE, 35 * NEWTON],
                         ids=lambda p: str(p))
def test_qty_mul_rational(qty: Quantity, other: Rational) -> None:
    res = other * qty
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == qty.amount * other
    res = qty * other
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == other * qty.amount


@pytest.mark.parametrize("other",
                         [29.4, 7.8, 0.000003],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [Decimal("2.5") * METRE, 35 * NEWTON],
                         ids=lambda p: str(p))
def test_qty_mul_float(qty: Quantity, other: float) -> None:
    res = other * qty
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == qty.amount * Decimal(other)
    res = qty * other
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == Decimal(other) * qty.amount


@pytest.mark.parametrize(("qty1", "qty2"),
                         [(3 * MILLIGRAM, 3 * METRE_PER_SECOND_SQUARED),
                          (15 * MILLIMETRE, 17 * NEWTON),
                          (Decimal("23.4") * METRE, 7 * CENTIMETRE),
                          ],
                         ids=lambda p: str(p))
def test_qty_mul_qty_defined_result(qty1: Quantity, qty2: Quantity) -> None:
    res = qty1 * qty2
    amount, unit = qty1.unit * qty2.unit
    amount *= qty1.amount * qty2.amount
    assert isinstance(res, Quantity)
    assert res.amount == amount
    assert res.unit == unit


@pytest.mark.parametrize("qty2",
                         [3 * KILOMETRE_PER_HOUR, 17 * JOULE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty1",
                         [3 * MILLIMETRE, 17 * FAHRENHEIT],
                         ids=lambda p: str(p))
def test_qty_mul_qty_undefined_result(qty1: Quantity, qty2: Quantity) -> None:
    with pytest.raises(UndefinedResultError):
        _ = qty1 * qty2
    with pytest.raises(UndefinedResultError):
        _ = qty2 * qty1


@pytest.mark.parametrize(("qty", "unit"),
                         [(3 * MILLIGRAM, METRE_PER_SECOND_SQUARED),
                          (15 * MILLIMETRE, NEWTON),
                          (Decimal("23.4") * METRE, KILOMETRE),
                          ],
                         ids=lambda p: str(p))
def test_qty_mul_unit_defined_result(qty: Quantity, unit: Unit) -> None:
    res = qty * unit
    res_amount, res_unit = qty.unit * unit
    res_amount *= qty.amount
    assert isinstance(res, Quantity)
    assert res.amount == res_amount
    assert res.unit == res_unit


@pytest.mark.parametrize("unit",
                         [KILOMETRE_PER_HOUR, JOULE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty1",
                         [3 * MILLIMETRE, 17 * FAHRENHEIT],
                         ids=lambda p: str(p))
def test_qty_mul_unit_undefined_result(qty1: Quantity, unit: Unit) -> None:
    with pytest.raises(UndefinedResultError):
        _ = qty1 * unit
    with pytest.raises(UndefinedResultError):
        _ = unit * qty1


@pytest.mark.parametrize("other",
                         [293, Decimal(5), Fraction(1, 3)],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [7 * METRE, 35 * NEWTON],
                         ids=lambda p: str(p))
def test_qty_div_rational(qty: Quantity, other: Rational) -> None:
    res = qty / other
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == qty.amount / other


@pytest.mark.parametrize("other",
                         [17.4, 5.0382, 0.00037],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [7 * METRE, 35 * NEWTON],
                         ids=lambda p: str(p))
def test_qty_div_float(qty: Quantity, other: float) -> None:
    res = qty / other
    assert res.__class__ is qty.__class__
    assert res.unit is qty.unit
    assert res.amount == qty.amount / Decimal(other)


@pytest.mark.parametrize("other",
                         [293, Decimal(5), Fraction(1, 3), 0.495],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [7 * SECOND, 35 * MICROSECOND],
                         ids=lambda p: str(p))
def test_rdiv_qty_defined_result(qty: Quantity, other: Real) \
        -> None:
    res = other / qty
    if isinstance(other, float):
        amount = Decimal(other) / qty.amount
    else:
        amount = other / qty.amount
    qty = ONE / qty.unit
    assert res == amount * qty


@pytest.mark.parametrize("other",
                         [293, Decimal(5), Fraction(1, 3)],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [7 * METRE, 35 * MILLIGRAM],
                         ids=lambda p: str(p))
def test_rational_div_qty_undefined_result(qty: Quantity, other: Rational) \
        -> None:
    with pytest.raises(UndefinedResultError):
        _ = other / qty


@pytest.mark.parametrize(("qty1", "qty2"),
                         [(3 * JOULE, 3 * MINUTE),
                          (15 * CUBIC_CENTIMETRE, 17 * MILLIMETRE),
                          (Decimal("23.4") * METRE, 7 * MICROSECOND),
                          ],
                         ids=lambda p: str(p))
def test_qty_div_qty_defined_result(qty1: Quantity, qty2: Quantity) -> None:
    res = qty1 / qty2
    amount, unit = qty1.unit / qty2.unit
    amount *= qty1.amount / qty2.amount
    assert isinstance(res, Quantity)
    assert res.amount == amount
    assert res.unit == unit


@pytest.mark.parametrize("qty2",
                         [3 * KILOMETRE_PER_HOUR, 17 * JOULE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty1",
                         [3 * GRAM, 17 * FAHRENHEIT],
                         ids=lambda p: str(p))
def test_qty_div_qty_undefined_result(qty1: Quantity, qty2: Quantity) -> None:
    with pytest.raises(UndefinedResultError):
        _ = qty1 / qty2
    with pytest.raises(UndefinedResultError):
        _ = qty2 / qty1


@pytest.mark.parametrize(("qty1", "qty2"),
                         [(3 * JOULE, 3 * JOULE),
                          (15 * METRE, 17 * MILLIMETRE),
                          (Decimal("23.4") * HOUR, 7 * MICROSECOND),
                          ],
                         ids=lambda p: str(p))
def test_qty_div_same_qty(qty1: Quantity, qty2: Quantity) -> None:
    res = qty1 / qty2
    amount = qty1.amount / qty2.amount
    factor, _ = qty1.unit / qty2.unit
    assert res == amount * factor


@pytest.mark.parametrize(("qty", "unit"),
                         [(3 * JOULE, MINUTE),
                          (15 * CUBIC_CENTIMETRE, MILLIMETRE),
                          (Decimal("23.4") * METRE, MICROSECOND),
                          (3 * JOULE, JOULE),
                          (15 * METRE, KILOMETRE),
                          (Decimal("23.4") * HOUR, MINUTE),
                          ],
                         ids=lambda p: str(p))
def test_qty_div_unit_defined_result(qty: Quantity, unit: Unit) -> None:
    res = qty / unit
    res_amount, res_unit = qty.unit / unit
    res_amount *= qty.amount
    if res_unit is None:
        assert res == res_amount
    else:
        assert isinstance(res, Quantity)
        assert res.amount == res_amount
        assert res.unit == res_unit


@pytest.mark.parametrize("unit",
                         [KILOMETRE_PER_HOUR, JOULE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("qty",
                         [3 * GRAM, 17 * FAHRENHEIT],
                         ids=lambda p: str(p))
def test_qty_div_unit_undefined_result(qty: Quantity, unit: Quantity) -> None:
    with pytest.raises(UndefinedResultError):
        _ = qty / unit


@pytest.mark.parametrize("op",
                         [operator.add, operator.sub, operator.truediv],
                         ids=lambda p: str(p.__name__))
def test_op_qty_without_conv(qty_cls_without_conv: QuantityMeta, op: BinOpT) \
        -> None:
    unit1, unit2 = qty_cls_without_conv.units()
    qty1 = 5 * unit1
    qty2 = 5 * unit2
    with pytest.raises(UnitConversionError):
        op(qty1, qty2)
    with pytest.raises(UnitConversionError):
        op(qty2, qty1)


def test_mul_qty_without_conv(qty_cls_without_conv: QuantityMeta) -> None:
    unit1, unit2 = qty_cls_without_conv.units()
    qty1 = 5 * unit1
    qty2 = 5 * unit2
    with pytest.raises(UndefinedResultError):
        _ = qty1 * qty2
    with pytest.raises(UndefinedResultError):
        _ = qty2 * qty1


@pytest.mark.parametrize("exp", [2, 3], ids=lambda p: str(p))
@pytest.mark.parametrize("unit",
                         Length.units(),
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_pos_exp_defined_result(value: Rational, unit: Unit, exp: int) \
        -> None:
    base = value * unit
    res = base ** exp
    qty = base.unit ** exp
    assert res.unit == qty.unit
    assert res.amount == base.amount ** exp * qty.amount


@pytest.mark.parametrize("unit",
                         Duration.units(),
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_neg_exp_defined_result(value: Rational, unit: Unit) -> None:
    exp = -1
    base = value * unit
    res = base ** exp
    qty = base.unit ** exp
    assert res.unit == qty.unit
    assert res.amount == base.amount ** exp * qty.amount


@pytest.mark.parametrize("exp", [-1, 2], ids=lambda p: str(p))
@pytest.mark.parametrize("unit",
                         [GRAM, FAHRENHEIT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_undefined_result(value: Rational, unit: Unit, exp: int) -> None:
    base = value * unit
    with pytest.raises(UndefinedResultError):
        _ = base ** exp


@pytest.mark.parametrize("unit",
                         [NEWTON, FAHRENHEIT, CUBIC_CENTIMETRE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_one(value: Rational, unit: Unit) -> None:
    base = value * unit
    assert base == base ** 1


@pytest.mark.parametrize("unit",
                         [NEWTON, FAHRENHEIT, CUBIC_CENTIMETRE],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_zero(value: Rational, unit: Unit) -> None:
    base = value * unit
    assert base ** 0 == ONE


@pytest.mark.parametrize("exp", [-1.0, Fraction(1, 2)], ids=lambda p: str(p))
@pytest.mark.parametrize("unit",
                         [GRAM, FAHRENHEIT],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("value",
                         [Decimal("0.0003"),
                          Fraction(1000, 3),
                          ],
                         ids=lambda p: str(p))
def test_pow_non_int(value: Rational, unit: Unit, exp: int) -> None:
    base = value * unit
    with pytest.raises(TypeError):
        _ = base ** exp
