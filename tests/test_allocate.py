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

"""Test driver for Quantity.allocate."""
from fractions import Fraction
from numbers import Rational
from typing import Generator, List, Type, Union

import pytest
from decimalfp import (
    Decimal, ROUNDING, get_dflt_rounding_mode, set_dflt_rounding_mode,
    )

from quantity import IncompatibleUnitsError, Quantity
from quantity.predefined import GRAM, KILOGRAM, Mass


@pytest.fixture(scope="module")
def dflt_rounding() -> Generator[None, None, None]:
    rnd = get_dflt_rounding_mode()
    # noinspection PyTypeChecker
    set_dflt_rounding_mode(ROUNDING.ROUND_HALF_UP)
    yield
    set_dflt_rounding_mode(rnd)


def test_dflt_rounding(dflt_rounding: None) -> None:
    """Activate fixture to set default rounding"""
    pass


class Quantized(Quantity, ref_unit_symbol="q", quantum=Decimal("0.01")):
    pass


@pytest.mark.parametrize(("qty", "ratios", "portions"),
                         [
                             (24 * KILOGRAM, [3, 2, 1],
                              [12 * KILOGRAM, 8 * KILOGRAM, 4 * KILOGRAM]),
                             (Decimal(100) * GRAM,
                              [Fraction(1, 4), Fraction(1, 8), Fraction(1, 8),
                               Fraction(1, 2)],
                              [25 * GRAM, Decimal("12.5") * GRAM,
                               Decimal("12.5") * GRAM, 50 * GRAM]),
                             ],
                         ids=("int_ratios", "fractional_ratios"))
def test_alloc_no_rounding_error(qty: Mass, ratios: List[Rational],
                                 portions: List[Mass]) -> None:
    assert qty.allocate(ratios) == (portions, 0 * KILOGRAM)


@pytest.mark.parametrize(("qty", "ratios", "portions", "rounding_error"),
                         [(Quantized(Decimal(10)),
                           [3, 7, 5, 6, 81, 3, 7],
                           [Quantized(Decimal('0.27')),
                            Quantized(Decimal('0.63')),
                            Quantized(Decimal('0.45')),
                            Quantized(Decimal('0.54')),
                            Quantized(Decimal('7.23')),
                            Quantized(Decimal('0.27')),
                            Quantized(Decimal('0.63')),
                            ],
                           Quantized(Decimal('-0.02'))),
                          (Quantized(Decimal(10)),
                           [3, 7, 5, 6, 87, 3, 7],
                           [Quantized(Decimal('0.25')),
                            Quantized(Decimal('0.59')),
                            Quantized(Decimal('0.42')),
                            Quantized(Decimal('0.51')),
                            Quantized(Decimal('7.37')),
                            Quantized(Decimal('0.25')),
                            Quantized(Decimal('0.59')),
                            ],
                           Quantized(Decimal("0.02"))),
                          (Quantized(Decimal(1)),
                           [Mass(Decimal(24)),
                            Mass(Decimal(69)),
                            Mass(Decimal(5)),
                            ],
                           [Quantized(Decimal("0.24")),
                            Quantized(Decimal("0.70")),
                            Quantized(Decimal("0.05")),
                            ],
                           Quantized(Decimal("0.01")))
                          ],
                         ids=("int-ratios-neg_error", "int-ratios-pos_error",
                              "qty-ratios"))
def test_alloc_with_rounding_error(qty: Quantized,
                                   ratios: Union[List[Rational],
                                                 List[Quantity]],
                                   portions: List[Quantized],
                                   rounding_error: Quantized) -> None:
    assert qty.allocate(ratios, False) == (portions, rounding_error)


@pytest.mark.parametrize(("qty", "ratios", "portions", "rounding_error"),
                         [(Quantized(Decimal(10)),
                           [3, 7, 5, 6, 81, 3, 7],
                           [Quantized(Decimal('0.27')),
                            Quantized(Decimal('0.62')),
                            Quantized(Decimal('0.45')),
                            Quantized(Decimal('0.54')),
                            Quantized(Decimal('7.23')),
                            Quantized(Decimal('0.27')),
                            Quantized(Decimal('0.62')),
                            ],
                           Quantized(Decimal())),
                          (Quantized(Decimal(10)),
                           [3, 7, 5, 6, 87, 3, 7],
                           [Quantized(Decimal('0.26')),
                            Quantized(Decimal('0.59')),
                            Quantized(Decimal('0.42')),
                            Quantized(Decimal('0.51')),
                            Quantized(Decimal('7.37')),
                            Quantized(Decimal('0.26')),
                            Quantized(Decimal('0.59')),
                            ],
                           Quantized(Decimal())),
                          ],
                         ids=("int-ratios-neg_error", "int-ratios-pos_error"))
def test_alloc_disperse_rounding_error(qty: Quantized, ratios: List[Rational],
                                       portions: List[Quantized],
                                       rounding_error: Quantized) -> None:
    assert qty.allocate(ratios, True) == (portions, rounding_error)


@pytest.mark.parametrize(("qty", "ratios", "exc"),
                         [(Quantized(Decimal(1)),
                           [Quantized(Decimal(3)),
                            Quantized(Decimal(23)),
                            Quantized(Decimal(4)),
                            Decimal(8),
                            Quantized(Decimal(7)),
                            ],
                           TypeError),
                          (Quantized(Decimal(1)),
                           [Quantized(Decimal(3)),
                            Quantized(Decimal(23)),
                            Quantized(Decimal(4)),
                            Mass(Decimal(8)),
                            Quantized(Decimal(7)),
                            ],
                           IncompatibleUnitsError),
                          ],
                         ids=("mixed_quantity_and_non_quantity",
                              "mixed_different_quantity_types"))
def test_alloc_inconsistent_ratios(qty: Quantized,
                                   ratios: List[Union[Quantity, Rational]],
                                   exc: Type[Exception]) -> None:
    with pytest.raises(exc):
        _ = qty.allocate(ratios)
