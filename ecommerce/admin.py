from django.contrib import admin
from parler.admin import TranslatableAdmin
from ecommerce.models import Order, OrderItem, Promocode

# Register your models here.

admin.site.register(Promocode)
admin.site.register(Order)
admin.site.register(OrderItem)