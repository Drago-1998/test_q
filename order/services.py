import decimal
import xml.etree.ElementTree as ET

import requests


def get_currency(currency_id):
    req = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
    currencies = ET.fromstring(req.content)
    for currency in currencies:
        c_id = currency.attrib['ID']
        if currency.attrib['ID'] == currency_id:
            return decimal.Decimal(currency[4].text.replace(',', '.'))
