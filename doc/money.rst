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
        inverseQuotation, inverted


Submodules
==========

quantity.money.currencies
-------------------------

.. automodule:: quantity.money.currencies

Functions
^^^^^^^^^

.. autofunction:: getCurrencyInfo
.. autofunction:: registerCurrency
