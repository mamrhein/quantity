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


"""Define commonly used quantities."""

#TODO: add more units

from __future__ import absolute_import, division, unicode_literals
from decimal import Decimal
from .quantity import Quantity


__version__ = 0, 0, 1

__metaclass__ = type


class Length(Quantity):
    refUnitName = 'Meter'
    refUnitSymbol = 'm'

METER = Length.refUnit
CENTIMETER = Length.Unit('cm', 'Centimeter', Decimal('0.01') * METER)
MILLIMETER = Length.Unit('mm', 'Millimeter', Decimal('0.001') * METER)
KILOMETER = Length.Unit('km', 'Kilometer', Decimal(1000) * METER)

# some imperial units
INCH = Length.Unit('in', 'Inch', Decimal('2.54') * CENTIMETER)
FOOT = Length.Unit('ft', 'Foot', Decimal(12) * INCH)
YARD = Length.Unit('yd', 'Inch', Decimal(3) * FOOT)


class Mass(Quantity):
    refUnitName = 'Kilogram'
    refUnitSymbol = 'kg'

KILOGRAM = Mass.refUnit


class Duration(Quantity):
    refUnitName = 'Second'
    refUnitSymbol = 's'

SECOND = Duration.refUnit
MINUTE = Duration.Unit('min', 'Minute', Decimal(60) * SECOND)
HOUR = Duration.Unit('h', 'Hour', Decimal(60) * MINUTE)
DAY = Duration.Unit('d', 'Day', Decimal(24) * HOUR)


class Area(Quantity):
    defineAs = Length ** 2
    refUnitName = 'Square Meter'

SQUARE_METER = Area.refUnit


class Volume(Quantity):
    defineAs = Length ** 3
    refUnitName = 'Cubic Meter'

CUBIC_METER = Volume.refUnit


class Velocity(Quantity):
    defineAs = Length / Duration
    refUnitName = 'Meter per Second'

METER_PER_SECOND = Velocity.refUnit
KILOMETER_PER_HOUR = Velocity.Unit('', 'Kilometer per hour', KILOMETER / HOUR)


class Acceleration(Quantity):
    defineAs = Length / Duration ** 2
    refUnitName = 'Meter per Second squared'

METER_PER_SECOND_SQUARED = Acceleration.refUnit


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


class DataVolume(Quantity):
    refUnitName = 'Byte'
    refUnitSymbol = 'B'

BYTE = DataVolume.refUnit


class DataThroughput(Quantity):
    defineAs = DataVolume / Duration
    refUnitName = 'Bytes per Second'

BYTES_PER_SECOND = DataThroughput.refUnit


class Temperature(Quantity):
    pass

CELSIUS = Temperature.Unit('°C', 'Degree Celsius')
KELVIN = Temperature.Unit('°K', 'Degree Kelvin')
FAHRENHEIT = Temperature.Unit('°F', 'Degree Fahrenheit')

#TODO: provide converter for Temperature
