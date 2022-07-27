from django.contrib import admin

# Register your models here.
from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'id', 'article', 'price_usd', 'price_rub', 'delivery_time'
