# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright:   (c) 2015 ff. Michael Amrhein (michael@adrhinum.de)
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Provide dict of currencies based on ISO 4217."""


import os.path
from typing import List, MutableMapping, Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

CurrencyInfoT = Tuple[str, int, str, int, List[str]]
CurrencyDictT = MutableMapping[str, CurrencyInfoT]

_currency_dict: CurrencyDictT = {}

# Create currency dict from ISO 4217 xml file
iso_4217_file_name = "iso_4217.xml"
_fpath = os.path.join(os.path.dirname(__file__), iso_4217_file_name)
_xmltree = ElementTree.parse(_fpath)
_root = _xmltree.getroot()

published = f"{_root.attrib['Pblshd']}"

for entry in _root.findall("CcyTbl/CcyNtry"):
    elem: Element
    descr: List[str] = [elem.text or "" for elem in iter(entry)]
    if len(descr) == 5:
        country, name, iso_code, iso_num_code, minor_units = descr
        if iso_num_code.isdigit() and minor_units.isdigit():
            try:
                curr_entry = _currency_dict[iso_code]
            except KeyError:
                _currency_dict[iso_code] = (iso_code, int(iso_num_code), name,
                                            int(minor_units), [country])
            else:
                curr_entry[4].append(country)


def get_currency_info(iso_code: str) -> CurrencyInfoT:
    """Return infos from ISO 4217 currency database.

    Args:
        iso_code (str): ISO 4217 3-character code for the currency to be
            looked-up

    Returns:
        tuple: 3-character code, numerical code, name, minor unit and list of
            countries which use the currency as functional currency

    Raises:
        ValueError: currency with code `iso_code` not in database

    .. note::
        The database available here does only include entries from ISO 4217
        which are used as functional currency, not those used for bond
        markets, noble metals and testing purposes.
    """
    try:
        return _currency_dict[iso_code]
    except KeyError:
        raise ValueError(f"Unknown ISO 4217 code: '{iso_code}'.")
