# cart.py
from decimal import Decimal

from store.models import Product  # Use Decimal for precise monetary calculations


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)  # Convert to string for session keys
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),  # Store price as a string
                "name": product.name,
                "image": str(product.image),  # Assuming you have an image field
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):  # Iterate over items in the cart
        product_ids = self.cart.keys()
        # Retrieve product objects from the database using their IDs
        products = Product.objects.filter(id__in=product_ids)  # Assuming Product model

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product  # Add the Product object
        for item in cart.values():
            item["price"] = Decimal(item["price"])  # Convert price back to Decimal
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        del self.session["cart"]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
