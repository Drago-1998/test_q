from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    article = models.CharField(verbose_name='Номер заказа', max_length=255, unique=True)
    price_usd = models.DecimalField(verbose_name='Сумма в долларах', max_digits=17, decimal_places=2)
    price_rub = models.DecimalField(verbose_name='Сумма в рублях', max_digits=17, decimal_places=2)
    delivery_time = models.DateField(verbose_name='Срок поставки')
    delivery_massage = models.BooleanField(verbose_name='Оповещение о итечение срока', default=False)

    def __str__(self):
        return self.article

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProjectSetting(SingletonModel):
    currency = models.DecimalField(verbose_name='Курс доллара', default=0, max_digits=17, decimal_places=2)

    def __str__(self):
        return str(self.currency)

    class Meta:
        verbose_name = 'Курс доллара'
        verbose_name_plural = 'Курс доллара'