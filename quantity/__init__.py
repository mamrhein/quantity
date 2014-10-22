# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        quantity (package)
## Purpose:     Unit-safe computations with quantities.
##
## Author:      Michael Amrhein (mamrhein@users.sourceforge.net)
##
## Copyright:   (c) 2012 ff. Michael Amrhein
## License:     This program is free software; you can redistribute it and/or
##              modify it under the terms of the GNU Lesser General Public
##              License as published by the Free Software Foundation; either
##              version 2 of the License, or (at your option) any later
##              version.
##              This program is distributed in the hope that it will be
##              useful, but WITHOUT ANY WARRANTY; without even the implied
##              warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
##              PURPOSE.
##              See the GNU Lesser General Public License for more details.
##              You should have received a copy of the license text along with
##              this program; if not, get it from http://www.gnu.org/licenses,
##              or write to the Free Software Foundation, Inc.,
##              59 Temple Place, Suite 330, Boston MA 02111-1307, USA
##----------------------------------------------------------------------------
## $Source:$
## $Revision:$


"""Unit-safe computations with quantities.

============
Introduction
============

-------------------
What is a quantity?
-------------------

"The value of a quantity is generally expressed as the product of a number
and a unit. The unit is simply a particular example of the quantity concerned
which is used as a reference, and the number is the ratio of the value of the
quantity to the unit." (Bureau International des Poids et Mesures: The
International System of Units, 8th edition, 2006)
"""
#TODO: more documentation

from .quantity import Quantity, Unit
from .quantity import IncompatibleUnitsError, UndefinedResultError

__all__ = ['Quantity',
           'Unit',
           'IncompatibleUnitsError',
           'UndefinedResultError']
