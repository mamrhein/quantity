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

# Third-party imports
from decimalfp import Decimal


class SIPrefix:

    """Prefix used to scale SI units."""

    def __init__(self, name: str, abbr: str, exp: int):
        self.name = name
        self.abbr = abbr
        self.exp = exp

    @property
    def factor(self) -> Decimal:
        """Scale factor"""
        return Decimal(10) ** self.exp  # type: ignore


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

SI_PREFIXES = [
    YOCTO,
    ZEPTO,
    ATTO,
    FEMTO,
    PICO,
    NANO,
    MICRO,
    MILLI,
    CENTI,
    DECI,
    DECA,
    HECTO,
    KILO,
    MEGA,
    GIGA,
    TERA,
    PETA,
    EXA,
    ZETTA,
    YOTTA,
]

SI_PREFIX_MAP = {prefix.factor: prefix for prefix in SI_PREFIXES}
