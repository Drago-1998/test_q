from order.models import Order


def unpacking_data(imported_orders_data: dict):

    """ Работа сартеровка обектов и работа с ОРМ-ом"""

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

            update_order_objects.append(_order_object)
        else:
            delete_articles.append(_article)

    create_orders = (                                       # Гниратор для создание новых обектов
        Order(article=_new_order_data['article'],
              price_usd=_new_order_data['price_usd'],
              price_rub=_new_order_data['price_rub'],
              delivery_time=_new_order_data['delivery_time'])
        for _article, _new_order_data in imported_orders_data.items()
        if _article not in old_orders.keys()
    )

    # Запросы на БД
    Order.objects.bulk_create(create_orders)
    Order.objects.bulk_update(update_order_objects,
                              fields=('price_usd', 'price_rub', 'delivery_time'))
    Order.objects.filter(article__in=delete_articles).delete()

    return 1
