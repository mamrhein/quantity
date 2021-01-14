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


"""Provide metaclass for defining classes with terms as definitions."""


# Standard library imports

# Third-party imports
from numbers import Integral
from typing import Any, cast, Dict, Optional, Tuple, Union

# Local imports
from .term import Term

ClassDefT = Term['ClassWithDefinitionMeta']


class ClassWithDefinitionMeta(type):

    """Meta class allowing to construct classes with terms as definitions."""

    # TODO: remove this class variable after mypy issue #1021 got fixed:
    _definition: Optional[ClassDefT]

    def __new__(mcs, name: str, bases: Tuple[type, ...],
                clsdict: Dict[str, Any],
                define_as: Optional[ClassDefT] = None) \
            -> 'ClassWithDefinitionMeta':
        cls = cast('ClassWithDefinitionMeta',
                   super().__new__(mcs, name, bases, clsdict))
        # check definition
        if define_as is not None:
            assert isinstance(define_as, Term), \
                "Definition given in 'define_as' must be an instance of " \
                "'Term'."
            assert all(isinstance(elem, mcs)
                       for elem, _ in define_as), \
                "All elements of definition given in 'define_as' must be " \
                f"instances of '{mcs.__name__}'."
        cls._definition = define_as
        return cls

    @property
    def definition(cls) -> ClassDefT:
        """Definition of `cls`."""
        if cls._definition is None:
            return ClassDefT(((cls, 1),))
        return cls._definition

    def is_base_cls(cls) -> bool:
        """Return True if `cls` is not derived from other class(es)."""
        # base class -> definition is None or empty term
        return cls._definition is None or len(cls._definition) == 0

    @property
    def normalized_definition(cls) -> ClassDefT:
        """Normalized definition of `cls`."""
        if cls._definition is None:
            return ClassDefT(((cls, 1),))
        else:
            return cls._definition.normalized()

    def is_derived_cls(cls) -> bool:
        """Return True if `cls` is derived from other class(es)."""
        return not cls.is_base_cls()

    def __mul__(cls, other: Union['ClassWithDefinitionMeta', ClassDefT]) \
            -> ClassDefT:
        """Return class definition: `cls` * `other`."""
        if isinstance(other, ClassWithDefinitionMeta):
            return ClassDefT(((cls, 1), (other, 1)))
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta)
                    for (elem, exp) in other)):
                return ClassDefT(((cls, 1),)) * other
        return NotImplemented

    def __rmul__(cls, other: ClassDefT) -> ClassDefT:
        """Return class definition: `other` * `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta)
                    for (elem, exp) in other)):
                return other * ClassDefT(((cls, 1),))
        return NotImplemented

    def __truediv__(cls, other: Union['ClassWithDefinitionMeta',
                                      ClassDefT]) -> ClassDefT:
        """Return class definition: `cls` / `other`."""
        if isinstance(other, ClassWithDefinitionMeta):
            return ClassDefT(((cls, 1), (other, -1)))
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta) for (elem, exp) in other)):
                return ClassDefT(((cls, 1),)) * other.reciprocal()
        return NotImplemented

    def __rtruediv__(cls, other: ClassDefT) -> ClassDefT:
        """Return class definition: `other` / `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta)
                    for (elem, exp) in other)):
                return other * ClassDefT(((cls, -1),))
        return NotImplemented

    def __pow__(cls, exp: int) -> ClassDefT:
        """Return class definition: `cls` ** `exp`."""
        if isinstance(exp, Integral):
            return ClassDefT(((cls, exp),))
        return NotImplemented

    def __str__(cls) -> str:
        return cls.__name__

    # implement abstract methods of NonNumTermElem to allow instances of
    # ClassWithDefinitionMeta to be elements in terms:

    is_base_elem = is_base_cls

    def norm_sort_key(cls) -> int:
        """Return sort key for `cls` used for normalization of terms."""
        return hash(cls)

    def _get_factor(cls, other: Any) -> int:
        """Instances are not convertable, raise TypeError."""
        raise TypeError