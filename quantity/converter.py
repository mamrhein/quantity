# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        converter
## Purpose:     Provides classes used to convert quantities
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
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

__version__ = 0, 7, 0

__metaclass__ = type


class Converter:

    """Convert a quantity's amount to the equivalent amount for another
    unit.

    A quantity converter can be any callable with a signature like
    conv(qty, toUnit) -> number f so that type(qty)(f, toUnit) == qty.

    Must return None if conversion can not be done."""

    def __call__(self, qty, toUnit):
        return None


class RefUnitConverter:

    """Converter for Quantity classes that have a reference unit."""

    def __call__(self, qty, toUnit):
        """Return f so that type(qty)(f, toUnit) == qty."""
        if qty.unit is toUnit:          # same unit
            return qty.amount
        if qty.Unit == toUnit.Unit:     # same Unit class
            resDef = (qty.unit.normalizedDefinition
                      / toUnit.normalizedDefinition)
            return qty.amount * resDef.amount
        return None


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

        If there is no mapping from `qty.unit` to `toUnit` or vice versa
        defined in the conversion table, None is returned."""
        if qty.unit is toUnit:          # same unit
            return qty.amount
        try:
            factor, offset = self._unitMap[(qty.unit, toUnit)]
        except KeyError:
            # try reverse
            try:
                factor, offset = self._unitMap[(toUnit, qty.unit)]
            except KeyError:
                return None
            else:
                return (qty.amount - offset) / factor
        else:
            return factor * qty.amount + offset
