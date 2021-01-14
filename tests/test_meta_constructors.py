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
from typing import Tuple

# Third-party imports
import pytest

# Local imports
from quantity import Quantity, QuantityClsDefT, QuantityMeta, Unit, UnitDefT
from quantity.si_prefixes import SI_PREFIXES, SIPrefix


@pytest.fixture(scope="session")
def qty_simple() -> QuantityMeta:
    return QuantityMeta("SimpleQty", (Quantity,), {})


@pytest.fixture(scope="session", params=[("a", "1a")])
def qty_a(request) -> Tuple[str, str, QuantityMeta]:
    symbol, name = request.param
    return symbol, name, QuantityMeta(symbol.upper(), (Quantity,), {},
                                      ref_unit_symbol=symbol,
                                      ref_unit_name=name)


@pytest.fixture(scope="session")
def qties_bcd() -> Tuple[QuantityMeta, ...]:
    return tuple(QuantityMeta(name, (Quantity,), {},
                              ref_unit_symbol=name.lower())
                 for name in ("B", "C", "D"))


@pytest.fixture(scope="session",
                params=[
                    ("BC", lambda b, c, d: b * c),
                    ("C_D", lambda b, c, d: c / d),
                    ("B2_D3", lambda b, c, d: b ** 2 * d ** 3),
                    ("BC2_D", lambda b, c, d: b * c ** 2 / d)],
                ids=lambda t: t[0])
def qty_name_n_def(request, qties_bcd) -> Tuple[str, QuantityClsDefT]:
    # noinspection PyPep8Naming
    B, C, D = qties_bcd
    name, func = request.param
    return name, func(B, C, D)


def test_simple_base_qty(qty_simple) -> None:
    # noinspection PyPep8Naming
    Q = qty_simple
    assert Q.definition == QuantityClsDefT([(Q, 1)])
    assert Q.normalized_definition == Q.definition
    with pytest.raises(AttributeError):
        _ = Q.define_as
    assert Q.ref_unit is None
    assert Q.is_base_cls()
    assert not Q.is_derived_cls()


def test_base_qty_with_ref_unit(qty_a) -> None:
    # noinspection PyPep8Naming
    symbol, name, A = qty_a
    assert isinstance(A.ref_unit, Unit)
    with pytest.raises(AttributeError):
        _ = A.ref_unit_name
        _ = A.ref_unit_symbol
    unit = A.ref_unit
    assert unit.symbol == symbol
    assert unit.name == name
    assert unit.qty_cls is A
    assert unit.is_base_unit()
    assert not unit.is_derived_unit()
    assert unit.is_ref_unit()


# noinspection PyPep8Naming
def test_simple_derived_qty(qty_a) -> None:
    symbol, name, A = qty_a
    R = QuantityMeta("R", (Quantity,), {}, define_as=A ** 2)
    assert R.definition == QuantityClsDefT([(R, 1)])
    assert R.normalized_definition == QuantityClsDefT([(A, 2)])
    assert not R.is_base_cls()
    assert R.is_derived_cls()
    unit = R.ref_unit
    assert isinstance(unit, Unit)
    assert unit.symbol == unit.name == A.ref_unit.symbol + "²"
    assert unit.definition == UnitDefT(((A.ref_unit, 2),))


def test_cmplx_derived_qty(qty_name_n_def) -> None:
    name, qty_def = qty_name_n_def
    # noinspection PyPep8Naming
    Q = QuantityMeta(name, (Quantity,), {}, define_as=qty_def)
    assert Q.definition == qty_def
    norm_qty_def = qty_def.normalized()
    assert Q.normalized_definition == norm_qty_def
    assert not Q.is_base_cls()
    assert Q.is_derived_cls()
    unit = Q.ref_unit
    ref_unit_def = UnitDefT(((elem.ref_unit, exp)
                             for (elem, exp) in norm_qty_def))
    assert isinstance(unit, Unit)
    assert unit.definition == ref_unit_def
    assert unit.symbol == unit.name == str(ref_unit_def)


@pytest.mark.parametrize(("symbol", "name"),
                         [
                             ("sqa", "sqa_name"),
                             ("sqb", "sqb_name"),
                             ("sqc", "sqc_name"),
                         ],
                         ids=lambda t: t[0])
def test_simple_qty_units(qty_simple, symbol, name) -> None:
    # noinspection PyPep8Naming
    Q = qty_simple
    unit = Q.new_unit(symbol, name)
    assert isinstance(unit, Unit)
    assert unit.qty_cls is Q
    assert unit in Q.units()
    assert not hasattr(unit, '_definition')
    assert unit.symbol == symbol
    assert unit.name == name


@pytest.mark.parametrize("prefix",
                         [p for p in SI_PREFIXES],
                         ids=[p.name for p in SI_PREFIXES])
def test_scaled_units(qty_a, prefix: SIPrefix) -> None:
    # noinspection PyPep8Naming
    _, _, Q = qty_a
    ref_unit = Q.ref_unit
    symbol = f"{prefix.abbr}{ref_unit.symbol}"
    name = f"{prefix.name} {ref_unit.name}"
    factor = prefix.factor
    unit_def = factor * ref_unit
    unit = Q.new_unit(symbol, name, define_as=unit_def)
    assert isinstance(unit, Unit)
    assert unit.qty_cls is Q
    assert unit in Q.units()
    assert unit.definition == UnitDefT([(factor, 1), (ref_unit, 1)])
    assert unit.symbol == symbol
    assert unit.name == name
    assert unit._equiv == factor