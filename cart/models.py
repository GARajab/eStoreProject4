from django.db import models
from store.models import Product
from decimal import Decimal


class Cart(models.Model):
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


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return Decimal(self.price) * self.quantity
