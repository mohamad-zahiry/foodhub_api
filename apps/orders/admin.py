from django.contrib import admin

from .models import Order, DoneOrder, OrderItem, DoneOrderItem


admin.site.register(Order)
admin.site.register(DoneOrder)
admin.site.register(OrderItem)
admin.site.register(DoneOrderItem)
