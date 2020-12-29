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
from functools import partial
from numbers import Integral
from typing import Any, Dict, Optional, Tuple, Union

# Local imports
from .registry import DefinedItemRegistry, Term


class ClassWithDefinitionMeta(type):

    """Meta class allowing to construct classes with terms as definitions."""

    def __init__(cls, name: str, bases: Tuple[type, ...],
                 clsdict: Dict[str, Any]):
        definition: Optional[Term] = clsdict.pop('define_as', None)
        super().__init__(name, bases, clsdict)
        # check definition
        if definition is not None:
            assert isinstance(definition, Term), \
                "Definition given in 'define_as' must be an instance of " \
                "'Term'"
            assert all(isinstance(elem, cls.__class__)
                       for elem, _ in definition), \
                "All elements of definition given in 'define_as' must be " \
                f"instances of '{cls.__class__.__name__}'."
        cls._definition = definition
        # register cls
        cls._reg_id = _register_cls(cls)

    @property
    def definition(cls) -> Term:
        """Definition of `cls`."""
        if cls._definition is None:
            return Term(((cls, 1),))
        return cls._definition

    def is_base_cls(cls) -> bool:
        """Return True if `cls` is not derived from other class(es)."""
        # base class -> definition is None or empty term
        return cls._definition is None or len(cls._definition) == 0

    @property
    def normalized_definition(cls) -> Term:
        """Normalized definition of `cls`."""
        try:
            return cls._definition.normalized()
        except AttributeError:
            return cls.definition

    def is_derived_cls(cls) -> bool:
        """Return True if `cls` is derived from other class(es)."""
        return not cls.is_base_cls()

    def __mul__(cls, other: Union['ClassWithDefinitionMeta', Term]) -> Term:
        """Return class definition: `cls` * `other`."""
        if isinstance(other, ClassWithDefinitionMeta):
            return Term(((cls, 1), (other, 1)))
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta) for (elem, exp) in other)):
                return Term(((cls, 1),)) * other
        return NotImplemented

    def __rmul__(cls, other: Term) -> Term:
        """Return class definition: `other` * `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta) for (elem, exp) in other)):
                return other * Term(((cls, 1),))
        return NotImplemented

    def __truediv__(cls, other: Union['ClassWithDefinitionMeta', Term]) -> Term:
        """Return class definition: `cls` / `other`."""
        if isinstance(other, ClassWithDefinitionMeta):
            return Term(((cls, 1), (other, -1)))
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta) for (elem, exp) in other)):
                return Term(((cls, 1),)) * other.reciprocal()
        return NotImplemented

    def __rtruediv__(cls, other: Term) -> Term:
        """Return class definition: `other` / `cls`."""
        if isinstance(other, Term):
            if all((isinstance(elem, ClassWithDefinitionMeta) for (elem, exp) in other)):
                return other * Term(((cls, -1),))
        return NotImplemented

    def __pow__(cls, exp: int) -> Term:
        """Return class definition: `cls` ** `exp`."""
        if isinstance(exp, Integral):
            return Term(((cls, exp),))
        return NotImplemented

    def __str__(cls) -> str:
        return cls.__name__

    # implement abstract methods of NonNumTermElem to allow instances of
    # ClassWithDefinitionMeta to be elements in terms:

    is_base_elem = is_base_cls

    def norm_sort_key(cls) -> int:
        """Return sort key for `cls` used for normalization of terms."""
        return cls._reg_id

    def _get_factor(cls, other: Any) -> int:
        """Instances are not convertable, raise TypeError."""
        raise TypeError


# Global registry of Quantities
_registry = DefinedItemRegistry()

_register_cls = partial(DefinedItemRegistry.register_item,
                        _registry)
