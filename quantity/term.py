# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        term
## Purpose:     Terms of tuples of elements and corresponding exponents.
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


"""Terms of tuples of elements and corresponding exponents."""


from __future__ import absolute_import, unicode_literals
from numbers import Real
from itertools import chain

# unicode handling Python 2 / Python 3
import sys
PY_VERSION = sys.version_info[0]
del sys
if PY_VERSION < 3:
    str = unicode

__metaclass__ = type


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
        if Term.isNumerical(elem):
            return ''
        return str(elem)

    @staticmethod
    def convert(elem, into):
        """Return factor f so that f * Term([(into, 1)]) == Term([(elem, 1)]).

        Raises TypeError if conversion is not possible."""
        raise NotImplementedError

    @staticmethod
    def isNumerical(elem):
        """Return True if elem is a Real number"""
        return isinstance(elem, Real)

    def __init__(self, items=[]):
        self._items = self._reduceItems(items)

    def _mapItem(self, item):
        (elem, exp) = item
        return self.normSortKey(elem)

    def _mulItems(self, item1, item2):
        """(elem1, exp1) * (elem2, exp2)"""
        (elem1, exp1), (elem2, exp2) = item1, item2
        if self.isNumerical(elem1) and self.isNumerical(elem2):
            return [(elem1 ** exp1 * elem2 ** exp2, 1)]
        if elem1 is elem2:
            return [(elem1, exp1 + exp2)]
        if type(elem1) == type(elem2):
            try:
                conv = self.convert(elem2, elem1)
            except (NotImplementedError, TypeError):
                pass
            else:
                return [(conv ** exp2, 1), (elem1, exp1 + exp2)]
        return [(elem1, exp1), (elem2, exp2)]

    def _filterItems(self, items):
        for (elem, exp) in items:
            # eliminate items equivalent to 1:
            if exp != 0 and elem != 1:
                # adjust numerical elements to exp = 1:
                if self.isNumerical(elem):
                    yield (elem ** exp, 1)
                else:
                    yield (elem, exp)

    def _reduceItems(self, items, sortKey=None):
        # TODO: tune it !?!
        itemList = [(elem, exp) for (elem, exp) in self._filterItems(items)]
        nItems = len(itemList)
        if nItems <= 1:             # already reduced
            return tuple(itemList)
        if nItems == 2:
            item1, item2 = itemList
            items = self._filterItems(self._mulItems(item1, item2))
            if sortKey is None:
                return tuple(items)
            else:
                return tuple(sorted(items, key=sortKey))
        itemDict = {}
        sortMap = {'': 0, 0: 0}     # initialize for both, int and str keys
        n = 0
        for (elem, exp) in itemList:
            key = self._mapItem((elem, exp))
            try:
                items = itemDict[key]
            except KeyError:
                itemDict[key] = [(elem, exp)]
                if key:
                    n += 1
                    sortMap[key] = n
            else:
                done = False
                for idx, item in enumerate(items):
                    resItems = self._mulItems(item, (elem, exp))
                    if len(resItems) == 1:
                        items[idx] = resItems[0]
                        done = True
                        break
                    else:
                        # resItems[0] is numeric -> put into itemDict[0]
                        resElem1, resExp1 = resItems[0]
                        if self.isNumerical(resElem1):
                            items[idx] = resItems[1]
                            try:
                                numElem, numExp = itemDict[0][0]
                            except KeyError:
                                itemDict[0] = [resItems[0]]
                            else:
                                itemDict[0] = self._mulItems(
                                    (numElem, numExp), (resElem1, resExp1))
                            done = True
                            break
                if not done:
                    items.append((elem, exp))
                itemDict[key] = items
        if sortKey is None:
            sortKey = lambda item: sortMap[self._mapItem(item)]
        return tuple(sorted(((elem, exp)
                     for (elem, exp) in chain(*itemDict.values())
                     if exp != 0 and elem != 1), key=sortKey))

    def normalized(self):
        # TODO: tune it !?!
        try:
            term = self._normalized
        except AttributeError:
            cls = self.__class__
            baseItems = []
            items = [(elem, exp) for (elem, exp) in self]
            while items:
                (elem, exp) = items.pop()
                if cls.isNumerical(elem) or cls.isBaseElem(elem):
                    baseItems.append((elem, exp))
                else:
                    items += [(nElem, nExp * exp)
                              for (nElem, nExp) in cls.normalizeElem(elem)]
            items = self._reduceItems(baseItems, sortKey=self._mapItem)
            if items == self._items:        # self is already normalized
                self._normalized = None
                return self
            term = cls()
            term._items = items
            term._normalized = None
            self._normalized = term
            return term
        else:
            if term is None:
                return self
            return term

    @property
    def isNormalized(self):
        return self.normalized() is self

    def reciprocal(self):
        return self.__class__(((elem, -exp) for (elem, exp) in self))

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
                hashVal = self._hash = hash(self._items)
            else:
                hashVal = self._hash = hash(self.normalized())
        return hashVal

    def __eq__(self, other):
        """self == other"""
        return list(self.normalized()) == list(other.normalized())

    def __mul__(self, other):
        """self * other"""
        cls = self.__class__
        if isinstance(other, cls):
            return cls(chain(self, other))
        if self.isNumerical(other):
            return cls(chain(self, [(other, 1)]))
        return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        """self / other"""
        cls = self.__class__
        if isinstance(other, cls):
            return cls(chain(self, other.reciprocal()))
        if self.isNumerical(other):
            return cls(chain(self, [(other, -1)]))
        return NotImplemented

    __truediv__ = __div__

    def __rdiv__(self, other):
        """other / self"""
        if self.isNumerical(other):
            return self.__class__(chain(self.reciprocal(), [(other, 1)]))
        return NotImplemented

    __rtruediv__ = __rdiv__

    def __pow__(self, pExp):
        """self ** pExp"""
        return self.__class__(((elem, exp * pExp) for (elem, exp) in self))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._items))

    def __unicode__(self):
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

    if PY_VERSION < 3:
        def __str__(self):
            return self.__unicode__().encode('utf8')
    else:
        __str__ = __unicode__
