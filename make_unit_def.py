# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimalfp import Decimal

# helpers for defining units

from collections import namedtuple
DecimalScaleFactor = namedtuple('DecimalScaleFactor', ['name', 'abbr', 'exp'])

MICRO = DecimalScaleFactor('Micro', 'µ', -6)
MILLI = DecimalScaleFactor('Milli', 'm', -3)
CENTI = DecimalScaleFactor('Centi', 'c', -2)
DECI = DecimalScaleFactor('Deci', 'd', -1)
KILO = DecimalScaleFactor('Kilo', 'k', 3)
MEGA = DecimalScaleFactor('Mega', 'M', 6)
GIGA = DecimalScaleFactor('Giga', 'G', 9)
TERA = DecimalScaleFactor('Tera', 'T', 12)


def make_unit_def(clsName, baseSym, baseName, *scales):
    for scale in scales:
        varname = '%s%s' % (scale.name.upper(), baseName.upper())
        name = '%s%s' % (scale.name, baseName.lower())
        symbol = '%s%s' % (scale.abbr, baseSym)
        print("%s = %s.Unit('%s', '%s', %s * %s)"
              % (varname, clsName, symbol, name,
                 repr(Decimal(10) ** scale.exp), baseName.upper()))
