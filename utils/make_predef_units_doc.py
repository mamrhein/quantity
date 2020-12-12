# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from quantity.predefined import *


COLWIDTH = (6, 25, 20, 20)


def printHeader(cls):
    name = cls.__name__
    print()
    print(name)
    print('-' * len(name))
    if cls._clsDefinition:
        print()
        print("Definition: %s" % cls._clsDefinition)


def printRefUnit(refUnit):
    print()
    print("Reference unit: %s ('%s')" % (refUnit.name, refUnit.symbol))


def printColMarker():
    print("=" * COLWIDTH[0],
          "=" * COLWIDTH[1],
          "=" * COLWIDTH[2],
          "=" * COLWIDTH[3])


def printUnitListHeader(sym):
    print()
    print("Predefined units:")
    print()
    printColMarker()
    print(format("Symbol", '<%i' % COLWIDTH[0]),
          format("Name", '<%i' % COLWIDTH[1]),
          format("Definition", '<%i' % COLWIDTH[2]),
          format("Equivalent in '%s'" % sym, '<%i' % (COLWIDTH[3])))
    printColMarker()


def printUnitLine(unit, equiv):
    print(format(unit.symbol, '<%i' % COLWIDTH[0]),
          format(unit.name, '<%i' % COLWIDTH[1]),
          format(unit.definition, '<%i' % COLWIDTH[2]),
          format(equiv, '<%i' % (COLWIDTH[3])))


def printUnitListFooter():
    printColMarker()


localdict = dict(locals())
qtyClsList = [cls for cls in localdict.itervalues()
              if isinstance(cls, type) and issubclass(cls, Quantity)
              and cls.__name__ != 'Quantity']
unitClsList = [cls.Unit for cls in sorted(qtyClsList,
                                          key=lambda cls: cls._regIdx)]

for unitCls in unitClsList:
    qtyCls = unitCls.Quantity
    printHeader(qtyCls)
    refUnit = unitCls.refUnit
    if refUnit:
        printRefUnit(refUnit)
        unitList = [unit for unit in sorted(unitCls.registeredUnits(),
                                            key=lambda unit: refUnit(unit))
                    if unit is not refUnit]
        if unitList:
            printUnitListHeader(refUnit.symbol)
            for unit in unitList:
                equiv = refUnit(unit)
                printUnitLine(unit, equiv)
            printUnitListFooter()
    else:
        unitList = [unit for unit in sorted(unitCls.registeredUnits(),
                                            key=lambda unit: unit.symbol)]
        if unitList:
            printUnitListHeader('')
            for unit in unitList:
                printUnitLine(unit, '')
            printUnitListFooter()
