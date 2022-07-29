import datetime
import decimal

import requests
from aiogram import Bot

from order.models import Order
from test_q.settings import TELEGRAM_USER_ID, BOT_TOKEN


def updating_data(imported_orders_data: dict):

    """ Сартеровка обектов и работа с ОРМ-ом """

    old_orders = {
        _order.article: _order
        for _order in Order.objects.all().in_bulk().values()
    }

    delete_articles = []                                    # Список удаляимых объектов
    update_order_objects = []                               # Список обновляемых объектов

    for _article, _order_object in old_orders.items():      # Цикл провкрки на удаление или обновление объекта
        if _article in imported_orders_data.keys():
            _order_data = imported_orders_data[_article]

            _order_object.article = _order_data['article']
            _order_object.price_usd = _order_data['price_usd']
            _order_object.price_rub = _order_data['price_rub']
            _order_object.delivery_time = _order_data['delivery_time']

            check_delivery_time(_order_object)              # Проверка заказа на срок поставки
            update_order_objects.append(_order_object)
        else:
            delete_articles.append(_article)

    create_orders = (                                       # Гниратор для создание новых обектов
        check_delivery_time(                                # Проверка заказа на срок поставки
            Order(article=_new_order_data['article'],
                  price_usd=_new_order_data['price_usd'],
                  price_rub=_new_order_data['price_rub'],
                  delivery_time=_new_order_data['delivery_time'])
        )
        for _article, _new_order_data in imported_orders_data.items()
        if _article not in old_orders.keys()
    )

    # Запросы на БД
    Order.objects.bulk_create(create_orders)
    Order.objects.bulk_update(update_order_objects,
                              fields=('price_usd', 'price_rub', 'delivery_time', 'delivery_massage'))
    Order.objects.filter(article__in=delete_articles).delete()
    return 1


def check_delivery_time(order_obj: Order) -> Order:

    """ Проверка заказа на срок поставки """

    now_date = datetime.datetime.now().date()
    if order_obj.delivery_time < now_date and not order_obj.delivery_massage:
        order_obj.delivery_massage = True
        telegram_send_massage(order_obj.article, order_obj.delivery_time, order_obj.price_usd)
    elif order_obj.delivery_time >= now_date and order_obj.delivery_massage:
        order_obj.delivery_massage = False

    return order_obj


def telegram_send_massage(article: str, delivery_time, total: decimal.Decimal):

    """ Отправка сообщений телеграм бот """

    text = f"""\tЗаказ № {article}                                      
            \tСрок поставки: {delivery_time.strftime('%d.%m.%Y')}
            \tСумма: {total} $
            """
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                  data={
                      'chat_id': TELEGRAM_USER_ID,
                      'text': text
                  })
    return 1

