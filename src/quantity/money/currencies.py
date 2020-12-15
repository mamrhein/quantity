# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        currencies
# Purpose:     Provide dict of currencies based on ISO 4217
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2015 Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Provide dict of currencies based on ISO 4217."""


import os.path
from xml.etree import ElementTree

from .moneybase import Currency

# Create currency dict from ISO 4217 xml file
iso_4217_file_name = "iso_4217.xml"
_fpath = os.path.join(os.path.dirname(__file__), iso_4217_file_name)
_xmltree = ElementTree.parse(_fpath)
_root = _xmltree.getroot()

published = f"{_root.attrib['Pblshd']}"

_currencyDict = {}

for entry in _root.findall("CcyTbl/CcyNtry"):
    descr = [elem.text for elem in iter(entry)]
    if len(descr) == 5:
        country, name, isoCode, isoNumCode, minorUnits = descr
        if minorUnits.isdigit():
            try:
                currEntry = _currencyDict[isoCode]
            except KeyError:
                _currencyDict[isoCode] = (isoCode, int(isoNumCode), name,
                                          int(minorUnits), [country])
            else:
                currEntry[4].append(country)


def getCurrencyInfo(isoCode):
    """Return infos from ISO 4217 currency database.

    Args:
        isoCode (str): ISO 4217 3-character code for the currency to be
            looked-up

    Returns:
        tuple: 3-character code, numerical code, name, minorUnit and list of
            countries which use the currency as functional currency

    Raises:
        ValueError: currency with code `isoCode` not in database

    .. note::
        The database available here does only include entries from ISO 4217
        which are used as functional currency, not those used for bond
        markets, noble metals and testing purposes.
    """
    try:
        return _currencyDict[isoCode]
    except KeyError:
        raise ValueError("Unknown ISO 4217 code: '%s'." % isoCode)


def registerCurrency(isoCode):
    """Register the currency with code `isoCode` from ISO 4217 database.

    Args:
        isoCode (string): ISO 4217 3-character code for the currency to be
            registered

    Returns:
        :class:`Currency`: registered currency

    Raises:
        ValueError: currency with code `isoCode` not in database
    """
    regCurrency = Currency.getUnitBySymbol(isoCode)
    if regCurrency is not None:         # currency already registered
        return regCurrency
    isoCode, isoNumCode, name, minorUnit, countries = getCurrencyInfo(isoCode)
    return Currency(isoCode, name, minorUnit)
