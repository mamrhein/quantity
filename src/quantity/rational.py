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

from __future__ import annotations

import sys
from abc import abstractmethod
from typing import Any, Optional, Union

if sys.version_info >= (3, 8):
    from typing import Protocol, runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable

from decimalfp import Decimal


@runtime_checkable
class RationalT(Protocol):
    """Protocol for rational numbers."""

    @abstractmethod
    def __abs__(self) -> RationalT:
        """abs(self)"""

    @abstractmethod
    def __add__(self, other) -> RationalT:
        """self + other"""

    @abstractmethod
    def __sub__(self, other) -> RationalT:
        """self - other"""

    @abstractmethod
    def __mul__(self, other) -> RationalT:
        """self * other"""

    @abstractmethod
    def __truediv__(self, other) -> RationalT:
        """self / other"""

    @abstractmethod
    def __pow__(self, exponent) -> RationalT:
        """self ** exponent"""

    @abstractmethod
    def __round__(self, n_digits: Optional[int]) -> Union[int, RationalT]:
        """round(self)"""

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
