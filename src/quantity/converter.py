# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        converter
# Purpose:     Provides classes used to convert quantities
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Provides classes used to convert quantities."""

# TODO: uncomment the following when compatibility for Python 3.6 is dropped
#       and replace forward references
# from __future__ import annotations

from typing import (
    Callable, Iterable, Mapping, Optional, TYPE_CHECKING, Tuple, Union, cast, )

from .exceptions import IncompatibleUnitsError

if TYPE_CHECKING:
    from . import Quantity, Rational, Unit

ConverterT = Callable[['Quantity', 'Unit'], Optional['Rational']]


class Converter:
    """Convert a quantity's amount to the equivalent amount for another unit.

    A quantity converter can be any callable with a signature like
    conv(qty, to_unit) -> number f so that type(qty)(f, to_unit) == qty.
    """

    def __call__(self, qty: 'Quantity', to_unit: 'Unit') \
            -> Optional['Rational']:
        """Convert a `qty`s amount to the equivalent amount for `to_unit`.

        Args:
            qty (sub-class of :class:`Quantity`): quantity to be converted
            to_unit (:class:`Unit`): unit for equivalent amount

        Returns:
            Optional[Rational]: factor f so that f * `to_unit` == `qty`,
                or None if no such factor is available

        Raises:
            IncompatibleUnitsError: `qty` and `to_unit` are incompatible
            UnitConversionError: conversion factor not available
        """
        if qty.unit is to_unit:  # same unit
            return qty.amount
        if qty.__class__ is to_unit.qty_cls:
            return self._get_factor(qty, to_unit)
        raise IncompatibleUnitsError(
            "Can't convert a '%s' unit to a '%s' unit.",
            qty.__class__, to_unit.qty_cls)

    def _get_factor(self, qty: 'Quantity', to_unit: 'Unit') \
            -> Optional['Rational']:
        """Return factor f so that f * `to_unit` == `qty`.

        Returns None if factor can't be determined.
        """
        return NotImplemented


ConvMapT = Mapping[Tuple['Unit', 'Unit'], Tuple['Rational', 'Rational']]
ConvSpecIterableT = Iterable[Tuple['Unit', 'Unit', 'Rational', 'Rational']]


class TableConverter(Converter):
    """Converter using a conversion table.

    Args:
        conv_table (Mapping or list): the mapping used to initialize the
            conversion table

    Each item of the conversion table defines a conversion from one unit to
    another unit and consists of four elements:

    * from_unit (:class:`Unit`): unit of the quantity to be converted

    * to_unit (:class:`Unit`): target unit of the conversion

    * factor (`Rational`): factor to be applied to the quantity's amount

    * offset (`Rational`): an amount added after applying the factor

    When a `Mapping` is given as `convTable`, each key / value pair must map a
    tuple (from_unit, to_unit) to a tuple (factor, offset).

    When a `list` is given as `convTable`, each item must be a tuple
    (from_unit, to_unit, factor, offset).

    `factor` and `offset` must be set so that for an amount in terms of
    `from_unit` the eqivalent amount in terms of `to_unit` is:

    result = amount * factor + offset

    An instance of `TableConverter` can be called with a :class:`Quantity`
    sub-class' instance `qty` and a :class:`Unit` sub-class' instance `to_unit`
    as parameters. It looks-up the pair (`qty.unit`, `to_unit`) for a factor
    and an offset and returns the resulting amount according to the formula
    given above.

    If there is no item for the pair (`qty.unit`, `to_unit`), it tries to find
    a reverse mapping by looking-up the pair (`to_unit`, `qty.unit`), and, if
    it finds one, it returns a result by applying a reversed formula:

    result = (amount - offset) / factor

    That means, for each pair of units it is sufficient to define a conversion
    in one direction.

    An instance of `TableConverter` can be directly registered as a converter
    by calling the method :meth:`Unit.register_converter`.
    """

    def __init__(self, conv_table: Union[ConvMapT, ConvSpecIterableT]):
        self._unit_map: ConvMapT
        if isinstance(conv_table, Mapping):
            conv_table = cast(ConvMapT, conv_table)
            self._unit_map = conv_table
        elif isinstance(conv_table, Iterable):
            conv_table = cast(ConvSpecIterableT, conv_table)
            unit_map = self._unit_map = {}
            for (from_unit, to_unit, factor, offset) in conv_table:
                unit_map[(from_unit, to_unit)] = (factor, offset)
        else:
            raise TypeError("A Mapping or list must be given.")

    def _get_factor(self, qty: 'Quantity', to_unit: 'Unit') \
            -> Optional['Rational']:
        """Return factor f so that f * `to_unit` == `qty`.

        Returns None if factor can't be determined.
        """
        try:
            factor, offset = self._unit_map[(qty.unit, to_unit)]
        except KeyError:
            # try reverse
            try:
                factor, offset = self._unit_map[(to_unit, qty.unit)]
            except KeyError:
                return None
            else:
                return (qty.amount - offset) / factor
        else:
            return factor * qty.amount + offset
