# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        term
# Purpose:     Terms of tuples of elements and corresponding exponents.
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


"""Terms of tuples of elements and corresponding exponents."""


from functools import reduce
from itertools import chain, groupby
from numbers import Real
from operator import mul


# characters for string representation of terms
import unicodedata
_SUPERSCRIPT_CHARS = [unicodedata.lookup("SUPERSCRIPT %s" % num)
                      for num in ["TWO", "THREE", "FOUR", "FIVE", "SIX",
                                  "SEVEN", "EIGHT", "NINE"]]
_MIDDLEDOT = unicodedata.lookup('MIDDLE DOT')
del unicodedata
_powerChars = ['', ''] + _SUPERSCRIPT_CHARS
_mulSign = _MIDDLEDOT
_divSign = '/'


class Term:

    """Holds definitions of multidimensional items in the form of tuples of
    elements and corresponding exponents.

    ((x, 1), (y, 3), (z, -2)) means x * y ** 3 / z ** 2"""

    __slots__ = ['_items', '_normalized', '_hash']

    @staticmethod
    def isBaseElem(elem):
        """True if elem is a base element; i.e. can not be decomposed."""
        return True

    @staticmethod
    def normalizeElem(elem):
        """Return the decomposition of elem (list of items)."""
        return [(elem, 1)]

    @staticmethod
    def normSortKey(elem):
        """Return sort key for elem; used for normalized form of term.

        The type of the returned must be the same for all elements, either
        int (>= 0) or str. Numerical elements must get the lowest sort key:
        0 if int, '' if str."""
        if isinstance(elem, Real):
            return ''
        return str(elem)

    @staticmethod
    def convert(elem, into):
        """Return factor f so that f * Term([(into, 1)]) == Term([(elem, 1)]).

        Raises TypeError if conversion is not possible."""
        raise NotImplementedError

    def __init__(self, items=(), reduceItems=True):
        if items and reduceItems:
            self._items = items = self._reduceItems(items)
        else:
            self._items = items = tuple(items)
        # optimize a common case:
        if len(items) == 1:
            (elem, exp) = items[0]
            if isinstance(elem, Real) or self.isBaseElem(elem):
                self._normalized = self

    def _reduceItems(self, itemList, nItems=None, keepItemOrder=True):
        if nItems == 1:             # already reduced
            return tuple(_filterItems(itemList))
        if nItems == 2:
            (elem1, exp1), (elem2, exp2) = itemList
            elem1IsNum = isinstance(elem1, Real)
            elem2IsNum = isinstance(elem2, Real)
            # most relevant case: numeric + non-numeric element
            if elem1IsNum and not elem2IsNum:
                return tuple(_filterItems(((elem1, exp1), (elem2, exp2))))
            # second most relevant case: 2 non-numeric elements
            if not elem1IsNum and not elem2IsNum:
                if elem1 is elem2:
                    exp = exp1 + exp2
                    if exp == 0:
                        return ()
                    else:
                        return ((elem1, exp),)
                elif type(elem1) == type(elem2):
                    try:
                        conv = self.convert(elem2, elem1)
                    except (NotImplementedError, TypeError):
                        pass
                    else:
                        return tuple(_filterItems(((conv ** exp2, 1),
                                                   (elem1, exp1 + exp2))))
                if keepItemOrder:
                    return tuple(_filterItems(((elem1, exp1), (elem2, exp2))))
                else:
                    key = lambda item: self.normSortKey(item[0])
                    items = sorted(((elem1, exp1), (elem2, exp2)), key=key)
                    return tuple(_filterItems(items))
            # third most relevant case: non-numeric + numeric element
            if elem2IsNum and not elem1IsNum:
                return tuple(_filterItems(((elem2, exp2), (elem1, exp1))))
            # least relevant case: 2 numeric elements
            if elem1IsNum and elem2IsNum:
                num = elem1 ** exp1 * elem2 ** exp2
                if num != 1:
                    return ((num, 1),)
        # more than 2 items or number of items unknown:
        normSortKey = self.normSortKey
        sortKey = lambda x: x[0]
        if keepItemOrder:
            key2FirstIdxMap = {'': 0, 0: 0}
            mapIter = ((key2FirstIdxMap.setdefault(normSortKey(item[0]),
                                                   idx + 1),
                        item)
                       for idx, item in enumerate(itemList))
        else:
            mapIter = ((normSortKey(item[0]), item) for item in itemList)
        itemsSorted = sorted(mapIter, key=sortKey)
        resItems = []
        numElem = 1
        for key, groupIt in groupby(itemsSorted, key=sortKey):
            if key:     # non-numerical elements
                _, item = next(groupIt)
                accumItems = [item]
                for _, item in groupIt:
                    done = False
                    for idx, otherItem in enumerate(accumItems):
                        (elem1, exp1), (elem2, exp2) = otherItem, item
                        if elem1 is elem2:
                            accumItems[idx] = (elem1, exp1 + exp2)
                            done = True
                            break
                        elif type(elem1) == type(elem2):
                            try:
                                conv = self.convert(elem2, elem1)
                            except (NotImplementedError, TypeError):
                                pass
                            else:
                                numElem *= conv ** exp2
                                accumItems[idx] = (elem1, exp1 + exp2)
                                done = True
                                break
                    if not done:
                        accumItems.append(item)
                resItems += (item for item in accumItems if item[1] != 0)
            else:       # numerical elements
                numElem = reduce(mul,
                                 (elem ** exp for _, (elem, exp) in groupIt),
                                 numElem)
        if numElem == 1:
            return tuple(resItems)
        else:
            return tuple([(numElem, 1)] + resItems)

    def normalized(self):
        try:
            return self._normalized
        except AttributeError:
            it = _iterNormalized(self, self.isBaseElem, self.normalizeElem)
            items = self._reduceItems(it, keepItemOrder=False)
            if items == self._items:        # self is already normalized
                self._normalized = self
                return self
            term = self.__class__(items, reduceItems=False)
            term._normalized = term
            self._normalized = term
            return term

    @property
    def isNormalized(self):
        return self.normalized() is self

    @property
    def items(self):
        return self._items

    @property
    def numElem(self):
        try:
            firstElem = self[0][0]
        except IndexError:
            pass
        else:
            if isinstance(firstElem, Real):
                return firstElem
        return None

    def reciprocal(self):
        return self.__class__(_reciprocal(self), reduceItems=False)

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, idx):
        return self._items[idx]

    def __hash__(self):
        try:
            hashVal = self._hash
        except AttributeError:
            if self.isNormalized:
                self._hash = hashVal = hash(self._items)
            else:
                self._hash = hashVal = hash(self.normalized())
        return hashVal

    def __eq__(self, other):
        """self == other"""
        return (self is other.normalized()
                or self.normalized() is other
                or self.normalized().items == other.normalized().items)

    def __mul__(self, other):
        """self * other"""
        cls = self.__class__
        if isinstance(other, cls):
            nItems = len(self) + len(other)
            items = self._reduceItems(chain(self, other), nItems=nItems)
        elif isinstance(other, Real):
            nItems = len(self) + 1
            items = self._reduceItems(chain(((other, 1),), self),
                                      nItems=nItems)
        else:
            return NotImplemented
        return cls(items, reduceItems=False)

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        cls = self.__class__
        if isinstance(other, cls):
            nItems = len(self) + len(other)
            items = self._reduceItems(chain(self, _reciprocal(other)),
                                      nItems=nItems)
        elif isinstance(other, Real):
            nItems = len(self) + 1
            items = self._reduceItems(chain(((other, -1),), self),
                                      nItems=nItems)
        else:
            return NotImplemented
        return cls(items, reduceItems=False)

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if isinstance(other, Real):
            nItems = len(self) + 1
            items = self._reduceItems(chain(((other, 1),), _reciprocal(self)),
                                      nItems=nItems)
            return self.__class__(items, reduceItems=False)
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, pExp):
        """self ** pExp"""
        return self.__class__(((elem, exp * pExp) for (elem, exp) in self),
                              reduceItems=False)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._items))

    def __str__(self):
        elemsPosExp = []
        elemsNegExp = []
        expMap = [1, -1]
        for (elem, exp) in self:
            absexp = abs(exp)
            elemStr = str(elem)
            # if string representation of elem contains div-sign, split it:
            for i, s in enumerate(elemStr.split(_divSign)):
                e = exp * expMap[i]
                if e > 0:
                    elemsPosExp.append('%s%s' % (s, _powerChars[absexp]))
                else:
                    elemsNegExp.append('%s%s' % (s, _powerChars[absexp]))
        if elemsPosExp:
            posExpPart = _mulSign.join(elemsPosExp)
        else:
            posExpPart = '1'
        if elemsNegExp:
            divSign = _divSign
            negExpPart = _mulSign.join(elemsNegExp)
        else:
            divSign = negExpPart = ''
        return posExpPart + divSign + negExpPart


# helper functions


def _filterItems(items):
    return ((elem, exp) for (elem, exp) in items
            # eliminate items equivalent to 1:
            if exp != 0 and elem != 1)


def _reciprocal(items):
    return ((elem, -exp) for (elem, exp) in items)


def _iterNormalized(term, isBaseElem, normalizeElem):
    for (elem, exp) in term:
        if isinstance(elem, Real) or isBaseElem(elem):
            yield (elem, exp)
        else:
            for item in _iterNormalized(((nElem, nExp * exp)
                                        for (nElem, nExp)
                                        in normalizeElem(elem)),
                                        isBaseElem, normalizeElem):
                yield item
