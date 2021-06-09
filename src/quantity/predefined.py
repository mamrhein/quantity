# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2012 ff. Michael Amrhein
# License:     This program is free software. You can redistribute it, use it
#              and/or modify it under the terms of the 2-clause BSD license.
#              For license details please read the file LICENSE.txt provided
#              together with the source code.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


# @formatter:off
r"""Definitions of commonly used quantities and units.

Mass
^^^^

Reference unit: Kilogram ('kg')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'kg'
====== ========================= ==================== ====================
mg     Milligram                 0.001·g              0.000001
ct     Carat                     0.2·g                0.0002
g      Gram                      0.001·kg             0.001
oz     Ounce                     0.0625·lb            0.028349523125
lb     Pound                     0.45359237·kg        0.45359237
st     Stone                     14·lb                6.35029318
t      Tonne                     1000·kg              1000
====== ========================= ==================== ====================

Length
^^^^^^

Reference unit: Metre ('m')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'm'
====== ========================= ==================== ====================
nm     Nanometre                 0.000000001·m        0.000000001
µm     Micrometre                0.000001·m           0.000001
mm     Millimetre                0.001·m              0.001
cm     Centimetre                0.01·m               0.01
in     Inch                      2.54·cm              0.0254
dm     Decimetre                 0.1·m                0.1
ft     Foot                      12·in                0.3048
yd     Yard                      3·ft                 0.9144
ch     Chain                     22·yd                20.1168
fur    Furlog                    10·ch                201.168
km     Kilometre                 1000·m               1000
mi     Mile                      8·fur                1609.344
====== ========================= ==================== ====================

Duration
^^^^^^^^

Reference unit: Second ('s')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 's'
====== ========================= ==================== ====================
ns     Nanosecond                0.000000001·s        0.000000001
µs     Microsecond               0.000001·s           0.000001
ms     Millisecond               0.001·s              0.001
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
ac     Acre                      4840·yd²             4046.8564224
ha     Hectare                   100·a                10000
km²    Square Kilometre          km²                  1000000
mi²    Square Mile               mi²                  2589988.110336
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
cm³    Cubic Centimetre          cm³                  0.000001
ml     Millilitre                0.001·l              0.000001
cl     Centilitre                0.01·l               0.00001
in³    Cubic Inch                in³                  0.000016387064
dl     Decilitre                 0.1·l                0.0001
dm³    Cubic Decimetre           dm³                  0.001
l      Litre                     0.001·m³             0.001
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
mps²   Mile per Second squared   mi/s²                1609.344
====== ========================= ==================== ====================

Force
^^^^^

Definition: Mass·Acceleration

Reference unit: Newton ('N' = 'kg·m/s²')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'N'
====== ========================= ==================== ====================
J/m    Joule per Metre           J/m                  1
====== ========================= ==================== ====================

Energy
^^^^^^

Definition: Force·Length

Reference unit: Joule ('J' = 'N·m' = 'kg·m²/s²')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'J'
====== ========================= ==================== ====================
Nm     Newton Meter              N·m                  1
Ws     Watt Second               W·s                  1
kWh    Kilowatt Hour             kW·h                 3600000
====== ========================= ==================== ====================

Power
^^^^^

Definition: Energy/Duration

Reference unit: Watt ('W' = 'J/s' = 'kg·m²/s³')

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

Frequency
^^^^^^^^^

Definition: 1/Duration

Reference unit: Hertz ('Hz' = '1/s')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'Hz'
====== ========================= ==================== ====================
kHz    Kilohertz                 1000·Hz              1000
MHz    Megahertz                 1000000·Hz           1000000
GHz    Gigahertz                 1000000000·Hz        1000000000
====== ========================= ==================== ====================

DataVolume
^^^^^^^^^^

Reference unit: Byte ('B')

Predefined units:

====== ========================= ==================== ====================
Symbol Name                      Definition           Equivalent in 'B'
====== ========================= ==================== ====================
b      Bit                       0.125·B              0.125
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
from \ to  Celsius                     Fahrenheit                  Kelvin
========== =========================== =========================== ===========================
Celsius    -                           [°F] = [°C] * 9/5 + 32      [K] = [°C] + 273.15
Fahrenheit [°C] = ([°F] - 32) * 5/9    -                           [K] = ([°F] + 459.67) * 5/9
Kelvin     [°C] = [K] - 273.15         [°F] = [K] * 9/5 - 459.67   -
========== =========================== =========================== ===========================
"""  # noqa: E501   -- does not work see flake8 issue #375
# @formatter:on

from fractions import Fraction

from decimalfp import Decimal

from . import Quantity, TableConverter
from .si_prefixes import (
    CENTI, DECI, GIGA, KILO, MEGA, MICRO, MILLI, NANO, TERA,
    )
from .term import Term


class Mass(Quantity, ref_unit_name='Kilogram', ref_unit_symbol='kg'):
    """Mass: measure of a physical body's resistance to acceleration"""


assert Mass.ref_unit is not None
KILOGRAM = Mass.ref_unit

GRAM = Mass.new_unit('g', 'Gram', MILLI * KILOGRAM)
MILLIGRAM = Mass.new_unit('mg', 'Milligram', MILLI * GRAM)
TONNE = Mass.new_unit('t', 'Tonne', KILO * KILOGRAM)

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

SQUARE_MILLIMETRE = Area.derive_unit_from(MILLIMETRE, name='Square Millimetre')
SQUARE_CENTIMETRE = Area.derive_unit_from(CENTIMETRE, name='Square Centimetre')
SQUARE_DECIMETRE = Area.derive_unit_from(DECIMETRE, name='Square Decimetre')
SQUARE_KILOMETRE = Area.derive_unit_from(KILOMETRE, name='Square Kilometre')
ARE = Area.new_unit('a', 'Are', Decimal(100) * SQUARE_METRE)
HECTARE = Area.new_unit('ha', 'Hectare', Decimal(100) * ARE)

# some imperial units
SQUARE_INCH = Area.derive_unit_from(INCH, name='Square Inch')
SQUARE_FOOT = Area.derive_unit_from(FOOT, name='Square Foot')
SQUARE_YARD = Area.derive_unit_from(YARD, name='Square Yard')
SQUARE_MILE = Area.derive_unit_from(MILE, name='Square Mile')
ACRE = Area.new_unit('ac', 'Acre', Decimal(4840) * SQUARE_YARD)


class Volume(Quantity,
             define_as=Length ** 3,
             ref_unit_name='Cubic Metre'):
    """Volume = Length ** 3"""


assert Volume.ref_unit is not None
CUBIC_METRE = Volume.ref_unit

CUBIC_MILLIMETRE = Volume.derive_unit_from(MILLIMETRE, name='Cubic Millimetre')
CUBIC_CENTIMETRE = Volume.derive_unit_from(CENTIMETRE, name='Cubic Centimetre')
CUBIC_DECIMETRE = Volume.derive_unit_from(DECIMETRE, name='Cubic Decimetre')
CUBIC_KILOMETRE = Volume.derive_unit_from(KILOMETRE, name='Cubic Kilometre')

# litre
LITRE = Volume.new_unit('l', 'Litre', MILLI * CUBIC_METRE)
MILLILITRE = Volume.new_unit('ml', 'Millilitre', MILLI * LITRE)
CENTILITRE = Volume.new_unit('cl', 'Centilitre', CENTI * LITRE)
DECILITRE = Volume.new_unit('dl', 'Decilitre', DECI * LITRE)

# some imperial units
CUBIC_INCH = Volume.derive_unit_from(INCH, name='Cubic Inch')
CUBIC_FOOT = Volume.derive_unit_from(FOOT, name='Cubic Foot')
CUBIC_YARD = Volume.derive_unit_from(YARD, name='Cubic Yard')


class Velocity(Quantity,
               define_as=Length / Duration,
               ref_unit_name='Metre per Second'):
    """Velocity = Length / Duration"""


assert Velocity.ref_unit is not None
METRE_PER_SECOND = Velocity.ref_unit
KILOMETRE_PER_HOUR = Velocity.derive_unit_from(KILOMETRE, HOUR,
                                               name='Kilometre per Hour')

# some imperial units
FOOT_PER_SECOND = Velocity.derive_unit_from(FOOT, SECOND,
                                            name='Foot per Second')
MILE_PER_HOUR = Velocity.derive_unit_from(MILE, HOUR,
                                          symbol='mph',
                                          name='Mile per Hour')


class Acceleration(Quantity,
                   define_as=Length / Duration ** 2,
                   ref_unit_name='Metre per Second squared'):
    """Acceleration = Length / Duration²"""


assert Acceleration.ref_unit is not None
METRE_PER_SECOND_SQUARED = Acceleration.ref_unit

# some imperial units
MILE_PER_SECOND_SQUARED = \
    Acceleration.derive_unit_from(MILE, SECOND,
                                  symbol='mps²',
                                  name='Mile per Second squared')


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

NEWTON_METRE = Energy.derive_unit_from(NEWTON, METRE,
                                       symbol='Nm',
                                       name='Newton Metre')


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
# noinspection PyTypeChecker
JOULE_PER_METRE = Force.new_unit('J/m', 'Joule per Metre',
                                 Term(((JOULE, 1), (METRE, -1))))

# Energy
# noinspection PyTypeChecker
WATT_SECOND = Energy.new_unit('Ws', 'Watt Second',
                              Term(((WATT, 1), (SECOND, 1))))
# noinspection PyTypeChecker

KILOWATT_HOUR = Energy.new_unit('kWh', 'Kilowatt Hour',
                                Term(((KILOWATT, 1), (HOUR, 1))))


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

BIT_PER_SECOND = DataThroughput.derive_unit_from(BIT, SECOND,
                                                 name='Bit per Second')
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
_temp_conv = [
    (CELSIUS, FAHRENHEIT, Fraction(9, 5), Decimal(32)),
    (FAHRENHEIT, CELSIUS, Fraction(5, 9), Fraction(-160, 9)),
    (CELSIUS, KELVIN, Decimal(1), Decimal('273.15')),
    (KELVIN, CELSIUS, Decimal(1), Decimal('-273.15')),
    (FAHRENHEIT, KELVIN, Fraction(5, 9), Fraction(45967, 180)),
    (KELVIN, FAHRENHEIT, Fraction(9, 5), Decimal('-459.67')),
    ]

Temperature.register_converter(TableConverter(_temp_conv))

__all__ = [
    'ACRE',
    'ARE',
    'Acceleration',
    'Area',
    'BIT',
    'BIT_PER_SECOND',
    'BYTE',
    'BYTE_PER_SECOND',
    'CARAT',
    'CELSIUS',
    'CENTILITRE',
    'CENTIMETRE',
    'CHAIN',
    'CUBIC_CENTIMETRE',
    'CUBIC_DECIMETRE',
    'CUBIC_FOOT',
    'CUBIC_INCH',
    'CUBIC_KILOMETRE',
    'CUBIC_METRE',
    'CUBIC_MILLIMETRE',
    'CUBIC_YARD',
    'DAY',
    'DECILITRE',
    'DECIMETRE',
    'DataThroughput',
    'DataVolume',
    'Duration',
    'Energy',
    'FAHRENHEIT',
    'FOOT',
    'FOOT_PER_SECOND',
    'FURLONG',
    'Force',
    'Frequency',
    'GIBIBIT',
    'GIBIBIT_PER_SECOND',
    'GIBIBYTE',
    'GIBIBYTE_PER_SECOND',
    'GIGABIT',
    'GIGABIT_PER_SECOND',
    'GIGABYTE',
    'GIGABYTE_PER_SECOND',
    'GIGAHERTZ',
    'GIGAWATT',
    'GRAM',
    'HECTARE',
    'HERTZ',
    'HOUR',
    'INCH',
    'JOULE',
    'JOULE_PER_METRE',
    'KELVIN',
    'KIBIBIT',
    'KIBIBIT_PER_SECOND',
    'KIBIBYTE',
    'KIBIBYTE_PER_SECOND',
    'KILOBIT',
    'KILOBIT_PER_SECOND',
    'KILOBYTE',
    'KILOBYTE_PER_SECOND',
    'KILOGRAM',
    'KILOHERTZ',
    'KILOMETRE',
    'KILOMETRE_PER_HOUR',
    'KILOWATT',
    'KILOWATT_HOUR',
    'LITRE',
    'Length',
    'MEBIBIT',
    'MEBIBIT_PER_SECOND',
    'MEBIBYTE',
    'MEBIBYTE_PER_SECOND',
    'MEGABIT',
    'MEGABIT_PER_SECOND',
    'MEGABYTE',
    'MEGABYTE_PER_SECOND',
    'MEGAHERTZ',
    'MEGAWATT',
    'METRE',
    'METRE_PER_SECOND',
    'METRE_PER_SECOND_SQUARED',
    'MICROMETRE',
    'MICROSECOND',
    'MILE',
    'MILE_PER_HOUR',
    'MILE_PER_SECOND_SQUARED',
    'MILLIGRAM',
    'MILLILITRE',
    'MILLIMETRE',
    'MILLISECOND',
    'MILLIWATT',
    'MINUTE',
    'Mass',
    'NANOMETRE',
    'NANOSECOND',
    'NEWTON',
    'NEWTON_METRE',
    'OUNCE',
    'POUND',
    'Power',
    'SECOND',
    'SQUARE_CENTIMETRE',
    'SQUARE_DECIMETRE',
    'SQUARE_FOOT',
    'SQUARE_INCH',
    'SQUARE_KILOMETRE',
    'SQUARE_METRE',
    'SQUARE_MILE',
    'SQUARE_MILLIMETRE',
    'SQUARE_YARD',
    'STONE',
    'TEBIBIT',
    'TEBIBIT_PER_SECOND',
    'TEBIBYTE',
    'TEBIBYTE_PER_SECOND',
    'TERABIT',
    'TERABIT_PER_SECOND',
    'TERABYTE',
    'TERABYTE_PER_SECOND',
    'TERAWATT',
    'TONNE',
    'Temperature',
    'Velocity',
    'Volume',
    'WATT',
    'WATT_SECOND',
    'YARD'
    ]
