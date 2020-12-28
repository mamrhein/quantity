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


"""Provide metaclass for defining quantities."""


# Standard library imports

# Third-party imports
from numbers import Integral
from typing import Any, cast, Dict, Optional, Tuple, Union

# Local imports
from .qtyreg import register_quantity_cls
from .term import NonNumTermElem, Term


class QuantityMeta(type):

    """Meta class that provides operators to construct derived quantities."""

    def __init__(cls, name: str, bases: Tuple[type, ...],
                 clsdict: Dict[str, Any]):
        cls._definition: Optional[Term]
        # add hidden attributes for properties
        try:
            cls._definition = clsdict.pop('definition')
        except KeyError:
            cls._definition = None
        super().__init__(name, bases, clsdict)
        # register cls
        cls._reg_id = register_quantity_cls(cls)

    @property
    def definition(cls) -> Term:
        """Definition of quantity class."""
        if cls._definition is None:
            return Term(((cast(NonNumTermElem, cls), 1),))
        return cls._definition

    def is_base_quantity(cls) -> bool:
        """Return True if `cls` is not derived from other quantity classes."""
        # base quantity -> class definition is None or empty term
        return cls._definition is None or len(cls._definition) == 0

    @property
    def normalized_definition(cls) -> Term:
        """Normalized definition of quantity class."""
        try:
            return cls._definition.normalized()
        except AttributeError:
            return cls.definition

    def is_derived_quantity(cls) -> bool:
        """Return True if `cls` is derived from other quantity classes."""
        return not cls.is_base_quantity()

    def __mul__(cls, other: Union['QuantityMeta', Term]) -> Term:
        """Return class definition: `cls` * `other`."""
        if isinstance(other, QuantityMeta):
            return Term(((cast(NonNumTermElem, cls), 1),
                         (cast(NonNumTermElem, other), 1)))
        if isinstance(other, Term):
            if all((isinstance(elem, QuantityMeta) for (elem, exp) in other)):
                return Term(((cast(NonNumTermElem, cls), 1),)) * other
        return NotImplemented

    def __rmul__(cls, other: Term) -> Term:
        """Return class definition: `other` * `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, QuantityMeta) for (elem, exp) in other)):
                return other * Term(((cls, 1),))
        return NotImplemented

    def __truediv__(cls, other: Union['QuantityMeta', Term]) -> Term:
        """Return class definition: `cls` / `other`."""
        if isinstance(other, QuantityMeta):
            return Term(((cast(NonNumTermElem, cls), 1),
                         (cast(NonNumTermElem, other), -1)))
        if isinstance(other, Term):
            if all((isinstance(elem, QuantityMeta) for (elem, exp) in other)):
                return Term(((cast(NonNumTermElem, cls), 1),)) * \
                       other.reciprocal()
        return NotImplemented

    def __rtruediv__(cls, other: Term) -> Term:
        """Return class definition: `other` / `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, QuantityMeta) for (elem, exp) in other)):
                return other * Term(((cast(NonNumTermElem, cls), -1),))
        return NotImplemented

    def __pow__(cls, exp: int) -> Term:
        """Return class definition: `cls` ** `exp`."""
        if isinstance(exp, Integral):
            return Term(((cast(NonNumTermElem, cls), exp),))
        return NotImplemented

    def __str__(cls) -> str:
        return cls.__name__

    # implement abstract method of NonNumTermElem to allow instances of
    # QuantityMeta to be elements in terms:

    is_base_elem = is_base_quantity

    def norm_sort_key(cls) -> int:
        """Return sort key for `cls` used for normalization of terms."""
        return cls._reg_id

    def _get_factor(self, other: Any) -> int:
        """Instances of QuantityMeta are not convertable, raise TypeError"""
        raise TypeError


# noinspection PyUnresolvedReferences
NonNumTermElem.register(QuantityMeta)
