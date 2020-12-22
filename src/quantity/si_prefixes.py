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


"""SI metric prefixes."""

# Standard library imports
from collections import namedtuple

# Third-party imports
from decimalfp import Decimal


SIPrefix = namedtuple('SIPrefix', ['name', 'abbr', 'exp'])

SIPrefix.factor = property(fget=lambda self: Decimal(10) ** self.exp,
                           doc="Scale factor")

SIPrefix.__mul__ = lambda self, other: self.factor * other
SIPrefix.__rmul__ = SIPrefix.__mul__


YOCTO = SIPrefix('Yocto', 'y', -24)
ZEPTO = SIPrefix('Zepto', 'z', -21)
ATTO = SIPrefix('Atto', 'a', -18)
FEMTO = SIPrefix('Femto', 'f', -15)
PICO = SIPrefix('Pico', 'p', -12)
NANO = SIPrefix('Nano', 'n', -9)
MICRO = SIPrefix('Micro', 'μ', -6)
MILLI = SIPrefix('Milli', 'm', -3)
CENTI = SIPrefix('Centi', 'c', -2)
DECI = SIPrefix('Deci', 'd', -1)
DECA = SIPrefix('Deca', 'da', 1)
HECTO = SIPrefix('Hecto', 'h', 2)
KILO = SIPrefix('Kilo', 'k', 3)
MEGA = SIPrefix('Mega', 'M', 6)
GIGA = SIPrefix('Giga', 'G', 9)
TERA = SIPrefix('Tera', 'T', 12)
PETA = SIPrefix('Peta', 'P', 15)
EXA = SIPrefix('Exa', 'E', 18)
ZETTA = SIPrefix('Zetta', 'Z', 21)
YOTTA = SIPrefix('Yotta', 'Y', 24)
