import datetime
import decimal

from order.logic import updating_data
from order.models import ProjectSetting
from order.services import get_currency
from test_q.celery import app
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '1MHO3gRzWEzoG_DMJR7v4140MWaxjW4XZ4A1pX9Uc8ZA'         # Id - Google excel кинги
CURRENCY_CODE = 'R01235'                                                # Доллары


@app.task
def import_data():

    """Импортирование данных из Google Sheets книги"""

    currency = ProjectSetting.load().currency
    cred = service_account.Credentials.from_service_account_file(
        filename='test-q-357507-e92486ae209a.json'                      # Токен файл google account
    )
    service_sheets = build('sheets', 'v4', credentials=cred)
    sheet = service_sheets.spreadsheets()
    res = sheet.values().get(                                           # Получение данных от Google Sheet
        spreadsheetId=SPREADSHEET_ID,
        range='A:D'
    ).execute()

    imported_orders_data = {                                            # Преобразование данных
        _order_data[1]: {
            'article': _order_data[1],
            'price_usd': decimal.Decimal(_order_data[2]),
            'price_rub': decimal.Decimal(_order_data[2]) * currency,
            'delivery_time': datetime.datetime.strptime(_order_data[3], '%d.%m.%Y').date()
        }
        for _order_data in res['values'][1:]
    }

    updating_data(imported_orders_data)                                 # Сартеровка обектов и работа с ОРМ-ом
    return 1


@app.task
def update_currency():

    """Обновление курса волюты"""

    currency = get_currency(CURRENCY_CODE)
    ps = ProjectSetting.load()
    ps.currency = currency
    ps.save()
    return 1
