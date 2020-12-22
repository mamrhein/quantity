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

# Standard library imports
from numbers import Real
from typing import Iterable, Mapping, Optional, Tuple, TYPE_CHECKING, Union

# Third-party imports

# Local imports
from .exceptions import IncompatibleUnitsError, UnitConversionError

if TYPE_CHECKING:
    from . import Quantity, Unit


class Converter:

    """A quantity converter can be any callable with a signature like
    conv(qty, to_unit) -> number f so that type(qty)(f, to_unit) == qty."""

    def __call__(self, qty: 'Quantity', to_unit: 'Unit') -> Real:
        """Convert a quantity's amount to the equivalent amount for another
        unit.

        Args:
            qty (sub-class of :class:`Quantity`): quantity to be converted
            to_unit (:class:`Unit`): unit for equivalent amount

        Returns:
            Real: factor f so that f * to_unit == qty

        Raises:
            IncompatibleUnitsError: qty and to_unit are incompatible
            UnitConversionError: conversion factor not available
        """
        if qty.unit is to_unit:          # same unit
            return qty.amount
        if qty.Quantity is to_unit.Quantity:
            factor = self._get_factor(qty, to_unit)
            if factor is None:
                raise UnitConversionError(f"Can't convert '{qty.unit}' "
                                          f"to '{to_unit}'.")
            return factor
        raise IncompatibleUnitsError(f"Can't convert a '{qty.Quantity}' unit "
                                     f"to a '{to_unit.Quantity}' unit.")

    def _get_factor(self, qty: 'Quantity', to_unit: 'Unit') -> Optional[Real]:
        return NotImplemented


class RefUnitConverter(Converter):

    """Converter for Quantity classes that have a reference unit."""

    def _get_factor(self, qty: 'Quantity', to_unit: 'Unit') -> Optional[Real]:
        res_def = (qty.unit.normalizedDefinition /
                   to_unit.normalizedDefinition)
        return qty.amount * res_def.amount


class TableConverter(Converter):

    """Converter using a conversion table.

    Args:
        conv_table (Mapping or list): the mapping used to initialize the
            conversion table

    Each item of the conversion table defines a conversion from one unit to
    another unit and consists of four elements:

    * from_unit (:class:`Unit`): unit of the quantity to be converted

    * to_unit (:class:`Unit`): target unit of the conversion

    * factor (`Real`): factor to be applied to the quantity's amount

    * offset (`Real`): an amount added after applying the factor

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

    def __init__(self, conv_table: Union[Mapping[Tuple['Unit', 'Unit'],
                                                 Tuple[Real, Real]],
                                         Iterable[Tuple['Unit', 'Unit',
                                                        Real, Real]]]):
        if isinstance(conv_table, Mapping):
            self._unitMap = conv_table
        elif isinstance(conv_table, Iterable):
            self._unitMap = unitMap = {}
            for (from_unit, to_unit, factor, offset) in conv_table:
                unitMap[(from_unit, to_unit)] = (factor, offset)
        else:
            raise TypeError("A Mapping or list must be given.")

    def _get_factor(self, qty: 'Quantity', to_unit: 'Unit') -> Optional[Real]:
        try:
            factor, offset = self._unitMap[(qty.unit, to_unit)]
        except KeyError:
            # try reverse
            try:
                factor, offset = self._unitMap[(to_unit, qty.unit)]
            except KeyError:
                return None
            else:
                return (qty.amount - offset) / factor
        else:
            return factor * qty.amount + offset
