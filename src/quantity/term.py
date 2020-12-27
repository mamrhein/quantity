# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
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


"""Terms of tuples of elements and corresponding exponents."""


# Standard library imports
from abc import ABCMeta, abstractmethod
from functools import reduce
from itertools import chain, groupby
from numbers import Real
from operator import mul
from typing import (Any, Callable, Generator, Iterable, Iterator, Optional,
                    Tuple, Union)

# characters for string representation of terms
import unicodedata

_SUPERSCRIPT_CHARS = [unicodedata.lookup("SUPERSCRIPT %s" % num)
                      for num in ["TWO", "THREE", "FOUR", "FIVE", "SIX",
                                  "SEVEN", "EIGHT", "NINE"]]
_MIDDLEDOT = unicodedata.lookup('MIDDLE DOT')
del unicodedata
_powerChars = ['', ''] + _SUPERSCRIPT_CHARS
_mulSign = _MIDDLEDOT
_div_sign = '/'


class NonNumTermElem(metaclass=ABCMeta):

    """Abstract base class for non-numeric term elements"""

    @abstractmethod
    def is_base_elem(self) -> bool:
        """True if elem is a base element; i.e. can not be decomposed."""

    @property
    @abstractmethod
    def normalized_definition(self) -> 'ItemListType':
        """Return the decomposition of `self`."""

    @abstractmethod
    def norm_sort_key(self) -> int:
        """Return sort key for `self` used for normalization of terms."""

    @abstractmethod
    def _get_factor(self, other: 'NonNumTermElem') \
            -> Union['NonNumTermElem', Real]:
        """Return factor f so that f * `other` == `self`."""


ElemType = Union[NonNumTermElem, Real]
ItemType = Tuple[ElemType, int]
ItemListType = Iterable[ItemType]


class Term(metaclass=ABCMeta):
    """Holds definitions of multidimensional items in the form of tuples of
    elements and corresponding exponents.

    ((x, 1), (y, 3), (z, -2)) means x * y ** 3 / z ** 2"""

    __slots__ = ['_items', '_normalized', '_hash']

    @staticmethod
    def normalize_elem(elem: ElemType) -> ItemListType:
        """Return the decomposition of elem (list of items)."""
        if isinstance(elem, Real) or elem.is_base_elem():
            return [(elem, 1)]
        return elem.normalized_definition

    @staticmethod
    def norm_sort_key(elem: ElemType) -> int:
        """Return sort key for `elem` used for normalized form of term."""
        if isinstance(elem, Real):
            return -1
        return elem.norm_sort_key()

    def __init__(self, items: ItemListType = (),
                 reduce_items: bool = True):
        _items: Tuple[ItemType, ...]
        n_items: Optional[int]
        try:
            # noinspection PyTypeChecker
            n_items = len(items)
        except TypeError:
            n_items = None
        if items and reduce_items:
            _items = self._reduce_items(items, n_items=n_items)
        else:
            _items = tuple(items)
        self._items = _items
        # optimize a common case:
        if len(_items) == 1:
            (elem, exp) = _items[0]
            if isinstance(elem, Real) or elem.is_base_elem():
                self._normalized = self

    def _reduce_items(self, items: ItemListType,
                      n_items: Optional[int] = None,
                      keep_item_order: bool = True) \
            -> Tuple[ItemType, ...]:
        if n_items == 1:  # already reduced
            return tuple(_filter_items(items))
        if n_items == 2:
            (elem1, exp1), (elem2, exp2) = items
            elem1_is_num = isinstance(elem1, Real)
            elem2_is_num = isinstance(elem2, Real)
            # most relevant case: numeric + non-numeric element
            if elem1_is_num and not elem2_is_num:
                return tuple(_filter_items(((elem1, exp1), (elem2, exp2))))
            # second most relevant case: 2 non-numeric elements
            if not elem1_is_num and not elem2_is_num:
                # same elements?
                if elem1 is elem2:
                    exp = exp1 + exp2
                    if exp == 0:
                        return ()
                    else:
                        return (elem1, exp),
                # elements convertible?
                try:
                    # noinspection PyProtectedMember
                    conv = elem2._get_factor(elem1)
                except (NotImplementedError, TypeError):
                    pass
                else:
                    return tuple(_filter_items(((conv ** exp2, 1),
                                                (elem1, exp1 + exp2))))
                if keep_item_order:
                    return tuple(_filter_items(((elem1, exp1),
                                                (elem2, exp2))))
                else:
                    items = sorted(((elem1, exp1), (elem2, exp2)),
                                   key=lambda item:
                                       self.norm_sort_key(item[0]))
                    return tuple(_filter_items(items))
            # third most relevant case: non-numeric + numeric element
            if elem2_is_num and not elem1_is_num:
                return tuple(_filter_items(((elem2, exp2), (elem1, exp1))))
            # least relevant case: 2 numeric elements
            if elem1_is_num and elem2_is_num:
                num = elem1 ** exp1 * elem2 ** exp2
                if num != 1:
                    return (num, 1),
        # more than 2 items or number of items unknown:
        norm_sort_key = self.norm_sort_key
        sort_key: Callable[[Tuple[int, Any]], int] = lambda x: x[0]
        if keep_item_order:
            key2_first_idx_map = {-1: -1, 0: 0}
            map_iter = ((key2_first_idx_map.setdefault(norm_sort_key(item[0]),
                                                       idx + 1),
                        item)
                        for idx, item in enumerate(items))
        else:
            map_iter = ((norm_sort_key(item[0]), item) for item in items)
        items_sorted = sorted(map_iter, key=sort_key)
        res_items = []
        num_elem = 1
        for key, group_it in groupby(items_sorted, key=sort_key):
            if key > 0:  # non-numerical elements
                _, item = next(group_it)
                accum_items = [item]
                for _, item in group_it:
                    done = False
                    for idx, otherItem in enumerate(accum_items):
                        (elem1, exp1), (elem2, exp2) = otherItem, item
                        # same elements?
                        if elem1 is elem2:
                            accum_items[idx] = (elem1, exp1 + exp2)
                            done = True
                            break
                        # elements convertible?
                        try:
                            # noinspection PyProtectedMember
                            conv = elem2._get_factor(elem1)
                        except (NotImplementedError, TypeError):
                            pass
                        else:
                            num_elem *= conv ** exp2
                            accum_items[idx] = (elem1, exp1 + exp2)
                            done = True
                            break
                    if not done:
                        accum_items.append(item)
                res_items += (item for item in accum_items if item[1] != 0)
            else:  # numerical elements
                num_elem = reduce(mul, (elem ** exp
                                        for _, (elem, exp) in group_it),
                                  num_elem)
        if num_elem == 1:
            return tuple(res_items)
        else:
            return tuple([(num_elem, 1)] + res_items)

    def normalized(self) -> 'Term':
        """Return normalized term equivalent to `self`."""
        try:
            return self._normalized
        except AttributeError:
            pass
        it = _iter_normalized(self, self.normalize_elem)
        items = self._reduce_items(it, keep_item_order=False)
        if items == self._items:  # self is already normalized
            self._normalized = self
            return self
        term = self.__class__(items, reduce_items=False)
        term._normalized = term
        self._normalized = term
        return term

    @property
    def is_normalized(self) -> bool:
        """Return True if `self` is normalized."""
        return self.normalized() is self

    @property
    def items(self) -> Tuple[ItemType, ...]:
        """Return iterable of items in `self`."""
        return self._items

    @property
    def num_elem(self) -> Optional[Real]:
        """Return the numerical element of `self` (if there is any)."""
        try:
            first_elem = self[0][0]
        except IndexError:
            pass
        else:
            if isinstance(first_elem, Real):
                return first_elem
        return None

    def reciprocal(self) -> 'Term':
        """1 / `self`"""
        return self.__class__(_reciprocal(self), reduce_items=False)

    def __iter__(self) -> Iterator[ItemType]:
        """Return iterator over items in `self`."""
        return iter(self._items)

    def __len__(self) -> int:
        """Return number of items in `self`."""
        return len(self._items)

    def __getitem__(self, idx: int) -> ItemType:
        """Return the item in `self` at index `idx`."""
        return self._items[idx]

    def __hash__(self) -> int:
        """hash(self)"""
        try:
            return self._hash
        except AttributeError:
            pass
        if self.is_normalized:
            self._hash = hash_val = hash(self._items)
        else:
            self._hash = hash_val = hash(self.normalized())
        return hash_val

    def __eq__(self, other) -> bool:
        """self == other"""
        return (self is other.normalized()
                or self.normalized() is other
                or self.normalized().items == other.normalized().items)

    def __mul__(self, other) -> 'Term':
        """self * other"""
        cls = self.__class__
        if isinstance(other, cls):
            n_items = len(self) + len(other)
            items = self._reduce_items(chain(self, other), n_items=n_items)
        elif isinstance(other, Real):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, 1),), self),
                                       n_items=n_items)
        else:
            return NotImplemented
        return cls(items, reduce_items=False)

    __rmul__ = __mul__

    def __truediv__(self, other) -> 'Term':
        """self / other"""
        cls = self.__class__
        if isinstance(other, cls):
            n_items = len(self) + len(other)
            items = self._reduce_items(chain(self, _reciprocal(other)),
                                       n_items=n_items)
        elif isinstance(other, Real):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, -1),), self),
                                       n_items=n_items)
        else:
            return NotImplemented
        return cls(items, reduce_items=False)

    def __rtruediv__(self, other) -> 'Term':
        """other / self"""
        if isinstance(other, Real):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, 1),),
                                             _reciprocal(self)),
                                       n_items=n_items)
            return self.__class__(items, reduce_items=False)
        return NotImplemented

    def __pow__(self, exp: int) -> 'Term':
        """self ** exp"""
        return self.__class__(((ielem, exp * iexp) for (ielem, iexp) in self),
                              reduce_items=False)

    def __repr__(self) -> str:
        """repr(self)"""
        return "%s(%s)" % (self.__class__.__name__, repr(self._items))

    def __str__(self) -> str:
        """str(self)"""
        elems_pos_exp = []
        elems_neg_exp = []
        exp_map = [1, -1]
        for (elem, exp) in self:
            absexp = abs(exp)
            elem_str = str(elem)
            # if string representation of elem contains div-sign, split it:
            for i, s in enumerate(elem_str.split(_div_sign)):
                e = exp * exp_map[i]
                if e > 0:
                    elems_pos_exp.append('%s%s' % (s, _powerChars[absexp]))
                else:
                    elems_neg_exp.append('%s%s' % (s, _powerChars[absexp]))
        if elems_pos_exp:
            pos_exp_part = _mulSign.join(elems_pos_exp)
        else:
            pos_exp_part = '1'
        if elems_neg_exp:
            div_sign = _div_sign
            neg_exp_part = _mulSign.join(elems_neg_exp)
        else:
            div_sign = neg_exp_part = ''
        return pos_exp_part + div_sign + neg_exp_part


# helper functions

def _filter_items(items: ItemListType) \
        -> Generator[ItemType, None, None]:
    return ((elem, exp) for (elem, exp) in items
            # eliminate items equivalent to 1:
            if exp != 0 and elem != 1)


def _reciprocal(items: ItemListType) \
        -> Generator[ItemType, None, None]:
    return ((elem, -exp) for (elem, exp) in items)


def _iter_normalized(term: ItemListType,
                     normalize_elem: Callable[[ElemType], ItemListType]) \
        -> Generator[ItemType, None, None]:
    for (elem, exp) in term:
        if isinstance(elem, Real) or elem.is_base_elem():
            yield elem, exp
        else:
            for item in _iter_normalized(((nElem, nExp * exp)
                                          for (nElem, nExp)
                                          in normalize_elem(elem)),
                                         normalize_elem):
                yield item
