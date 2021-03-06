# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Author:      Michael Amrhein (michael@adrhinum.de)
#
# Copyright:   (c) 2021 ff. Michael Amrhein
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.txt provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source$
# $Revision$


"""Shared pytest fixtures."""

import pytest

from quantity import Quantity, QuantityMeta


# noinspection PyPep8Naming
@pytest.fixture(scope="session")
def qty_cls_without_conv() -> QuantityMeta:
    QWC = QuantityMeta("QtyWithoutConv", (Quantity,), {})
    _ = QWC.new_unit('qwc1')
    _ = QWC.new_unit('qwc2')
    _ = QuantityMeta("SquareQWC", (Quantity,), {}, define_as=QWC ** 2)
    return QWC
