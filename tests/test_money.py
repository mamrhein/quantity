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


"""Test driver for sub-package 'money'.."""
from fractions import Fraction
from numbers import Real
from typing import Any, Optional, Type, Union

import pytest
from decimalfp import Decimal, ONE

from quantity import (
    IncompatibleUnitsError, Quantity, QuantityError,
    UndefinedResultError, UnitConversionError, )
from quantity.money import Currency, Money
from quantity.predefined import GRAM, KILOGRAM, Mass, NEWTON

EUR = Money.register_currency('EUR')
HKD = Money.register_currency('HKD')
TND = Money.register_currency('TND')
USD = Money.register_currency('USD')
ZWL = Money.register_currency('ZWL')


class PricePerMass(Quantity,
                   define_as=Money / Mass):
    pass


EURpKg = PricePerMass.new_unit("EUR/kg", derive_from=(EUR, KILOGRAM))
HKDpKg = PricePerMass.new_unit("HKD/kg", derive_from=(HKD, KILOGRAM))


@pytest.mark.parametrize(("iso_code", "name", "minor_unit",
                          "smallest_fraction"),
                         [("x", None, None, None),
                          ("y", "Y", None, Decimal("0.1")),
                          ("z", "Z", 3, None),
                          ],
                         ids=lambda p: str(p))
def test_currency_constructor(iso_code: str, name: Optional[str],
                              minor_unit: Optional[int],
                              smallest_fraction: Union[Real, str, None]) \
        -> None:
    curr = Currency(iso_code, name, minor_unit, smallest_fraction)
    assert curr.iso_code == iso_code
    assert curr.name == name or iso_code
    if minor_unit is None:
        assert curr.smallest_fraction == smallest_fraction or Decimal("0.01")
    else:
        assert curr.smallest_fraction == Decimal(10) ** -minor_unit
    assert curr.quantum == curr.smallest_fraction


@pytest.mark.parametrize(("iso_code", "name", "minor_unit",
                          "smallest_fraction", "exc"),
                         [(5, None, None, None, TypeError),
                          ("", None, None, None, ValueError),
                          ("x", "x", 2.5, None, TypeError),
                          ("x", "x", -5, None, ValueError),
                          ("x", "x", None, 0, ValueError),
                          ("x", "x", None, Decimal("-0.01"), ValueError),
                          ("x", "x", None, Decimal("0.03"), ValueError),
                          ("x", "x", 3, Decimal("0.01"), ValueError),
                          ],
                         ids=("iso_code_non_str",
                              "iso_code_empty",
                              "minor_unit_non_int",
                              "minor_unit_negative",
                              "smallest_fraction_eq_zero",
                              "smallest_fraction_negative",
                              "smallest_fraction_not_int_frac_of_one",
                              "smallest_fraction_does_not_fit_minot_unit",
                              ))
def test_new_currency_fails(iso_code: str, name: Optional[str],
                            minor_unit: Optional[int],
                            smallest_fraction: Union[Real, str, None],
                            exc: Type[BaseException]) -> None:
    with pytest.raises(exc):
        _ = Currency(iso_code, name, minor_unit, smallest_fraction)


@pytest.mark.parametrize("reg_curr",
                         [EUR, HKD, USD],
                         ids=lambda p: str(p))
def test_registered_currency(reg_curr: Currency) -> None:
    curr = Money.get_unit_by_symbol(reg_curr.iso_code)
    assert curr is reg_curr


@pytest.mark.parametrize("iso_code",
                         ["SFR", "GBR"],
                         ids=lambda p: str(p))
def test_non_registered_currency(iso_code: str) -> None:
    with pytest.raises(ValueError):
        _ = Money.get_unit_by_symbol(iso_code)


@pytest.mark.parametrize("reg_curr",
                         [EUR, HKD, USD],
                         ids=lambda p: str(p))
def test_register_already_registered_currency(reg_curr: Currency) -> None:
    curr = Money.register_currency(reg_curr.iso_code)
    assert curr is reg_curr


@pytest.mark.parametrize("amnt",
                         [14, 3.7, Fraction(2, 7), Decimal("9283.10006")],
                         ids=lambda p: str(p))
def test_money_constructor(amnt: Real) -> None:
    quantum = USD.smallest_fraction
    mny = Money(amnt, USD)
    assert mny.currency is USD
    assert mny.amount == Decimal(amnt, 9).quantize(quantum)


@pytest.mark.parametrize("amnt", [Mass(ONE), Mass], ids=lambda p: str(p))
def test_wrong_amnt_type(amnt: Any) -> None:
    with pytest.raises(TypeError):
        _ = Money(amnt, USD)


@pytest.mark.parametrize("unit", [5, 'a', Mass], ids=lambda p: str(p))
def test_wrong_unit_type(unit: Any) -> None:
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        _ = Money(1, unit)  # type: ignore


@pytest.mark.parametrize("unit", [NEWTON, KILOGRAM], ids=lambda p: str(p))
def test_incompat_unit(unit: Any) -> None:
    with pytest.raises(QuantityError):
        # noinspection PyTypeChecker
        _ = Money(1, unit)  # type: ignore


@pytest.mark.parametrize("amnt",
                         [14, 3.7, Fraction(2, 7), Decimal("9283.10006")],
                         ids=lambda p: str(p))
def test_money_from_str(amnt: Real) -> None:
    quantum = TND.smallest_fraction
    mny = Money(f"{amnt} {TND}")
    assert mny.currency is TND
    assert mny.amount == Decimal(amnt, 9).quantize(quantum)


@pytest.mark.parametrize("amnt",
                         ["25", "25€", "25 €"],
                         ids=lambda p: str(p))
def test_money_fails_from_malformed_str(amnt: Real) -> None:
    with pytest.raises(QuantityError):
        _ = Money(amnt)


@pytest.mark.parametrize("amnt",
                         [14, 3.7, Fraction(2, 7), Decimal("9283.10006")],
                         ids=lambda p: str(p))
def test_amnt_mul_curr(amnt: Real) -> None:
    quantum = HKD.smallest_fraction
    mny = amnt * HKD
    assert mny.currency is HKD
    assert mny.amount == Decimal(amnt, 9).quantize(quantum)


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(3, Decimal(8)),
                          (2.5, 7),
                          (Fraction(1, 4), Decimal("0.5")),
                          ],
                         ids=lambda p: str(p))
def test_add_sub_same_curr(amnt1: Real, amnt2: Real) -> None:
    assert amnt1 * EUR + amnt2 * EUR == (amnt1 + amnt2) * EUR
    assert amnt2 * EUR + amnt1 * EUR == (amnt2 + amnt1) * EUR
    assert amnt1 * EUR - amnt2 * EUR == (amnt1 - amnt2) * EUR
    assert amnt2 * EUR - amnt1 * EUR == (amnt2 - amnt1) * EUR


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(3, Decimal(8)),
                          (2.5, 7),
                          (Fraction(1, 4), Decimal("0.5")),
                          ],
                         ids=lambda p: str(p))
def test_add_sub_diff_curr_fails(amnt1: Real, amnt2: Real) -> None:
    with pytest.raises(UnitConversionError):
        _ = amnt1 * HKD + amnt2 * ZWL
    with pytest.raises(UnitConversionError):
        _ = amnt1 * HKD - amnt2 * ZWL


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(3, Decimal(8)),
                          (2.5, 7),
                          (Fraction(1, 4), Decimal("0.5")),
                          ],
                         ids=lambda p: str(p))
def test_add_sub_non_money_fails(amnt1: Real, amnt2: Real) -> None:
    with pytest.raises(IncompatibleUnitsError):
        _ = amnt1 * HKD + amnt2 * KILOGRAM
    with pytest.raises(IncompatibleUnitsError):
        _ = amnt1 * HKD - amnt2 * KILOGRAM


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(13, Decimal("8.4")),
                          (12.5, 7),
                          (Fraction(1, 40), Decimal("50")),
                          ],
                         ids=lambda p: str(p))
def test_mul_div_scalar(amnt1: Real, amnt2: Real) -> None:
    mny = amnt1 * TND
    assert amnt2 * mny == (amnt2 * mny.amount) * TND
    assert mny / amnt2 == (mny.amount / amnt2) * TND


@pytest.mark.parametrize("curr2",
                         [ZWL, USD],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("curr1",
                         [EUR, USD],
                         ids=lambda p: str(p))
def test_mny_mul_mny_fails(curr1: Currency, curr2: Currency) -> None:
    with pytest.raises(UndefinedResultError):
        _ = Money(ONE, curr1) * Money(ONE, curr2)


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(3, Decimal(8)),
                          (2.5, 7),
                          (Fraction(1, 4), Decimal("0.5")),
                          ],
                         ids=lambda p: str(p))
def test_mny_div_mny_same_curr(amnt1: Real, amnt2: Real) -> None:
    mny1 = amnt1 * EUR
    mny2 = amnt2 * EUR
    assert mny1 / mny2 == mny1.amount / mny2.amount
    assert mny2 / mny1 == mny2.amount / mny1.amount


@pytest.mark.parametrize(("amnt1", "amnt2"),
                         [(3, Decimal(8)),
                          (2.5, 7),
                          (Fraction(1, 4), Decimal("0.5")),
                          ],
                         ids=lambda p: str(p))
def test_mny_div_mny_diff_curr_fails(amnt1: Real, amnt2: Real) -> None:
    with pytest.raises(UnitConversionError):
        _ = (amnt1 * HKD) / (amnt2 * ZWL)


@pytest.mark.parametrize(("qty", "amnt_per_kg", "curr", "discount", "total"),
                         [(3 * KILOGRAM, Decimal("0.5"), EUR, Decimal(20),
                           Decimal("1.2") * EUR),
                          (500 * GRAM, Decimal("2.55"), EUR, Decimal(10),
                           Decimal("1.15") * EUR),
                          ],
                         ids=lambda p: str(p))
def test_mixed_calc(qty: Mass, amnt_per_kg: Decimal, curr: Currency,
                    discount: Decimal, total: Money) -> \
        None:
    price = (amnt_per_kg * curr) / KILOGRAM
    assert isinstance(price, PricePerMass)
    discounted_price = price * ((Decimal(100) - discount) / Decimal(100))
    assert isinstance(discounted_price, PricePerMass)
    calc_total = qty * discounted_price
    assert isinstance(calc_total, Money)
    assert calc_total.amount == total.amount
    assert calc_total.currency == total.currency
