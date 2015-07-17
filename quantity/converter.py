# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        converter
## Purpose:     Provides classes used to convert quantities
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Provides classes used to convert quantities."""

from __future__ import absolute_import, division, unicode_literals
from .exceptions import IncompatibleUnitsError, UnitConversionError


__metaclass__ = type


class Converter:

    """A quantity converter can be any callable with a signature like
    conv(qty, toUnit) -> number f so that type(qty)(f, toUnit) == qty."""

    def __call__(self, qty, toUnit):
        """Convert a quantity's amount to the equivalent amount for another
        unit.

        Args:
            qty (sub-class of :class:`Quantity`): quantity thats amount is to
                be converted
            toUnit (sub-class of :class:`Unit`): unit thats equivalent amount
                to be returned

        Returns:
            number: factor f so that f ^ toUNit == qty

        Raises:
            IncompatibleUnitsError: qty and toUnit are of incompatible types
            UnitConversionError: conversion factor not available
        """
        if qty.Unit is not toUnit.Unit:
            raise IncompatibleUnitsError("Can't convert a '%s' to a '%s'.",
                                         qty.Unit, toUnit.Unit)
        raise UnitConversionError("Can't convert '%s' to '%s'.",
                                  qty.unit, toUnit)


class RefUnitConverter:

    """Converter for Quantity classes that have a reference unit."""

    def __call__(self, qty, toUnit):
        """Return f so that type(qty)(f, toUnit) == qty.

        Args:
            qty (sub-class of :class:`Quantity`): quantity thats amount is to
                be converted
            toUnit (sub-class of :class:`Unit`): unit thats equivalent amount
                to be returned

        Returns:
            number: factor f so that f ^ toUNit == qty

        Raises:
            IncompatibleUnitsError: qty and toUnit are of incompatible types
            UnitConversionError: conversion factor not available
        """
        if qty.unit is toUnit:          # same unit
            return qty.amount
        if qty.Unit == toUnit.Unit:     # same Unit class
            resDef = (qty.unit.normalizedDefinition
                      / toUnit.normalizedDefinition)
            return qty.amount * resDef.amount
        raise IncompatibleUnitsError("Can't convert a '%s' to a '%s'.",
                                     qty.Unit, toUnit.Unit)


class TableConverter:

    """Converter using a conversion table.

    Args:
        convTable (dict or list): the mapping used to initialize the
            conversion table

    Each item of the conversion table defines a conversion from one unit to
    another unit and consists of four elements:

    * fromUnit: unit of the quantity to be converted

    * toUnit: target unit of the conversion

    * factor: factor to be applied to the quantity's amount

    * offset: an amount added after applying the factor

    When a `dict` is given as `convTable`, each key / value pair must map a
    tuple (fromUnit, toUnit) to a tuple (factor, offset).

    When a `list` is given as `convTable`, each item must be a tuple
    (fromUnit, toUnit, factor, offset).

    `factor` and `offset` must be set so that for an amount in terms of
    `fromUnit` the eqivalent amount in terms of `toUnit` is:

    result = amount * factor + offset

    An instance of `TableConverter` can be called with a :class:`Quantity`
    sub-class' instance `qty` and a :class:`Unit` sub-class' instance `toUnit`
    as parameters. It looks-up the pair (`qty.unit`, `toUnit`) for a factor
    and an offset and returns the resulting amount according to the formula
    given above.

    If there is no item for the pair (`qty.unit`, `toUnit`), it tries to find
    a reverse mapping by looking-up the pair (`toUnit`, `qty.unit`), and, if
    it finds one, it returns a result by applying a reversed formula:

    result = (amount - offset) / factor

    That means, for each pair of units it is sufficient to define a conversion
    in one direction.

    An instance of `TableConverter` can be directly registered as a converter
    by calling the :meth:`Unit.registerConverter` method of a Unit class.
    """

    def __init__(self, convTable):
        if isinstance(convTable, dict):
            self._unitMap = convTable
        elif isinstance(convTable, list):
            self._unitMap = unitMap = {}
            for (fromUnit, toUnit, factor, offset) in convTable:
                unitMap[(fromUnit, toUnit)] = (factor, offset)
        else:
            raise TypeError("A dict or list must be given.")

    def __call__(self, qty, toUnit):
        """Return f so that type(qty)(f, toUnit) == qty.

        Args:
            qty (sub-class of :class:`Quantity`): quantity thats amount is to
                be converted
            toUnit (sub-class of :class:`Unit`): unit thats equivalent amount
                to be returned

        Returns:
            number: factor f so that f ^ toUNit == qty

        Raises:
            IncompatibleUnitsError: qty and toUnit are of incompatible types
            UnitConversionError: conversion factor not available
        """
        if qty.unit is toUnit:          # same unit
            return qty.amount
        if qty.Unit == toUnit.Unit:     # same Unit class
            try:
                factor, offset = self._unitMap[(qty.unit, toUnit)]
            except KeyError:
                # try reverse
                try:
                    factor, offset = self._unitMap[(toUnit, qty.unit)]
                except KeyError:
                    raise UnitConversionError("Can't convert '%s' to '%s'.",
                                              qty.unit, toUnit)
                else:
                    return (qty.amount - offset) / factor
            else:
                return factor * qty.amount + offset
        raise IncompatibleUnitsError("Can't convert a '%s' to a '%s'.",
                                     qty.Unit, toUnit.Unit)
