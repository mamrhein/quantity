# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2020 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.txt provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Class implementing a registry for items holding a term as definition."""

import sys
from typing import Generic, List, MutableMapping, TypeVar, cast

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

from .term import NonNumTermElem, Term


T = TypeVar("T", bound=NonNumTermElem)


class DefinedItemRegistry(Generic[T]):

    """Registers items by definition."""

    def __init__(self, unique_items: bool = True) -> None:
        self._unique_items: Final = unique_items
        self._item_def_map: MutableMapping[Term[T], int] = {}
        self._item_list: List[List[T]] = []

    def register_item(self, item: T) -> int:
        """Register `item` by its normalized definition.

        Args:
            item (T): defined item to be registered

        Returns:
            int: index of registered item

        Raises:
            ValueError: item with same or equivalent definition already
                registered
        """
        item_norm_def = cast(Term[T], item.normalized_definition)
        try:
            idx = self._item_def_map[item_norm_def]
        except KeyError:
            item_list = self._item_list
            idx = len(item_list)
            item_list.append([item])
            self._item_def_map[item_norm_def] = idx
            return idx
        else:
            reg_item = self._item_list[idx][0]
            if reg_item == item:
                return idx
            elif self._unique_items:
                raise ValueError("Item with same or equivalent definition "
                                 f"already registered: '{reg_item}'.")
            else:
                self._item_list[idx].append(item)
                return idx

    def __getitem__(self, item_def: Term[T]) -> T:
        """Get item by definition.

        Args:
            item_def (Term[T]): definition of item to be looked-up

        Returns:
            T: item registered with a definition equivalent
                to `item_def`

        Raises:
            KeyError: no item registered with definition equivalent to
                `item_def`
        """
        norm_item_def = item_def.normalized()
        idx = self._item_def_map[norm_item_def]
        return self._item_list[idx][0]

    def __len__(self) -> int:
        """len(self)"""
        return len(self._item_list)
