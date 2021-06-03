*****
Money
*****

.. automodule:: quantity.money

Types
=====

.. autodata:: MoneyConverterT

.. autodata:: ValidityT

.. autodata:: RateSpecT


Classes
=======

.. autoclass:: Currency
    :members: iso_code, name, smallest_fraction

.. autoclass:: Money
    :show-inheritance:
    :members: currency

    .. automethod:: MoneyMeta.register_currency

    .. automethod:: MoneyMeta.new_unit

.. autoclass:: ExchangeRate
    :members:
    :special-members: __hash__, __eq__, __mul__, __truediv__, __rtruediv__

.. autoclass:: MoneyConverter
    :members:
    :special-members: __call__, __enter__, __exit__

Functions
=========

.. autofunction:: get_currency_info
