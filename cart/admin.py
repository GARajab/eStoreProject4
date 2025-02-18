from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):  # or admin.StackedInline
    model = OrderItem
    extra = 0  # Number of empty forms to display


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "status",
        "created_at",
    )  # Adjust fields as needed
    inlines = [
        OrderItemInline
    ]  # This will display OrderItems inline in the Order admin page


admin.site.register(OrderItem)
