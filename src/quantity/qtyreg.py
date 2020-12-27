# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2020 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Global registry of defined quantities."""


# TODO: uncomment the following when compatibility for Python 3.6 is dropped
# from __future__ import annotations

# Standard library imports
from functools import partial
from typing import Iterator, List, MutableMapping, Optional, TYPE_CHECKING

# Third-party imports

# Local imports
from .term import Term

if TYPE_CHECKING:
    from . import Unit
    from .qtymeta import QuantityMeta


class QuantityClassRegistry:

    """Registers Quantity classes by definition."""

    def __init__(self) -> None:
        self._qty_def_map: MutableMapping[Term, int] = {}
        self._qty_cls_list: List[QuantityMeta] = []

    def register_quantity_cls(self, qty_cls: 'QuantityMeta') -> int:
        """Register Quantity class.

        Registers a sub-class of :class:`Quantity` by its normalized
        definition.

        Args:
            qty_cls (QuantityMeta): sub-class of :class:`Quantity` to be
                registered

        Returns:
            int: index of registered class

        Raises:
            ValueError: class with same definition already registered
        """
        qty_def = qty_cls.normalized_definition
        try:
            idx = self._qty_def_map[qty_def]
        except KeyError:
            qty_cls_list = self._qty_cls_list
            qty_cls_list.append(qty_cls)
            idx = len(qty_cls_list) - 1
            self._qty_def_map[qty_def] = idx
            return idx
        else:
            reg_cls = self._qty_cls_list[idx]
            if reg_cls == qty_cls:
                return idx
            else:
                raise ValueError(
                    "Class with same definition already registered.")

    def get_quantity_cls(self, qty_def: Term) -> 'QuantityMeta':
        """Get Quantity class by definition.

        Args:
            qty_def (Term): definition of class to be looked-up

        Returns:
            QuantityMeta: sub-class of :class:`Quantity` registered with
                definition `qty_def`

        Raises:
            ValueError: no sub-class of :class:`Quantity` registered with
                definition `qtyDef`
        """
        norm_qty_def = qty_def.normalized()
        try:
            idx = self._qty_def_map[norm_qty_def]
        except KeyError:
            raise ValueError('No quantity class registered with given '
                             'definition.')
        return self._qty_cls_list[idx]

    def get_unit_by_symbol(self, symbol: str) -> Optional['Unit']:
        """Return the unit with symbol `symbol`.

        Args:
            symbol (str): symbol to look-up

        Returns:
            :class:`Unit` sub-class if a unit with given `symbol` exists in
                one of the registered quantities' `Unit` class, otherwise
                `None`
        """
        for qty_cls in self:
            # noinspection PyUnresolvedReferences
            unit = qty_cls.get_unit_by_symbol(symbol)
            if unit:
                return unit
        return None

    def __len__(self) -> int:
        return len(self._qty_cls_list)

    def __iter__(self) -> Iterator['QuantityMeta']:
        return iter(self._qty_cls_list)


# Global registry of Quantities
_registry = QuantityClassRegistry()


get_unit_by_symbol = partial(QuantityClassRegistry.get_unit_by_symbol,
                             _registry)
get_unit_by_symbol.__doc__ = _registry.get_unit_by_symbol.__doc__

register_quantity_cls = partial(QuantityClassRegistry.register_quantity_cls,
                                _registry)
register_quantity_cls.__doc__ = _registry.register_quantity_cls.__doc__

get_quantity_cls = partial(QuantityClassRegistry.get_quantity_cls,
                           _registry)
get_quantity_cls.__doc__ = _registry.get_quantity_cls.__doc__
