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


"""Test constructors for Quantities and Units."""

from typing import Any, Tuple

import pytest
from decimalfp import Decimal

from quantity import Quantity, QuantityClsDefT, QuantityMeta, Unit, UnitDefT
from quantity.si_prefixes import KILO, MEGA, SIPrefix, SI_PREFIXES


@pytest.fixture(scope="session")
def qty_simple() -> QuantityMeta:
    return QuantityMeta("SimpleQty", (Quantity,), {})


@pytest.fixture(scope="session")
def qty_a() -> Tuple[str, str, QuantityMeta]:
    symbol, name = "#a", "1a"
    return symbol, name, QuantityMeta(symbol.upper(), (Quantity,), {},
                                      ref_unit_symbol=symbol,
                                      ref_unit_name=name)


# noinspection PyPep8Naming
@pytest.fixture(scope="session")
def qties_bcd() -> Tuple[QuantityMeta, ...]:
    B = QuantityMeta("B", (Quantity,), {}, ref_unit_symbol="#b")
    assert B.ref_unit is not None   # for mypy
    _ = B.new_unit(f"{KILO.abbr}{B.ref_unit.symbol}",
                   define_as=KILO * B.ref_unit)
    _ = B.new_unit(f"{MEGA.abbr}{B.ref_unit.symbol}",
                   define_as=MEGA * B.ref_unit)
    C = QuantityMeta("C", (Quantity,), {}, ref_unit_symbol="#c")
    assert C.ref_unit is not None   # for mypy
    _ = C.new_unit(f"{KILO.abbr}{C.ref_unit.symbol}",
                   define_as=KILO * C.ref_unit)
    D = QuantityMeta("D", (Quantity,), {}, ref_unit_symbol="#d")
    assert D.ref_unit is not None   # for mypy
    _ = D.new_unit(f"{KILO.abbr}{D.ref_unit.symbol}",
                   define_as=KILO * D.ref_unit)
    return B, C, D


@pytest.fixture(scope="session",
                params=[
                    ("BC", lambda b, c, d: b * c),
                    ("C_D", lambda b, c, d: c / d),
                    ("B2_D3", lambda b, c, d: b ** 2 * d ** 3),
                    ("BC2_D", lambda b, c, d: b * c ** 2 / d)],
                ids=lambda t: str(t[0]))
def qty_name_n_def(request: Any,
                   qties_bcd: Tuple[QuantityMeta, QuantityMeta, QuantityMeta])\
        -> Tuple[str, QuantityClsDefT]:
    # noinspection PyPep8Naming
    B, C, D = qties_bcd     # noqa: N806
    name, func = request.param
    return name, func(B, C, D)


def test_simple_base_qty(qty_simple: QuantityMeta) -> None:
    # noinspection PyPep8Naming
    Q = qty_simple
    assert Q.definition == QuantityClsDefT([(Q, 1)])
    assert Q.normalized_definition == Q.definition
    with pytest.raises(AttributeError):
        # noinspection PyUnresolvedReferences
        _ = Q.define_as     # type: ignore[attr-defined]
    assert Q.ref_unit is None
    assert Q.is_base_cls()
    assert not Q.is_derived_cls()


def test_base_qty_with_ref_unit(qty_a: Tuple[str, str, QuantityMeta]) -> None:
    # noinspection PyPep8Naming
    symbol, name, A = qty_a  # noqa: N806
    assert isinstance(A.ref_unit, Unit)
    with pytest.raises(AttributeError):
        # noinspection PyUnresolvedReferences
        _ = A.ref_unit_name     # type: ignore[attr-defined]
        # noinspection PyUnresolvedReferences
        _ = A.ref_unit_symbol   # type: ignore[attr-defined]
    assert A.quantum is None
    unit = A.ref_unit
    assert unit.symbol == symbol
    assert unit.name == name
    assert unit.qty_cls is A
    assert unit.is_base_unit()
    assert not unit.is_derived_unit()
    assert unit.is_ref_unit()


# noinspection PyPep8Naming
def test_simple_derived_qty(qty_a: Tuple[str, str, QuantityMeta]) -> None:
    symbol, name, A = qty_a  # noqa: N806
    R = QuantityMeta("R", (Quantity,), {},  # noqa: N806
                     define_as=A ** 2, quantum=1)
    assert R.definition == QuantityClsDefT([(R, 1)])
    assert R.normalized_definition == QuantityClsDefT([(A, 2)])
    assert not R.is_base_cls()
    assert R.is_derived_cls()
    assert R.quantum == 1
    unit = R.ref_unit
    assert isinstance(unit, Unit)
    assert A.ref_unit is not None   # for mypy
    assert unit.symbol == unit.name == A.ref_unit.symbol + "²"
    assert unit.definition == UnitDefT(((A.ref_unit, 2),))


def test_cmplx_derived_qty(qty_name_n_def: Tuple[str, QuantityClsDefT]) \
        -> None:
    name, qty_def = qty_name_n_def
    # noinspection PyPep8Naming
    Q = QuantityMeta(name, (Quantity,), {}, define_as=qty_def)  # noqa: N806
    assert Q.definition == qty_def
    norm_qty_def = qty_def.normalized()
    assert Q.normalized_definition == norm_qty_def
    assert not Q.is_base_cls()
    assert Q.is_derived_cls()
    assert Q.quantum is None
    unit = Q.ref_unit
    ref_unit_def = UnitDefT(((elem.ref_unit, exp)       # type: ignore
                             for (elem, exp) in norm_qty_def))
    assert isinstance(unit, Unit)
    assert unit.definition == ref_unit_def
    assert unit.symbol == unit.name == str(ref_unit_def)


# noinspection PyPep8Naming
def test_cls_already_registered(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    with pytest.raises(ValueError):
        _ = QuantityMeta("_", (Quantity,), {}, define_as=B.definition)
    _ = QuantityMeta("B2_DC", (Quantity,), {}, define_as=B ** 2 / (D * C))
    with pytest.raises(ValueError):
        _ = QuantityMeta("_", (Quantity,), {}, define_as=B ** 2 / (C * D))


def test_quantum_without_ref_unit() -> None:
    with pytest.raises(AssertionError):
        _ = QuantityMeta("X", (Quantity,), {}, quantum=1)


def test_unknown_keyword() -> None:
    with pytest.raises(AssertionError):
        _ = QuantityMeta("X", (Quantity,), {}, definition="foo")


@pytest.mark.parametrize(("symbol", "name"),
                         [
                             ("@sqa", "sqa_name"),
                             ("@sqb", "sqb_name"),
                             ("@sqc", "sqc_name"),
                             ],
                         ids=("sqa", "sqb", "sqc"))
def test_simple_qty_units(qty_simple: QuantityMeta, symbol: str, name: str) \
        -> None:
    # noinspection PyPep8Naming
    Q = qty_simple  # noqa: N806
    unit = Q.new_unit(symbol, name)
    assert isinstance(unit, Unit)
    assert unit.qty_cls is Q
    assert unit in Q.units()
    assert unit._definition is None
    assert unit.definition == UnitDefT(((unit, 1),))
    assert unit.symbol == symbol
    assert unit.name == name
    with pytest.raises(ValueError):
        _ = Q.new_unit(symbol, name)


@pytest.mark.parametrize("prefix",
                         [p for p in SI_PREFIXES],
                         ids=[p.name for p in SI_PREFIXES])
def test_scaled_units(qty_a: Tuple[str, str, QuantityMeta], prefix: SIPrefix) \
        -> None:
    # noinspection PyPep8Naming
    _, _, Q = qty_a  # noqa: N806
    assert Q.ref_unit is not None   # for mypy
    ref_unit = Q.ref_unit
    symbol = f"{prefix.abbr}{ref_unit.symbol}"
    name = f"{prefix.name} {ref_unit.name}"
    factor = prefix.factor
    unit = Q.new_unit(symbol, name, define_as=prefix * ref_unit)
    assert isinstance(unit, Unit)
    assert unit.qty_cls is Q
    assert unit in Q.units()
    assert unit.definition == UnitDefT([(factor, 1), (ref_unit, 1)])
    assert unit.symbol == symbol
    assert unit.name == name
    assert unit._equiv == factor
    assert not unit.is_ref_unit()
    assert not unit.is_base_unit()
    assert unit.is_derived_unit()


# noinspection PyPep8Naming
def test_unit_map(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    assert len(B) == len(B.units())
    for unit in B.units():
        assert unit.symbol in B
        assert B[unit.symbol] is unit
    for symbol in B:
        assert B[symbol] in B.units()


# noinspection PyPep8Naming
def test_unit_already_registered(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    assert B.ref_unit is not None   # for mypy
    with pytest.raises(ValueError):
        B.new_unit(B.ref_unit.symbol, B.ref_unit.name)
    Q = QuantityMeta("BDC", (Quantity,), {}, define_as=B * D * C)  # noqa: N806
    assert Q.ref_unit is not None
    Q.new_unit("kbdc", "kbdc", define_as=Decimal(1000) * Q.ref_unit)
    with pytest.raises(ValueError):
        Q.new_unit("kbdc", "kbdc")


# noinspection PyPep8Naming
def test_derived_units(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    Q = QuantityMeta("C2_BD", (Quantity,), {},      # noqa: N806
                     define_as=C ** 2 / (B * D))
    assert Q.ref_unit is not None
    for b_unit in B.units():
        for c_unit in C.units():
            for d_unit in D.units():
                symbol = f"{c_unit.symbol}2{b_unit.symbol}{d_unit.symbol}"
                unit = Q.new_unit(symbol,
                                  derive_from=(c_unit, b_unit, d_unit))
                assert isinstance(unit, Unit)
                assert unit.qty_cls is Q
                assert unit in Q.units()
                assert unit.symbol == symbol
                assert symbol in Q
                assert Q[symbol] is unit
                assert not unit.is_ref_unit()
                assert not unit.is_base_unit()
                assert unit.is_derived_unit()


# noinspection PyPep8Naming
def test_new_unit_wrong_qty(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    qty = 1 * C.units()[1]
    with pytest.raises(TypeError):
        B.new_unit('x', define_as=qty)


# noinspection PyPep8Naming
def test_new_unit_wrong_term(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    with pytest.raises(ValueError):
        B.new_unit('x', define_as=D.definition)     # type: ignore
    with pytest.raises(ValueError):
        B.new_unit('x', define_as=C.units()[1].definition)


# noinspection PyPep8Naming
def test_new_unit_wrong_type(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    with pytest.raises(TypeError):
        B.new_unit('x', define_as=D)    # type: ignore


# noinspection PyPep8Naming
def test_derive_unit_fails_on_base_qty(qties_bcd: Tuple[QuantityMeta, ...]) \
        -> None:
    B, C, D = qties_bcd  # noqa: N806
    with pytest.raises(TypeError):
        B.new_unit('x', derive_from=B.units()[1])


# noinspection PyPep8Naming
def test_define_and_derive_fails(qties_bcd: Tuple[QuantityMeta, ...]) -> None:
    B, C, D = qties_bcd  # noqa: N806
    Q = QuantityMeta("D_C", (Quantity,), {},      # noqa: N806
                     define_as=D / C)
    assert Q.ref_unit is not None   # for mypy
    with pytest.raises(ValueError):
        Q.new_unit('x', define_as=10 * Q.ref_unit, derive_from=Q.ref_unit)


# noinspection PyPep8Naming
def test_derive_unit_mismatched_units(qties_bcd: Tuple[QuantityMeta, ...]) \
        -> None:
    B, C, D = qties_bcd  # noqa: N806
    assert B.ref_unit is not None   # for mypy
    assert C.ref_unit is not None   # for mypy
    assert D.ref_unit is not None   # for mypy
    Q = QuantityMeta("B2C_D", (Quantity,), {},      # noqa: N806
                     define_as=B ** 2 * C / D)
    assert Q.ref_unit is not None   # for mypy
    with pytest.raises(ValueError):
        Q.new_unit('x', derive_from=(C.ref_unit, B.ref_unit, D.units()[1]))
