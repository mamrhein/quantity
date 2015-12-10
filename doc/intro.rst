************
Introduction
************

What is a Quantity?
===================

"The value of a quantity is generally expressed as the product of a number
and a unit. The unit is simply a particular example of the quantity concerned
which is used as a reference, and the number is the ratio of the value of the
quantity to the unit." (Bureau International des Poids et Mesures: The
International System of Units, 8th edition, 2006)

**Basic** types of quantities are defined "by convention", they do not depend on
other types of quantities, for example Length, Mass or Duration.

**Derived** types of quantities, on the opposite, are defined as products of
other types of quantities raised by some exponent.

Examples:

* Volume = Length ** 3

* Velocity = Length ** 1 * Duration ** -1

* Acceleration = Length ** 1 * Duration ** -2

* Force = Mass ** 1 * Acceleration ** 1

Each type of quantity may have one special unit which is used as a reference
for the definition of all other units, for example Metre, Kilogram and
Second. The other units are then defined by their relation to the reference
unit.

If a type of quantity is derived from types of quantities that all have a
reference unit, then the reference unit of that type is defined by a formula
that follows the formula defining the type of quantity.

Examples:

* Velocity -> Metre per Second = Metre ** 1 * Second ** -1

* Acceleration -> Metre per Second squared = Metre ** 1 * Second ** -2

* Force -> Newton = Kilogram ** 1 * Metre ** 1 * Second ** -2


"Systems of Measure"
--------------------

There may be different systems which define quantities, their units and the
relations between these units in a different way.

This is not directly supported by this module. For each type of quantity there
can be only no or exactly one reference unit. But, if you have units from
different systems for the same type of quantity, you can define these units
and provide mechanisms to convert between them (see :ref:`converters_label`).

Main Package Contents
=====================

The Basics: Quantity and Unit
-----------------------------

The essential functionality of the package :mod:`quantity` is provided by the
two classes :class:`~quantity.Quantity` and :class:`~quantity.Unit`.

A **basic** type of quantity is declared just by sub-classing
:class:`~quantity.Quantity`. A **derived** type of quantity is declared by
giving a definition based on more basic types of quantities. For details see
:ref:`defining_a_qty_label`.

Utility functions and classes
-----------------------------

In addition, the package :mod:`quantity` provides some utility functions (see
:ref:`functions_label`), base classes for defining unit converters (see
:ref:`Converter classes <converter_classes_label>`) and some specific
exceptions (see :ref:`exceptions_label`).

Commonly Used Quantities
------------------------

The module :mod:`quantity.predefined` provides definitions of commonly used
quantities and units.

A Special Quantity: Money
-------------------------

Money is a special type of quantity. Its unit type is known as currency.

Money differs from physical quantities mainly in two aspects:

* Money amounts are discrete. For each currency there is a smallest fraction
  that can not be split further.

* The relation between different currencies is not fixed, instead, it varies
  over time.

The sub-package :mod:`quantity.money` provides classes and functions dealing
with these specifics. Its main classes :class:`~quantity.money.Money`,
:class:`~quantity.money.Currency`, :class:`~quantity.money.ExchangeRate` and
the function :func:`~quantity.money.registerCurrency` can also be imported
from :mod:`quantity`.
