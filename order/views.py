from django.views.generic import TemplateView
import datetime
import decimal

from order.models import Order
from order.services import get_currency
from test_q.celery import app
from google.oauth2 import service_account
from googleapiclient.discovery import build

SPREADSHEET_ID = '1MHO3gRzWEzoG_DMJR7v4140MWaxjW4XZ4A1pX9Uc8ZA'

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        currency = get_currency('R01235')
        cred = service_account.Credentials.from_service_account_file(
            filename='test-q-357507-e92486ae209a.json'
        )
        service_sheets = build('sheets', 'v4', credentials=cred)
        sheet = service_sheets.spreadsheets()
        res = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='A:D'
        ).execute()
        orders = list(
            Order(article=_order_data[1],
                  price_usd=_order_data[2],
                  price_rub=decimal.Decimal(_order_data[2]) * currency,
                  delivery_time=datetime.datetime.strptime(_order_data[3], '%d.%m.%Y'))
            for _order_data in res['values'][1:]
        )
        return context
