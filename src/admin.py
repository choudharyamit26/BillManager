from django.contrib import admin
from .models import Product, Bill, Client, OrderItem

admin.site.register(Product)
admin.site.register(Bill)
admin.site.register(Client)
admin.site.register(OrderItem)
