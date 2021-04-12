# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2021 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Shared pytest fixtures."""

from typing import Tuple

import pytest

from quantity import Quantity, QuantityMeta, Unit


@pytest.fixture(scope="session")
def units_without_conv() -> Tuple[Unit, Unit]:
    _cls = QuantityMeta("QtyWithoutConv", (Quantity,), {})
    return _cls.new_unit('qwc1'), _cls.new_unit('qwc2')
