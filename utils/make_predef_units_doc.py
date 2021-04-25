# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright:   (c) 2012 ff. Michael Amrhein (michael@adrhinum.de)
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$

"""Utility used to create the doc of the predefined quantities."""

from numbers import Rational
from typing import Union

# noinspection PyProtectedMember
from quantity import Quantity, QuantityMeta, Unit
from quantity.predefined import *


COLWIDTH = (6, 25, 20, 20)


# noinspection PyMissingOrEmptyDocstring
def print_header(cls: QuantityMeta) -> None:
    name = cls.__name__
    print()
    print(name)
    print('^' * len(name))
    if cls.is_derived_cls():
        print()
        print("Definition: %s" % cls.definition)


# noinspection PyMissingOrEmptyDocstring
def print_ref_unit(ref_unit: Unit) -> None:
    symbol = ref_unit.symbol
    equiv = ''
    unit_def = str(ref_unit.definition)
    if unit_def != symbol:
        equiv = f" = '{unit_def}'"
    unit_norm_def = str(ref_unit.definition.normalized())
    if unit_norm_def != unit_def:
        equiv += f" = '{unit_norm_def}'"
    print()
    print(f"Reference unit: {ref_unit.name} ('{symbol}'{equiv})")


# noinspection PyMissingOrEmptyDocstring
def print_col_marker() -> None:
    print("=" * COLWIDTH[0],
          "=" * COLWIDTH[1],
          "=" * COLWIDTH[2],
          "=" * COLWIDTH[3])


# noinspection PyMissingOrEmptyDocstring
def print_unit_list_header(sym: str) -> None:
    print()
    print("Predefined units:")
    print()
    print_col_marker()
    print(format("Symbol", '<%i' % COLWIDTH[0]),
          format("Name", '<%i' % COLWIDTH[1]),
          format("Definition", '<%i' % COLWIDTH[2]),
          format("Equivalent in '%s'" % sym, '<%i' % (COLWIDTH[3])))
    print_col_marker()


# noinspection PyMissingOrEmptyDocstring
def print_unit_line(unit: Unit, equiv: Union[Rational, str]) -> None:
    print(format(unit.symbol, '<%i' % COLWIDTH[0]),
          format(unit.name, '<%i' % COLWIDTH[1]),
          format(str(unit.definition), '<%i' % COLWIDTH[2]),
          format(str(equiv), '<%i' % (COLWIDTH[3])))


# noinspection PyMissingOrEmptyDocstring
def print_unit_list_footer() -> None:
    print_col_marker()


localdict = dict(locals())
qty_cls_list = [cls for cls in localdict.values()
                if isinstance(cls, type) and issubclass(cls, Quantity)
                and cls.__name__ != 'Quantity']

for qty_cls in sorted(qty_cls_list, key=lambda cls: cls.norm_sort_key()):
    print_header(qty_cls)
    ref_unit = qty_cls.ref_unit
    if ref_unit:
        print_ref_unit(ref_unit)
        # noinspection PyProtectedMember
        unit_list = [unit for unit in sorted(qty_cls.units(),
                                             key=lambda unit: unit._equiv)
                     if unit is not ref_unit]
        if unit_list:
            print_unit_list_header(ref_unit.symbol)
            for unit in unit_list:
                # noinspection PyProtectedMember
                equiv = unit._equiv
                print_unit_line(unit, equiv)
            print_unit_list_footer()
    else:
        unit_list = [unit for unit in sorted(qty_cls.units(),
                                             key=lambda unit: unit.symbol)]
        if unit_list:
            print_unit_list_header('')
            for unit in unit_list:
                print_unit_line(unit, '')
            print_unit_list_footer()
