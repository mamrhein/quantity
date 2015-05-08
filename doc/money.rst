*****
Money
*****

.. automodule:: quantity.money

Classes
=======

.. autoclass:: Currency
    :members: isoCode, name, smallestFraction

.. autoclass:: Money
    :members: getQuantum, currency

.. autoclass:: ExchangeRate
    :members: unitCurrency, termCurrency, rate, inverseRate, quotation,
        inverseQuotation, inverted, __hash__, __eq__, __mul__, __div__,
        __rdiv__

Functions
=========

.. autofunction:: getCurrencyInfo
.. autofunction:: registerCurrency
