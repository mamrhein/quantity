# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Terms of tuples of elements and corresponding exponents."""

from __future__ import annotations

import sys
import unicodedata
from abc import abstractmethod
from functools import reduce
from itertools import chain, groupby
from numbers import Rational
from operator import mul
from typing import (
    Any, Callable, Generator, Iterable, Iterator, List, Optional, Sequence,
    Sized, Tuple, TypeVar, Union, cast, overload,
    )

from decimalfp import ONE

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

_SUPERSCRIPT_CHARS = [unicodedata.lookup("SUPERSCRIPT %s" % num)
                      for num in ["TWO", "THREE", "FOUR", "FIVE", "SIX",
                                  "SEVEN", "EIGHT", "NINE"]]
_MIDDLEDOT = unicodedata.lookup('MIDDLE DOT')
del unicodedata
_POWER_CHARS = ['', ''] + _SUPERSCRIPT_CHARS
_MUL_SIGN = _MIDDLEDOT
_DIV_SIGN = '/'


class NonNumTermElem(Protocol):
    """Abstract base class for non-numeric term elements"""

    @abstractmethod
    def is_base_elem(self) -> bool:
        """Return True if elem is a base element (i.e. can't be decomposed)."""

    @property
    @abstractmethod
    def definition(self) -> Term[NonNumTermElem]:
        """Definition of `self`."""

    @property
    @abstractmethod
    def normalized_definition(self) -> Term[NonNumTermElem]:
        """Return the decomposition of `self`."""

    @abstractmethod
    def norm_sort_key(self) -> int:
        """Return sort key for `self` used for normalization of terms."""

    @abstractmethod
    def _get_factor(self, other: NonNumTermElem) -> Optional[Rational]:
        """Return factor f so that f * `other` == `self`, or None."""


T = TypeVar("T", bound=NonNumTermElem, covariant=True)
ElemT = Union[T, Rational]
ItemT = Tuple[ElemT[T], int]
ItemIterableT = Iterable[ItemT[T]]
ItemSequenceT = Sequence[ItemT[T]]
ItemTupleT = Tuple[ItemT[T], ...]
ItemListT = List[ItemT[T]]


class Term(ItemSequenceT[T]):
    """Holds definitions of multidimensional items.

    The definitions are iterables of tuples of elements and corresponding
    exponents.

    ((x, 1), (y, 3), (z, -2)) means x * y ** 3 / z ** 2
    """

    __slots__ = ['_items', '_normalized', '_hash']

    @staticmethod
    def normalize_elem(elem: ElemT[T]) -> ItemIterableT[T]:
        """Return the decomposition of elem (list of items)."""
        if isinstance(elem, Rational):
            return [(elem, 1)]
        elif elem.is_base_elem():
            return [(elem, 1)]
        else:
            return cast(ItemIterableT[T], elem.normalized_definition)

    @staticmethod
    def norm_sort_key(elem: ElemT[T]) -> int:
        """Return sort key for `elem` used for normalized form of term."""
        if isinstance(elem, Rational):
            return -1
        return elem.norm_sort_key()

    def __init__(self, items: ItemIterableT[T] = (),
                 reduce_items: bool = True):
        _items: ItemTupleT[T]
        n_items: Optional[int]
        if isinstance(items, Sized):
            n_items = len(items)
        else:
            n_items = None
        if items and reduce_items:
            _items = self._reduce_items(items, n_items=n_items)
        else:
            _items = tuple(items)
        self._items = _items
        # optimize a common case:
        if len(_items) == 1:
            (elem, exp) = _items[0]
            if isinstance(elem, Rational) or elem.is_base_elem():
                self._normalized = self

    def _reduce_items(self, items: ItemIterableT[T],
                      n_items: Optional[int] = None,
                      keep_item_order: bool = True) -> ItemTupleT[T]:
        if n_items == 1:  # already reduced
            return tuple(_filter_items(items))
        if n_items == 2:
            elem1: ElemT[T]
            elem2: ElemT[T]
            (elem1, exp1), (elem2, exp2) = items
            # most relevant case: numeric + non-numeric element
            if isinstance(elem1, Rational) and \
                    not isinstance(elem2, Rational):
                return tuple(_filter_items(((elem1, exp1), (elem2, exp2))))
            # second most relevant case: 2 non-numeric elements
            if not isinstance(elem1, Rational) and \
                    not isinstance(elem2, Rational):
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
                except TypeError:
                    pass
                else:
                    if conv is not None:
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
            if isinstance(elem2, Rational) and \
                    not isinstance(elem1, Rational):
                return tuple(_filter_items(((elem2, exp2), (elem1, exp1))))
            # least relevant case: 2 numeric elements
            if isinstance(elem1, Rational) and isinstance(elem2, Rational):
                num: Rational = elem1 ** exp1 * elem2 ** exp2
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
        res_items: ItemListT[T] = []
        num_elem: Rational = ONE
        key: int
        group_it: Iterator[Tuple[int, ItemT[T]]]
        for key, group_it in groupby(items_sorted, key=sort_key):
            if key > 0:  # non-numerical elements
                group_it = cast(Iterator[Tuple[int, Tuple[T, int]]], group_it)
                _, item = next(group_it)
                accum_items = [item]
                for _, item in group_it:
                    done = False
                    for idx, other_item in enumerate(accum_items):
                        elem_t1, exp1 = other_item
                        elem_t2, exp2 = item
                        # same elements?
                        if elem_t1 is elem_t2:
                            accum_items[idx] = (elem_t1, exp1 + exp2)
                            done = True
                            break
                        # elements convertible?
                        try:
                            # noinspection PyProtectedMember
                            conv = elem_t2._get_factor(elem_t1)
                        except TypeError:
                            pass
                        else:
                            if conv is not None:
                                num_elem *= conv ** exp2
                                accum_items[idx] = (elem_t1, exp1 + exp2)
                                done = True
                                break
                    if not done:
                        accum_items.append(item)
                accum_items = [item for item in accum_items if item[1] != 0]
                res_items.extend(accum_items)
            else:  # numerical elements
                group_it = cast(Iterator[Tuple[int, Tuple[Rational, int]]],
                                group_it)
                num_elem = reduce(mul, (elem ** exp
                                        for _, (elem, exp) in group_it),
                                  num_elem)
        if num_elem != 1:
            num_item: ItemT[T] = (num_elem, 1)
            return tuple(chain((num_item,), res_items))
        return tuple(res_items)

    def normalized(self) -> Term[T]:
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
    def items(self) -> Tuple[ItemT[T], ...]:
        """Return items in `self` as tuple."""
        return self._items

    @property
    def num_elem(self) -> Optional[Rational]:
        """Return the numerical element of `self` (if there is any)."""
        try:
            elem, exp = self[0]
        except IndexError:
            pass
        else:
            if isinstance(elem, Rational):
                return cast(Rational, elem ** exp)
        return None

    def split(self, dflt_num: Rational = ONE) \
            -> Tuple[Rational, Term[T]]:
        """Return `self`s numeric element and `self`s non-numeric part.

        If `self` has no numeric element, `dflt_num` is returned instead.
        """
        num = self.num_elem
        if num is None:
            return dflt_num, self
        else:
            return num, Term(self[1:])

    def reciprocal(self) -> Term[T]:
        """1 / `self`"""
        return self.__class__(_reciprocal(self), reduce_items=False)

    def __iter__(self) -> Iterator[ItemT[T]]:
        """Return iterator over items in `self`."""
        return iter(self._items)

    def __len__(self) -> int:
        """Return number of items in `self`."""
        return len(self._items)

    @overload
    def __getitem__(self, idx: int) -> ItemT[T]:
        """Return the item in `self` at index `idx`."""

    @overload
    def __getitem__(self, idx: slice) -> ItemSequenceT[T]:
        """Return the items in `self` at slice `idx`."""

    def __getitem__(self, idx: Union[int, slice]) \
            -> Union[ItemT[T], ItemSequenceT[T]]:
        """Return the item(s) in `self` at index or slice `idx`."""
        return self._items[idx]

    def __hash__(self) -> int:
        """hash(self)"""
        hash_val: int
        try:
            hash_val = self._hash  # type: ignore
        except AttributeError:
            if self.is_normalized:
                self._hash = hash_val = hash(self._items)
            else:
                self._hash = hash_val = hash(self.normalized())
        return hash_val

    def __eq__(self, other: Any) -> bool:
        """self == other"""
        if isinstance(other, Term):
            return (self is other.normalized() or
                    self.normalized() is other or
                    self.normalized().items == other.normalized().items)
        return NotImplemented

    def __mul__(self, other: Union[Term[T], Rational]) -> Term[T]:
        """self * other"""
        cls = self.__class__
        if isinstance(other, cls):
            n_items = len(self) + len(other)
            items = self._reduce_items(chain(self, other), n_items=n_items)
        elif isinstance(other, Rational):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, 1),), self),
                                       n_items=n_items)
        else:
            return NotImplemented
        return cls(items, reduce_items=False)

    __rmul__ = __mul__

    def __truediv__(self, other: Union[Term[T], Rational]) -> Term[T]:
        """self / other"""
        cls = self.__class__
        if isinstance(other, cls):
            n_items = len(self) + len(other)
            items = self._reduce_items(chain(self, _reciprocal(other)),
                                       n_items=n_items)
        elif isinstance(other, Rational):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, -1),), self),
                                       n_items=n_items)
        else:
            return NotImplemented
        return cls(items, reduce_items=False)

    def __rtruediv__(self, other: Rational) -> Term[T]:
        """other / self"""
        if isinstance(other, Rational):
            n_items = len(self) + 1
            items = self._reduce_items(chain(((other, 1),),
                                             _reciprocal(self)),
                                       n_items=n_items)
            return self.__class__(items, reduce_items=False)
        return NotImplemented

    def __pow__(self, exp: int) -> Term[T]:
        """self ** exp"""
        return self.__class__(((ielem, exp * iexp) for (ielem, iexp) in self),
                              reduce_items=True)

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
            for i, s in enumerate(elem_str.split(_DIV_SIGN)):
                e = exp * exp_map[i]
                if e > 0:
                    elems_pos_exp.append('%s%s' % (s, _POWER_CHARS[absexp]))
                else:
                    elems_neg_exp.append('%s%s' % (s, _POWER_CHARS[absexp]))
        if elems_pos_exp:
            pos_exp_part = _MUL_SIGN.join(elems_pos_exp)
        else:
            pos_exp_part = '1'
        if elems_neg_exp:
            div_sign = _DIV_SIGN
            neg_exp_part = _MUL_SIGN.join(elems_neg_exp)
        else:
            div_sign = neg_exp_part = ''
        return pos_exp_part + div_sign + neg_exp_part


# helper functions

def _filter_items(items: ItemIterableT[T]) \
        -> Generator[ItemT[T], None, None]:
    return ((elem, exp) for (elem, exp) in items
            # eliminate items equivalent to 1:
            if exp != 0 and elem != 1)


def _reciprocal(items: ItemIterableT[T]) \
        -> Generator[ItemT[T], None, None]:
    return ((elem, -exp) for (elem, exp) in items)


def _iter_normalized(term: ItemIterableT[T],
                     normalize_elem: Callable[[ElemT[T]],
                                              ItemIterableT[T]]) \
        -> Generator[ItemT[T], None, None]:
    for (elem, exp) in term:
        if isinstance(elem, Rational) or elem.is_base_elem():
            yield elem, exp
        else:
            for item in _iter_normalized(((base_elem, base_exp * exp)
                                          for (base_elem, base_exp)
                                          in normalize_elem(elem)),
                                         normalize_elem):
                yield item
