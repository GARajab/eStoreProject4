from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem  # Import all models
from .models import Product  # Import the Product model
from cart.cart import Cart  # Import the Cart class
import logging
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


def cart_summary(request):
    cart = Cart(request)
    if request.method == "POST":
        try:
            order = Order.objects.create(
                user=request.user,
                total=cart.get_total_price(),
                status=Order.STATUS_PENDING,
            )
            for item in cart:
                OrderItem.objects.create(
                    product_id=item["product_id"],
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
            cart.clear()
            print("Order created:", order)
            return redirect("payment", order_id=order.id)  # Pass order.id to payment
        except Exception as e:
            print("Error creating order:", e)
            # Handle the error appropriately, possibly redirect back to the cart.
            return redirect("cart_summary")  # Or display an error message

    # GET request or form not submitted:
    return render(request, "cart_summary.html", {"cart": cart})


def cart_add(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        quantity = int(
            request.POST.get("quantity", 1)
        )  # Default to 1 if quantity is not provided
        product = get_object_or_404(Product, id=product_id)

        cart = Cart(request)
        cart.add(product=product, quantity=quantity)

        cart_quantity = len(cart)

        return JsonResponse(
            {
                "success": True,
                "qty": cart_quantity,
                "product_name": product.name,
                "quantity_added": quantity,
            }
        )

    return HttpResponseBadRequest("Invalid request method or missing action")


def cart_delete(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("Missing product_id")

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid product_id")

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.remove(product)
        messages.success(request, f"{product.name} has been removed from your cart.")
        # Redirect to the cart view after deletion
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    return HttpResponseBadRequest("Invalid request method or missing action")


def get_sub_total_price(self):
    return sum(item.get_total_price() for item in self.cart.values())


def cart_update(request):
    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        if not product_id or not quantity:
            messages.success(request, "Missing product_id or quantity.")
            return messages

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except (ValueError, TypeError):
            messages.success(request, "Missing product_id or quantity.")
            return messages

        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, f"Updated {product.name} quantity to {quantity}.")
        # Redirect to the cart view after update
        return redirect("cart_summary")  # Change 'cart_detail' to your actual view name

    messages.success(request, "Invalid request method or missing action")
    return messages


@login_required
def checkout(request):
    cart = Cart(request)  # Instantiate cart at the beginning
    if not cart:
        messages.error(
            request, "Your cart is empty.  Please add items before checking out."
        )
        return redirect("cart_summary")

    if request.method == "POST":
        # Log the form data
        logger.info("Form data received: %s", request.POST)

        # Extract form data (as before)
        first_name = request.POST.get("firstName")
        last_name = request.POST.get("lastName")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        shipping_method = request.POST.get("shippingMethod")
        address = request.POST.get("address")
        city = request.POST.get("city")
        house = request.POST.get("house")
        postal_code = request.POST.get("postalCode")
        zip_code = request.POST.get("zip")
        message_to_seller = request.POST.get("message")

        # Create an order
        try:
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                shipping_method=shipping_method,
                address=address,
                city=city,
                house=house,
                postal_code=postal_code,
                zip_code=zip_code,
                message_to_seller=message_to_seller,
                total_price=cart.get_total_price(),
            )
            logger.info("Order created: %s", order)

            # Create OrderItems based on the cart content
            for item in cart:
                try:
                    OrderItem.objects.create(
                        order=order,
                        product_id=item["product"].id,  # Use .id
                        quantity=item["quantity"],
                    )
                    logger.info(
                        f"OrderItem created: Product ID {item['product'].id}, Quantity {item['quantity']}"
                    )

                except Exception as item_error:
                    logger.error(
                        f"Error creating OrderItem for product ID {item.get('product_id', 'Unknown')}: {item_error}"
                    )
                    messages.error(
                        request,
                        f"An error occurred while adding product to your order. Please contact support.",
                    )  # Provide user feedback.
                    # Consider rolling back the order if an item fails.
                    # order.delete()
                    return render(request, "checkout.html", {"cart": cart})

        except Exception as e:
            logger.error("Error creating order: %s", str(e))
            messages.error(request, "An error occurred while processing your order.")
            return render(request, "checkout.html", {"cart": cart})

        # Clear the cart after the order is created
        cart.clear()  # Use cart.clear()
        logger.info("Cart cleared after order creation.")

        # Redirect to a success page or payment page
        messages.success(request, "Order placed successfully!")
        return redirect(
            "payment", order_id=order.id
        )  # Redirect to the payment page, pass order_id

    # GET request: Render the checkout form
    return render(
        request, "checkout.html", {"cart": cart}
    )  # Pass cart to template # Pass cart to template # Pass cart to template


@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payment.html", {"order": order})


@csrf_exempt
@login_required
def clear_cart(request):
    if request.method == "POST":
        # Clear the cart session
        if "cart" in request.session:
            del request.session["cart"]
            request.session.modified = True
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Cart cleared successfully!",
                    "cart_count": 0,
                }
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Cart is already empty."}, status=400
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid request method."}, status=405
        )


def order_list(request):
    if request.user.username != "Admin":
        orders = Order.objects.filter(user=request.user)
        # Display all orders
    else:
        orders = Order.objects.all()  # Filter by the user
    context = {"orders": orders}
    return render(request, "order_list.html", context)
