# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        money (package)
## Purpose:     Currency-safe computations with money amounts.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2013 ff. Michael Amrhein
## License:     This program is part of a larger application. For license
##              details please read the file LICENSE.TXT provided together
##              with the application.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Currency-safe computations with money amounts.

Money derives from Quantity, so all operations on quantities can also be
apllied to instances of Money. All amounts of money are rounded according to
the smallest fraction defined for the currency.
"""


from __future__ import absolute_import, division, unicode_literals
from .moneybase import Currency, Money, ExchangeRate
from .currencies import getCurrencyInfo, registerCurrency


__metaclass__ = type


__all__ = [
    'Currency',
    'Money',
    'ExchangeRate',
    'getCurrencyInfo',
    'registerCurrency',
]
