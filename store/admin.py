from django.contrib import admin
from .models import Category, Customer, Product
from cart.models import Order

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
