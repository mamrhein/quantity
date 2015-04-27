# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        money (package)
## Purpose:     Currency-safe computations with money amounts.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2013 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Currency-safe computations with money amounts.

Money derives from Quantity, so all operations on quantities can also be
apllied to instances of Money. All amounts of money are rounded according to
the smallest fraction defined for the currency.
"""


from __future__ import absolute_import
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
