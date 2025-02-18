from django.contrib import admin
from .models import Order, OrderItem

# Unregister the existing Order model registration if you're modifying its admin interface
admin.site.unregister(Order)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "status", "created_at")
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
