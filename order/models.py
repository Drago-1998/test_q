from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.CharField(verbose_name='Номер заказа', max_length=255, unique=True)
    price_usd = models.DecimalField(verbose_name='Сумма в долларах', max_digits=17, decimal_places=2)
    price_rub = models.DecimalField(verbose_name='Сумма в рублях', max_digits=17, decimal_places=2)
    delivery_time = models.DateField(verbose_name='Срок поставки')

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

