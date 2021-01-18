# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Name:        quantities.predefined
# Purpose:     Define commonly used quantities.
#
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.TXT provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


# @formatter:off
"""The module `quantity.predefined` provides definitions of commonly used
quantities and units.

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
^^^^^^^^^^^^^^

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
# @formatter:on

# Standard library imports
from fractions import Fraction

# Third-party imports
from decimalfp import Decimal

# Local imports
from . import Quantity, TableConverter
from .si_prefixes import (
    MICRO, MILLI, CENTI, DECI, KILO, MEGA, GIGA, NANO, TERA,
    )


class Mass(Quantity, ref_unit_name='Kilogram', ref_unit_symbol='kg'):
    """Mass: measure of a physical body's resistance to acceleration"""


assert Mass.ref_unit is not None
KILOGRAM = Mass.ref_unit

GRAM = Mass.new_unit('g', 'Gram', MILLI * KILOGRAM)
MILLIGRAM = Mass.new_unit('mg', 'Milligram', MILLI * GRAM)
TONNE = Mass.new_unit('t', 'Tonne', MEGA * GRAM)

# some imperial units
POUND = Mass.new_unit('lb', 'Pound', Decimal('0.45359237') * KILOGRAM)
STONE = Mass.new_unit('st', 'Stone', Decimal(14) * POUND)
OUNCE = Mass.new_unit('oz', 'Ounce', Decimal('0.0625') * POUND)

# others
CARAT = Mass.new_unit('ct', 'Carat', Decimal('0.2') * GRAM)


class Length(Quantity,
             ref_unit_name='Metre',
             ref_unit_symbol='m'):
    """Length: measure of distance"""


assert Length.ref_unit is not None
METRE = Length.ref_unit

NANOMETRE = Length.new_unit('nm', 'Nanometre', NANO * METRE)
MICROMETRE = Length.new_unit('µm', 'Micrometre', MICRO * METRE)
MILLIMETRE = Length.new_unit('mm', 'Millimetre', MILLI * METRE)
CENTIMETRE = Length.new_unit('cm', 'Centimetre', CENTI * METRE)
DECIMETRE = Length.new_unit('dm', 'Decimetre', DECI * METRE)
KILOMETRE = Length.new_unit('km', 'Kilometre', KILO * METRE)

# some imperial units
INCH = Length.new_unit('in', 'Inch', Decimal('2.54') * CENTIMETRE)
FOOT = Length.new_unit('ft', 'Foot', Decimal(12) * INCH)
YARD = Length.new_unit('yd', 'Yard', Decimal(3) * FOOT)
CHAIN = Length.new_unit('ch', 'Chain', Decimal(22) * YARD)
FURLONG = Length.new_unit('fur', 'Furlog', Decimal(10) * CHAIN)
MILE = Length.new_unit('mi', 'Mile', Decimal(8) * FURLONG)


class Duration(Quantity,
               ref_unit_name='Second',
               ref_unit_symbol='s'):
    """Duration: 'what a clock reads'"""


assert Duration.ref_unit is not None
SECOND = Duration.ref_unit

NANOSECOND = Duration.new_unit('ns', 'Nanosecond', NANO * SECOND)
MICROSECOND = Duration.new_unit('µs', 'Microsecond', MICRO * SECOND)
MILLISECOND = Duration.new_unit('ms', 'Millisecond', MILLI * SECOND)
MINUTE = Duration.new_unit('min', 'Minute', Decimal(60) * SECOND)
HOUR = Duration.new_unit('h', 'Hour', Decimal(60) * MINUTE)
DAY = Duration.new_unit('d', 'Day', Decimal(24) * HOUR)


class Area(Quantity,
           define_as=Length ** 2,
           ref_unit_name='Square Metre'):
    """Area = Length ** 2"""


assert Area.ref_unit is not None
SQUARE_METRE = Area.ref_unit

SQUARE_MILLIMETRE = Area.new_unit('mm²', 'Square Millimetre', MILLIMETRE ** 2)
SQUARE_CENTIMETRE = Area.new_unit('cm²', 'Square Centimetre', CENTIMETRE ** 2)
SQUARE_DECIMETRE = Area.new_unit('dm²', 'Square Decimetre', DECIMETRE ** 2)
SQUARE_KILOMETRE = Area.new_unit('km²', 'Square Kilometre', KILOMETRE ** 2)
ARE = Area.new_unit('a', 'Are', Decimal(100) * SQUARE_METRE)
HECTARE = Area.new_unit('ha', 'Hectare', Decimal(100) * ARE)

# some imperial units
SQUARE_INCH = Area.new_unit('in²', 'Square Inch', INCH ** 2)
SQUARE_FOOT = Area.new_unit('ft²', 'Square Foot', FOOT ** 2)
SQUARE_YARD = Area.new_unit('yd²', 'Square Yard', YARD ** 2)
SQUARE_MILE = Area.new_unit('mi²', 'Square Mile', MILE ** 2)
ACRE = Area.new_unit('ac', 'Acre', Decimal(4840) * SQUARE_YARD)


class Volume(Quantity,
             define_as=Length ** 3,
             ref_unit_name='Cubic Metre'):
    """Volume = Length ** 3"""


assert Volume.ref_unit is not None
CUBIC_METRE = Volume.ref_unit

CUBIC_MILLIMETRE = Volume.new_unit('mm³', 'Cubic Millimetre', MILLIMETRE ** 3)
CUBIC_CENTIMETRE = Volume.new_unit('cm³', 'Cubic Centimetre', CENTIMETRE ** 3)
CUBIC_DECIMETRE = Volume.new_unit('dm³', 'Cubic Decimetre', DECIMETRE ** 3)
CUBIC_KILOMETRE = Volume.new_unit('km³', 'Cubic Kilometre', KILOMETRE ** 3)

# litre
LITRE = Volume.new_unit('l', 'Litre', MILLI * CUBIC_METRE)
MILLILITRE = Volume.new_unit('ml', 'Millilitre', MILLI * LITRE)
CENTILITRE = Volume.new_unit('cl', 'Centilitre', CENTI * LITRE)
DECILITRE = Volume.new_unit('dl', 'Decilitre', DECI * LITRE)

# some imperial units
CUBIC_INCH = Volume.new_unit('in³', 'Cubic Inch', INCH ** 3)
CUBIC_FOOT = Volume.new_unit('ft³', 'Cubic Foot', FOOT ** 3)
CUBIC_YARD = Volume.new_unit('yd³', 'Cubic Yard', YARD ** 3)


class Velocity(Quantity,
               define_as=Length / Duration,
               ref_unit_name='Metre per Second'):
    """Velocity = Length / Duration"""


assert Velocity.ref_unit is not None
METRE_PER_SECOND = Velocity.ref_unit
KILOMETRE_PER_HOUR = Velocity.new_unit('km/h', 'Kilometre per hour',
                                       KILOMETRE / HOUR)  # type: ignore

# some imperial units
FOOT_PER_SECOND = Velocity.new_unit('ft/s', 'Foot per Second',
                                    FOOT / SECOND)  # type: ignore
MILE_PER_HOUR = Velocity.new_unit('mph', 'Mile per Hour',
                                  MILE / HOUR)  # type: ignore


class Acceleration(Quantity,
                   define_as=Velocity / Duration,
                   ref_unit_name='Metre per Second squared'):
    """Acceleration = Velocity / Duration"""


assert Acceleration.ref_unit is not None
METRE_PER_SECOND_SQUARED = Acceleration.ref_unit

# some imperial units
MILE_PER_SECOND_SQUARED = Acceleration.new_unit(
    'mps²', 'Mile per Second squared',
    (MILE / SECOND) / SECOND)  # type: ignore


class Force(Quantity,
            define_as=Mass * Acceleration,
            ref_unit_name='Newton',
            ref_unit_symbol='N'):
    """Force = Mass * Acceleration"""


assert Force.ref_unit is not None
NEWTON = Force.ref_unit


class Energy(Quantity,
             define_as=Force * Length,
             ref_unit_name='Joule',
             ref_unit_symbol='J'):
    """Energy = Force * Length"""


assert Energy.ref_unit is not None
JOULE = Energy.ref_unit


class Power(Quantity,
            define_as=Energy / Duration,
            ref_unit_name='Watt',
            ref_unit_symbol='W'):
    """Power = Energy / Duration"""


assert Power.ref_unit is not None
WATT = Power.ref_unit

MILLIWATT = Power.new_unit('mW', 'Milliwatt', MILLI * WATT)
KILOWATT = Power.new_unit('kW', 'Kilowatt', KILO * WATT)
MEGAWATT = Power.new_unit('MW', 'Megawatt', MEGA * WATT)
GIGAWATT = Power.new_unit('GW', 'Gigawatt', GIGA * WATT)
TERAWATT = Power.new_unit('TW', 'Terawatt', TERA * WATT)


class Frequency(Quantity,
                define_as=Duration ** -1,
                ref_unit_name='Hertz',
                ref_unit_symbol='Hz'):
    """Frequency = 1 / Duration"""


assert Frequency.ref_unit is not None
HERTZ = Frequency.ref_unit

KILOHERTZ = Frequency.new_unit('kHz', 'Kilohertz', KILO * HERTZ)
MEGAHERTZ = Frequency.new_unit('MHz', 'Megahertz', MEGA * HERTZ)
GIGAHERTZ = Frequency.new_unit('GHz', 'Gigahertz', GIGA * HERTZ)

# some more unit definitions based on others than the reference units

# Force
JOULE_PER_METRE = Force.new_unit('J/m', 'Joule per Metre',
                                 JOULE / METRE)  # type: ignore

# Energy
WATT_SECOND = Energy.new_unit('Ws', 'Watt Second',
                              WATT * SECOND)  # type: ignore
KILOWATT_HOUR = Energy.new_unit('kWh', 'Kilowatt Hour',
                                KILOWATT * HOUR)  # type: ignore


class DataVolume(Quantity,
                 ref_unit_name='Byte',
                 ref_unit_symbol='B',
                 quantum=Fraction(1, 8)):
    """DataVolume according to IEEE 1541-2002"""


assert DataVolume.ref_unit is not None
BYTE = DataVolume.ref_unit

KILOBYTE = DataVolume.new_unit('kB', 'Kilobyte', KILO * BYTE)
MEGABYTE = DataVolume.new_unit('MB', 'Megabyte', MEGA * BYTE)
GIGABYTE = DataVolume.new_unit('GB', 'Gigabyte', GIGA * BYTE)
TERABYTE = DataVolume.new_unit('TB', 'Terabyte', TERA * BYTE)
KIBIBYTE = DataVolume.new_unit('KiB', 'Kibibyte', Decimal(2) ** 10 * BYTE)
MEBIBYTE = DataVolume.new_unit('MiB', 'Mebibyte', Decimal(2) ** 20 * BYTE)
GIBIBYTE = DataVolume.new_unit('GiB', 'Gibibyte', Decimal(2) ** 30 * BYTE)
TEBIBYTE = DataVolume.new_unit('TiB', 'Tebibyte', Decimal(2) ** 40 * BYTE)

BIT = DataVolume.new_unit('b', 'Bit', Fraction(1, 8) * BYTE)
KILOBIT = DataVolume.new_unit('kb', 'Kilobit', KILO * BIT)
MEGABIT = DataVolume.new_unit('Mb', 'Megabit', MEGA * BIT)
GIGABIT = DataVolume.new_unit('Gb', 'Gigabit', GIGA * BIT)
TERABIT = DataVolume.new_unit('Tb', 'Terabit', TERA * BIT)
KIBIBIT = DataVolume.new_unit('Kib', 'Kibibit', Decimal(2) ** 10 * BIT)
MEBIBIT = DataVolume.new_unit('Mib', 'Mebibit', Decimal(2) ** 20 * BIT)
GIBIBIT = DataVolume.new_unit('Gib', 'Gibibit', Decimal(2) ** 30 * BIT)
TEBIBIT = DataVolume.new_unit('Tib', 'Tebibit', Decimal(2) ** 40 * BIT)


class DataThroughput(Quantity,
                     define_as=DataVolume / Duration,
                     ref_unit_name='Byte per Second'):
    """DataThroughput = DataVolume / Duration"""


assert DataThroughput.ref_unit is not None
BYTE_PER_SECOND = DataThroughput.ref_unit

KILOBYTE_PER_SECOND = DataThroughput.new_unit(
    'kB/s', 'Kilobyte per Second', KILO * BYTE_PER_SECOND)
MEGABYTE_PER_SECOND = DataThroughput.new_unit(
    'MB/s', 'Megabyte per Second', MEGA * BYTE_PER_SECOND)
GIGABYTE_PER_SECOND = DataThroughput.new_unit(
    'GB/s', 'Gigabyte per Second', GIGA * BYTE_PER_SECOND)
TERABYTE_PER_SECOND = DataThroughput.new_unit(
    'TB/s', 'Terabyte per Second', TERA * BYTE_PER_SECOND)
KIBIBYTE_PER_SECOND = DataThroughput.new_unit(
    'KiB/s', 'Kibibyte per Second', Decimal(2) ** 10 * BYTE_PER_SECOND)
MEBIBYTE_PER_SECOND = DataThroughput.new_unit(
    'MiB/s', 'Mebibyte per Second', Decimal(2) ** 20 * BYTE_PER_SECOND)
GIBIBYTE_PER_SECOND = DataThroughput.new_unit(
    'GiB/s', 'Gibibyte per Second', Decimal(2) ** 30 * BYTE_PER_SECOND)
TEBIBYTE_PER_SECOND = DataThroughput.new_unit(
    'TiB/s', 'Tebibyte per Second', Decimal(2) ** 40 * BYTE_PER_SECOND)

BIT_PER_SECOND = DataThroughput.new_unit(
    'b/s', 'Bit per Second', BIT / SECOND)  # type: ignore
KILOBIT_PER_SECOND = DataThroughput.new_unit(
    'kb/s', 'Kilobit per Second', KILO * BIT_PER_SECOND)
MEGABIT_PER_SECOND = DataThroughput.new_unit(
    'Mb/s', 'Megabit per Second', MEGA * BIT_PER_SECOND)
GIGABIT_PER_SECOND = DataThroughput.new_unit(
    'Gb/s', 'Gigabit per Second', GIGA * BIT_PER_SECOND)
TERABIT_PER_SECOND = DataThroughput.new_unit(
    'Tb/s', 'Terabit per Second', TERA * BIT_PER_SECOND)
KIBIBIT_PER_SECOND = DataThroughput.new_unit(
    'Kib/s', 'Kibibit per Second', Decimal(2) ** 10 * BIT_PER_SECOND)
MEBIBIT_PER_SECOND = DataThroughput.new_unit(
    'Mib/s', 'Mebibit per Second', Decimal(2) ** 20 * BIT_PER_SECOND)
GIBIBIT_PER_SECOND = DataThroughput.new_unit(
    'Gib/s', 'Gibibit per Second', Decimal(2) ** 30 * BIT_PER_SECOND)
TEBIBIT_PER_SECOND = DataThroughput.new_unit(
    'Tib/s', 'Tebibit per Second', Decimal(2) ** 40 * BIT_PER_SECOND)


class Temperature(Quantity):
    """Temperature: measure of thermal energy"""


CELSIUS = Temperature.new_unit('°C', 'Degree Celsius')
FAHRENHEIT = Temperature.new_unit('°F', 'Degree Fahrenheit')
KELVIN = Temperature.new_unit('K', 'Kelvin')

# Temperature converter
_tempConv = [
    (CELSIUS, FAHRENHEIT, Fraction(9, 5), Decimal(32)),
    (FAHRENHEIT, CELSIUS, Fraction(5, 9), Fraction(-160, 9)),
    (CELSIUS, KELVIN, Decimal(1), Decimal('273.15')),
    (KELVIN, CELSIUS, Decimal(1), Decimal('-273.15')),
    (FAHRENHEIT, KELVIN, Fraction(5, 9), Fraction(45967, 180)),
    (KELVIN, FAHRENHEIT, Fraction(9, 5), Decimal('-459.67')),
    ]

Temperature.register_converter(TableConverter(_tempConv))
