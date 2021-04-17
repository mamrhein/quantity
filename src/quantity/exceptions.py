# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        exceptions
# Purpose:     Provide quantity specific exceptions
#
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


"""Quantity specific exceptions."""

import operator
from typing import Any, Callable


class QuantityError(ValueError):
    """Raised when a quantity can not be instanciated."""


class IncompatibleUnitsError(QuantityError):
    """Raised when operands do not have compatible units."""

    def __init__(self, msg: str, operand1: Any, operand2: Any):
        QuantityError.__init__(self, msg % (operand1, operand2))


class UndefinedResultError(QuantityError):
    """Raised when operation results in an undefined quantity."""

    _op_syms = {
        operator.mul: '*',
        operator.truediv: '/',
        operator.floordiv: '//',
        operator.mod: '%',
        operator.pow: '**'
        }

    def __init__(self, op: Callable[[Any, Any], Any],
                 operand1: Any, operand2: Any):
        msg = f"Undefined result: '{operand1}' {self._op_syms[op]} '" \
              f"{operand2}'"
        QuantityError.__init__(self, msg)


class UnitConversionError(QuantityError):
    """Raised when a conversion between two compatible units fails."""

    def __init__(self, msg: str, from_unit: Any, to_unit: Any):
        QuantityError.__init__(self, msg % (from_unit, to_unit))
