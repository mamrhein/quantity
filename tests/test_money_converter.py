# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright:   (c) 2021 ff. Michael Amrhein (michael@adrhinum.de)
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$

"""Test driver for MoneyConverter."""

from datetime import date, timedelta
from numbers import Rational
from typing import Generator, List, Tuple, Union

import pytest
from decimalfp import Decimal, ONE

from quantity import UnitConversionError
from quantity.money import Currency, Money, MoneyConverter

# constants
EUR = Money.register_currency("EUR")
HKD = Money.register_currency("HKD")
TND = Money.register_currency("TND")
USD = Money.register_currency("USD")
TODAY = date.today()

# types
RateListT = List[Tuple[Currency, Decimal, Rational]]
PeriodT = Union[None, int, Tuple[int, int], date]


# helper functions

def _gen_rates() -> Generator[Tuple[date, RateListT], None, None]:
    this_year = TODAY.year
    prev_year = this_year - 1
    this_month = TODAY.month
    for day in (1, 2):
        for month in (1, 2, this_month):
            for year in (prev_year, this_year):
                dt = date(year, month, day)
                rate = Decimal("%i.%02i%i" % (day, month, year))
                yield (dt, [(USD, rate, ONE),
                            (HKD, Decimal(2) * rate, ONE)])
    year, month, day = TODAY.timetuple()[:3]
    rate = Decimal("%i.%02i%i" % (day, month, year))
    yield (TODAY, [(USD, rate, ONE),
                   (HKD, Decimal(2) * rate, ONE)])


# setup converters

def money_converters() -> Tuple[MoneyConverter, ...]:
    constant_rates = [(USD, Decimal('1.2'), ONE),
                      (HKD, Decimal('8.5'), ONE)]
    constant_rates_conv = MoneyConverter(EUR)
    constant_rates_conv.update(None, constant_rates)
    daily_rates = list(_gen_rates())
    daily_rate_conv = MoneyConverter(EUR)
    for dt, rates in daily_rates:
        daily_rate_conv.update(dt, rates)
    monthly_rates = [((dt.year, dt.month), rates)
                     for dt, rates in daily_rates
                     if dt.day == 1]
    monthly_rate_conv = MoneyConverter(EUR)
    for period, rates in monthly_rates:
        monthly_rate_conv.update(period, rates)
    yearly_rates = [(year, rates)
                    for (year, month), rates in monthly_rates
                    if month == 1]
    yearly_rate_conv = MoneyConverter(EUR)
    for year, rates in yearly_rates:
        yearly_rate_conv.update(year, rates)
    return (constant_rates_conv, daily_rate_conv, monthly_rate_conv,
            yearly_rate_conv)


CONSTANT, DAILY, MONTHLY, YEARLY = money_converters()


# tests

@pytest.mark.parametrize("other_period",
                         [None, TODAY.year, (TODAY.year, TODAY.month), TODAY],
                         ids=lambda p: str(p))
@pytest.mark.parametrize("period",
                         [None, TODAY.year, (TODAY.year, TODAY.month), TODAY],
                         ids=lambda p: str(p))
def test_conv_update(period: PeriodT, other_period: PeriodT) -> None:
    rates = [(USD, Decimal('1.2'), ONE),
             (HKD, Decimal('8.5'), ONE)]
    conv = MoneyConverter(EUR)
    conv.update(period, rates)
    assert conv._type_of_validity is type(period)
    if period != other_period:
        with pytest.raises(ValueError):
            conv.update(other_period, rates)


@pytest.mark.parametrize("effective_date",
                         [date.today(), date.today() - timedelta(days=1)],
                         ids=("today", "yesterday"))
def test_conv_dflt_effective_date(effective_date: date) -> None:
    the_day_before = effective_date - timedelta(days=1)
    rates = [(USD, Decimal('1.2'), ONE),
             (HKD, Decimal('8.5'), ONE)]
    conv = MoneyConverter(EUR, get_dflt_effective_date=lambda: effective_date)
    conv.update(effective_date, rates)
    assert conv.get_rate(EUR, USD) == conv.get_rate(EUR, USD, effective_date)
    assert conv.get_rate(EUR, USD, the_day_before) is None
    # other default effective date
    conv = MoneyConverter(EUR, get_dflt_effective_date=lambda: the_day_before)
    conv.update(the_day_before, rates)
    assert conv.get_rate(EUR, USD) == conv.get_rate(EUR, USD, the_day_before)
    assert conv.get_rate(EUR, USD, effective_date) is None


# noinspection PyPep8Naming
def test_constant_conv() -> None:
    conv = CONSTANT
    assert conv.base_currency == EUR
    EUR2USD = conv.get_rate(EUR, USD, date.today())
    assert EUR2USD.quotation == (EUR, USD, Decimal('1.2'))
    HKD2EUR = conv.get_rate(HKD, EUR)
    assert HKD2EUR == conv.get_rate(EUR, HKD).inverted()
    HKD2USD = conv.get_rate(HKD, USD, date(2004, 12, 17))
    assert HKD2USD == conv.get_rate(EUR, USD) / conv.get_rate(EUR, HKD)
    ZWL2EUR = conv.get_rate(TND, EUR)
    assert ZWL2EUR is None


# noinspection PyPep8Naming
def test_daily_conv() -> None:
    today = date.today()
    year, month, day = today.timetuple()[:3]
    conv = DAILY
    assert conv.base_currency == EUR
    EUR2USD = conv.get_rate(EUR, USD)
    assert EUR2USD.rate == Decimal(f"{day}.{month:02d}{year}")
    EUR2USD = conv.get_rate(EUR, USD, date(year, 1, 1))
    assert EUR2USD.rate == Decimal(f"1.01{year}")
    EUR2HKD = conv.get_rate(EUR, HKD, date(year - 1, 2, 2))
    assert EUR2HKD.rate == 2 * Decimal(f"2.02{year - 1}")
    if day <= 3:
        ref_date = date(year, month, 4)
    else:
        ref_date = date(year, month, day - 1)
    EUR2HKD = conv.get_rate(EUR, HKD, ref_date)
    assert EUR2HKD is None


# noinspection PyPep8Naming
def test_monthly_conv() -> None:
    today = date.today()
    year, month, day = today.timetuple()[:3]
    conv = MONTHLY
    assert conv.base_currency == EUR
    EUR2USD = conv.get_rate(EUR, USD)
    assert EUR2USD.rate == Decimal(f"1.{month:02d}{year}")
    EUR2USD = conv.get_rate(EUR, USD, date(year, 1, 17))
    assert EUR2USD.rate == Decimal(f"1.01{year}")
    EUR2HKD = conv.get_rate(EUR, HKD, date(year - 1, 2, 24))
    assert EUR2HKD.rate == 2 * Decimal(f"1.02{year - 1}")
    if month <= 3:
        ref_date = date(year, 4, 14)
    else:
        ref_date = date(year, month - 1, 14)
    EUR2HKD = conv.get_rate(EUR, HKD, ref_date)
    assert EUR2HKD is None


# noinspection PyPep8Naming
def test_yearly_conv() -> None:
    today = date.today()
    year, month, day = today.timetuple()[:3]
    conv = YEARLY
    assert conv.base_currency == EUR
    EUR2USD = conv.get_rate(EUR, USD)
    assert EUR2USD.rate == Decimal(f"1.01{year}")
    EUR2USD = conv.get_rate(EUR, USD, date(year, 11, 17))
    assert EUR2USD.rate == Decimal(f"1.01{year}")
    EUR2HKD = conv.get_rate(EUR, HKD, date(year - 1, 2, 24))
    assert EUR2HKD.rate == 2 * Decimal(f"1.01{year - 1}")
    EUR2HKD = conv.get_rate(EUR, HKD, date(year - 2, 1, 1))
    assert EUR2HKD is None


def test_registration() -> None:
    # assert that there are no registered money converters yet
    assert not list(Money.registered_converters())
    Money.register_converter(CONSTANT)
    assert list(Money.registered_converters()) == [CONSTANT]
    Money.register_converter(MONTHLY)
    assert list(Money.registered_converters()) == [MONTHLY, CONSTANT]
    with pytest.raises(ValueError):
        Money.remove_converter(YEARLY)
    with pytest.raises(ValueError):
        Money.remove_converter(CONSTANT)
    Money.register_converter(MONTHLY)
    assert list(Money.registered_converters()) == [MONTHLY, MONTHLY, CONSTANT]
    Money.remove_converter(MONTHLY)
    assert list(Money.registered_converters()) == [MONTHLY, CONSTANT]
    Money.remove_converter(MONTHLY)
    assert list(Money.registered_converters()) == [CONSTANT]
    with CONSTANT as conv1:
        assert list(Money.registered_converters()) == [conv1, CONSTANT]
        with YEARLY as conv2:
            assert conv2 is YEARLY
            assert list(Money.registered_converters()) == [conv2, conv1,
                                                           CONSTANT]
        assert list(Money.registered_converters()) == [conv1, CONSTANT]
    assert list(Money.registered_converters()) == [CONSTANT]
    Money.remove_converter(CONSTANT)
    assert not list(Money.registered_converters())


def test_conversion() -> None:
    today = date.today()
    year, month, day = today.timetuple()[:3]
    # assert that there are no registered money converters yet
    assert not list(Money.registered_converters())
    four_eur = 4 * EUR
    with pytest.raises(UnitConversionError):
        four_eur.convert(USD)
    with CONSTANT:
        assert four_eur.convert(USD) == Decimal('4.8') * USD
        with YEARLY:
            amnt = 4 * Decimal(f"1.01{year}")
            assert four_eur.convert(USD) == amnt * USD
            with MONTHLY:
                amnt = 4 * Decimal(f"1.{month:02d}{year}")
                assert four_eur.convert(USD) == amnt * USD
                with DAILY:
                    amnt = 4 * Decimal(f"{day}.{month:02d}{year}")
                    assert four_eur.convert(USD) == amnt * USD
                amnt = 4 * Decimal(f"1.{month:02d}{year}")
                assert four_eur.convert(USD) == amnt * USD
            amnt = 4 * Decimal(f"1.01{year}")
            assert four_eur.convert(USD) == amnt * USD
        assert four_eur.convert(USD) == Decimal('4.8') * USD
    # assert that there are no registered money converters yet
    assert not list(Money.registered_converters())
