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


"""Utility functions."""


# Standard library imports
from builtins import sum as builtin_sum
from typing import Any, Iterable

# Third-party imports

# Local imports


def sum(items: Iterable, start: Any = None):
    """sum(items[, start]) -> value

    Args:
        items: iterable of numbers or number-like objects (NOT strings)
        start: starting value to be added (default: None)

    Returns:
        sum of all elements in `items` plus the value of `start` (if not
        None). When `items` is empty, returns `start`, if not None,
        otherwise 0.

    In contrast to the built-in function 'sum' this function allows to sum
    sequences of number-like objects (like quantities) without having to
    provide a start value.
    """
    it = iter(items)
    if start is None:
        try:
            start = next(it)
        except StopIteration:
            # return 0 in order to be backwards compatible
            return 0
    return builtin_sum(it, start)
