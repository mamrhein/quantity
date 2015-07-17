# -*- coding: utf-8 -*-
##----------------------------------------------------------------------------
## Name:        currencies
## Purpose:     Provide dict of currencies based on ISO 4217
##
## Author:      Michael Amrhein (michael@adrhinum.de)
##
## Copyright:   (c) 2015 Michael Amrhein
## License:     This program is free software. You can redistribute it, use it
##              and/or modify it under the terms of the 2-clause BSD license.
##              For license details please read the file LICENSE.TXT provided
##              together with the source code.
##----------------------------------------------------------------------------
## $Source$
## $Revision$


"""Provide dict of currencies based on ISO 4217."""


from __future__ import absolute_import, unicode_literals
from . import Currency


__metaclass__ = type


published = '2014-08-15'

_currencyDict = {
    'AED': ('AED', 784, 'UAE Dirham', 2,
            ['UNITED ARAB EMIRATES']),
    'AFN': ('AFN', 971, 'Afghani', 2,
            ['AFGHANISTAN']),
    'ALL': ('ALL', 8, 'Lek', 2,
            ['ALBANIA']),
    'AMD': ('AMD', 51, 'Armenian Dram', 2,
            ['ARMENIA']),
    'ANG': ('ANG', 532, 'Netherlands Antillean Guilder', 2,
            [u'CURA\xc7AO', 'SINT MAARTEN (DUTCH PART)']),
    'AOA': ('AOA', 973, 'Kwanza', 2,
            ['ANGOLA']),
    'ARS': ('ARS', 32, 'Argentine Peso', 2,
            ['ARGENTINA']),
    'AUD': ('AUD', 36, 'Australian Dollar', 2,
            ['AUSTRALIA', 'CHRISTMAS ISLAND', 'COCOS (KEELING) ISLANDS',
             'HEARD ISLAND AND McDONALD ISLANDS', 'KIRIBATI', 'NAURU',
             'NORFOLK ISLAND', 'TUVALU']),
    'AWG': ('AWG', 533, 'Aruban Florin', 2,
            ['ARUBA']),
    'AZN': ('AZN', 944, 'Azerbaijanian Manat', 2,
            ['AZERBAIJAN']),
    'BAM': ('BAM', 977, 'Convertible Mark', 2,
            ['BOSNIA AND HERZEGOVINA']),
    'BBD': ('BBD', 52, 'Barbados Dollar', 2,
            ['BARBADOS']),
    'BDT': ('BDT', 50, 'Taka', 2,
            ['BANGLADESH']),
    'BGN': ('BGN', 975, 'Bulgarian Lev', 2,
            ['BULGARIA']),
    'BHD': ('BHD', 48, 'Bahraini Dinar', 3,
            ['BAHRAIN']),
    'BIF': ('BIF', 108, 'Burundi Franc', 0,
            ['BURUNDI']),
    'BMD': ('BMD', 60, 'Bermudian Dollar', 2,
            ['BERMUDA']),
    'BND': ('BND', 96, 'Brunei Dollar', 2,
            ['BRUNEI DARUSSALAM']),
    'BOB': ('BOB', 68, 'Boliviano', 2,
            ['BOLIVIA, PLURINATIONAL STATE OF']),
    'BOV': ('BOV', 984, 'Mvdol', 2,
            ['BOLIVIA, PLURINATIONAL STATE OF']),
    'BRL': ('BRL', 986, 'Brazilian Real', 2,
            ['BRAZIL']),
    'BSD': ('BSD', 44, 'Bahamian Dollar', 2,
            ['BAHAMAS']),
    'BTN': ('BTN', 64, 'Ngultrum', 2,
            ['BHUTAN']),
    'BWP': ('BWP', 72, 'Pula', 2,
            ['BOTSWANA']),
    'BYR': ('BYR', 974, 'Belarussian Ruble', 0,
            ['BELARUS']),
    'BZD': ('BZD', 84, 'Belize Dollar', 2,
            ['BELIZE']),
    'CAD': ('CAD', 124, 'Canadian Dollar', 2,
            ['CANADA']),
    'CDF': ('CDF', 976, 'Congolese Franc', 2,
            ['CONGO, DEMOCRATIC REPUBLIC OF THE ']),
    'CHE': ('CHE', 947, 'WIR Euro', 2,
            ['SWITZERLAND']),
    'CHF': ('CHF', 756, 'Swiss Franc', 2,
            ['LIECHTENSTEIN', 'SWITZERLAND']),
    'CHW': ('CHW', 948, 'WIR Franc', 2,
            ['SWITZERLAND']),
    'CLF': ('CLF', 990, 'Unidad de Fomento', 4,
            ['CHILE']),
    'CLP': ('CLP', 152, 'Chilean Peso', 0,
            ['CHILE']),
    'CNY': ('CNY', 156, 'Yuan Renminbi', 2,
            ['CHINA']),
    'COP': ('COP', 170, 'Colombian Peso', 2,
            ['COLOMBIA']),
    'COU': ('COU', 970, 'Unidad de Valor Real', 2,
            ['COLOMBIA']),
    'CRC': ('CRC', 188, 'Costa Rican Colon', 2,
            ['COSTA RICA']),
    'CUC': ('CUC', 931, 'Peso Convertible', 2,
            ['CUBA']),
    'CUP': ('CUP', 192, 'Cuban Peso', 2,
            ['CUBA']),
    'CVE': ('CVE', 132, 'Cabo Verde Escudo', 2,
            ['CABO VERDE']),
    'CZK': ('CZK', 203, 'Czech Koruna', 2,
            ['CZECH REPUBLIC']),
    'DJF': ('DJF', 262, 'Djibouti Franc', 0,
            ['DJIBOUTI']),
    'DKK': ('DKK', 208, 'Danish Krone', 2,
            ['DENMARK', 'FAROE ISLANDS', 'GREENLAND']),
    'DOP': ('DOP', 214, 'Dominican Peso', 2,
            ['DOMINICAN REPUBLIC']),
    'DZD': ('DZD', 12, 'Algerian Dinar', 2,
            ['ALGERIA']),
    'EGP': ('EGP', 818, 'Egyptian Pound', 2,
            ['EGYPT']),
    'ERN': ('ERN', 232, 'Nakfa', 2,
            ['ERITREA']),
    'ETB': ('ETB', 230, 'Ethiopian Birr', 2,
            ['ETHIOPIA']),
    'EUR': ('EUR', 978, 'Euro', 2,
            ['ANDORRA', 'AUSTRIA', 'BELGIUM', 'CYPRUS', 'ESTONIA',
             'EUROPEAN UNION', 'FINLAND', 'FRANCE', 'FRENCH GUIANA',
             'FRENCH SOUTHERN TERRITORIES', 'GERMANY', 'GREECE', 'GUADELOUPE',
             'HOLY SEE (VATICAN CITY STATE)', 'IRELAND', 'ITALY', 'LATVIA',
             'LUXEMBOURG', 'MALTA', 'MARTINIQUE', 'MAYOTTE', 'MONACO',
             'MONTENEGRO', 'NETHERLANDS', 'PORTUGAL', u'R\xc9UNION',
             u'SAINT BARTH\xc9LEMY', 'SAINT MARTIN (FRENCH PART)',
             'SAINT PIERRE AND MIQUELON', 'SAN MARINO', 'SLOVAKIA',
             'SLOVENIA', 'SPAIN', u'\xc5LAND ISLANDS']),
    'FJD': ('FJD', 242, 'Fiji Dollar', 2,
            ['FIJI']),
    'FKP': ('FKP', 238, 'Falkland Islands Pound', 2,
            ['FALKLAND ISLANDS (MALVINAS)']),
    'GBP': ('GBP', 826, 'Pound Sterling', 2,
            ['GUERNSEY', 'ISLE OF MAN', 'JERSEY', 'UNITED KINGDOM']),
    'GEL': ('GEL', 981, 'Lari', 2,
            ['GEORGIA']),
    'GHS': ('GHS', 936, 'Ghana Cedi', 2,
            ['GHANA']),
    'GIP': ('GIP', 292, 'Gibraltar Pound', 2,
            ['GIBRALTAR']),
    'GMD': ('GMD', 270, 'Dalasi', 2,
            ['GAMBIA']),
    'GNF': ('GNF', 324, 'Guinea Franc', 0,
            ['GUINEA']),
    'GTQ': ('GTQ', 320, 'Quetzal', 2,
            ['GUATEMALA']),
    'GYD': ('GYD', 328, 'Guyana Dollar', 2,
            ['GUYANA']),
    'HKD': ('HKD', 344, 'Hong Kong Dollar', 2,
            ['HONG KONG']),
    'HNL': ('HNL', 340, 'Lempira', 2,
            ['HONDURAS']),
    'HRK': ('HRK', 191, 'Croatian Kuna', 2,
            ['CROATIA']),
    'HTG': ('HTG', 332, 'Gourde', 2,
            ['HAITI']),
    'HUF': ('HUF', 348, 'Forint', 2,
            ['HUNGARY']),
    'IDR': ('IDR', 360, 'Rupiah', 2,
            ['INDONESIA']),
    'ILS': ('ILS', 376, 'New Israeli Sheqel', 2,
            ['ISRAEL']),
    'INR': ('INR', 356, 'Indian Rupee', 2,
            ['BHUTAN', 'INDIA']),
    'IQD': ('IQD', 368, 'Iraqi Dinar', 3,
            ['IRAQ']),
    'IRR': ('IRR', 364, 'Iranian Rial', 2,
            ['IRAN, ISLAMIC REPUBLIC OF']),
    'ISK': ('ISK', 352, 'Iceland Krona', 0,
            ['ICELAND']),
    'JMD': ('JMD', 388, 'Jamaican Dollar', 2,
            ['JAMAICA']),
    'JOD': ('JOD', 400, 'Jordanian Dinar', 3,
            ['JORDAN']),
    'JPY': ('JPY', 392, 'Yen', 0,
            ['JAPAN']),
    'KES': ('KES', 404, 'Kenyan Shilling', 2,
            ['KENYA']),
    'KGS': ('KGS', 417, 'Som', 2,
            ['KYRGYZSTAN']),
    'KHR': ('KHR', 116, 'Riel', 2,
            ['CAMBODIA']),
    'KMF': ('KMF', 174, 'Comoro Franc', 0,
            ['COMOROS']),
    'KPW': ('KPW', 408, 'North Korean Won', 2,
            [u'KOREA, DEMOCRATIC PEOPLE\u2019S REPUBLIC OF']),
    'KRW': ('KRW', 410, 'Won', 0,
            ['KOREA, REPUBLIC OF']),
    'KWD': ('KWD', 414, 'Kuwaiti Dinar', 3,
            ['KUWAIT']),
    'KYD': ('KYD', 136, 'Cayman Islands Dollar', 2,
            ['CAYMAN ISLANDS']),
    'KZT': ('KZT', 398, 'Tenge', 2,
            ['KAZAKHSTAN']),
    'LAK': ('LAK', 418, 'Kip', 2,
            [u'LAO PEOPLE\u2019S DEMOCRATIC REPUBLIC']),
    'LBP': ('LBP', 422, 'Lebanese Pound', 2,
            ['LEBANON']),
    'LKR': ('LKR', 144, 'Sri Lanka Rupee', 2,
            ['SRI LANKA']),
    'LRD': ('LRD', 430, 'Liberian Dollar', 2,
            ['LIBERIA']),
    'LSL': ('LSL', 426, 'Loti', 2,
            ['LESOTHO']),
    'LTL': ('LTL', 440, 'Lithuanian Litas', 2,
            ['LITHUANIA']),
    'LYD': ('LYD', 434, 'Libyan Dinar', 3,
            ['LIBYA']),
    'MAD': ('MAD', 504, 'Moroccan Dirham', 2,
            ['MOROCCO', 'WESTERN SAHARA']),
    'MDL': ('MDL', 498, 'Moldovan Leu', 2,
            ['MOLDOVA, REPUBLIC OF']),
    'MGA': ('MGA', 969, 'Malagasy Ariary', 2,
            ['MADAGASCAR']),
    'MKD': ('MKD', 807, 'Denar', 2,
            ['MACEDONIA, THE FORMER \nYUGOSLAV REPUBLIC OF']),
    'MMK': ('MMK', 104, 'Kyat', 2,
            ['MYANMAR']),
    'MNT': ('MNT', 496, 'Tugrik', 2,
            ['MONGOLIA']),
    'MOP': ('MOP', 446, 'Pataca', 2,
            ['MACAO']),
    'MRO': ('MRO', 478, 'Ouguiya', 2,
            ['MAURITANIA']),
    'MUR': ('MUR', 480, 'Mauritius Rupee', 2,
            ['MAURITIUS']),
    'MVR': ('MVR', 462, 'Rufiyaa', 2,
            ['MALDIVES']),
    'MWK': ('MWK', 454, 'Kwacha', 2,
            ['MALAWI']),
    'MXN': ('MXN', 484, 'Mexican Peso', 2,
            ['MEXICO']),
    'MXV': ('MXV', 979, 'Mexican Unidad de Inversion (UDI)', 2,
            ['MEXICO']),
    'MYR': ('MYR', 458, 'Malaysian Ringgit', 2,
            ['MALAYSIA']),
    'MZN': ('MZN', 943, 'Mozambique Metical', 2,
            ['MOZAMBIQUE']),
    'NAD': ('NAD', 516, 'Namibia Dollar', 2,
            ['NAMIBIA']),
    'NGN': ('NGN', 566, 'Naira', 2,
            ['NIGERIA']),
    'NIO': ('NIO', 558, 'Cordoba Oro', 2,
            ['NICARAGUA']),
    'NOK': ('NOK', 578, 'Norwegian Krone', 2,
            ['BOUVET ISLAND', 'NORWAY', 'SVALBARD AND JAN MAYEN']),
    'NPR': ('NPR', 524, 'Nepalese Rupee', 2,
            ['NEPAL']),
    'NZD': ('NZD', 554, 'New Zealand Dollar', 2,
            ['COOK ISLANDS', 'NEW ZEALAND', 'NIUE', 'PITCAIRN', 'TOKELAU']),
    'OMR': ('OMR', 512, 'Rial Omani', 3,
            ['OMAN']),
    'PAB': ('PAB', 590, 'Balboa', 2,
            ['PANAMA']),
    'PEN': ('PEN', 604, 'Nuevo Sol', 2,
            ['PERU']),
    'PGK': ('PGK', 598, 'Kina', 2,
            ['PAPUA NEW GUINEA']),
    'PHP': ('PHP', 608, 'Philippine Peso', 2,
            ['PHILIPPINES']),
    'PKR': ('PKR', 586, 'Pakistan Rupee', 2,
            ['PAKISTAN']),
    'PLN': ('PLN', 985, 'Zloty', 2,
            ['POLAND']),
    'PYG': ('PYG', 600, 'Guarani', 0,
            ['PARAGUAY']),
    'QAR': ('QAR', 634, 'Qatari Rial', 2,
            ['QATAR']),
    'RON': ('RON', 946, 'New Romanian Leu', 2,
            ['ROMANIA']),
    'RSD': ('RSD', 941, 'Serbian Dinar', 2,
            ['SERBIA']),
    'RUB': ('RUB', 643, 'Russian Ruble', 2,
            ['RUSSIAN FEDERATION']),
    'RWF': ('RWF', 646, 'Rwanda Franc', 0,
            ['RWANDA']),
    'SAR': ('SAR', 682, 'Saudi Riyal', 2,
            ['SAUDI ARABIA']),
    'SBD': ('SBD', 90, 'Solomon Islands Dollar', 2,
            ['SOLOMON ISLANDS']),
    'SCR': ('SCR', 690, 'Seychelles Rupee', 2,
            ['SEYCHELLES']),
    'SDG': ('SDG', 938, 'Sudanese Pound', 2,
            ['SUDAN']),
    'SEK': ('SEK', 752, 'Swedish Krona', 2,
            ['SWEDEN']),
    'SGD': ('SGD', 702, 'Singapore Dollar', 2,
            ['SINGAPORE']),
    'SHP': ('SHP', 654, 'Saint Helena Pound', 2,
            ['SAINT HELENA, ASCENSION AND \nTRISTAN DA CUNHA']),
    'SLL': ('SLL', 694, 'Leone', 2,
            ['SIERRA LEONE']),
    'SOS': ('SOS', 706, 'Somali Shilling', 2,
            ['SOMALIA']),
    'SRD': ('SRD', 968, 'Surinam Dollar', 2,
            ['SURINAME']),
    'SSP': ('SSP', 728, 'South Sudanese Pound', 2,
            ['SOUTH SUDAN']),
    'STD': ('STD', 678, 'Dobra', 2,
            ['SAO TOME AND PRINCIPE']),
    'SVC': ('SVC', 222, 'El Salvador Colon', 2,
            ['EL SALVADOR']),
    'SYP': ('SYP', 760, 'Syrian Pound', 2,
            ['SYRIAN ARAB REPUBLIC']),
    'SZL': ('SZL', 748, 'Lilangeni', 2,
            ['SWAZILAND']),
    'THB': ('THB', 764, 'Baht', 2,
            ['THAILAND']),
    'TJS': ('TJS', 972, 'Somoni', 2,
            ['TAJIKISTAN']),
    'TMT': ('TMT', 934, 'Turkmenistan New Manat', 2,
            ['TURKMENISTAN']),
    'TND': ('TND', 788, 'Tunisian Dinar', 3,
            ['TUNISIA']),
    'TOP': ('TOP', 776, 'Pa’anga', 2,
            ['TONGA']),
    'TRY': ('TRY', 949, 'Turkish Lira', 2,
            ['TURKEY']),
    'TTD': ('TTD', 780, 'Trinidad and Tobago Dollar', 2,
            ['TRINIDAD AND TOBAGO']),
    'TWD': ('TWD', 901, 'New Taiwan Dollar', 2,
            ['TAIWAN, PROVINCE OF CHINA']),
    'TZS': ('TZS', 834, 'Tanzanian Shilling', 2,
            ['TANZANIA, UNITED REPUBLIC OF']),
    'UAH': ('UAH', 980, 'Hryvnia', 2,
            ['UKRAINE']),
    'UGX': ('UGX', 800, 'Uganda Shilling', 0,
            ['UGANDA']),
    'USD': ('USD', 840, 'US Dollar', 2,
            ['AMERICAN SAMOA', 'BONAIRE, SINT EUSTATIUS AND SABA',
             'BRITISH INDIAN OCEAN TERRITORY', 'ECUADOR', 'EL SALVADOR',
             'GUAM', 'HAITI', 'MARSHALL ISLANDS',
             'MICRONESIA, FEDERATED STATES OF', 'NORTHERN MARIANA ISLANDS',
             'PALAU', 'PANAMA', 'PUERTO RICO', 'TIMOR-LESTE',
             'TURKS AND CAICOS ISLANDS', 'UNITED STATES',
             'UNITED STATES MINOR OUTLYING ISLANDS',
             'VIRGIN ISLANDS (BRITISH)', 'VIRGIN ISLANDS (U.S.)']),
    'USN': ('USN', 997, 'US Dollar (Next day)', 2,
            ['UNITED STATES']),
    'UYI': ('UYI', 940, 'Uruguay Peso en Unidades Indexadas (URUIURUI)', 0,
            ['URUGUAY']),
    'UYU': ('UYU', 858, 'Peso Uruguayo', 2,
            ['URUGUAY']),
    'UZS': ('UZS', 860, 'Uzbekistan Sum', 2,
            ['UZBEKISTAN']),
    'VEF': ('VEF', 937, 'Bolivar', 2,
            ['VENEZUELA, BOLIVARIAN REPUBLIC OF']),
    'VND': ('VND', 704, 'Dong', 0,
            ['VIET NAM']),
    'VUV': ('VUV', 548, 'Vatu', 0,
            ['VANUATU']),
    'WST': ('WST', 882, 'Tala', 2,
            ['SAMOA']),
    'XAF': ('XAF', 950, 'CFA Franc BEAC', 0,
            ['CAMEROON', 'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'CONGO',
             'EQUATORIAL GUINEA', 'GABON']),
    'XCD': ('XCD', 951, 'East Caribbean Dollar', 2,
            ['ANGUILLA', 'ANTIGUA AND BARBUDA', 'DOMINICA', 'GRENADA',
             'MONTSERRAT', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA',
             'SAINT VINCENT AND THE GRENADINES']),
    'XOF': ('XOF', 952, 'CFA Franc BCEAO', 0,
            ['BENIN', 'BURKINA FASO', u"C\xd4TE D'IVOIRE", 'GUINEA-BISSAU',
             'MALI', 'NIGER', 'SENEGAL', 'TOGO']),
    'XPF': ('XPF', 953, 'CFP Franc', 0,
            ['FRENCH POLYNESIA', 'NEW CALEDONIA', 'WALLIS AND FUTUNA']),
    'YER': ('YER', 886, 'Yemeni Rial', 2,
            ['YEMEN']),
    'ZAR': ('ZAR', 710, 'Rand', 2,
            ['LESOTHO', 'NAMIBIA', 'SOUTH AFRICA']),
    'ZMW': ('ZMW', 967, 'Zambian Kwacha', 2,
            ['ZAMBIA']),
    'ZWL': ('ZWL', 932, 'Zimbabwe Dollar', 2,
            ['ZIMBABWE']),
}


def getCurrencyInfo(isoCode):
    """Return infos from ISO 4217 currency database.

    Args:
        isoCode (string): ISO 4217 3-character code for the currency to be
            looked-up

    Returns:
        tuple: 3-character code, numerical code, name, minorUnit and list of
            countries which use the currency as functional currency

    Raises:
        ValueError: currency with code `isoCode` not in database

    .. note::
        The database available here does only include entries from ISO 4217
        which are used as functional currency, not those used for bond
        markets, noble metals and testing purposes.
    """
    try:        # transform to unicode
        isoCode = isoCode.decode()
    except (AttributeError, UnicodeEncodeError):
        pass
    try:
        return _currencyDict[isoCode]
    except KeyError:
        raise ValueError("Unknown ISO 4217 code: '%s'." % isoCode)


def registerCurrency(isoCode):
    """Register the currency with code `isoCode` from ISO 4217 database.

    Args:
        isoCode (string): ISO 4217 3-character code for the currency to be
            registered

    Returns:
        :class:`Currency`: registered currency

    Raises:
        ValueError: currency with code `isoCode` not in database
    """
    regCurrency = Currency.getUnitBySymbol(isoCode)
    if regCurrency is not None:         # currency already registered
        return regCurrency
    isoCode, isoNumCode, name, minorUnit, countries = getCurrencyInfo(isoCode)
    return Currency(isoCode, name, minorUnit)
