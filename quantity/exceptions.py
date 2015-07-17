# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        exceptions
## Purpose:     Provide quantity specific exceptions
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


"""Quantity specific exceptions."""

from __future__ import absolute_import, division, unicode_literals
import operator


__metaclass__ = type


class QuantityError(TypeError):

    """Exception raised when a quantity can not not be instanciated with the
    given parameters."""


class IncompatibleUnitsError(QuantityError):

    """Exception raised when operands do not have compatible units."""

    def __init__(self, msg, operand1, operand2):
        if not isinstance(operand1, type):
            operand1 = operand1.__class__.__name__
        if not isinstance(operand2, type):
            operand2 = operand2.__class__.__name__
        QuantityError.__init__(self, msg % (operand1, operand2))


class UndefinedResultError(QuantityError):

    """Exception raised when operation results in an undefined quantity."""

    opSym = {operator.mul: '*',
             operator.truediv: '/',
             operator.floordiv: '//',
             operator.mod: '%',
             operator.pow: '**'
             }

    def __init__(self, op, operand1, operand2):
        if not isinstance(operand1, type):
            operand1 = operand1.__class__.__name__
        if not isinstance(operand2, type):
            operand2 = operand2.__class__.__name__
        QuantityError.__init__(self, "Undefined result: %s %s %s" %
                               (operand1, self.opSym[op], operand2))


class UnitConversionError(QuantityError):

    """Exception raised when a conversion between two compatible units
    fails."""

    def __init__(self, msg, fromUnit, toUnit):
        QuantityError.__init__(self, msg % (fromUnit, toUnit))
