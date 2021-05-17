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


"""Test driver for sub-package 'money'."""

from fractions import Fraction
from numbers import Rational, Real
from typing import Any, Optional, Type, Union

import pytest
from decimalfp import Decimal, ONE

from quantity import (
    IncompatibleUnitsError, Quantity, QuantityError,
    UndefinedResultError, Unit, UnitConversionError, )
from quantity.money import Currency, ExchangeRate, Money
from quantity.predefined import GRAM, KILOGRAM, Mass, NEWTON

EUR = Money.register_currency("EUR")
HKD = Money.register_currency("HKD")
TND = Money.register_currency("TND")
USD = Money.register_currency("USD")
ZWL = Money.register_currency("ZWL")


class PricePerMass(Quantity,
                   define_as=Money / Mass):
    pass


EURpKg = PricePerMass.new_unit("EUR/kg", derive_from=(EUR, KILOGRAM))
HKDpKg = PricePerMass.new_unit("HKD/kg", derive_from=(HKD, KILOGRAM))
TNDpKg = PricePerMass.new_unit("TND/kg", derive_from=(TND, KILOGRAM))
USDpKg = PricePerMass.new_unit("USD/kg", derive_from=(USD, KILOGRAM))
ZWLpKg = PricePerMass.new_unit("ZWL/kg", derive_from=(ZWL, KILOGRAM))


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


@pytest.mark.parametrize("curr",
                         [EUR, TND, USD],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("amnt",
                         [14, 3.7, Fraction(2, 7), Decimal("9283.10006")],
                         ids=lambda p: str(p))
def test_money_constructor(amnt: Real, curr: Currency) -> None:
    quantum = curr.smallest_fraction
    mny = Money(amnt, curr)
    assert mny.currency is curr
    assert mny.amount == Decimal(amnt, 9).quantize(quantum)


@pytest.mark.parametrize("amnt", [Mass(ONE), Mass], ids=lambda p: str(p))
def test_wrong_amnt_type(amnt: Any) -> None:
    with pytest.raises(TypeError):
        _ = Money(amnt, USD)


@pytest.mark.parametrize("unit", [5, "a", Mass], ids=lambda p: str(p))
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
def test_mny_qty_mixed_calc(qty: Mass, amnt_per_kg: Decimal, curr: Currency,
                            discount: Decimal, total: Money) -> None:
    price = (amnt_per_kg * curr) / KILOGRAM
    assert isinstance(price, PricePerMass)
    discounted_price = price * ((Decimal(100) - discount) / Decimal(100))
    assert isinstance(discounted_price, PricePerMass)
    calc_total = qty * discounted_price
    assert isinstance(calc_total, Money)
    assert calc_total.amount == total.amount
    assert calc_total.currency == total.currency


@pytest.mark.parametrize(("unit_currency", "unit_multiple", "term_currency",
                          "term_amount"),
                         [(EUR, 1, HKD, Decimal("8.395804")),
                          (EUR, Fraction(50, 1), HKD, 8.5),
                          ("EUR", 100, "HKD", "839.5804"),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_constructor(unit_currency: Union[Currency, str],
                               unit_multiple: Rational,
                               term_currency: Union[Currency, str],
                               term_amount: Union[Rational, float, str]) \
        -> None:
    exch = ExchangeRate(unit_currency, unit_multiple, term_currency,
                        term_amount)
    assert isinstance(exch, ExchangeRate)
    if isinstance(unit_currency, Currency):
        assert exch.unit_currency == unit_currency
    else:
        assert exch.unit_currency.iso_code == unit_currency
        unit_currency = exch.unit_currency
    if isinstance(term_currency, Currency):
        assert exch.term_currency == term_currency
    else:
        assert exch.term_currency.iso_code == term_currency
        term_currency = exch.term_currency
    assert exch.rate == Decimal(term_amount) / Decimal(unit_multiple)
    assert exch.inverse_rate == Decimal(unit_multiple) / Decimal(term_amount)
    assert exch.quotation == (unit_currency, term_currency, exch.rate)
    assert exch.inverse_quotation == (term_currency, unit_currency,
                                      exch.inverse_rate)


@pytest.mark.parametrize(("unit_currency", "unit_multiple", "term_currency",
                          "term_amount", "exc"),
                         [("ABC", 1, HKD, 2, ValueError),
                          (EUR, 1, "HXX", 5, ValueError),
                          (3, 1, HKD, 5, TypeError),
                          (EUR, 1, 2.5, 5, TypeError),
                          (EUR, 1, EUR, 5, ValueError),
                          (EUR, 1.5, HKD, 5, ValueError),
                          (EUR, -10, HKD, 5, ValueError),
                          (EUR, 0, HKD, 5, ValueError),
                          (EUR, 1, HKD, float, TypeError),
                          (EUR, 1, HKD, float("inf"), ValueError),
                          (EUR, 1, HKD, 0, ValueError),
                          (EUR, 1, HKD, -5, ValueError),
                          (EUR, 1, HKD, Decimal("0.00000002"), ValueError),
                          ],
                         ids=("unknown_unit_curr",
                              "unknown_term_curr",
                              "wrong_type_unit_curr",
                              "wrong_type_term_curr",
                              "identical_curr",
                              "unit_multiple_non_int",
                              "unit_multiple_neg",
                              "unit_multiple_zero",
                              "term_amount_wrong_type",
                              "term_amount_not_conv_decimal",
                              "term_amount_zero",
                              "term_amount_neg",
                              "term_amount_too_small",
                              ))
def test_exch_rate_wrong_params(unit_currency: Any, unit_multiple: Any,
                                term_currency: Any, term_amount: Any,
                                exc: Type[BaseException]) -> None:
    with pytest.raises(exc):
        _ = ExchangeRate(unit_currency, unit_multiple, term_currency,
                         term_amount)


@pytest.mark.parametrize(("unit_currency", "unit_multiple", "term_currency",
                          "term_amount", "adj_unit_multiple",
                          "adj_term_amount"),
                         [(EUR, 50, HKD, Decimal("50.38"),
                           Decimal(10), Decimal("10.076")),
                          (EUR, 755, HKD, Decimal("3001.4027006"),
                           100, Decimal("397.536782")),
                          (EUR, 1, ZWL, Decimal("0.0004027006"),
                           1000, Decimal("0.402701")),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_adjustment(unit_currency: Currency, unit_multiple: Rational,
                              term_currency: Currency, term_amount: Decimal,
                              adj_unit_multiple: int,
                              adj_term_amount: Decimal) -> None:
    exch = ExchangeRate(unit_currency, unit_multiple, term_currency,
                        term_amount)
    assert isinstance(exch, ExchangeRate)
    assert exch._unit_multiple == adj_unit_multiple
    assert exch._term_amount == adj_term_amount


@pytest.mark.parametrize(("unit_currency", "unit_multiple", "term_currency",
                          "term_amount"),
                         [(EUR, 1, HKD, Decimal("8.395804")),
                          (EUR, 50, HKD, Decimal("401.509")),
                          (EUR, 100, HKD, Decimal("839.5804")),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_inversion(unit_currency: Currency, unit_multiple: Rational,
                             term_currency: Currency, term_amount: Decimal) \
        -> None:
    exch = ExchangeRate(unit_currency, unit_multiple, term_currency,
                        term_amount)
    inv_exch = exch.inverted()
    assert inv_exch.unit_currency == term_currency
    assert inv_exch.term_currency == unit_currency
    assert inv_exch.rate == Decimal(unit_multiple / term_amount, 6)


@pytest.mark.parametrize(("exch_rate", "amnt"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           Decimal("335.04")),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("1.09827")),
                           Decimal("12033.20")),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_mny_ok(exch_rate: ExchangeRate, amnt: Decimal) -> None:
    unit_curr = exch_rate.unit_currency
    term_curr = exch_rate.term_currency
    quantum = term_curr.smallest_fraction
    res = exch_rate * (amnt * unit_curr)
    assert isinstance(res, Money)
    assert res.unit == term_curr
    assert res.amount == (amnt * exch_rate.rate).quantize(quantum)


@pytest.mark.parametrize("curr", [USD, HKD], ids=lambda p: str(p))
@pytest.mark.parametrize(("exch_rate", "amnt"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           Decimal("335.04")),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("1.09827")),
                           Decimal("12033.20")),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_mny_wrong_curr(exch_rate: ExchangeRate, amnt: Decimal,
                                      curr: Currency) -> None:
    with pytest.raises(ValueError):
        _ = Money(amnt, curr) * exch_rate


@pytest.mark.parametrize(("exch_rate", "price", "res_unit"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           Decimal("335.04") * EURpKg, USDpKg),
                          (ExchangeRate(HKD, Decimal("100"), TND,
                                        Decimal("10.9827")),
                           Decimal("12033.20") * HKDpKg, TNDpKg),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_mny_per_qty_ok(exch_rate: ExchangeRate,
                                      price: PricePerMass,
                                      res_unit: Unit) -> None:
    res = exch_rate * price
    assert isinstance(res, PricePerMass)
    assert res.unit == res_unit
    assert res.amount == price.amount * exch_rate.rate


@pytest.mark.parametrize(("exch_rate", "price"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           Decimal("335.04") * USDpKg),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("1.09827")),
                           Decimal("12033.20") * HKDpKg),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_mny_per_qty_wrong_curr(exch_rate: ExchangeRate,
                                              price: PricePerMass) -> None:
    with pytest.raises(QuantityError):
        _ = price * exch_rate


# noinspection DuplicatedCode
@pytest.mark.parametrize(("exch_rate_1", "exch_rate_2"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           ExchangeRate(USD, ONE, TND, Decimal("335.04"))),
                          (ExchangeRate(HKD, Decimal("100"), TND,
                                        Decimal("10.9827")),
                           ExchangeRate(ZWL, Decimal(1000), HKD,
                                        Decimal("120.33205"))),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_triangl_mul_ok(exch_rate_1: ExchangeRate,
                                  exch_rate_2: ExchangeRate) -> None:
    res = exch_rate_1 * exch_rate_2
    assert isinstance(res, ExchangeRate)
    if exch_rate_1.term_currency == exch_rate_2.unit_currency:
        assert res.unit_currency == exch_rate_1.unit_currency
        assert res.term_currency == exch_rate_2.term_currency
    else:
        assert res.unit_currency == exch_rate_2.unit_currency
        assert res.term_currency == exch_rate_1.term_currency
    assert isinstance(exch_rate_1.rate, Decimal)
    assert isinstance(exch_rate_2.rate, Decimal)
    rate: Decimal = exch_rate_1.rate * exch_rate_2.rate
    multiple = Decimal(10) ** -min(0, rate.magnitude + 1)
    assert res._unit_multiple == multiple
    assert res._term_amount == Decimal(rate * multiple, 6)


@pytest.mark.parametrize(("exch_rate_1", "exch_rate_2"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.0482"))),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("10.9827")),
                           ExchangeRate(ZWL, Decimal(1000), HKD,
                                        Decimal("120.33205"))),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_triangl_mul_wrong_curr(exch_rate_1: ExchangeRate,
                                          exch_rate_2: ExchangeRate) \
        -> None:
    with pytest.raises(ValueError):
        _ = exch_rate_1 * exch_rate_2


@pytest.mark.parametrize(("exch_rate", "other"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           USD),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("10.9827")),
                           Decimal("120.33205")),
                          (ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.0482")),
                           Mass),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_wrong_type(exch_rate: ExchangeRate, other: Any) \
        -> None:
    with pytest.raises(TypeError):
        _ = exch_rate * other


@pytest.mark.parametrize(("exch_rate", "qty"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           Decimal(7) * NEWTON),
                          (ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.0482")),
                           Mass(25)),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_mul_wrong_qty(exch_rate: ExchangeRate, qty: Quantity) \
        -> None:
    with pytest.raises(QuantityError):
        _ = exch_rate * qty


# noinspection DuplicatedCode
@pytest.mark.parametrize(("exch_rate_1", "exch_rate_2"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.070043")),
                           ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.104423"))),
                          (ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("11.082745")),
                           ExchangeRate(ZWL, Decimal(1000), HKD,
                                        Decimal("120.000005"))),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_triangl_div_ok(exch_rate_1: ExchangeRate,
                                  exch_rate_2: ExchangeRate) \
        -> None:
    res = exch_rate_1 / exch_rate_2
    assert isinstance(res, ExchangeRate)
    if exch_rate_1.unit_currency == exch_rate_2.unit_currency:
        assert res.unit_currency == exch_rate_2.term_currency
        assert res.term_currency == exch_rate_1.term_currency
    else:
        assert res.unit_currency == exch_rate_1.unit_currency
        assert res.term_currency == exch_rate_2.unit_currency
    assert isinstance(exch_rate_1.rate, Decimal)
    assert isinstance(exch_rate_2.rate, Decimal)
    rate: Decimal = Decimal(exch_rate_1.rate / exch_rate_2.rate, 30)
    multiple = Decimal(10) ** -min(0, rate.magnitude + 1)
    assert res._unit_multiple == multiple
    assert res._term_amount == Decimal(rate * multiple, 6)


@pytest.mark.parametrize(("exch_rate_1", "exch_rate_2"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.004827")),
                           ExchangeRate(USD, ONE, TND, Decimal("335.041702"))),
                          (ExchangeRate(HKD, Decimal("100"), TND,
                                        Decimal("11.0027")),
                           ExchangeRate(ZWL, Decimal(1000), HKD,
                                        Decimal("120.040205"))),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_triangl_div_wrong_curr(exch_rate_1: ExchangeRate,
                                          exch_rate_2: ExchangeRate) -> None:
    with pytest.raises(ValueError):
        _ = exch_rate_1 / exch_rate_2


@pytest.mark.parametrize(("exch_rate", "other"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                           EUR),
                          (ExchangeRate(ZWL, Decimal("1000"), TND,
                                        Decimal("109.008247")),
                           Decimal("120.322054")),
                          (ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.02")),
                           Mass),
                          (ExchangeRate(TND, Decimal("10"), USD,
                                        Decimal("0.302")),
                           Mass(17.5)),
                          ],
                         ids=lambda p: str(p))
def test_exch_rate_div_wrong_type(exch_rate: ExchangeRate, other: Any) \
        -> None:
    with pytest.raises(TypeError):
        _ = exch_rate / other


@pytest.mark.parametrize(("mny", "exch_rate"),
                         [(Decimal("335.04") * USD,
                           ExchangeRate(EUR, ONE, USD, Decimal("1.09827"))),
                          (Decimal("12033.20") * TND,
                           ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("1.09827"))),
                          ],
                         ids=lambda p: str(p))
def test_mny_div_exch_rate_ok(mny: Money, exch_rate: ExchangeRate) -> None:
    res = mny / exch_rate
    mult = exch_rate.unit_currency.quantum
    amnt = mny.amount * exch_rate.inverse_rate
    assert isinstance(res, Money)
    assert res.unit == exch_rate.unit_currency
    assert res.amount == Decimal(amnt, 9).quantize(mult)


@pytest.mark.parametrize("mny",
                         [Decimal("335.04") * EUR,
                          Decimal("12033.20") * HKD,
                          ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("exch_rate",
                         [ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                          ExchangeRate(ZWL, Decimal("100"), TND,
                                       Decimal("1.09827")),
                          ],
                         ids=lambda p: str(p))
def test_mny_div_exch_rate_wrong_curr(mny: Money, exch_rate: ExchangeRate) \
        -> None:
    with pytest.raises(ValueError):
        _ = mny / exch_rate


@pytest.mark.parametrize(("price", "exch_rate"),
                         [(Decimal("335.04") * USDpKg,
                           ExchangeRate(EUR, ONE, USD, Decimal("1.09827"))),
                          (Decimal("12033.20") * TNDpKg,
                           ExchangeRate(ZWL, Decimal("100"), TND,
                                        Decimal("1.09827"))),
                          ],
                         ids=lambda p: str(p))
def test_mny_per_qty_div_exch_rate_ok(price: PricePerMass,
                                      exch_rate: ExchangeRate) -> None:
    res = price / exch_rate
    amnt = price.amount / exch_rate.rate
    _, unit = exch_rate.unit_currency / KILOGRAM
    assert isinstance(res, PricePerMass)
    assert res.amount == amnt
    assert res.unit == unit


@pytest.mark.parametrize("price",
                         [Decimal("335.04") * EURpKg,
                          Decimal("12033.20") * HKDpKg,
                          ],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("exch_rate",
                         [ExchangeRate(EUR, ONE, USD, Decimal("1.09827")),
                          ExchangeRate(ZWL, Decimal("100"), TND,
                                       Decimal("1.09827")),
                          ],
                         ids=lambda p: str(p))
def test_mny_per_qty_div_exch_rate_wrong_curr(price: PricePerMass,
                                              exch_rate: ExchangeRate) \
        -> None:
    with pytest.raises(ValueError):
        _ = price / exch_rate


@pytest.mark.parametrize(("exch_rate", "qty"),
                         [(ExchangeRate(TND, Decimal("10"), USD,
                                        Decimal("0.302")),
                           Mass(17.5)),
                          ],
                         ids=lambda p: str(p))
def test_wrong_qty_div_exch_rate(exch_rate: ExchangeRate, qty: Quantity) \
        -> None:
    with pytest.raises(QuantityError):
        _ = qty / exch_rate


@pytest.mark.parametrize(("exch_rate", "other"),
                         [(ExchangeRate(EUR, ONE, USD, Decimal("1.0204")),
                           EUR),
                          (ExchangeRate(ZWL, Decimal("1000"), TND,
                                        Decimal("109.008247")),
                           Decimal("120.322054")),
                          (ExchangeRate(TND, Decimal("100"), USD,
                                        Decimal("3.02")),
                           Mass),
                          ],
                         ids=lambda p: str(p))
def test_wrong_type_div_exch_rate(exch_rate: ExchangeRate, other: Any) \
        -> None:
    with pytest.raises(TypeError):
        _ = other / exch_rate
