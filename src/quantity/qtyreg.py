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


# Standard library imports
from abc import abstractmethod
from functools import partial
from typing import Iterator, List, MutableMapping, Optional
try:
    from typing import Protocol
except ImportError:
    # noinspection PyUnresolvedReferences
    from typing_extensions import Protocol

# Third-party imports

# Local imports
from .term import Term


class SupportsDefinition(Protocol):

    """Abstract base class for items holding a term as definition."""

    @property
    @abstractmethod
    def definition(self) -> Term:
        """Definition of `self`."""

    @property
    @abstractmethod
    def normalized_definition(self) -> Term:
        """Normalized definition of `self`.

        Must be the normalized form of `self.definition`."""


class DefinedItemRegistry:

    """Registers items by definition."""

    def __init__(self) -> None:
        self._item_def_map: MutableMapping[Term, int] = {}
        self._item_list: List[SupportsDefinition] = []

    def register_item(self, item: SupportsDefinition) -> int:
        """Register `item` by its normalized definition.

        Args:
            item (SupportsDefinition): defined item to be registered

        Returns:
            int: index of registered item

        Raises:
            ValueError: item with same or equivalent definition already
                registered
        """
        item_norm_def = item.normalized_definition
        try:
            idx = self._item_def_map[item_norm_def]
        except KeyError:
            item_list = self._item_list
            item_list.append(item)
            idx = len(item_list) - 1
            self._item_def_map[item_norm_def] = idx
            return idx
        else:
            reg_item = self._item_list[idx]
            if reg_item == item:
                return idx
            else:
                raise ValueError("Item with same or equivalent definition "
                                 f"already registered: '{reg_item}'.")

    def __getitem__(self, item_def: Term) -> SupportsDefinition:
        """Get item by definition.

        Args:
            item_def (Term): definition of item to be looked-up

        Returns:
            SupportsDefinition: item registered with a definition equivalent
                to `item_def`

        Raises:
            ValueError: no item registered with definition equivalent to
                `item_def`
        """
        norm_qty_def = item_def.normalized()
        try:
            idx = self._item_def_map[norm_qty_def]
        except KeyError:
            raise ValueError('No item registered with given definition.')
        return self._item_list[idx]

    def __len__(self) -> int:
        return len(self._item_list)

    def __iter__(self) -> Iterator[SupportsDefinition]:
        return iter(self._item_list)


# Global registry of Quantities
_registry = DefinedItemRegistry()


register_quantity_cls = partial(DefinedItemRegistry.register_item,
                                _registry)
register_quantity_cls.__doc__ = _registry.register_item.__doc__
