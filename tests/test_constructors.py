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


"""Test constructors for Quantities and Units."""

# Standard library imports
from typing import Any

# Third-party imports
import pytest
from decimalfp import Decimal

# Local imports
from quantity import Quantity, QuantityMeta, Term, Unit


@pytest.fixture(scope="session")
def qty_simple_base() -> Any:
    return QuantityMeta("SimpleQty", (Quantity,), {})


@pytest.fixture(scope="session", params=[("q1", "q1unit")])
def qty_base_with_ref_unit1(request) -> Any:
    symbol, name = request.param
    return symbol, name, QuantityMeta("Qty1", (Quantity,), {},
                                      ref_unit_symbol=symbol,
                                      ref_unit_name=name)


def test_simple_base_qty(qty_simple_base) -> None:
    # noinspection PyPep8Naming
    Qty = qty_simple_base
    assert Qty.definition == Term([(Qty, 1)])
    assert Qty.normalized_definition == Qty.definition
    with pytest.raises(AttributeError):
        _ = Qty.define_as
    assert Qty.ref_unit is None
    assert Qty.is_base_cls()
    assert not Qty.is_derived_cls()


def test_base_qty_with_ref_unit(qty_base_with_ref_unit1) -> None:
    # noinspection PyPep8Naming
    symbol, name, Qty = qty_base_with_ref_unit1
    assert isinstance(Qty.ref_unit, Unit)
    with pytest.raises(AttributeError):
        _ = Qty.ref_unit_name
        _ = Qty.ref_unit_symbol
    unit = Qty.ref_unit
    assert unit.symbol == symbol
    assert unit.name == name
    assert unit.qty_cls is Qty
    assert unit.is_base_unit()
    assert not unit.is_derived_unit()
    assert unit.is_ref_unit()


# noinspection PyPep8Naming
def test_simple_derived_qty(qty_base_with_ref_unit1) -> None:
    symbol, name, Qty1 = qty_base_with_ref_unit1
    Qty2 = QuantityMeta("Qty2", (Quantity,), {}, define_as=Qty1 ** 2)
    assert Qty2.definition == Term([(Qty2, 1)])
    assert Qty2.normalized_definition == Term([(Qty1, 2)])
    assert not Qty2.is_base_cls()
    assert Qty2.is_derived_cls()
    unit = Qty2.ref_unit
    assert isinstance(unit, Unit)
    assert unit.symbol == unit.name == "q1²"
    assert unit.definition == Term(((Qty1.ref_unit, 2),))
