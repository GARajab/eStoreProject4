from django.db import models
from store.models import Product  # Import Product from your 'store' app
from decimal import Decimal
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    shipping_method = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    message_to_seller = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"
    ORDER_STATUSES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]
    status = models.CharField(
        max_length=20, choices=ORDER_STATUSES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )  # Corrected related_name
    product = models.ForeignKey(
        "store.Product", on_delete=models.CASCADE
    )  # Assuming Product is in the 'store' app
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} in Order #{self.order.id}"

    def get_total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        # Ensure the price is saved to the DB when a product is updated
        if self.pk:  # If the instance already exists
            old_quantity = OrderItem.objects.get(pk=self.pk).quantity
            if old_quantity != self.quantity:
                self.order.total_price += self.product.price * (
                    self.quantity - old_quantity
                )
                self.order.save()  # Save the updated order total
        super(OrderItem, self).save(*args, **kwargs)  # Call the "real" save() method.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add(self, product, quantity=1, override_quantity=False):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)

        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

    def clear(self):
        self.cart_items.all().delete()

    def get_sub_total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    def __len__(self):
        return sum(item.quantity for item in self.cart_items.all())

    def get_total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
