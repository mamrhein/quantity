# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from xml.etree import ElementTree


fname = 'quantity/money/iso_4217_a1.xml'

xmltree = ElementTree.parse(fname)
root = xmltree.getroot()

_currencyDict = {}

for entry in root.findall('CcyTbl/CcyNtry'):
    descr = [elem.text for elem in iter(entry)]
    if len(descr) == 5:
        country, name, isoCode, isoNumCode, minorUnits = descr
        if minorUnits.isdigit():
            try:
                currEntry = _currencyDict[isoCode]
            except KeyError:
                _currencyDict[isoCode] = (isoCode, isoNumCode, name,
                                          minorUnits, [country])
            else:
                currEntry[4].append(country)


print("published = '%s'\n" % root.attrib['Pblshd'])

print("_currencyDict = {")

for key in sorted(_currencyDict):
    isoCode, isoNumCode, name, minorUnits, countries = _currencyDict[key]
    print("    '%s': ('%s', %s, '%s', %s,\n            %s)," %
          (isoCode, isoCode, int(isoNumCode), name, minorUnits,
           sorted(countries)))
