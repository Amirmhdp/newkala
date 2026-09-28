from django.contrib import admin

# Register your models here.
from order_module.models import Order, DetailOrder, Transaction

admin.site.register(Order)
admin.site.register(DetailOrder)
admin.site.register(Transaction)
