# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2021 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Provisional typing support for Rational numbers."""

# Standard library imports
import sys
from abc import abstractmethod
from typing import Any
if sys.version_info >= (3, 8):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable

# Third-party imports
from decimalfp import Decimal

# Local imports


@runtime_checkable
class Rational(Protocol):
    """Protocol for rational numbers."""

    @abstractmethod
    def __abs__(self):
        """abs(self)"""

    @abstractmethod
    def __mul__(self, other):
        """self * other"""

    @abstractmethod
    def __truediv__(self, other):
        """self / other"""

    @abstractmethod
    def __pow__(self, exponent):
        """self ** exponent"""

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """self == other"""

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """self < other"""

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        """self <= other"""

    @abstractmethod
    def __hash__(self) -> int:
        """hash(self)"""


ONE = Decimal(1)
