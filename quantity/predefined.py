# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        quantities.predefined
## Purpose:     Define commonly used quantities.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


r"""Defines commonly used quantities.

Length
^^^^^^

Reference unit: Metre ('m')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm'
====== ========================= ==================== ====================
µm     Micrometre                0.000001·m           0.000001
mm     Millimetre                0.001·m              0.001
cm     Centimetre                0.01·m               0.01
in     Inch                      2.54·cm              0.0254
dm     Decimetre                 0.1·m                0.1
ft     Foot                      12·in                0.3048
yd     Yard                      3·ft                 0.9144
ch     Chain                     22·yd                20.1168
fur    Furlog                    10·ch                201.1680
km     Kilometre                 1000·m               1000
mi     Mile                      8·fur                1609.3440
====== ========================= ==================== ====================

Mass
^^^^

Reference unit: Kilogram ('kg')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'kg'
====== ========================= ==================== ====================
mg     Milligram                 0.000001·kg          0.000001
ct     Carat                     0.2·g                0.0002
g      Gram                      0.001·kg             0.001
oz     Ounce                     0.0625·lb            0.028349523125
lb     Pound                     0.45359237·kg        0.45359237
st     Stone                     14·lb                6.35029318
t      Tonne                     1000·kg              1000
====== ========================= ==================== ====================

Duration
^^^^^^^^

Reference unit: Second ('s')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 's'
====== ========================= ==================== ====================
min    Minute                    60·s                 60
h      Hour                      60·min               3600
d      Day                       24·h                 86400
====== ========================= ==================== ====================

Area
^^^^

Definition: Length²

Reference unit: Square Metre ('m²')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm²'
====== ========================= ==================== ====================
mm²    Square Millimetre         mm²                  0.000001
cm²    Square Centimetre         cm²                  0.0001
in²    Square Inch               in²                  0.00064516
dm²    Square Decimetre          dm²                  0.01
ft²    Square Foot               ft²                  0.09290304
yd²    Square Yard               yd²                  0.83612736
a      Are                       100·m²               100
ac     Acre                      4840·yd²             4046.85642240
ha     Hectare                   100·a                10000
km²    Square Kilometre          km²                  1000000
mi²    Square Mile               mi²                  2589988.11033600
====== ========================= ==================== ====================

Volume
^^^^^^

Definition: Length³

Reference unit: Cubic Metre ('m³')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm³'
====== ========================= ==================== ====================
mm³    Cubic Millimetre          mm³                  0.000000001
ml     Millilitre                0.001·l              0.000001
cm³    Cubic Centimetre          cm³                  0.000001
cl     Centilitre                0.01·l               0.00001
in³    Cubic Inch                in³                  0.000016387064
dl     Decilitre                 0.1·l                0.0001
l      Litre                     0.001·m³             0.001
dm³    Cubic Decimetre           dm³                  0.001
ft³    Cubic Foot                ft³                  0.028316846592
yd³    Cubic Yard                yd³                  0.764554857984
km³    Cubic Kilometre           km³                  1000000000
====== ========================= ==================== ====================

Velocity
^^^^^^^^

Definition: Length/Duration

Reference unit: Metre per Second ('m/s')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm/s'
====== ========================= ==================== ====================
km/h   Kilometre per hour        km/h                 5/18
ft/s   Foot per Second           ft/s                 0.3048
mph    Mile per Hour             mi/h                 0.44704
====== ========================= ==================== ====================

Acceleration
^^^^^^^^^^^^

Definition: Length/Duration²

Reference unit: Metre per Second squared ('m/s²')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm/s²'
====== ========================= ==================== ====================
mps²   Mile per Second squared   mi/s²                1609.3440
====== ========================= ==================== ====================

Force
^^^^^

Definition: Mass·Acceleration

Reference unit: Newton ('N')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'N'
====== ========================= ==================== ====================
J/m    Joule per Metre           J/m                  1
====== ========================= ==================== ====================

Energy
^^^^^^

Definition: Length·Force

Reference unit: Joule ('J')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'J'
====== ========================= ==================== ====================
Ws     Watt Second               s·W                  1
kWh    Kilowatt Hour             h·kW                 3600000
====== ========================= ==================== ====================

Power
^^^^^

Definition: Energy/Duration

Reference unit: Watt ('W')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'W'
====== ========================= ==================== ====================
mW     Milliwatt                 0.001·W              0.001
kW     Kilowatt                  1000·W               1000
MW     Megawatt                  1000000·W            1000000
GW     Gigawatt                  1000000000·W         1000000000
TW     Terawatt                  1000000000000·W      1000000000000
====== ========================= ==================== ====================

DataVolume
^^^^^^^^^^

Reference unit: Byte ('B')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'B'
====== ========================= ==================== ====================
b      Bit                       1·B/8                0.125
kb     Kilobit                   1000·b               125
Kib    Kibibit                   1024·b               128
kB     Kilobyte                  1000·B               1000
KiB    Kibibyte                  1024·B               1024
Mb     Megabit                   1000000·b            125000
Mib    Mebibit                   1048576·b            131072
MB     Megabyte                  1000000·B            1000000
MiB    Mebibyte                  1048576·B            1048576
Gb     Gigabit                   1000000000·b         125000000
Gib    Gibibit                   1073741824·b         134217728
GB     Gigabyte                  1000000000·B         1000000000
GiB    Gibibyte                  1073741824·B         1073741824
Tb     Terabit                   1000000000000·b      125000000000
Tib    Tebibit                   1099511627776·b      137438953472
TB     Terabyte                  1000000000000·B      1000000000000
TiB    Tebibyte                  1099511627776·B      1099511627776
====== ========================= ==================== ====================

DataThroughput
^^^^^^^^^^^^--

Definition: DataVolume/Duration

Reference unit: Byte per Second ('B/s')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'B/s'
====== ========================= ==================== ====================
b/s    Bit per Second            b/s                  0.125
kb/s   Kilobit per Second        1000·b/s             125
Kib/s  Kibibit per Second        1024·b/s             128
kB/s   Kilobyte per Second       1000·B/s             1000
KiB/s  Kibibyte per Second       1024·B/s             1024
Mb/s   Megabit per Second        1000000·b/s          125000
Mib/s  Mebibit per Second        1048576·b/s          131072
MB/s   Megabyte per Second       1000000·B/s          1000000
MiB/s  Mebibyte per Second       1048576·B/s          1048576
Gb/s   Gigabit per Second        1000000000·b/s       125000000
Gib/s  Gibibit per Second        1073741824·b/s       134217728
GB/s   Gigabyte per Second       1000000000·B/s       1000000000
GiB/s  Gibibyte per Second       1073741824·B/s       1073741824
Tb/s   Terabit per Second        1000000000000·b/s    125000000000
Tib/s  Tebibit per Second        1099511627776·b/s    137438953472
TB/s   Terabyte per Second       1000000000000·B/s    1000000000000
TiB/s  Tebibyte per Second       1099511627776·B/s    1099511627776
====== ========================= ==================== ====================

Temperature
^^^^^^^^^^^

Predefined units:

====== ========================= =============================
Symbol Name                      Equivalents
====== ========================= =============================
°C     Degree Celsius            0 °C = 32 °F = 273,25 K
°F     Degree Fahrenheit         0 °F ≅ -17.778 °C ≅ 255.372 K
K      Kelvin                    0 K = -273,25 °C = -459.67 °F
====== ========================= =============================

Temperature units are converted using the following formulas:

========== =========================== =========================== ===========================
from \\ to Celsius                     Fahrenheit                  Kelvin
========== =========================== =========================== ===========================
Celsius    -                           [°F] = [°C] * 9/5 + 32      [K] = [°C] + 273.15
Fahrenheit [°C] = ([°F] - 32) * 5/9    -                           [K] = ([°F] + 459.67) * 5/9
Kelvin     [°C] = [K] - 273.15         [°F] = [K] * 9/5 - 459.67   -
========== =========================== =========================== ===========================
"""

from __future__ import absolute_import, division, unicode_literals
from fractions import Fraction
from decimalfp import Decimal
from . import Quantity, TableConverter

__metaclass__ = type


class Length(Quantity):
    refUnitName = 'Metre'
    refUnitSymbol = 'm'

METRE = Length.refUnit

MICROMETRE = Length.Unit('µm', 'Micrometre', Decimal('0.000001') * METRE)
MILLIMETRE = Length.Unit('mm', 'Millimetre', Decimal('0.001') * METRE)
CENTIMETRE = Length.Unit('cm', 'Centimetre', Decimal('0.01') * METRE)
DECIMETRE = Length.Unit('dm', 'Decimetre', Decimal('0.1') * METRE)
KILOMETRE = Length.Unit('km', 'Kilometre', Decimal(1000) * METRE)

# some imperial units
INCH = Length.Unit('in', 'Inch', Decimal('2.54') * CENTIMETRE)
FOOT = Length.Unit('ft', 'Foot', Decimal(12) * INCH)
YARD = Length.Unit('yd', 'Yard', Decimal(3) * FOOT)
CHAIN = Length.Unit('ch', 'Chain', Decimal(22) * YARD)
FURLONG = Length.Unit('fur', 'Furlog', Decimal(10) * CHAIN)
MILE = Length.Unit('mi', 'Mile', Decimal(8) * FURLONG)


class Mass(Quantity):
    refUnitName = 'Kilogram'
    refUnitSymbol = 'kg'

KILOGRAM = Mass.refUnit

GRAM = Mass.Unit('g', 'Gram', Decimal('0.001') * KILOGRAM)
MILLIGRAM = Mass.Unit('mg', 'Milligram', Decimal('0.000001') * KILOGRAM)
TONNE = Mass.Unit('t', 'Tonne', Decimal(1000) * KILOGRAM)

# some imperial units
POUND = Mass.Unit('lb', 'Pound', Decimal('0.45359237') * KILOGRAM)
STONE = Mass.Unit('st', 'Stone', Decimal(14) * POUND)
OUNCE = Mass.Unit('oz', 'Ounce', Decimal('0.0625') * POUND)

# others
CARAT = Mass.Unit('ct', 'Carat', Decimal('0.2') * GRAM)


class Duration(Quantity):
    refUnitName = 'Second'
    refUnitSymbol = 's'

SECOND = Duration.refUnit

MINUTE = Duration.Unit('min', 'Minute', Decimal(60) * SECOND)
HOUR = Duration.Unit('h', 'Hour', Decimal(60) * MINUTE)
DAY = Duration.Unit('d', 'Day', Decimal(24) * HOUR)


class Area(Quantity):
    defineAs = Length ** 2
    refUnitName = 'Square Metre'

SQUARE_METRE = Area.refUnit

SQUARE_MILLIMETRE = Area.Unit('mm²', 'Square Millimetre', MILLIMETRE ** 2)
SQUARE_CENTIMETRE = Area.Unit('cm²', 'Square Centimetre', CENTIMETRE ** 2)
SQUARE_DECIMETRE = Area.Unit('dm²', 'Square Decimetre', DECIMETRE ** 2)
SQUARE_KILOMETRE = Area.Unit('km²', 'Square Kilometre', KILOMETRE ** 2)
ARE = Area.Unit('a', 'Are', Decimal(100) * SQUARE_METRE)
HECTARE = Area.Unit('ha', 'Hectare', Decimal(100) * ARE)


# some imperial units
SQUARE_INCH = Area.Unit('in²', 'Square Inch', INCH ** 2)
SQUARE_FOOT = Area.Unit('ft²', 'Square Foot', FOOT ** 2)
SQUARE_YARD = Area.Unit('yd²', 'Square Yard', YARD ** 2)
SQUARE_MILE = Area.Unit('mi²', 'Square Mile', MILE ** 2)
ACRE = Area.Unit('ac', 'Acre', Decimal(4840) * SQUARE_YARD)


class Volume(Quantity):
    defineAs = Length ** 3
    refUnitName = 'Cubic Metre'

CUBIC_METRE = Volume.refUnit

CUBIC_MILLIMETRE = Volume.Unit('mm³', 'Cubic Millimetre', MILLIMETRE ** 3)
CUBIC_CENTIMETRE = Volume.Unit('cm³', 'Cubic Centimetre', CENTIMETRE ** 3)
CUBIC_DECIMETRE = Volume.Unit('dm³', 'Cubic Decimetre', DECIMETRE ** 3)
CUBIC_KILOMETRE = Volume.Unit('km³', 'Cubic Kilometre', KILOMETRE ** 3)

# litre
LITRE = Volume.Unit('l', 'Litre', Decimal('0.1') ** 3 * CUBIC_METRE)
MILLILITRE = Volume.Unit('ml', 'Millilitre', Decimal('0.001') * LITRE)
CENTILITRE = Volume.Unit('cl', 'Centilitre', Decimal('0.01') * LITRE)
DECILITRE = Volume.Unit('dl', 'Decilitre', Decimal('0.1') * LITRE)

# some imperial units
CUBIC_INCH = Volume.Unit('in³', 'Cubic Inch', INCH ** 3)
CUBIC_FOOT = Volume.Unit('ft³', 'Cubic Foot', FOOT ** 3)
CUBIC_YARD = Volume.Unit('yd³', 'Cubic Yard', YARD ** 3)


class Velocity(Quantity):
    defineAs = Length / Duration
    refUnitName = 'Metre per Second'

METRE_PER_SECOND = Velocity.refUnit
KILOMETRE_PER_HOUR = Velocity.Unit('km/h', 'Kilometre per hour',
                                   KILOMETRE / HOUR)

# some imperial units
FOOT_PER_SECOND = Velocity.Unit('ft/s', 'Foot per Second', FOOT / SECOND)
MILE_PER_HOUR = Velocity.Unit('mph', 'Mile per Hour', MILE / HOUR)


class Acceleration(Quantity):
    defineAs = Length / Duration ** 2
    refUnitName = 'Metre per Second squared'

METRE_PER_SECOND_SQUARED = Acceleration.refUnit

# some imperial units
MILE_PER_SECOND_SQUARED = Acceleration.Unit('mps²',
                                            'Mile per Second squared',
                                            MILE / SECOND ** 2)


class Force(Quantity):
    defineAs = Mass * Acceleration
    refUnitName = 'Newton'
    refUnitSymbol = 'N'

NEWTON = Force.refUnit


class Energy(Quantity):
    defineAs = Force * Length
    refUnitName = 'Joule'
    refUnitSymbol = 'J'

JOULE = Energy.refUnit


class Power(Quantity):
    defineAs = Energy / Duration
    refUnitName = 'Watt'
    refUnitSymbol = 'W'

WATT = Power.refUnit

MILLIWATT = Power.Unit('mW', 'Milliwatt', Decimal('0.001') * WATT)
KILOWATT = Power.Unit('kW', 'Kilowatt', Decimal(1000) * WATT)
MEGAWATT = Power.Unit('MW', 'Megawatt', Decimal(1000000) * WATT)
GIGAWATT = Power.Unit('GW', 'Gigawatt', Decimal(1000000000) * WATT)
TERAWATT = Power.Unit('TW', 'Terawatt', Decimal(1000000000000) * WATT)


# some more unit definitions based on other than the reference units

# Force
JOULE_PER_METRE = Force.Unit('J/m', 'Joule per Metre', JOULE / METRE)

# Energy
WATT_SECOND = Energy.Unit('Ws', 'Watt Second', WATT * SECOND)
KILOWATT_HOUR = Energy.Unit('kWh', 'Kilowatt Hour', KILOWATT * HOUR)


class DataVolume(Quantity):
    """According to IEEE 1541-2002"""
    refUnitName = 'Byte'
    refUnitSymbol = 'B'
    quantum = Fraction(1, 8)

BYTE = DataVolume.refUnit

KILOBYTE = DataVolume.Unit('kB', 'Kilobyte', Decimal(10) ** 3 * BYTE)
MEGABYTE = DataVolume.Unit('MB', 'Megabyte', Decimal(10) ** 6 * BYTE)
GIGABYTE = DataVolume.Unit('GB', 'Gigabyte', Decimal(10) ** 9 * BYTE)
TERABYTE = DataVolume.Unit('TB', 'Terabyte', Decimal(10) ** 12 * BYTE)
KIBIBYTE = DataVolume.Unit('KiB', 'Kibibyte', Decimal(2) ** 10 * BYTE)
MEBIBYTE = DataVolume.Unit('MiB', 'Mebibyte', Decimal(2) ** 20 * BYTE)
GIBIBYTE = DataVolume.Unit('GiB', 'Gibibyte', Decimal(2) ** 30 * BYTE)
TEBIBYTE = DataVolume.Unit('TiB', 'Tebibyte', Decimal(2) ** 40 * BYTE)

BIT = DataVolume.Unit('b', 'Bit', Fraction(1, 8) * BYTE)
KILOBIT = DataVolume.Unit('kb', 'Kilobit', Decimal(10) ** 3 * BIT)
MEGABIT = DataVolume.Unit('Mb', 'Megabit', Decimal(10) ** 6 * BIT)
GIGABIT = DataVolume.Unit('Gb', 'Gigabit', Decimal(10) ** 9 * BIT)
TERABIT = DataVolume.Unit('Tb', 'Terabit', Decimal(10) ** 12 * BIT)
KIBIBIT = DataVolume.Unit('Kib', 'Kibibit', Decimal(2) ** 10 * BIT)
MEBIBIT = DataVolume.Unit('Mib', 'Mebibit', Decimal(2) ** 20 * BIT)
GIBIBIT = DataVolume.Unit('Gib', 'Gibibit', Decimal(2) ** 30 * BIT)
TEBIBIT = DataVolume.Unit('Tib', 'Tebibit', Decimal(2) ** 40 * BIT)


class DataThroughput(Quantity):
    defineAs = DataVolume / Duration
    refUnitName = 'Byte per Second'

BYTE_PER_SECOND = DataThroughput.refUnit

KILOBYTE_PER_SECOND = DataThroughput.Unit('kB/s', 'Kilobyte per Second',
                                          Decimal(10) ** 3 * BYTE_PER_SECOND)
MEGABYTE_PER_SECOND = DataThroughput.Unit('MB/s', 'Megabyte per Second',
                                          Decimal(10) ** 6 * BYTE_PER_SECOND)
GIGABYTE_PER_SECOND = DataThroughput.Unit('GB/s', 'Gigabyte per Second',
                                          Decimal(10) ** 9 * BYTE_PER_SECOND)
TERABYTE_PER_SECOND = DataThroughput.Unit('TB/s', 'Terabyte per Second',
                                          Decimal(10) ** 12 * BYTE_PER_SECOND)
KIBIBYTE_PER_SECOND = DataThroughput.Unit('KiB/s', 'Kibibyte per Second',
                                          Decimal(2) ** 10 * BYTE_PER_SECOND)
MEBIBYTE_PER_SECOND = DataThroughput.Unit('MiB/s', 'Mebibyte per Second',
                                          Decimal(2) ** 20 * BYTE_PER_SECOND)
GIBIBYTE_PER_SECOND = DataThroughput.Unit('GiB/s', 'Gibibyte per Second',
                                          Decimal(2) ** 30 * BYTE_PER_SECOND)
TEBIBYTE_PER_SECOND = DataThroughput.Unit('TiB/s', 'Tebibyte per Second',
                                          Decimal(2) ** 40 * BYTE_PER_SECOND)

BIT_PER_SECOND = DataThroughput.Unit('b/s', 'Bit per Second', BIT / SECOND)
KILOBIT_PER_SECOND = DataThroughput.Unit('kb/s', 'Kilobit per Second',
                                         Decimal(10) ** 3 * BIT_PER_SECOND)
MEGABIT_PER_SECOND = DataThroughput.Unit('Mb/s', 'Megabit per Second',
                                         Decimal(10) ** 6 * BIT_PER_SECOND)
GIGABIT_PER_SECOND = DataThroughput.Unit('Gb/s', 'Gigabit per Second',
                                         Decimal(10) ** 9 * BIT_PER_SECOND)
TERABIT_PER_SECOND = DataThroughput.Unit('Tb/s', 'Terabit per Second',
                                         Decimal(10) ** 12 * BIT_PER_SECOND)
KIBIBIT_PER_SECOND = DataThroughput.Unit('Kib/s', 'Kibibit per Second',
                                         Decimal(2) ** 10 * BIT_PER_SECOND)
MEBIBIT_PER_SECOND = DataThroughput.Unit('Mib/s', 'Mebibit per Second',
                                         Decimal(2) ** 20 * BIT_PER_SECOND)
GIBIBIT_PER_SECOND = DataThroughput.Unit('Gib/s', 'Gibibit per Second',
                                         Decimal(2) ** 30 * BIT_PER_SECOND)
TEBIBIT_PER_SECOND = DataThroughput.Unit('Tib/s', 'Tebibit per Second',
                                         Decimal(2) ** 40 * BIT_PER_SECOND)


class Temperature(Quantity):
    pass

CELSIUS = Temperature.Unit('°C', 'Degree Celsius')
FAHRENHEIT = Temperature.Unit('°F', 'Degree Fahrenheit')
KELVIN = Temperature.Unit('K', 'Kelvin')

# Temperature converter
_tempConv = [
    (CELSIUS, FAHRENHEIT, Fraction(9, 5), Decimal(32)),
    (FAHRENHEIT, CELSIUS, Fraction(5, 9), Fraction(-160, 9)),
    (CELSIUS, KELVIN, Decimal(1), Decimal('273.15')),
    (KELVIN, CELSIUS, Decimal(1), Decimal('-273.15')),
    (FAHRENHEIT, KELVIN, Fraction(5, 9), Fraction(45967, 180)),
    (KELVIN, FAHRENHEIT, Fraction(9, 5), Decimal('-459.67')),
]
Temperature.Unit.registerConverter(TableConverter(_tempConv))
