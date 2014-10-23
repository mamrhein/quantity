# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        term
## Purpose:     Terms of tuples of elements and corresponding exponents.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2013 ff. Michael Amrhein
## License:     This program is free software; you can redistribute it and/or
##              modify it under the terms of the GNU Lesser General Public
##              License as published by the Free Software Foundation; either
##              version 2 of the License, or (at your option) any later
##              version.
##              This program is distributed in the hope that it will be
##              useful, but WITHOUT ANY WARRANTY; without even the implied
##              warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##              PURPOSE.
##              See the GNU Lesser General Public License for more details.
##              You should have received a copy of the license text along with
##              this program; if not, get it from http://www.gnu.org/licenses,
##              or write to the Free Software Foundation, Inc.,
##              59 Temple Place, Suite 330, Boston MA 02111-1307, USA
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Terms of tuples of elements and corresponding exponents."""


from __future__ import absolute_import
from decimal import Decimal
from numbers import Real
from itertools import chain

# unicode handling Python 2 / Python 3
try:
    unicode('a')
except NameError:
    basestring = unicode = str


__version__ = 0, 0, 1

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
        int (<= 0) or str. Numerical elements must get the lowest sort key:
        0 if int, '' if str."""
        if Term.isNumerical(elem):
            return unicode('')
        return unicode(elem)

    @staticmethod
    def convert(elem, into):
        """Return factor f so that f * Term([(into, 1)]) == Term([(elem, 1)]).

        Raises TypeError if conversion is not possible."""
        raise NotImplementedError

    @staticmethod
    def isNumerical(elem):
        """Return True if elem is a Real number"""
        # because decimal.Decimal is nor registered as number, we have test it
        # explicitly
        return isinstance(elem, (Real, Decimal))

    def __init__(self, items=[]):
        self._items = self._reduceItems(items)

    def _mapItem(self, item):
        (elem, exp) = item
        return self.normSortKey(elem)

    def _mulItems(self, item1, item2):
        """(elem1, exp1) * (elem2, exp2)"""
        (elem1, exp1), (elem2, exp2) = item1, item2
        if self.isNumerical(elem1) and self.isNumerical(elem2):
            try:
                return [(elem1 ** exp1 * elem2 ** exp2, 1)]
            except TypeError:
                return [(Decimal(elem1) ** exp1 * Decimal(elem2) ** exp2, 1)]
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
        itemList = [(elem, exp) for (elem, exp) in self._filterItems(items)]
        nItems = len(itemList)
        if nItems <= 1:             # already reduced
            return tuple(itemList)
        if nItems == 2:
            item1, item2 = itemList
            items = self._filterItems(self._mulItems(item1, item2))
            if sortKey is None:
                return tuple(sorted(items, key=self._mapItem))
            else:
                return tuple(sorted(items, key=sortKey))
        itemDict = {}
        sortMap = {unicode(''): 0, 0: 0}  # initialize for both, integer and
                                          # string keys
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

    def __str__(self):
        elemsPosExp = []
        elemsNegExp = []
        expMap = [1, -1]
        for (elem, exp) in self:
            absexp = abs(exp)
            elemStr = unicode(elem)
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
